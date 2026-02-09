# PLAN.md: Create Task Repository Abstraction

**Task:** TASK-SSOT-022 - Task operations scattered without abstraction
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 4-5 hours
**Importance:** 75 (High)

---

## 1. First Principles Analysis

### The Core Problem
Task operations are scattered throughout the codebase:
- Direct file reads/writes for tasks
- No centralized task management
- Inconsistent task state handling
- No validation on task operations
- Duplicate task query logic

This creates:
1. **Code Duplication**: Same task operations in multiple places
2. **Inconsistency**: Different ways to read/update tasks
3. **No Validation**: Invalid task states possible
4. **Query Complexity**: Hard to find tasks by criteria
5. **Maintenance Burden**: Changes needed in many places

### First Principles Solution
- **Repository Pattern**: Centralized task operations
- **Domain Model**: Task as first-class entity
- **Validation**: Ensure valid task states
- **Query Interface**: Easy task discovery
- **Event Publishing**: Task lifecycle events

---

## 2. Current State Analysis

### Current Task Operations

```python
# Pattern 1: Direct file read
task_file = f"tasks/active/{task_id}/task.md"
with open(task_file) as f:
    content = f.read()

# Pattern 2: Parse task status
status = "pending"
if "Status:** in_progress" in content:
    status = "in_progress"

# Pattern 3: Update task
with open(task_file, 'w') as f:
    f.write(updated_content)
```

### Issues

1. **No Abstraction**: Direct file manipulation
2. **String Parsing**: Fragile content parsing
3. **No Validation**: Can write invalid states
4. **No Events**: Other systems don't know about changes

---

## 3. Proposed Solution

### Task Domain Model

**File:** `2-engine/.autonomous/lib/task_model.py`

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class Task:
    """Task domain model."""
    id: str
    title: str
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    description: str = ""
    acceptance_criteria: List[str] = field(default_factory=list)
    assigned_to: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    parent_task: Optional[str] = None
    subtasks: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    def start(self, agent: str) -> None:
        """Mark task as started."""
        if self.status != TaskStatus.PENDING:
            raise InvalidStateError(f"Cannot start task in {self.status} state")
        self.status = TaskStatus.IN_PROGRESS
        self.assigned_to = agent
        self.started_at = datetime.now()

    def complete(self) -> None:
        """Mark task as completed."""
        if self.status != TaskStatus.IN_PROGRESS:
            raise InvalidStateError(f"Cannot complete task in {self.status} state")
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status.value,
            'priority': self.priority.value,
            'created_at': self.created_at.isoformat(),
            'description': self.description,
            'acceptance_criteria': self.acceptance_criteria,
            'assigned_to': self.assigned_to,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'parent_task': self.parent_task,
            'subtasks': self.subtasks,
            'tags': self.tags,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create Task from dictionary."""
        return cls(
            id=data['id'],
            title=data['title'],
            status=TaskStatus(data['status']),
            priority=TaskPriority(data['priority']),
            created_at=datetime.fromisoformat(data['created_at']),
            description=data.get('description', ''),
            acceptance_criteria=data.get('acceptance_criteria', []),
            assigned_to=data.get('assigned_to'),
            started_at=datetime.fromisoformat(data['started_at']) if data.get('started_at') else None,
            completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None,
            parent_task=data.get('parent_task'),
            subtasks=data.get('subtasks', []),
            tags=data.get('tags', []),
            metadata=data.get('metadata', {})
        )
```

### Task Repository

**File:** `2-engine/.autonomous/lib/task_repository.py`

```python
from typing import List, Optional, Callable
from .storage_backend import StorageBackend
from .task_model import Task, TaskStatus, TaskPriority

class TaskRepository:
    """Repository for task operations."""

    def __init__(self, storage: StorageBackend, event_publisher=None):
        self.storage = storage
        self.event_publisher = event_publisher

    def get(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        path = f"tasks/active/{task_id}/task.yaml"
        if not self.storage.exists(path):
            return None
        data = self.storage.read(path)
        return Task.from_dict(data)

    def save(self, task: Task) -> None:
        """Save task."""
        path = f"tasks/active/{task.id}/task.yaml"
        self.storage.write(path, task.to_dict())

        if self.event_publisher:
            self.event_publisher.publish('task.updated', task.to_dict())

    def list_all(self) -> List[Task]:
        """List all tasks."""
        task_dirs = self.storage.list("tasks/active")
        tasks = []
        for task_id in task_dirs:
            task = self.get(task_id)
            if task:
                tasks.append(task)
        return tasks

    def find_by_status(self, status: TaskStatus) -> List[Task]:
        """Find tasks by status."""
        return [t for t in self.list_all() if t.status == status]

    def find_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Find tasks by priority."""
        return [t for t in self.list_all() if t.priority == priority]

    def find_by_assignee(self, assignee: str) -> List[Task]:
        """Find tasks by assignee."""
        return [t for t in self.list_all() if t.assigned_to == assignee]

    def find_by_criteria(self, criteria: Callable[[Task], bool]) -> List[Task]:
        """Find tasks matching custom criteria."""
        return [t for t in self.list_all() if criteria(t)]

    def move_to_completed(self, task_id: str) -> None:
        """Move task to completed folder."""
        task = self.get(task_id)
        if not task:
            raise TaskNotFoundError(task_id)

        # Remove from active
        old_path = f"tasks/active/{task_id}"
        # Add to completed (implementation depends on storage backend)
        new_path = f"tasks/completed/{task_id}"
        self.storage.move(old_path, new_path)

    def create(self, task: Task) -> None:
        """Create new task."""
        # Validate
        if self.get(task.id):
            raise TaskExistsError(task.id)

        # Create directory and save
        path = f"tasks/active/{task.id}"
        self.storage.mkdir(path)
        self.save(task)

        if self.event_publisher:
            self.event_publisher.publish('task.created', task.to_dict())
