"""Integration tests for end-to-end task workflows."""

import json
import pytest
from pathlib import Path

from task_registry.registry import TaskRegistryManager
from task_registry.state_machine import TaskStateMachine, StateTransitionError
from task_registry.workspace import WorkspaceFactory
from task_registry.models import TaskState


@pytest.fixture
def full_system(tmp_path):
    """Set up a full task registry system."""
    registry_path = tmp_path / "registry.json"
    workspace_base = tmp_path / "workspaces"
    
    registry_manager = TaskRegistryManager(registry_path)
    state_machine = TaskStateMachine(registry_manager)
    workspace_factory = WorkspaceFactory(workspace_base)
    
    return {
        "registry": registry_manager,
        "state_machine": state_machine,
        "workspace": workspace_factory,
    }


class TestEpicImportWorkflow:
    """Test the complete epic import workflow."""
    
    def test_import_simple_epic(self, full_system, tmp_path):
        """Test importing a simple epic."""
        # Create a simple epic file
        epic_content = """---
name: Test Epic
status: planned
---

# Epic: Test Epic

## Overview

A test epic for integration testing.

### Phase 1: Foundation

**Task 1.1**: First task
- Description of first task
- **Dependencies**: None
- **Parallel**: No
- **Estimated**: 2 hours

**Task 1.2**: Second task
- Description of second task
- **Dependencies**: Task 1.1
- **Parallel**: No
- **Estimated**: 3 hours
"""
        epic_path = tmp_path / "test_epic.md"
        epic_path.write_text(epic_content)
        
        # Import the epic
        from task_registry.epic_import import EpicParser, import_from_epic
        
        parser = EpicParser(epic_path)
        epic_data = parser.parse()
        
        assert epic_data["name"] == "Test Epic"
        assert len(epic_data["tasks"]) == 2
        
        # Import into registry
        created = import_from_epic(
            epic_path,
            full_system["registry"],
            objective_name="test-epic",
        )
        
        assert len(created) == 2
        assert "TASK-1-1" in created
        assert "TASK-1-2" in created


class TestFullTaskLifecycle:
    """Test the complete task lifecycle from creation to completion."""
    
    def test_task_lifecycle(self, full_system):
        """Test: BACKLOG → ASSIGNED → ACTIVE → DONE."""
        registry = full_system["registry"]
        state_machine = full_system["state_machine"]
        workspace = full_system["workspace"]
        
        # 1. Create task
        task = registry.create_task(
            task_id="TASK-001",
            title="Lifecycle Test Task",
            description="Testing the full lifecycle",
            objective="test-lifecycle",
        )
        assert task.state == TaskState.BACKLOG
        
        # 2. Assign task
        task = state_machine.transition("TASK-001", TaskState.ASSIGNED, assignee="test-agent")
        assert task.state == TaskState.ASSIGNED
        assert task.assignee == "test-agent"
        assert workspace.workspace_exists("TASK-001")
        
        # 3. Start task
        task = state_machine.transition("TASK-001", TaskState.ACTIVE)
        assert task.state == TaskState.ACTIVE
        
        # 4. Complete task
        task = state_machine.transition("TASK-001", TaskState.DONE)
        assert task.state == TaskState.DONE
        assert task.completed_at is not None
        
        # 5. Verify workspace has timeline entries
        workspace_path = workspace.get_workspace_path("TASK-001")
        timeline_files = list((workspace_path / "timeline").glob("*.json"))
        assert len(timeline_files) >= 2  # assigned, started, completed
    
    def test_task_failure_and_retry(self, full_system):
        """Test: BACKLOG → ASSIGNED → ACTIVE → FAILED → BACKLOG → ASSIGNED."""
        state_machine = full_system["state_machine"]
        registry = full_system["registry"]
        
        # Create and assign task
        registry.create_task(
            task_id="TASK-001",
            title="Failing Task",
            description="Will fail then succeed",
            objective="test-failure",
        )
        state_machine.transition("TASK-001", TaskState.ASSIGNED, assignee="test-agent")
        state_machine.transition("TASK-001", TaskState.ACTIVE)
        
        # Fail the task
        task = state_machine.transition(
            "TASK-001",
            TaskState.FAILED,
            failure_reason="Simulated failure"
        )
        assert task.state == TaskState.FAILED
        
        # Retry - should go back to backlog
        task = state_machine.transition("TASK-001", TaskState.BACKLOG)
        assert task.state == TaskState.BACKLOG
        assert task.assignee is None


