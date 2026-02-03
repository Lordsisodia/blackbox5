# BlackBox5 Architecture Audit

**Date:** 2026-02-02
**Auditor:** Claude
**Scope:** Full project memory review
**Status:** In Progress

---

## Executive Summary

Found **12 architectural issues** across BlackBox5 project memory, ranging from duplicate folders to unclear separation of concerns.

**Critical Issues:** 3
**Medium Issues:** 5
**Low Issues:** 4

---

## Critical Issues (Fix First)

### ARCH-001: Duplicate .autonomous Folders
**Location:** Root level
**Issue:** Two folders with similar purpose:
- `.autonomous/` (dot folder)
- `autonomous/` (regular folder)

**Impact:** Confusion about which to use
**Evidence:**
```
.autonomous/     - 26 subfolders, contains runs, tasks, communications
autonomous/      - 1 subfolder (MIGRATION-PLAN.md)
```

**Recommendation:** Consolidate into single `autonomous/`

---

### ARCH-002: Duplicate Run Systems
**Location:** Multiple
**Issue:** Three places storing run data:
1. `.autonomous/runs/` (8 folders)
2. `runs/` (planner/, executor/, timeline/)
3. `autonomous/runs/` (doesn't exist yet but planned)

**Impact:** Run history fragmented
**Evidence:**
```
.autonomous/runs/     - Old runs (run-20260131_192605, etc.)
runs/planner/         - 77 run folders
runs/executor/        - 61 run folders
```

**Recommendation:** Consolidate all runs into `runs/` only

---

### ARCH-003: Legacy Task System
**Location:** `tasks/` vs `.autonomous/tasks/`
**Issue:** Two task systems coexist:
- `tasks/` - Legacy (backlog/, working/, completed/)
- `.autonomous/tasks/` - New system (active/, completed/, improvements/)

**Impact:** Agents confused about which to use
**Evidence:**
```
tasks/backlog/           - Legacy
tasks/working/           - Legacy
.autonomous/tasks/active/ - New (1 task)
```

**Recommendation:** Migrate legacy tasks to `.autonomous/tasks/manual/`

---

## Medium Issues

### ARCH-004: Empty/Underused Folders
**Locations:**
- `.analysis/` - Empty?
- `.archived/` - Check if needed
- `memory/` - vs `.autonomous/memory/` - Duplicate?
- `project/` - What's this for?

**Recommendation:** Audit and delete if unused

---

### ARCH-005: Unclear .docs vs .templates Distinction
**Issue:** Both contain templates/documentation
- `.docs/` - Documentation templates
- `.templates/` - File templates

**Question:** What's the difference?
**Recommendation:** Clarify or consolidate

---

### ARCH-006: Planner Tracking Duplication
**Locations:**
- `.autonomous/planner-tracking/`
- `runs/planner/`

**Issue:** Planner data in two places
**Recommendation:** Consolidate into `runs/planner/`

---

### ARCH-007: Operations Folder Scope
**Location:** `.autonomous/operations/`
**Issue:** Contains:
- `.docs/`
- `architecture/` (empty)
- `dashboard/`
- `logs/`
- `sessions/`
- `workflows/`

**Question:** How is this different from root `operations/`?
**Recommendation:** Clarify scope or consolidate

---

### ARCH-008: Validations Folder Empty
**Location:** `.autonomous/validations/`
**Issue:** Empty folder
**Recommendation:** Delete or document purpose

---

## Low Issues

### ARCH-009: Naming Inconsistency
**Issue:** Some folders use kebab-case, some camelCase
- `planner-tracking/` (kebab)
- `FG-1769138998/` (camel/task ID)

**Recommendation:** Standardize on kebab-case

---

### ARCH-010: Feedback Folder Location
**Location:** `.autonomous/feedback/incoming/`
**Issue:** Only one subfolder, rarely used
**Recommendation:** Consider if needed or merge with communications

---

### ARCH-011: Goals in Two Places
**Locations:**
- `goals.yaml` (root)
- `.autonomous/goals/` (completed/, templates/)

**Issue:** Goals split between file and folder
**Recommendation:** Consolidate into single system

---

### ARCH-012: Timeline Duplication
**Locations:**
- `.autonomous/timeline/`
- `runs/timeline/`
- `timeline.yaml` (root file)

**Issue:** Three timeline locations
**Recommendation:** Consolidate into single timeline system

---

## Recommendations Summary

### Phase 1: Consolidation (Critical)
1. Merge `.autonomous/` into `autonomous/`
2. Move `.autonomous/runs/` to `runs/archived/`
3. Migrate `tasks/` to `autonomous/tasks/manual/`

### Phase 2: Cleanup (Medium)
4. Delete empty folders (.analysis?, .archived?, validations/)
5. Consolidate planner tracking
6. Clarify operations scope

### Phase 3: Standardization (Low)
7. Standardize naming conventions
8. Merge timeline systems
9. Consolidate goals

---

## Files to Review

### High Priority
- [ ] `.autonomous/` vs `autonomous/` - Which stays?
- [ ] `.autonomous/runs/` - Move to `runs/`?
- [ ] `tasks/` - Migrate to new system?

### Medium Priority
- [ ] `memory/` vs `.autonomous/memory/` - Duplicate?
- [ ] `project/` - What's this for?
- [ ] `.autonomous/validations/` - Delete?

### Low Priority
- [ ] Naming conventions across folders
- [ ] Timeline consolidation
- [ ] Goals consolidation

---

## Questions for Review

1. Is `.analysis/` used for anything?
2. What's the difference between `.docs/` and `.templates/`?
3. Should `memory/` be inside `.autonomous/` or separate?
4. What's `project/` folder for?
5. Is `.archived/` still needed?

---

## Next Steps

1. Review this audit
2. Decide on consolidation approach
3. Update architecture/plans/TARGET_STRUCTURE.md
4. Create migration tasks
5. Execute phase by phase
