"""
Action Plan Data Models

Defines the core data structures for the Action Plan system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pathlib import Path


class PhaseStatus(Enum):
    """Status of a phase in the action plan."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class TaskStatus(Enum):
    """Status of a task in the action plan."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class ConstraintType(Enum):
    """Type of constraint."""
    HARD = "hard"  # Cannot violate (physics, law, math)
    SOFT = "soft"  # Can negotiate (preferences, conventions)


@dataclass
class Constraint:
    """A constraint (limitation or requirement)."""
    text: str
    type: ConstraintType
    source: str = "unknown"


@dataclass
class Assumption:
    """An assumption (belief without evidence)."""
    text: str
    confidence: str  # high, medium, low
    test: str = ""  # How to validate
    validated: bool = False


@dataclass
class FirstPrinciplesResult:
    """Result of first principles analysis."""
    true_problem: str
    fundamental_truths: List[str]
    assumptions: List[Assumption]
    essential_requirements: List[str]
    optional_elements: List[str]
    hypotheses: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'true_problem': self.true_problem,
            'fundamental_truths': self.fundamental_truths,
            'assumptions': [
                {
                    'text': a.text,
                    'confidence': a.confidence,
                    'test': a.test,
                    'validated': a.validated
                }
                for a in self.assumptions
            ],
            'essential_requirements': self.essential_requirements,
            'optional_elements': self.optional_elements,
            'hypotheses': self.hypotheses,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class TaskContext:
    """Template and context for task execution."""
    objective: str
    constraints: List[Constraint]
    assumptions: List[Assumption]
    resources: List[str]
    success_criteria: List[str]
    thinking_process: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'objective': self.objective,
            'constraints': [
                {'text': c.text, 'type': c.type.value, 'source': c.source}
                for c in self.constraints
            ],
            'assumptions': [
                {
                    'text': a.text,
                    'confidence': a.confidence,
                    'test': a.test,
                    'validated': a.validated
                }
                for a in self.assumptions
            ],
            'resources': self.resources,
            'success_criteria': self.success_criteria,
            'thinking_process': self.thinking_process,
            'metadata': self.metadata
        }


@dataclass
class ActionSubtask:
    """A subtask within an action task."""
    id: str
    parent_task_id: str
    title: str
    description: str
    thinking_process: str  # First principles reasoning
    status: TaskStatus = TaskStatus.PENDING
    order: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'parent_task_id': self.parent_task_id,
            'title': self.title,
            'description': self.description,
            'thinking_process': self.thinking_process,
            'status': self.status.value,
            'order': self.order,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


@dataclass
class ActionTask:
    """An executable task within a phase."""
    id: str
    phase_id: str
    title: str
    description: str
    context_template: TaskContext
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    subtasks: List[ActionSubtask] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    error: Optional[str] = None

    def add_subtask(self, subtask: ActionSubtask) -> None:
        """Add a subtask to this task."""
        self.subtasks.append(subtask)
        # Reorder by order field
        self.subtasks.sort(key=lambda st: st.order)

    def get_pending_subtasks(self) -> List[ActionSubtask]:
        """Get all pending subtasks."""
        return [st for st in self.subtasks if st.status == TaskStatus.PENDING]

    def is_ready(self, completed_task_ids: List[str]) -> bool:
        """Check if this task is ready to execute (dependencies satisfied)."""
        return all(dep_id in completed_task_ids for dep_id in self.dependencies)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'phase_id': self.phase_id,
            'title': self.title,
            'description': self.description,
            'context_template': self.context_template.to_dict(),
            'status': self.status.value,
            'dependencies': self.dependencies,
            'subtasks': [st.to_dict() for st in self.subtasks],
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'result': self.result,
            'error': self.error
        }


@dataclass
class ActionPhase:
    """A phase in the action plan."""
    id: str
    name: str
    description: str
    order: int
    first_principles_analysis: Optional[FirstPrinciplesResult] = None
    tasks: List[ActionTask] = field(default_factory=list)
    status: PhaseStatus = PhaseStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    exit_criteria: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def add_task(self, task: ActionTask) -> None:
        """Add a task to this phase."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[ActionTask]:
        """Get all pending tasks in this phase."""
        return [t for t in self.tasks if t.status == TaskStatus.PENDING]

    def is_ready(self, completed_phase_ids: List[str]) -> bool:
        """Check if this phase is ready to start (dependencies satisfied)."""
        return all(dep_id in completed_phase_ids for dep_id in self.dependencies)

    def is_complete(self) -> bool:
        """Check if all tasks in this phase are complete."""
        if not self.tasks:
            return False
        return all(t.status in [TaskStatus.COMPLETED, TaskStatus.SKIPPED]
                  for t in self.tasks)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'order': self.order,
            'first_principles_analysis': (
                self.first_principles_analysis.to_dict()
                if self.first_principles_analysis else None
            ),
            'tasks': [t.to_dict() for t in self.tasks],
            'status': self.status.value,
            'dependencies': self.dependencies,
            'exit_criteria': self.exit_criteria,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


@dataclass
class TaskResult:
    """Result from executing a task."""
    task_id: str
    success: bool
    output: str
    artifacts: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration: float = 0.0
    thinking_steps: List[str] = field(default_factory=list)
    completed_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'task_id': self.task_id,
            'success': self.success,
            'output': self.output,
            'artifacts': self.artifacts,
            'metadata': self.metadata,
            'error': self.error,
            'duration': self.duration,
            'thinking_steps': self.thinking_steps,
            'completed_at': self.completed_at.isoformat()
        }


@dataclass
class Checkpoint:
    """A checkpoint for plan recovery."""
    checkpoint_id: str
    timestamp: datetime
    plan_state: Dict[str, Any]
    context: Dict[str, Any]
    workspace_snapshot: Optional[str] = None  # Path to workspace snapshot

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'checkpoint_id': self.checkpoint_id,
            'timestamp': self.timestamp.isoformat(),
            'plan_state': self.plan_state,
            'context': self.context,
            'workspace_snapshot': self.workspace_snapshot
        }
