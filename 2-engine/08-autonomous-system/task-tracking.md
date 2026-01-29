# Task Tracking for Autonomous Agents

> **How to track tasks across multiple autonomous agents so others can view them later**

## Overview

Task tracking is the backbone of any autonomous agent system. Without it, you can't know:
- What agents are working on
- What's been completed
- What's blocked or failing
- How long things take

This document covers production patterns for task tracking in multi-agent autonomous systems.

---

## Core Data Structures

### The Task Object

Based on research from LangGraph, CrewAI, Temporal, and your existing Blackbox5 implementation:

```python
@dataclass
class Task:
    """Production-ready task tracking"""

    # Identity
    id: str                    # Unique identifier
    title: str                 # Human-readable name
    description: str           # Detailed description

    # Classification
    type: str                  # Task type (development, testing, etc.)
    priority: int              # 1-10, higher is more important
    tags: List[str]            # Custom tags

    # State
    state: TaskState           # Current state
    assignee: Optional[str]    # Who's working on it
    created_at: datetime
    assigned_at: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    # Dependencies
    depends_on: List[str]      # Tasks that must complete first
    blocks: List[str]          # Tasks waiting on this one

    # Execution
    retry_count: int = 0
    error_log: List[str] = field(default_factory=list)

    # Checkpointing (for resumable workflows)
    checkpoint_data: dict = field(default_factory=dict)
    checkpoint_timestamp: Optional[datetime] = None

    # Metrics
    cycle_time: Optional[float] = None      # Total time
    wait_time: Optional[float] = None        # Time until started
    work_time: Optional[float] = None        # Actual work time

    # Result
    result: Optional[dict] = None
    artifacts: List[str] = field(default_factory=list)  # Files/commits created

class TaskState(Enum):
    """Task lifecycle states"""
    BACKLOG = "backlog"         # Not yet scheduled
    PENDING = "pending"         # Ready to be claimed
    ASSIGNED = "assigned"       # Claimed by agent
    ACTIVE = "active"          # Agent is working
    PAUSED = "paused"          # Waiting for input
    REVIEW = "review"          # Under review
    APPROVED = "approved"       # Ready to merge
    DONE = "done"              # Complete
    FAILED = "failed"          # Execution failed
    CANCELLED = "cancelled"    # Cancelled
```

---

## State Transitions

### Production State Machine

Based on research from Temporal, LangGraph, and production systems:

```
                    ┌─────────────┐
                    │   BACKLOG   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   PENDING   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  ASSIGNED   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   ACTIVE    │◄─────────────────┐
                    └──────┬──────┘                   │
                           │                          │
                ┌──────────┴───────────┐           │
                │                      │           │
         ┌──────▼──────┐    ┌───────▼─────┐  ┌────▼──────┐
         │   DONE       │    │   FAILED     │  │  PAUSED   │
         │              │    │              │  │           │
         └──────────────┘    └──────────────┘  └─────┬─────┘
                                                  │
                                                  │  (resume)
                                                  └──────┘
```

### Transition Rules

```python
class TaskStateMachine:
    def transition(self, task: Task, new_state: TaskState) -> bool:
        """Safely transition task state"""

        # Validate transition
        valid_transitions = {
            TaskState.BACKLOG: [TaskState.PENDING],
            TaskState.PENDING: [TaskState.ASSIGNED, TaskState.CANCELLED],
            TaskState.ASSIGNED: [TaskState.ACTIVE, TaskState.CANCELLED],
            TaskState.ACTIVE: [TaskState.DONE, TaskState.FAILED, TaskState.PAUSED],
            TaskState.PAUSED: [TaskState.ACTIVE, TaskState.CANCELLED],
            TaskState.FAILED: [TaskState.PENDING],  # Retry
            TaskState.DONE: [],  # Terminal
            TaskState.CANCELLED: []  # Terminal
        }

        if new_state not in valid_transitions.get(task.state, []):
            raise InvalidTransition(f"{task.state} → {new_state}")

        # Apply transition
        old_state = task.state
        task.state = new_state

        # Record transition
        self.record_event(task.id, old_state, new_state)

        return True
```

---

## Multi-Agent Coordination

### Claiming Tasks (Atomic)

```python
def claim_task(task_id: str, agent_id: str) -> bool:
    """Atomically claim a task"""

    # Use Redis for distributed locking
    lock = redis.lock(f"lock:task:{task_id}", timeout=10)

    if lock.acquire(blocking=False):
        try:
            # Double-check state
            task = task_registry.get(task_id)

            if task.state != TaskState.PENDING:
                return False  # Already claimed

            # Transition state
            task.state = TaskState.ASSIGNED
            task.assignee = agent_id
            task.assigned_at = datetime.now()

            # Save
            task_registry.save(task)

            # Notify
            redis.publish("tasks:claimed", {
                "task_id": task_id,
                "agent": agent_id
            })

            return True

        finally:
            lock.release()

    return False
```

### Dependency Resolution

