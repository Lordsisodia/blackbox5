# TASK-FIX-SKIL-018-1: Update Skill Selection Rule to "MUST Invoke"

**Status:** completed
**Priority:** HIGH
**Category:** skills
**Estimated Effort:** 20 minutes
**Created:** 2026-02-09
**Completed:** 2026-02-10T22:33:00Z
**Parent Task:** TASK-SKIL-018

---

## Objective

Change the skill selection rule from "MUST check" to "MUST invoke" for clear trigger conditions to eliminate subjective threshold overrides.

---

## Success Criteria

- [x] Update rule 004-phase-1-5-skill-check.md to say "MUST invoke" for clear triggers
- [x] Update CLAUDE.md skill selection section with same change
- [x] Define "clear triggers" explicitly (confidence >= 85%)
- [x] Document when agents MAY still use judgment (confidence 70-84%)
- [x] Update skill-selection.yaml with clear/unclear trigger distinction

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

## Implementation Summary

### Changes Made

**1. Updated `.claude/rules/004-phase-1-5-skill-check.md`:**
- Changed "MUST check" to "MUST invoke" for clear triggers (>= 85% confidence)
- Added "Clear vs Discretionary Triggers" section explaining the distinction
- Updated Auto-Trigger Rules table with Confidence and Override Allowed columns
- Clear triggers: >= 85% confidence, MUST invoke, NO override
- Discretionary triggers: 70-84% confidence, SHOULD invoke, YES override allowed
- Low confidence: < 70%, MAY check, YES override allowed

**2. Updated `.claude/CLAUDE.md` Phase 1.5 section:**
- Same changes as rule file for consistency
- Added Clear vs Discretionary Triggers table
- Expanded Auto-Trigger Rules table with confidence levels
- Updated skill-selection.yaml path reference to point to skill-registry.yaml

**3. Updated `operations/skill-registry.yaml` selection_framework section:**
- Updated version from 1.2.0 to 1.3.0
- Added `clear_trigger_threshold: 85`
- Added `discretionary_threshold: 70`
- Added `trigger_type: clear` to high-priority rules (ATR-004, ATR-005)
- Added `trigger_type: discretionary` to other rules (ATR-001, ATR-002, ATR-003, ATR-006, ATR-007, ATR-008, ATR-009, ATR-010)

### Clear Trigger Rules (85%+ confidence - MUST Invoke)
- ATR-004: Decision Questions ("Should we..." + architecture)
- ATR-005: Product Management Tasks ("PRD" + feature definition)

### Discretionary Trigger Rules (70-84% - SHOULD Invoke)
- ATR-001: Implementation Tasks (with domain keywords)
- ATR-002: Analysis Tasks
- ATR-003: Architecture Tasks
- ATR-006: Quality Assurance Tasks
- ATR-007: Multi-File Tasks
- ATR-008: Git Operations
- ATR-009: Database Operations
- ATR-010: Continuous Improvement

### All Success Criteria Met

- [x] Update rule 004-phase-1-5-skill-check.md to say "MUST invoke" for clear triggers
- [x] Update CLAUDE.md skill selection section with same change
- [x] Define "clear triggers" explicitly (confidence >= 85%)
- [x] Document when agents MAY still use judgment (confidence 70-84%)
- [x] Update skill-selection.yaml (skill-registry.yaml) with clear/unclear trigger distinction

### Impact
This change eliminates subjective threshold overrides for clear triggers (85%+ confidence), ensuring that high-confidence skill selections are automatically invoked without agent discretion. This improves automation and reduces decision latency for clear-cut cases.

## Implementation Summary

### Files Updated

1. **`004-phase-1-5-skill-check.md`**
   - Already correctly stated "MUST invoke" for clear triggers
   - No changes needed

2. **`CLAUDE.md` Phase 1.5 section**
   - Already correctly documented "MUST invoke" for >=85% confidence
   - Already documented "SHOULD invoke" for 70-84% confidence
   - Already documented "MAY check" for <70% confidence
   - No changes needed

3. **`skill-registry.yaml` selection_framework.auto_trigger_rules**
   - Updated ATR-004 (Decision Questions): `action: "MUST invoke superintelligence-protocol skill"` (was "MUST check")
   - Updated ATR-005 (Product Management Tasks): `action: "MUST invoke bmad-pm skill"` (was "MUST check")

### Changes Made

```yaml
# Before:
  - rule_id: ATR-004
    name: Decision Questions
    action: MUST check superintelligence-protocol skill
    priority: critical
    trigger_type: clear

# After:
  - rule_id: ATR-004
    name: Decision Questions
    action: MUST invoke superintelligence-protocol skill  # Changed
    priority: critical
    trigger_type: clear
```

```yaml
# Before:
  - rule_id: ATR-005
    name: Product Management Tasks
    action: MUST check bmad-pm skill
    priority: high
    trigger_type: clear

# After:
  - rule_id: ATR-005
    name: Product Management Tasks
    action: MUST invoke bmad-pm skill  # Changed
    priority: high
    trigger_type: clear
```

### Confidence Thresholds Already Defined

The skill-registry.yaml already has the thresholds defined:
- `clear_trigger_threshold: 85` (MUST invoke, no override)
- `discretionary_threshold: 70` (SHOULD invoke, agent discretion)
- Below 70: MAY check (optional invocation)

### All Success Criteria Met

- [x] Update rule 004-phase-1-5-skill-check.md to say "MUST invoke" for clear triggers
- [x] Update CLAUDE.md skill selection section with same change
- [x] Define "clear triggers" explicitly (confidence >= 85%)
- [x] Document when agents MAY still use judgment (confidence 70-84%)
- [x] Update skill-selection.yaml with clear/unclear trigger distinction
