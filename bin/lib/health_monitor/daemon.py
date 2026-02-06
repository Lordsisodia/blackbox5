"""Daemon implementation for BB5 Health Monitor."""

import json
import logging
import os
import signal
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from .collectors import collect_queue, collect_heartbeat, collect_events, collect_metrics
from .calculators import calculate_health_score, detect_stuck_tasks
from .database import init_database, save_snapshot
from .models import HealthSnapshot
from .alerts import AlertManager, AlertConfig

logger = logging.getLogger(__name__)


@dataclass
class DaemonConfig:
    """Configuration for the monitoring daemon."""
    check_interval_seconds: int = 30
    health_score_threshold: int = 60
    alert_cooldown_seconds: int = 300
    heartbeat_timeout_seconds: int = 120
    stuck_task_multiplier: float = 2.0
    pid_file: Path = Path("/tmp/bb5-watch.pid")
    log_file: Optional[Path] = None


class MonitoringDaemon:
    """BB5 Health Monitoring Daemon."""

    def __init__(self, config: DaemonConfig, alert_manager: Optional[AlertManager] = None):
        self.config = config
        self.alert_manager = alert_manager
        self.running = False
        self.last_check: Optional[datetime] = None
        self.health_score = 100
        self.status = "healthy"

    def run(self) -> None:
        """Main monitoring loop."""
        logger.info("Starting BB5 Watch daemon")
        self.running = True

        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGHUP, self._handle_reload)

        # Initialize database
        init_database()

        while self.running:
            try:
                self._check_all()
                self.last_check = datetime.now()
                time.sleep(self.config.check_interval_seconds)
            except Exception as e:
                logger.error(f"Check failed: {e}", exc_info=True)
                time.sleep(self.config.check_interval_seconds)

        logger.info("BB5 Watch daemon stopped")

    def _handle_signal(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

    def _handle_reload(self, signum, frame):
        """Handle reload signal."""
        logger.info("Received SIGHUP, reloading configuration...")
        # Configuration reload would happen here

    def _check_all(self) -> None:
        """Run all enabled checks."""
        logger.debug("Running health checks")

        # Collect data
        tasks = collect_queue()
        agents = collect_heartbeat()
        events = collect_events()
        metrics = collect_metrics()

        # Calculate health score
        score, status, details = calculate_health_score(
            tasks, agents, events, metrics,
            timeout_seconds=self.config.heartbeat_timeout_seconds
        )

        self.health_score = score
        self.status = status.value

        # Detect stuck tasks
        stuck = detect_stuck_tasks(tasks, events, multiplier=self.config.stuck_task_multiplier)

        # Create snapshot
        pending = sum(1 for t in tasks if t.is_pending)
        in_progress = sum(1 for t in tasks if t.is_in_progress)
        completed = sum(1 for t in tasks if t.is_completed)
        online = sum(1 for a in agents if a.is_online())
        stale = sum(1 for a in agents if a.is_stale())

        snapshot = HealthSnapshot(
            timestamp=datetime.now(),
            health_score=score,
            status=status,
            queue_pending=pending,
            queue_in_progress=in_progress,
            queue_completed=completed,
            agents_online=online,
            agents_stale=stale,
            agents_total=len(agents),
            stuck_tasks=len(stuck),
        )

        # Save to database
        save_snapshot(snapshot, details)

        # Send alerts if needed
        if self.alert_manager:
            self._send_alerts(score, status, agents, stuck, tasks)

        logger.info(f"Health check complete: {score}/100 ({status.value})")

    def _send_alerts(self, score: int, status, agents: list, stuck: list, tasks: list) -> None:
        """Send alerts for critical issues."""
        # Alert on critical health score
        if score < self.config.health_score_threshold:
            self.alert_manager.send_alert(
                severity="critical",
                component="health_score",
                message=f"Health score dropped to {score}/100",
                context={
                    "health_score": score,
                    "queue": {
                        "pending": sum(1 for t in tasks if t.is_pending),
                        "in_progress": sum(1 for t in tasks if t.is_in_progress),
                    }
                }
            )

        # Alert on stale agents
        for agent in agents:
            if agent.is_stale(self.config.heartbeat_timeout_seconds):
                self.alert_manager.send_alert(
                    severity="critical",
                    component=f"agent:{agent.name}",
                    message=f"Agent {agent.name} timeout - no heartbeat for {agent.seconds_since_seen()}s",
                    context={"agent": agent.to_dict()}
                )

        # Alert on stuck tasks
        for stuck_task in stuck:
            self.alert_manager.send_alert(
                severity="warning",
                component=f"task:{stuck_task.task.id}",
                message=f"Task {stuck_task.task.id} stuck for {stuck_task.stuck_duration}",
                context={"task": stuck_task.task.to_dict()}
            )


class PIDManager:
    """Manages PID file for daemon."""

    def __init__(self, pid_file: Path):
        self.pid_file = pid_file

    def write(self) -> bool:
        """Write PID to file."""
        try:
            self.pid_file.write_text(str(os.getpid()))
            return True
        except Exception as e:
            logger.error(f"Failed to write PID file: {e}")
            return False

    def read(self) -> Optional[int]:
        """Read PID from file."""
        try:
            if self.pid_file.exists():
                return int(self.pid_file.read_text().strip())
        except Exception as e:
            logger.error(f"Failed to read PID file: {e}")
        return None

    def remove(self) -> None:
        """Remove PID file."""
        try:
            if self.pid_file.exists():
                self.pid_file.unlink()
        except Exception as e:
            logger.error(f"Failed to remove PID file: {e}")

    def is_running(self) -> bool:
        """Check if process is running."""
        pid = self.read()
        if not pid:
            return False

        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False


def get_default_pid_file() -> Path:
    """Get default PID file path."""
    bb5_home = os.environ.get("BB5_HOME", os.path.expanduser("~/.blackbox5"))
    return Path(bb5_home) / ".autonomous" / "health" / "watch.pid"
