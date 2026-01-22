"""Task Registry System - Single source of truth for hierarchical task execution tracking.

This module provides the execution tracking layer for the 3D planning structure
defined in epic.md and TASK-BREAKDOWN.md.

Main components:
- TaskRegistry: Central task database (JSON file)
- TaskStateMachine: State transitions and validation
- WorkspaceFactory: Per-task workspace creation
- CLI: Command-line interface for agents
- Integrations: Vibe Kanban and GitHub sync
"""

from .models import Task, TaskState, TaskPriority, TaskStatistics
from .registry import TaskRegistryManager
from .state_machine import TaskStateMachine, StateTransitionError
from .workspace import WorkspaceFactory

__version__ = "1.0.0"

__all__ = [
    # Models
    "Task",
    "TaskState",
    "TaskPriority",
    "TaskStatistics",
    # Core classes
    "TaskRegistryManager",
    "TaskStateMachine",
    "StateTransitionError",
    "WorkspaceFactory",
]
