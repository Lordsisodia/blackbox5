"""
Unit tests for test utilities.

Tests the test utility functions themselves.
"""

import pytest
import yaml
from pathlib import Path
import sys

# Add lib to path
AUTONOMOUS_LIB = Path(__file__).parent.parent.parent / ".autonomous" / "lib"
sys.path.insert(0, str(AUTONOMOUS_LIB))

# Import test utilities
TESTS_LIB = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(TESTS_LIB))

from test_utils import (
    assert_file_exists,
    assert_file_not_exists,
    assert_yaml_valid,
    assert_dict_contains,
    assert_lists_equal,
    create_mock_config,
    create_mock_task,
    create_mock_event,
    create_mock_queue,
    yaml_to_dict,
    dict_to_yaml,
    validate_task_structure,
    validate_event_structure
)


# ============================================================================
# TESTS FOR ASSERTION HELPERS
# ============================================================================

@pytest.mark.unit
def test_assert_file_exists_with_existing_file(temp_dir):
    """Test assert_file_exists with existing file."""
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")

    # Should not raise
    assert_file_exists(test_file)


@pytest.mark.unit
def test_assert_file_exists_with_nonexistent_file():
    """Test assert_file_exists with nonexistent file."""
    test_file = Path("/nonexistent/file.txt")

    with pytest.raises(AssertionError, match="File does not exist"):
        assert_file_exists(test_file)


@pytest.mark.unit
def test_assert_file_not_exists_with_nonexistent_file():
    """Test assert_file_not_exists with nonexistent file."""
    test_file = Path("/nonexistent/file.txt")

    # Should not raise
    assert_file_not_exists(test_file)


@pytest.mark.unit
def test_assert_file_not_exists_with_existing_file(temp_dir):
    """Test assert_file_not_exists with existing file."""
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")

    with pytest.raises(AssertionError, match="File should not exist"):
        assert_file_not_exists(test_file)


@pytest.mark.unit
def test_assert_yaml_valid_with_valid_yaml():
    """Test assert_yaml_valid with valid YAML."""
    valid_yaml = "key: value\nnumber: 42"

    # Should not raise
    assert_yaml_valid(valid_yaml)


@pytest.mark.unit
def test_assert_yaml_valid_with_invalid_yaml():
    """Test assert_yaml_valid with invalid YAML."""
    invalid_yaml = "key: value\n  bad: ["

    with pytest.raises(AssertionError, match="Invalid YAML"):
        assert_yaml_valid(invalid_yaml)


@pytest.mark.unit
def test_assert_dict_contains_with_matching_dict():
    """Test assert_dict_contains when dict contains expected values."""
    dict1 = {"key1": "value1", "key2": "value2", "key3": "value3"}
    dict2 = {"key1": "value1", "key3": "value3"}

    # Should not raise
    assert_dict_contains(dict1, dict2)


@pytest.mark.unit
def test_assert_dict_contains_with_missing_key():
    """Test assert_dict_contains when dict doesn't contain expected key."""
    dict1 = {"key1": "value1", "key2": "value2"}
    dict2 = {"key1": "value1", "key3": "value3"}

    with pytest.raises(AssertionError, match="Missing key: key3"):
        assert_dict_contains(dict1, dict2)


@pytest.mark.unit
def test_assert_dict_contains_with_mismatched_value():
    """Test assert_dict_contains when dict has different value."""
    dict1 = {"key1": "value1", "key2": "value2"}
    dict2 = {"key1": "value1", "key2": "different_value"}

    with pytest.raises(AssertionError):
        assert_dict_contains(dict1, dict2)


@pytest.mark.unit
def test_assert_lists_equal_with_equal_lists():
    """Test assert_lists_equal with equal lists."""
    list1 = ["a", "b", "c"]
    list2 = ["c", "b", "a"]

    # Should not raise (order-insensitive)
    assert_lists_equal(list1, list2)


@pytest.mark.unit
def test_assert_lists_equal_with_unequal_lists():
    """Test assert_lists_equal with unequal lists."""
    list1 = ["a", "b", "c"]
    list2 = ["a", "b", "d"]

    with pytest.raises(AssertionError, match="Lists are not equal"):
        assert_lists_equal(list1, list2)


# ============================================================================
# TESTS FOR FIXTURE GENERATORS
# ============================================================================

@pytest.mark.unit
def test_create_mock_config():
    """Test create_mock_config generates valid config."""
    config = create_mock_config()

    assert isinstance(config, dict)
    assert "executor" in config
    assert "planner" in config
    assert config["executor"]["skill_threshold"] == 0.7
    assert config["executor"]["max_retries"] == 3


@pytest.mark.unit
def test_create_mock_config_with_custom_values():
    """Test create_mock_config with custom values."""
    config = create_mock_config(
        executor_threshold=0.9,
        max_retries=5,
        queue_depth=10
    )

    assert config["executor"]["skill_threshold"] == 0.9
    assert config["executor"]["max_retries"] == 5
    assert config["planner"]["queue_depth_target"] == 10


@pytest.mark.unit
def test_create_mock_task():
    """Test create_mock_task generates valid task."""
    task = create_mock_task()

    assert isinstance(task, dict)
    assert task["task_id"] == "TASK-001"
    assert task["title"] == "Test Task"
    assert task["status"] == "pending"
    assert task["priority"] == "high"


