# TASK-ARCH-017: blackbox.py References Non-Existent Directory Structure

**Status:** completed
**Priority:** MEDIUM
**Category:** architecture
**Estimated Effort:** 15 minutes
**Created:** 2026-02-05T01:57:10.949955
**Source:** Scout opportunity arch-012 (Score: 11.5)

---

## Objective

Fix the ENGINE_DIR path reference in blackbox.py to point to the correct directory.

---

## Success Criteria

- [x] Understand the issue completely
- [x] Implement the suggested action
- [x] Validate the fix works
- [x] Document changes in LEARNINGS.md

---

## Context

**Suggested Action:** Update ENGINE_DIR path to '2-engine/core'

**Files to Check/Modify:**
- `/Users/shaansisodia/.blackbox5/bin/blackbox.py`

---

## Rollback Strategy

If changes cause issues:
1. Revert to previous state using git
2. Document what went wrong
3. Update this task with learnings

---

## Notes

**Completed 2026-02-05:**
- Found blackbox.py at `/Users/shaansisodia/.blackbox5/bin/blackbox.py`
- Line 26 had: `ENGINE_DIR = Path(__file__).parent / "2-engine" / "01-core"`
- Changed to: `ENGINE_DIR = Path(__file__).parent / "2-engine" / "core"`
- Verified the `core/` directory exists at `/Users/shaansisodia/.blackbox5/2-engine/core/`
- Fix applied using sed command
