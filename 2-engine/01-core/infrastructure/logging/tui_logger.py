"""
TUI Logger - Terminal User Interface Logger

Provides color-coded, real-time logging with filtering.
"""

import logging
import sys
from typing import Optional, List
from datetime import datetime


class TUILogger(logging.Handler):
    """
    TUI Logger with color-coded output and real-time updates.

    Usage:
        logger = logging.getLogger(__name__)
        handler = TUILogger()
        logger.addHandler(handler)
    """

    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[37m',       # White
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }

    def __init__(self, level: int = logging.INFO):
        super().__init__(level)
        self._filters: List[str] = []
        self._enabled = True

    def emit(self, record):
        """Emit a log record."""
        if not self._enabled:
            return

        # Check filters
        if self._filters:
            if not any(f in record.name for f in self._filters):
                return

        # Format message
        color = self.COLORS.get(record.levelname, '')
        reset = self.COLORS['RESET']
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')

        message = f"{color}[{timestamp}] {record.levelname}: {record.getMessage()}{reset}\n"

        sys.stderr.write(message)
        sys.stderr.flush()

    def add_filter(self, pattern: str):
        """Add a filter pattern."""
        self._filters.append(pattern)

    def enable(self):
        """Enable the logger."""
        self._enabled = True

    def disable(self):
        """Disable the logger."""
        self._enabled = False
