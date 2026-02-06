# PLAN.md: Queue/Communication System Abstraction

**Task:** TASK-ARCH-021: No Abstraction for Queue/Communication System  
**Status:** Planning  
**Priority:** HIGH  
**Estimated Effort:** 90 minutes  
**Created:** 2026-02-06  

---

## 1. First Principles Analysis

### The Core Problem

The 6-agent pipeline (Scout → Planner → Executor → Verifier + Analyst + Orchestrator) currently uses raw YAML file operations with inline Python parsing for all inter-agent communication. This creates several fundamental issues:

1. **Tight Coupling**: Agents know the exact file paths and YAML structure of other agents
2. **No Encapsulation**: Queue operations are scattered across multiple files with duplicate parsing logic
3. **Brittleness**: Changes to queue structure require updates in multiple places
4. **No Flexibility**: Cannot easily switch from file-based to Redis-based communication
5. **Testing Difficulty**: Cannot mock queue operations for unit testing

### What Should Be True

1. Agents should communicate through a well-defined interface, not raw file operations
2. The storage mechanism (file, Redis, database) should be swappable without changing agent code
3. Queue operations should be atomic and encapsulated
4. The interface should support both synchronous and asynchronous patterns
5. Error handling should be consistent across all queue operations

---

## 2. Current State Analysis

### 2.1 Raw YAML Parsing Pattern (Current)

**Location:** Multiple files across the codebase

```python
# Current pattern found in:
# - bb5-queue-manager.py (lines 249-268)
# - task_completion_skill_recorder.py (lines 34-43, 117-127)
# - planner-prioritize.py (lines 77-108)
# - executor-implement.py (lines 59-91)
# - verifier-validate.py (lines 51-65)

# Direct file operations with inline parsing
def load_queue():
    with open("queue.yaml", "r") as f:
        data = yaml.safe_load(f)
    
    tasks = []
    for task_data in data["tasks"]:
        # Inline conversion logic
        converted = {
            "task_id": task_data.get("id"),
            "priority": task_data.get("priority", "medium").lower(),
            # ... more inline parsing
        }
        tasks.append(converted)
    return tasks

def save_queue(tasks):
    with open("queue.yaml", "w") as f:
        yaml.dump({"tasks": tasks}, f)
```

### 2.2 Communication Flow (Current)

```
Scout Agent
  ↓ Writes to: .autonomous/analysis/scout-reports/*.yaml
  
Planner Agent
  ↓ Reads from: scout-reports/*.yaml
  ↓ Writes to: tasks/active/TASK-XXX/task.md
  
Executor Agent
  ↓ Reads from: tasks/active/TASK-XXX/task.md
  ↓ Writes to: operations/*.yaml (direct file modification)
  
Verifier Agent
  ↓ Reads from: operations/*.yaml
  ↓ Writes to: .autonomous/analysis/verifier-reports/*.yaml

Events System
  ↓ All agents append to: .autonomous/agents/communications/events.yaml
```

### 2.3 Files with Raw Queue Operations

| File | Operations | Lines |
|------|------------|-------|
| `bb5-queue-manager.py` | Load, parse, convert, save | 241-335 |
| `task_completion_skill_recorder.py` | Load YAML, append, save | 33-53, 116-127 |
| `planner-prioritize.py` | Load scout report, parse | 77-108 |
| `executor-implement.py` | Load task, parse markdown | 59-91 |
| `verifier-validate.py` | Load report, validate | 51-65 |
| `bb5-reanalysis-engine.py` | Queue operations | TBD |
| `improvement-loop.py` | Subprocess orchestration | 44-181 |

### 2.4 Current Queue Schema

**File:** `.autonomous/agents/communications/queue.yaml`

