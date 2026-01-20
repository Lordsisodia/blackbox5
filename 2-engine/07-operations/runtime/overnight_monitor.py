#!/usr/bin/env python3
"""
Overnight Stability Monitor for BLACKBOX5

This is a SIMPLE, STABLE monitoring system that:
- Does NOT modify any code
- Does NOT restart the server
- Just monitors health and logs issues
- Runs indefinitely without crashes

Perfect for overnight monitoring when you want to ensure BLACKBOX5 stays healthy
without risking autonomous fixes that might break things.
"""

import asyncio
import aiohttp
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "2-engine" / "01-core"))

# Configure logging
LOG_DIR = Path("/tmp")
LOG_FILE = LOG_DIR / "blackbox5_overnight.log"
HEALTH_LOG = LOG_DIR / "blackbox5_health.jsonl"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "http://localhost:8000"
CHECK_INTERVAL = 60  # Check every 60 seconds
TIMEOUT = 10  # 10 second timeout for health checks


class OvernightMonitor:
    """Simple overnight health monitor for BLACKBOX5"""

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.start_time = datetime.now()
        self.check_count = 0
        self.failure_count = 0
        self.consecutive_failures = 0

    async def check_health(self) -> bool:
        """
        Check if BLACKBOX5 API is healthy.

        Returns:
            True if healthy, False otherwise
        """
        try:
            async with self.session.get(
                f"{BASE_URL}/health",
                timeout=aiohttp.ClientTimeout(total=TIMEOUT)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.debug(f"Health check passed: {data}")
                    return True
                else:
                    logger.warning(f"Health check failed with status {response.status}")
                    return False
        except asyncio.TimeoutError:
            logger.warning("Health check timed out")
            return False
        except aiohttp.ClientError as e:
            logger.warning(f"Health check failed with error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during health check: {e}")
            return False

    async def check_agents_list(self) -> bool:
        """
        Check if agents list endpoint works.

        Returns:
            True if successful, False otherwise
        """
        try:
            async with self.session.get(
                f"{BASE_URL}/agents",
                timeout=aiohttp.ClientTimeout(total=TIMEOUT)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    agent_count = len(data.get('agents', []))
                    logger.debug(f"Agents check passed: {agent_count} agents available")
                    return True
                else:
                    logger.warning(f"Agents check failed with status {response.status}")
                    return False
        except Exception as e:
            logger.warning(f"Agents check failed: {e}")
            return False

    async def log_health_status(self, healthy: bool):
        """
        Log health status to JSONL file for analysis.

        Args:
            healthy: Whether the system is healthy
        """
        timestamp = datetime.now().isoformat()
        uptime = (datetime.now() - self.start_time).total_seconds()

        status = {
            "timestamp": timestamp,
            "healthy": healthy,
            "uptime_seconds": uptime,
            "check_number": self.check_count,
            "total_failures": self.failure_count,
            "consecutive_failures": self.consecutive_failures
        }

        with open(HEALTH_LOG, 'a') as f:
            f.write(f"{status}\n")

    async def run_once(self) -> bool:
        """
        Run a single monitoring cycle.

        Returns:
            True if system is healthy, False otherwise
        """
        self.check_count += 1
        logger.info(f"--- Health check #{self.check_count} ---")

        # Check basic health endpoint
        health_ok = await self.check_health()

        # Check agents endpoint
        agents_ok = await self.check_agents_list()

        # System is healthy if all checks pass
        is_healthy = health_ok and agents_ok

        if not is_healthy:
            self.failure_count += 1
            self.consecutive_failures += 1
            logger.error(
                f"HEALTH CHECK FAILED! "
                f"Health: {health_ok}, Agents: {agents_ok}, "
                f"Consecutive failures: {self.consecutive_failures}"
            )

            # Alert if we have 3+ consecutive failures
            if self.consecutive_failures >= 3:
                logger.critical(
                    f"⚠️  ALERT: {self.consecutive_failures} consecutive failures! "
                    f"BLACKBOX5 may be down!"
                )
        else:
            self.consecutive_failures = 0
            uptime_minutes = (datetime.now() - self.start_time).total_seconds() / 60
            logger.info(
                f"✓ System healthy | "
                f"Uptime: {uptime_minutes:.1f} min | "
                f"Failures: {self.failure_count}/{self.check_count}"
            )

        # Log to file
        await self.log_health_status(is_healthy)

        return is_healthy

    async def run(self):
        """
        Run the monitor indefinitely.

        This will run until manually stopped (Ctrl+C).
        """
        logger.info("=" * 60)
        logger.info("BLACKBOX5 Overnight Stability Monitor Starting")
        logger.info(f"Base URL: {BASE_URL}")
        logger.info(f"Check interval: {CHECK_INTERVAL}s")
        logger.info(f"Log file: {LOG_FILE}")
        logger.info(f"Health data: {HEALTH_LOG}")
        logger.info("=" * 60)

        # Create HTTP session
        timeout = aiohttp.ClientTimeout(total=TIMEOUT)
        self.session = aiohttp.ClientSession(timeout=timeout)

        try:
            # Initial health check
            logger.info("Performing initial health check...")
            if not await self.run_once():
                logger.warning("⚠️  Initial health check failed! BLACKBOX5 may not be running.")

            # Main monitoring loop
            logger.info(f"Starting monitoring loop (checking every {CHECK_INTERVAL}s)...")
            logger.info("Press Ctrl+C to stop monitoring\n")

            while True:
                await asyncio.sleep(CHECK_INTERVAL)
                await self.run_once()

        except asyncio.CancelledError:
            logger.info("Monitoring cancelled")
        except KeyboardInterrupt:
            logger.info("\nMonitoring stopped by user (Ctrl+C)")
        except Exception as e:
            logger.critical(f"Fatal error in monitoring loop: {e}", exc_info=True)
        finally:
            # Cleanup
            if self.session:
                await self.session.close()

            # Print summary
            self.print_summary()

    def print_summary(self):
        """Print monitoring summary"""
        uptime = (datetime.now() - self.start_time).total_seconds() / 60
        success_rate = ((self.check_count - self.failure_count) / self.check_count * 100) if self.check_count > 0 else 0

        logger.info("=" * 60)
        logger.info("MONITORING SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total uptime: {uptime:.1f} minutes")
        logger.info(f"Total checks: {self.check_count}")
        logger.info(f"Successful checks: {self.check_count - self.failure_count}")
        logger.info(f"Failed checks: {self.failure_count}")
        logger.info(f"Success rate: {success_rate:.1f}%")
        logger.info(f"Log file: {LOG_FILE}")
        logger.info(f"Health data: {HEALTH_LOG}")
        logger.info("=" * 60)


async def main():
    """Main entry point"""
    monitor = OvernightMonitor()
    await monitor.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nShutdown complete")
