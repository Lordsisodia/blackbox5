"""
Safe Mode Module

Degraded operation mode for BlackBox 5 when issues are detected.
"""

from .safe_mode import (
    SafeMode,
    SafeModeLevel,
    get_safe_mode,
    enter_safe_mode,
    exit_safe_mode,
    require_operation,
)

__all__ = [
    'SafeMode',
    'SafeModeLevel',
    'get_safe_mode',
    'enter_safe_mode',
    'exit_safe_mode',
    'require_operation',
]