```

### Implementation Plan

#### Phase 1: Create Task Model (1 hour)

1. Define Task dataclass
2. Define Status and Priority enums
3. Add validation methods
4. Add serialization methods

#### Phase 2: Create Task Repository (2 hours)

1. Implement CRUD operations
2. Add query methods
3. Add event publishing
4. Integrate with StorageBackend

#### Phase 3: Create Task Service (1 hour)

**File:** `2-engine/.autonomous/lib/task_service.py`

```python
class TaskService:
    """High-level task operations."""

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def start_task(self, task_id: str, agent: str) -> Task:
        """Start a task."""
        task = self.repository.get(task_id)
        if not task:
            raise TaskNotFoundError(task_id)

        task.start(agent)
        self.repository.save(task)
        return task

    def complete_task(self, task_id: str) -> Task:
        """Complete a task."""
        task = self.repository.get(task_id)
        if not task:
            raise TaskNotFoundError(task_id)

        task.complete()
        self.repository.save(task)
        self.repository.move_to_completed(task_id)
        return task
```

#### Phase 4: Add Tests (1 hour)

Create tests for:
- Task model validation
- Repository operations
- Service operations

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/lib/task_model.py` - Task domain model
2. `2-engine/.autonomous/lib/task_repository.py` - Task repository
3. `2-engine/.autonomous/lib/task_service.py` - Task service
4. `2-engine/.autonomous/lib/test_task.py` - Unit tests

---

## 5. Success Criteria

- [ ] Task model created with validation
- [ ] Task repository implemented
- [ ] Task service created
- [ ] All CRUD operations working
- [ ] Query methods working
- [ ] Event publishing integrated
- [ ] Unit tests passing

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Keep old file-based operations
2. **Fix**: Debug repository implementation
3. **Gradual Migration**: Migrate one operation at a time

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Task Model | 1 hour | 1 hour |
| Phase 2: Repository | 2 hours | 3 hours |
| Phase 3: Service | 1 hour | 4 hours |
| Phase 4: Tests | 1 hour | 5 hours |
| **Total** | | **4-5 hours** |

---

*Plan created based on SSOT violation analysis - Task operations scattered*