class TestDependencyWorkflow:
    """Test workflows involving task dependencies."""
    
    def test_sequential_dependencies(self, full_system):
        """Test that tasks must be done in order when dependencies exist."""
        registry = full_system["registry"]
        state_machine = full_system["state_machine"]
        
        # Create tasks: TASK-001 → TASK-002 → TASK-003
        registry.create_task(
            task_id="TASK-001",
            title="First Task",
            description="First in sequence",
            objective="test-deps",
        )
        registry.create_task(
            task_id="TASK-002",
            title="Second Task",
            description="Depends on TASK-001",
            objective="test-deps",
            dependencies=["TASK-001"],
        )
        registry.create_task(
            task_id="TASK-003",
            title="Third Task",
            description="Depends on TASK-002",
            objective="test-deps",
            dependencies=["TASK-002"],
        )
        
        # TASK-002 should not be available until TASK-001 is done
        available = registry.get_available_tasks()
        assert len(available) == 1
        assert available[0].id == "TASK-001"
        
        # Complete TASK-001
        state_machine.transition("TASK-001", TaskState.ASSIGNED, assignee="agent-1")
        state_machine.transition("TASK-001", TaskState.ACTIVE)
        state_machine.transition("TASK-001", TaskState.DONE)
        
        # Now TASK-002 should be available
        available = registry.get_available_tasks()
        assert len(available) == 1
        assert available[0].id == "TASK-002"
        
        # Complete TASK-002
        state_machine.transition("TASK-002", TaskState.ASSIGNED, assignee="agent-1")
        state_machine.transition("TASK-002", TaskState.ACTIVE)
        state_machine.transition("TASK-002", TaskState.DONE)
        
        # Now TASK-003 should be available
        available = registry.get_available_tasks()
        assert len(available) == 1
        assert available[0].id == "TASK-003"
    
    def test_parallel_tasks(self, full_system):
        """Test that independent tasks can be done in parallel."""
        registry = full_system["registry"]
        
        # Create independent tasks
        registry.create_task(
            task_id="TASK-001",
            title="Task A",
            description="Independent",
            objective="test-parallel",
        )
        registry.create_task(
            task_id="TASK-002",
            title="Task B",
            description="Independent",
            objective="test-parallel",
        )
        registry.create_task(
            task_id="TASK-003",
            title="Task C",
            description="Independent",
            objective="test-parallel",
        )
        
        # All should be available
        available = registry.get_available_tasks()
        assert len(available) == 3


class TestWorkspaceWorkflow:
    """Test workspace creation and management."""
    
    def test_workspace_timeline_tracking(self, full_system):
        """Test that workspace tracks all state changes."""
        registry = full_system["registry"]
        state_machine = full_system["state_machine"]
        workspace = full_system["workspace"]
        
        registry.create_task(
            task_id="TASK-001",
            title="Timeline Test",
            description="Testing timeline",
            objective="test-timeline",
        )
        
        # Assign
        state_machine.transition("TASK-001", TaskState.ASSIGNED, assignee="agent-1")
        
        # Start
        state_machine.transition("TASK-001", TaskState.ACTIVE)
        
        # Complete
        state_machine.transition("TASK-001", TaskState.DONE)
        
        # Check timeline
        workspace_path = workspace.get_workspace_path("TASK-001")
        timeline_files = sorted((workspace_path / "timeline").glob("*.json"))
        
        # Should have entries for: assigned, started, completed
        assert len(timeline_files) >= 3
        
        # Verify timeline entry format
        for timeline_file in timeline_files:
            with open(timeline_file) as f:
                entry = json.load(f)
            assert "timestamp" in entry
            assert "event_type" in entry
            assert "data" in entry
    
    def test_workspace_context_and_thoughts(self, full_system):
        """Test adding context and thoughts to workspace."""
        workspace = full_system["workspace"]
        registry = full_system["registry"]
        
        registry.create_task(
            task_id="TASK-001",
            title="Context Test",
            description="Testing context",
            objective="test-context",
        )
        
        # Add context
        workspace.add_context(
            "TASK-001",
            "requirements.md",
            "# Requirements\n\nRequirement 1: Do X"
        )
        
        # Add thought
        workspace.add_thought(
            "TASK-001",
            "analysis",
            "# Analysis\n\nHere's my analysis of the requirements."
        )
        
        # Verify files exist
        workspace_path = workspace.get_workspace_path("TASK-001")
        assert (workspace_path / "context" / "requirements.md").exists()
        assert (workspace_path / "thoughts" / "analysis.md").exists()


class TestVibeKanbanIntegration:
    """Test Vibe Kanban integration."""
    
    def test_active_tasks_filter(self, full_system):
        """Test that only ACTIVE tasks are returned for Vibe Kanban."""
        registry = full_system["registry"]
        state_machine = full_system["state_machine"]
        
        # Create multiple tasks
        registry.create_task(
            task_id="TASK-001",
            title="Backlog Task",
            description="In backlog",
            objective="test-kanban",
        )
        registry.create_task(
            task_id="TASK-002",
            title="Active Task",
            description="Being worked on",
            objective="test-kanban",
        )
        registry.create_task(
            task_id="TASK-003",
            title="Done Task",
            description="Completed",
            objective="test-kanban",
        )
        
        # Set states
        state_machine.transition("TASK-002", TaskState.ASSIGNED, assignee="agent-1")
        state_machine.transition("TASK-002", TaskState.ACTIVE)
        state_machine.transition("TASK-003", TaskState.ASSIGNED, assignee="agent-2")
        state_machine.transition("TASK-003", TaskState.DONE)
        
        # Get active tasks
        active_tasks = registry.list_tasks(state=TaskState.ACTIVE)
        
        # Only TASK-002 should be active
        assert len(active_tasks) == 1
        assert active_tasks[0].id == "TASK-002"