@pytest.mark.unit
def test_create_mock_task_with_custom_values():
    """Test create_mock_task with custom values."""
    task = create_mock_task(
        task_id="TASK-999",
        title="Custom Task",
        status="completed",
        priority="critical"
    )

    assert task["task_id"] == "TASK-999"
    assert task["title"] == "Custom Task"
    assert task["status"] == "completed"
    assert task["priority"] == "critical"


@pytest.mark.unit
def test_create_mock_event():
    """Test create_mock_event generates valid event."""
    event = create_mock_event()

    assert isinstance(event, dict)
    assert event["task_id"] == "TASK-001"
    assert event["type"] == "started"
    assert "timestamp" in event
    assert "agent" in event


@pytest.mark.unit
def test_create_mock_event_with_result():
    """Test create_mock_event with result."""
    event = create_mock_event(result="success")

    assert event["type"] == "started"  # Default type
    assert event["result"] == "success"
    assert "duration_seconds" in event
    assert "commit_hash" in event


@pytest.mark.unit
def test_create_mock_queue():
    """Test create_mock_queue generates valid queue."""
    queue = create_mock_queue()

    assert isinstance(queue, dict)
    assert "metadata" in queue
    assert "queue" in queue
    assert isinstance(queue["queue"], list)
    assert len(queue["queue"]) == 2  # Default is 2 tasks


@pytest.mark.unit
def test_create_mock_queue_with_custom_tasks():
    """Test create_mock_queue with custom tasks."""
    tasks = [
        create_mock_task("TASK-001"),
        create_mock_task("TASK-002"),
        create_mock_task("TASK-003")
    ]
    queue = create_mock_queue(tasks)

    assert len(queue["queue"]) == 3
    assert queue["queue"][0]["task_id"] == "TASK-001"


# ============================================================================
# TESTS FOR YAML HELPERS
# ============================================================================

@pytest.mark.unit
def test_yaml_to_dict():
    """Test yaml_to_dict converts YAML to dict."""
    yaml_content = "key: value\nnumber: 42"
    result = yaml_to_dict(yaml_content)

    assert isinstance(result, dict)
    assert result["key"] == "value"
    assert result["number"] == 42


@pytest.mark.unit
def test_yaml_to_dict_with_invalid_yaml():
    """Test yaml_to_dict raises error for invalid YAML."""
    invalid_yaml = "key: value\n  bad: ["

    with pytest.raises(yaml.YAMLError):
        yaml_to_dict(invalid_yaml)


@pytest.mark.unit
def test_dict_to_yaml():
    """Test dict_to_yaml converts dict to YAML."""
    data = {"key": "value", "number": 42}
    result = dict_to_yaml(data)

    assert isinstance(result, str)
    assert "key: value" in result
    assert "number: 42" in result


@pytest.mark.unit
def test_dict_to_yaml_with_sorted_keys():
    """Test dict_to_yaml with sorted keys."""
    data = {"z": 1, "a": 2, "m": 3}
    result = dict_to_yaml(data, sort_keys=True)

    # Check that keys are in sorted order
    lines = result.strip().split("\n")
    assert lines[0].startswith("a:")
    assert lines[1].startswith("m:")
    assert lines[2].startswith("z:")


# ============================================================================
# TESTS FOR VALIDATION HELPERS
# ============================================================================

@pytest.mark.unit
def test_validate_task_structure_valid():
    """Test validate_task_structure with valid task."""
    task = create_mock_task()

    # Should not raise
    assert validate_task_structure(task) is True


@pytest.mark.unit
def test_validate_task_structure_missing_field():
    """Test validate_task_structure with missing field."""
    invalid_task = {
        "task_id": "TASK-001",
        # Missing "title", "type", "priority", "status"
    }

    with pytest.raises(AssertionError, match="missing required field"):
        validate_task_structure(invalid_task)


@pytest.mark.unit
def test_validate_event_structure_valid():
    """Test validate_event_structure with valid event."""
    event = create_mock_event()

    # Should not raise
    assert validate_event_structure(event) is True


@pytest.mark.unit
def test_validate_event_structure_missing_field():
    """Test validate_event_structure with missing field."""
    invalid_event = {
        "timestamp": "2026-02-01T12:00:00Z",
        # Missing "task_id", "type", "agent", "run_number"
    }

    with pytest.raises(AssertionError, match="missing required field"):
        validate_event_structure(invalid_event)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
def test_mock_workflow_end_to_end(temp_dir):
    """Test complete mock workflow: create config, task, event, queue."""
    # Create mock objects
    config = create_mock_config(executor_threshold=0.8)
    task = create_mock_task("TASK-001", "Test Task", "pending")
    event = create_mock_event("TASK-001", "started")
    queue = create_mock_queue([task])

    # Validate structures
    validate_task_structure(task)
    validate_event_structure(event)

    # Write to temp files
    config_file = temp_dir / "config.yaml"
    with open(config_file, 'w') as f:
        f.write(dict_to_yaml(config))

    # Verify file was created and is valid
    assert_file_exists(config_file)
    assert_yaml_file_valid(config_file)

    # Load and verify
    with open(config_file, 'r') as f:
        loaded_config = yaml.safe_load(f)

    assert_dict_contains(loaded_config, config)


@pytest.mark.integration
def test_yaml_conversion_roundtrip():
    """Test YAML conversion roundtrip: dict -> yaml -> dict."""
    original = {
        "executor": {
            "skill_threshold": 0.75,
            "max_retries": 3
        },
        "planner": {
            "queue_depth_target": 5
        }
    }

    # Convert to YAML
    yaml_str = dict_to_yaml(original)

    # Convert back to dict
    restored = yaml_to_dict(yaml_str)

    # Verify they match
    assert restored == original
