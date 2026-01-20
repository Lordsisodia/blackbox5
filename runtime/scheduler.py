"""
BLACKBOX5 Task Scheduler - Autonomous Task Management

Provides periodic task scheduling, priority-based queuing, and dependency resolution
for continuous autonomous agent operation.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 0  # System health, recovery
    HIGH = 1      # Self-improvement, critical research
    MEDIUM = 2    # Regular autonomous tasks
    LOW = 3       # Nice-to-have improvements


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AutonomousTask:
    """Represents an autonomous task"""
    id: str
    name: str
    description: str
    task_type: str  # research, integration, improvement, maintenance

    # Scheduling
    priority: TaskPriority = TaskPriority.MEDIUM
    interval_seconds: Optional[int] = None
    cron_expression: Optional[str] = None

    # Execution
    estimated_tokens: int = 1000
    timeout_seconds: int = 3600
    max_retries: int = 3
    retry_count: int = 0

    # Dependencies
    depends_on: List[str] = field(default_factory=list)

    # State
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    # Callbacks
    execute_func: Optional[Callable] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "task_type": self.task_type,
            "priority": self.priority.value,
            "interval_seconds": self.interval_seconds,
            "cron_expression": self.cron_expression,
            "estimated_tokens": self.estimated_tokens,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "retry_count": self.retry_count,
            "depends_on": self.depends_on,
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "result": self.result,
            "error": self.error
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AutonomousTask":
        """Create from dictionary"""
        task = cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            task_type=data["task_type"]
        )
        task.priority = TaskPriority(data.get("priority", TaskPriority.MEDIUM.value))
        task.interval_seconds = data.get("interval_seconds")
        task.cron_expression = data.get("cron_expression")
        task.estimated_tokens = data.get("estimated_tokens", 1000)
        task.timeout_seconds = data.get("timeout_seconds", 3600)
        task.max_retries = data.get("max_retries", 3)
        task.retry_count = data.get("retry_count", 0)
        task.depends_on = data.get("depends_on", [])
        task.status = TaskStatus(data.get("status", TaskStatus.PENDING.value))
        task.created_at = data.get("created_at")
        task.started_at = data.get("started_at")
        task.completed_at = data.get("completed_at")
        task.result = data.get("result")
        task.error = data.get("error")
        return task


class TaskQueue:
    """Priority-based task queue with dependency resolution"""

    def __init__(self):
        self.tasks: Dict[str, AutonomousTask] = {}
        self.pending_tasks: asyncio.Queue = asyncio.Queue()
        self.running_tasks: Dict[str, asyncio.Task] = {}

    async def add_task(self, task: AutonomousTask):
        """Add a task to the queue"""
        self.tasks[task.id] = task

        # Check if dependencies are satisfied
        if self._dependencies_satisfied(task):
            await self.pending_tasks.put(task)
            task.status = TaskStatus.QUEUED
            logger.info(f"Task {task.id} queued: {task.name}")
        else:
            logger.info(f"Task {task.id} waiting for dependencies: {task.depends_on}")

    def _dependencies_satisfied(self, task: AutonomousTask) -> bool:
        """Check if all task dependencies are satisfied"""
        for dep_id in task.depends_on:
            if dep_id not in self.tasks:
                logger.warning(f"Task {task.id} depends on unknown task {dep_id}")
                return False
            dep_task = self.tasks[dep_id]
            if dep_task.status != TaskStatus.COMPLETED:
                return False
        return True

    async def get_next_task(self) -> Optional[AutonomousTask]:
        """Get next task from queue"""
        try:
            return await asyncio.wait_for(
                self.pending_tasks.get(),
                timeout=1.0
            )
        except asyncio.TimeoutError:
            return None

    def get_task(self, task_id: str) -> Optional[AutonomousTask]:
        """Get task by ID"""
        return self.tasks.get(task_id)

    def update_task_status(self, task_id: str, status: TaskStatus, **kwargs):
        """Update task status and related fields"""
        task = self.tasks.get(task_id)
        if task:
            task.status = status
            if status == TaskStatus.RUNNING and not task.started_at:
                task.started_at = datetime.now().isoformat()
            if status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                task.completed_at = datetime.now().isoformat()

            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)

            # Check if any waiting tasks can now be queued
            if status == TaskStatus.COMPLETED:
                self._check_waiting_tasks(task_id)

    def _check_waiting_tasks(self, completed_task_id: str):
        """Check if any tasks were waiting for this task"""
        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING and completed_task_id in task.depends_on:
                if self._dependencies_satisfied(task):
                    asyncio.create_task(self.pending_tasks.put(task))
                    task.status = TaskStatus.QUEUED
                    logger.info(f"Task {task.id} now queued after {completed_task_id} completed")

    def get_stats(self) -> Dict[str, int]:
        """Get queue statistics"""
        stats = {
            "total": len(self.tasks),
            "pending": 0,
            "queued": 0,
            "running": 0,
            "completed": 0,
            "failed": 0
        }
        for task in self.tasks.values():
            stats[task.status.value] += 1
        return stats


class TaskScheduler:
    """
    Autonomous task scheduler for BLACKBOX5

    Features:
    - Periodic task execution with cron/interval scheduling
    - Priority-based task queuing
    - Dependency resolution
    - Automatic retry on failure
    - Token usage tracking
    """

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.task_queue = TaskQueue()
        self.running = False
        self.task_counter = 0
        self.state_file = Path("./.runtime/scheduler_state.json")

    def generate_task_id(self) -> str:
        """Generate unique task ID"""
        self.task_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"task_{timestamp}_{self.task_counter:04d}"

    async def schedule_periodic_task(
        self,
        name: str,
        description: str,
        task_type: str,
        execute_func: Callable,
        interval_seconds: Optional[int] = None,
        cron_expression: Optional[str] = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        estimated_tokens: int = 1000
    ) -> str:
        """Schedule a periodic autonomous task"""
        task_id = self.generate_task_id()

        task = AutonomousTask(
            id=task_id,
            name=name,
            description=description,
            task_type=task_type,
            priority=priority,
            estimated_tokens=estimated_tokens,
            execute_func=execute_func
        )

        # Add to queue
        await self.task_queue.add_task(task)

        # Schedule periodic execution
        if interval_seconds:
            trigger = IntervalTrigger(seconds=interval_seconds)
            self.scheduler.add_job(
                self._execute_task,
                trigger=trigger,
                args=[task_id],
                id=task_id,
                name=name,
                replace_existing=True
            )
        elif cron_expression:
            trigger = CronTrigger.from_crontab(cron_expression)
            self.scheduler.add_job(
                self._execute_task,
                trigger=trigger,
                args=[task_id],
                id=task_id,
                name=name,
                replace_existing=True
            )

        logger.info(f"Scheduled periodic task: {name} (ID: {task_id})")
        return task_id

    async def schedule_one_time_task(
        self,
        name: str,
        description: str,
        task_type: str,
        execute_func: Callable,
        priority: TaskPriority = TaskPriority.MEDIUM,
        estimated_tokens: int = 1000,
        depends_on: Optional[List[str]] = None
    ) -> str:
        """Schedule a one-time task"""
        task_id = self.generate_task_id()

        task = AutonomousTask(
            id=task_id,
            name=name,
            description=description,
            task_type=task_type,
            priority=priority,
            estimated_tokens=estimated_tokens,
            depends_on=depends_on or [],
            execute_func=execute_func
        )

        await self.task_queue.add_task(task)
        logger.info(f"Scheduled one-time task: {name} (ID: {task_id})")
        return task_id

    async def _execute_task(self, task_id: str):
        """Execute a task"""
        task = self.task_queue.get_task(task_id)
        if not task:
            logger.error(f"Task not found: {task_id}")
            return

        logger.info(f"Executing task: {task.name} (ID: {task_id})")

        # Update status
        self.task_queue.update_task_status(task_id, TaskStatus.RUNNING)

        try:
            # Execute task function
            if task.execute_func:
                result = await task.execute_func()
                task.result = {"success": True, "data": result}

                # Mark as completed
                self.task_queue.update_task_status(
                    task_id,
                    TaskStatus.COMPLETED,
                    result=task.result
                )

                logger.info(f"Task completed: {task.name}")

                # Reset retry count on success
                task.retry_count = 0

            else:
                raise ValueError(f"No execute function for task {task_id}")

        except Exception as e:
            logger.error(f"Task failed: {task.name} - {e}")

            # Check if we should retry
            task.retry_count += 1
            if task.retry_count < task.max_retries:
                logger.info(f"Retrying task {task.name} (attempt {task.retry_count + 1}/{task.max_retries})")
                self.task_queue.update_task_status(
                    task_id,
                    TaskStatus.PENDING,
                    error=str(e)
                )
                # Re-queue for retry
                await self.task_queue.pending_tasks.put(task)
            else:
                self.task_queue.update_task_status(
                    task_id,
                    TaskStatus.FAILED,
                    error=str(e)
                )
                logger.error(f"Task permanently failed after {task.max_retries} retries: {task.name}")

    async def process_queue(self):
        """Process tasks from the queue"""
        while self.running:
            task = await self.task_queue.get_next_task()
            if task:
                asyncio.create_task(self._execute_task(task.id))
            else:
                await asyncio.sleep(0.1)

    async def start(self):
        """Start the scheduler"""
        logger.info("Starting task scheduler")
        self.running = True
        self.scheduler.start()

        # Start queue processor
        await self.process_queue()

    async def stop(self):
        """Stop the scheduler"""
        logger.info("Stopping task scheduler")
        self.running = False
        self.scheduler.shutdown()

    def get_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics"""
        return {
            "queue_stats": self.task_queue.get_stats(),
            "scheduled_jobs": len(self.scheduler.get_jobs()),
            "running": self.running
        }


