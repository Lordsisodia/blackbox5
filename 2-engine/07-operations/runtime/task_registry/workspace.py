"""Workspace factory for creating per-task workspaces."""

from pathlib import Path
from datetime import datetime
from typing import Union
import json


class WorkspaceFactory:
    """Creates and manages per-task workspaces."""
    
    def __init__(self, base_path: Union[str, Path] = "./workspaces"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def create_workspace(self, task_id: str, task_title: str) -> Path:
        """Create a new workspace for a task.
        
        Returns:
            Path to the created workspace
        """
        workspace_path = self.base_path / task_id
        workspace_path.mkdir(parents=True, exist_ok=True)
        
        # Create directory structure
        (workspace_path / "timeline").mkdir(exist_ok=True)
        (workspace_path / "thoughts").mkdir(exist_ok=True)
        (workspace_path / "context").mkdir(exist_ok=True)
        (workspace_path / "work").mkdir(exist_ok=True)
        
        # Create initial timeline entry
        self._add_timeline_entry(
            workspace_path,
            "created",
            {"task_id": task_id, "task_title": task_title}
        )
        
        # Create empty result.json
        result_path = workspace_path / "result.json"
        result_path.write_text(json.dumps({
            "task_id": task_id,
            "status": "created",
            "created_at": datetime.utcnow().isoformat(),
        }, indent=2))
        
        # Create README in workspace
        readme_path = workspace_path / "README.md"
        readme_path.write_text(f"""# Workspace for {task_id}

## Task: {task_title}

## Directory Structure

- **timeline/**: State transition history
- **thoughts/**: Agent thought dumps and analysis
- **context/**: Task context materials (PRDs, requirements, etc.)
- **work/**: Work in progress (code, drafts, etc.)
- **result.json**: Final output when task is complete

## Workflow

1. Review context materials in `context/`
2. Add analysis to `thoughts/` as you work
3. Place work in progress in `work/`
4. When complete, update `result.json` with final output
5. Mark task as complete via CLI

## Timeline

See `timeline/` for state transition history.
""")
        
        return workspace_path
    
    def get_workspace_path(self, task_id: str) -> Path:
        """Get the path to a task's workspace."""
        return self.base_path / task_id
    
    def workspace_exists(self, task_id: str) -> bool:
        """Check if a workspace exists for a task."""
        return (self.base_path / task_id).exists()
    
    def add_timeline_entry(
        self,
        task_id: str,
        event_type: str,
        data: dict,
    ):
        """Add a timeline entry to a task's workspace."""
        workspace_path = self.get_workspace_path(task_id)
        if not workspace_path.exists():
            raise ValueError(f"Workspace for {task_id} does not exist")
        
        self._add_timeline_entry(workspace_path, event_type, data)
    
    def _add_timeline_entry(self, workspace_path: Path, event_type: str, data: dict):
        """Internal method to add a timeline entry."""
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp}-{event_type}.json"
        timeline_path = workspace_path / "timeline" / filename
        
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "data": data,
        }
        
        timeline_path.write_text(json.dumps(entry, indent=2))
    
    def add_thought(self, task_id: str, thought_name: str, content: str):
        """Add a thought dump to a task's workspace."""
        workspace_path = self.get_workspace_path(task_id)
        if not workspace_path.exists():
            raise ValueError(f"Workspace for {task_id} does not exist")
        
        thoughts_path = workspace_path / "thoughts" / f"{thought_name}.md"
        thoughts_path.write_text(content)
    
    def add_context(self, task_id: str, context_name: str, content: str):
        """Add context material to a task's workspace."""
        workspace_path = self.get_workspace_path(task_id)
        if not workspace_path.exists():
            raise ValueError(f"Workspace for {task_id} does not exist")
        
        context_path = workspace_path / "context" / context_name
        context_path.write_text(content)
    
    def update_result(self, task_id: str, result_data: dict):
        """Update the result.json for a task."""
        workspace_path = self.get_workspace_path(task_id)
        if not workspace_path.exists():
            raise ValueError(f"Workspace for {task_id} does not exist")
        
        result_path = workspace_path / "result.json"
        result_data["updated_at"] = datetime.utcnow().isoformat()
        result_path.write_text(json.dumps(result_data, indent=2))
