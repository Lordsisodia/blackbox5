# TASK-DOCU-051: Goals System Guide References Non-Existent Files

**Status:** completed
**Priority:** LOW
**Category:** documentation
**Estimated Effort:** 30 minutes
**Created:** 2026-02-05T01:57:10.950131
**Source:** Scout opportunity docs-010 (Score: 5.0)
**Started:** 2026-02-12T21:51:00Z
**Completed:** 2026-02-12T21:58:00Z

---

## Objective

Update GOALS-SYSTEM.md documentation to match the actual goals/ folder structure and create missing completed/ directory.

---

## Success Criteria

- [x] Understand the issue completely
- [x] Update GOALS-SYSTEM.md with correct paths
- [x] Update GOALS-SYSTEM.md with correct file format
- [x] Create completed/ directory
- [x] Document changes in task.md

---

## Context

**Issues Found:**

1. **Wrong Path in Documentation:**
   - Documented: `5-project-memory/ralf-core/.autonomous/goals/`
   - Actual: `5-project-memory/blackbox5/goals/`

2. **Wrong File Format:**
   - Documented: Individual `.md` files (`GOAL-XXX-*.md`)
   - Actual: Subdirectories with `goal.yaml` (`IG-XXX/goal.yaml`)

3. **Missing Directory:**
   - Documented: `completed/` directory exists
   - Actual: `completed/` directory does not exist

**Root Cause:**
Documentation in `/opt/blackbox5/1-docs/02-implementation/07-task-management/design/GOALS-SYSTEM.md` is outdated and doesn't reflect the current implementation which is better documented in `/opt/blackbox5/5-project-memory/blackbox5/goals/README.md`.

**Files to Check/Modify:**
- `/opt/blackbox5/1-docs/02-implementation/07-task-management/design/GOALS-SYSTEM.md` - Update to match actual structure
- `/opt/blackbox5/5-project-memory/blackbox5/goals/completed/` - Create if missing

---

## Rollback Strategy

If changes cause issues:
1. Revert to previous state using git
2. Document what went wrong
3. Update this task with learnings

---

## Notes

### Implementation Summary

**Completed Actions:**

1. **Created completed/ directory** ✅
   - Path: `/opt/blackbox5/5-project-memory/blackbox5/goals/completed/`
   - Added README.md explaining purpose and structure
   - Documented outcome.yaml format for completed goals

2. **Updated GOALS-SYSTEM.md** ✅
   - File: `/opt/blackbox5/1-docs/02-implementation/07-task-management/design/GOALS-SYSTEM.md`
   - Updated Directory Structure section to show correct paths
   - Updated Goal Format section to show YAML-based structure
   - Updated Goal Processing Steps to use subdirectories and YAML
   - Updated Creating a New Goal section with correct commands
   - Updated Updating Goal Progress section for YAML format
   - Updated Completing a Goal section for YAML format
   - Updated RALF integration to use correct paths

**Key Changes:**
- Path: `5-project-memory/ralf-core/.autonomous/goals/` → `5-project-memory/blackbox5/goals/`
- Format: Individual `.md` files → Subdirectories with `goal.yaml`
- Added: `completed/` directory structure documentation

**Files Modified:**
- `/opt/blackbox5/1-docs/02-implementation/07-task-management/design/GOALS-SYSTEM.md`
- `/opt/blackbox5/5-project-memory/blackbox5/goals/completed/README.md` (created)

**Files Created:**
- `/opt/blackbox5/5-project-memory/blackbox5/goals/completed/` (directory)

### Learnings

1. **Documentation Drift:** Design documentation can become outdated when implementation evolves. Regular audits are needed to ensure docs match reality.

2. **Better Source of Truth:** The actual README in the goals/ directory (`goals/README.md`) was more accurate than the design document (`1-docs/.../GOALS-SYSTEM.md`). Should prioritize README files over design docs when discrepancies exist.

3. **YAML vs Markdown:** The switch from markdown files with frontmatter to pure YAML files provides better structure and easier programmatic parsing, at the cost of some human readability.

4. **Directory Structure:** Using subdirectories for goals (IG-XXX/) instead of flat files allows better organization of related files (goal.yaml, timeline.yaml, journal/).

### Time Taken

- Started: 2026-02-12T21:51:00Z
- Completed: 2026-02-12T21:58:00Z
- Total: ~7 minutes (well under 30-minute estimate)
