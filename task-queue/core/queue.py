"""
Task Queue Manager
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from .database import TaskQueueDatabase
from .models import Task, TaskStatus, TaskPriority

logger = logging.getLogger(__name__)


class TaskQueue:
    """High-level queue management interface"""

    def __init__(self, db_path: Optional[str] = None):
        self.db = TaskQueueDatabase(db_path)
        self.db.initialize_schema()

    def enqueue(self, task: Task) -> bool:
        """Add a task to the queue"""
        logger.info(f"Enqueueing task: {task.task_id}")
        return self.db.add_task(task)

    def dequeue(self, agent_id: Optional[str] = None) -> Optional[Task]:
        """Get the next task to execute"""
        task = self.db.get_next_task(agent_id)
        if task:
            # Mark as queued
            self.update_status(task.task_id, TaskStatus.QUEUED)
            logger.info(f"Dequeued task: {task.task_id} for agent {agent_id}")
        return task

    def claim_task(self, task_id: str, agent_id: str) -> bool:
        """Claim a task for execution by an agent"""
        task = self.db.get_task(task_id)
        if not task:
            return False

        # Check if dependencies are satisfied
        if task.depends_on:
            for dep_id in task.depends_on:
                dep_task = self.db.get_task(dep_id)
                if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                    logger.warning(f"Task {task_id} blocked by dependency {dep_id}")
                    self.update_status(task_id, TaskStatus.BLOCKED)
                    return False

        # Claim the task
        success = self.db.update_task_status(task_id, TaskStatus.IN_PROGRESS, agent_id)
        if success:
            logger.info(f"Task {task_id} claimed by agent {agent_id}")
        return success

    def update_status(self, task_id: str, status: TaskStatus,
                     agent_id: Optional[str] = None,
                     message: str = "") -> bool:
        """Update task status"""
        return self.db.update_task_status(task_id, status, agent_id, message)

    def update_progress(self, task_id: str, progress: Dict[str, Any]) -> bool:
        """Update task progress"""
        return self.db.update_task_progress(task_id, progress)

    def complete_task(self, task_id: str, result: Dict[str, Any],
                      agent_id: Optional[str] = None) -> bool:
        """Mark a task as completed with results"""
        success = self.db.set_task_result(task_id, result)
        if success:
            self.db.update_task_status(task_id, TaskStatus.COMPLETED, agent_id, "Task completed")
            logger.info(f"Task {task_id} completed successfully")
        return success

    def fail_task(self, task_id: str, error_message: str,
                  agent_id: Optional[str] = None, retry: bool = True) -> bool:
        """Mark a task as failed, optionally retrying"""
        if retry:
            return self.db.increment_retry(task_id, error_message)
        else:
            self.db.update_task_status(task_id, TaskStatus.FAILED, agent_id, error_message)
            logger.error(f"Task {task_id} failed: {error_message}")
            return True

    def cancel_task(self, task_id: str, reason: str = "") -> bool:
        """Cancel a task"""
        return self.db.update_task_status(task_id, TaskStatus.CANCELLED, None, reason)

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        return self.db.get_task(task_id)

    def get_pending_tasks(self, max_count: int = 10) -> List[Task]:
        """Get pending tasks"""
        return self.db.get_pending_tasks(max_count)

    def get_overdue_tasks(self) -> List[Task]:
        """Get overdue tasks"""
        return self.db.get_overdue_tasks()

    def get_stalled_tasks(self, threshold_minutes: int = 30) -> List[Task]:
        """Get stalled tasks"""
        return self.db.get_stalled_tasks(threshold_minutes)

    def get_statistics(self) -> Dict[str, Any]:
        """Get queue statistics"""
        return self.db.get_task_statistics()

    def list_tasks(self, status: Optional[TaskStatus] = None,
                   limit: Optional[int] = None) -> List[Task]:
        """List tasks with optional filtering"""
        tasks = self.db.get_all_tasks(status)
        if limit:
            tasks = tasks[:limit]
        return tasks

    def search_tasks(self, query: str, limit: int = 20) -> List[Task]:
        """Search tasks by title or description"""
        all_tasks = self.db.get_all_tasks()
        query_lower = query.lower()
        matching = [
            task for task in all_tasks
            if query_lower in task.title.lower()
            or query_lower in task.description.lower()
            or any(query_lower in label.lower() for label in task.labels)
        ]
        return matching[:limit]

    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Get tasks by priority level"""
        return [task for task in self.db.get_all_tasks() if task.priority == priority]

    def get_tasks_by_type(self, task_type) -> List[Task]:
        """Get tasks by type"""
        return [task for task in self.db.get_all_tasks() if task.task_type == task_type]

    def purge_completed(self, days_old: int = 7) -> int:
        """Remove completed tasks older than specified days"""
        cutoff = datetime.now() - timedelta(days=days_old)
        # This would require adding a purge method to the database
        # For now, just log the action
        logger.info(f"Would purge completed tasks older than {days_old} days")
        return 0

    def bulk_enqueue(self, tasks: List[Task]) -> Dict[str, bool]:
        """Enqueue multiple tasks"""
        results = {}
        for task in tasks:
            results[task.task_id] = self.enqueue(task)
        success_count = sum(1 for v in results.values() if v)
        logger.info(f"Bulk enqueued {success_count}/{len(tasks)} tasks")
        return results
