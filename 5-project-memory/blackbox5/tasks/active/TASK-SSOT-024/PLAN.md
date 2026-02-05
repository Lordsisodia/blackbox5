# PLAN.md: Implement File Locking for Concurrent Access

**Task:** TASK-SSOT-024 - Race conditions possible in file operations
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 80 (High)

---

## 1. First Principles Analysis

### The Core Problem
File operations throughout the codebase lack proper locking:
- Multiple agents can read/write same files simultaneously
- Race conditions can corrupt data
- No atomic operations
- Partial writes possible
- Read-modify-write cycles not protected

This creates:
1. **Data Corruption**: Concurrent writes can interleave
2. **Lost Updates**: One update overwrites another
3. **Inconsistent State**: Files in partially written state
4. **Race Conditions**: Timing-dependent bugs
5. **No Concurrency Control**: System doesn't scale

### First Principles Solution
- **File Locking**: Exclusive and shared locks
- **Atomic Operations**: All-or-nothing writes
- **Lock Hierarchy**: Prevent deadlocks
- **Timeout Handling**: Don't block forever
- **Recovery**: Handle lock failures gracefully

---

## 2. Current State Analysis

### Current File Operations

```python
# Pattern 1: Read
with open('file.yaml') as f:
    data = yaml.safe_load(f)

# Pattern 2: Modify
data['field'] = new_value

# Pattern 3: Write
with open('file.yaml', 'w') as f:
    yaml.dump(data, f)
```

### Race Condition Scenario

```
Time  Agent A              Agent B
----  -------              -------
T1    Read file.yaml  ->   Read file.yaml
      (data = v1)          (data = v1)

T2    Modify data          Modify data
      (data = v2)          (data = v3)

T3    Write file.yaml
      (file = v2)

T4                           Write file.yaml
                             (file = v3, v2 LOST!)
```

---

## 3. Proposed Solution

### File Locking Utilities

**File:** `2-engine/.autonomous/lib/file_locking.py`

```python
import fcntl
import os
import time
from contextlib import contextmanager
from typing import Optional

class LockError(Exception):
    """Lock acquisition failed."""
    pass

class FileLock:
    """File-based locking utility."""

    def __init__(self, lock_file: str, timeout: float = 30.0):
        self.lock_file = lock_file
        self.timeout = timeout
        self._lock_fd = None

    @contextmanager
    def acquire_exclusive(self):
        """Acquire exclusive lock."""
        start_time = time.time()

        while True:
            try:
                self._lock_fd = open(self.lock_file, 'w')
                fcntl.flock(self._lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                yield
                break
            except (IOError, OSError):
                if self._lock_fd:
                    self._lock_fd.close()
                    self._lock_fd = None

                if time.time() - start_time > self.timeout:
                    raise LockError(f"Could not acquire exclusive lock on {self.lock_file}")

                time.sleep(0.1)

        self._release()

    @contextmanager
    def acquire_shared(self):
        """Acquire shared lock."""
        start_time = time.time()

        while True:
            try:
                self._lock_fd = open(self.lock_file, 'w')
                fcntl.flock(self._lock_fd.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
                yield
                break
            except (IOError, OSError):
                if self._lock_fd:
                    self._lock_fd.close()
                    self._lock_fd = None

                if time.time() - start_time > self.timeout:
                    raise LockError(f"Could not acquire shared lock on {self.lock_file}")

                time.sleep(0.1)

        self._release()

    def _release(self):
        """Release lock."""
        if self._lock_fd:
            try:
                fcntl.flock(self._lock_fd.fileno(), fcntl.LOCK_UN)
            finally:
                self._lock_fd.close()
                self._lock_fd = None


class AtomicFileWriter:
    """Atomic file writer using temp file and rename."""

    def __init__(self, file_path: str, lock_file: Optional[str] = None):
        self.file_path = file_path
        self.lock_file = lock_file or f"{file_path}.lock"
        self._temp_path = f"{file_path}.tmp.{os.getpid()}"
        self._lock = FileLock(self.lock_file)

    @contextmanager
    def write(self):
        """Context manager for atomic write."""
        with self._lock.acquire_exclusive():
            # Open temp file
            temp_fd = open(self._temp_path, 'w')
            try:
                yield temp_fd
            finally:
                temp_fd.close()

            # Atomic rename
            os.replace(self._temp_path, self.file_path)


class SafeFileReader:
    """Safe file reader with shared locking."""

    def __init__(self, file_path: str, lock_file: Optional[str] = None):
        self.file_path = file_path
        self.lock_file = lock_file or f"{file_path}.lock"
        self._lock = FileLock(self.lock_file)

    def read(self):
        """Read file with shared lock."""
        with self._lock.acquire_shared():
            with open(self.file_path, 'r') as f:
                return f.read()

    def read_yaml(self):
        """Read and parse YAML with shared lock."""
        import yaml
        content = self.read()
        return yaml.safe_load(content)


class ReadModifyWrite:
    """Thread-safe read-modify-write operation."""

    def __init__(self, file_path: str, lock_file: Optional[str] = None):
        self.file_path = file_path
        self.lock_file = lock_file or f"{file_path}.lock"
        self._lock = FileLock(self.lock_file)

    def execute(self, modify_fn, deserializer=None, serializer=None):
        """Execute read-modify-write atomically."""
        deserializer = deserializer or self._default_deserializer
        serializer = serializer or self._default_serializer

        with self._lock.acquire_exclusive():
            # Read
            with open(self.file_path, 'r') as f:
                data = deserializer(f)

            # Modify
            data = modify_fn(data)

            # Write
            temp_path = f"{self.file_path}.tmp.{os.getpid()}"
            with open(temp_path, 'w') as f:
                serializer(data, f)

            os.replace(temp_path, self.file_path)

            return data

    def _default_deserializer(self, f):
        import yaml
        return yaml.safe_load(f)

    def _default_serializer(self, data, f):
        import yaml
        yaml.dump(data, f, default_flow_style=False)
```