```python
def get_available_tasks(agent_id: str) -> List[Task]:
    """Get tasks this agent can work on now"""

    available = []
    tasks = task_registry.get_all()

    for task in tasks:
        # Skip if not in pending state
        if task.state != TaskState.PENDING:
            continue

        # Check dependencies
        deps_satisfied = True
        for dep_id in task.depends_on:
            dep = task_registry.get(dep_id)

            if dep.state != TaskState.DONE:
                deps_satisfied = False
                break

        if deps_satisfied:
            available.append(task)

    # Sort by priority
    available.sort(key=lambda t: t.priority, reverse=True)

    return available
```

### Conflict Prevention

**Optimistic Locking Pattern**:

```python
@dataclass
class Task:
    version: int = 1  # Increment on each update

def update_task(task: Task, **kwargs):
    """Update with version check"""

    # Get current version
    current = task_registry.get(task.id)

    # Check version
    if task.version != current.version:
        raise ConflictError("Task was modified by another agent")

    # Apply updates
    for key, value in kwargs.items():
        setattr(task, key, value)

    # Increment version
    task.version += 1

    # Save
    task_registry.save(task)
```

---

## Persistence Strategies

### Decision Matrix

| Approach | Best For | Pros | Cons |
|----------|----------|------|------|
| **JSON Files** | Development, <1K tasks | Simple, git-tracked | No ACID, slow at scale |
| **SQLite** | Embedded, single-server | ACID, zero-config | Limited concurrency |
| **PostgreSQL** | Production, multi-server | Reliable, concurrent | Operational overhead |
| **Redis** | High-concurrency queues | Fast, pub/sub | Not durable w/o config |

### Hybrid Approach (Recommended)

```python
class HybridTaskStore:
    """Combines best of all worlds"""

    def __init__(self):
        # Hot cache (fast lookups)
        self.redis = redis.Redis()

        # Durable storage (source of truth)
        self.postgres = psycopg2.connect("...")

        # Backup/debugging (git-tracked)
        self.json_file = "tasks/tasks.json"

    def get_task(self, task_id: str) -> Task:
        # Check cache first
        cached = self.redis.get(f"task:{task_id}")
        if cached:
            return json.loads(cached)

        # Check DB
        with self.postgres.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            row = cur.fetchone()
            if row:
                task = Task.from_row(row)
                # Cache it
                self.redis.set(f"task:{task_id}", task.to_json())
                return task

        # Fallback to JSON
        return self._load_from_json(task_id)

    def save_task(self, task: Task):
        # Write to DB (source of truth)
        with self.postgres.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks VALUES (%s)",
                (task.to_db_row(),)
            )
            self.postgres.commit()

        # Update cache
        self.redis.set(f"task:{task_id}", task.to_json())

        # Update JSON (git-tracked)
        self._append_to_json(task)
```

---

## Observability

### Event Sourcing Pattern

```python
class TaskEventLogger:
    """Log all task events for replay"""

    def log(self, task_id: str, event_type: str, data: dict):
        """Log task event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "event_type": event_type,
            "data": data
        }

        # Write to event log
        with open(f"task_events/{task_id}.jsonl", "a") as f:
            f.write(json.dumps(event) + "\n")

        # Also publish for real-time
        redis.publish(f"events:task:{task_id}", event)

# Usage
logger.log("task-123", "created", {...})
logger.log("task-123", "assigned", {"agent": "agent-1"})
logger.log("task-123", "started", {"at": "..."})
logger.log("task-123", "completed", {"result": "..."})
```

### Replay for Debugging

```python
def replay_task(task_id: str, from_event: int = None):
    """Rebuild task state from event history"""

    events = []
    with open(f"task_events/{task_id}.jsonl") as f:
        for line in f:
            events.append(json.loads(line))

    # Rebuild state
    task = Task()
    for event in events[from_event:]:
        task = apply_event(task, event)

    return task
```

### Metrics Collection

```python
@dataclass
class TaskMetrics:
    """Metrics for task analysis"""

    # Execution
    duration: float
    token_usage: int
    api_calls: int

    # Quality
    success_rate: float
    error_count: int
    retry_count: int

    # Agent performance
    agent_id: str
    agent_performance: dict

    # Calculate metrics
    def calculate(self):
        """Calculate derived metrics"""
        self.cycle_time = self.completed_at - self.created_at
        self.wait_time = self.started_at - self.created_at
        self.work_time = self.completed_at - self.started_at
        self.success_rate = 1.0 if self.state == TaskState.DONE else 0.0
```

---

## Task Registry Implementation

Based on your existing Blackbox5 implementation:

