"""
Unit tests for RoadmapSync library.

Tests roadmap synchronization, state updates, and improvement backlog sync.
"""

import pytest
import yaml
from pathlib import Path
import sys
import tempfile
import shutil

# Add lib to path
AUTONOMOUS_LIB = Path(__file__).parent.parent.parent / ".autonomous" / "lib"
sys.path.insert(0, str(AUTONOMOUS_LIB))

from roadmap_sync import (
    validate_state_yaml,
    extract_plan_id_from_task,
    find_plan_by_id,
    sync_roadmap_on_task_completion
)


# ============================================================================
# TESTS FOR STATE VALIDATION
# ============================================================================

@pytest.mark.unit
@pytest.mark.roadmap
def test_validate_state_yaml_valid_structure():
    """Test validation of valid STATE.yaml structure."""
    valid_state = {
        "plans": {
            "ready_to_start": [],
            "blocked": [],
            "completed": []
        },
        "next_action": "Some action"
    }

    is_valid, error = validate_state_yaml(valid_state)

    assert is_valid
    assert error is None


@pytest.mark.unit
@pytest.mark.roadmap
def test_validate_state_yaml_missing_plans():
    """Test validation fails when plans section is missing."""
    invalid_state = {
        "next_action": "Some action"
        # Missing "plans"
    }

    is_valid, error = validate_state_yaml(invalid_state)

    assert not is_valid
    assert "Missing required key: plans" in error


@pytest.mark.unit
@pytest.mark.roadmap
def test_validate_state_yaml_missing_next_action():
    """Test validation fails when next_action is missing."""
    invalid_state = {
        "plans": {
            "ready_to_start": []
        }
        # Missing "next_action"
    }

    is_valid, error = validate_state_yaml(invalid_state)

    assert not is_valid
    assert "Missing required key: next_action" in error


@pytest.mark.unit
@pytest.mark.roadmap
def test_validate_state_yaml_invalid_plans_type():
    """Test validation fails when plans is not a dict."""
    invalid_state = {
        "plans": "not_a_dict",  # Should be dict
        "next_action": "Some action"
    }

    is_valid, error = validate_state_yaml(invalid_state)

    assert not is_valid
    assert "plans section is not a dictionary" in error


@pytest.mark.unit
@pytest.mark.roadmap
def test_validate_state_yaml_invalid_plans_section_type():
    """Test validation fails when plans section is not a list."""
    invalid_state = {
        "plans": {
            "ready_to_start": "not_a_list"  # Should be list
        },
        "next_action": "Some action"
    }

    is_valid, error = validate_state_yaml(invalid_state)

    assert not is_valid
    assert "plans.ready_to_start is not a list" in error


# ============================================================================
# TESTS FOR PLAN ID EXTRACTION
# ============================================================================

@pytest.mark.unit
@pytest.mark.roadmap
def test_extract_plan_id_from_task_content():
    """Test extracting plan ID from task content."""
    task_content = """
    # TASK-123
    Plan ID: PLAN-001
    Some other content
    """

    plan_id = extract_plan_id_from_task("TASK-123", task_content)

    assert plan_id == "PLAN-001"


@pytest.mark.unit
@pytest.mark.roadmap
def test_extract_plan_id_from_task_id():
    """Test extracting plan ID from task ID itself."""
    task_id = "PLAN-002-TASK-456"

    plan_id = extract_plan_id_from_task(task_id)

    assert plan_id == "PLAN-002"


@pytest.mark.unit
@pytest.mark.roadmap
def test_extract_plan_id_no_match():
    """Test extract_plan_id returns None when no match found."""
    task_id = "TASK-123"
    task_content = "Some content without plan ID"

    plan_id = extract_plan_id_from_task(task_id, task_content)

    assert plan_id is None


@pytest.mark.unit
@pytest.mark.roadmap
def test_extract_plan_id_case_insensitive():
    """Test plan ID extraction is case-insensitive."""
    task_content = "plan id: plan-005"

    plan_id = extract_plan_id_from_task("TASK-123", task_content)

    assert plan_id == "PLAN-005"


# ============================================================================
# TESTS FOR PLAN FINDING
# ============================================================================

