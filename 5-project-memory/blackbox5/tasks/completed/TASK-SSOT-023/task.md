# TASK-SSOT-023: Create Queue Repository with Locking

**Status:** completed
**Priority:** HIGH
**Created:** 2026-02-06
**Completed:** 2026-02-07
**Parent:** Issue #3 - Missing Storage Abstraction Layer

## Objective
Create QueueRepository that encapsulates queue operations with file locking for concurrency.

## Success Criteria
- [ ] Create `storage/repository/queue_repository.py`
- [ ] Implement Queue class with in-memory operations
- [ ] Implement QueuePersistence layer
- [ ] Add file locking (flock for Unix)
- [ ] Implement atomic claim operations
- [ ] Add dependency resolution (topological sort)
- [ ] Add priority scoring
- [ ] Migrate bb5-queue-manager.py to use QueueRepository

## Context
Current bb5-queue-manager.py:
- Direct YAML manipulation (lines 241-332)
- No Queue abstraction class
- No file locking (race conditions)
- Mixed concerns (file I/O + business logic)

## Required Methods
```python
class Queue:
    def load(filepath: Path) -> Queue
    def save(filepath: Optional[Path] = None) -> None
    def add_task(task: Task) -> None
    def claim_task(task_id: str, claimed_by: str) -> Optional[Task]
    def get_execution_order() -> list[Task]
    def get_next_executable() -> Optional[Task]
    def calculate_priority_scores() -> None
    def detect_cycles() -> Optional[list[str]]
```

## Related Files
- queue-abstraction-requirements.md
- bb5-queue-manager.py
- bb5-parallel-dispatch.sh

## Rollback Strategy
Keep bb5-queue-manager.py until QueueRepository proven stable.
