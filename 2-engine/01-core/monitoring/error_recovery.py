#!/usr/bin/env python3
"""
Error Recovery - Automatic error classification and retry logic
"""

import logging
import time
from typing import Callable, Optional, Dict, Any, TypeVar, List
from datetime import datetime
from enum import Enum
from functools import wraps

logger = logging.getLogger(__name__)

T = TypeVar('T')


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"           # Recoverable, non-critical
    MEDIUM = "medium"     # May require intervention
    HIGH = "high"         # Critical, needs attention
    CRITICAL = "critical" # System-affecting


class ErrorCategory(Enum):
    """Error categories for classification."""
    BUG = "bug"                           # Code bug
    MISSING_DEPENDENCY = "dependency"     # Missing dependency
    BLOCKAGE = "blockage"                 # External service timeout
    CRITICAL_MISSING = "critical_missing" # Validation error
    UNKNOWN = "unknown"                   # Unknown error


class RecoveryAction(Enum):
    """Recovery actions."""
    RETRY = "retry"                       # Retry operation
    FALLBACK = "fallback"                 # Use fallback
    ESCALATE = "escalate"                 # Escalate to human
    IGNORE = "ignore"                     # Ignore and continue


class ErrorRecovery:
    """
    Automatic error recovery with classification and retry logic.

    Implements the 4-rule deviation handling system:
    - BUG: Test failure, runtime error recovery
    - MISSING_DEPENDENCY: ImportError handling
    - BLOCKAGE: External API timeout handling
    - CRITICAL_MISSING: Validation error recovery
    """

    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        """
        Initialize error recovery system.

        Args:
            max_retries: Maximum number of retry attempts
            backoff_factor: Exponential backoff multiplier
        """
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self._error_history: List[Dict[str, Any]] = []

    def classify_error(self, error: Exception) -> ErrorCategory:
        """
        Classify an error into a category.

        Args:
            error: The exception to classify

        Returns:
            Error category
        """
        error_type = type(error).__name__
        error_msg = str(error).lower()

        # Check for import errors
        if error_type in ["ImportError", "ModuleNotFoundError"]:
            return ErrorCategory.MISSING_DEPENDENCY

        # Check for timeout/network errors
        if any(kw in error_msg for kw in ["timeout", "connection", "network", "unreachable"]):
            return ErrorCategory.BLOCKAGE

        # Check for validation errors
        if error_type in ["ValueError", "ValidationError", "AssertionError"]:
            return ErrorCategory.CRITICAL_MISSING

        # Default to BUG
        return ErrorCategory.BUG

    def get_severity(self, category: ErrorCategory) -> ErrorSeverity:
        """Get severity level for an error category."""
        severity_map = {
            ErrorCategory.MISSING_DEPENDENCY: ErrorSeverity.HIGH,
            ErrorCategory.BLOCKAGE: ErrorSeverity.MEDIUM,
            ErrorCategory.CRITICAL_MISSING: ErrorSeverity.CRITICAL,
            ErrorCategory.BUG: ErrorSeverity.MEDIUM,
            ErrorCategory.UNKNOWN: ErrorSeverity.LOW,
        }
        return severity_map.get(category, ErrorSeverity.MEDIUM)

    def get_recovery_action(self, category: ErrorCategory) -> RecoveryAction:
        """Get recommended recovery action for an error category."""
        action_map = {
            ErrorCategory.BLOCKAGE: RecoveryAction.RETRY,
            ErrorCategory.MISSING_DEPENDENCY: RecoveryAction.ESCALATE,
            ErrorCategory.CRITICAL_MISSING: RecoveryAction.ESCALATE,
            ErrorCategory.BUG: RecoveryAction.FALLBACK,
            ErrorCategory.UNKNOWN: RecoveryAction.IGNORE,
        }
        return action_map.get(category, RecoveryAction.IGNORE)

    def execute_with_retry(
        self,
        func: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        """
        Execute function with automatic retry on failure.

        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If all retries exhausted
        """
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                category = self.classify_error(e)
                action = self.get_recovery_action(category)

                self._error_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "category": category.value,
                    "action": action.value,
                    "error": str(e),
                    "attempt": attempt
                })

                if action == RecoveryAction.RETRY and attempt < self.max_retries:
                    delay = self.backoff_factor ** attempt
                    logger.warning(f"Retry {attempt + 1}/{self.max_retries} after {delay}s: {e}")
                    time.sleep(delay)
                elif action == RecoveryAction.ESCALATE:
                    logger.error(f"Escalating error: {e}")
                    raise
                elif attempt >= self.max_retries:
                    logger.error(f"Max retries ({self.max_retries}) exhausted")
                    raise

        raise last_error  # Should never reach here

    def get_error_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent error history."""
        return self._error_history[-limit:]

    def get_stats(self) -> Dict[str, Any]:
        """Get error recovery statistics."""
        if not self._error_history:
            return {"total_errors": 0}

        categories = {}
        for error in self._error_history:
            cat = error["category"]
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "total_errors": len(self._error_history),
            "categories": categories,
            "last_error": self._error_history[-1] if self._error_history else None
        }


def with_retry(max_retries: int = 3):
    """Decorator for automatic retry."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        recovery = ErrorRecovery(max_retries=max_retries)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return recovery.execute_with_retry(func, *args, **kwargs)

        return wrapper
    return decorator
