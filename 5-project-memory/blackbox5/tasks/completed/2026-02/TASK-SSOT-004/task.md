# TASK-SSOT-004: Derive Task Counts from Files

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Issue:** #11 - SSOT Task State Violations

## Objective
Eliminate duplicate task counts by deriving all statistics from canonical task.md files instead of maintaining separate counts in queue.yaml.

## Current Problem

Task counts are duplicated in multiple locations:
- **queue.yaml**: `total_tasks: 90`, `completed: 25`, `in_progress: 5`, `pending: 60`
- **queue_metadata**: Same counts repeated
- **STATE.yaml**: Lists active and completed tasks separately (only 4 completed listed)
- **timeline.yaml**: Has 81 completion events but STATE.yaml shows only 4

This creates data inconsistency and requires manual synchronization.

## Success Criteria

- [ ] Create script to scan tasks/active/ and tasks/completed/ directories
- [ ] Derive counts dynamically: total, completed, in_progress, pending
- [ ] Replace hardcoded counts in queue.yaml with derived values
- [ ] Remove queue_metadata duplicate counts
- [ ] Add validation that derived counts match actual task files
- [ ] Document the canonical source of truth (task.md files)

## Context

From `ssot-task-state-violations.md`:
- Task status exists in 5 different places
- queue.yaml documents 90 tasks but actual count may differ
- STATE.yaml shows only 4 completed tasks vs 81 in timeline
- Manual sync has 0% success rate

## Recommended SSOT Hierarchy

| Data | SSOT Location | Rationale |
|------|---------------|-----------|
| **Task Status** | `tasks/{active,completed}/TASK-XXX/task.md` | Filesystem location + file content |
| **Task Counts** | Derived from scanning task files | Single calculation point |
| **Task Queue/Ordering** | `queue.yaml` | Purpose-built for RALF scheduling |

## Approach

1. Create `bb5-task-counts.py` script
2. Scan tasks/active/ for active tasks
3. Scan tasks/completed/ for completed tasks
4. Count by status from task.md frontmatter
5. Update queue.yaml counts dynamically
6. Remove manual count maintenance

## Rollback Strategy

- Keep backup of current queue.yaml
- If derivation fails, restore manual counts
- Add validation before committing changes

## Related

- Issue #11: SSOT Task State Violations
- Report: `ssot-task-state-violations.md`
- Related tasks: TASK-SSOT-010, TASK-SSOT-019
