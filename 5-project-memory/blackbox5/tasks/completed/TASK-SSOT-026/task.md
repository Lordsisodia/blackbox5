# TASK-SSOT-026: Add File Locking to Shell Scripts

**Status:** completed
**Completed:** 2026-02-07
**Priority:** CRITICAL
**Created:** 2026-02-06
**Parent:** Issue #3 - Missing Storage Abstraction Layer / Issue #5 - Race Conditions

## Objective
Implement file locking in all shell scripts that do read-modify-write operations.

## Success Criteria
- [ ] Add flock to ralf-task-select.sh (queue.yaml operations)
- [ ] Add flock to ralf-stop-hook.sh (metadata.yaml, queue.yaml)
- [ ] Add flock to bb5-parallel-dispatch.sh (execution-state.yaml, queue.yaml)
- [ ] Add flock to subagent-tracking.sh (agent-state.yaml)
- [ ] Add flock to timeline-maintenance.sh (timeline.yaml)
- [ ] Add flock to stop-hierarchy-update.sh (task.md, metadata.yaml)
- [ ] Create locking utility script for reuse
- [ ] Test concurrent access scenarios

## Context
20+ shell scripts perform read-modify-write WITHOUT locking:
```bash
# Current (RISKY)
awk ... "$QUEUE_FILE" > "$QUEUE_FILE.tmp" && mv "$QUEUE_FILE.tmp" "$QUEUE_FILE"

# Should be (SAFE)
flock "$QUEUE_FILE.lock" -c 'awk ... "$QUEUE_FILE" > "$QUEUE_FILE.tmp" && mv "$QUEUE_FILE.tmp" "$QUEUE_FILE"'
```

## Critical Files Needing Locks
1. queue.yaml - ralf-task-select.sh, ralf-stop-hook.sh, bb5-parallel-dispatch.sh
2. events.yaml - ralf-stop-hook.sh, ralf-post-tool-hook.sh
3. heartbeat.yaml - ralf-task-select.sh
4. execution-state.yaml - bb5-parallel-dispatch.sh
5. agent-state.yaml - subagent-tracking.sh
6. timeline.yaml - timeline-maintenance.sh

## Related Files
- shell-script-storage-patterns.md
- storage-transaction-locking-analysis.md

## Rollback Strategy
Can disable locks if issues arise.
