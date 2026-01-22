"""Unit tests for the Workspace Factory."""

import json
import pytest
from pathlib import Path

from task_registry.workspace import WorkspaceFactory


@pytest.fixture
def workspace_factory(tmp_path):
    """Create a workspace factory with temporary base path."""
    return WorkspaceFactory(tmp_path / "workspaces")


class TestWorkspaceFactory:
    """Tests for the WorkspaceFactory."""

    def test_create_workspace(self, workspace_factory):
        """Test creating a new workspace."""
        workspace_path = workspace_factory.create_workspace(
            "TASK-001",
            "Test Task"
        )
        
        assert workspace_path.exists()
        assert (workspace_path / "timeline").exists()
        assert (workspace_path / "thoughts").exists()
        assert (workspace_path / "context").exists()
        assert (workspace_path / "work").exists()
        assert (workspace_path / "result.json").exists()
        assert (workspace_path / "README.md").exists()

    def test_workspace_has_initial_timeline_entry(self, workspace_factory):
        """Test that workspace has initial timeline entry."""
        workspace_path = workspace_factory.create_workspace(
            "TASK-001",
            "Test Task"
        )
        
        timeline_files = list((workspace_path / "timeline").glob("*.json"))
        assert len(timeline_files) >= 1
        
        # Check timeline entry format
        with open(timeline_files[0]) as f:
            entry = json.load(f)
        
        assert "timestamp" in entry
        assert "event_type" in entry
        assert entry["event_type"] == "created"

    def test_workspace_has_result_json(self, workspace_factory):
        """Test that workspace has result.json."""
        workspace_path = workspace_factory.create_workspace(
            "TASK-001",
            "Test Task"
        )
        
        result_path = workspace_path / "result.json"
        assert result_path.exists()
        
        with open(result_path) as f:
            result = json.load(f)
        
        assert result["task_id"] == "TASK-001"
        assert result["status"] == "created"

    def test_workspace_has_readme(self, workspace_factory):
        """Test that workspace has README.md."""
        workspace_path = workspace_factory.create_workspace(
            "TASK-001",
            "Test Task"
        )
        
        readme_path = workspace_path / "README.md"
        assert readme_path.exists()
        
        content = readme_path.read_text()
        assert "TASK-001" in content
        assert "Test Task" in content

    def test_get_workspace_path(self, workspace_factory):
        """Test getting workspace path."""
        workspace_factory.create_workspace("TASK-001", "Test Task")
        
        path = workspace_factory.get_workspace_path("TASK-001")
        assert path.exists()
        assert path.name == "TASK-001"

    def test_workspace_exists(self, workspace_factory):
        """Test checking if workspace exists."""
        assert not workspace_factory.workspace_exists("TASK-001")
        
        workspace_factory.create_workspace("TASK-001", "Test Task")
        assert workspace_factory.workspace_exists("TASK-001")

    def test_add_timeline_entry(self, workspace_factory):
        """Test adding a timeline entry."""
        workspace_factory.create_workspace("TASK-001", "Test Task")
        
        workspace_factory.add_timeline_entry(
            "TASK-001",
            "assigned",
            {"agent": "test-agent"}
        )
        
        workspace_path = workspace_factory.get_workspace_path("TASK-001")
        timeline_files = list((workspace_path / "timeline").glob("*.json"))
        assert len(timeline_files) >= 2  # created + assigned

    def test_add_thought(self, workspace_factory):
        """Test adding a thought dump."""
        workspace_factory.create_workspace("TASK-001", "Test Task")
        
        workspace_factory.add_thought(
            "TASK-001",
            "initial-analysis",
            "# Initial Analysis\n\nThis is my analysis."
        )
        
        thought_path = workspace_factory.get_workspace_path("TASK-001") / "thoughts" / "initial-analysis.md"
        assert thought_path.exists()
        content = thought_path.read_text()
        assert "Initial Analysis" in content

    def test_add_context(self, workspace_factory):
        """Test adding context material."""
        workspace_factory.create_workspace("TASK-001", "Test Task")
        
        workspace_factory.add_context(
            "TASK-001",
            "prd-requirements.md",
            "# PRD Requirements\n\nSome requirements."
        )
        
        context_path = workspace_factory.get_workspace_path("TASK-001") / "context" / "prd-requirements.md"
        assert context_path.exists()

    def test_update_result(self, workspace_factory):
        """Test updating result.json."""
        workspace_factory.create_workspace("TASK-001", "Test Task")
        
        result_data = {
            "task_id": "TASK-001",
            "status": "completed",
            "output": "Task completed successfully",
        }
        
        workspace_factory.update_result("TASK-001", result_data)
        
        result_path = workspace_factory.get_workspace_path("TASK-001") / "result.json"
        with open(result_path) as f:
            result = json.load(f)
        
        assert result["status"] == "completed"
        assert result["output"] == "Task completed successfully"
        assert "updated_at" in result

    def test_multiple_workspaces(self, workspace_factory):
        """Test creating multiple workspaces."""
        workspace_factory.create_workspace("TASK-001", "Task 1")
        workspace_factory.create_workspace("TASK-002", "Task 2")
        workspace_factory.create_workspace("TASK-003", "Task 3")
        
        assert workspace_factory.workspace_exists("TASK-001")
        assert workspace_factory.workspace_exists("TASK-002")
        assert workspace_factory.workspace_exists("TASK-003")
