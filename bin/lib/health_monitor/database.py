"""SQLite database interface for BB5 Health Monitor."""

import json
import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Tuple

from .config import get_config
from .models import HealthSnapshot, Metric, HealthStatus

logger = logging.getLogger(__name__)


SCHEMA = """
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,
    health_score INTEGER NOT NULL,
    status TEXT NOT NULL,
    queue_pending INTEGER,
    queue_in_progress INTEGER,
    queue_completed INTEGER,
    agents_online INTEGER,
    agents_stale INTEGER,
    agents_total INTEGER,
    stuck_tasks INTEGER,
    details TEXT
);

CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,
    name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT,
    tags TEXT
);

CREATE INDEX IF NOT EXISTS idx_snapshots_time ON snapshots(timestamp);
CREATE INDEX IF NOT EXISTS idx_metrics_time_name ON metrics(timestamp, name);
"""


def _get_connection() -> sqlite3.Connection:
    """Get database connection with WAL mode enabled."""
    config = get_config()
    conn = sqlite3.connect(str(config.db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


def init_database() -> None:
    """Initialize database schema."""
    config = get_config()
    config.db_path.parent.mkdir(parents=True, exist_ok=True)

    with _get_connection() as conn:
        conn.executescript(SCHEMA)
        conn.commit()

    logger.info(f"Database initialized at {config.db_path}")


def save_snapshot(snapshot: HealthSnapshot, details: Optional[dict] = None) -> None:
    """Save a health snapshot to the database."""
    with _get_connection() as conn:
        conn.execute(
            """
            INSERT INTO snapshots
            (timestamp, health_score, status, queue_pending, queue_in_progress,
             queue_completed, agents_online, agents_stale, agents_total, stuck_tasks, details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(snapshot.timestamp.timestamp()),
                snapshot.health_score,
                snapshot.status.value,
                snapshot.queue_pending,
                snapshot.queue_in_progress,
                snapshot.queue_completed,
                snapshot.agents_online,
                snapshot.agents_stale,
                snapshot.agents_total,
                snapshot.stuck_tasks,
                json.dumps(details) if details else None,
            )
        )
        conn.commit()


def save_metric(metric: Metric) -> None:
    """Save a metric to the database."""
    with _get_connection() as conn:
        conn.execute(
            """
            INSERT INTO metrics (timestamp, name, value, unit, tags)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                int(metric.timestamp.timestamp()),
                metric.name,
                metric.value,
                metric.unit,
                json.dumps(metric.tags) if metric.tags else None,
            )
        )
        conn.commit()


def get_recent_snapshots(hours: int = 24) -> List[HealthSnapshot]:
    """Get health snapshots from the last N hours."""
    cutoff = int((datetime.now() - timedelta(hours=hours)).timestamp())

    with _get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM snapshots
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
            """,
            (cutoff,)
        ).fetchall()

    return [
        HealthSnapshot(
            timestamp=datetime.fromtimestamp(row['timestamp']),
            health_score=row['health_score'],
            status=HealthStatus(row['status']),
            queue_pending=row['queue_pending'],
            queue_in_progress=row['queue_in_progress'],
            queue_completed=row['queue_completed'],
            agents_online=row['agents_online'],
            agents_stale=row['agents_stale'],
            agents_total=row['agents_total'],
            stuck_tasks=row['stuck_tasks'],
        )
        for row in rows
    ]


def get_metrics_range(start: datetime, end: datetime, name: Optional[str] = None) -> List[Metric]:
    """Get metrics within a time range, optionally filtered by name."""
    start_ts = int(start.timestamp())
    end_ts = int(end.timestamp())

    with _get_connection() as conn:
        if name:
            rows = conn.execute(
                """
                SELECT * FROM metrics
                WHERE timestamp >= ? AND timestamp <= ? AND name = ?
                ORDER BY timestamp DESC
                """,
                (start_ts, end_ts, name)
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT * FROM metrics
                WHERE timestamp >= ? AND timestamp <= ?
                ORDER BY timestamp DESC
                """,
                (start_ts, end_ts)
            ).fetchall()

    return [
        Metric(
            timestamp=datetime.fromtimestamp(row['timestamp']),
            name=row['name'],
            value=row['value'],
            unit=row['unit'],
            tags=json.loads(row['tags']) if row['tags'] else {},
        )
        for row in rows
    ]


def get_latest_snapshot() -> Optional[HealthSnapshot]:
    """Get the most recent health snapshot."""
    with _get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM snapshots ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()

    if not row:
        return None

    return HealthSnapshot(
        timestamp=datetime.fromtimestamp(row['timestamp']),
        health_score=row['health_score'],
        status=HealthStatus(row['status']),
        queue_pending=row['queue_pending'],
        queue_in_progress=row['queue_in_progress'],
        queue_completed=row['queue_completed'],
        agents_online=row['agents_online'],
        agents_stale=row['agents_stale'],
        agents_total=row['agents_total'],
        stuck_tasks=row['stuck_tasks'],
    )