### Implementation Plan

#### Phase 1: Create Locking Utilities (2 hours)

1. Implement FileLock class
2. Implement AtomicFileWriter
3. Implement SafeFileReader
4. Implement ReadModifyWrite

#### Phase 2: Add Locking to Storage Backend (1 hour)

Update StorageBackend to use locking:

```python
class FileSystemBackend(StorageBackend):
    def write(self, path: str, data: Any) -> None:
        full_path = self.base_path / path
        lock_file = f"{full_path}.lock"

        writer = AtomicFileWriter(str(full_path), lock_file)
        with writer.write() as f:
            yaml.dump(data, f)
```

#### Phase 3: Add Locking to Critical Sections (1 hour)

Identify and update critical file operations:
- Queue updates
- Task status changes
- State updates
- Event publishing

#### Phase 4: Add Tests (30 min)

Create tests for:
- Concurrent writes
- Lock timeout
- Atomic operations

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/lib/file_locking.py` - Locking utilities
2. `2-engine/.autonomous/lib/test_file_locking.py` - Unit tests

### Modified Files
1. `2-engine/.autonomous/lib/storage_backend.py` - Add locking
2. Critical file operations throughout codebase

---

## 5. Success Criteria

- [ ] FileLock class implemented
- [ ] AtomicFileWriter working
- [ ] SafeFileReader working
- [ ] ReadModifyWrite working
- [ ] StorageBackend uses locking
- [ ] Concurrent access tests passing
- [ ] No race conditions in critical sections

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Disable locking (set timeout to 0)
2. **Fix**: Debug locking implementation
3. **Re-enable**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Locking Utilities | 2 hours | 2 hours |
| Phase 2: Storage Backend | 1 hour | 3 hours |
| Phase 3: Critical Sections | 1 hour | 4 hours |
| Phase 4: Tests | 30 min | 4.5 hours |
| **Total** | | **3-4 hours** |

---

*Plan created based on SSOT violation analysis - Race conditions in file operations*