```yaml
schema:
  version: "1.0.0"
  generated: "2026-02-06"
  total_tasks: 90

tasks:
  - id: "TASK-ARCH-001"
    type: "architecture"
    status: "completed"
    priority: "HIGH"
    priority_score: 8.5
    title: "..."
    estimated_minutes: 45
    roi:
      impact: 8.5
      effort: 45
      confidence: 1.2
    blockedBy: []
    blocks: ["TASK-ARCH-002"]
    resource_type: "memory_bound"
    parallel_group: "wave_1"
    goal: "IG-007"

queue_metadata:
  total_tasks: 90
  by_status:
    completed: 25
    in_progress: 5
    pending: 60
```

### 2.5 Current Events Schema

**File:** `.autonomous/agents/communications/events.yaml`

```yaml
- timestamp: '2026-02-01T16:01:00Z'
  task_id: TASK-1738375000
  type: started
  agent: executor
  run_number: 66
  notes: 'Claimed task: ...'
  
- timestamp: '2026-02-03T23:31:29+07:00'
  type: queue_refilled
  agent: planner
  run_id: 20260203-233129
  data:
    previous_depth: 2
    new_depth: 3
```

---

## 3. Proposed Queue Interface Design

### 3.1 Core Abstraction

```python
# lib/queue/abstract.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class EventType(Enum):
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_BLOCKED = "task_blocked"
    QUEUE_REFILLED = "queue_refilled"
    AGENT_STARTED = "agent_started"
    AGENT_STOPPED = "agent_stopped"

@dataclass
class Task:
    id: str
    title: str
    status: TaskStatus
    priority: str
    priority_score: float
    type: str
    estimated_minutes: int
    blocked_by: List[str]
    blocks: List[str]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

@dataclass
class Event:
    timestamp: datetime
    type: EventType
    agent: str
    task_id: Optional[str]
    data: Dict[str, Any]
    run_id: Optional[str] = None

class QueueInterface(ABC):
    """Abstract interface for queue operations."""
    
    @abstractmethod
    def get_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """Get tasks, optionally filtered by status."""
        pass
    
    @abstractmethod
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        pass
    
    @abstractmethod
    def update_task(self, task: Task) -> bool:
        """Update a task. Returns success."""
        pass
    
    @abstractmethod
    def create_task(self, task: Task) -> bool:
        """Create a new task. Returns success."""
        pass
    
    @abstractmethod
    def get_execution_order(self) -> List[str]:
        """Get task IDs in dependency-resolved execution order."""
        pass
    
    @abstractmethod
    def emit_event(self, event: Event) -> bool:
        """Emit an event to the event stream."""
        pass
    
    @abstractmethod
    def get_events(self, 
                   since: Optional[datetime] = None,
                   agent: Optional[str] = None,
                   event_type: Optional[EventType] = None) -> List[Event]:
        """Get events with optional filtering."""
        pass
    
    @abstractmethod
    def subscribe(self, 
                  callback: Callable[[Event], None],
                  event_types: Optional[List[EventType]] = None):
        """Subscribe to events (for async implementations)."""
        pass
```

### 3.2 FileQueue Implementation

