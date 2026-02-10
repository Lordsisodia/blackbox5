"""
Task Monitor - Tracks task progress and generates reports
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from ..core.queue import TaskQueue
from ..core.models import Task, TaskStatus

logger = logging.getLogger(__name__)


class TaskMonitor:
    """Monitors task execution and provides status reports"""

    def __init__(self, queue: TaskQueue, config: Dict[str, Any]):
        self.queue = queue
        self.config = config
        self.running = False

        monitoring_config = config.get('monitoring', {})
        self.enabled = monitoring_config.get('enabled', True)
        self.alert_on_stalled = monitoring_config.get('alert_on_stalled', True)
        self.stalled_threshold = monitoring_config.get('stalled_threshold_minutes', 30)
        self.alert_on_overdue = monitoring_config.get('alert_on_overdue', True)
        self.progress_update_interval = monitoring_config.get('progress_update_interval_seconds', 60)

    async def start(self):
        """Start the monitoring loop"""
        if not self.enabled:
            return

        logger.info("Task monitor starting")
        self.running = True

        try:
            while self.running:
                await self.check_status()
                await asyncio.sleep(self.progress_update_interval)
        except asyncio.CancelledError:
            logger.info("Monitor cancelled")
        finally:
            self.running = False

    async def stop(self):
        """Stop the monitor"""
        logger.info("Task monitor stopping")
        self.running = False

    async def check_status(self):
        """Check status of all tasks and generate alerts if needed"""
        # Check for stalled tasks
        if self.alert_on_stalled:
            stalled = self.queue.get_stalled_tasks(self.stalled_threshold)
            if stalled:
                logger.warning(f"Found {len(stalled)} stalled tasks")
                for task in stalled:
                    await self._handle_stalled_task(task)

        # Check for overdue tasks
        if self.alert_on_overdue:
            overdue = self.queue.get_overdue_tasks()
            if overdue:
                logger.warning(f"Found {len(overdue)} overdue tasks")
                for task in overdue:
                    await self._handle_overdue_task(task)

    async def _handle_stalled_task(self, task: Task):
        """Handle a stalled task"""
        # Log the issue
        logger.warning(f"Task {task.task_id} appears stalled (started: {task.started_at})")

        # Could implement escalation, notification, etc.
        # For now, just log

    async def _handle_overdue_task(self, task: Task):
        """Handle an overdue task"""
        logger.error(f"Task {task.task_id} is overdue (deadline: {task.deadline_at})")

        # Could implement escalation, notification, etc.
        # For now, just log

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for a monitoring dashboard"""
        stats = self.queue.get_statistics()

        # Get task counts by status
        by_status = defaultdict(int)
        for status, count in stats.get('by_status', {}).items():
            by_status[status] = count

        # Get task counts by priority
        by_priority = defaultdict(int)
        for priority, count in stats.get('by_priority', {}).items():
            by_priority[priority] = count

        # Get recent tasks
        recent_completed = self.queue.list_tasks(status=TaskStatus.COMPLETED, limit=10)
        recent_failed = self.queue.list_tasks(status=TaskStatus.FAILED, limit=5)

        # Get active tasks
        active_tasks = self.queue.list_tasks(status=TaskStatus.IN_PROGRESS, limit=10)

        return {
            'summary': {
                'total_pending': by_status.get('pending', 0) + by_status.get('queued', 0),
                'in_progress': by_status.get('in_progress', 0),
                'completed_today': len([t for t in recent_completed
                                      if datetime.fromisoformat(t.completed_at or '').date() == datetime.now().date()]),
                'failed_today': len([t for t in recent_failed
                                   if datetime.fromisoformat(t.completed_at or '').date() == datetime.now().date()]),
            },
            'by_status': dict(by_status),
            'by_priority': dict(by_priority),
            'active_tasks': [
                {
                    'task_id': t.task_id,
                    'title': t.title,
                    'started_at': t.started_at,
                    'progress': t.progress,
                    'assigned_agent': t.assigned_agent,
                }
                for t in active_tasks
            ],
            'recent_completed': [
                {
                    'task_id': t.task_id,
                    'title': t.title,
                    'completed_at': t.completed_at,
                    'duration_seconds': t.result.duration_seconds if t.result else 0,
                }
                for t in recent_completed
            ],
            'recent_failed': [
                {
                    'task_id': t.task_id,
                    'title': t.title,
                    'failed_at': t.completed_at,
                    'error': t.last_error,
                }
                for t in recent_failed
            ],
            'health': {
                'stalled_tasks': len(self.queue.get_stalled_tasks(self.stalled_threshold)),
                'overdue_tasks': len(self.queue.get_overdue_tasks()),
                'success_rate': stats.get('success_rate', 0.0),
                'avg_execution_time_seconds': stats.get('avg_execution_time_seconds', 0),
            }
        }

    def get_task_timeline(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get task activity timeline"""
        cutoff = datetime.now() - timedelta(hours=hours)

        # Get all tasks and filter by time
        all_tasks = self.queue.list_tasks()

        events = []

        for task in all_tasks:
            created_time = datetime.fromisoformat(task.created_at)
            if created_time < cutoff:
                continue

            events.append({
                'timestamp': task.created_at,
                'event_type': 'created',
                'task_id': task.task_id,
                'title': task.title,
                'task_type': task.task_type.value,
                'priority': task.priority.value,
            })

            if task.started_at:
                events.append({
                    'timestamp': task.started_at,
                    'event_type': 'started',
                    'task_id': task.task_id,
                    'title': task.title,
                })

            if task.completed_at:
                events.append({
                    'timestamp': task.completed_at,
                    'event_type': 'completed' if task.status == TaskStatus.COMPLETED else 'failed',
                    'task_id': task.task_id,
                    'title': task.title,
                    'status': task.status.value,
                })

        # Sort by timestamp
        events.sort(key=lambda e: e['timestamp'])

        return events

    def get_progress_report(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed progress report for a task"""
        task = self.queue.get_task(task_id)
        if not task:
            return None

        report = {
            'task_id': task.task_id,
            'title': task.title,
            'status': task.status.value,
            'created_at': task.created_at,
            'started_at': task.started_at,
            'completed_at': task.completed_at,
            'estimated_duration': task.estimated_duration_seconds,
            'progress': task.progress,
            'result': task.result,
            'dependencies': task.depends_on,
            'retry_count': task.retry_count,
            'max_retries': task.max_retries,
        }

        # Calculate actual duration if completed
        if task.started_at and task.completed_at:
            started = datetime.fromisoformat(task.started_at)
            completed = datetime.fromisoformat(task.completed_at)
            report['actual_duration_seconds'] = (completed - started).total_seconds()

        return report

    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status of a specific agent"""
        # Get tasks assigned to this agent
        all_tasks = self.queue.list_tasks()
        agent_tasks = [t for t in all_tasks if t.assigned_agent == agent_id]

        current = [t for t in agent_tasks if t.status == TaskStatus.IN_PROGRESS]
        completed = [t for t in agent_tasks if t.status == TaskStatus.COMPLETED]
        failed = [t for t in agent_tasks if t.status == TaskStatus.FAILED]

        total_duration = sum(
            (t.result.duration_seconds if t.result and t.result.duration_seconds else 0)
            for t in completed
        )

        return {
            'agent_id': agent_id,
            'current_task': current[0].task_id if current else None,
            'current_task_title': current[0].title if current else None,
            'total_completed': len(completed),
            'total_failed': len(failed),
            'total_time_spent_seconds': total_duration,
            'average_task_duration_seconds': total_duration / len(completed) if completed else 0,
            'success_rate': len(completed) / (len(completed) + len(failed)) if (completed or failed) else 0,
        }
