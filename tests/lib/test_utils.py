"""
Test Utilities for RALF Testing Framework
==========================================

Provides helper functions, assertions, and utilities for writing tests.
"""

import os
import yaml
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional
import sys


# Add engine lib to path for importing RALF components
ENGINE_LIB = Path("/workspaces/blackbox5/2-engine/.autonomous/lib")
if str(ENGINE_LIB) not in sys.path:
    sys.path.insert(0, str(ENGINE_LIB))


class AssertionError(Exception):
    """Custom assertion error for test utilities."""
    pass


# ============================================================================
# File Assertions
# ============================================================================

def assert_file_exists(file_path: str, msg: Optional[str] = None) -> None:
    """
    Assert that a file exists.

    Args:
        file_path: Path to file
        msg: Optional error message

    Raises:
        AssertionError: If file doesn't exist
    """
    if not os.path.exists(file_path):
        raise AssertionError(
            msg or f"File does not exist: {file_path}"
        )


def assert_file_not_exists(file_path: str, msg: Optional[str] = None) -> None:
    """
    Assert that a file does not exist.

    Args:
        file_path: Path to file
        msg: Optional error message

    Raises:
        AssertionError: If file exists
    """
    if os.path.exists(file_path):
        raise AssertionError(
            msg or f"File exists but shouldn't: {file_path}"
        )


def assert_dir_exists(dir_path: str, msg: Optional[str] = None) -> None:
    """
    Assert that a directory exists.

    Args:
        dir_path: Path to directory
        msg: Optional error message

    Raises:
        AssertionError: If directory doesn't exist
    """
    if not os.path.isdir(dir_path):
        raise AssertionError(
            msg or f"Directory does not exist: {dir_path}"
        )


# ============================================================================
# YAML Assertions
# ============================================================================

def assert_yaml_valid(file_path: str, msg: Optional[str] = None) -> None:
    """
    Assert that a YAML file is valid.

    Args:
        file_path: Path to YAML file
        msg: Optional error message

    Raises:
        AssertionError: If YAML is invalid
    """
    try:
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
    except Exception as e:
        raise AssertionError(
            msg or f"Invalid YAML file {file_path}: {e}"
        )


def assert_yaml_has_key(file_path: str, key: str, msg: Optional[str] = None) -> None:
    """
    Assert that a YAML file contains a specific key.

    Args:
        file_path: Path to YAML file
        key: Key to check (supports dot notation for nested keys)
        msg: Optional error message

    Raises:
        AssertionError: If key not found
    """
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f) or {}

    # Navigate nested keys
    keys = key.split('.')
    current = data
    for k in keys:
        if not isinstance(current, dict) or k not in current:
            raise AssertionError(
                msg or f"Key '{key}' not found in {file_path}"
            )
        current = current[k]


# ============================================================================
# Mock Generators
# ============================================================================

def mock_config(
    skill_invocation_confidence: int = 70,
    queue_depth_min: int = 3,
    queue_depth_max: int = 5,
    default_agent: str = "executor"
) -> Dict[str, Any]:
    """
    Generate a mock configuration.

    Args:
        skill_invocation_confidence: Skill threshold
        queue_depth_min: Minimum queue depth
        queue_depth_max: Maximum queue depth
        default_agent: Default agent name

    Returns:
        dict: Mock configuration
    """
    return {
        "thresholds": {
            "skill_invocation_confidence": skill_invocation_confidence,
            "queue_depth_min": queue_depth_min,
            "queue_depth_max": queue_depth_max,
        },
        "routing": {
            "default_agent": default_agent,
            "task_type_routing": {
                "implementation": "executor",
                "planning": "planner",
            }
        },
        "notifications": {
            "enabled": False,
            "level": "INFO",
        }
    }


def mock_task(
    task_id: str = "TASK-001",
    task_type: str = "implement",
    priority: str = "high",
    status: str = "pending"
) -> Dict[str, Any]:
    """
    Generate a mock task.

    Args:
        task_id: Task ID
        task_type: Task type
        priority: Task priority
        status: Task status

    Returns:
        dict: Mock task
    """
    return {
        "task_id": task_id,
        "type": task_type,
        "priority": priority,
        "status": status,
        "title": f"Mock Task {task_id}",
        "objective": "Mock objective for testing",
        "approach": "Mock approach for testing"
    }