```python
# lib/queue/file_queue.py
import yaml
import fcntl
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable
from datetime import datetime
from .abstract import QueueInterface, Task, Event, TaskStatus, EventType

class FileQueue(QueueInterface):
    """
    File-based queue implementation using YAML files.
    Suitable for single-node deployments.
    """
    
    def __init__(self, 
                 queue_file: Path,
                 events_file: Path,
                 lock_timeout: float = 30.0):
        self.queue_file = queue_file
        self.events_file = events_file
        self.lock_timeout = lock_timeout
        self._subscribers: List[tuple] = []
    
    def _acquire_lock(self, file):
        """Acquire file lock for atomic operations."""
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
    
    def _release_lock(self, file):
        """Release file lock."""
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)
    
    def _load_queue(self) -> Dict[str, Any]:
        """Load queue data with file locking."""
        if not self.queue_file.exists():
            return {"tasks": [], "metadata": {}}
        
        with open(self.queue_file, 'r') as f:
            self._acquire_lock(f)
            try:
                return yaml.safe_load(f) or {"tasks": [], "metadata": {}}
            finally:
                self._release_lock(f)
    
    def _save_queue(self, data: Dict[str, Any]) -> bool:
        """Save queue data with file locking."""
        with open(self.queue_file, 'w') as f:
            self._acquire_lock(f)
            try:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                return True
            finally:
                self._release_lock(f)
    
    def _task_from_dict(self, data: Dict) -> Task:
        """Convert dict to Task object."""
        return Task(
            id=data.get("id") or data.get("task_id"),
            title=data.get("title", "Untitled"),
            status=TaskStatus(data.get("status", "pending")),
            priority=data.get("priority", "medium"),
            priority_score=data.get("priority_score", 0.0),
            type=data.get("type", "general"),
            estimated_minutes=data.get("estimated_minutes", 0),
            blocked_by=data.get("blockedBy", []),
            blocks=data.get("blocks", []),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else None
        )
    
    def _task_to_dict(self, task: Task) -> Dict:
        """Convert Task object to dict."""
        return {
            "id": task.id,
            "title": task.title,
            "status": task.status.value,
            "priority": task.priority,
            "priority_score": task.priority_score,
            "type": task.type,
            "estimated_minutes": task.estimated_minutes,
            "blockedBy": task.blocked_by,
            "blocks": task.blocks,
            "metadata": task.metadata,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        }
    
    def get_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """Get tasks, optionally filtered by status."""
        data = self._load_queue()
        tasks = [self._task_from_dict(t) for t in data.get("tasks", [])]
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        return tasks
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        tasks = self.get_tasks()
        return next((t for t in tasks if t.id == task_id), None)
    
    def update_task(self, task: Task) -> bool:
        """Update a task atomically."""
        data = self._load_queue()
        tasks = data.get("tasks", [])
        
        # Find and update task
        for i, t in enumerate(tasks):
            if (t.get("id") or t.get("task_id")) == task.id:
                task.updated_at = datetime.now()
                tasks[i] = self._task_to_dict(task)
                break
        else:
            return False  # Task not found
        
        data["tasks"] = tasks
        return self._save_queue(data)
    
    def create_task(self, task: Task) -> bool:
        """Create a new task."""
        data = self._load_queue()
        
        if "tasks" not in data:
            data["tasks"] = []
        
        data["tasks"].append(self._task_to_dict(task))
        return self._save_queue(data)
    
    def get_execution_order(self) -> List[str]:
        """Get task IDs in dependency-resolved order."""
        from .dependency_resolver import topological_sort
        
        tasks = self.get_tasks()
        return topological_sort(tasks)
    
    def emit_event(self, event: Event) -> bool:
        """Emit an event to the event stream."""
        events = []
        if self.events_file.exists():
            with open(self.events_file, 'r') as f:
                events = yaml.safe_load(f) or []
        
        events.append({
            "timestamp": event.timestamp.isoformat(),
            "type": event.type.value,
            "agent": event.agent,
            "task_id": event.task_id,
            "data": event.data,
            "run_id": event.run_id
        })
        
        with open(self.events_file, 'w') as f:
            yaml.dump(events, f, default_flow_style=False, sort_keys=False)
        
        # Notify subscribers
        for callback, event_types in self._subscribers:
            if event_types is None or event.type in event_types:
                callback(event)
        
        return True
    
    def get_events(self, 
                   since: Optional[datetime] = None,
                   agent: Optional[str] = None,
                   event_type: Optional[EventType] = None) -> List[Event]:
        """Get events with optional filtering."""
        if not self.events_file.exists():
            return []
        
        with open(self.events_file, 'r') as f:
            events_data = yaml.safe_load(f) or []
        
        events = []
        for e in events_data:
            event = Event(
                timestamp=datetime.fromisoformat(e["timestamp"]),
                type=EventType(e["type"]),
                agent=e["agent"],
                task_id=e.get("task_id"),
                data=e.get("data", {}),
                run_id=e.get("run_id")
            )
            
            # Apply filters
            if since and event.timestamp < since:
                continue
            if agent and event.agent != agent:
                continue
            if event_type and event.type != event_type:
                continue
            
            events.append(event)
        
        return events
    
    def subscribe(self, 
                  callback: Callable[[Event], None],
                  event_types: Optional[List[EventType]] = None):
        """Subscribe to events."""
        self._subscribers.append((callback, event_types))
```

