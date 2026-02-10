"""
Task Queue Data Models
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
import json


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"
    TIMEOUT = "timeout"
    RETRYING = "retrying"


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskType(Enum):
    """Types of tasks"""
    FEATURE = "feature"
    BUGFIX = "bugfix"
    REFACTOR = "refactor"
    TEST = "test"
    DOCUMENTATION = "documentation"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTENANCE = "maintenance"
    INVESTIGATION = "investigation"


@dataclass
class TaskDependency:
    """Task dependency"""
    task_id: str
    type: str  # "task", "epic", "external", "resource"
    description: str
    blocking: bool = True


@dataclass
class TaskProgress:
    """Task progress tracking"""
    percentage: int = 0
    current_step: str = ""
    total_steps: int = 0
    completed_steps: int = 0
    message: str = ""
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TaskResult:
    """Task execution result"""
    success: bool
    output: str = ""
    error_message: str = ""
    exit_code: Optional[int] = None
    duration_seconds: float = 0.0
    artifacts: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """Central task model for the queue system"""
    # Core identification
    task_id: str
    title: str
    description: str

    # Classification
    task_type: TaskType
    priority: TaskPriority
    status: TaskStatus = TaskStatus.PENDING

    # Execution details
    command: Optional[str] = None
    script_path: Optional[str] = None
    working_dir: Optional[str] = None
    environment: Dict[str, str] = field(default_factory=dict)
    timeout_seconds: int = 3600

    # Scheduling
    scheduled_at: Optional[str] = None
    deadline_at: Optional[str] = None
    estimated_duration_seconds: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    # Dependencies
    dependencies: List[TaskDependency] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)  # Task IDs

    # Execution tracking
    retry_count: int = 0
    max_retries: int = 3
    last_error: Optional[str] = None

    # Progress and results
    progress: Optional[TaskProgress] = None
    result: Optional[TaskResult] = None

    # Agent assignment
    assigned_agent: Optional[str] = None
    required_agent: Optional[str] = None

    # Metadata
    epic_id: Optional[str] = None
    prd_id: Optional[str] = None
    labels: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    # Scribe integration
    scribe_logged: bool = False
    scribe_doc_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'task_type': self.task_type.value,
            'priority': self.priority.value,
            'status': self.status.value,
            'command': self.command,
            'script_path': self.script_path,
            'working_dir': self.working_dir,
            'environment': json.dumps(self.environment),
            'timeout_seconds': self.timeout_seconds,
            'scheduled_at': self.scheduled_at,
            'deadline_at': self.deadline_at,
            'estimated_duration_seconds': self.estimated_duration_seconds,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'dependencies': json.dumps([d.__dict__ for d in self.dependencies]),
            'depends_on': json.dumps(self.depends_on),
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'last_error': self.last_error,
            'progress': json.dumps(self.progress.__dict__) if self.progress else None,
            'result': json.dumps(self.result.__dict__) if self.result else None,
            'assigned_agent': self.assigned_agent,
            'required_agent': self.required_agent,
            'epic_id': self.epic_id,
            'prd_id': self.prd_id,
            'labels': json.dumps(self.labels),
            'tags': json.dumps(self.tags),
            'scribe_logged': self.scribe_logged,
            'scribe_doc_path': self.scribe_doc_path,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create task from database dictionary"""
        return cls(
            task_id=data['task_id'],
            title=data['title'],
            description=data['description'],
            task_type=TaskType(data['task_type']),
            priority=TaskPriority(data['priority']),
            status=TaskStatus(data['status']),
            command=data.get('command'),
            script_path=data.get('script_path'),
            working_dir=data.get('working_dir'),
            environment=json.loads(data.get('environment', '{}')),
            timeout_seconds=data.get('timeout_seconds', 3600),
            scheduled_at=data.get('scheduled_at'),
            deadline_at=data.get('deadline_at'),
            estimated_duration_seconds=data.get('estimated_duration_seconds'),
            created_at=data['created_at'],
            started_at=data.get('started_at'),
            completed_at=data.get('completed_at'),
            dependencies=[TaskDependency(**d) for d in json.loads(data.get('dependencies', '[]'))],
            depends_on=json.loads(data.get('depends_on', '[]')),
            retry_count=data.get('retry_count', 0),
            max_retries=data.get('max_retries', 3),
            last_error=data.get('last_error'),
            progress=TaskProgress(**json.loads(data['progress'])) if data.get('progress') else None,
            result=TaskResult(**json.loads(data['result'])) if data.get('result') else None,
            assigned_agent=data.get('assigned_agent'),
            required_agent=data.get('required_agent'),
            epic_id=data.get('epic_id'),
            prd_id=data.get('prd_id'),
            labels=json.loads(data.get('labels', '[]')),
            tags=json.loads(data.get('tags', '[]')),
            scribe_logged=data.get('scribe_logged', False),
            scribe_doc_path=data.get('scribe_doc_path'),
        )

    def can_execute(self) -> bool:
        """Check if task can be executed"""
        if self.status not in [TaskStatus.PENDING, TaskStatus.QUEUED, TaskStatus.RETRYING]:
            return False
        if self.scheduled_at:
            scheduled_time = datetime.fromisoformat(self.scheduled_at)
            if datetime.now() < scheduled_time:
                return False
        return True

    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if not self.deadline_at:
            return False
        deadline = datetime.fromisoformat(self.deadline_at)
        return datetime.now() > deadline and self.status not in [
            TaskStatus.COMPLETED, TaskStatus.CANCELLED
        ]

    def priority_score(self) -> int:
        """Get numeric priority score for sorting"""
        scores = {
            TaskPriority.CRITICAL: 100,
            TaskPriority.HIGH: 75,
            TaskPriority.MEDIUM: 50,
            TaskPriority.LOW: 25,
        }
        return scores.get(self.priority, 50)
