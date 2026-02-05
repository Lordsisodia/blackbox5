# TASK-SSOT-004: Derive Task Counts from Files Instead of Hardcoding

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #11 - SSOT Task State Violations

## Objective
Remove hardcoded task counts from queue.yaml metadata. Create dynamic counting from actual task files.

## Success Criteria
- [ ] Create bb5 task:count command that scans task directories
- [ ] Remove hardcoded counts from queue.yaml metadata
- [ ] Update queue.yaml to derive counts dynamically
- [ ] Update bb5-queue-manager.py to calculate counts
- [ ] Ensure counts match actual task files

## Context
Current discrepancy:
- queue.yaml shows: 90 total, 25 completed, 5 in_progress, 60 pending
- Actual task files: 104 total, 30+ completed

Hardcoded counts in queue.yaml are stale and unreliable.

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