### 3.3 RedisQueue Implementation

```python
# lib/queue/redis_queue.py
import json
import redis
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable
from datetime import datetime
from .abstract import QueueInterface, Task, Event, TaskStatus, EventType

class RedisQueue(QueueInterface):
    """
    Redis-based queue implementation.
    Suitable for multi-node deployments and real-time event streaming.
    """
    
    def __init__(self, 
                 redis_url: str = "redis://localhost:6379",
                 queue_key: str = "bb5:queue",
                 events_channel: str = "bb5:events"):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.queue_key = queue_key
        self.events_channel = events_channel
        self._pubsub = None
        self._subscribers: List[tuple] = []
    
    def _task_to_json(self, task: Task) -> str:
        """Serialize task to JSON."""
        return json.dumps({
            "id": task.id,
            "title": task.title,
            "status": task.status.value,
            "priority": task.priority,
            "priority_score": task.priority_score,
            "type": task.type,
            "estimated_minutes": task.estimated_minutes,
            "blocked_by": task.blocked_by,
            "blocks": task.blocks,
            "metadata": task.metadata,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        })
    
    def _task_from_json(self, data: str) -> Task:
        """Deserialize task from JSON."""
        d = json.loads(data)
        return Task(
            id=d["id"],
            title=d["title"],
            status=TaskStatus(d["status"]),
            priority=d["priority"],
            priority_score=d["priority_score"],
            type=d["type"],
            estimated_minutes=d["estimated_minutes"],
            blocked_by=d.get("blocked_by", []),
            blocks=d.get("blocks", []),
            metadata=d.get("metadata", {}),
            created_at=datetime.fromisoformat(d["created_at"]),
            updated_at=datetime.fromisoformat(d["updated_at"]) if d.get("updated_at") else None
        )
    
    def get_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """Get tasks from Redis hash."""
        tasks_data = self.redis.hgetall(self.queue_key)
        tasks = [self._task_from_json(t) for t in tasks_data.values()]
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        return tasks
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        task_data = self.redis.hget(self.queue_key, task_id)
        if task_data:
            return self._task_from_json(task_data)
        return None
    
    def update_task(self, task: Task) -> bool:
        """Update a task in Redis."""
        task.updated_at = datetime.now()
        return self.redis.hset(self.queue_key, task.id, self._task_to_json(task)) == 1
    
    def create_task(self, task: Task) -> bool:
        """Create a new task in Redis."""
        return self.redis.hset(self.queue_key, task.id, self._task_to_json(task)) == 1
    
    def get_execution_order(self) -> List[str]:
        """Get task IDs in dependency-resolved order."""
        from .dependency_resolver import topological_sort
        tasks = self.get_tasks()
        return topological_sort(tasks)
    
    def emit_event(self, event: Event) -> bool:
        """Publish event to Redis pub/sub."""
        event_data = json.dumps({
            "timestamp": event.timestamp.isoformat(),
            "type": event.type.value,
            "agent": event.agent,
            "task_id": event.task_id,
            "data": event.data,
            "run_id": event.run_id
        })
        
        # Publish to channel
        self.redis.publish(self.events_channel, event_data)
        
        # Also store in sorted set for history
        score = event.timestamp.timestamp()
        self.redis.zadd(f"{self.events_channel}:history", {event_data: score})
        
        return True
    
    def get_events(self, 
                   since: Optional[datetime] = None,
                   agent: Optional[str] = None,
                   event_type: Optional[EventType] = None) -> List[Event]:
        """Get events from Redis sorted set."""
        min_score = since.timestamp() if since else 0
        max_score = datetime.now().timestamp()
        
        events_data = self.redis.zrangebyscore(
            f"{self.events_channel}:history",
            min_score,
            max_score
        )
        
        events = []
        for data in events_data:
            d = json.loads(data)
            event = Event(
                timestamp=datetime.fromisoformat(d["timestamp"]),
                type=EventType(d["type"]),
                agent=d["agent"],
                task_id=d.get("task_id"),
                data=d.get("data", {}),
                run_id=d.get("run_id")
            )
            
            # Apply filters
            if agent and event.agent != agent:
                continue
            if event_type and event.type != event_type:
                continue
            
            events.append(event)
        
        return events
    
    def subscribe(self, 
                  callback: Callable[[Event], None],
                  event_types: Optional[List[EventType]] = None):
        """Subscribe to Redis pub/sub events."""
        if self._pubsub is None:
            self._pubsub = self.redis.pubsub()
            self._pubsub.subscribe(self.events_channel)
        
        self._subscribers.append((callback, event_types))
        
        # Start listener thread if not already running
        # (Implementation would use threading)
```

