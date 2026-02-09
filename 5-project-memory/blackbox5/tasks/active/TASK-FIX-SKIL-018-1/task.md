# TASK-FIX-SKIL-018-1: Update Skill Selection Rule to "MUST Invoke"

**Status:** pending
**Priority:** HIGH
**Category:** skills
**Estimated Effort:** 20 minutes
**Created:** 2026-02-09
**Parent Task:** TASK-SKIL-018

---

## Objective

Change the skill selection rule from "MUST check" to "MUST invoke" for clear trigger conditions to eliminate subjective threshold overrides.

---

## Success Criteria

- [ ] Update rule 004-phase-1-5-skill-check.md to say "MUST invoke" for clear triggers
- [ ] Update CLAUDE.md skill selection section with same change
- [ ] Define "clear triggers" explicitly (confidence >= 85%)
- [ ] Document when agents MAY still use judgment (confidence 70-84%)
- [ ] Update skill-selection.yaml with clear/unclear trigger distinction

---

## Context

**Root Cause Identified:**
The current rule says "MUST check" not "MUST invoke" - this allows agents to override the threshold subjectively even when triggers are clear.

**Current Wording:**
```
"MUST check for applicable skills"
"Invoke skill only if confidence >= 70%"
```

**Problem:** Agents read the skill, calculate confidence, then override based on subjective judgment.

**Solution:** For clear triggers (confidence >= 85%), change to "MUST invoke" - no override allowed.

---

## Files to Modify

1. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.claude/rules/004-phase-1-5-skill-check.md`
   - Change "MUST check" to "MUST invoke" for clear triggers
   - Add "Clear Trigger" definition (>= 85% confidence)
   - Add "Discretionary" range (70-84% confidence)

2. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.claude/CLAUDE.md`
   - Update Phase 1.5 section with same distinction
   - Update Auto-Trigger Rules table

3. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-selection.yaml`
   - Add `clear_trigger_threshold: 85`
   - Add `discretionary_threshold: 70`
   - Update domain mappings with trigger_type (clear/discretionary)

---

## Approach

1. Read current versions of all three files
2. Draft new wording for rule 004
3. Update CLAUDE.md Phase 1.5 section
4. Update skill-selection.yaml schema
5. Review for consistency across all files

---

## Rollback Strategy

If changes cause issues:
1. Revert to previous git commit
2. Document which wording caused problems
3. Create new task to refine the rule

---

## Notes

**Key Distinction to Add:**

| Confidence | Action | Override Allowed |
|------------|--------|------------------|
| >= 85% | MUST invoke | NO - Automatic |
| 70-84% | SHOULD invoke | YES - Agent discretion |
| < 70% | MAY check | YES - Agent discretion |

**Clear Trigger Examples (85%+ confidence):**
- "implement" + exact domain match (e.g., "implement git commit")
- "Should we..." + architecture keyword
- "PRD" + feature definition

**Discretionary Examples (70-84% confidence):**
- "implement" + related domain
- "analyze" + partial match
- "test" + unclear scope
