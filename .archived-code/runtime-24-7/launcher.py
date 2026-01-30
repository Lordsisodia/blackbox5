#!/usr/bin/env python3
"""
BLACKBOX5 24/7 Launcher

Unified launcher for autonomous BLACKBOX5 operation with daemon, scheduler,
discovery, and monitoring integrated for continuous self-improvement.
"""

import asyncio
import sys
import logging
from pathlib import Path
from datetime import datetime
import signal

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from runtime.daemon import Blackbox5Daemon, DaemonConfig
from runtime.scheduler import TaskScheduler, setup_autonomous_tasks
from runtime.discovery import AutonomousDiscovery
from runtime.monitor import ResourceMonitor

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


class Blackbox5Runtime:
    """
    Unified runtime for 24/7 BLACKBOX5 autonomous operation

    Integrates:
    - Daemon for process management
    - Scheduler for task execution
    - Discovery for skill/framework finding
    - Monitor for resource tracking
    """

    def __init__(self, config: DaemonConfig = None):
        self.config = config or DaemonConfig()
        self.daemon = Blackbox5Daemon(self.config)
        self.scheduler = TaskScheduler()
        self.discovery = AutonomousDiscovery()
        self.monitor = ResourceMonitor(
            target_tokens_per_day=self.config.target_tokens_per_day
        )

        self.running = False

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, initiating shutdown...")
        self.running = False

    async def initialize(self):
        """Initialize all components"""
        logger.info("=" * 70)
        logger.info("BLACKBOX5 24/7 Runtime Initializing")
        logger.info("=" * 70)
        logger.info(f"Target tokens/day: {self.config.target_tokens_per_day:,}")
        logger.info(f"Runtime directory: {self.config.runtime_dir}")
        logger.info("=" * 70)

        # Ensure runtime directory exists
        self.config.runtime_dir.mkdir(parents=True, exist_ok=True)

        # Setup autonomous tasks
        await setup_autonomous_tasks(self.scheduler)

        # Add discovery task
        await self.scheduler.schedule_periodic_task(
            name="Autonomous Discovery",
            description="Discover and integrate new skills and frameworks",
            task_type="discovery",
            execute_func=self.discovery.run_discovery_cycle,
            interval_seconds=7200,  # Every 2 hours
            priority=self.scheduler.task_queue.__class__.__dict__.get('TaskPriority', type('TaskPriority', (), {'HIGH': 1})).HIGH if hasattr(self.scheduler.task_queue, '__class__') else 1,
            estimated_tokens=100000
        )

        # Add monitoring task
        await self.scheduler.schedule_periodic_task(
            name="Resource Status Report",
            description="Generate and log resource status report",
            task_type="monitoring",
            execute_func=self._log_status,
            interval_seconds=300,  # Every 5 minutes
            priority=0,  # CRITICAL
            estimated_tokens=100
        )

        logger.info("All components initialized successfully")

    async def _log_status(self):
        """Log current status"""
        self.monitor.log_status()
        return {"status": "logged"}

    async def start(self):
        """Start the 24/7 runtime"""
        await self.initialize()

        logger.info("")
        logger.info("=" * 70)
        logger.info("BLACKBOX5 24/7 Runtime Starting")
        logger.info("=" * 70)
        logger.info("Press Ctrl+C to stop")
        logger.info("")

        self.running = True

        # Start all components concurrently
        try:
            await asyncio.gather(
                self.daemon.start(),
                self.scheduler.start(),
                self.monitor.monitor_loop(interval_seconds=60)
            )
        except Exception as e:
            logger.error(f"Fatal error in runtime: {e}")
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Graceful shutdown"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("BLACKBOX5 24/7 Runtime Shutting Down")
        logger.info("=" * 70)

        self.running = False

        # Save final state
        self.monitor.save_metrics()
        await self.daemon.save_state()
        await self.discovery.save_state()

        # Stop components
        await self.scheduler.stop()

        # Log final status
        self.monitor.log_status()

        logger.info("Shutdown complete")
        logger.info("=" * 70)


def print_banner():
    """Print startup banner"""
    banner = """
╔════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗                      ║
║   ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝                      ║
║   ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗                      ║
║   ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║                      ║
║   ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║                      ║
║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝                      ║
║                                                                      ║
║                    24/7 Autonomous Operation                        ║
║                    Self-Improving AI Infrastructure                  ║
║                                                                      ║
║   Target: 100-200M tokens/day                                       ║
║                                                                      ║
╚════════════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")


async def main():
    """Main entry point"""
    print_banner()

    # Create and start runtime
    config = DaemonConfig(
        target_tokens_per_day=150_000_000,  # 150M tokens/day target
        health_check_interval=30,
        max_concurrent_tasks=10
    )

    runtime = Blackbox5Runtime(config)

    try:
        await runtime.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutdown complete")
