"""Task data models for the Task Registry System."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import uuid4


class TaskState(Enum):
    """Possible states for a task."""
    BACKLOG = "BACKLOG"
    ASSIGNED = "ASSIGNED"
    ACTIVE = "ACTIVE"
    DONE = "DONE"
    FAILED = "FAILED"


class TaskPriority(Enum):
    """Priority levels for tasks."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """A task in the hierarchical planning system."""
    
    # Identity
    id: str
    title: str
    description: str
    
    # Hierarchy
    objective: str  # Which objective/epic this belongs to
    phase: Optional[str] = None  # Which phase within the objective
    
    # State tracking
    state: TaskState = TaskState.BACKLOG
    assignee: Optional[str] = None
    assigned_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Dependencies
    dependencies: List[str] = field(default_factory=list)
    blocks: List[str] = field(default_factory=list)
    
    # Workspace
    workspace: Optional[str] = None
    
    # External references
    github_issue: Optional[int] = None
    github_url: Optional[str] = None
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def can_assign(self) -> tuple[bool, Optional[str]]:
        """Check if task can be assigned.
        
        Returns:
            (can_assign, reason_if_not)
        """
        if self.state != TaskState.BACKLOG:
            return False, f"Task is {self.state.value}, not BACKLOG"
        
        # This would check the registry for dependency states
        # For now, return True - validation happens at registry level
        return True, None
    
    def can_start(self) -> tuple[bool, Optional[str]]:
        """Check if task can be started."""
        if self.state != TaskState.ASSIGNED:
            return False, f"Task is {self.state.value}, not ASSIGNED"
        
        if self.assignee is None:
            return False, "Task has no assignee"
        
        return True, None
    
    def can_complete(self) -> tuple[bool, Optional[str]]:
        """Check if task can be completed."""
        if self.state not in [TaskState.ASSIGNED, TaskState.ACTIVE]:
            return False, f"Task is {self.state.value}"
        
        # This would check for incomplete subtasks
        # For now, return True - validation happens at registry level
        return True, None
    
    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "objective": self.objective,
            "phase": self.phase,
            "state": self.state.value,
            "assignee": self.assignee,
            "assigned_at": self.assigned_at.isoformat() if self.assigned_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "dependencies": self.dependencies,
            "blocks": self.blocks,
            "workspace": self.workspace,
            "github_issue": self.github_issue,
            "github_url": self.github_url,
            "tags": self.tags,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create task from dictionary."""
        # Parse datetime fields
        for field_name in ["assigned_at", "started_at", "completed_at", "created_at", "updated_at"]:
            if data.get(field_name):
                data[field_name] = datetime.fromisoformat(data[field_name])
        
        # Parse enum fields
        data["state"] = TaskState(data["state"])
        data["priority"] = TaskPriority(data["priority"])
        
        return cls(**data)


@dataclass
class TaskStatistics:
    """Statistics about tasks in the registry."""
    total: int
    by_state: dict[TaskState, int]
    by_objective: dict[str, int]
    by_assignee: dict[str, int]
    
    def to_dict(self) -> dict:
        """Convert statistics to dictionary."""
        return {
            "total": self.total,
            "by_state": {state.value: count for state, count in self.by_state.items()},
            "by_objective": self.by_objective,
            "by_assignee": self.by_assignee,
        }


@dataclass
class TaskRegistry:
    """The task registry - single source of truth for all tasks."""
    
    version: str = "1.0"
    last_updated: datetime = field(default_factory=datetime.utcnow)
    tasks: dict[str, Task] = field(default_factory=dict)
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.tasks.get(task_id)
    
    def list_tasks(
        self,
        state: Optional[TaskState] = None,
        objective: Optional[str] = None,
        assignee: Optional[str] = None,
    ) -> list[Task]:
        """List tasks with optional filters."""
        tasks = list(self.tasks.values())
        
        if state:
            tasks = [t for t in tasks if t.state == state]
        
        if objective:
            tasks = [t for t in tasks if t.objective == objective]
        
        if assignee:
            tasks = [t for t in tasks if t.assignee == assignee]
        
        return tasks
    
    def get_available_tasks(self, assignee: Optional[str] = None) -> list[Task]:
        """Get tasks that can be assigned (dependencies met, not assigned)."""
        available = []
        
        for task in self.tasks.values():
            if task.state != TaskState.BACKLOG:
                continue
            
            # Check if dependencies are met
            deps_met = True
            for dep_id in task.dependencies:
                dep_task = self.tasks.get(dep_id)
                if not dep_task or dep_task.state != TaskState.DONE:
                    deps_met = False
                    break
            
            if deps_met:
                available.append(task)
        
        return available
    
    def calculate_statistics(self) -> TaskStatistics:
        """Calculate statistics about tasks."""
        by_state: dict[TaskState, int] = {state: 0 for state in TaskState}
        by_objective: dict[str, int] = {}
        by_assignee: dict[str, int] = {}
        
        for task in self.tasks.values():
            by_state[task.state] += 1
            by_objective[task.objective] = by_objective.get(task.objective, 0) + 1
            
            if task.assignee:
                by_assignee[task.assignee] = by_assignee.get(task.assignee, 0) + 1
        
        return TaskStatistics(
            total=len(self.tasks),
            by_state=by_state,
            by_objective=by_objective,
            by_assignee=by_assignee,
        )
    
    def to_dict(self) -> dict:
        """Convert registry to dictionary for JSON serialization."""
        return {
            "version": self.version,
            "last_updated": self.last_updated.isoformat(),
            "tasks": {task_id: task.to_dict() for task_id, task in self.tasks.items()},
            "statistics": self.calculate_statistics().to_dict(),
        }
