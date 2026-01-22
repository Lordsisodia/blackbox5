"""Unit tests for the State Machine."""

import pytest
from datetime import datetime

from task_registry.models import Task, TaskState, TaskPriority
from task_registry.registry import TaskRegistryManager
from task_registry.state_machine import (
    TaskStateMachine,
    StateTransitionError,
)


@pytest.fixture
def registry_manager(tmp_path):
    """Create a registry manager with temporary storage."""
    return TaskRegistryManager(tmp_path / "test_registry.json")


@pytest.fixture
def state_machine(registry_manager):
    """Create a state machine."""
    return TaskStateMachine(registry_manager)


@pytest.fixture
def sample_task(registry_manager):
    """Create a sample task."""
    return registry_manager.create_task(
        task_id="TASK-001",
        title="Test Task",
        description="A test task",
        objective="test-objective",
    )


class TestStateMachine:
    """Tests for the TaskStateMachine."""

    def test_initial_state_is_backlog(self, sample_task):
        """Test that new tasks start in BACKLOG state."""
        assert sample_task.state == TaskState.BACKLOG

    def test_transition_backlog_to_assigned(self, state_machine):
        """Test transitioning from BACKLOG to ASSIGNED."""
        task = state_machine.transition(
            "TASK-001",
            TaskState.ASSIGNED,
            assignee="test-agent",
        )
        assert task.state == TaskState.ASSIGNED
        assert task.assignee == "test-agent"
        assert task.assigned_at is not None

    def test_transition_assigned_to_active(self, state_machine, sample_task):
        """Test transitioning from ASSIGNED to ACTIVE."""
        # First assign
        state_machine.transition("TASK-001", TaskState.ASSIGNED, assignee="test-agent")
        
        # Then start
        task = state_machine.transition("TASK-001", TaskState.ACTIVE)
        assert task.state == TaskState.ACTIVE
        assert task.started_at is not None

    def test_transition_active_to_done(self, state_machine):
        """Test transitioning from ACTIVE to DONE."""
        # Assign and start
        state_machine.transition("TASK-001", TaskState.ASSIGNED, assignee="test-agent")
        state_machine.transition("TASK-001", TaskState.ACTIVE)
        
        # Complete
        task = state_machine.transition("TASK-001", TaskState.DONE)
        assert task.state == TaskState.DONE
        assert task.completed_at is not None

    def test_cannot_assign_without_dependencies(self, registry_manager, state_machine):
        """Test that tasks with unmet dependencies cannot be assigned."""
        # Create dependency
        registry_manager.create_task(
            task_id="TASK-DEP",
            title="Dependency",
            description="Must be done first",
            objective="test-objective",
        )
        
        # Create dependent task
        registry_manager.create_task(
            task_id="TASK-001",
            title="Dependent Task",
            description="Depends on TASK-DEP",
            objective="test-objective",
            dependencies=["TASK-DEP"],
        )
        
        # Should fail - dependency not met
        with pytest.raises(StateTransitionError) as exc_info:
            state_machine.transition("TASK-001", TaskState.ASSIGNED, assignee="test-agent")
        
        assert "Dependency" in str(exc_info.value)

    def test_can_assign_with_met_dependencies(self, registry_manager, state_machine):
        """Test that tasks can be assigned when dependencies are met."""
        # Create and complete dependency
        registry_manager.create_task(
            task_id="TASK-DEP",
            title="Dependency",
            description="Must be done first",
            objective="test-objective",
        )
        registry_manager.update_task("TASK-DEP", state=TaskState.DONE)
        
        # Create dependent task
        registry_manager.create_task(
            task_id="TASK-001",
            title="Dependent Task",
            description="Depends on TASK-DEP",
            objective="test-objective",
            dependencies=["TASK-DEP"],
        )
        
        # Should succeed - dependency met
        task = state_machine.transition("TASK-001", TaskState.ASSIGNED, assignee="test-agent")
        assert task.state == TaskState.ASSIGNED

    def test_invalid_transition(self, state_machine):
        """Test that invalid transitions are rejected."""
        # Can't go from BACKLOG directly to ACTIVE
        with pytest.raises(StateTransitionError):
            state_machine.transition("TASK-001", TaskState.ACTIVE)

    def test_transition_to_failed(self, state_machine):
        """Test transitioning to FAILED state."""
        state_machine.transition("TASK-001", TaskState.ASSIGNED, assignee="test-agent")
        
        task = state_machine.transition(
            "TASK-001",
            TaskState.FAILED,
            failure_reason="Test failure",
        )
        assert task.state == TaskState.FAILED
        assert "failed: Test failure" in task.tags

    def test_get_blocking_tasks(self, registry_manager, state_machine):
        """Test getting tasks that block a task."""
        # Create dependency
        registry_manager.create_task(
            task_id="TASK-DEP",
            title="Dependency",
            description="Blocks TASK-001",
            objective="test-objective",
        )
        
        # Create dependent task
        registry_manager.create_task(
            task_id="TASK-001",
            title="Dependent Task",
            description="Depends on TASK-DEP",
            objective="test-objective",
            dependencies=["TASK-DEP"],
        )
        
        blocking = state_machine.get_blocking_tasks("TASK-001")
        assert len(blocking) == 1
        assert blocking[0].id == "TASK-DEP"

    def test_get_blocked_tasks(self, registry_manager, state_machine):
        """Test getting tasks that are blocked by a task."""
        # Create dependency
        registry_manager.create_task(
            task_id="TASK-DEP",
            title="Dependency",
            description="Blocks TASK-001",
            objective="test-objective",
        )
        
        # Create dependent task
        registry_manager.create_task(
            task_id="TASK-001",
            title="Dependent Task",
            description="Depends on TASK-DEP",
            objective="test-objective",
            dependencies=["TASK-DEP"],
        )
        
        blocked = state_machine.get_blocked_tasks("TASK-DEP")
        assert len(blocked) == 1
        assert blocked[0].id == "TASK-001"

    def test_valid_transitions_matrix(self):
        """Test the valid transitions matrix."""
        valid_from_backlog = TaskStateMachine.VALID_TRANSITIONS[TaskState.BACKLOG]
        assert TaskState.ASSIGNED in valid_from_backlog
        assert TaskState.FAILED in valid_from_backlog
        assert TaskState.ACTIVE not in valid_from_backlog

        valid_from_done = TaskStateMachine.VALID_TRANSITIONS[TaskState.DONE]
        assert len(valid_from_done) == 0  # Terminal state
