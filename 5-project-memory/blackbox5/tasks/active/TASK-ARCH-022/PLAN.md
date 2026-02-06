# PLAN.md: State Machine Lacks Persistence Integration

**Task:** TASK-ARCH-022 - State Machine Lacks Persistence Integration  
**Status:** Planning  
**Created:** 2026-02-06  
**Estimated Effort:** 18 hours  
**Importance:** 75/100 (High)

---

## 1. First Principles Analysis

### The Core Problem
Task states exist in multiple places with no unified persistence:
- `queue.yaml` - queue status
- `task.md` - task status in frontmatter
- `events.yaml` - event log
- No automatic persistence on state transitions

This creates:
1. **State loss on crashes** - In-progress status lost
2. **Inconsistency** - Files show different states
3. **Race conditions** - Concurrent modifications
4. **No audit trail** - Cannot reconstruct history

### First Principles Solution
- **TaskStore Interface**: Abstract persistence layer
- **Automatic Persistence**: State transitions trigger saves
- **Transaction Safety**: Atomic operations
- **Event-driven**: Observers notified of changes

---

## 2. Current State Assessment

### TaskStatus Enums (3 incompatible versions)

```python
# bb5-queue-manager.py
class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# bb5-reanalysis-engine.py
class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    INVALID = "invalid"
    OBSOLETE = "obsolete"
```

### State Storage Locations

| Location | Format | Purpose |
|----------|--------|---------|
| queue.yaml | YAML | Queue state |
| task.md | Frontmatter | Canonical task |
| events.yaml | YAML | Event log |

---

## 3. Proposed Solution

### TaskStore Interface

```python
class TaskStore(ABC):
    @abstractmethod
    def load_task(self, task_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def transition_state(
        self,
        task_id: str,
        new_status: TaskStatus
    ) -> StateTransition:
        pass

    @abstractmethod
    def get_transition_history(self, task_id: str) -> List[StateTransition]:
        pass
```

### Persistence Hooks

1. **QueueSyncHook** - Syncs to queue.yaml
2. **TaskFileHook** - Updates task.md
3. **EventLogHook** - Appends to events.yaml
4. **ValidationHook** - Validates transitions

---

## 4. Implementation Plan

### Phase 1: Design TaskStore Interface (2 hours)

1. Define abstract base class
2. Define StateTransition dataclass
3. Define PersistenceHook protocol

### Phase 2: Implement FileSystemTaskStore (4 hours)

1. Implement atomic file operations
2. Implement transaction journal
3. Add file locking
4. Create recovery mechanism

### Phase 3: Add Persistence Hooks (4 hours)

1. QueueSyncHook
2. TaskFileHook
3. EventLogHook
4. ValidationHook

### Phase 4: Create State Transition Events (2 hours)

1. Define event types
2. Implement event bus
3. Add event persistence

### Phase 5: Write Tests (4 hours)

1. Unit tests for TaskStore
2. Integration tests
3. Concurrency tests
4. Recovery tests

### Phase 6: Update Documentation (2 hours)

1. Update storage README
2. Create migration guide
3. Document architecture

---

## 5. Success Criteria

- [ ] TaskStore interface defined
- [ ] FileSystemTaskStore implemented
- [ ] State transitions automatically persist
- [ ] No state loss on crashes
- [ ] Tests pass

---

## 6. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Interface | 2 hours |
| FileSystemTaskStore | 4 hours |
| Hooks | 4 hours |
| Events | 2 hours |
| Tests | 4 hours |
| Documentation | 2 hours |
| **Total** | **18 hours** |

---

*Plan created based on structural issue analysis*
