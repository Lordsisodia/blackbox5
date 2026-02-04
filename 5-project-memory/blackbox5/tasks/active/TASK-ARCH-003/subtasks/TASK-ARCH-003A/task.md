# TASK-ARCH-003A: Plan the SSOT Fix

**Status:** completed
**Completed:** 2026-02-04
**Priority:** CRITICAL
**Parent Task:** TASK-ARCH-003
**Created:** 2026-02-04
**Estimated:** 15 minutes

---

## Objective

Create detailed plan for fixing SSOT violations. Define exactly what needs to change, in what order, with rollback points.

## Results

✅ **Sub-Agent Delegation Plan Created**

Location: `.autonomous/research-pipeline/agents/ssot-fix/DELEGATION-PLAN.md`

**Agents Created:**
- auditor-worker (bmad-analyst) + auditor-validator (bmad-qa)
- fixer-worker (bmad-dev) + fixer-validator (bmad-architect)
- final-validator (bmad-qa + bmad-tea)

**Infrastructure Created:**
- Agent directories with timeline-memory.md for each
- Communication files (state, events, chat-log)
- Work assignment logic and validation checklists

---

## Success Criteria

- [x] Complete list of all changes needed
- [x] Order of operations defined
- [x] Rollback points identified
- [x] Risk assessment complete
- [x] Plan reviewed and approved
- [x] Sub-agent delegation plan created
- [x] Agent infrastructure set up

---

## Changes to Plan

### 1. STATE.yaml Structural Changes

**Files to Remove from root_files section:**
- ACTIVE.md (deleted in cleanup)
- WORK-LOG.md (deleted in cleanup)
- _NAMING.md (moved to knowledge/conventions/naming.md)
- QUERIES.md (deleted in cleanup)
- UNIFIED-STRUCTURE.md (deleted in cleanup)

**YAML Fix Needed:**
- Location: Lines 360-361 (docs section)
- Issue: Indentation/mapping error
- Fix: Correct list syntax

### 2. Project Identity Changes

**Option A:** Keep context.yaml as canonical
- STATE.yaml removes duplicate project: section
- STATE.yaml adds: `project_reference: "project/context.yaml"`
- Update context.yaml version to 5.1.0 (match STATE.yaml)

**Option B:** Keep STATE.yaml as canonical
- Update context.yaml to match STATE.yaml
- Less ideal (violates hierarchy principle)

**Decision:** Option A (context.yaml = canonical)

### 3. Goal-Task Link Fixes

**IG-006 references non-existent tasks:**
- TASK-001, TASK-002, TASK-003 don't exist
- **Fix:** Remove references from IG-006 goal.yaml

**IG-007 references:**
- TASK-ARCH-003, TASK-ARCH-004 exist ✅
- **Fix:** Already created, just verify symlinks

### 4. Validation Checkpoints

**Checkpoint 1:** After STATE.yaml fixes
- Run: `python3 bin/validate-ssot.py`
- Should pass YAML parse + file existence checks

**Checkpoint 2:** After canonical source changes
- Verify context.yaml is loadable
- Verify references work

**Checkpoint 3:** Final validation
- All validation checks pass
- RALF loop test (read Ralf-context.md)

---

## Execution Order

```
1. Backup current STATE.yaml
2. Fix YAML parse error (lines 360-361)
3. Remove deleted file references
4. Update project section to reference context.yaml
5. Sync version numbers
6. Fix IG-006 goal.yaml (remove bad task refs)
7. Validate with script
8. Test RALF context loading
```

---

## Rollback Points

**Point 1:** After Step 2 (YAML fix)
- If parse still fails: restore backup, debug

**Point 2:** After Step 5 (all STATE.yaml changes)
- If validation fails: restore backup, reassess

**Point 3:** After Step 7 (validation)
- If RALF breaks: restore backup, check Ralf-context.md generation

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| YAML still broken after fix | Low | High | Test syntax before commit |
| RALF loop breaks | Medium | High | Test after each change |
| Lose important data | Low | Critical | Git backup before changes |
| Validation still fails | Medium | Medium | Fix iteratively |

---

## Deliverable

This document = the plan. Once approved, proceed to TASK-ARCH-003B (Audit).
