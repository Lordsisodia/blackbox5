"""BB5 Health Monitor - Core library for system health monitoring."""

from .config import Config
from .models import Task, Agent, Event, HealthSnapshot, Metric
from .collectors import (
    collect_queue,
    collect_heartbeat,
    collect_events,
    collect_metrics,
    collect_skills,
    collect_run_metrics,
    collect_all
)
from .calculators import (
    calculate_health_score,
    calculate_queue_health,
    calculate_agent_health,
    calculate_throughput,
    detect_stuck_tasks
)
from .database import (
    init_database,
    save_snapshot,
    save_metric,
    get_recent_snapshots,
    get_metrics_range
)
from .utils import format_duration, parse_timestamp, get_bb5_root
from .alerts import AlertManager, AlertConfig

__version__ = "1.0.0"

__all__ = [
    # Config
    "Config",
    # Models
    "Task",
    "Agent",
    "Event",
    "HealthSnapshot",
    "Metric",
    # Collectors
    "collect_queue",
    "collect_heartbeat",
    "collect_events",
    "collect_metrics",
    "collect_skills",
    "collect_run_metrics",
    "collect_all",
    # Calculators
    "calculate_health_score",
    "calculate_queue_health",
    "calculate_agent_health",
    "calculate_throughput",
    "detect_stuck_tasks",
    # Database
    "init_database",
    "save_snapshot",
    "save_metric",
    "get_recent_snapshots",
    "get_metrics_range",
    # Utils
    "format_duration",
    "parse_timestamp",
    "get_bb5_root",
    # Alerts
    "AlertManager",
    "AlertConfig",
]
