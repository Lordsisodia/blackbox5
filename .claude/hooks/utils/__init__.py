"""
BlackBox5 Hooks Utilities

Shared utilities for RALF hooks in the BlackBox5 system.
"""

from .json_logger import (
    log_hook_data,
    read_hook_log,
    get_hook_log_file,
    get_total_log_entries,
    clear_hook_log,
    get_latest_log_entry
)

__all__ = [
    'log_hook_data',
    'read_hook_log',
    'get_hook_log_file',
    'get_total_log_entries',
    'clear_hook_log',
    'get_latest_log_entry',
]
