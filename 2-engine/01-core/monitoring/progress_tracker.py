#!/usr/bin/env python3
"""
Progress Tracker - Real-time progress monitoring and ETA calculation
"""

import logging
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProgressTracker:
    """
    Tracks progress of tasks with real-time updates and ETA calculation.

    Features:
    - Progress percentage calculation
    - ETA estimation
    - Speed tracking (items per second)
    """

    def __init__(self, total_items: int = 100):
        """
        Initialize progress tracker.

        Args:
            total_items: Total number of items to process
        """
        self.total = total_items
        self.completed = 0
        self.failed = 0
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None
        self._status = TaskStatus.PENDING

    def start(self):
        """Start tracking."""
        self._start_time = datetime.now()
        self._status = TaskStatus.IN_PROGRESS
        logger.info("Progress tracking started")

    def update(self, completed: int, failed: int = 0):
        """Update progress."""
        self.completed = completed
        self.failed = failed

    def increment(self, amount: int = 1, failed: bool = False):
        """Increment progress."""
        if failed:
            self.failed += amount
        else:
            self.completed += amount

    def finish(self):
        """Mark as finished."""
        self._end_time = datetime.now()
        self._status = TaskStatus.COMPLETED
        logger.info(f"Progress tracking finished: {self.completed}/{self.total} completed")

    def get_progress_percent(self) -> float:
        """Get progress as percentage."""
        return (self.completed / self.total * 100) if self.total > 0 else 0

    def get_eta(self) -> Optional[timedelta]:
        """
        Get estimated time to completion.

        Returns:
            Timedelta until completion, or None if unable to estimate
        """
        if not self._start_time or self.completed == 0:
            return None

        elapsed = datetime.now() - self._start_time
        speed = self.completed / elapsed.total_seconds()  # items per second

        if speed <= 0:
            return None

        remaining = self.total - self.completed
        eta_seconds = remaining / speed
        return timedelta(seconds=eta_seconds)

    def get_speed(self) -> Optional[float]:
        """
        Get processing speed.

        Returns:
            Items per second, or None if unable to calculate
        """
        if not self._start_time or self.completed == 0:
            return None

        elapsed = (datetime.now() - self._start_time).total_seconds()
        return self.completed / elapsed

    def get_stats(self) -> Dict[str, Any]:
        """Get progress statistics."""
        return {
            "total": self.total,
            "completed": self.completed,
            "failed": self.failed,
            "percent": self.get_progress_percent(),
            "status": self._status.value,
            "eta_seconds": self.get_eta().total_seconds() if self.get_eta() else None,
            "speed": self.get_speed(),
            "start_time": self._start_time.isoformat() if self._start_time else None,
            "elapsed_seconds": (datetime.now() - self._start_time).total_seconds() if self._start_time else 0
        }

    def is_complete(self) -> bool:
        """Check if task is complete."""
        return self.completed >= self.total
