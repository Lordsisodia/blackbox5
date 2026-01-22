"""
Action Plan Core Module

Main ActionPlan class that orchestrates the planning and execution process.
"""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable

from .models import (
    ActionPhase,
    ActionTask,
    ActionSubtask,
    TaskContext,
    TaskResult,
    PhaseStatus,
    TaskStatus,
    FirstPrinciplesResult,
    Checkpoint,
    Constraint,
    Assumption,
    ConstraintType
)
from .workspace_manager import WorkspaceManager
from .first_principles_integration import FirstPrinciplesIntegration


class ActionPlan:
    """
    Main Action Plan class that orchestrates planning and execution.

    Provides:
    - Plan creation and initialization
    - Phase and task management
    - First principles integration
    - Progress tracking and checkpointing
    - Workspace management
    """

    def __init__(
        self,
        name: str,
        description: str,
        workspace_path: Optional[str] = None,
        apply_first_principles: bool = True
    ):
        """
        Initialize an Action Plan.

        Args:
            name: Name of the action plan
            description: Description of what the plan achieves
            workspace_path: Path to workspace (auto-generated if None)
            apply_first_principles: Whether to apply first principles analysis
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.apply_first_principles = apply_first_principles

        # Phases and tasks
        self.phases: List[ActionPhase] = []
        self._phase_order: List[str] = []  # Track order of phase IDs

        # State tracking
        self.current_phase_id: Optional[str] = None
        self.current_task_id: Optional[str] = None
        self.completed_phase_ids: List[str] = []
        self.completed_task_ids: List[str] = []

        # First principles
        self.fp_integration = FirstPrinciplesIntegration() if apply_first_principles else None
        self.overall_fp_analysis: Optional[FirstPrinciplesResult] = None

        # Workspace
        self.workspace_manager = WorkspaceManager()
        if workspace_path:
            self.workspace_path = workspace_path
        else:
            self.workspace_path = self.workspace_manager.create_workspace(self.id)

        # Metadata
        self.metadata: Dict[str, Any] = {
            'decisions_made': [],
            'assumptions_validated': [],
            'blockers_resolved': []
        }

        # Initial analysis
        if self.fp_integration:
            self.overall_fp_analysis = self.fp_integration.analyze_problem(
                problem=f"{name}: {description}"
            )

        # Save initial state
        self._save_state()

    def add_phase(
        self,
        name: str,
        description: str,
        dependencies: Optional[List[str]] = None,
        exit_criteria: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ActionPhase:
        """
        Add a phase to the action plan.

        Args:
            name: Phase name
            description: Phase description
            dependencies: List of phase IDs this phase depends on
            exit_criteria: Criteria that must be met to complete the phase
            metadata: Additional metadata

        Returns:
            Created ActionPhase
        """
        phase_id = f"phase_{len(self.phases) + 1:03d}"
        order = len(self.phases) + 1

        # Apply first principles analysis if enabled
        fp_analysis = None
        if self.fp_integration:
            fp_analysis = self.fp_integration.analyze_phase(
                phase_name=name,
                phase_description=description,
                context={'plan_id': self.id, 'plan_name': self.name}
            )

        phase = ActionPhase(
            id=phase_id,
            name=name,
            description=description,
            order=order,
            first_principles_analysis=fp_analysis,
            dependencies=dependencies or [],
            exit_criteria=exit_criteria or [],
            metadata=metadata or {}
        )

        self.phases.append(phase)
        self._phase_order.append(phase_id)

        # Save phase analysis to workspace
        if fp_analysis:
            self.workspace_manager.save_phase_analysis(
                self.id,
                phase_id,
                fp_analysis.to_dict()
            )

        self._save_state()
        return phase

    def create_task(
        self,
        phase_id: str,
        title: str,
        description: str,
        context_template: TaskContext,
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ActionTask:
        """
        Create a task within a phase.

        Args:
            phase_id: ID of the phase to add the task to
            title: Task title
            description: Task description
            context_template: Task context template
            dependencies: List of task IDs this task depends on
            metadata: Additional metadata

        Returns:
            Created ActionTask
        """
        # Find the phase
        phase = self._get_phase_by_id(phase_id)
        if not phase:
            raise ValueError(f"Phase not found: {phase_id}")

        # Create task ID
        task_id = f"{phase_id}_task_{len(phase.tasks) + 1:03d}"

        # Create task
        task = ActionTask(
            id=task_id,
            phase_id=phase_id,
            title=title,
            description=description,
            context_template=context_template,
            dependencies=dependencies or [],
            metadata=metadata or {}
        )

        # Add to phase
        phase.add_task(task)

        # Save task context to workspace
        self.workspace_manager.save_task_context(
            self.id,
            task_id,
            context_template.to_dict()
        )

        self._save_state()
        return task

    def add_subtask(
        self,
        task_id: str,
        title: str,
        description: str,
        thinking_process: str,
        order: int = 0
    ) -> ActionSubtask:
        """
        Add a subtask to a task.

        Args:
            task_id: ID of the parent task
            title: Subtask title
            description: Subtask description
            thinking_process: First principles reasoning for this subtask
            order: Order of subtask (0 to append at end)

        Returns:
            Created ActionSubtask
        """
        # Find the task
        task = self._get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        # Create subtask ID
        subtask_id = f"{task_id}_sub_{len(task.subtasks) + 1:03d}"

        # Determine order
        if order == 0:
            order = len(task.subtasks) + 1

        # Create subtask
        subtask = ActionSubtask(
            id=subtask_id,
            parent_task_id=task_id,
            title=title,
            description=description,
            thinking_process=thinking_process,
            order=order
        )

        # Add to task
        task.add_subtask(subtask)

        self._save_state()
        return subtask

    def get_next_task(self) -> Optional[ActionTask]:
        """
        Get the next task ready for execution.

        Returns:
            Next ActionTask or None if no tasks are ready
        """
        # Check each phase in order
        for phase_id in self._phase_order:
            phase = self._get_phase_by_id(phase_id)

            # Skip if phase is already complete
            if phase.status == PhaseStatus.COMPLETED:
                continue

            # Check if phase is ready (dependencies satisfied)
            if not phase.is_ready(self.completed_phase_ids):
                continue

            # Mark phase as in progress
            if phase.status == PhaseStatus.PENDING:
                phase.status = PhaseStatus.IN_PROGRESS
                phase.started_at = datetime.now()
                self.current_phase_id = phase_id
                self._save_state()

            # Look for ready tasks in this phase
            for task in phase.tasks:
                if task.status == TaskStatus.PENDING and task.is_ready(self.completed_task_ids):
                    return task

        return None

    def start_task(self, task: ActionTask) -> None:
        """
        Mark a task as started.

        Args:
            task: Task to start
        """
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        self.current_task_id = task.id
        self._save_state()

        # Log to workspace
        self.workspace_manager.log_execution(
            self.id,
            f"Started task: {task.title}",
            level="INFO"
        )

    def complete_task(
        self,
        task_id: str,
        result: TaskResult
    ) -> None:
        """
        Mark a task as complete and save the result.

        Args:
            task_id: ID of the task
            result: Task execution result
        """
        task = self._get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        # Update task
        task.status = TaskStatus.COMPLETED if result.success else TaskStatus.FAILED
        task.completed_at = datetime.now()
        task.result = result.output
        task.error = result.error

        # Save result to workspace
        self.workspace_manager.save_task_result(
            self.id,
            task_id,
            result.to_dict()
        )

        # Add to completed list
        if result.success:
            self.completed_task_ids.append(task_id)

        # Log to workspace
        level = "INFO" if result.success else "ERROR"
        self.workspace_manager.log_execution(
            self.id,
            f"Completed task: {task.title} (success={result.success})",
            level=level
        )

        # Check if phase is complete
        self._check_phase_completion(task.phase_id)

        self.current_task_id = None
        self._save_state()

        # Create checkpoint
        self.create_checkpoint()

    def save_checkpoint(self) -> str:
        """
        Save a checkpoint for recovery.

        Returns:
            Checkpoint ID
        """
        checkpoint_id = f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        checkpoint_data = {
            'checkpoint_id': checkpoint_id,
            'timestamp': datetime.now().isoformat(),
            'plan_state': {
                'current_phase': self.current_phase_id,
                'current_task': self.current_task_id,
                'completed_phases': self.completed_phase_ids,
                'completed_tasks': self.completed_task_ids
            },
            'context': self.metadata
        }

        self.workspace_manager.save_checkpoint(self.id, checkpoint_id, checkpoint_data)

        return checkpoint_id

    def create_checkpoint(self) -> str:
        """
        Create a checkpoint (alias for save_checkpoint).
        """
        return self.save_checkpoint()

    def load_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Load a checkpoint to recover state.

        Args:
            checkpoint_id: ID of checkpoint to load

        Returns:
            True if checkpoint was loaded successfully
        """
        checkpoint_data = self.workspace_manager.load_checkpoint(self.id, checkpoint_id)

        if not checkpoint_data:
            return False

        # Restore state
        plan_state = checkpoint_data.get('plan_state', {})
        self.current_phase_id = plan_state.get('current_phase')
        self.current_task_id = plan_state.get('current_task')
        self.completed_phase_ids = plan_state.get('completed_phases', [])
        self.completed_task_ids = plan_state.get('completed_tasks', [])

        # Restore metadata
        self.metadata = checkpoint_data.get('context', {})

        return True

    def get_progress(self) -> Dict[str, Any]:
        """
        Get current progress of the action plan.

        Returns:
            Progress information
        """
        total_tasks = sum(len(phase.tasks) for phase in self.phases)
        completed_tasks = len(self.completed_task_ids)
        total_phases = len(self.phases)
        completed_phases = len(self.completed_phase_ids)

        return {
            'plan_id': self.id,
            'plan_name': self.name,
            'total_phases': total_phases,
            'completed_phases': completed_phases,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'phase_progress': f"{completed_phases}/{total_phases}",
            'task_progress': f"{completed_tasks}/{total_tasks}",
            'current_phase': self.current_phase_id,
            'current_task': self.current_task_id,
            'percent_complete': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }

    def generate_report(self) -> str:
        """
        Generate a human-readable progress report.

        Returns:
            Markdown report
        """
        progress = self.get_progress()

        report = f"""# Action Plan Report: {self.name}

## Overview
**Plan ID:** {self.id}
**Created:** {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}

**Description:** {self.description}

## Progress
- **Phases:** {progress['completed_phases']}/{progress['total_phases']} ({progress['phase_progress']})
- **Tasks:** {progress['completed_tasks']}/{progress['total_tasks']} ({progress['task_progress']})
- **Complete:** {progress['percent_complete']:.1f}%

"""

        # First principles analysis
        if self.overall_fp_analysis:
            report += "## First Principles Analysis\n\n"
            report += f"**True Problem:** {self.overall_fp_analysis.true_problem}\n\n"
            report += "**Fundamental Truths:**\n"
            for truth in self.overall_fp_analysis.fundamental_truths:
                report += f"- {truth}\n"
            report += "\n"

        # Phases
        report += "## Phases\n\n"
        for phase in self.phases:
            status_emoji = {
                PhaseStatus.PENDING: "⏳",
                PhaseStatus.IN_PROGRESS: "🔄",
                PhaseStatus.COMPLETED: "✅",
                PhaseStatus.BLOCKED: "🚫",
                PhaseStatus.FAILED: "❌"
            }.get(phase.status, "❓")

            report += f"### {status_emoji} Phase {phase.order}: {phase.name}\n"
            report += f"{phase.description}\n\n"

            if phase.first_principles_analysis:
                report += f"**True Problem:** {phase.first_principles_analysis.true_problem}\n\n"

            # Tasks
            for task in phase.tasks:
                task_status_emoji = {
                    TaskStatus.PENDING: "⏳",
                    TaskStatus.IN_PROGRESS: "🔄",
                    TaskStatus.COMPLETED: "✅",
                    TaskStatus.FAILED: "❌",
                    TaskStatus.BLOCKED: "🚫",
                    TaskStatus.SKIPPED: "⏭️"
                }.get(task.status, "❓")

                report += f"- {task_status_emoji} **Task:** {task.title}\n"

                if task.subtasks:
                    for subtask in task.subtasks:
                        st_status_emoji = {
                            TaskStatus.PENDING: "⏳",
                            TaskStatus.IN_PROGRESS: "🔄",
                            TaskStatus.COMPLETED: "✅",
                            TaskStatus.FAILED: "❌",
                        }.get(subtask.status, "❓")
                        report += f"  - {st_status_emoji} {subtask.title}\n"

            report += "\n"

        return report

    def cleanup(self) -> None:
        """
        Clean up the workspace.
        """
        self.workspace_manager.cleanup_workspace(self.id)

    def _get_phase_by_id(self, phase_id: str) -> Optional[ActionPhase]:
        """Get a phase by ID."""
        for phase in self.phases:
            if phase.id == phase_id:
                return phase
        return None

    def _get_task_by_id(self, task_id: str) -> Optional[ActionTask]:
        """Get a task by ID."""
        for phase in self.phases:
            for task in phase.tasks:
                if task.id == task_id:
                    return task
        return None

    def _check_phase_completion(self, phase_id: str) -> None:
        """Check if a phase is complete and update its status."""
        phase = self._get_phase_by_id(phase_id)
        if not phase:
            return

        if phase.is_complete():
            phase.status = PhaseStatus.COMPLETED
            phase.completed_at = datetime.now()
            self.completed_phase_ids.append(phase_id)

            # Log to workspace
            self.workspace_manager.log_execution(
                self.id,
                f"Completed phase: {phase.name}",
                level="INFO"
            )

    def _save_state(self) -> None:
        """Save current plan state to workspace."""
        state = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'current_phase_id': self.current_phase_id,
            'current_task_id': self.current_task_id,
            'completed_phase_ids': self.completed_phase_ids,
            'completed_task_ids': self.completed_task_ids,
            'phases': [phase.to_dict() for phase in self.phases],
            'metadata': self.metadata
        }

        self.workspace_manager.save_plan_state(self.id, state)


def create_action_plan(
    name: str,
    description: str,
    workspace_path: Optional[str] = None,
    apply_first_principles: bool = True
) -> ActionPlan:
    """
    Convenience function to create an action plan.

    Args:
        name: Name of the action plan
        description: Description of what the plan achieves
        workspace_path: Path to workspace (auto-generated if None)
        apply_first_principles: Whether to apply first principles analysis

    Returns:
        ActionPlan instance
    """
    return ActionPlan(
        name=name,
        description=description,
        workspace_path=workspace_path,
        apply_first_principles=apply_first_principles
    )
