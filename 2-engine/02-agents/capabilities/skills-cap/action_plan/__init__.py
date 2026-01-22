"""
Action Plan Skill for Blackbox5

A comprehensive system for creating and executing structured action plans
with first principles integration, context management, and progress tracking.
"""

from .models import (
    ActionPhase,
    ActionTask,
    ActionSubtask,
    TaskContext,
    TaskResult,
    Checkpoint,
    PhaseStatus,
    TaskStatus,
    ConstraintType,
    Constraint,
    Assumption,
    FirstPrinciplesResult
)

from .action_plan import ActionPlan, create_action_plan
from .workspace_manager import WorkspaceManager
from .first_principles_integration import (
    FirstPrinciplesIntegration,
    create_first_principles_analysis
)

__version__ = "1.0.0"
__author__ = "Blackbox5 Team"

__all__ = [
    # Models
    'ActionPhase',
    'ActionTask',
    'ActionSubtask',
    'TaskContext',
    'TaskResult',
    'Checkpoint',
    'PhaseStatus',
    'TaskStatus',
    'ConstraintType',
    'Constraint',
    'Assumption',
    'FirstPrinciplesResult',

    # Core
    'ActionPlan',
    'create_action_plan',

    # Supporting
    'WorkspaceManager',
    'FirstPrinciplesIntegration',
    'create_first_principles_analysis'
]

# Skill metadata for Blackbox5 skills registry
SKILL_INFO = {
    'name': 'action_plan',
    'version': '1.0.0',
    'description': 'Structured action planning with first principles integration',
    'category': 'planning',
    'capabilities': [
        'create_action_plan',
        'manage_phases',
        'manage_tasks',
        'first_principles_analysis',
        'progress_tracking',
        'checkpoint_recovery',
        'workspace_management'
    ],
    'dependencies': [
        'first_principles'
    ],
    'examples': [
        'Create an action plan for implementing a new feature',
        'Plan a refactoring effort with multiple phases',
        'Organize a complex debugging task with first principles analysis'
    ]
}


def get_skill_info():
    """Return skill metadata."""
    return SKILL_INFO
