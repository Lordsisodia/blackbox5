"""
Task Executor - Main executor that coordinates task execution
"""

import asyncio
import logging
import signal
import sys
import json
import os
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import traceback

from ..core.queue import TaskQueue
from ..core.models import Task, TaskStatus, TaskResult, TaskProgress
from ..core.scriber import ScribeIntegration

logger = logging.getLogger(__name__)


class TaskExecutor:
    """Main task executor that pulls from queue and runs tasks"""

    def __init__(self, config: Dict[str, Any], agent_id: str = "task-executor"):
        self.config = config
        self.agent_id = agent_id
        self.queue = TaskQueue(config['database']['path'])
        self.scribe = ScribeIntegration(config.get('scribe', {}))
        self.running = False
        self.current_task: Optional[Task] = None
        self.workers: List['TaskWorker'] = []

        # Load execution settings
        exec_config = config.get('execution', {})
        self.max_concurrent = exec_config.get('max_concurrent_tasks', 3)
        self.poll_interval = exec_config.get('poll_interval_seconds', 5)
        self.task_timeout = exec_config.get('task_timeout_seconds', 3600)
        self.retry_delay = exec_config.get('retry_delay_seconds', 60)

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    async def start(self):
        """Start the executor main loop"""
        logger.info(f"Task executor starting (max_concurrent: {self.max_concurrent})")
        self.running = True

        # Start worker threads
        for i in range(self.max_concurrent):
            worker = TaskWorker(
                executor=self,
                worker_id=f"{self.agent_id}-worker-{i+1}",
                config=self.config
            )
            self.workers.append(worker)
            asyncio.create_task(worker.run())

        # Main monitoring loop
        try:
            while self.running:
                await asyncio.sleep(self.poll_interval)
                await self._monitor_tasks()
        except asyncio.CancelledError:
            logger.info("Executor cancelled")
        finally:
            await self.stop()

    async def stop(self):
        """Stop the executor"""
        logger.info("Task executor stopping...")
        self.running = False

        # Stop all workers
        for worker in self.workers:
            await worker.stop()

        # Wait for current task to finish
        if self.current_task:
            logger.info(f"Waiting for current task {self.current_task.task_id} to finish...")
            # Give it some time to complete
            await asyncio.sleep(5)

        logger.info("Task executor stopped")

    async def _monitor_tasks(self):
        """Monitor task execution and health"""
        # Check for stalled tasks
        stalled_threshold = self.config.get('monitoring', {}).get('stalled_threshold_minutes', 30)
        stalled = self.queue.get_stalled_tasks(stalled_threshold)

        if stalled:
            logger.warning(f"Found {len(stalled)} stalled tasks")
            for task in stalled:
                logger.warning(f"Stalled task: {task.task_id} (started: {task.started_at})")

        # Check for overdue tasks
        overdue = self.queue.get_overdue_tasks()
        if overdue:
            logger.warning(f"Found {len(overdue)} overdue tasks")
            for task in overdue:
                logger.warning(f"Overdue task: {task.task_id} (deadline: {task.deadline_at})")

        # Log to scribe if needed
        if self.scribe.enabled:
            await self.scribe.log_status(self.agent_id, {
                'running': self.running,
                'active_workers': sum(1 for w in self.workers if w.is_busy()),
                'current_task': self.current_task.task_id if self.current_task else None,
                'stalled_tasks': len(stalled),
                'overdue_tasks': len(overdue)
            })

    async def get_next_task(self, worker_id: str) -> Optional[Task]:
        """Get the next task for a worker"""
        task = self.queue.dequeue(worker_id)
        if task and self.scribe.enabled:
            await self.scribe.log_event(
                task.task_id,
                "dequeued",
                f"Task dequeued by {worker_id}"
            )
        return task

    async def execute_task(self, task: Task, worker_id: str) -> TaskResult:
        """Execute a task and return the result"""
        self.current_task = task
        task_id = task.task_id

        logger.info(f"[{worker_id}] Executing task: {task_id}")

        # Claim the task
        if not self.queue.claim_task(task_id, worker_id):
            return TaskResult(success=False, error_message="Failed to claim task")

        # Log to scribe
        if self.scribe.enabled:
            await self.scribe.log_event(task_id, "started", f"Task started by {worker_id}")

        result = TaskResult(success=False)
        start_time = datetime.now()

        try:
            # Update initial progress
            await self._update_progress(task_id, 10, "Initializing task execution", 0, 0)

            # Execute based on task type
            if task.command:
                result = await self._execute_command(task, worker_id)
            elif task.script_path:
                result = await self._execute_script(task, worker_id)
            else:
                # Task with no command/script - mark as informational
                result = TaskResult(
                    success=True,
                    output="Task completed (informational, no execution)",
                    duration_seconds=(datetime.now() - start_time).total_seconds()
                )

            # Update final status
            if result.success:
                self.queue.complete_task(task_id, result.__dict__, worker_id)
                await self._update_progress(task_id, 100, "Task completed", 0, 0)
            else:
                self.queue.fail_task(task_id, result.error_message, worker_id)
                await self._update_progress(task_id, 0, f"Task failed: {result.error_message}", 0, 0)

            # Log to scribe
            if self.scribe.enabled:
                if result.success:
                    await self.scribe.log_event(task_id, "completed", f"Task completed successfully\nOutput: {result.output[:500]}")
                else:
                    await self.scribe.log_event(task_id, "failed", f"Task failed: {result.error_message}")

        except Exception as e:
            error_msg = f"Task execution error: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            result = TaskResult(success=False, error_message=error_msg)
            self.queue.fail_task(task_id, error_msg, worker_id)

            # Log to scribe
            if self.scribe.enabled:
                await self.scribe.log_event(task_id, "error", f"Task error: {error_msg}")

        finally:
            result.duration_seconds = (datetime.now() - start_time).total_seconds()
            self.current_task = None

        return result

    async def _execute_command(self, task: Task, worker_id: str) -> TaskResult:
        """Execute a shell command"""
        logger.info(f"[{worker_id}] Executing command: {task.command}")

        await self._update_progress(task_id=task.task_id, percentage=20, current_step="Running command")

        try:
            working_dir = task.working_dir or "/opt/blackbox5"
            env = os.environ.copy()
            env.update(task.environment)

            process = await asyncio.create_subprocess_shell(
                task.command,
                cwd=working_dir,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.task_timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                return TaskResult(
                    success=False,
                    error_message=f"Command timed out after {self.task_timeout}s"
                )

            output = stdout.decode('utf-8', errors='replace')
            error_output = stderr.decode('utf-8', errors='replace')

            await self._update_progress(task.task_id, 90, f"Command completed (exit code: {process.returncode})")

            return TaskResult(
                success=process.returncode == 0,
                output=output,
                error_message=error_output if process.returncode != 0 else "",
                exit_code=process.returncode,
                artifacts=self._extract_artifacts(output, task.working_dir)
            )

        except Exception as e:
            return TaskResult(success=False, error_message=str(e))

    async def _execute_script(self, task: Task, worker_id: str) -> TaskResult:
        """Execute a Python script"""
        logger.info(f"[{worker_id}] Executing script: {task.script_path}")

        await self._update_progress(task.task_id, 20, f"Running script: {Path(task.script_path).name}")

        try:
            script_path = Path(task.script_path)
            if not script_path.exists():
                return TaskResult(success=False, error_message=f"Script not found: {task.script_path}")

            working_dir = task.working_dir or script_path.parent
            env = os.environ.copy()
            env.update(task.environment)

            process = await asyncio.create_subprocess_exec(
                sys.executable,
                str(script_path),
                cwd=working_dir,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.task_timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                return TaskResult(
                    success=False,
                    error_message=f"Script timed out after {self.task_timeout}s"
                )

            output = stdout.decode('utf-8', errors='replace')
            error_output = stderr.decode('utf-8', errors='replace')

            await self._update_progress(task.task_id, 90, f"Script completed (exit code: {process.returncode})")

            return TaskResult(
                success=process.returncode == 0,
                output=output,
                error_message=error_output if process.returncode != 0 else "",
                exit_code=process.returncode,
                artifacts=self._extract_artifacts(output, working_dir)
            )

        except Exception as e:
            return TaskResult(success=False, error_message=str(e))

    async def _update_progress(self, task_id: str, percentage: int,
                              message: str, total_steps: int = 0,
                              completed_steps: int = 0):
        """Update task progress"""
        progress = {
            'percentage': percentage,
            'current_step': message,
            'total_steps': total_steps,
            'completed_steps': completed_steps,
            'message': message,
            'updated_at': datetime.now().isoformat()
        }
        self.queue.update_progress(task_id, progress)
        logger.debug(f"Task {task_id} progress: {percentage}% - {message}")

    def _extract_artifacts(self, output: str, working_dir: str) -> List[str]:
        """Extract artifact paths from command output"""
        artifacts = []
        # Look for common artifact patterns
        if "Created:" in output or "Generated:" in output or "Output:" in output:
            # Simple extraction - could be more sophisticated
            for line in output.split('\n'):
                if any(marker in line for marker in ['Created:', 'Generated:', 'Output:', 'Wrote:']):
                    # Extract potential file paths
                    words = line.split()
                    for word in words:
                        if '/' in word or word.endswith('.md') or word.endswith('.py') or word.endswith('.json'):
                            artifacts.append(word.strip())
        return artifacts

    def _handle_shutdown(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

    def get_status(self) -> Dict[str, Any]:
        """Get executor status"""
        return {
            'running': self.running,
            'agent_id': self.agent_id,
            'active_workers': sum(1 for w in self.workers if w.is_busy()),
            'current_task': self.current_task.task_id if self.current_task else None,
            'queue_stats': self.queue.get_statistics()
        }
