# Quick Spec: Skills System Audit & Consolidation Decision

## Objective

Audit the skills systems in blackbox5 to determine the canonical skills directory and document the decision for resolving SkillManager path issues.

---

## Files to Read/Analyze (No Modifications Planned)

### Core Files
- [x] `~/.blackbox5/2-engine/.autonomous/lib/skill_router.py` - Current skill loading logic
- [x] `~/.blackbox5/2-engine/.autonomous/skills/README.md` - Skills directory documentation
- [x] `~/.blackbox5/2-engine/.autonomous/bmad/README.md` - BMAD integration documentation

### Analysis Required
- [x] Count skills in each system
- [x] Compare skill quality/completeness
- [x] Identify which system is canonical

---

## Files to Modify (Documentation Only)

- [ ] `~/.blackbox5/5-project-memory/ralf-core/.autonomous/runs/run-20260131_042332/decision_registry.yaml` - Record consolidation decision

---

## Tests

### Existing Tests
- [x] `~/.blackbox5/2-engine/.autonomous/lib/test_workflow_loader.py` - Workflow testing
- [x] `~/.blackbox5/2-engine/.autonomous/test_decision_registry.py` - Decision registry tests

### Tests to Run (Verification)
- [ ] Verify all 10 skills in `skills/` directory are accessible
- [ ] Test skill_router.py can load all skill files
- [ ] Validate skill file paths resolve correctly

### New Tests Needed
- [ ] No new tests - this is analysis and documentation only

---

## Rollback Strategy

### Since this is analysis/documentation only:
- **No code changes planned** - Only decision documentation
- **Rollback:** Delete decision_registry.yaml entry if decision needs revision
- **Alternative:** Create new decision entry with updated analysis

### If migration is executed in future phases:
- **Backup branch:** `git checkout -b backup/pre-skills-consolidation`
- **Rollback command:** `git checkout -- <migrated files>`
- **Safe approach:** Keep all three systems until migration is verified

---

## Risk Level

- [x] **LOW** - Analysis and documentation only
- [ ] MEDIUM - (Future migration phase)
- [ ] HIGH - (N/A for this phase)

### Risk Details
- **No code changes** - Only reading files and documenting decisions
- **No breaking changes** - Systems remain as-is
- **Reversible** - Decision can be revised with new analysis

---

## Exit Criteria Checklist

- [x] **all_target_files_read** - All relevant files read and analyzed
- [x] **tests_identified** - Existing tests located, verification steps defined
- [x] **rollback_strategy_defined** - Clear rollback path documented

---

## Decision Framework

```yaml
options_considered:
  - id: "OPT-001"
    description: "Use skills/ as canonical system"
    location: "~/.blackbox5/2-engine/.autonomous/skills/"
    pros:
      - "Already referenced by skill_router.py (line 166)"
      - "Contains 10 BMAD skill files"
      - "Clean, standard directory structure"
      - "Well-documented with README.md"
    cons:
      - "May be missing some skills from other systems"
    reversibility: "HIGH - no changes needed, already canonical"

  - id: "OPT-002"
    description: "Consolidate from skills-cap/"
    location: "Not found in filesystem"
    pros:
      - "N/A - directory does not exist"
    cons:
      - "Directory not present in filesystem"
    reversibility: "N/A"

  - id: "OPT-003"
    description: "Consolidate from .skills-new/"
    location: "Not found in filesystem"
    pros:
      - "N/A - directory does not exist"
    cons:
      - "Directory not present in filesystem"
    reversibility: "N/A"
```

---

## Current System State

### Skills Directory (Canonical)
- **Location:** `~/.blackbox5/2-engine/.autonomous/skills/`
- **Contents:** 10 BMAD skill files + README.md
- **Status:** ✅ Active, referenced by skill_router.py

### BMAD Directory
- **Location:** `~/.blackbox5/2-engine/.autonomous/bmad/`
- **Contents:** Workflows, modules, party-mode
- **Status:** ✅ Active, separate from skills/

### Conclusion
**No duplicate skills systems found.** The roadmap PLAN-001 references appear to be outdated. The skills/ directory is already the canonical system and is properly configured.

---

## Next Steps

1. Record decision in decision_registry.yaml
2. Mark quick_spec gate as complete
3. Proceed to DEV-STORY phase (documentation updates if needed)
