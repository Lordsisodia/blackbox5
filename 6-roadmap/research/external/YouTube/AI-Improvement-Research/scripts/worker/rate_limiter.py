"""
Rate Limiter for Transcript Fetching

Manages daily quotas and prevents API bans.
"""

import json
import time
from datetime import datetime, date
from pathlib import Path
from typing import Optional


class RateLimiter:
    """Manages rate limiting and daily quotas."""

    def __init__(
        self,
        state_file: Path,
        daily_limit: int = 200,
        request_delay: float = 2.0,
        max_consecutive_errors: int = 5
    ):
        """
        Initialize rate limiter.

        Args:
            state_file: Path to JSON state file
            daily_limit: Max videos per day
            request_delay: Seconds between requests
            max_consecutive_errors: Stop after N consecutive errors
        """
        self.state_file = state_file
        self.daily_limit = daily_limit
        self.request_delay = request_delay
        self.max_consecutive_errors = max_consecutive_errors

        self.state = self._load_state()
        self.consecutive_errors = 0

    def _load_state(self) -> dict:
        """Load rate limiter state from file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {
            'date': str(date.today()),
            'count': 0,
            'last_request_time': 0
        }

    def _save_state(self):
        """Save rate limiter state to file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)

    def can_proceed(self) -> bool:
        """Check if we can make another request."""
        # Check if it's a new day
        today = str(date.today())
        if self.state['date'] != today:
            self.state = {
                'date': today,
                'count': 0,
                'last_request_time': 0
            }
            self._save_state()

        # Check daily limit
        if self.state['count'] >= self.daily_limit:
            return False

        # Check consecutive errors
        if self.consecutive_errors >= self.max_consecutive_errors:
            return False

        return True

    def get_remaining(self) -> int:
        """Get remaining requests for today."""
        today = str(date.today())
        if self.state['date'] != today:
            return self.daily_limit
        return max(0, self.daily_limit - self.state['count'])

    def record_request(self, success: bool = True):
        """Record a request attempt."""
        self.state['count'] += 1
        self.state['last_request_time'] = time.time()

        if success:
            self.consecutive_errors = 0
        else:
            self.consecutive_errors += 1

        self._save_state()

    def get_delay(self) -> float:
        """Get required delay before next request."""
        elapsed = time.time() - self.state.get('last_request_time', 0)
        return max(0, self.request_delay - elapsed)

    def should_stop_for_today(self) -> bool:
        """Check if we should stop fetching for today."""
        return not self.can_proceed()

    def get_status(self) -> dict:
        """Get current rate limiter status."""
        return {
            'date': self.state['date'],
            'daily_limit': self.daily_limit,
            'used_today': self.state['count'],
            'remaining_today': self.get_remaining(),
            'consecutive_errors': self.consecutive_errors,
            'can_proceed': self.can_proceed()
        }
