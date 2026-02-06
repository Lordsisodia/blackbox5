# TASK-SSOT-019: Make STATE.yaml a Derived View

**Status:** pending
**Priority:** LOW
**Created:** 2026-02-06
**Issue:** #11 - SSOT Task State Violations

## Objective
Transform STATE.yaml from a manually-maintained duplicate data store into a derived view that aggregates information from canonical task.md files.

## Current Problem

STATE.yaml claims to be "Single Source of Truth" but actually duplicates data:
- Only **4 completed tasks** listed vs **110+ actual** completed tasks
- TASK-ARCH-016 appears twice with conflicting statuses
- Data must be manually synced from task.md files
- Manual sync has 0% success rate

**Current STATE.yaml structure:**
```yaml
tasks:
  active:
    - id: "TASK-xxx"
      title: "..."
      type: "..."
      priority: "..."
      started_at: "..."
  completed:
    - id: "TASK-xxx"
      title: "..."
      completed_at: "..."
```

## Success Criteria

- [ ] Create script to generate STATE.yaml from task.md files
- [ ] Scan tasks/active/ for active tasks
- [ ] Scan tasks/completed/ for completed tasks
- [ ] Extract metadata from task.md frontmatter
- [ ] Generate STATE.yaml automatically
- [ ] Add validation that derived STATE.yaml is consistent
- [ ] Document that STATE.yaml is DERIVED, not source
- [ ] Remove manual STATE.yaml updates from workflow

## Context

From `ssot-task-state-violations.md`:
- STATE.yaml claims to be SSOT but duplicates data
- Timeline.yaml has 81 completion events but STATE.yaml shows only 4
- 24 tasks in active directory have Status: completed but weren't moved
- Data inconsistency across all state files

## Recommended SSOT Hierarchy

| Data | SSOT Location | Rationale |
|------|---------------|-----------|
| **Task Status** | `tasks/{active,completed}/TASK-XXX/task.md` | Filesystem location + file content |
| **Project Summary** | `STATE.yaml` | Should be DERIVED, not source |

## Approach

1. Create `bb5-generate-state.py` script
2. Read all tasks/active/*/task.md files
3. Read all tasks/completed/*/task.md files
4. Extract: id, title, type, priority, dates
5. Generate STATE.yaml structure
6. Add to pre-commit hook or CI pipeline
7. Document derivation process

## Rollback Strategy

- Keep backup of manual STATE.yaml
- If derivation has issues, can restore manual version
- Add --check mode to validate without writing

## Related

- Issue #11: SSOT Task State Violations
- Report: `ssot-task-state-violations.md`
- Related tasks: TASK-SSOT-004, TASK-SSOT-010