@pytest.mark.unit
@pytest.mark.roadmap
def test_find_plan_by_id_in_ready_to_start():
    """Test finding plan in ready_to_start section."""
    state_data = {
        "plans": {
            "ready_to_start": [
                {"id": "PLAN-001", "title": "Plan 1"},
                {"id": "PLAN-002", "title": "Plan 2"}
            ],
            "blocked": [],
            "completed": []
        },
        "next_action": "Test"
    }

    plan = find_plan_by_id(state_data, "PLAN-001")

    assert plan is not None
    assert plan["id"] == "PLAN-001"
    assert plan["title"] == "Plan 1"


@pytest.mark.unit
@pytest.mark.roadmap
def test_find_plan_by_id_in_completed():
    """Test finding plan in completed section."""
    state_data = {
        "plans": {
            "ready_to_start": [],
            "blocked": [],
            "completed": [
                {"id": "PLAN-003", "title": "Completed Plan"}
            ]
        },
        "next_action": "Test"
    }

    plan = find_plan_by_id(state_data, "PLAN-003")

    assert plan is not None
    assert plan["id"] == "PLAN-003"


@pytest.mark.unit
@pytest.mark.roadmap
def test_find_plan_by_id_not_found():
    """Test finding non-existent plan returns None."""
    state_data = {
        "plans": {
            "ready_to_start": [],
            "blocked": [],
            "completed": []
        },
        "next_action": "Test"
    }

    plan = find_plan_by_id(state_data, "PLAN-999")

    assert plan is None


@pytest.mark.unit
@pytest.mark.roadmap
def test_find_plan_by_id_case_insensitive():
    """Test plan finding is case-insensitive."""
    state_data = {
        "plans": {
            "ready_to_start": [
                {"id": "PLAN-001", "title": "Plan 1"}
            ],
            "blocked": [],
            "completed": []
        },
        "next_action": "Test"
    }

    plan = find_plan_by_id(state_data, "plan-001")

    assert plan is not None
    assert plan["id"] == "PLAN-001"


# ============================================================================
# TESTS FOR STATE SYNC
# ============================================================================

@pytest.mark.integration
@pytest.mark.roadmap
def test_sync_roadmap_updates_plan_status(temp_dir):
    """Test that sync_roadmap updates plan status to completed."""
    # Create test STATE.yaml
    state_file = temp_dir / "STATE.yaml"
    state_data = {
        "plans": {
            "ready_to_start": [
                {
                    "id": "PLAN-001",
                    "title": "Test Plan",
                    "status": "ready_to_start",
                    "task_id": "TASK-001"
                }
            ],
            "blocked": [],
            "completed": []
        },
        "next_action": "Execute PLAN-001"
    }

    with open(state_file, 'w') as f:
        yaml.dump(state_data, f)

    # Create test task file
    task_file = temp_dir / "TASK-001.md"
    task_content = "# TASK-001\nPlan ID: PLAN-001"
    with open(task_file, 'w') as f:
        f.write(task_content)

    # Sync
    result = sync_roadmap_on_task_completion(
        task_id="TASK-001",
        state_yaml_path=str(state_file),
        task_file_path=str(task_file)
    )

    # Verify result
    assert result["success"]
    assert result["plans_updated"] == 1

    # Verify STATE.yaml was updated
    with open(state_file, 'r') as f:
        updated_state = yaml.safe_load(f)

    # Plan should be moved to completed
    assert len(updated_state["plans"]["completed"]) == 1
    assert updated_state["plans"]["completed"][0]["id"] == "PLAN-001"
    assert updated_state["plans"]["completed"][0]["status"] == "completed"


@pytest.mark.integration
@pytest.mark.roadmap
def test_sync_roadmap_handles_missing_state_file():
    """Test that sync_roadmap handles missing STATE.yaml gracefully."""
    result = sync_roadmap_on_task_completion(
        task_id="TASK-001",
        state_yaml_path="/nonexistent/STATE.yaml"
    )

    # Should not raise exception, should return error
    assert "success" in result
    assert not result["success"] or result.get("error") is not None