### 3.4 Queue Factory

```python
# lib/queue/__init__.py
from pathlib import Path
from typing import Optional
from .abstract import QueueInterface
from .file_queue import FileQueue

def create_queue(
    backend: str = "file",
    queue_file: Optional[Path] = None,
    events_file: Optional[Path] = None,
    redis_url: Optional[str] = None
) -> QueueInterface:
    """
    Factory function to create the appropriate queue implementation.
    
    Args:
        backend: "file" or "redis"
        queue_file: Path to queue.yaml (for file backend)
        events_file: Path to events.yaml (for file backend)
        redis_url: Redis connection URL (for redis backend)
    
    Returns:
        QueueInterface implementation
    """
    if backend == "file":
        if queue_file is None:
            queue_file = Path(".autonomous/agents/communications/queue.yaml")
        if events_file is None:
            events_file = Path(".autonomous/agents/communications/events.yaml")
        
        return FileQueue(queue_file, events_file)
    
    elif backend == "redis":
        from .redis_queue import RedisQueue
        return RedisQueue(redis_url=redis_url or "redis://localhost:6379")
    
    else:
        raise ValueError(f"Unknown backend: {backend}")
```

---

## 4. Implementation Steps

### Phase 1: Create Queue Interface (30 min)

1. **Create directory structure:**
   ```
   2-engine/.autonomous/lib/queue/
   ├── __init__.py
   ├── abstract.py
   ├── file_queue.py
   ├── redis_queue.py
   └── dependency_resolver.py
   ```

2. **Implement abstract.py:**
   - Define QueueInterface abstract base class
   - Define Task and Event dataclasses
   - Define enums for TaskStatus and EventType

3. **Implement dependency_resolver.py:**
   - Extract topological sort logic from bb5-queue-manager.py
   - Make it reusable for both implementations

### Phase 2: Implement FileQueue (20 min)

1. **Implement file_queue.py:**
   - File-based queue operations with locking
   - YAML serialization/deserialization
   - Event emission and subscription
   - Atomic updates

2. **Add unit tests:**
   - Test task CRUD operations
   - Test event emission
   - Test concurrent access with locking

### Phase 3: Implement RedisQueue (20 min)

1. **Implement redis_queue.py:**
   - Redis hash for task storage
   - Redis pub/sub for events
   - Sorted set for event history
   - Connection pooling

2. **Add unit tests:**
   - Mock Redis for testing
   - Test pub/sub functionality

### Phase 4: Refactor Existing Code (20 min)

1. **Update bb5-queue-manager.py:**
   - Replace inline parsing with FileQueue
   - Remove duplicate conversion logic
   - Use QueueInterface methods

2. **Update task_completion_skill_recorder.py:**
   - Use QueueInterface for events
   - Remove direct YAML operations

3. **Update improvement-loop.py:**
   - Use QueueInterface for agent coordination
   - Emit events instead of direct file writes

### Phase 5: Add Configuration (10 min)

1. **Create queue configuration:**
   - Add QUEUE_BACKEND env variable
   - Add Redis URL configuration
   - Add file paths configuration

