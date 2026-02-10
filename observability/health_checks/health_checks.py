#!/usr/bin/env python3
"""
Health Check Endpoints for BlackBox5 Observability System.

Provides HTTP endpoints for checking the health of all services:
- Database connectivity
- Redis status
- NATS status
- Agent liveness
- API status
- Cron job status
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Parent imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "bin" / "lib"))

from health_monitor.config import get_config
from health_monitor.collectors import collect_queue, collect_heartbeat
from health_monitor.database import _get_connection

try:
    import redis
except ImportError:
    redis = None
    REDIS_AVAILABLE = False
else:
    REDIS_AVAILABLE = True

try:
    import nats
    from nats.js.api import StreamConfig, ConsumerConfig
except ImportError:
    nats = None
    NATS_AVAILABLE = False
else:
    NATS_AVAILABLE = True

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status levels."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheckResult:
    """Result of a single health check."""
    name: str
    status: HealthStatus
    message: str
    response_time_ms: float
    details: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.message,
            "response_time_ms": self.response_time_ms,
            "details": self.details,
        }


class HealthChecker:
    """Main health check coordinator."""

    def __init__(
        self,
        redis_host: str = "77.42.66.40",
        redis_port: int = 6379,
        redis_password: Optional[str] = None,
        nats_url: str = "nats://77.42.66.40:4222",
    ):
        """Initialize health checker."""
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.nats_url = nats_url

        self._redis_client: Optional[redis.Redis] = None
        self._nats_client: Optional[nats.NATS] = None

    def check_all(self) -> Dict[str, HealthCheckResult]:
        """Run all health checks."""
        results = {}

        # Database health
        results["database"] = self.check_database()

        # Redis health
        if REDIS_AVAILABLE:
            results["redis"] = self.check_redis()

        # NATS health
        if NATS_AVAILABLE:
            results["nats"] = self.check_nats()

        # Agent health
        results["agents"] = self.check_agents()

        # Queue health
        results["queue"] = self.check_queue()

        return results

    def check_database(self) -> HealthCheckResult:
        """Check database connectivity."""
        start = datetime.now()
        try:
            with _get_connection() as conn:
                conn.execute("SELECT 1").fetchone()

            response_time = (datetime.now() - start).total_seconds() * 1000

            if response_time < 100:
                status = HealthStatus.HEALTHY
            elif response_time < 500:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.UNHEALTHY

            return HealthCheckResult(
                name="database",
                status=status,
                message=f"Database response time: {response_time:.2f}ms",
                response_time_ms=response_time,
            )
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return HealthCheckResult(
                name="database",
                status=HealthStatus.UNHEALTHY,
                message=f"Database error: {str(e)}",
                response_time_ms=(datetime.now() - start).total_seconds() * 1000,
            )

    def check_redis(self) -> HealthCheckResult:
        """Check Redis connectivity."""
        start = datetime.now()
        try:
            client = self._get_redis()
            if not client:
                return HealthCheckResult(
                    name="redis",
                    status=HealthStatus.UNKNOWN,
                    message="Redis client not available",
                    response_time_ms=0,
                )

            info = client.info()
            response_time = (datetime.now() - start).total_seconds() * 1000

            connected_clients = info.get('connected_clients', 0)
            used_memory = info.get('used_memory_human', 'N/A')

            if response_time < 50:
                status = HealthStatus.HEALTHY
            elif response_time < 200:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.UNHEALTHY

            return HealthCheckResult(
                name="redis",
                status=status,
                message=f"Redis response time: {response_time:.2f}ms",
                response_time_ms=response_time,
                details={
                    "connected_clients": connected_clients,
                    "used_memory": used_memory,
                    "uptime": info.get('uptime_in_seconds', 0),
                },
            )
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return HealthCheckResult(
                name="redis",
                status=HealthStatus.UNHEALTHY,
                message=f"Redis error: {str(e)}",
                response_time_ms=(datetime.now() - start).total_seconds() * 1000,
            )

    def check_nats(self) -> HealthCheckResult:
        """Check NATS connectivity."""
        start = datetime.now()
        try:
            client = self._get_nats()
            if not client:
                return HealthCheckResult(
                    name="nats",
                    status=HealthStatus.UNKNOWN,
                    message="NATS client not available",
                    response_time_ms=0,
                )

            # Get JetStream status
            js = client.jetstream()
            streams = js.stream_info_get()

            response_time = (datetime.now() - start).total_seconds() * 1000

            if response_time < 100:
                status = HealthStatus.HEALTHY
            elif response_time < 300:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.UNHEALTHY

            return HealthCheckResult(
                name="nats",
                status=status,
                message=f"NATS JetStream response time: {response_time:.2f}ms",
                response_time_ms=response_time,
                details={
                    "streams": len(streams.config.subjects) if streams else 0,
                },
            )
        except Exception as e:
            logger.error(f"NATS health check failed: {e}")
            return HealthCheckResult(
                name="nats",
                status=HealthStatus.UNHEALTHY,
                message=f"NATS error: {str(e)}",
                response_time_ms=(datetime.now() - start).total_seconds() * 1000,
            )

    def check_agents(self) -> HealthCheckResult:
        """Check all agent heartbeats."""
        start = datetime.now()
        try:
            agents = collect_heartbeat()

            online = sum(1 for a in agents if a.is_online())
            stale = sum(1 for a in agents if a.is_stale())
            offline = len(agents) - online - stale

            response_time = (datetime.now() - start).total_seconds() * 1000

            if stale == 0 and offline == 0:
                status = HealthStatus.HEALTHY
                message = f"All {online} agents online"
            elif stale > 0 and offline == 0:
                status = HealthStatus.DEGRADED
                message = f"{online} online, {stale} stale"
            else:
                status = HealthStatus.UNHEALTHY
                message = f"{online} online, {stale} stale, {offline} offline"

            # Agent details
            agent_details = {}
            for agent in agents:
                agent_details[agent.name] = {
                    "status": agent.get_status().value,
                    "last_seen": agent.last_seen.isoformat(),
                    "seconds_since_seen": agent.seconds_since_seen(),
                    "current_task": agent.current_task,
                }

            return HealthCheckResult(
                name="agents",
                status=status,
                message=message,
                response_time_ms=response_time,
                details={
                    "total": len(agents),
                    "online": online,
                    "stale": stale,
                    "offline": offline,
                    "agents": agent_details,
                },
            )
        except Exception as e:
            logger.error(f"Agent health check failed: {e}")
            return HealthCheckResult(
                name="agents",
                status=HealthStatus.UNHEALTHY,
                message=f"Agent error: {str(e)}",
                response_time_ms=(datetime.now() - start).total_seconds() * 1000,
            )

    def check_queue(self) -> HealthCheckResult:
        """Check task queue health."""
        start = datetime.now()
        try:
            tasks = collect_queue()

            pending = sum(1 for t in tasks if t.is_pending)
            in_progress = sum(1 for t in tasks if t.is_in_progress)
            completed = sum(1 for t in tasks if t.is_completed)

            response_time = (datetime.now() - start).total_seconds() * 1000

            # Check for stuck tasks
            stuck_count = 0
            for task in tasks:
                if task.is_in_progress and task.elapsed_minutes():
                    if task.elapsed_minutes() > 120:  # 2 hours
                        stuck_count += 1

            if stuck_count == 0:
                status = HealthStatus.HEALTHY
                message = f"Queue healthy: {pending} pending, {in_progress} in progress"
            elif stuck_count < 3:
                status = HealthStatus.DEGRADED
                message = f"Queue degraded: {stuck_count} tasks stuck"
            else:
                status = HealthStatus.UNHEALTHY
                message = f"Queue unhealthy: {stuck_count} tasks stuck"

            return HealthCheckResult(
                name="queue",
                status=status,
                message=message,
                response_time_ms=response_time,
                details={
                    "pending": pending,
                    "in_progress": in_progress,
                    "completed": completed,
                    "stuck": stuck_count,
                    "total": len(tasks),
                },
            )
        except Exception as e:
            logger.error(f"Queue health check failed: {e}")
            return HealthCheckResult(
                name="queue",
                status=HealthStatus.UNHEALTHY,
                message=f"Queue error: {str(e)}",
                response_time_ms=(datetime.now() - start).total_seconds() * 1000,
            )

    def check_agent(self, agent_name: str, timeout_seconds: int = 120) -> HealthCheckResult:
        """Check a specific agent's health."""
        start = datetime.now()
        try:
            agents = collect_heartbeat()

            agent = next((a for a in agents if a.name == agent_name), None)

            if not agent:
                return HealthCheckResult(
                    name=f"agent:{agent_name}",
                    status=HealthStatus.UNKNOWN,
                    message=f"Agent {agent_name} not found",
                    response_time_ms=(datetime.now() - start).total_seconds() * 1000,
                )

            response_time = (datetime.now() - start).total_seconds() * 1000

            if agent.is_online(timeout_seconds):
                status = HealthStatus.HEALTHY
                message = f"Agent {agent_name} online"
            elif agent.is_stale(timeout_seconds):
                status = HealthStatus.DEGRADED
                message = f"Agent {agent_name} stale (last seen {agent.seconds_since_seen()}s ago)"
            else:
                status = HealthStatus.UNHEALTHY
                message = f"Agent {agent_name} offline"

            return HealthCheckResult(
                name=f"agent:{agent_name}",
                status=status,
                message=message,
                response_time_ms=response_time,
                details={
                    "last_seen": agent.last_seen.isoformat(),
                    "seconds_since_seen": agent.seconds_since_seen(),
                    "current_task": agent.current_task,
                    "loop_number": agent.loop_number,
                },
            )
        except Exception as e:
            logger.error(f"Agent {agent_name} health check failed: {e}")
            return HealthCheckResult(
                name=f"agent:{agent_name}",
                status=HealthStatus.UNHEALTHY,
                message=f"Error: {str(e)}",
                response_time_ms=(datetime.now() - start).total_seconds() * 1000,
            )

    def check_cron_jobs(self) -> HealthCheckResult:
        """Check cron job status (if cron status tracking is implemented)."""
        start = datetime.now()
        try:
            config = get_config()

            # Check for cron status file
            cron_status_file = config.bb5_root / ".autonomous" / "cron_status.yaml"

            if not cron_status_file.exists():
                return HealthCheckResult(
                    name="cron",
                    status=HealthStatus.UNKNOWN,
                    message="Cron status tracking not implemented",
                    response_time_ms=(datetime.now() - start).total_seconds() * 1000,
                )

            # Read and parse cron status
            import yaml
            with open(cron_status_file) as f:
                cron_data = yaml.safe_load(f) or {}

            jobs = cron_data.get("jobs", [])
            failed = [j for j in jobs if j.get("status") == "failed"]
            running = [j for j in jobs if j.get("status") == "running"]

            response_time = (datetime.now() - start).total_seconds() * 1000

            if not failed:
                status = HealthStatus.HEALTHY
                message = f"All {len(jobs)} cron jobs healthy"
            elif len(failed) < 3:
                status = HealthStatus.DEGRADED
                message = f"{len(failed)} cron jobs failed"
            else:
                status = HealthStatus.UNHEALTHY
                message = f"{len(failed)} cron jobs failed"

            return HealthCheckResult(
                name="cron",
                status=status,
                message=message,
                response_time_ms=response_time,
                details={
                    "total_jobs": len(jobs),
                    "running": len(running),
                    "failed": len(failed),
                    "jobs": jobs,
                },
            )
        except Exception as e:
            logger.error(f"Cron health check failed: {e}")
            return HealthCheckResult(
                name="cron",
                status=HealthStatus.UNKNOWN,
                message=f"Error: {str(e)}",
                response_time_ms=(datetime.now() - start).total_seconds() * 1000,
            )

    def _get_redis(self) -> Optional[redis.Redis]:
        """Get or create Redis client."""
        if not REDIS_AVAILABLE:
            return None

        if self._redis_client is None:
            try:
                self._redis_client = redis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    password=self.redis_password,
                    decode_responses=True,
                )
                self._redis_client.ping()
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                self._redis_client = None

        return self._redis_client

    def _get_nats(self) -> Optional[nats.NATS]:
        """Get or create NATS client."""
        if not NATS_AVAILABLE:
            return None

        if self._nats_client is None:
            try:
                self._nats_client = nats.connect(self.nats_url)
            except Exception as e:
                logger.error(f"Failed to connect to NATS: {e}")
                self._nats_client = None

        return self._nats_client

    async def close(self):
        """Close connections."""
        if self._nats_client:
            await self._nats_client.close()