@pytest.mark.integration
@pytest.mark.roadmap
def test_sync_roadmap_creates_backup(temp_dir):
    """Test that sync_roadmap creates backup before modifying."""
    state_file = temp_dir / "STATE.yaml"
    state_data = {
        "plans": {
            "ready_to_start": [
                {
                    "id": "PLAN-001",
                    "title": "Test Plan",
                    "status": "ready_to_start",
                    "task_id": "TASK-001"
                }
            ],
            "blocked": [],
            "completed": []
        },
        "next_action": "Execute PLAN-001"
    }

    with open(state_file, 'w') as f:
        yaml.dump(state_data, f)

    # Sync
    sync_roadmap_on_task_completion(
        task_id="TASK-001",
        state_yaml_path=str(state_file)
    )

    # Backup should exist
    backup_files = list(temp_dir.glob("STATE.yaml.backup*"))
    assert len(backup_files) > 0


@pytest.mark.integration
@pytest.mark.roadmap
def test_sync_roadmap_idempotent(temp_dir):
    """Test that sync_roadmap can run multiple times safely."""
    state_file = temp_dir / "STATE.yaml"
    state_data = {
        "plans": {
            "ready_to_start": [
                {
                    "id": "PLAN-001",
                    "title": "Test Plan",
                    "status": "ready_to_start",
                    "task_id": "TASK-001"
                }
            ],
            "blocked": [],
            "completed": []
        },
        "next_action": "Execute PLAN-001"
    }

    with open(state_file, 'w') as f:
        yaml.dump(state_data, f)

    # Run sync twice
    result1 = sync_roadmap_on_task_completion(
        task_id="TASK-001",
        state_yaml_path=str(state_file)
    )
    result2 = sync_roadmap_on_task_completion(
        task_id="TASK-001",
        state_yaml_path=str(state_file)
    )

    # Both should succeed
    assert result1["success"]
    assert result2["success"]

    # Plan should still be completed (not duplicated)
    with open(state_file, 'r') as f:
        final_state = yaml.safe_load(f)

    assert len(final_state["plans"]["completed"]) == 1


# ============================================================================
# TESTS FOR NEXT ACTION UPDATE
# ============================================================================

@pytest.mark.integration
@pytest.mark.roadmap
def test_sync_roadmap_updates_next_action(temp_dir):
    """Test that sync_roadmap updates next_action."""
    state_file = temp_dir / "STATE.yaml"
    state_data = {
        "plans": {
            "ready_to_start": [
                {
                    "id": "PLAN-001",
                    "title": "Test Plan",
                    "status": "ready_to_start",
                    "task_id": "TASK-001"
                },
                {
                    "id": "PLAN-002",
                    "title": "Next Plan",
                    "status": "ready_to_start",
                    "task_id": "TASK-002"
                }
            ],
            "blocked": [],
            "completed": []
        },
        "next_action": "Execute PLAN-001"
    }

    with open(state_file, 'w') as f:
        yaml.dump(state_data, f)

    # Sync PLAN-001
    sync_roadmap_on_task_completion(
        task_id="TASK-001",
        state_yaml_path=str(state_file)
    )

    # Verify next_action was updated
    with open(state_file, 'r') as f:
        updated_state = yaml.safe_load(f)

    assert "PLAN-002" in updated_state["next_action"]


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.roadmap
def test_sync_roadmap_with_no_matching_plan(temp_dir):
    """Test sync_roadmap when task doesn't match any plan."""
    state_file = temp_dir / "STATE.yaml"
    state_data = {
        "plans": {
            "ready_to_start": [
                {
                    "id": "PLAN-001",
                    "title": "Test Plan",
                    "status": "ready_to_start",
                    "task_id": "TASK-001"
                }
            ],
            "blocked": [],
            "completed": []
        },
        "next_action": "Execute PLAN-001"
    }

    with open(state_file, 'w') as f:
        yaml.dump(state_data, f)

    # Sync with non-matching task
    result = sync_roadmap_on_task_completion(
        task_id="TASK-999",  # Doesn't match any plan
        state_yaml_path=str(state_file)
    )

    # Should succeed but not update anything
    assert result["success"]
    assert result["plans_updated"] == 0
