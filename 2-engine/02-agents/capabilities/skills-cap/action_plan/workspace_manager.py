"""
Workspace Manager for Action Plans

Manages temporary workspaces for action plan execution.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import hashlib


class WorkspaceManager:
    """
    Manages temporary workspaces for action plan execution.

    Provides isolated environments for each action plan with:
    - Plan state storage
    - Task-specific context
    - Checkpoint management
    - Artifact storage
    - Execution logging
    """

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize the workspace manager.

        Args:
            base_path: Base directory for workspaces. Defaults to /tmp/action_plans/
        """
        if base_path is None:
            base_path = Path("/tmp/action_plans")

        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def create_workspace(self, plan_id: str) -> str:
        """
        Create a new workspace for an action plan.

        Args:
            plan_id: Unique identifier for the action plan

        Returns:
            Path to the created workspace
        """
        workspace_path = self.get_workspace_path(plan_id)

        # Create directory structure
        workspace_path.mkdir(parents=True, exist_ok=True)
        (workspace_path / "checkpoints").mkdir(exist_ok=True)
        (workspace_path / "tasks").mkdir(exist_ok=True)
        (workspace_path / "phases").mkdir(exist_ok=True)
        (workspace_path / "artifacts").mkdir(exist_ok=True)
        (workspace_path / "artifacts" / "diagrams").mkdir(exist_ok=True)
        (workspace_path / "artifacts" / "code").mkdir(exist_ok=True)
        (workspace_path / "artifacts" / "docs").mkdir(exist_ok=True)
        (workspace_path / "logs").mkdir(exist_ok=True)

        # Create workspace metadata
        metadata = {
            "plan_id": plan_id,
            "created_at": datetime.now().isoformat(),
            "workspace_path": str(workspace_path)
        }

        self._save_json(workspace_path / "workspace.json", metadata)

        return str(workspace_path)

    def get_workspace_path(self, plan_id: str) -> Path:
        """
        Get the path to a workspace.

        Args:
            plan_id: Unique identifier for the action plan

        Returns:
            Path to the workspace
        """
        return self.base_path / plan_id

    def workspace_exists(self, plan_id: str) -> bool:
        """
        Check if a workspace exists.

        Args:
            plan_id: Unique identifier for the action plan

        Returns:
            True if workspace exists
        """
        return self.get_workspace_path(plan_id).exists()

    def save_plan_state(self, plan_id: str, state: Dict[str, Any]) -> None:
        """
        Save the current plan state.

        Args:
            plan_id: Unique identifier for the action plan
            state: Plan state to save
        """
        workspace_path = self.get_workspace_path(plan_id)
        self._save_json(workspace_path / "plan.json", state)

    def load_plan_state(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """
        Load the current plan state.

        Args:
            plan_id: Unique identifier for the action plan

        Returns:
            Plan state or None if not found
        """
        workspace_path = self.get_workspace_path(plan_id)
        plan_file = workspace_path / "plan.json"

        if not plan_file.exists():
            return None

        return self._load_json(plan_file)

    def save_task_context(
        self,
        plan_id: str,
        task_id: str,
        context: Dict[str, Any]
    ) -> None:
        """
        Save task-specific context.

        Args:
            plan_id: Unique identifier for the action plan
            task_id: Unique identifier for the task
            context: Task context data
        """
        workspace_path = self.get_workspace_path(plan_id)
        task_dir = workspace_path / "tasks" / task_id
        task_dir.mkdir(exist_ok=True)

        self._save_json(task_dir / "context.json", context)

    def load_task_context(self, plan_id: str, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Load task-specific context.

        Args:
            plan_id: Unique identifier for the action plan
            task_id: Unique identifier for the task

        Returns:
            Task context or None if not found
        """
        workspace_path = self.get_workspace_path(plan_id)
        context_file = workspace_path / "tasks" / task_id / "context.json"

        if not context_file.exists():
            return None

        return self._load_json(context_file)

    def save_task_result(
        self,
        plan_id: str,
        task_id: str,
        result: Dict[str, Any]
    ) -> None:
        """
        Save task execution result.

        Args:
            plan_id: Unique identifier for the action plan
            task_id: Unique identifier for the task
            result: Task result data
        """
        workspace_path = self.get_workspace_path(plan_id)
        task_dir = workspace_path / "tasks" / task_id
        task_dir.mkdir(exist_ok=True)

        self._save_json(task_dir / "result.json", result)

    def load_task_result(self, plan_id: str, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Load task execution result.

        Args:
            plan_id: Unique identifier for the action plan
            task_id: Unique identifier for the task

        Returns:
            Task result or None if found
        """
        workspace_path = self.get_workspace_path(plan_id)
        result_file = workspace_path / "tasks" / task_id / "result.json"

        if not result_file.exists():
            return None

        return self._load_json(result_file)

    def save_task_thinking(
        self,
        plan_id: str,
        task_id: str,
        thinking: str
    ) -> None:
        """
        Save task thinking process (as markdown).

        Args:
            plan_id: Unique identifier for the action plan
            task_id: Unique identifier for the task
            thinking: Thinking process markdown
        """
        workspace_path = self.get_workspace_path(plan_id)
        task_dir = workspace_path / "tasks" / task_id
        task_dir.mkdir(exist_ok=True)

        with open(task_dir / "thinking.md", "w") as f:
            f.write(thinking)

    def load_task_thinking(self, plan_id: str, task_id: str) -> Optional[str]:
        """
        Load task thinking process.

        Args:
            plan_id: Unique identifier for the action plan
            task_id: Unique identifier for the task

        Returns:
            Thinking process or None if not found
        """
        workspace_path = self.get_workspace_path(plan_id)
        thinking_file = workspace_path / "tasks" / task_id / "thinking.md"

        if not thinking_file.exists():
            return None

        with open(thinking_file, "r") as f:
            return f.read()

    def save_phase_analysis(
        self,
        plan_id: str,
        phase_id: str,
        analysis: Dict[str, Any]
    ) -> None:
        """
        Save phase first principles analysis.

        Args:
            plan_id: Unique identifier for the action plan
            phase_id: Unique identifier for the phase
            analysis: Phase analysis data
        """
        workspace_path = self.get_workspace_path(plan_id)
        phase_dir = workspace_path / "phases" / phase_id
        phase_dir.mkdir(exist_ok=True)

        self._save_json(phase_dir / "analysis.json", analysis)

    def load_phase_analysis(
        self,
        plan_id: str,
        phase_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Load phase first principles analysis.

        Args:
            plan_id: Unique identifier for the action plan
            phase_id: Unique identifier for the phase

        Returns:
            Phase analysis or None if not found
        """
        workspace_path = self.get_workspace_path(plan_id)
        analysis_file = workspace_path / "phases" / phase_id / "analysis.json"

        if not analysis_file.exists():
            return None

        return self._load_json(analysis_file)

    def save_checkpoint(
        self,
        plan_id: str,
        checkpoint_id: str,
        checkpoint_data: Dict[str, Any]
    ) -> None:
        """
        Save a checkpoint.

        Args:
            plan_id: Unique identifier for the action plan
            checkpoint_id: Unique identifier for the checkpoint
            checkpoint_data: Checkpoint data
        """
        workspace_path = self.get_workspace_path(plan_id)
        checkpoints_dir = workspace_path / "checkpoints"

        checkpoint_file = checkpoints_dir / f"{checkpoint_id}.json"
        self._save_json(checkpoint_file, checkpoint_data)

    def load_checkpoint(
        self,
        plan_id: str,
        checkpoint_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Load a checkpoint.

        Args:
            plan_id: Unique identifier for the action plan
            checkpoint_id: Unique identifier for the checkpoint

        Returns:
            Checkpoint data or None if not found
        """
        workspace_path = self.get_workspace_path(plan_id)
        checkpoint_file = workspace_path / "checkpoints" / f"{checkpoint_id}.json"

        if not checkpoint_file.exists():
            return None

        return self._load_json(checkpoint_file)

    def list_checkpoints(self, plan_id: str) -> List[str]:
        """
        List all checkpoints for a plan.

        Args:
            plan_id: Unique identifier for the action plan

        Returns:
            List of checkpoint IDs sorted by timestamp (most recent last)
        """
        workspace_path = self.get_workspace_path(plan_id)
        checkpoints_dir = workspace_path / "checkpoints"

        if not checkpoints_dir.exists():
            return []

        checkpoints = []
        for checkpoint_file in sorted(checkpoints_dir.glob("*.json")):
            checkpoints.append(checkpoint_file.stem)

        return checkpoints

    def save_artifact(
        self,
        plan_id: str,
        artifact_type: str,
        artifact_name: str,
        content: str
    ) -> str:
        """
        Save an artifact (code, diagram, doc, etc.).

        Args:
            plan_id: Unique identifier for the action plan
            artifact_type: Type of artifact (code, diagrams, docs)
            artifact_name: Name of the artifact
            content: Artifact content

        Returns:
            Path to saved artifact
        """
        workspace_path = self.get_workspace_path(plan_id)
        artifact_dir = workspace_path / "artifacts" / artifact_type
        artifact_dir.mkdir(exist_ok=True)

        artifact_path = artifact_dir / artifact_name
        with open(artifact_path, "w") as f:
            f.write(content)

        return str(artifact_path)

    def log_execution(
        self,
        plan_id: str,
        message: str,
        level: str = "INFO"
    ) -> None:
        """
        Log an execution message.

        Args:
            plan_id: Unique identifier for the action plan
            message: Log message
            level: Log level (INFO, WARNING, ERROR, DEBUG)
        """
        workspace_path = self.get_workspace_path(plan_id)
        log_file = workspace_path / "logs" / "execution.log"

        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        with open(log_file, "a") as f:
            f.write(log_entry)

    def get_execution_log(self, plan_id: str) -> Optional[str]:
        """
        Get the execution log.

        Args:
            plan_id: Unique identifier for the action plan

        Returns:
            Execution log or None if not found
        """
        workspace_path = self.get_workspace_path(plan_id)
        log_file = workspace_path / "logs" / "execution.log"

        if not log_file.exists():
            return None

        with open(log_file, "r") as f:
            return f.read()

    def cleanup_workspace(self, plan_id: str) -> None:
        """
        Remove a workspace.

        Args:
            plan_id: Unique identifier for the action plan
        """
        workspace_path = self.get_workspace_path(plan_id)

        if workspace_path.exists():
            shutil.rmtree(workspace_path)

    def archive_workspace(
        self,
        plan_id: str,
        destination: Path
    ) -> None:
        """
        Archive a workspace to a destination.

        Args:
            plan_id: Unique identifier for the action plan
            destination: Destination path for archive
        """
        workspace_path = self.get_workspace_path(plan_id)

        if not workspace_path.exists():
            raise FileNotFoundError(f"Workspace not found: {plan_id}")

        # Create destination if needed
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)

        # Create archive
        archive_name = f"{plan_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        archive_path = destination / f"{archive_name}.tar.gz"

        shutil.make_archive(
            str(archive_path).replace('.tar.gz', ''),
            'gztar',
            str(workspace_path.parent),
            workspace_path.name
        )

    def _save_json(self, path: Path, data: Dict[str, Any]) -> None:
        """Save data to JSON file."""
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def _load_json(self, path: Path) -> Dict[str, Any]:
        """Load data from JSON file."""
        with open(path, "r") as f:
            return json.load(f)