```python
class TaskRegistry:
    """Central task registry with persistence"""

    def __init__(self, backend="json"):
        if backend == "json":
            self.store = JSONTaskStore()
        elif backend == "sqlite":
            self.store = SQLiteTaskStore()
        elif backend == "postgres":
            self.store = PostgresTaskStore()
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def create(self, task: Task) -> Task:
        """Create new task"""
        task.id = f"task-{uuid.uuid4()}"
        task.state = TaskState.BACKLOG
        task.created_at = datetime.now()

        self.store.save(task)

        # Log event
        self.event_logger.log(task.id, "created", task.to_dict())

        return task

    def assign(self, task_id: str, agent_id: str) -> Task:
        """Assign task to agent"""
        task = self.get(task_id)

        if task.state != TaskState.PENDING:
            raise InvalidTransition(f"Task is {task.state}")

        task.state = TaskState.ASSIGNED
        task.assignee = agent_id
        task.assigned_at = datetime.now()

        self.store.save(task)
        self.event_logger.log(task.id, "assigned", {
            "agent": agent_id
        })

        return task

    def get_available(self, agent_id: str, capabilities: List[str]) -> List[Task]:
        """Get tasks available to this agent"""
        available = []

        for task in self.store.get_all():
            # Check state
            if task.state != TaskState.PENDING:
                continue

            # Check capabilities
            if task.type not in capabilities:
                continue

            # Check dependencies
            if not self._deps_satisfied(task):
                continue

            available.append(task)

        # Sort by priority
        available.sort(key=lambda t: t.priority, reverse=True)

        return available

    def _deps_satisfied(self, task: Task) -> bool:
        """Check if task dependencies are satisfied"""
        for dep_id in task.depends_on:
            dep = self.get(dep_id)
            if dep.state != TaskState.DONE:
                return False
        return True
```

---

## Anti-Patterns to Avoid

### ❌ Multiple Task Registries

```python
# BAD - Tasks in multiple places
tasks_json = load_tasks("tasks.json")
tasks_db = db.query("SELECT * FROM tasks")
tasks_redis = redis.hgetall("tasks")

# Conflicts, inconsistencies, bugs!
```

### ❌ Missing Idempotency

```python
# BAD - Can run multiple times
def start_task(task_id):
    task.state = "ACTIVE"  # Always sets to ACTIVE

# GOOD - Idempotent
def start_task(task_id):
    task = registry.get(task_id)
    if task.state != TaskState.PENDING:
        raise InvalidTransition("Not in PENDING state")
    task.state = "ACTIVE"
```

### ❌ No Version Control

```python
# BAD - No schema version
task = {"id": 1, "status": "doing"}

# GOOD - Versioned schema
@dataclass
class Task:
    schema_version: str = "2.0"  # Can evolve
    id: str
    state: TaskState
```

### ❌ Siloed Agent State

```python
# BAD - State hidden in agent
class Agent:
    def work(self):
        self.my_tasks = {}  # Not shared!

# GOOD - Central registry
registry = TaskRegistry()
task = registry.get(task_id)
```

---

## Production Checklist

Based on research from LinkedIn, Uber, Replit, Elastic:

### ✅ Required for Production

- [ ] **Idempotent Operations**: All state transitions safe to retry
- [ ] **Atomic Updates**: No partial state updates
- [ ] **Event Logging**: Every state change logged
- [ ] **Error Recovery**: Can recover from crashes
- [ ] **Metrics Collection**: Track success rates, latency
- [ ] **Observability**: Debug by replaying execution
- [ ] **Schema Versioning**: Can evolve task structure
- [ ] **Backup/Restore**: Can recover from data loss
- [ ] **Monitoring**: Alerts on failures, anomalies
- [ ] **Testing**: Unit + integration tests

### ✅ Recommended for Scale

- [ ] **Distributed Locking**: Multi-agent coordination
- [ ] **Caching Layer**: Fast task lookup
- [ ] **Message Queue**: Agent communication
- [ ] **Circuit Breakers**: Prevent cascading failures
- [ ] **Rate Limiting**: Protect resources
- [ ] **Dead Letter Queues**: Handle failed tasks
- [ ] **Tracing**: Distributed tracing (OpenTelemetry)

---

## Implementation Examples

See `implementation/schemas/` for:
- Complete Task dataclass
- TaskState enum
- TaskRegistry class
- Event logger

See `examples/` for:
- Complete autonomous agent loop
- Task claiming and execution
- Multi-agent coordination

---

## Summary

**Key Principles:**
1. **Single Source of Truth**: One task registry
2. **Event Sourcing**: Log everything, replay for debugging
3. **Atomic Operations**: Prevent conflicts with locking
4. **Optimistic Locking**: Version checks for concurrent updates
5. **Hybrid Storage**: JSON for dev, SQLite/PostgreSQL for prod, Redis for cache
6. **Observable**: Log, trace, and replay all execution

**Your Current Blackbox5 Implementation**: Already follows many best practices. The enhancements above will make it production-ready.

---

## Sources

- [Temporal: Durable Execution for Distributed Systems](https://temporal.io/)
- [LangGraph State Management](https://docs.langchain.com/langgraph/)
- [CrewAI Task Management](https://docs.crewai.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Redis Task Queues](https://redis.io/docs/manual/patterns/distributed-locks.html)

---

**Document Version**: 1.0
**Last Updated**: 2026-01-28
