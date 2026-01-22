"""
Action Plan - Task Registry Integration

This module provides bidirectional integration between Action Plans and the Task Registry:
- Export Action Plan phases/tasks to Task Registry
- Import Task Registry tasks into Action Plans
- Sync status between systems
"""

import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

# Find the 2-engine directory for imports
current_dir = Path(__file__).parent
engine_dir = current_dir
while engine_dir.name != "2-engine" and engine_dir.parent != engine_dir:
    engine_dir = engine_dir.parent

if str(engine_dir) not in sys.path:
    sys.path.insert(0, str(engine_dir))

# Import models - handle both relative and absolute imports
try:
    from .models import (
        ActionPhase,
        ActionTask,
        ActionSubtask,
        TaskStatus,
        PhaseStatus,
        TaskContext,
        Constraint,
        Assumption,
        ConstraintType
    )
except ImportError:
    # Running standalone, use absolute import
    from models import (
        ActionPhase,
        ActionTask,
        ActionSubtask,
        TaskStatus,
        PhaseStatus,
        TaskContext,
        Constraint,
        Assumption,
        ConstraintType
    )

# Task Registry imports - handle if not available
try:
    from capabilities.runtime.task_registry.models import Task, TaskState, TaskPriority
    from capabilities.runtime.task_registry.registry import TaskRegistryManager
    TASK_REGISTRY_AVAILABLE = True
except ImportError:
    try:
        # Alternative import path
        sys.path.insert(0, str(engine_dir / "07-operations" / "runtime"))
        from task_registry.models import Task, TaskState, TaskPriority
        from task_registry.registry import TaskRegistryManager
        TASK_REGISTRY_AVAILABLE = True
    except ImportError:
        TASK_REGISTRY_AVAILABLE = False
        Task = None
        TaskState = None
        TaskPriority = None
        TaskRegistryManager = None


