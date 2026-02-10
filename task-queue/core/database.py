"""
Task Queue Database - SQLite Backend
"""

import sqlite3
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from .models import Task, TaskStatus, TaskPriority, TaskType

logger = logging.getLogger(__name__)


class TaskQueueDatabase:
    """SQLite database for task queue management"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or "/opt/blackbox5/task-queue/data/task_queue.db"
        self._ensure_db_directory()

    def _ensure_db_directory(self):
        """Ensure database directory exists"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def _get_connection(self):
        """Get database connection with context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()

    def initialize_schema(self):
        """Initialize database schema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Tasks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    task_type TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    command TEXT,
                    script_path TEXT,
                    working_dir TEXT,
                    environment TEXT,
                    timeout_seconds INTEGER DEFAULT 3600,
                    scheduled_at TEXT,
                    deadline_at TEXT,
                    estimated_duration_seconds INTEGER,
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    dependencies TEXT,
                    depends_on TEXT,
                    retry_count INTEGER DEFAULT 0,
                    max_retries INTEGER DEFAULT 3,
                    last_error TEXT,
                    progress TEXT,
                    result TEXT,
                    assigned_agent TEXT,
                    required_agent TEXT,
                    epic_id TEXT,
                    prd_id TEXT,
                    labels TEXT,
                    tags TEXT,
                    scribe_logged BOOLEAN DEFAULT 0,
                    scribe_doc_path TEXT,
                    created_timestamp INTEGER DEFAULT (strftime('%s', 'now')),
                    updated_timestamp INTEGER DEFAULT (strftime('%s', 'now'))
                )
            ''')

            # Task execution log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS execution_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    agent_id TEXT,
                    action TEXT NOT NULL,
                    old_status TEXT,
                    new_status TEXT,
                    message TEXT,
                    timestamp INTEGER DEFAULT (strftime('%s', 'now')),
                    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
                )
            ''')

            # Task metrics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS task_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE NOT NULL,
                    queued_duration_seconds INTEGER DEFAULT 0,
                    execution_duration_seconds INTEGER DEFAULT 0,
                    total_duration_seconds INTEGER DEFAULT 0,
                    retry_count INTEGER DEFAULT 0,
                    success BOOLEAN,
                    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
                )
            ''')

            # Agent assignments
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    assigned_at INTEGER DEFAULT (strftime('%s', 'now')),
                    status TEXT DEFAULT 'active',
                    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
                    UNIQUE(task_id, agent_id)
                )
            ''')

            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_deadline ON tasks(deadline_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_execution_log_task ON execution_log(task_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_execution_log_timestamp ON execution_log(timestamp)')

            logger.info("Database schema initialized")

    def add_task(self, task: Task) -> bool:
        """Add a task to the database"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                data = task.to_dict()
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['?'] * len(data))
                values = list(data.values())

                cursor.execute(f'''
                    INSERT INTO tasks ({columns})
                    VALUES ({placeholders})
                ''', values)

                self._log_event(task.task_id, None, 'created', None, task.status.value, 'Task created')
                logger.info(f"Task {task.task_id} added to queue")
                return True
            except sqlite3.IntegrityError:
                logger.error(f"Task {task.task_id} already exists")
                return False

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE task_id = ?', (task_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_task(row)
            return None

    def get_all_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """Get all tasks, optionally filtered by status"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute('SELECT * FROM tasks WHERE status = ?', (status.value,))
            else:
                cursor.execute('SELECT * FROM tasks ORDER BY priority DESC, created_timestamp ASC')
            return [self._row_to_task(row) for row in cursor.fetchall()]

    def get_pending_tasks(self, max_count: int = 10) -> List[Task]:
        """Get pending tasks ordered by priority and creation time"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM tasks
                WHERE status IN ('pending', 'queued', 'retrying')
                ORDER BY
                    CASE priority
                        WHEN 'critical' THEN 1
                        WHEN 'high' THEN 2
                        WHEN 'medium' THEN 3
                        WHEN 'low' THEN 4
                    END,
                    created_timestamp ASC
                LIMIT ?
            ''', (max_count,))
            return [self._row_to_task(row) for row in cursor.fetchall()]

    def get_next_task(self, agent_id: Optional[str] = None) -> Optional[Task]:
        """Get the next executable task (highest priority, ready to run)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            query = '''
                SELECT * FROM tasks
                WHERE status IN ('pending', 'queued', 'retrying')
                AND (scheduled_at IS NULL OR datetime(scheduled_at) <= datetime('now'))
                AND (required_agent IS NULL OR required_agent = ?)
                AND (deadline_at IS NULL OR datetime(deadline_at) > datetime('now'))
                ORDER BY
                    CASE priority
                        WHEN 'critical' THEN 1
                        WHEN 'high' THEN 2
                        WHEN 'medium' THEN 3
                        WHEN 'low' THEN 4
                    END,
                    created_timestamp ASC
                LIMIT 1
            '''

            cursor.execute(query, (agent_id or '',))
            row = cursor.fetchone()
            if row:
                return self._row_to_task(row)
            return None

    def update_task_status(self, task_id: str, status: TaskStatus,
                          agent_id: Optional[str] = None,
                          message: str = "") -> bool:
        """Update task status"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Get current status
            cursor.execute('SELECT status FROM tasks WHERE task_id = ?', (task_id,))
            row = cursor.fetchone()
            if not row:
                return False

            old_status = row['status']

            # Update status
            updates = {'status': status.value, 'updated_timestamp': int(datetime.now().timestamp())}

            if status == TaskStatus.IN_PROGRESS:
                updates['started_at'] = datetime.now().isoformat()
            elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED, TaskStatus.TIMEOUT]:
                updates['completed_at'] = datetime.now().isoformat()

            set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [task_id]

            cursor.execute(f'UPDATE tasks SET {set_clause} WHERE task_id = ?', values)

            # Log the event
            self._log_event(task_id, agent_id, 'status_change', old_status, status.value, message)

            logger.info(f"Task {task_id} status: {old_status} -> {status.value}")
            return True

    def update_task_progress(self, task_id: str, progress: Dict[str, Any]) -> bool:
        """Update task progress"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET progress = ?, updated_timestamp = ?
                WHERE task_id = ?
            ''', (json.dumps(progress), int(datetime.now().timestamp()), task_id))
            return cursor.rowcount > 0

    def set_task_result(self, task_id: str, result: Dict[str, Any]) -> bool:
        """Set task result"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET result = ?, updated_timestamp = ?
                WHERE task_id = ?
            ''', (json.dumps(result), int(datetime.now().timestamp()), task_id))
            return cursor.rowcount > 0

    def increment_retry(self, task_id: str, error_message: str) -> bool:
        """Increment retry count and set error"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET retry_count = retry_count + 1,
                    last_error = ?,
                    status = CASE
                        WHEN retry_count + 1 >= max_retries THEN 'failed'
                        ELSE 'retrying'
                    END,
                    updated_timestamp = ?
                WHERE task_id = ?
            ''', (error_message, int(datetime.now().timestamp()), task_id))

            new_status = 'retrying' if cursor.rowcount > 0 else None
            cursor.execute('SELECT retry_count, max_retries FROM tasks WHERE task_id = ?', (task_id,))
            row = cursor.fetchone()
            if row and row['retry_count'] >= row['max_retries']:
                new_status = 'failed'

            if new_status:
                self._log_event(task_id, None, 'retry', None, new_status, f"Retry {row['retry_count']}/{row['max_retries']}: {error_message}")

            return cursor.rowcount > 0

    def get_overdue_tasks(self) -> List[Task]:
        """Get tasks that are overdue"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM tasks
                WHERE deadline_at IS NOT NULL
                AND datetime(deadline_at) < datetime('now')
                AND status NOT IN ('completed', 'cancelled')
                ORDER BY datetime(deadline_at) ASC
            ''')
            return [self._row_to_task(row) for row in cursor.fetchall()]

    def get_stalled_tasks(self, threshold_minutes: int = 30) -> List[Task]:
        """Get tasks that have been in-progress too long without updates"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            threshold = datetime.now() - timedelta(minutes=threshold_minutes)
            cursor.execute('''
                SELECT * FROM tasks
                WHERE status = 'in_progress'
                AND started_at IS NOT NULL
                AND datetime(started_at) < datetime(?)
                ORDER BY started_at ASC
            ''', (threshold.isoformat(),))
            return [self._row_to_task(row) for row in cursor.fetchall()]

    def get_task_statistics(self) -> Dict[str, Any]:
        """Get overall task queue statistics"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            stats = {}

            # Count by status
            cursor.execute('SELECT status, COUNT(*) as count FROM tasks GROUP BY status')
            stats['by_status'] = {row['status']: row['count'] for row in cursor.fetchall()}

            # Count by priority
            cursor.execute('SELECT priority, COUNT(*) as count FROM tasks GROUP BY priority')
            stats['by_priority'] = {row['priority']: row['count'] for row in cursor.fetchall()}

            # Average execution time
            cursor.execute('''
                SELECT AVG(execution_duration_seconds) as avg_time
                FROM task_metrics
                WHERE success = 1
            ''')
            row = cursor.fetchone()
            stats['avg_execution_time_seconds'] = row['avg_time'] if row and row['avg_time'] else 0

            # Success rate
            cursor.execute('''
                SELECT
                    COUNT(CASE WHEN success = 1 THEN 1 END) as successful,
                    COUNT(*) as total
                FROM task_metrics
            ''')
            row = cursor.fetchone()
            if row and row['total'] > 0:
                stats['success_rate'] = row['successful'] / row['total']
            else:
                stats['success_rate'] = 0.0

            return stats

    def _log_event(self, task_id: str, agent_id: Optional[str], action: str,
                   old_status: Optional[str], new_status: Optional[str], message: str):
        """Log an event to the execution log"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO execution_log (task_id, agent_id, action, old_status, new_status, message)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (task_id, agent_id, action, old_status, new_status, message))

    def _row_to_task(self, row: sqlite3.Row) -> Task:
        """Convert database row to Task object"""
        data = dict(row)
        return Task.from_dict(data)

    def backup(self, backup_path: Optional[str] = None) -> str:
        """Create a backup of the database"""
        if not backup_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"{self.db_path}.backup_{timestamp}"

        import shutil
        shutil.copy2(self.db_path, backup_path)
        logger.info(f"Database backed up to {backup_path}")
        return backup_path
