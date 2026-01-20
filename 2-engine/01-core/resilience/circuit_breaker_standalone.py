#!/usr/bin/env python3
"""
Standalone Circuit Breaker for BLACKBOX5

A simplified circuit breaker implementation that works independently
without external dependencies.

Usage:
    cb = CircuitBreaker("service_name", failure_threshold=5, timeout=60)
    with cb:
        result = risky_operation()
"""

import logging
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Callable, Any
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"       # Normal operation
    OPEN = "open"           # Circuit is tripped, blocking calls
    HALF_OPEN = "half_open" # Testing if service has recovered


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open."""
    pass


class CircuitBreaker:
    """
    Circuit Breaker pattern implementation.

    Prevents cascading failures by fast-failing when a service
    is experiencing issues.
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        timeout: int = 60,
        half_open_attempts: int = 1
    ):
        """
        Initialize circuit breaker.

        Args:
            name: Name of the circuit breaker
            failure_threshold: Number of failures before opening
            timeout: Seconds to wait before trying again
            half_open_attempts: Number of attempts in half-open state
        """
        self.name = name
        self._failure_threshold = failure_threshold
        self._timeout = timeout
        self._half_open_attempts = half_open_attempts

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: Optional[datetime] = None
        self._success_count = 0

        logger.info(f"CircuitBreaker '{name}' initialized (threshold={failure_threshold})")

    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        # Auto-transition from OPEN to HALF_OPEN after timeout
        if self._state == CircuitState.OPEN:
            if self._last_failure_time and \
               datetime.now() - self._last_failure_time > timedelta(seconds=self._timeout):
                logger.info(f"CircuitBreaker '{self.name}' transitioning OPEN -> HALF_OPEN")
                self._state = CircuitState.HALF_OPEN
                self._success_count = 0

        return self._state

    @property
    def is_open(self) -> bool:
        """Check if circuit is open (blocking)."""
        return self.state != CircuitState.CLOSED

    @property
    def failure_count(self) -> int:
        """Get current failure count."""
        return self._failure_count

    def record_success(self):
        """Record a successful call."""
        if self._state == CircuitState.HALF_OPEN:
            self._success_count += 1
            if self._success_count >= self._half_open_attempts:
                logger.info(f"CircuitBreaker '{self.name}' recovered -> CLOSED")
                self._state = CircuitState.CLOSED
                self._failure_count = 0
        else:
            self._failure_count = 0

    def record_failure(self):
        """Record a failed call."""
        self._failure_count += 1
        self._last_failure_time = datetime.now()

        if self._failure_count >= self._failure_threshold:
            logger.warning(f"CircuitBreaker '{self.name}' tripped -> OPEN")
            self._state = CircuitState.OPEN

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function through circuit breaker.

        Args:
            func: Function to call
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            CircuitBreakerError: If circuit is open
        """
        if self.is_open:
            raise CircuitBreakerError(f"CircuitBreaker '{self.name}' is {self.state.value}")

        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception as e:
            self.record_failure()
            raise

    @contextmanager
    def __enter__(self):
        """Context manager entry."""
        if self.is_open:
            raise CircuitBreakerError(f"CircuitBreaker '{self.name}' is {self.state.value}")
        yield self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if exc_type is None:
            self.record_success()
        else:
            self.record_failure()

    def reset(self):
        """Manually reset the circuit breaker."""
        logger.info(f"CircuitBreaker '{self.name}' manually reset")
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None

    def get_stats(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self._failure_count,
            "failure_threshold": self._failure_threshold,
            "is_open": self.is_open,
            "last_failure": self._last_failure_time.isoformat() if self._last_failure_time else None
        }