class TaskRegistryIntegration:
    """
    Integrates Action Plans with Task Registry System.

    Allows exporting Action Plan tasks to the Task Registry for tracking,
    and importing Task Registry tasks into Action Plans for planning.
    """

    def __init__(self, registry_path: str = "data/task_registry.json"):
        """
        Initialize the integration.

        Args:
            registry_path: Path to the task registry JSON file
        """
        if not TASK_REGISTRY_AVAILABLE:
            raise ImportError(
                "Task Registry is not available. Please ensure task_registry is installed.\n"
                "Location: 2-engine/07-operations/runtime/task_registry/"
            )

        self.registry_manager = TaskRegistryManager(registry_path)
        self.registry = self.registry_manager.load()

    def export_plan_to_registry(
        self,
        plan_name: str,
        phases: List[ActionPhase],
        objective: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[str]:
        """
        Export all tasks from an Action Plan to the Task Registry.

        Args:
            plan_name: Name of the action plan (used as objective if not provided)
            phases: List of ActionPhase objects to export
            objective: Objective name for tasks (defaults to plan_name)
            tags: Tags to add to all tasks

        Returns:
            List of created task IDs
        """
        if not TASK_REGISTRY_AVAILABLE:
            raise RuntimeError("Task Registry not available")

        if objective is None:
            objective = plan_name

        if tags is None:
            tags = ["action-plan"]

        created_task_ids = []

        for phase in phases:
            for task in phase.tasks:
                # Convert ActionTask to Task Registry Task
                task_id = f"ap-{task.id}"

                # Map dependencies
                dependencies = [
                    f"ap-{dep_id}" for dep_id in task.dependencies
                ]

                # Extract description from context if available
                description = task.description
                if task.context_template and task.context_template.objective:
                    description += f"\n\nObjective: {task.context_template.objective}"

                    # Add constraints to description
                    if task.context_template.constraints:
                        description += "\n\nConstraints:"
                        for c in task.context_template.constraints:
                            description += f"\n  - [{c.type.value.upper()}] {c.text}"

                    # Add assumptions to description
                    if task.context_template.assumptions:
                        description += "\n\nAssumptions:"
                        for a in task.context_template.assumptions:
                            description += f"\n  - [{a.confidence}] {a.text}"

                # Create task in registry
                registry_task = self.registry_manager.create_task(
                    task_id=task_id,
                    title=task.title,
                    description=description,
                    objective=objective,
                    phase=phase.name,
                    dependencies=dependencies,
                    tags=tags + [f"phase:{phase.name}"]
                )

                created_task_ids.append(task_id)

                # Export subtasks as separate tasks
                for subtask in task.subtasks:
                    subtask_id = f"ap-{subtask.id}"
                    subtask_deps = [task_id]  # Subtask depends on parent task

                    subtask_description = subtask.description
                    if subtask.thinking_process:
                        subtask_description += f"\n\nThinking Process:\n{subtask.thinking_process}"

                    self.registry_manager.create_task(
                        task_id=subtask_id,
                        title=f"[Subtask] {subtask.title}",
                        description=subtask_description,
                        objective=objective,
                        phase=phase.name,
                        dependencies=subtask_deps,
                        tags=tags + [f"phase:{phase.name}", "subtask"]
                    )

                    created_task_ids.append(subtask_id)

        return created_task_ids

    def import_tasks_to_plan(
        self,
        objective: str,
        phase_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Import tasks from Task Registry as Action Plan task templates.

        Args:
            objective: Objective name to filter tasks
            phase_filter: Optional phase name to filter

        Returns:
            List of task dictionaries suitable for creating ActionTasks
        """
        if not TASK_REGISTRY_AVAILABLE:
            raise RuntimeError("Task Registry not available")

        # Get tasks for the objective
        tasks = self.registry_manager.list_tasks(objective=objective)

        if phase_filter:
            tasks = [t for t in tasks if t.phase == phase_filter]

        # Filter out subtasks (they'll be handled separately)
        main_tasks = [t for t in tasks if "subtask" not in t.tags]

        task_templates = []

        for task in main_tasks:
            # Build TaskContext from task description and metadata
            context = TaskContext(
                objective=task.title,
                constraints=[],
                assumptions=[],
                resources=[],
                success_criteria=[],
                thinking_process=f"Imported from Task Registry\nOriginal ID: {task.id}"
            )

            # Extract dependencies (remove 'ap-' prefix if present)
            dependencies = [
                dep_id.replace("ap-", "") for dep_id in task.dependencies
            ]

            task_template = {
                "id": task.id.replace("ap-", ""),
                "title": task.title,
                "description": task.description,
                "phase": task.phase,
                "context_template": context,
                "dependencies": dependencies
            }

            task_templates.append(task_template)

        return task_templates

    def sync_task_status(
        self,
        action_task: ActionTask,
        task_id: Optional[str] = None
    ) -> bool:
        """
        Sync task status from Action Plan to Task Registry.

        Args:
            action_task: The ActionTask to sync from
            task_id: Optional Task Registry ID (defaults to f"ap-{action_task.id}")

        Returns:
            True if sync was successful
        """
        if not TASK_REGISTRY_AVAILABLE:
            return False

        if task_id is None:
            task_id = f"ap-{action_task.id}"

        # Map TaskStatus to TaskState
        status_map = {
            TaskStatus.PENDING: TaskState.BACKLOG,
            TaskStatus.IN_PROGRESS: TaskState.ACTIVE,
            TaskStatus.COMPLETED: TaskState.DONE,
            TaskStatus.FAILED: TaskState.FAILED,
            TaskStatus.BLOCKED: TaskState.BACKLOG,
            TaskStatus.SKIPPED: TaskState.DONE
        }

        new_state = status_map.get(action_task.status)
        if new_state:
            self.registry_manager.update_task(task_id, state=new_state.value)

        return True

    def sync_registry_status_to_plan(
        self,
        task_id: str,
        phases: List[ActionPhase]
    ) -> bool:
        """
        Sync task status from Task Registry to Action Plan.

        Args:
            task_id: Task Registry ID (with or without 'ap-' prefix)
            phases: List of phases to search for the task

        Returns:
            True if sync was successful
        """
        if not TASK_REGISTRY_AVAILABLE:
            return False

        # Normalize task ID
        if not task_id.startswith("ap-"):
            task_id = f"ap-{task_id}"

        # Get task from registry
        registry_task = self.registry_manager.get_task(task_id)
        if not registry_task:
            return False

        # Find corresponding ActionTask
        action_task_id = task_id.replace("ap-", "")
        for phase in phases:
            for task in phase.tasks:
                if task.id == action_task_id:
                    # Map TaskState to TaskStatus
                    state_map = {
                        TaskState.BACKLOG: TaskStatus.PENDING,
                        TaskState.ASSIGNED: TaskStatus.PENDING,
                        TaskState.ACTIVE: TaskStatus.IN_PROGRESS,
                        TaskState.DONE: TaskStatus.COMPLETED,
                        TaskState.FAILED: TaskStatus.FAILED
                    }

                    new_status = state_map.get(registry_task.state)
                    if new_status:
                        task.status = new_status

                    return True

        return False

    def create_plan_from_registry(
        self,
        objective: str,
        plan_name: str,
        description: str
    ) -> Dict[str, Any]:
        """
        Create a complete Action Plan structure from Task Registry tasks.

        Args:
            objective: Objective name in Task Registry
            plan_name: Name for the Action Plan
            description: Description of the plan

        Returns:
            Dictionary with phases data ready for ActionPlan creation
        """
        if not TASK_REGISTRY_AVAILABLE:
            raise RuntimeError("Task Registry not available")

        # Get all tasks for the objective
        tasks = self.registry_manager.list_tasks(objective=objective)

        # Group by phase
        phases_by_name: Dict[str, List[Task]] = {}
        for task in tasks:
            if "subtask" in task.tags:
                continue  # Skip subtasks for now

            phase_name = task.phase or "Default"
            if phase_name not in phases_by_name:
                phases_by_name[phase_name] = []
            phases_by_name[phase_name].append(task)

        # Build phases data
        phases_data = []
        phase_order = 1

        for phase_name, phase_tasks in sorted(phases_by_name.items()):
            phase_data = {
                "name": phase_name,
                "description": f"Phase for {objective}",
                "order": phase_order,
                "tasks": []
            }

            for task in phase_tasks:
                # Build context template
                context = TaskContext(
                    objective=task.title,
                    constraints=[
                        Constraint(
                            text="Imported from Task Registry",
                            type=ConstraintType.SOFT,
                            source="task_registry"
                        )
                    ],
                    assumptions=[],
                    resources=[],
                    success_criteria=[]
                )

                task_data = {
                    "title": task.title,
                    "description": task.description,
                    "context_template": context,
                    "dependencies": [
                        d.replace("ap-", "") for d in task.dependencies
                    ]
                }

                phase_data["tasks"].append(task_data)

            phases_data.append(phase_data)
            phase_order += 1

        return {
            "plan_name": plan_name,
            "description": description,
            "phases": phases_data
        }


def export_action_plan(
    plan_name: str,
    phases: List[ActionPhase],
    registry_path: str = "data/task_registry.json"
) -> List[str]:
    """
    Convenience function to export an Action Plan to Task Registry.

    Args:
        plan_name: Name of the action plan
        phases: List of ActionPhase objects
        registry_path: Path to task registry file

    Returns:
        List of created task IDs
    """
    integration = TaskRegistryIntegration(registry_path)
    return integration.export_plan_to_registry(plan_name, phases)


def import_action_plan(
    objective: str,
    registry_path: str = "data/task_registry.json"
) -> List[Dict[str, Any]]:
    """
    Convenience function to import tasks from Task Registry.

    Args:
        objective: Objective name to import
        registry_path: Path to task registry file

    Returns:
        List of task templates
    """
    integration = TaskRegistryIntegration(registry_path)
    return integration.import_tasks_to_plan(objective)