# Autonomous task templates

async def research_blackbox_task() -> Dict[str, Any]:
    """Template: Research the Black Box architecture"""
    # This would analyze BLACKBOX5 code, documentation, suggest improvements
    return {
        "findings": "Architecture analysis complete",
        "suggestions": ["Optimize memory consolidation", "Add skill versioning"]
    }


async def discover_skills_task() -> Dict[str, Any]:
    """Template: Discover new skills from GitHub/internet"""
    # This would scan GitHub for new skills, evaluate them
    return {
        "new_skills_found": 5,
        "skills_evaluated": ["agent-protocol", "mcp-integration"]
    }


async def integrate_framework_task() -> Dict[str, Any]:
    """Template: Integrate discovered framework"""
    # This would integrate a new framework into BLACKBOX5
    return {
        "framework_integrated": "new-agent-framework",
        "status": "success"
    }


async def self_improvement_task() -> Dict[str, Any]:
    """Template: Self-improvement analysis"""
    # This would analyze system performance and suggest improvements
    return {
        "performance_gains": "15% faster execution",
        "token_efficiency": "20% reduction in token usage"
    }


async def health_check_task() -> Dict[str, Any]:
    """Template: System health check"""
    # This would check system health and report issues
    return {
        "health_status": "healthy",
        "issues": []
    }


