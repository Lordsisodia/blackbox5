# TASK-SSOT-010: Remove Duplicate Task Entries from Queue

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #11 - SSOT Task State Violations

## Objective
Remove 13 duplicate task entries from queue.yaml. Fix TASK-ARCH-016 appearing twice.

## Success Criteria
- [ ] Identify all 13 duplicate task pairs in queue.yaml
- [ ] Remove duplicate entries
- [ ] Fix TASK-ARCH-016 double entry (keep one with correct status)
- [ ] Verify queue.yaml is valid YAML after changes
- [ ] Update task count metadata

## Context
queue.yaml documents 13 duplicate task pairs (lines 49-62):
- AGENT-SYSTEM-AUDIT / TASK-AUTO-010
- TASK-1769978192 / TASK-ARCH-016
- And 11 more...

TASK-ARCH-016 appears twice with different statuses.

## Approach
1. Read queue.yaml duplicate comments
2. Remove duplicate entries
3. Keep the "real" task ID in each case
4. Validate YAML syntax
5. Update counts

## Related Files
- queue.yaml
- tasks/active/TASK-ARCH-016/task.md

## Rollback Strategy
Keep backup of queue.yaml before editing.
