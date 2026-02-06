# Results: TASK-ARCH-004 Document SSOT Pattern

**Status:** COMPLETED
**Completed:** 2026-02-04
**Duration:** 15 minutes

---

## Summary

Created comprehensive documentation explaining the Single Source of Truth pattern used in BlackBox5. The document serves as a reference for future AI agents to understand where information lives and how to maintain SSOT principles.

---

## Deliverable

**Document:** `knowledge/architecture/ssot-pattern.md`

**Sections:**
1. **Overview** - Core principle: Reference, don't duplicate
2. **The Pattern** - One canonical source per concern
3. **Canonical Sources Reference** - Table of all canonical locations
4. **Anti-Patterns to Avoid** - Common mistakes with examples
5. **Ralf-context.md** - Explanation of derived documents
6. **Validation Process** - How to check for SSOT violations
7. **Examples** - Real-world scenarios (correct vs incorrect)
8. **Quick Reference** - Lookup table for common actions

---

## Key Content

### Canonical Sources Table

| Concern | Location | Update When |
|---------|----------|-------------|
| Project identity | project/context.yaml | Project changes |
| Active goals | goals/active/*/goal.yaml | Goals change |
| Active tasks | tasks/active/*/task.md | Tasks change |
| Decisions | decisions/*/*.md | Decisions made |
| Structure | STATE.yaml | Structure changes |
| Templates | .templates/ | Templates change |

### Anti-Patterns Documented

1. ❌ Copying data between files
2. ❌ Assuming STATE.yaml is always right
3. ❌ Not updating references when moving files
4. ❌ Creating multiple sources for same info

### Examples Provided

1. Adding a new goal (correct vs incorrect flow)
2. Updating project version
3. Moving a task

---

## Impact

Future AI agents working on BlackBox5 can now:
- Understand where information lives
- Follow SSOT principles correctly
- Avoid common duplication mistakes
- Validate their changes
- Maintain consistency across the project

---

## Next Steps

This documentation supports the continuous architecture evolution goal (IG-007) by making the patterns explicit and discoverable.

**Related:**
- TASK-ARCH-003 (SSOT violations fixed)
- IG-007 (Continuous Architecture Evolution)
- `bin/validate-ssot.py` (validation script)
