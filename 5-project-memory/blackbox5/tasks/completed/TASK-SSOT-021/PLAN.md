# PLAN.md: Create StorageBackend Abstraction Layer

**Task:** TASK-SSOT-021 - StorageBackend abstraction needed
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 6-8 hours
**Importance:** 80 (High)

---

## 1. First Principles Analysis

### The Core Problem
Storage operations are scattered throughout the codebase with direct file system calls:
- Direct YAML file reads/writes
- No abstraction layer for storage operations
- No transaction support
- No caching layer
- Race conditions possible

This creates:
1. **Code Duplication**: Same file operations repeated
2. **Inconsistency**: Different error handling
3. **Race Conditions**: No locking mechanisms
4. **Testing Difficulty**: Hard to mock file system
5. **Migration Complexity**: Hard to change storage backend

### First Principles Solution
- **Abstraction Layer**: StorageBackend interface
- **Unified API**: Consistent storage operations
- **Transaction Support**: Atomic operations
- **Caching**: Performance optimization
- **Testability**: Easy to mock

---

## 2. Current State Analysis

### Current Storage Patterns

```python
# Pattern 1: Direct file read
with open('file.yaml') as f:
    data = yaml.safe_load(f)

# Pattern 2: Direct file write
with open('file.yaml', 'w') as f:
    yaml.dump(data, f)

# Pattern 3: No error handling
data = yaml.safe_load(open('file.yaml'))
```

### Issues

1. **No Abstraction**: Direct file system access everywhere
2. **Inconsistent Error Handling**: Some places catch, others don't
3. **No Transactions**: Partial writes possible
4. **No Caching**: Repeated reads of same files

---

## 3. Proposed Solution

### StorageBackend Interface

**File:** `2-engine/.autonomous/lib/storage_backend.py`

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from contextlib import contextmanager

class StorageBackend(ABC):
    """Abstract base class for storage operations."""

    @abstractmethod
    def read(self, path: str) -> Any:
        """Read data from storage."""
        pass

    @abstractmethod
    def write(self, path: str, data: Any) -> None:
        """Write data to storage."""
        pass

    @abstractmethod
    def exists(self, path: str) -> bool:
        """Check if path exists."""
        pass

    @abstractmethod
    def delete(self, path: str) -> None:
        """Delete from storage."""
        pass

    @abstractmethod
    def list(self, path: str) -> List[str]:
        """List contents of path."""
        pass

    @abstractmethod
    @contextmanager
    def transaction(self):
        """Transaction context manager."""
        pass

class FileSystemBackend(StorageBackend):
    """File system implementation of StorageBackend."""

    def __init__(self, base_path: str, cache_enabled: bool = True):
        self.base_path = Path(base_path)
        self.cache = {} if cache_enabled else None
        self._lock = threading.RLock()

    def read(self, path: str) -> Any:
        """Read with caching."""
        full_path = self.base_path / path

        # Check cache
        if self.cache is not None:
            cache_key = str(full_path)
            if cache_key in self.cache:
                return self.cache[cache_key]

        # Read from disk
        with self._lock:
            with open(full_path) as f:
                data = yaml.safe_load(f)

            # Update cache
            if self.cache is not None:
                self.cache[cache_key] = data

            return data

    def write(self, path: str, data: Any) -> None:
        """Write with atomicity."""
        full_path = self.base_path / path
        temp_path = full_path.with_suffix('.tmp')

        with self._lock:
            # Write to temp file
            with open(temp_path, 'w') as f:
                yaml.dump(data, f)

            # Atomic rename
            temp_path.replace(full_path)

            # Update cache
            if self.cache is not None:
                self.cache[str(full_path)] = data

    def exists(self, path: str) -> bool:
        return (self.base_path / path).exists()

    def delete(self, path: str) -> None:
        full_path = self.base_path / path
        with self._lock:
            full_path.unlink()
            if self.cache is not None:
                self.cache.pop(str(full_path), None)

    def list(self, path: str) -> List[str]:
        full_path = self.base_path / path
        return [str(p.relative_to(self.base_path)) for p in full_path.iterdir()]

    @contextmanager
    def transaction(self):
        """Simple transaction support."""
        transaction_data = {}
        try:
            yield transaction_data
            # Commit: apply all changes
            for path, data in transaction_data.items():
                self.write(path, data)
        except Exception as e:
            # Rollback: discard changes
            raise TransactionError(f"Transaction failed: {e}")
```

### Implementation Plan

#### Phase 1: Design Interface (1 hour)

Define:
- Core methods (read, write, exists, delete, list)
- Transaction support
- Caching strategy
- Error handling

#### Phase 2: Implement FileSystemBackend (2 hours)

1. Implement all abstract methods
2. Add caching layer
3. Add file locking
4. Add atomic writes

#### Phase 3: Create Repository Classes (2 hours)

**File:** `2-engine/.autonomous/lib/repositories.py`

```python
class TaskRepository:
    """Repository for task operations."""

    def __init__(self, storage: StorageBackend):
        self.storage = storage

    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get task by ID."""
        path = f"tasks/active/{task_id}/task.md"
        if not self.storage.exists(path):
            return None
        return self.storage.read(path)

    def save_task(self, task_id: str, data: Dict) -> None:
        """Save task."""
        path = f"tasks/active/{task_id}/task.md"
        self.storage.write(path, data)

    def list_tasks(self) -> List[str]:
        """List all task IDs."""
        return self.storage.list("tasks/active")
```

#### Phase 4: Migrate Existing Code (2 hours)

Replace direct file operations:

```python
# Before
with open(f"tasks/active/{task_id}/task.md") as f:
    task = yaml.safe_load(f)

# After
storage = FileSystemBackend(project_path)
repo = TaskRepository(storage)
task = repo.get_task(task_id)
```

#### Phase 5: Add Tests (1 hour)

Create unit tests for:
- StorageBackend implementations
- Repository classes
- Transaction support

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/lib/storage_backend.py` - Abstract interface
2. `2-engine/.autonomous/lib/storage_backends/` - Implementations
3. `2-engine/.autonomous/lib/repositories.py` - Repository classes
4. `2-engine/.autonomous/lib/test_storage.py` - Unit tests

### Modified Files
1. All scripts with direct file operations (gradual migration)

---

## 5. Success Criteria

- [ ] StorageBackend interface defined
- [ ] FileSystemBackend implemented
- [ ] Repository classes created
- [ ] Caching working
- [ ] Transactions working
- [ ] Unit tests passing
- [ ] At least one script migrated as proof of concept

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Keep old file operations alongside new
2. **Fix**: Debug storage backend
3. **Gradual Migration**: Migrate scripts one at a time

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Interface | 1 hour | 1 hour |
| Phase 2: FileSystemBackend | 2 hours | 3 hours |
| Phase 3: Repositories | 2 hours | 5 hours |
| Phase 4: Migration | 2 hours | 7 hours |
| Phase 5: Tests | 1 hour | 8 hours |
| **Total** | | **6-8 hours** |

---

*Plan created based on SSOT violation analysis - No storage abstraction*
