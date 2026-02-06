"""Utility functions for BB5 Health Monitor."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional


def get_bb5_root() -> Path:
    """Get BB5 root directory from environment or default."""
    return Path(os.environ.get("BB5_HOME", os.path.expanduser("~/.blackbox5")))


def parse_timestamp(value: Optional[str]) -> Optional[datetime]:
    """Parse timestamp string to datetime."""
    if not value:
        return None

    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    return None


def format_duration(seconds: int) -> str:
    """Format seconds as human-readable duration."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m"
    elif seconds < 86400:
        return f"{seconds // 3600}h"
    elif seconds < 604800:
        return f"{seconds // 86400}d"
    elif seconds < 2592000:
        return f"{seconds // 604800}w"
    else:
        return f"{seconds // 2592000}mo"


def format_datetime(dt: Optional[datetime]) -> str:
    """Format datetime for display."""
    if not dt:
        return "never"

    now = datetime.now()
    diff = now - dt

    if diff.total_seconds() < 60:
        return "just now"
    elif diff.total_seconds() < 3600:
        return f"{int(diff.total_seconds() // 60)}m ago"
    elif diff.total_seconds() < 86400:
        return f"{int(diff.total_seconds() // 3600)}h ago"
    elif diff.total_seconds() < 604800:
        return f"{int(diff.total_seconds() // 86400)}d ago"
    else:
        return dt.strftime("%Y-%m-%d")


def get_health_color(score: int) -> str:
    """Get color name for health score."""
    if score >= 90:
        return "green"
    elif score >= 75:
        return "yellow"
    elif score >= 60:
        return "orange"
    else:
        return "red"


def get_health_emoji(score: int) -> str:
    """Get emoji for health score."""
    if score >= 90:
        return "✅"
    elif score >= 75:
        return "⚠️"
    elif score >= 60:
        return "🔶"
    else:
        return "🚨"