2. **Update documentation:**
   - Document the Queue interface
   - Document migration path
   - Add usage examples

---

## 5. Files to Modify/Create

### New Files

| File | Purpose | Lines |
|------|---------|-------|
| `2-engine/.autonomous/lib/queue/__init__.py` | Package init + factory | ~50 |
| `2-engine/.autonomous/lib/queue/abstract.py` | Abstract interface | ~100 |
| `2-engine/.autonomous/lib/queue/file_queue.py` | File-based implementation | ~250 |
| `2-engine/.autonomous/lib/queue/redis_queue.py` | Redis implementation | ~200 |
| `2-engine/.autonomous/lib/queue/dependency_resolver.py` | Topological sort | ~100 |
| `tests/unit/test_queue_interface.py` | Unit tests | ~200 |

### Modified Files

| File | Changes | Lines |
|------|---------|-------|
| `bb5-queue-manager.py` | Use QueueInterface | -100, +50 |
| `task_completion_skill_recorder.py` | Use QueueInterface | -50, +30 |
| `improvement-loop.py` | Use QueueInterface | -30, +40 |
| `planner-prioritize.py` | Use QueueInterface (optional) | -20, +20 |
| `executor-implement.py` | Use QueueInterface (optional) | -20, +20 |
| `verifier-validate.py` | Use QueueInterface (optional) | -20, +20 |

---

## 6. Success Criteria

### Functional Requirements

- [ ] QueueInterface abstract class is defined and documented
- [ ] FileQueue implementation passes all unit tests
- [ ] RedisQueue implementation passes all unit tests
- [ ] Factory function creates correct implementation based on config
- [ ] bb5-queue-manager.py uses QueueInterface (no raw YAML parsing)
- [ ] task_completion_skill_recorder.py uses QueueInterface for events
- [ ] All existing functionality is preserved (backward compatible)

### Non-Functional Requirements

- [ ] FileQueue uses file locking for concurrent access
- [ ] RedisQueue handles connection failures gracefully
- [ ] Both implementations have < 10ms overhead per operation
- [ ] Unit test coverage > 80%
- [ ] Documentation is complete with examples

### Migration Requirements

- [ ] Existing queue.yaml files continue to work
- [ ] Existing events.yaml files continue to work
- [ ] No breaking changes to agent behavior
- [ ] Can switch between FileQueue and RedisQueue via config

---

## 7. Estimated Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1. Create Interface | 30 min | abstract.py, dependency_resolver.py |
| 2. FileQueue | 20 min | file_queue.py + tests |
| 3. RedisQueue | 20 min | redis_queue.py + tests |
| 4. Refactor Code | 20 min | Updated bb5-queue-manager.py, etc. |
| 5. Configuration | 10 min | Config + docs |
| **Total** | **100 min** | **Complete abstraction layer** |

---

## 8. Rollback Strategy

If issues occur:

1. **Immediate:** Switch back to raw YAML parsing by reverting modified files
2. **Short-term:** Keep both implementations side-by-side with feature flag
3. **Long-term:** Fix issues in Queue implementations without affecting agents

---

## 9. Future Enhancements

1. **SQLiteQueue**: For single-node with SQL querying
2. **HybridQueue**: File for tasks, Redis for events
3. **Caching Layer**: LRU cache for frequently accessed tasks
4. **Metrics Integration**: Automatic metrics collection on queue operations
5. **WebSocket Events**: Real-time event streaming for UI

---

## 10. Design Decisions

### Why Abstract Base Class?

- Enforces consistent interface across all implementations
- Enables static type checking
- Self-documenting through method signatures

### Why FileQueue First?

- Current deployment is single-node
- No infrastructure changes required
- Easier to debug and test

### Why RedisQueue?

- Enables multi-node deployments
- Real-time event streaming
- Better performance for high-frequency operations
- Industry standard for message queues

### Why Factory Pattern?

- Centralized configuration
- Easy to add new backends
- Clean separation of creation logic

---

*Plan created: 2026-02-06*  
*Ready for implementation*
