"""
Task Scheduler - Handles task prioritization and deadline management
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict

from .queue import TaskQueue
from .models import Task, TaskStatus, TaskPriority

logger = logging.getLogger(__name__)


class TaskScheduler:
    """Manages task scheduling and deadline enforcement"""

    def __init__(self, queue: TaskQueue):
        self.queue = queue

    def schedule_task(self, task: Task, scheduled_at: datetime) -> bool:
        """Schedule a task for a specific time"""
        task.scheduled_at = scheduled_at.isoformat()
        return self.queue.enqueue(task)

    def set_deadline(self, task_id: str, deadline: datetime) -> bool:
        """Set a deadline for a task"""
        task = self.queue.get_task(task_id)
        if not task:
            return False
        task.deadline_at = deadline.isoformat()
        return self.queue.db.add_task(task) or True  # Update would be better

    def get_ready_tasks(self, agent_id: Optional[str] = None) -> List[Task]:
        """Get all tasks ready to execute now"""
        pending = self.queue.get_pending_tasks(max_count=100)
        now = datetime.now()

        ready = []
        for task in pending:
            # Check if scheduled time has passed
            if task.scheduled_at:
                scheduled_time = datetime.fromisoformat(task.scheduled_at)
                if scheduled_time > now:
                    continue

            # Check if dependencies are met
            if task.depends_on:
                deps_met = all(
                    self.queue.get_task(dep_id) and
                    self.queue.get_task(dep_id).status == TaskStatus.COMPLETED
                    for dep_id in task.depends_on
                )
                if not deps_met:
                    continue

            # Check if required agent matches
            if task.required_agent and task.required_agent != agent_id:
                continue

            ready.append(task)

        # Sort by priority (critical first) then by deadline urgency
        ready.sort(key=lambda t: (
            -t.priority_score(),
            t.deadline_at if t.deadline_at else '9999-12-31'
        ))

        return ready

    def get_priority_queue(self, limit: int = 10) -> List[Task]:
        """Get tasks sorted by priority"""
        tasks = self.queue.get_pending_tasks(max_count=100)

        # Calculate priority score
        for task in tasks:
            task._priority_score = self._calculate_priority_score(task)

        tasks.sort(key=lambda t: -t._priority_score)
        return tasks[:limit]

    def _calculate_priority_score(self, task: Task) -> float:
        """Calculate a composite priority score"""
        score = task.priority_score()

        # Boost for approaching deadlines
        if task.deadline_at:
            deadline = datetime.fromisoformat(task.deadline_at)
            time_until_deadline = (deadline - datetime.now()).total_seconds()

            if time_until_deadline < 3600:  # Less than 1 hour
                score += 50
            elif time_until_deadline < 86400:  # Less than 24 hours
                score += 25
            elif time_until_deadline < 604800:  # Less than 7 days
                score += 10

        # Penalize tasks that have been waiting too long
        created_time = datetime.fromisoformat(task.created_at)
        waiting_time = (datetime.now() - created_time).total_seconds()
        if waiting_time > 86400:  # More than 1 day
            score += min(20, waiting_time / 86400)  # Add up to 20 points

        # Boost for critical task types
        if task.task_type.value == 'bugfix':
            score += 10
        elif task.task_type.value == 'security':
            score += 15

        return score

    def check_deadlines(self) -> List[Task]:
        """Check for tasks approaching or past deadlines"""
        overdue = self.queue.get_overdue_tasks()

        # Also find tasks with approaching deadlines (< 1 hour)
        all_tasks = self.queue.list_tasks()
        now = datetime.now()
        approaching = []

        for task in all_tasks:
            if task.deadline_at and task.status not in [
                TaskStatus.COMPLETED, TaskStatus.CANCELLED
            ]:
                deadline = datetime.fromisoformat(task.deadline_at)
                time_until = (deadline - now).total_seconds()

                if 0 < time_until < 3600:  # Less than 1 hour, not overdue yet
                    approaching.append(task)

        logger.warning(f"Found {len(overdue)} overdue tasks and {len(approaching)} approaching deadlines")
        return overdue + approaching

    def escalate_overdue_tasks(self) -> List[str]:
        """Escalate overdue tasks (increase priority, notify)"""
        overdue = self.queue.get_overdue_tasks()
        escalated = []

        for task in overdue:
            # Escalate priority if not already critical
            if task.priority != TaskPriority.CRITICAL:
                old_priority = task.priority
                task.priority = TaskPriority.CRITICAL
                # Update task in database (would need update method)
                escalated.append(f"{task.task_id}: {old_priority.value} -> CRITICAL")
                logger.warning(f"Escalated task {task.task_id} to CRITICAL (overdue)")

        return escalated

    def balance_load(self) -> Dict[str, int]:
        """Calculate optimal task distribution across agents"""
        # This is a simple implementation - could be more sophisticated
        pending = self.queue.get_pending_tasks(max_count=100)

        # Count tasks by required agent
        agent_load = defaultdict(int)
        for task in pending:
            if task.required_agent:
                agent_load[task.required_agent] += 1
            else:
                agent_load['any'] += 1

        return dict(agent_load)

    def suggest_task_reordering(self) -> List[Dict[str, Any]]:
        """Suggest reordering based on changing priorities"""
        suggestions = []

        # Find tasks that should be reprioritized
        all_tasks = self.queue.list_tasks()

        for task in all_tasks:
            if task.status == TaskStatus.PENDING:
                original_score = task.priority_score()
                new_score = self._calculate_priority_score(task)

                if abs(new_score - original_score) > 20:
                    suggestions.append({
                        'task_id': task.task_id,
                        'current_priority': task.priority.value,
                        'suggested_score': new_score,
                        'reason': 'Priority score changed significantly'
                    })

        return suggestions

    def get_execution_plan(self, agent_id: Optional[str] = None,
                          time_window_hours: int = 24) -> List[Dict[str, Any]]:
        """Generate an execution plan for the next time window"""
        ready = self.get_ready_tasks(agent_id)

        plan = []
        total_estimated = 0

        for task in ready:
            if total_estimated >= time_window_hours * 3600:
                break

            duration = task.estimated_duration_seconds or 3600
            total_estimated += duration

            plan.append({
                'task_id': task.task_id,
                'title': task.title,
                'priority': task.priority.value,
                'estimated_duration_seconds': duration,
                'deadline': task.deadline_at,
                'dependencies': task.depends_on,
                'start_time': None,  # Could be calculated
            })

        return plan

    def optimize_schedule(self) -> Dict[str, Any]:
        """Optimize task schedule for efficiency"""
        all_tasks = self.queue.list_tasks(status=TaskStatus.PENDING)

        # Calculate metrics
        total_tasks = len(all_tasks)
        total_estimated_time = sum(
            t.estimated_duration_seconds or 3600
            for t in all_tasks
        )

        # Identify critical path (tasks blocking others)
        blocking_tasks = set()
        for task in all_tasks:
            blocking_tasks.update(task.depends_on)

        critical_path = [t for t in all_tasks if t.task_id in blocking_tasks]

        return {
            'total_pending': total_tasks,
            'total_estimated_hours': total_estimated_time / 3600,
            'critical_path_tasks': len(critical_path),
            'critical_path': [t.task_id for t in critical_path],
            'recommendations': [
                'Focus on critical path tasks first',
                'Balance high-priority short tasks with long-running tasks',
                'Review blocked tasks for dependency resolution'
            ]
        }
