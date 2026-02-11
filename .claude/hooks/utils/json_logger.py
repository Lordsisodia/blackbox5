"""
JSON Logger Utility for BlackBox5 Hooks

This module provides a standardized logging helper for RALF hooks.
All hooks should use this utility to ensure consistent JSON logging.

Usage:
    from hooks.utils.json_logger import log_hook_data

    def main():
        input_data = json.load(sys.stdin)
        log_hook_data("hook_name", input_data)
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def log_hook_data(hook_name: str, data: dict) -> None:
    """
    Standard JSON logging for hooks.

    Appends input data to logs/{hook_name}.json in a structured format.

    Log structure:
        [
            {
                "timestamp": "2026-02-10T12:34:56.789012",
                "data": { ... input data ... }
            },
            ...
        ]

    Args:
        hook_name: Name of the hook (e.g., "pre_tool_use", "post_message_agent_teams")
        data: Dictionary containing the input data to log

    The function handles:
    - Creating log directory if it doesn't exist
    - Reading existing log file or initializing empty list
    - Appending new data with timestamp
    - Writing back with proper formatting
    - Graceful error handling for corrupted JSON files
    """
    # Ensure log directory exists
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # Log file path
    log_path = log_dir / f'{hook_name}.json'

    # Read existing log data or initialize empty list
    if log_path.exists():
        try:
            with open(log_path, 'r') as f:
                log_data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            # Handle corrupted JSON - start fresh
            log_data = []
    else:
        log_data = []

    # Create entry with timestamp
    entry = {
        "timestamp": datetime.now().isoformat(),
        "data": data
    }

    # Append and write back
    log_data.append(entry)

    with open(log_path, 'w') as f:
        json.dump(log_data, f, indent=2)


def read_hook_log(hook_name: str) -> list:
    """
    Read existing log data for a hook.

    Args:
        hook_name: Name of the hook

    Returns:
        List of log entries, or empty list if file doesn't exist or is corrupted
    """
    log_dir = Path("logs")
    log_path = log_dir / f'{hook_name}.json'

    if not log_path.exists():
        return []

    try:
        with open(log_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []


def get_hook_log_file(hook_name: str) -> Path:
    """
    Get the log file path for a hook without creating the file.

    Args:
        hook_name: Name of the hook

    Returns:
        Path to the log file
    """
    log_dir = Path("logs")
    return log_dir / f'{hook_name}.json'


def get_total_log_entries(hook_name: str) -> int:
    """
    Get the total number of entries in a hook's log.

    Args:
        hook_name: Name of the hook

    Returns:
        Number of log entries
    """
    logs = read_hook_log(hook_name)
    return len(logs)


def clear_hook_log(hook_name: str) -> bool:
    """
    Clear all entries from a hook's log.

    Args:
        hook_name: Name of the hook

    Returns:
        True if successful, False if file doesn't exist
    """
    log_path = get_hook_log_file(hook_name)

    if not log_path.exists():
        return False

    with open(log_path, 'w') as f:
        json.dump([], f, indent=2)

    return True


def get_latest_log_entry(hook_name: str) -> dict | None:
    """
    Get the most recent log entry for a hook.

    Args:
        hook_name: Name of the hook

    Returns:
        The latest entry, or None if no entries exist
    """
    logs = read_hook_log(hook_name)

    if not logs:
        return None

    return logs[-1]
