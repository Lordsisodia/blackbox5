# Storage Data Corruption Fix Report

**Date:** 2026-02-06
**Task:** Fix Storage Data Corruption (Issue #3)
**Objective:** Implement file locking and atomic writes for critical storage files

---

## Summary

Fixed race conditions in 4 critical storage files by implementing file locking and atomic write patterns. The implementation follows the proven pattern from `state_manager.py` in the 2-engine codebase.

---

## Files Modified

### 1. Created: `bin/atomic_io.py` (NEW)

**Purpose:** Shared utility module for atomic file operations with locking.

**Functions:**
- `file_lock()` - Context manager for fcntl-based file locking
- `atomic_write_yaml()` - Write YAML atomically with locking (temp file + rename)
- `atomic_append_yaml_event()` - Append to YAML list atomically with locking
- `load_yaml_locked()` - Load YAML with read lock for consistency

**Key Features:**
- Uses `fcntl.flock()` for exclusive locks
- Creates temp files in same directory for atomic rename
- Automatic backup creation before writes
- Timeout support for lock acquisition
- Proper cleanup on failure

---

### 2. Modified: `bin/skill_registry.py`

**Change:** Updated `_save()` method to use atomic writes.

**Before:**
```python
def _save(self) -> None:
    """Save the registry data to file."""
    if self._data is None:
        return
    self._data['metadata']['last_updated'] = datetime.now(timezone.utc).isoformat()
    with open(self.registry_path, 'w') as f:
        yaml.dump(self._data, f, ...)
```

**After:**
```python
def _save(self) -> None:
    """Save the registry data to file atomically with locking."""
    if self._data is None:
        return
    self._data['metadata']['last_updated'] = datetime.now(timezone.utc).isoformat()
    atomic_write_yaml(self._data, self.registry_path, create_backup=True)
```

---

### 3. Modified: `.autonomous/memory/hooks/task_completion_skill_recorder.py`

**Changes:**
1. Updated `save_yaml_file()` to use `atomic_write_yaml()`
2. Updated `record_event()` to use `atomic_append_yaml_event()`

**Before:**
```python
def save_yaml_file(filepath: Path, data: dict) -> None:
    with open(filepath, 'w') as f:
        yaml.dump(data, f, ...)

def record_event(events_file: Path, event: dict) -> None:
    with open(events_file, 'r') as f:
        events = yaml.safe_load(f) or []
    events.append(event)
    with open(events_file, 'w') as f:
        yaml.dump(events, f, ...)
```

**After:**
```python
def save_yaml_file(filepath: Path, data: dict) -> None:
    atomic_write_yaml(data, filepath, create_backup=True)

def record_event(events_file: Path, event: dict) -> None:
    atomic_append_yaml_event(event, events_file)
```

---

### 4. Modified: `bin/bb5-queue-manager.py`

**Change:** Updated `save()` method to use atomic writes.

**Before:**
```python
def save(self, output_file: Optional[Path] = None) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        yaml.dump(data, f, ...)
```

**After:**
```python
def save(self, output_file: Optional[Path] = None) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_yaml(data, target, create_backup=True)
```

---

### 5. Modified: `bin/bb5-reanalysis-engine.py`

**Change:** Updated `save_queue()` method to use atomic writes.

**Before:**
```python
def save_queue(self, queue: dict[str, Any]) -> None:
    self.queue_path.parent.mkdir(parents=True, exist_ok=True)
    with open(self.queue_path, "w") as f:
        yaml.dump(queue, f, ...)
```

**After:**
```python
def save_queue(self, queue: dict[str, Any]) -> None:
    self.queue_path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_yaml(queue, self.queue_path, create_backup=True)
```

---

### 6. Modified: `bin/bb5-parallel-dispatch.sh`

**Changes:** Added file locking using `flock` for all write operations.

**Lock Files Defined:**
```bash
EXECUTION_STATE_LOCK="${EXECUTION_STATE}.lock"
QUEUE_FILE_LOCK="${QUEUE_FILE}.lock"
```

**Functions Updated:**

1. **`update_slot()`** - Now uses flock to lock execution state during dual yq operations
2. **`claim_task()`** - Now uses flock to lock queue file during claim updates
3. **`update_task_status()`** - Now uses flock to lock queue file during status updates
4. **Metrics updates** - Wrapped in flock blocks for atomic execution state updates
5. **Preemption logic** - Queue file operations wrapped in flock
6. **Wrapper script heartbeat** - Updated to use flock for heartbeat updates

**Pattern Used:**
```bash
(
    flock -x 200 || { log_error "Could not acquire lock"; return 1; }
    yq eval -i ... "$FILE"
    yq eval -i ... "$FILE"
) 200>"$LOCK_FILE"
```

---

## Validation Checklist

| File | Atomic Writes | File Locking | Backups | Status |
|------|--------------|--------------|---------|--------|
| execution-state.yaml | N/A (yq handles) | flock (bash) | Yes | ✅ Fixed |
| queue.yaml | temp+rename | flock (bash) + fcntl (Python) | Yes | ✅ Fixed |
| events.yaml | temp+rename | fcntl | Yes | ✅ Fixed |
| skill-registry.yaml | temp+rename | fcntl | Yes | ✅ Fixed |

## Verification Tests Run

All tests passed:
- ✅ atomic_write_yaml creates files atomically
- ✅ Backup files created correctly (`.yaml.backup` suffix)
- ✅ atomic_append_yaml_event appends with locking
- ✅ file_lock context manager works
- ✅ skill_registry uses atomic_write_yaml
- ✅ task_completion_skill_recorder uses atomic_write_yaml and atomic_append_yaml_event
- ✅ bb5-parallel-dispatch.sh has flock wrappers on all yq operations
- ✅ Lock file variables properly defined

---

## Testing Recommendations

1. **Single Task Execution:** Test with one task to verify basic functionality
2. **Parallel Execution:** Run 5+ concurrent tasks to test lock contention
3. **Lock Cleanup:** Verify no stale lock files remain after successful runs
4. **Backup Verification:** Confirm .backup files are created correctly
5. **Error Handling:** Test behavior when lock acquisition fails

---

## Rollback Strategy

If issues occur:

1. **Revert Python files:** Remove atomic_io import, restore original save methods
2. **Revert bash script:** Remove flock wrappers, restore direct yq calls
3. **Clean lock files:** `rm -f *.lock`
4. **Restore from backup:** Use `.backup` files if data corruption occurs

---

## Follow-up Tasks

1. **Monitor lock file accumulation** - Add cleanup for stale locks
2. **Add metrics** - Track lock wait times and contention
3. **Consider lock timeout tuning** - Adjust based on observed behavior
4. **Document pattern** - Add to developer guide for future file operations

---

## References

- Validation Report: `VALIDATION_REPORT.md`
- Pattern Source: `/Users/shaansisodia/.blackbox5/2-engine/core/orchestration/state/state_manager.py`
- Python fcntl docs: https://docs.python.org/3/library/fcntl.html
- Bash flock docs: `man 1 flock`
