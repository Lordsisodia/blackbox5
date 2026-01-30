"""
BLACKBOX5 Daemon - 24/7 Autonomous Operation Manager

Provides continuous operation infrastructure for BLACKBOX5 agents with health monitoring,
auto-restart capabilities, and resource tracking for 100-200M tokens/day utilization.
"""

import asyncio
import signal
import sys
import logging
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
import psutil
import aiofiles

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('blackbox5_runtime.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class DaemonConfig:
    """Configuration for the BLACKBOX5 daemon"""
    # Health check interval (seconds)
    health_check_interval: int = 30

    # Task execution timeout (seconds)
    task_timeout: int = 3600

    # Maximum concurrent tasks
    max_concurrent_tasks: int = 10

    # Token usage targets
    target_tokens_per_day: int = 150_000_000  # 150M
    target_tokens_per_hour: int = 6_250_000  # ~6.25M

    # Resource limits
    max_memory_mb: int = 8192  # 8GB
    max_cpu_percent: float = 80.0

    # Auto-restart settings
    max_restarts_per_hour: int = 5
    restart_cooldown_seconds: int = 60

    # Paths
    runtime_dir: Path = Path("./.runtime")
    state_file: Path = Path("./.runtime/daemon_state.json")
    log_file: Path = Path("./blackbox5_runtime.log")


@dataclass
class DaemonState:
    """Runtime state of the daemon"""
    pid: int
    start_time: str
    uptime_seconds: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    tokens_used: int = 0
    restart_count: int = 0
    last_health_check: str = ""
    status: str = "running"  # running, stopped, error

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ResourceMonitor:
    """Monitor system resources and token usage"""

    def __init__(self, config: DaemonConfig):
        self.config = config
        self.process = psutil.Process()

    def get_memory_usage_mb(self) -> float:
        """Get current memory usage in MB"""
        return self.process.memory_info().rss / 1024 / 1024

    def get_cpu_percent(self) -> float:
        """Get current CPU usage percentage"""
        return self.process.cpu_percent(interval=1)

    def get_uptime_seconds(self) -> int:
        """Get daemon uptime in seconds"""
        return int(datetime.now().timestamp())

    def check_resource_limits(self) -> Dict[str, bool]:
        """Check if resource usage is within limits"""
        memory_mb = self.get_memory_usage_mb()
        cpu_percent = self.get_cpu_percent()

        return {
            "memory_ok": memory_mb < self.config.max_memory_mb,
            "cpu_ok": cpu_percent < self.config.max_cpu_percent,
            "memory_mb": memory_mb,
            "cpu_percent": cpu_percent
        }

    def estimate_tokens_per_hour(self, current_tokens: int, uptime_seconds: int) -> int:
        """Estimate tokens per hour based on current usage"""
        if uptime_seconds < 3600:
            # Extrapolate from current usage
            return int((current_tokens / uptime_seconds) * 3600) if uptime_seconds > 0 else 0
        return current_tokens // (uptime_seconds // 3600)


class HealthChecker:
    """Health monitoring and auto-restart capabilities"""

    def __init__(self, config: DaemonConfig):
        self.config = config
        self.restart_history: List[datetime] = []
        self.consecutive_failures = 0

    def should_restart(self, error_count: int) -> bool:
        """Determine if a restart is needed"""
        # Check restart rate limit
        now = datetime.now()
        recent_restarts = [
            t for t in self.restart_history
            if (now - t).total_seconds() < 3600
        ]

        if len(recent_restarts) >= self.config.max_restarts_per_hour:
            logger.warning(f"Restart rate limit reached: {len(recent_restarts)} restarts in last hour")
            return False

        # Check consecutive failures
        if error_count >= 3:
            logger.warning(f"Too many consecutive failures: {error_count}")
            return True

        return False

    def record_restart(self):
        """Record a restart event"""
        self.restart_history.append(datetime.now())
        self.consecutive_failures = 0

    def record_failure(self):
        """Record a failure event"""
        self.consecutive_failures += 1


class Blackbox5Daemon:
    """
    Main daemon class for 24/7 BLACKBOX5 operation

    Features:
    - Continuous task execution loop
    - Health monitoring with auto-restart
    - Resource usage tracking
    - Token utilization monitoring
    - Graceful shutdown handling
    """

    def __init__(self, config: Optional[DaemonConfig] = None):
        self.config = config or DaemonConfig()
        self.state = DaemonState(
            pid=psutil.Process().pid,
            start_time=datetime.now().isoformat()
        )
        self.resource_monitor = ResourceMonitor(self.config)
        self.health_checker = HealthChecker(self.config)
        self.running = False
        self.task_queue: asyncio.Queue = None

        # Ensure runtime directory exists
        self.config.runtime_dir.mkdir(parents=True, exist_ok=True)

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.running = False

    async def load_state(self) -> bool:
        """Load previous daemon state if available"""
        try:
            if self.config.state_file.exists():
                async with aiofiles.open(self.config.state_file, 'r') as f:
                    data = json.loads(await f.read())
                    # Update state with loaded data
                    for key, value in data.items():
                        if hasattr(self.state, key):
                            setattr(self.state, key, value)
                logger.info(f"Loaded state from {self.config.state_file}")
                return True
        except Exception as e:
            logger.warning(f"Could not load state: {e}")
        return False

    async def save_state(self):
        """Persist current daemon state"""
        try:
            async with aiofiles.open(self.config.state_file, 'w') as f:
                await f.write(json.dumps(self.state.to_dict(), indent=2))
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    async def health_check(self) -> bool:
        """Perform health check and update state"""
        try:
            # Check resource usage
            resource_status = self.resource_monitor.check_resource_limits()

            # Update health check timestamp
            self.state.last_health_check = datetime.now().isoformat()

            # Log warnings if resources are high
            if not resource_status["memory_ok"]:
                logger.warning(
                    f"High memory usage: {resource_status['memory_mb']:.1f}MB / "
                    f"{self.config.max_memory_mb}MB"
                )

            if not resource_status["cpu_ok"]:
                logger.warning(
                    f"High CPU usage: {resource_status['cpu_percent']:.1f}% / "
                    f"{self.config.max_cpu_percent}%"
                )

            # Return overall health status
            return resource_status["memory_ok"] and resource_status["cpu_ok"]

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single task with timeout and error handling"""
        task_id = task.get("id", "unknown")
        task_type = task.get("type", "unknown")

        logger.info(f"Executing task {task_id} (type: {task_type})")

        try:
            # Task execution would go here
            # For now, simulate execution
            await asyncio.sleep(1)

            self.state.tasks_completed += 1

            # Estimate token usage (this would be tracked by actual execution)
            estimated_tokens = task.get("estimated_tokens", 1000)
            self.state.tokens_used += estimated_tokens

            return {
                "task_id": task_id,
                "status": "completed",
                "result": "Task executed successfully"
            }

        except asyncio.TimeoutError:
            logger.error(f"Task {task_id} timed out")
            self.state.tasks_failed += 1
            self.health_checker.record_failure()
            return {
                "task_id": task_id,
                "status": "failed",
                "error": "Task execution timeout"
            }

        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
            self.state.tasks_failed += 1
            self.health_checker.record_failure()
            return {
                "task_id": task_id,
                "status": "failed",
                "error": str(e)
            }

    async def task_execution_loop(self):
        """Main task execution loop"""
        logger.info("Starting task execution loop")

        while self.running:
            try:
                # Check for restart condition
                if self.health_checker.should_restart(self.state.tasks_failed):
                    logger.warning("Initiating restart due to failures")
                    self.state.restart_count += 1
                    self.health_checker.record_restart()
                    # In production, this would trigger a restart
                    # For now, just reset failure count
                    self.state.tasks_failed = 0

                # Execute tasks from queue
                if self.task_queue and not self.task_queue.empty():
                    task = await self.task_queue.get()
                    await self.execute_task(task)
                    self.task_queue.task_done()

                # Save state periodically
                await self.save_state()

                # Small sleep to prevent busy waiting
                await asyncio.sleep(0.1)

            except Exception as e:
                logger.error(f"Error in execution loop: {e}")
                await asyncio.sleep(1)

    async def monitoring_loop(self):
        """Health monitoring and resource tracking loop"""
        logger.info("Starting monitoring loop")

        while self.running:
            try:
                # Perform health check
                is_healthy = await self.health_check()

                # Update uptime
                start_time = datetime.fromisoformat(self.state.start_time)
                self.state.uptime_seconds = int((datetime.now() - start_time).total_seconds())

                # Log periodic status
                tokens_per_hour = self.resource_monitor.estimate_tokens_per_hour(
                    self.state.tokens_used,
                    self.state.uptime_seconds
                )

                logger.info(
                    f"Status: {self.state.status} | "
                    f"Tasks: {self.state.tasks_completed} completed, "
                    f"{self.state.tasks_failed} failed | "
                    f"Tokens: {self.state.tokens_used:,} "
                    f"({tokens_per_hour:,}/hour target: {self.config.target_tokens_per_hour:,}) | "
                    f"Uptime: {self.state.uptime_seconds}s"
                )

                # Check if we need more tasks to meet token target
                if tokens_per_hour < self.config.target_tokens_per_hour:
                    logger.info("Below token target, adding more tasks to queue")

                await asyncio.sleep(self.config.health_check_interval)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)

    async def start(self):
        """Start the daemon"""
        logger.info("=" * 60)
        logger.info("BLACKBOX5 Daemon Starting")
        logger.info("=" * 60)
        logger.info(f"PID: {self.state.pid}")
        logger.info(f"Target tokens/day: {self.config.target_tokens_per_day:,}")
        logger.info(f"Target tokens/hour: {self.config.target_tokens_per_hour:,}")
        logger.info(f"Runtime directory: {self.config.runtime_dir}")
        logger.info("=" * 60)

        # Load previous state
        await self.load_state()

        # Initialize task queue
        self.task_queue = asyncio.Queue()

        # Set running flag
        self.running = True
        self.state.status = "running"

        # Start concurrent loops
        try:
            await asyncio.gather(
                self.task_execution_loop(),
                self.monitoring_loop()
            )
        except Exception as e:
            logger.error(f"Fatal error in daemon: {e}")
            self.state.status = "error"
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Graceful shutdown"""
        logger.info("Shutting down daemon...")
        self.running = False
        self.state.status = "stopped"
        await self.save_state()
        logger.info("Daemon shutdown complete")


async def main():
    """Main entry point"""
    config = DaemonConfig()

    # Create and start daemon
    daemon = Blackbox5Daemon(config)

    try:
        await daemon.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
