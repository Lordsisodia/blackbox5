"""
BLACKBOX5 Resource Monitor - Token Usage & Performance Tracking

Comprehensive monitoring for token utilization, cost tracking, and performance metrics
to achieve 100-200M tokens/day target.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
import json
import psutil

logger = logging.getLogger(__name__)


@dataclass
class TokenUsage:
    """Token usage tracking"""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

    def add(self, input_tokens: int, output_tokens: int):
        """Add token usage"""
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.total_tokens += input_tokens + output_tokens


@dataclass
class TaskMetrics:
    """Task execution metrics"""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    avg_task_duration_seconds: float = 0.0
    total_task_duration_seconds: float = 0.0


@dataclass
class ResourceSnapshot:
    """System resource snapshot"""
    timestamp: str
    memory_mb: float
    memory_percent: float
    cpu_percent: float
    disk_usage_percent: float
    active_connections: int = 0


@dataclass
class HourlyMetrics:
    """Metrics for an hour"""
    hour: str
    tokens_used: int = 0
    tasks_completed: int = 0
    avg_cpu_percent: float = 0.0
    avg_memory_mb: float = 0.0
    cost_estimate_usd: float = 0.0


class TokenTracker:
    """Track token usage and costs"""

    # Pricing (example for Claude - adjust as needed)
    INPUT_COST_PER_1K = 0.003  # $0.003 per 1K input tokens
    OUTPUT_COST_PER_1K = 0.015  # $0.015 per 1K output tokens

    def __init__(self):
        self.usage = TokenUsage()
        self.hourly_usage: Dict[str, TokenUsage] = {}

    def record_usage(self, input_tokens: int, output_tokens: int):
        """Record token usage"""
        self.usage.add(input_tokens, output_tokens)

        # Track hourly
        hour_key = datetime.now().strftime("%Y-%m-%d-%H")
        if hour_key not in self.hourly_usage:
            self.hourly_usage[hour_key] = TokenUsage()
        self.hourly_usage[hour_key].add(input_tokens, output_tokens)

    def get_total_cost(self) -> float:
        """Calculate total cost in USD"""
        input_cost = (self.usage.input_tokens / 1000) * self.INPUT_COST_PER_1K
        output_cost = (self.usage.output_tokens / 1000) * self.OUTPUT_COST_PER_1K
        return input_cost + output_cost

    def get_hourly_cost(self, hour: str) -> float:
        """Get cost for a specific hour"""
        if hour not in self.hourly_usage:
            return 0.0
        usage = self.hourly_usage[hour]
        input_cost = (usage.input_tokens / 1000) * self.INPUT_COST_PER_1K
        output_cost = (usage.output_tokens / 1000) * self.OUTPUT_COST_PER_1K
        return input_cost + output_cost

    def get_tokens_last_hour(self) -> int:
        """Get tokens used in the last hour"""
        hour_key = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d-%H")
        if hour_key in self.hourly_usage:
            return self.hourly_usage[hour_key].total_tokens
        return 0

    def get_tokens_today(self) -> int:
        """Get total tokens used today"""
        today = datetime.now().strftime("%Y-%m-%d")
        total = 0
        for hour_key, usage in self.hourly_usage.items():
            if hour_key.startswith(today):
                total += usage.total_tokens
        return total

    def estimate_daily_tokens(self) -> int:
        """Estimate total tokens for the day based on current rate"""
        current_hour = datetime.now().strftime("%Y-%m-%d-%H")
        if current_hour in self.hourly_usage:
            tokens_this_hour = self.hourly_usage[current_hour].total_tokens
            hours_passed = datetime.now().hour + 1
            if hours_passed > 0:
                avg_per_hour = self.get_tokens_today() / hours_passed
                return int(avg_per_hour * 24)
        return 0


class PerformanceMonitor:
    """Monitor system performance"""

    def __init__(self):
        self.process = psutil.Process()
        self.snapshots: List[ResourceSnapshot] = []
        self.max_snapshots = 1440  # Keep 24 hours of minute-by-minute snapshots

    def take_snapshot(self) -> ResourceSnapshot:
        """Capture current resource usage"""
        memory_info = self.process.memory_info()
        snapshot = ResourceSnapshot(
            timestamp=datetime.now().isoformat(),
            memory_mb=memory_info.rss / 1024 / 1024,
            memory_percent=self.process.memory_percent(),
            cpu_percent=self.process.cpu_percent(),
            disk_usage_percent=psutil.disk_usage('/').percent
        )

        self.snapshots.append(snapshot)

        # Keep only recent snapshots
        if len(self.snapshots) > self.max_snapshots:
            self.snapshots = self.snapshots[-self.max_snapshots:]

        return snapshot

    def get_avg_resources_last_hour(self) -> Dict[str, float]:
        """Get average resource usage over the last hour"""
        cutoff = datetime.now() - timedelta(hours=1)
        recent = [s for s in self.snapshots if datetime.fromisoformat(s.timestamp) > cutoff]

        if not recent:
            return {"cpu_percent": 0.0, "memory_mb": 0.0}

        return {
            "cpu_percent": sum(s.cpu_percent for s in recent) / len(recent),
            "memory_mb": sum(s.memory_mb for s in recent) / len(recent)
        }

    def get_peak_resources(self) -> Dict[str, Any]:
        """Get peak resource usage"""
        if not self.snapshots:
            return {"cpu_percent": 0, "memory_mb": 0}

        return {
            "cpu_percent": max(s.cpu_percent for s in self.snapshots),
            "memory_mb": max(s.memory_mb for s in self.snapshots),
            "timestamp": max(s.snapshots, key=lambda x: x.cpu_percent).timestamp
        }


class ResourceMonitor:
    """
    Comprehensive resource monitoring for BLACKBOX5

    Tracks:
    - Token usage and costs
    - Task execution metrics
    - System resources (CPU, memory, disk)
    - Performance trends
    """

    def __init__(self, target_tokens_per_day: int = 150_000_000):
        self.target_tokens_per_day = target_tokens_per_day
        self.target_tokens_per_hour = target_tokens_per_day / 24

        self.token_tracker = TokenTracker()
        self.performance_monitor = PerformanceMonitor()
        self.task_metrics = TaskMetrics()

        self.start_time = datetime.now()
        self.metrics_file = Path("./.runtime/metrics.jsonl")

    def record_task_execution(
        self,
        duration_seconds: float,
        input_tokens: int,
        output_tokens: int,
        success: bool
    ):
        """Record task execution metrics"""
        # Update token tracking
        self.token_tracker.record_usage(input_tokens, output_tokens)

        # Update task metrics
        self.task_metrics.total_tasks += 1
        self.task_metrics.total_task_duration_seconds += duration_seconds

        if success:
            self.task_metrics.completed_tasks += 1
        else:
            self.task_metrics.failed_tasks += 1

        # Update average duration
        if self.task_metrics.total_tasks > 0:
            self.task_metrics.avg_task_duration_seconds = (
                self.task_metrics.total_task_duration_seconds / self.task_metrics.total_tasks
            )

    def get_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report"""

        uptime = datetime.now() - self.start_time
        tokens_today = self.token_tracker.get_tokens_today()
        tokens_last_hour = self.token_tracker.get_tokens_last_hour()
        estimated_daily = self.token_tracker.estimate_daily_tokens()

        # Calculate progress toward target
        target_progress = (tokens_today / self.target_tokens_per_day) * 100
        hour_progress = ((datetime.now().hour + 1) / 24) * 100

        avg_resources = self.performance_monitor.get_avg_resources_last_hour()
        peak_resources = self.performance_monitor.get_peak_resources()

        return {
            "uptime": str(uptime).split('.')[0],
            "token_usage": {
                "total_today": tokens_today,
                "last_hour": tokens_last_hour,
                "estimated_daily": estimated_daily,
                "target_daily": self.target_tokens_per_day,
                "target_progress": f"{target_progress:.1f}%",
                "hour_progress": f"{hour_progress:.1f}%",
                "on_track": target_progress >= hour_progress * 0.8  # Allow some buffer
            },
            "costs": {
                "total_cost": f"${self.token_tracker.get_total_cost():.2f}",
                "cost_per_hour": f"${self.token_tracker.get_hourly_cost(datetime.now().strftime('%Y-%m-%d-%H')):.4f}"
            },
            "tasks": {
                "total": self.task_metrics.total_tasks,
                "completed": self.task_metrics.completed_tasks,
                "failed": self.task_metrics.failed_tasks,
                "success_rate": f"{(self.task_metrics.completed_tasks / self.task_metrics.total_tasks * 100) if self.task_metrics.total_tasks > 0 else 0:.1f}%",
                "avg_duration": f"{self.task_metrics.avg_task_duration_seconds:.1f}s"
            },
            "resources": {
                "current_cpu": f"{avg_resources['cpu_percent']:.1f}%",
                "current_memory": f"{avg_resources['memory_mb']:.0f}MB",
                "peak_cpu": f"{peak_resources['cpu_percent']:.1f}%",
                "peak_memory": f"{peak_resources['memory_mb']:.0f}MB"
            },
            "hourly_breakdown": self._get_hourly_breakdown()
        }

    def _get_hourly_breakdown(self) -> List[Dict[str, Any]]:
        """Get hourly breakdown for today"""
        today = datetime.now().strftime("%Y-%m-%d")
        hourly = []

        for hour in range(24):
            hour_key = f"{today}-{hour:02d}"
            if hour_key in self.token_tracker.hourly_usage:
                usage = self.token_tracker.hourly_usage[hour_key]
                hourly.append({
                    "hour": f"{hour:02d}:00",
                    "tokens": usage.total_tokens,
                    "cost": f"${self.token_tracker.get_hourly_cost(hour_key):.4f}"
                })

        return hourly

    def log_status(self):
        """Log current status"""
        report = self.get_status_report()

        logger.info("=" * 60)
        logger.info("BLACKBOX5 Resource Monitor Status")
        logger.info("=" * 60)
        logger.info(f"Uptime: {report['uptime']}")
        logger.info("")
        logger.info("Token Usage:")
        logger.info(f"  Today: {report['token_usage']['total_today']:,} / {report['token_usage']['target_daily']:,}")
        logger.info(f"  Progress: {report['token_usage']['target_progress']} (Hour: {report['token_usage']['hour_progress']})")
        logger.info(f"  Last Hour: {report['token_usage']['last_hour']:,}")
        logger.info(f"  Est. Daily: {report['token_usage']['estimated_daily']:,}")
        logger.info(f"  On Track: {'✓' if report['token_usage']['on_track'] else '✗'}")
        logger.info("")
        logger.info("Costs:")
        logger.info(f"  Total: {report['costs']['total_cost']}")
        logger.info(f"  This Hour: {report['costs']['cost_per_hour']}")
        logger.info("")
        logger.info("Tasks:")
        logger.info(f"  Total: {report['tasks']['total']} | Completed: {report['tasks']['completed']} | Failed: {report['tasks']['failed']}")
        logger.info(f"  Success Rate: {report['tasks']['success_rate']}")
        logger.info(f"  Avg Duration: {report['tasks']['avg_duration']}")
        logger.info("")
        logger.info("Resources:")
        logger.info(f"  CPU: {report['resources']['current_cpu']} | Memory: {report['resources']['current_memory']}")
        logger.info(f"  Peak CPU: {report['resources']['peak_cpu']} | Peak Memory: {report['resources']['peak_memory']}")
        logger.info("=" * 60)

    async def monitor_loop(self, interval_seconds: int = 60):
        """Continuous monitoring loop"""
        logger.info("Starting resource monitor loop")

        while True:
            try:
                # Take resource snapshot
                self.performance_monitor.take_snapshot()

                # Log status every 5 minutes
                if datetime.now().minute % 5 == 0:
                    self.log_status()

                await asyncio.sleep(interval_seconds)

            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                await asyncio.sleep(5)

    def save_metrics(self):
        """Save metrics to file"""
        try:
            report = self.get_status_report()
            self.metrics_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.metrics_file, 'a') as f:
                f.write(json.dumps({
                    "timestamp": datetime.now().isoformat(),
                    **report
                }) + '\n')

        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")
