"""
Task Worker - Executes individual tasks
"""

import asyncio
import logging
from typing import Optional, Dict, Any

from .executor import TaskExecutor

logger = logging.getLogger(__name__)


class TaskWorker:
    """Individual task worker that runs in a loop pulling and executing tasks"""

    def __init__(self, executor: TaskExecutor, worker_id: str, config: Dict[str, Any]):
        self.executor = executor
        self.worker_id = worker_id
        self.config = config
        self.running = False
        self.current_task_id: Optional[str] = None
        self.task_count = 0

    async def run(self):
        """Main worker loop"""
        logger.info(f"Worker {self.worker_id} starting")
        self.running = True

        while self.running and self.executor.running:
            try:
                # Get next task
                task = await self.executor.get_next_task(self.worker_id)

                if task:
                    self.current_task_id = task.task_id
                    logger.info(f"[{self.worker_id}] Got task: {task.task_id}")

                    # Execute the task
                    result = await self.executor.execute_task(task, self.worker_id)
                    self.task_count += 1

                    logger.info(
                        f"[{self.worker_id}] Task {task.task_id} completed: "
                        f"success={result.success}, duration={result.duration_seconds:.2f}s"
                    )

                    self.current_task_id = None

                    # Small delay between tasks
                    await asyncio.sleep(1)
                else:
                    # No tasks available, wait
                    await asyncio.sleep(5)

            except asyncio.CancelledError:
                logger.info(f"[{self.worker_id}] Worker cancelled")
                break
            except Exception as e:
                logger.error(f"[{self.worker_id}] Worker error: {e}")
                await asyncio.sleep(5)

        logger.info(f"Worker {self.worker_id} stopped (processed {self.task_count} tasks)")

    async def stop(self):
        """Stop the worker"""
        logger.info(f"Stopping worker {self.worker_id}...")
        self.running = False

    def is_busy(self) -> bool:
        """Check if worker is currently executing a task"""
        return self.current_task_id is not None

    def get_status(self) -> Dict[str, Any]:
        """Get worker status"""
        return {
            'worker_id': self.worker_id,
            'running': self.running,
            'busy': self.is_busy(),
            'current_task': self.current_task_id,
            'tasks_processed': self.task_count
        }