def main():
    """CLI for health checks."""
    import argparse

    parser = argparse.ArgumentParser(description="BlackBox5 Health Checks")
    parser.add_argument("--all", action="store_true", help="Check all services")
    parser.add_argument("--database", action="store_true", help="Check database")
    parser.add_argument("--redis", action="store_true", help="Check Redis")
    parser.add_argument("--nats", action="store_true", help="Check NATS")
    parser.add_argument("--agents", action="store_true", help="Check all agents")
    parser.add_argument("--agent", type=str, help="Check specific agent")
    parser.add_argument("--queue", action="store_true", help="Check task queue")
    parser.add_argument("--cron", action="store_true", help="Check cron jobs")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    checker = HealthChecker()

    # Default to all if no specific check requested
    if not any([args.all, args.database, args.redis, args.nats, args.agents,
                args.agent, args.queue, args.cron]):
        args.all = True

    results = {}

    if args.all or args.database:
        results["database"] = checker.check_database()

    if args.all or args.redis:
        results["redis"] = checker.check_redis()

    if args.all or args.nats:
        results["nats"] = checker.check_nats()

    if args.all or args.agents:
        results["agents"] = checker.check_agents()

    if args.agent:
        results[f"agent:{args.agent}"] = checker.check_agent(args.agent)

    if args.all or args.queue:
        results["queue"] = checker.check_queue()

    if args.all or args.cron:
        results["cron"] = checker.check_cron_jobs()

    # Output results
    if args.json:
        output = {
            "timestamp": datetime.now().isoformat(),
            "checks": {k: v.to_dict() for k, v in results.items()},
        }
        print(json.dumps(output, indent=2, default=str))
    else:
        print("🏥 BlackBox5 Health Check")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print()

        for name, result in results.items():
            status_emoji = {
                "healthy": "✅",
                "degraded": "⚠️",
                "unhealthy": "❌",
                "unknown": "❓",
            }.get(result.status.value, "❓")

            print(f"{status_emoji} {name.upper()}: {result.message}")
            if result.details:
                for key, value in result.details.items():
                    if isinstance(value, dict):
                        continue  # Skip nested dicts for cleaner output
                    print(f"   {key}: {value}")
            print()

        # Overall status
        overall = min([r.status for r in results.values()], key=lambda s: ["healthy", "degraded", "unhealthy", "unknown"].index(s.value))
        overall_emoji = {
            "healthy": "✅",
            "degraded": "⚠️",
            "unhealthy": "❌",
            "unknown": "❓",
        }.get(overall.value, "❓")

        print(f"{overall_emoji} Overall Status: {overall.value.upper()}")


if __name__ == "__main__":
    main()
