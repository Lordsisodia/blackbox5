"""Unit tests for the Task Registry."""

import json
import pytest
from pathlib import Path
from datetime import datetime

from task_registry.models import Task, TaskState, TaskPriority, TaskRegistry
from task_registry.registry import TaskRegistryManager


@pytest.fixture
def temp_registry_path(tmp_path):
    """Create a temporary registry file path."""
    return tmp_path / "test_registry.json"


@pytest.fixture
def registry_manager(temp_registry_path):
    """Create a registry manager with temporary storage."""
    return TaskRegistryManager(temp_registry_path)


@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return Task(
        id="TASK-001",
        title="Test Task",
        description="A test task for unit testing",
        objective="test-objective",
        phase="foundation",
        priority=TaskPriority.HIGH,
    )


class TestTask:
    """Tests for the Task model."""

    def test_task_creation(self, sample_task):
        """Test creating a new task."""
        assert sample_task.id == "TASK-001"
        assert sample_task.title == "Test Task"
        assert sample_task.state == TaskState.BACKLOG
        assert sample_task.priority == TaskPriority.HIGH

    def test_task_to_dict(self, sample_task):
        """Test converting task to dictionary."""
        task_dict = sample_task.to_dict()
        assert task_dict["id"] == "TASK-001"
        assert task_dict["title"] == "Test Task"
        assert task_dict["state"] == "BACKLOG"
        assert task_dict["priority"] == "high"

    def test_task_from_dict(self):
        """Test creating task from dictionary."""
        task_data = {
            "id": "TASK-002",
            "title": "Another Task",
            "description": "Another test task",
            "objective": "test-objective",
            "phase": "implementation",
            "state": "BACKLOG",
            "priority": "medium",
            "dependencies": [],
            "blocks": [],
            "tags": [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        task = Task.from_dict(task_data)
        assert task.id == "TASK-002"
        assert task.title == "Another Task"
        assert task.state == TaskState.BACKLOG

    def test_can_assign_backlog_task(self, sample_task):
        """Test that backlog tasks can be assigned."""
        can_assign, reason = sample_task.can_assign()
        assert can_assign is True
        assert reason is None

    def test_cannot_assign_assigned_task(self, sample_task):
        """Test that assigned tasks cannot be reassigned."""
        sample_task.state = TaskState.ASSIGNED
        can_assign, reason = sample_task.can_assign()
        assert can_assign is False
        assert "not BACKLOG" in reason


class TestTaskRegistryManager:
    """Tests for the TaskRegistryManager."""

    def test_registry_initialization(self, registry_manager):
        """Test registry manager initializes empty registry."""
        registry = registry_manager.load()
        assert isinstance(registry, TaskRegistry)
        assert registry.version == "1.0"

    def test_create_task(self, registry_manager):
        """Test creating a new task."""
        task = registry_manager.create_task(
            task_id="TASK-001",
            title="New Task",
            description="A new task",
            objective="test-objective",
        )
        assert task.id == "TASK-001"
        assert task.title == "New Task"
        assert task.state == TaskState.BACKLOG

    def test_get_task(self, registry_manager):
        """Test retrieving a task."""
        registry_manager.create_task(
            task_id="TASK-001",
            title="New Task",
            description="A new task",
            objective="test-objective",
        )
        task = registry_manager.get_task("TASK-001")
        assert task is not None
        assert task.id == "TASK-001"

    def test_list_tasks(self, registry_manager):
        """Test listing all tasks."""
        registry_manager.create_task(
            task_id="TASK-001",
            title="Task 1",
            description="First task",
            objective="test-objective",
        )
        registry_manager.create_task(
            task_id="TASK-002",
            title="Task 2",
            description="Second task",
            objective="test-objective",
        )
        tasks = registry_manager.list_tasks()
        assert len(tasks) == 2

    def test_list_tasks_by_state(self, registry_manager):
        """Test filtering tasks by state."""
        registry_manager.create_task(
            task_id="TASK-001",
            title="Task 1",
            description="First task",
            objective="test-objective",
        )
        task2 = registry_manager.create_task(
            task_id="TASK-002",
            title="Task 2",
            description="Second task",
            objective="test-objective",
        )
        registry_manager.update_task("TASK-002", state=TaskState.DONE)

        backlog_tasks = registry_manager.list_tasks(state=TaskState.BACKLOG)
        done_tasks = registry_manager.list_tasks(state=TaskState.DONE)

        assert len(backlog_tasks) == 1
        assert len(done_tasks) == 1

    def test_update_task(self, registry_manager):
        """Test updating a task."""
        registry_manager.create_task(
            task_id="TASK-001",
            title="Original Title",
            description="Original description",
            objective="test-objective",
        )
        updated = registry_manager.update_task("TASK-001", title="Updated Title")
        assert updated.title == "Updated Title"

    def test_delete_task(self, registry_manager):
        """Test deleting a task."""
        registry_manager.create_task(
            task_id="TASK-001",
            title="Task to Delete",
            description="Will be deleted",
            objective="test-objective",
        )
        deleted = registry_manager.delete_task("TASK-001")
        assert deleted is True
        assert registry_manager.get_task("TASK-001") is None

    def test_get_available_tasks_no_dependencies(self, registry_manager):
        """Test getting tasks with no dependencies."""
        registry_manager.create_task(
            task_id="TASK-001",
            title="Available Task",
            description="No dependencies",
            objective="test-objective",
        )
        available = registry_manager.get_available_tasks()
        assert len(available) == 1

    def test_get_available_tasks_with_dependencies(self, registry_manager):
        """Test that tasks with dependencies are not available until deps are met."""
        # Create dependent task first
        registry_manager.create_task(
            task_id="TASK-001",
            title="Dependency",
            description="Must be done first",
            objective="test-objective",
        )
        # Create task that depends on TASK-001
        registry_manager.create_task(
            task_id="TASK-002",
            title="Dependent Task",
            description="Depends on TASK-001",
            objective="test-objective",
            dependencies=["TASK-001"],
        )

        available = registry_manager.get_available_tasks()
        # Only TASK-001 should be available
        assert len(available) == 1
        assert available[0].id == "TASK-001"

        # Complete TASK-001
        registry_manager.update_task("TASK-001", state=TaskState.DONE)

        # Now TASK-002 should be available
        available = registry_manager.get_available_tasks()
        assert len(available) == 1
        assert available[0].id == "TASK-002"

    def test_persistence(self, registry_manager, temp_registry_path):
        """Test that registry persists to disk."""
        registry_manager.create_task(
            task_id="TASK-001",
            title="Persistent Task",
            description="Should persist",
            objective="test-objective",
        )

        # Create new registry manager (simulates restart)
        new_manager = TaskRegistryManager(temp_registry_path)
        task = new_manager.get_task("TASK-001")
        assert task is not None
        assert task.title == "Persistent Task"

    def test_calculate_statistics(self, registry_manager):
        """Test calculating task statistics."""
        registry_manager.create_task(
            task_id="TASK-001",
            title="Task 1",
            description="First task",
            objective="test-objective",
        )
        registry_manager.create_task(
            task_id="TASK-002",
            title="Task 2",
            description="Second task",
            objective="test-objective",
        )
        registry_manager.update_task("TASK-002", state=TaskState.DONE)

        stats = registry_manager.get_statistics()
        assert stats.total == 2
        assert stats.by_state[TaskState.BACKLOG] == 1
        assert stats.by_state[TaskState.DONE] == 1