def mock_event(
    task_id: str = "TASK-001",
    event_type: str = "started",
    agent: str = "executor",
    result: str = "success"
) -> Dict[str, Any]:
    """
    Generate a mock event.

    Args:
        task_id: Task ID
        event_type: Event type
        agent: Agent name
        result: Event result

    Returns:
        dict: Mock event
    """
    return {
        "timestamp": "2026-02-01T12:00:00Z",
        "task_id": task_id,
        "type": event_type,
        "agent": agent,
        "run_number": 1,
        "result": result
    }


# ============================================================================
# Test Data Helpers
# ============================================================================

def create_temp_yaml_file(content: Dict[str, Any]) -> str:
    """
    Create a temporary YAML file with content.

    Args:
        content: Dictionary to write as YAML

    Returns:
        str: Path to temporary file
    """
    fd, path = tempfile.mkstemp(suffix='.yaml')
    with os.fdopen(fd, 'w') as f:
        yaml.dump(content, f)
    return path


def create_temp_file(content: str, suffix: str = '.txt') -> str:
    """
    Create a temporary file with content.

    Args:
        content: String content to write
        suffix: File suffix

    Returns:
        str: Path to temporary file
    """
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    return path


def cleanup_test_files(*paths: str) -> None:
    """
    Clean up test files.

    Args:
        *paths: Paths to clean up
    """
    for path in paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass  # Ignore cleanup errors


# ============================================================================
# Import Helpers
# ============================================================================

def import_config_manager():
    """
    Import ConfigManager from engine lib.

    Returns:
        ConfigManager class
    """
    try:
        from config_manager import ConfigManager
        return ConfigManager
    except ImportError:
        raise ImportError(
            "ConfigManager not found. Ensure engine lib is in path."
        )


def import_queue_sync():
    """
    Import queue sync module.

    Returns:
        queue_sync module
    """
    try:
        import queue_sync
        return queue_sync
    except ImportError:
        raise ImportError(
            "queue_sync not found. Ensure engine lib is in path."
        )


def import_roadmap_sync():
    """
    Import roadmap sync module.

    Returns:
        roadmap_sync module
    """
    try:
        import roadmap_sync
        return roadmap_sync
    except ImportError:
        raise ImportError(
            "roadmap_sync not found. Ensure engine lib is in path."
        )


# ============================================================================
# Validation Helpers
# ============================================================================

def assert_valid_confidence(value: int, msg: Optional[str] = None) -> None:
    """
    Assert that confidence value is valid (0-100).

    Args:
        value: Confidence value
        msg: Optional error message

    Raises:
        AssertionError: If confidence invalid
    """
    if not (0 <= value <= 100):
        raise AssertionError(
            msg or f"Confidence must be 0-100, got {value}"
        )


def assert_valid_queue_depth(min_depth: int, max_depth: int, msg: Optional[str] = None) -> None:
    """
    Assert that queue depth range is valid.

    Args:
        min_depth: Minimum queue depth
        max_depth: Maximum queue depth
        msg: Optional error message

    Raises:
        AssertionError: If queue depth invalid
    """
    if min_depth < 0 or max_depth < 0:
        raise AssertionError(
            msg or f"Queue depth must be >= 0, got min={min_depth}, max={max_depth}"
        )
    if min_depth > max_depth:
        raise AssertionError(
            msg or f"Min queue depth ({min_depth}) > max ({max_depth})"
        )


# ============================================================================
# Export All
# ============================================================================

__all__ = [
    # File assertions
    'assert_file_exists',
    'assert_file_not_exists',
    'assert_dir_exists',
    # YAML assertions
    'assert_yaml_valid',
    'assert_yaml_has_key',
    # Mock generators
    'mock_config',
    'mock_task',
    'mock_event',
    # Test data helpers
    'create_temp_yaml_file',
    'create_temp_file',
    'cleanup_test_files',
    # Import helpers
    'import_config_manager',
    'import_queue_sync',
    'import_roadmap_sync',
    # Validation helpers
    'assert_valid_confidence',
    'assert_valid_queue_depth',
]
