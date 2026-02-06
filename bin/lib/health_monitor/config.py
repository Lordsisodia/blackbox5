"""Configuration module for BB5 Health Monitor."""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration for BB5 Health Monitor."""

    # Base paths
    bb5_root: Path
    project_memory: Path

    # Data source paths
    queue_path: Path
    heartbeat_path: Path
    events_path: Path
    metrics_path: Path
    skills_path: Path
    runs_dir: Path

    # Database
    db_path: Path

    # Thresholds
    heartbeat_timeout_seconds: int = 120
    stuck_task_multiplier: float = 2.0
    health_score_threshold: int = 60

    # Alert cooldown
    alert_cooldown_seconds: int = 300

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables or defaults."""
        bb5_root = Path(os.environ.get("BB5_HOME", os.path.expanduser("~/.blackbox5")))
        project_memory = bb5_root / "5-project-memory" / "blackbox5"

        return cls(
            bb5_root=bb5_root,
            project_memory=project_memory,
            queue_path=project_memory / ".autonomous" / "agents" / "communications" / "queue.yaml",
            heartbeat_path=project_memory / ".autonomous" / "agents" / "communications" / "heartbeat.yaml",
            events_path=project_memory / ".autonomous" / "agents" / "communications" / "events.yaml",
            metrics_path=project_memory / ".autonomous" / "agents" / "metrics" / "metrics-dashboard.yaml",
            skills_path=project_memory / "operations" / "skill-registry.yaml",
            runs_dir=project_memory / ".autonomous" / "runs",
            db_path=bb5_root / ".autonomous" / "health" / "health.db",
        )

    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create global config instance."""
    global _config
    if _config is None:
        _config = Config.from_env()
        _config.ensure_directories()
    return _config
