"""
Pytest configuration and fixtures for RALF testing framework.

This file contains shared fixtures and configuration for all tests.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Generator
import pytest
import yaml


# Add 2-engine/.autonomous/lib to path for imports
AUTONOMOUS_LIB = Path(__file__).parent.parent / ".autonomous" / "lib"
sys.path.insert(0, str(AUTONOMOUS_LIB))


# ============================================================================
# PATH FIXTURES
# ============================================================================

@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def tests_dir(project_root: Path) -> Path:
    """Get the tests directory."""
    return project_root / "2-engine" / "tests"


@pytest.fixture
def fixtures_dir(tests_dir: Path) -> Path:
    """Get the test fixtures directory."""
    return tests_dir / "fixtures"


# ============================================================================
# TEMPORARY DIRECTORY FIXTURES
# ============================================================================

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """
    Create a temporary directory for testing.

    The directory is automatically cleaned up after the test.
    """
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def temp_config_file(temp_dir: Path) -> Path:
    """
    Create a temporary config file path.

    Returns Path object for a config file in temp directory.
    """
    return temp_dir / "config.yaml"


@pytest.fixture
def temp_user_config_file(temp_dir: Path) -> Path:
    """
    Create a temporary user config file path.

    Returns Path object for a user config file in temp directory.
    """
    return temp_dir / "user_config.yaml"


# ============================================================================
# CONFIG FIXTURES
# ============================================================================

@pytest.fixture
def default_config_content() -> Dict[str, Any]:
    """Default configuration content for testing."""
    return {
        "executor": {
            "skill_threshold": 0.7,
            "max_retries": 3,
            "timeout_seconds": 120
        },
        "planner": {
            "queue_depth_target": 5,
            "look_ahead_tasks": 10
        },
        "testing": {
            "enabled": True,
            "verbose": False
        }
    }


@pytest.fixture
def user_config_content() -> Dict[str, Any]:
    """User configuration content for testing."""
    return {
        "executor": {
            "skill_threshold": 0.8,  # Override default
            "custom_setting": "user_value"
        }
    }


@pytest.fixture
def sample_config_file(temp_config_file: Path, default_config_content: Dict[str, Any]) -> Path:
    """Create a sample config file with default content."""
    with open(temp_config_file, 'w') as f:
        yaml.dump(default_config_content, f)
    return temp_config_file


@pytest.fixture
def sample_user_config_file(temp_user_config_file: Path, user_config_content: Dict[str, Any]) -> Path:
    """Create a sample user config file."""
    with open(temp_user_config_file, 'w') as f:
        yaml.dump(user_config_content, f)
    return temp_user_config_file


# ============================================================================
# TASK FIXTURES
# ============================================================================

@pytest.fixture
def sample_task() -> Dict[str, Any]:
    """Sample task for testing."""
    return {
        "task_id": "TASK-001",
        "title": "Test Task",
        "type": "implement",
        "priority": "high",
        "status": "pending",
        "objective": "Test objective",
        "approach": "Test approach",
        "files_to_modify": [],
        "success_criteria": []
    }


@pytest.fixture
def sample_completed_task(sample_task: Dict[str, Any]) -> Dict[str, Any]:
    """Sample completed task for testing."""
    task = sample_task.copy()
    task["status"] = "completed"
    task["result"] = "success"
    return task


# ============================================================================
# EVENT FIXTURES
# ============================================================================

@pytest.fixture
def sample_event() -> Dict[str, Any]:
    """Sample event for testing."""
    return {
        "timestamp": "2026-02-01T12:00:00Z",
        "task_id": "TASK-001",
        "type": "started",
        "agent": "executor",
        "run_number": 1,
        "notes": "Test event"
    }


@pytest.fixture
def sample_completion_event(sample_event: Dict[str, Any]) -> Dict[str, Any]:
    """Sample completion event for testing."""
    event = sample_event.copy()
    event["type"] = "completed"
    event["result"] = "success"
    event["duration_seconds"] = 300
    event["commit_hash"] = "abc123"
    return event


# ============================================================================
# QUEUE FIXTURES
# ============================================================================

@pytest.fixture
def sample_queue() -> Dict[str, Any]:
    """Sample queue configuration for testing."""
    return {
        "metadata": {
            "last_updated": "2026-02-01T12:00:00Z",
            "updated_by": "planner",
            "queue_depth_target": "3-5",
            "current_depth": 3,
            "last_completed": "TASK-000"
        },
        "queue": [
            {
                "task_id": "TASK-001",
                "feature_id": "F-001",
                "title": "Test Task 1",
                "priority": "high",
                "status": "pending"
            },
            {
                "task_id": "TASK-002",
                "feature_id": "F-002",
                "title": "Test Task 2",
                "priority": "medium",
                "status": "pending"
            }
        ]
    }


# ============================================================================
# METRICS FIXTURES
# ============================================================================

@pytest.fixture
def sample_metrics() -> Dict[str, Any]:
    """Sample metrics for testing."""
    return {
        "system_health": {
            "overall": 9.0,
            "task_completion": 9.5,
            "queue_depth": 8.0,
            "feature_delivery": 9.0
        },
        "task_velocity": {
            "tasks_per_loop": 0.8,
            "avg_task_duration_minutes": 15
        },
        "feature_delivery": {
            "total_features": 5,
            "features_per_week": 2.5
        }
    }


# ============================================================================
# YAML FILE FIXTURES
# ============================================================================

@pytest.fixture
def valid_yaml_file(temp_dir: Path) -> Path:
    """Create a valid YAML file for testing."""
    yaml_file = temp_dir / "valid.yaml"
    with open(yaml_file, 'w') as f:
        yaml.dump({"key": "value", "number": 42}, f)
    return yaml_file


@pytest.fixture
def invalid_yaml_file(temp_dir: Path) -> Path:
    """Create an invalid YAML file for testing."""
    yaml_file = temp_dir / "invalid.yaml"
    with open(yaml_file, 'w') as f:
        f.write("key: value\n  bad: indentation: [")
    return yaml_file


# ============================================================================
# MOCK FIXTURES
# ============================================================================

@pytest.fixture
def mock_logger(mocker):
    """Mock logger for testing."""
    return mocker.patch('logging.getLogger')


@pytest.fixture
def mock_filesystem(temp_dir):
    """
    Mock filesystem operations to use temp directory.

    This fixture can be used to mock file operations in a safe temp directory.
    """
    class MockFilesystem:
        def __init__(self, base_path: Path):
            self.base_path = base_path

        def write_file(self, filename: str, content: str):
            """Write content to a file in the temp directory."""
            file_path = self.base_path / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
            return file_path

        def read_file(self, filename: str) -> str:
            """Read content from a file in the temp directory."""
            file_path = self.base_path / filename
            with open(file_path, 'r') as f:
                return f.read()

        def file_exists(self, filename: str) -> bool:
            """Check if a file exists in the temp directory."""
            return (self.base_path / filename).exists()

    return MockFilesystem(temp_dir)


# ============================================================================
# TEST DATA FIXTURES
# ============================================================================

@pytest.fixture
def test_data_dir(fixtures_dir: Path) -> Path:
    """Get the test data directory."""
    data_dir = fixtures_dir / "test_data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture
def sample_test_data(test_data_dir: Path) -> Path:
    """Create sample test data files."""
    data_file = test_data_dir / "sample.json"
    with open(data_file, 'w') as f:
        f.write('{"test": "data"}')
    return data_file
