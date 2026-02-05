# TASK-SSOT-024: Implement File Locking for Race Condition Prevention

**Status:** pending
**Priority:** CRITICAL
**Created:** 2026-02-06
**Parent:** Issue #5 - File-Based Coordination Race Conditions

## Objective
Implement file locking mechanisms to prevent race conditions in shared files.

## Success Criteria
- [ ] Create `storage/locking.py` with FileLock class
- [ ] Implement Python fcntl locking (Unix)
- [ ] Implement cross-platform portalocker fallback
- [ ] Create bash flock wrapper for shell scripts
- [ ] Add atomic read-modify-write operations
- [ ] Update bb5-parallel-dispatch.sh with locking
- [ ] Update queue.yaml operations with locking
- [ ] Update events.yaml appends with locking
- [ ] Test concurrent access scenarios

## Context
7 critical files with race condition risks:
- queue.yaml - task claims (CRITICAL)
- events.yaml - append-only writes (CRITICAL)
- execution-state.yaml - slot updates (MEDIUM)
- agent-state.yaml - status updates (MEDIUM)

## Locking Patterns
```python
# Python
with FileLock(filepath):
    data = storage.load(filepath)
    data['status'] = 'claimed'
    storage.save(filepath, data)

# Bash
flock /tmp/queue.lock -c 'yq eval ".tasks[0].status = \"claimed\"" queue.yaml'
```

## Related Files
- storage-transaction-locking-analysis.md
- bb5-parallel-dispatch.sh
- bb5-queue-manager.py

## Rollback Strategy
Can disable locking if performance issues arise.
