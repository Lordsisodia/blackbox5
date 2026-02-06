#!/usr/bin/env python3
"""
Atomic I/O utilities for BlackBox5 storage files.

Provides thread-safe and process-safe file operations using:
- File locking (fcntl on Unix)
- Atomic writes (temp file + rename)
- Automatic backups
"""

import fcntl
import logging
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Optional

import yaml

logger = logging.getLogger(__name__)


@contextmanager
def file_lock(lock_path: Path, timeout: Optional[float] = None):
    """
    Acquire exclusive file lock using fcntl.

    Args:
        lock_path: Path to lock file (typically filepath.with_suffix('.lock'))
        timeout: Maximum time to wait for lock (None = block indefinitely)

    Raises:
        TimeoutError: If lock cannot be acquired within timeout
        RuntimeError: If lock acquisition fails
    """
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    lock_fd = open(lock_path, 'w')
    try:
        if timeout is not None:
            # Non-blocking with retry loop for timeout
            import time
            start = time.time()
            while True:
                try:
                    fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except (IOError, OSError) as e:
                    if time.time() - start >= timeout:
                        raise TimeoutError(f"Could not acquire lock on {lock_path} within {timeout}s")
                    time.sleep(0.1)
        else:
            # Blocking lock
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)

        logger.debug(f"Acquired lock: {lock_path}")
        yield lock_fd

    finally:
        try:
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)
            logger.debug(f"Released lock: {lock_path}")
        except Exception as e:
            logger.warning(f"Error releasing lock {lock_path}: {e}")
        finally:
            lock_fd.close()


def atomic_write_yaml(
    data: dict,
    filepath: Path,
    create_backup: bool = True,
    lock_timeout: Optional[float] = None
) -> None:
    """
    Write YAML data atomically with file locking.

    Process:
    1. Acquire exclusive lock
    2. Create backup of existing file (if create_backup=True)
    3. Write to temp file in same directory
    4. Atomic rename (os.replace)
    5. Release lock

    Args:
        data: Dictionary to write as YAML
        filepath: Target file path
        create_backup: Whether to create .backup file before write
        lock_timeout: Maximum time to wait for lock (None = block indefinitely)

    Raises:
        TimeoutError: If lock cannot be acquired
        OSError: If write fails
    """
    filepath = Path(filepath)
    lock_path = filepath.with_suffix(filepath.suffix + '.lock')

    with file_lock(lock_path, timeout=lock_timeout):
        # Create backup if requested and file exists
        if create_backup and filepath.exists():
            backup_path = filepath.parent / (filepath.name + '.backup')
            try:
                import shutil
                shutil.copy2(filepath, backup_path)
                logger.debug(f"Created backup: {backup_path}")
            except Exception as e:
                logger.warning(f"Failed to create backup: {e}")

        # Write to temp file in same directory (for atomic rename)
        temp_fd, temp_path = tempfile.mkstemp(
            dir=filepath.parent,
            prefix=filepath.name + '.tmp.'
        )
        try:
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                yaml.dump(
                    data,
                    f,
                    default_flow_style=False,
                    sort_keys=False,
                    allow_unicode=True
                )

            # Atomic rename
            os.replace(temp_path, filepath)
            logger.debug(f"Atomically wrote: {filepath}")

        except Exception:
            # Clean up temp file on failure
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise


def atomic_append_yaml_event(
    event: dict,
    filepath: Path,
    lock_timeout: Optional[float] = None
) -> None:
    """
    Append event to YAML list atomically with file locking.

    This is specifically for events.yaml files that are lists of events.
    Uses read-modify-write pattern with proper locking.

    Args:
        event: Event dictionary to append
        filepath: Target file path
        lock_timeout: Maximum time to wait for lock

    Raises:
        TimeoutError: If lock cannot be acquired
    """
    filepath = Path(filepath)
    lock_path = filepath.with_suffix(filepath.suffix + '.lock')

    with file_lock(lock_path, timeout=lock_timeout):
        # Read existing events
        events = []
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    events = yaml.safe_load(f) or []
            except Exception as e:
                logger.warning(f"Failed to read existing events: {e}")
                events = []

        # Append new event
        events.append(event)

        # Write atomically (within lock, so no need for separate atomic write)
        temp_fd, temp_path = tempfile.mkstemp(
            dir=filepath.parent,
            prefix=filepath.name + '.tmp.'
        )
        try:
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                yaml.dump(
                    events,
                    f,
                    default_flow_style=False,
                    sort_keys=False,
                    allow_unicode=True
                )

            os.replace(temp_path, filepath)
            logger.debug(f"Appended event to: {filepath}")

        except Exception:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise


def load_yaml_locked(
    filepath: Path,
    default: Any = None,
    lock_timeout: Optional[float] = None
) -> Any:
    """
    Load YAML file with read lock for consistency.

    Args:
        filepath: File to load
        default: Default value if file doesn't exist or is empty
        lock_timeout: Maximum time to wait for lock

    Returns:
        Parsed YAML data or default value
    """
    filepath = Path(filepath)
    lock_path = filepath.with_suffix(filepath.suffix + '.lock')

    with file_lock(lock_path, timeout=lock_timeout):
        if not filepath.exists():
            return default

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or default
        except Exception as e:
            logger.error(f"Failed to load {filepath}: {e}")
            return default
