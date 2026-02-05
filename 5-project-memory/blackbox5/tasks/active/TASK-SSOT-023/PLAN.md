# PLAN.md: Create Queue Repository with File Locking

**Task:** TASK-SSOT-023 - Queue operations need repository abstraction with locking
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 4-5 hours
**Importance:** 75 (High)

---

## 1. First Principles Analysis

### The Core Problem
Queue operations have several issues:
- No abstraction layer for queue operations
- Race conditions possible with concurrent access
- No transaction support
- Inconsistent error handling
- Queue state can become corrupted

This creates:
1. **Race Conditions**: Concurrent updates can lose data
2. **Corruption**: Queue file can become inconsistent
3. **No Recovery**: Hard to recover from errors
4. **Testing Difficulty**: Hard to test queue operations
5. **Maintenance Burden**: Queue logic scattered

### First Principles Solution
- **Repository Pattern**: Centralized queue operations
- **File Locking**: Prevent race conditions
- **Transaction Support**: Atomic operations
- **Queue Model**: Well-defined queue entity
- **Recovery**: Handle errors gracefully

---

## 2. Current State Analysis

### Current Queue Operations

```python
# Pattern 1: Read queue
with open('queue.yaml') as f:
    queue = yaml.safe_load(f)

# Pattern 2: Add item
queue['queue'].append(new_item)

# Pattern 3: Write queue
with open('queue.yaml', 'w') as f:
    yaml.dump(queue, f)
```

### Issues

1. **No Locking**: Race conditions possible
2. **No Validation**: Can add invalid items
3. **No Atomicity**: Partial writes possible
4. **No Recovery**: Errors leave queue in bad state

---

## 3. Proposed Solution

### Queue Domain Model

**File:** `2-engine/.autonomous/lib/queue_model.py`

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
import uuid

class QueueItemStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class QueueItem:
    """Queue item domain model."""
    id: str
    type: str
    payload: Dict
    status: QueueItemStatus
    created_at: datetime
    priority: int = 0
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    error_message: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

    @classmethod
    def create(cls, item_type: str, payload: Dict, priority: int = 0) -> 'QueueItem':
        """Create a new queue item."""
        return cls(
            id=str(uuid.uuid4())[:8],
            type=item_type,
            payload=payload,
            status=QueueItemStatus.PENDING,
            created_at=datetime.now(),
            priority=priority
        )

    def start(self) -> None:
        """Mark item as processing."""
        self.status = QueueItemStatus.PROCESSING
        self.started_at = datetime.now()

    def complete(self) -> None:
        """Mark item as completed."""
        self.status = QueueItemStatus.COMPLETED
        self.completed_at = datetime.now()

    def fail(self, error: str) -> None:
        """Mark item as failed."""
        self.status = QueueItemStatus.FAILED
        self.error_message = error
        self.retry_count += 1

        if self.retry_count < self.max_retries:
            self.status = QueueItemStatus.PENDING
            self.scheduled_at = datetime.now()  # Could add delay here

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'type': self.type,
            'payload': self.payload,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'priority': self.priority,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'error_message': self.error_message,
            'metadata': self.metadata
        }

@dataclass
class Queue:
    """Queue domain model."""
    name: str
    items: List[QueueItem] = field(default_factory=list)
    max_size: Optional[int] = None
    default_max_retries: int = 3

    def enqueue(self, item: QueueItem) -> None:
        """Add item to queue."""
        if self.max_size and len(self.items) >= self.max_size:
            raise QueueFullError(f"Queue {self.name} is full")
        self.items.append(item)
        # Sort by priority
        self.items.sort(key=lambda x: x.priority, reverse=True)

    def dequeue(self) -> Optional[QueueItem]:
        """Get next item from queue."""
        pending = [i for i in self.items if i.status == QueueItemStatus.PENDING]
        if not pending:
            return None
        return pending[0]

    def peek(self) -> Optional[QueueItem]:
        """Peek at next item without removing."""
        return self.dequeue()

    def get_item(self, item_id: str) -> Optional[QueueItem]:
        """Get item by ID."""
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def remove_item(self, item_id: str) -> bool:
        """Remove item by ID."""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                self.items.pop(i)
                return True
        return False

    def get_stats(self) -> Dict:
        """Get queue statistics."""
        return {
            'total': len(self.items),
            'pending': len([i for i in self.items if i.status == QueueItemStatus.PENDING]),
            'processing': len([i for i in self.items if i.status == QueueItemStatus.PROCESSING]),
            'completed': len([i for i in self.items if i.status == QueueItemStatus.COMPLETED]),
            'failed': len([i for i in self.items if i.status == QueueItemStatus.FAILED])
        }
```

### Queue Repository with Locking

**File:** `2-engine/.autonomous/lib/queue_repository.py`

```python
import fcntl
import threading
from typing import Optional
from .storage_backend import StorageBackend
from .queue_model import Queue, QueueItem

