# TASK-ARCH-004: Document SSOT Pattern for Future Agents

**Status:** completed
**Completed:** 2026-02-04
**Actual Time:** 15 minutes
**Priority:** MEDIUM
**Created:** 2026-02-04
**Estimated:** 30 minutes
**Goal:** IG-007
**Plan:** PLAN-ARCH-001
**Depends On:** TASK-ARCH-003

---

## Objective

Create comprehensive documentation explaining the Single Source of Truth pattern used in BlackBox5, so future AI agents understand where to find and update information.

---

## Success Criteria

- [x] Document created at knowledge/architecture/ssot-pattern.md
- [x] Clear table showing what lives where
- [x] Examples of correct vs. incorrect patterns
- [x] Instructions for Ralf-context.md generation
- [x] Validation process documented

---

## Content Outline

### 1. The Pattern
- Reference, don't duplicate
- One canonical source per concern
- STATE.yaml as aggregator/index

### 2. Canonical Sources Reference
| Concern | Location | Update When |
|---------|----------|-------------|
| Project identity | project/context.yaml | Project changes |
| Active goals | goals/active/*/goal.yaml | Goals change |
| Active tasks | tasks/active/*/task.md | Tasks change |
| Decisions | decisions/*/*.md | Decisions made |
| Structure | STATE.yaml | Structure changes |
| Templates | .templates/ | Templates change |

### 3. Anti-Patterns to Avoid
- Copying data between files
- Assuming STATE.yaml is always right
- Not updating references when moving files

### 4. Ralf-context.md
- Derived from canonical sources
- Updated per RALF loop
- Not a source of truth

---

## Notes

This documentation prevents future SSOT violations by making the pattern explicit and discoverable.
