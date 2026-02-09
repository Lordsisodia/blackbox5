# TASK-SSOT-004: Derive Task Counts from Files Instead of Hardcoding

**Status:** completed
**Priority:** HIGH
**Created:** 2026-02-06
**Completed:** 2026-02-07
**Parent:** Issue #11 - SSOT Task State Violations

## Objective
Remove hardcoded task counts from queue.yaml metadata. Create dynamic counting from actual task files.

## Success Criteria
- [x] Create bb5 task:count command that scans task directories
- [x] Remove hardcoded counts from queue.yaml metadata
- [x] Update queue.yaml to derive counts dynamically
- [x] Update bb5-queue-manager.py to calculate counts
- [x] Ensure counts match actual task files

## Context
Current discrepancy (before fix):
- queue.yaml showed: 88 total, 24 completed, 4 in_progress, 60 pending
- Actual task files: 244 total, 92 completed, 8 in_progress, 112 pending

Hardcoded counts in queue.yaml were stale and unreliable.

## Implementation Summary

Created `bin/bb5-task-counter.py` with the following features:
- `count` command: Scans tasks/active/, tasks/completed/, tasks/cancelled/ and counts by status
- `update` command: Updates queue.yaml with dynamically calculated counts
- `validate` command: Validates queue.yaml counts match filesystem

Updated `bin/bb5-queue-manager.py` with:
- `sync-counts` command: Delegates to bb5-task-counter.py update
- `validate-counts` command: Delegates to bb5-task-counter.py validate

The queue.yaml now includes:
- `derived_from_filesystem: true` flag
- `last_counted_at` timestamp
- Dynamic counts in both `schema` and `queue_metadata` sections

## Files Modified
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/bb5-task-counter.py` (created)
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/bb5-queue-manager.py` (updated)
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` (updated with dynamic counts)

## Approach
1. Create function to scan tasks/active/ and tasks/completed/
2. Count tasks by status from file content
3. Update queue.yaml generation to use dynamic counts
4. Remove manual count updates
5. Add validation that counts match reality

## Related Files
- queue.yaml
- bin/bb5-queue-manager.py
- bin/bb5-task
- tasks/active/*/task.md
- tasks/completed/*/task.md

## Rollback Strategy
Can revert to hardcoded counts if dynamic counting has issues.