class QueueRepository:
    """Repository for queue operations with file locking."""

    def __init__(self, storage: StorageBackend, queue_path: str):
        self.storage = storage
        self.queue_path = queue_path
        self._local_lock = threading.RLock()

    def _acquire_lock(self, file_obj, exclusive: bool = True):
        """Acquire file lock."""
        if exclusive:
            fcntl.flock(file_obj.fileno(), fcntl.LOCK_EX)
        else:
            fcntl.flock(file_obj.fileno(), fcntl.LOCK_SH)

    def _release_lock(self, file_obj):
        """Release file lock."""
        fcntl.flock(file_obj.fileno(), fcntl.LOCK_UN)

    def get_queue(self) -> Queue:
        """Get queue with shared lock."""
        with self._local_lock:
            with open(self.queue_path, 'r') as f:
                self._acquire_lock(f, exclusive=False)
                try:
                    data = self.storage.read(self.queue_path)
                    return self._deserialize_queue(data)
                finally:
                    self._release_lock(f)

    def save_queue(self, queue: Queue) -> None:
        """Save queue with exclusive lock."""
        with self._local_lock:
            with open(self.queue_path, 'r+') as f:
                self._acquire_lock(f, exclusive=True)
                try:
                    data = self._serialize_queue(queue)
                    f.seek(0)
                    f.truncate()
                    yaml.dump(data, f)
                finally:
                    self._release_lock(f)

    def enqueue(self, item: QueueItem) -> None:
        """Add item to queue atomically."""
        with self._local_lock:
            with open(self.queue_path, 'r+') as f:
                self._acquire_lock(f, exclusive=True)
                try:
                    # Read current state
                    data = yaml.safe_load(f)
                    queue = self._deserialize_queue(data)

                    # Modify
                    queue.enqueue(item)

                    # Write back
                    f.seek(0)
                    f.truncate()
                    yaml.dump(self._serialize_queue(queue), f)
                finally:
                    self._release_lock(f)

    def dequeue(self) -> Optional[QueueItem]:
        """Get and mark item as processing atomically."""
        with self._local_lock:
            with open(self.queue_path, 'r+') as f:
                self._acquire_lock(f, exclusive=True)
                try:
                    # Read current state
                    data = yaml.safe_load(f)
                    queue = self._deserialize_queue(data)

                    # Get next item
                    item = queue.dequeue()
                    if item:
                        item.start()

                        # Write back
                        f.seek(0)
                        f.truncate()
                        yaml.dump(self._serialize_queue(queue), f)

                    return item
                finally:
                    self._release_lock(f)

    def update_item(self, item_id: str, update_fn) -> Optional[QueueItem]:
        """Update item atomically."""
        with self._local_lock:
            with open(self.queue_path, 'r+') as f:
                self._acquire_lock(f, exclusive=True)
                try:
                    data = yaml.safe_load(f)
                    queue = self._deserialize_queue(data)

                    item = queue.get_item(item_id)
                    if item:
                        update_fn(item)

                        f.seek(0)
                        f.truncate()
                        yaml.dump(self._serialize_queue(queue), f)

                    return item
                finally:
                    self._release_lock(f)

    def _deserialize_queue(self, data: dict) -> Queue:
        """Deserialize queue from dictionary."""
        items = [QueueItem(**item_data) for item_data in data.get('items', [])]
        return Queue(
            name=data['name'],
            items=items,
            max_size=data.get('max_size'),
            default_max_retries=data.get('default_max_retries', 3)
        )

    def _serialize_queue(self, queue: Queue) -> dict:
        """Serialize queue to dictionary."""
        return {
            'name': queue.name,
            'items': [item.to_dict() for item in queue.items],
            'max_size': queue.max_size,
            'default_max_retries': queue.default_max_retries
        }
```

### Implementation Plan

#### Phase 1: Create Queue Model (1 hour)

1. Define QueueItem dataclass
2. Define Queue dataclass
3. Add status enums
4. Add business logic methods

#### Phase 2: Create Repository with Locking (2 hours)

1. Implement file locking
2. Implement atomic operations
3. Add error handling
4. Add recovery mechanisms

#### Phase 3: Create Queue Service (1 hour)

```python
class QueueService:
    """High-level queue operations."""

    def __init__(self, repository: QueueRepository):
        self.repository = repository

    def submit_task(self, task_id: str, priority: int = 0) -> QueueItem:
        """Submit task to queue."""
        item = QueueItem.create(
            item_type='task',
            payload={'task_id': task_id},
            priority=priority
        )
        self.repository.enqueue(item)
        return item

    def get_next_task(self) -> Optional[QueueItem]:
        """Get next task to process."""
        return self.repository.dequeue()

    def complete_task(self, item_id: str) -> None:
        """Mark task as completed."""
        def complete(item):
            item.complete()
        self.repository.update_item(item_id, complete)
```

#### Phase 4: Add Tests (1 hour)

Create tests for:
- Concurrent access
- Atomic operations
- Error recovery

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/lib/queue_model.py` - Queue domain model
2. `2-engine/.autonomous/lib/queue_repository.py` - Queue repository
3. `2-engine/.autonomous/lib/queue_service.py` - Queue service
4. `2-engine/.autonomous/lib/test_queue.py` - Unit tests

---

## 5. Success Criteria

- [ ] Queue model created
- [ ] Repository with file locking implemented
- [ ] Atomic operations working
- [ ] Queue service created
- [ ] Concurrent access tested
- [ ] Error recovery working

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Keep old queue operations
2. **Fix**: Debug repository
3. **Gradual Migration**: Switch one operation at a time

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Queue Model | 1 hour | 1 hour |
| Phase 2: Repository | 2 hours | 3 hours |
| Phase 3: Service | 1 hour | 4 hours |
| Phase 4: Tests | 1 hour | 5 hours |
| **Total** | | **4-5 hours** |

---

*Plan created based on SSOT violation analysis - Queue operations need abstraction*
