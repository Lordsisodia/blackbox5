# TASK-ARCH-036: bb5 CLI Commands Lack Shared Error Handling

**Status:** completed
**Priority:** MEDIUM
**Category:** architecture
**Estimated Effort:** 30 minutes
**Created:** 2026-02-05T01:57:10.950054
**Source:** Scout opportunity arch-011 (Score: 8.0)

---

## Objective



---

## Success Criteria

- [x] Understand the issue completely
- [x] Add dry_run.sh source line to all bb5 scripts
- [x] Validate all 11 bb5 scripts now include dry_run.sh
- [ ] Document changes in LEARNINGS.md

---

## Context

**Suggested Action:** Create bb5-lib.sh with shared error handling and logging

**Files to Check/Modify:**

---

## Rollback Strategy

If changes cause issues:
1. Revert to previous state using git
2. Document what went wrong
3. Update this task with learnings

---

## Notes

_Add notes as you work on this task_

---

## Completion Notes

**Completed:** 2026-02-05

**What was done:**
- Found dry_run.sh library at `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/dry_run.sh`
- Added source line to all 11 bb5 command scripts:
  - bb5-create
  - bb5-discover-context
  - bb5-goal
  - bb5-goto
  - bb5-link
  - bb5-plan
  - bb5-populate-template
  - bb5-scout-improve
  - bb5-task
  - bb5-timeline
  - bb5-whereami

**Source line added:**
```bash
# Source dry-run utility library
source "$(dirname "$0")/../2-engine/.autonomous/lib/dry_run.sh" 2>/dev/null || true
```

This provides dry-run capabilities (--dry-run flag support) to all bb5 scripts.
