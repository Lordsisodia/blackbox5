# TASK-FIX-SKIL-018-4: Add Skill Override Documentation Workflow

**Status:** pending
**Priority:** MEDIUM
**Category:** skills
**Estimated Effort:** 30 minutes
**Created:** 2026-02-09
**Parent Task:** TASK-SKIL-018

---

## Objective

Create a documentation workflow that requires agents to justify skill overrides, creating an audit trail for improving trigger accuracy over time.

---

## Success Criteria

- [ ] Create `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.templates/skill-override-justification.md`
- [ ] Update rule 004-phase-1-5-skill-check.md with override documentation requirement
- [ ] Update CLAUDE.md with override justification workflow
- [ ] Create `bb5 skill:override-log` command to view override history
- [ ] Add override analysis to skill-metrics.yaml
- [ ] Document common override patterns and their validity

---

## Context

**Root Cause Identified:**
Agents override thresholds subjectively with no documentation or audit trail.

**Current Behavior:**
1. Agent calculates 75% confidence
2. Agent decides "I don't need this skill"
3. No record of why override occurred
4. No data to improve trigger accuracy

**Desired Behavior:**
1. Agent calculates 75% confidence
2. Agent must document justification in THOUGHTS.md
3. Justification logged to skill-metrics.yaml
4. Periodic analysis of overrides to improve triggers

---

## Files to Create/Modify

### New Files

1. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.templates/skill-override-justification.md`
   - Template for override justification
   - Required fields: reason, confidence, expected_outcome

2. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/bb5-skill-override-log`
   - CLI command to view override history
   - Filter by skill, date, or validity

### Modified Files

3. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.claude/rules/004-phase-1-5-skill-check.md`
   - Add override documentation requirement
   - Specify required fields for justification

4. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.claude/CLAUDE.md`
   - Add override workflow section
   - Document analysis process

5. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-metrics.yaml`
   - Add override_analysis section
   - Track patterns and outcomes

---

## Approach

1. Design override justification template
2. Update skill-check rule with documentation requirement
3. Create CLI command for viewing override log
4. Add override analysis to metrics
5. Document common valid/invalid override patterns
6. Create process for periodic override review

---

## Override Justification Template

**File:** `.templates/skill-override-justification.md`

```markdown
## Skill Override Justification

**Task ID:** [TASK-XXX]
**Timestamp:** [YYYY-MM-DD HH:MM]
**Skill Recommended:** [skill-name]
**Confidence Score:** [XX%]
**Trigger Type:** [clear/discretionary/none]

### Override Reason

[Required: Explain why skill is not being invoked despite recommendation]

### Confidence Assessment

[Required: Why is the confidence calculation wrong or misleading?]

### Expected Outcome

[Required: What will happen without the skill?]

### Risk Acknowledgment

[Required: What could go wrong by not using the skill?]

---

**Valid Override Patterns:**
- [ ] Simple documentation typo fix
- [ ] One-line configuration change
- [ ] Emergency hotfix (speed critical)
- [ ] Skill content already known/memorized
- [ ] Task is skill maintenance itself

**Invalid Override Patterns:**
- [ ] "I can handle this" (no specific reason)
- [ ] "It will be faster" (without risk assessment)
- [ ] "The skill is wrong" (without explaining why)
- [ ] No justification provided
```

---

## Override Log Analysis

**Metrics to Track:**

```yaml
override_analysis:
  total_overrides: 150
  by_skill:
    git-commit:
      overrides: 25
      valid: 20
      invalid: 5
      common_reason: "Simple one-line fix"
    bmad-architect:
      overrides: 10
      valid: 3
      invalid: 7
      common_reason: "I understand the architecture"

  validity_patterns:
    valid:
      - "Simple documentation typo fix"
      - "One-line configuration change"
      - "Emergency hotfix"
    invalid:
      - "I can handle this"
      - "It will be faster"
      - "Skill not needed"

  improvement_recommendations:
    - skill: bmad-architect
      issue: Agents override architecture skill frequently
      suggestion: Increase clear trigger threshold to 90%
      expected_impact: Reduce invalid overrides by 50%
```

---

## Rollback Strategy

If workflow is too burdensome:
1. Simplify justification template
2. Reduce required fields
3. Document learnings and adjust

---

## Notes

**Override Review Process (Monthly):**

1. Run `bb5 skill:override-log --last-month`
2. Categorize each override as valid/invalid
3. Identify patterns in invalid overrides
4. Adjust trigger rules to reduce invalid overrides
5. Update skill-selection.yaml with learnings

**Integration with Continuous Improvement:**

- Override data feeds into skill system improvement
- Part of every-5-runs first principles review
- Used to refine confidence calculation formula
- Triggers updates to skill-selection.yaml

**Example Valid Override:**
```markdown
## Skill Override Justification

**Task:** Fix typo in README.md
**Skill Recommended:** git-commit (confidence: 72%)
**Override Reason:** Simple documentation typo fix - single character change
**Confidence Assessment:** Triggered because "commit" keyword present, but no actual git workflow needed
**Expected Outcome:** Direct file edit, no commit strategy needed
**Risk:** None - trivial change
```

**Example Invalid Override:**
```markdown
## Skill Override Justification

**Task:** Implement user authentication
**Skill Recommended:** bmad-architect (confidence: 88%)
**Override Reason:** I can handle this
**Confidence Assessment:** [Missing]
**Expected Outcome:** [Missing]
**Risk:** [Missing]

# FLAGGED: Insufficient justification for clear trigger override
```