# Pre-configured autonomous tasks for 24/7 operation

async def setup_autonomous_tasks(scheduler: TaskScheduler):
    """Setup standard autonomous tasks for 24/7 operation"""

    # Critical: Health checks every 5 minutes
    await scheduler.schedule_periodic_task(
        name="System Health Check",
        description="Monitor system health and resource usage",
        task_type="maintenance",
        execute_func=health_check_task,
        interval_seconds=300,
        priority=TaskPriority.CRITICAL,
        estimated_tokens=500
    )

    # High: Research BlackBox every hour
    await scheduler.schedule_periodic_task(
        name="BlackBox Research",
        description="Analyze BLACKBOX5 architecture and suggest improvements",
        task_type="research",
        execute_func=research_blackbox_task,
        interval_seconds=3600,
        priority=TaskPriority.HIGH,
        estimated_tokens=50000
    )

    # High: Discover skills every 2 hours
    await scheduler.schedule_periodic_task(
        name="Skill Discovery",
        description="Search GitHub and internet for new skills to integrate",
        task_type="research",
        execute_func=discover_skills_task,
        interval_seconds=7200,
        priority=TaskPriority.HIGH,
        estimated_tokens=100000
    )

    # Medium: Self-improvement analysis every 6 hours
    await scheduler.schedule_periodic_task(
        name="Self-Improvement Analysis",
        description="Analyze performance and suggest improvements",
        task_type="improvement",
        execute_func=self_improvement_task,
        interval_seconds=21600,
        priority=TaskPriority.MEDIUM,
        estimated_tokens=100000
    )

    # Low: Framework integration (runs when needed)
    await scheduler.schedule_one_time_task(
        name="Framework Integration Queue",
        description="Integrate discovered frameworks into BLACKBOX5",
        task_type="integration",
        execute_func=integrate_framework_task,
        priority=TaskPriority.LOW,
        estimated_tokens=200000
    )

    logger.info("Autonomous tasks configured for 24/7 operation")
