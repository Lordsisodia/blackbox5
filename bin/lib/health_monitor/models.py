"""Data models for BB5 Health Monitor."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List


class TaskStatus(Enum):
    """Task status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class AgentStatus(Enum):
    """Agent status values."""
    ONLINE = "online"
    STALE = "stale"
    OFFLINE = "offline"


class HealthStatus(Enum):
    """Overall health status."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Task:
    """Represents a BB5 task."""
    id: str
    title: str
    status: TaskStatus
    priority: str
    estimated_minutes: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    agent: Optional[str] = None
    blocked_by: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    @property
    def is_in_progress(self) -> bool:
        return self.status == TaskStatus.IN_PROGRESS

    @property
    def is_pending(self) -> bool:
        return self.status == TaskStatus.PENDING

    @property
    def is_completed(self) -> bool:
        return self.status == TaskStatus.COMPLETED

    def elapsed_minutes(self) -> Optional[int]:
        """Calculate elapsed minutes since task started."""
        if self.started_at:
            elapsed = datetime.now() - self.started_at
            return int(elapsed.total_seconds() / 60)
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status.value,
            "priority": self.priority,
            "estimated_minutes": self.estimated_minutes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "agent": self.agent,
            "blocked_by": self.blocked_by,
            "tags": self.tags,
        }


@dataclass
class Agent:
    """Represents a BB5 agent."""
    name: str
    last_seen: datetime
    status: str
    loop_number: int
    current_task: Optional[str] = None
    version: Optional[str] = None

    def seconds_since_seen(self) -> int:
        """Calculate seconds since last heartbeat."""
        elapsed = datetime.now() - self.last_seen
        return int(elapsed.total_seconds())

    def is_stale(self, timeout_seconds: int = 120) -> bool:
        """Check if agent is stale based on timeout."""
        return self.seconds_since_seen() > timeout_seconds

    def is_online(self, timeout_seconds: int = 120) -> bool:
        """Check if agent is online."""
        return not self.is_stale(timeout_seconds)

    def get_status(self, timeout_seconds: int = 120) -> AgentStatus:
        """Get agent status."""
        if self.is_online(timeout_seconds):
            return AgentStatus.ONLINE
        elif self.seconds_since_seen() > timeout_seconds * 2:
            return AgentStatus.OFFLINE
        return AgentStatus.STALE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "status": self.status,
            "loop_number": self.loop_number,
            "current_task": self.current_task,
            "version": self.version,
            "seconds_since_seen": self.seconds_since_seen(),
        }


@dataclass
class Event:
    """Represents a BB5 event."""
    timestamp: datetime
    event_type: str
    task_id: Optional[str] = None
    agent: Optional[str] = None
    message: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "event_type": self.event_type,
            "task_id": self.task_id,
            "agent": self.agent,
            "message": self.message,
            "data": self.data,
        }


@dataclass
class HealthSnapshot:
    """Represents a health snapshot."""
    timestamp: datetime
    health_score: int
    status: HealthStatus
    queue_pending: int
    queue_in_progress: int
    queue_completed: int
    agents_online: int
    agents_stale: int
    agents_total: int
    stuck_tasks: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "health_score": self.health_score,
            "status": self.status.value,
            "queue": {
                "pending": self.queue_pending,
                "in_progress": self.queue_in_progress,
                "completed": self.queue_completed,
            },
            "agents": {
                "online": self.agents_online,
                "stale": self.agents_stale,
                "total": self.agents_total,
            },
            "stuck_tasks": self.stuck_tasks,
        }


@dataclass
class Metric:
    """Represents a time-series metric."""
    timestamp: datetime
    name: str
    value: float
    unit: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "tags": self.tags,
        }


@dataclass
class StuckTask:
    """Represents a stuck task with reason."""
    task: Task
    reason: str
    stuck_duration: str
    stuck_minutes: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task.to_dict(),
            "reason": self.reason,
            "stuck_duration": self.stuck_duration,
            "stuck_minutes": self.stuck_minutes,
        }
