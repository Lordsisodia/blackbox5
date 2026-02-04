# TASK-ARCH-003: Fix Single Source of Truth Violations

**Status:** in_progress
**Started:** 2026-02-04
**Sub-Agent Plan:** Complete
**Priority:** CRITICAL
**Created:** 2026-02-04
**Estimated:** 90 minutes
**Goal:** IG-007
**Plan:** PLAN-ARCH-001
**Decision:** DEC-2026-02-04-ssot-violations-analysis

---

## Objective

Implement Option A from the SSOT analysis: Make STATE.yaml an aggregator that references canonical sources, not a duplicator. Fix all 8 validation errors found by validate-ssot.py.

---

## Success Criteria

- [ ] STATE.yaml YAML parse errors fixed
- [ ] All deleted file references removed from STATE.yaml
- [ ] Project identity references project/context.yaml
- [ ] Version numbers synchronized
- [ ] Goal task references fixed (TASK-001, TASK-002, TASK-003, TASK-ARCH-003, TASK-ARCH-004)
- [ ] Validation script passes
- [ ] RALF loop still works after changes

---

## Violations to Fix

### 1. YAML Parse Errors (STATE.yaml)
**Location:** Lines 360-361
**Issue:** Malformed YAML in docs section
**Fix:** Correct indentation/list syntax

### 2. Deleted File References
**Files to Remove from STATE.yaml:**
- ACTIVE.md (deleted)
- WORK-LOG.md (deleted)
- _NAMING.md (moved to knowledge/conventions/)
- QUERIES.md (deleted)
- UNIFIED-STRUCTURE.md (deleted)

### 3. Version Mismatch
**Current:** STATE.yaml says 5.1.0, context.yaml says 5.0.0
**Fix:** Decide canonical version, update both

### 4. Missing Task References
**Goals reference non-existent tasks:**
- IG-006 references TASK-001, TASK-002, TASK-003
- IG-007 references TASK-ARCH-003, TASK-ARCH-004
**Fix:** Either create tasks or remove references

---

## Sub-Agent Delegation Plan

**Approach:** Dual-RALF Worker-Validator Pattern
**Location:** `.autonomous/research-pipeline/agents/ssot-fix/`
**Plan:** `DELEGATION-PLAN.md`

### Agent Mapping

| Subtask | Worker | Validator | Skill | Phase |
|---------|--------|-----------|-------|-------|
| TASK-ARCH-003B | auditor-worker | auditor-validator | bmad-analyst + bmad-qa | Audit |
| TASK-ARCH-003C | fixer-worker | fixer-validator | bmad-dev + bmad-architect | Execute |
| TASK-ARCH-003D | final-validator | (self) | bmad-qa + bmad-tea | Validate |

### Communication Files
- `communications/ssot-pipeline-state.yaml` - Overall pipeline state
- `communications/ssot-events.yaml` - Event bus
- `communications/ssot-chat-log.yaml` - Agent coordination

### Agent Timeline Memory
Each agent has `memory/timeline-memory.md` injected via SessionStart hook:
- `auditor-worker/memory/timeline-memory.md` - Audit work queue
- `auditor-validator/memory/timeline-memory.md` - Validation checklist
- `fixer-worker/memory/timeline-memory.md` - Fix specifications
- `fixer-validator/memory/timeline-memory.md` - SSOT principles
- `final-validator/memory/timeline-memory.md` - Validation checklist

---

## Subtasks (Plan → Audit → Execute → Validate)

### TASK-ARCH-003A: Plan the SSOT Fix (15 min)
**Status:** completed
**Completed:** 2026-02-04
- Defined exact changes needed
- Created sub-agent delegation plan
- Set up worker-validator pairs
- Created communication infrastructure

### TASK-ARCH-003B: Audit Current State (20 min)
**Status:** pending
**Agent:** auditor-worker (bmad-analyst)
**Validator:** auditor-validator (bmad-qa)
- Inventory all root files vs. STATE.yaml references
- Document broken references
- Version number audit
- Goal-task link audit
- Create audit report

### TASK-ARCH-003C: Execute SSOT Fixes (45 min)
**Status:** pending
**Agent:** fixer-worker (bmad-dev)
**Validator:** fixer-validator (bmad-architect)
- Backup STATE.yaml
- Fix YAML parse error
- Remove deleted file references
- Update project section to reference context.yaml
- Sync version numbers
- Fix goal-task links
- Validate and commit

### TASK-ARCH-003D: Validate and Document (10 min)
**Status:** pending
**Agent:** final-validator (bmad-qa + bmad-tea)
- Run full validation
- Test RALF context
- Update RESULTS.md
- Update LEARNINGS.md
- Mark task complete

---

## Rollback Strategy

If changes break something:
1. Git revert to pre-change state
2. Document what failed
3. Try smaller incremental changes

---

## Notes

**Key Principle:** STATE.yaml should be an index, not a database.

**Before:**
```yaml
project:
  name: blackbox5
  version: "5.1.0"  # Duplicate of context.yaml
  description: "..." # Duplicate of context.yaml
```

**After:**
```yaml
project:
  reference: "project/context.yaml"  # Canonical source
  cached_version: "5.1.0"  # For quick access
  last_sync: "2026-02-04"
```

**Ralf-context.md:**
- Keep as-is (needed for RALF loop)
- Document that it's derived from canonical sources
- Update generation process if needed
