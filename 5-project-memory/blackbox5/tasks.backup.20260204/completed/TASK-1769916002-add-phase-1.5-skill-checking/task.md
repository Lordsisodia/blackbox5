# TASK-1769916002: Add Phase 1.5 Skill Checking to Executor Prompt

**Type:** fix
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T12:43:00Z
**Source:** TASK-1769916000 Analysis

---

## Objective

Integrate the skill checking workflow into the executor prompt to close the gap between the skill framework (created in Run 24) and actual usage (0% invocation in Runs 30-40).

---

## Context

**Problem Identified (TASK-1769916000):**

The skill selection framework (skill-selection.yaml) is comprehensive and well-designed, BUT the executor prompt (v2-legacy-based.md) does NOT include the mandatory Phase 1.5 skill checking step. Executors are NOT instructed to check for skills before starting execution.

**Evidence:**
- Runs 30-40: 0% skill invocation rate (0/10 tasks)
- Runs 30-31: 20% skill consideration (voluntary, not required)
- Runs 32-40: 0% skill consideration (practice abandoned)
- Executor prompt missing Phase 1.5 workflow
- skill-selection.yaml says "Usage: Executors MUST check this file before starting Phase 2" but this requirement is not in the executor prompt

**Impact:**
- 13 runs of skill system work (Runs 22-35) not being utilized
- Complex tasks missing skill guidance (Runs 37-39)
- Quality issues in implementations that skills might have prevented
- Wasted investment in skill framework

**Root Cause:** Workflow integration failure
- Framework exists and is well-designed
- Executor prompt does not include Phase 1.5
- Executors have no instruction to check for skills

---

## Success Criteria

- [ ] Phase 1.5 added to executor prompt between Phase 1 and Phase 2
- [ ] Skill checking workflow documented (when, how, what threshold)
- [ ] THOUGHTS.md template includes "Skill Usage for This Task" section
- [ ] Validation checklist requires skill documentation
- [ ] Next 3 runs show 100% skill consideration rate

---

## Approach

### Step 1: Read Executor Prompt (5 min)
- Read `2-engine/.autonomous/prompts/system/executor/variations/v2-legacy-based.md`
- Identify where to insert Phase 1.5 (between Phase 1 and Phase 2)
- Understand current prompt structure

### Step 2: Insert Phase 1.5 (10 min)
Add new section between Phase 1 and Phase 2:

```markdown
## Phase 1.5: Skill Checking (MANDATORY)

**EVERY task MUST go through skill evaluation before execution.**

### Step 1: Check for Applicable Skills
```bash
# Read skill selection framework
cat "$RALF_PROJECT_DIR/operations/skill-selection.yaml"

# Check skill-usage.yaml for matching skills
cat "$RALF_PROJECT_DIR/operations/skill-usage.yaml"
```

### Step 2: Evaluate Skill Match
1. Match task type against domains in skill-selection.yaml
2. Check trigger keywords in task description
3. Calculate confidence using formula from skill-selection.yaml
4. Determine if confidence >= threshold

### Step 3: Make Decision
- **If confidence >= threshold:** Invoke the skill (read skill file from 2-engine/.autonomous/skills/)
- **If confidence < threshold:** Proceed with standard execution
- **If uncertain:** Ask Planner via chat-log.yaml

### Step 4: Document Decision
Add to THOUGHTS.md:
```markdown
## Skill Usage for This Task

**Applicable skills:** [list skills or 'None']
**Skill invoked:** [name or 'None']
**Confidence:** [percentage if calculated]
**Rationale:** [why skill was or wasn't used]
```

**Non-negotiable:** ALL tasks must have this section in THOUGHTS.md
```

### Step 3: Update THOUGHTS.md Template (3 min)
- Read `.templates/tasks/THOUGHTS.md.template`
- Add mandatory "Skill Usage for This Task" section
- Include fields: applicable skills, skill invoked, confidence, rationale

### Step 4: Update Validation Checklist (2 min)
- Add to executor prompt Phase 3 validation:
  - [ ] Skill evaluation completed (Phase 1.5)
  - [ ] "Skill Usage for This Task" section present in THOUGHTS.md
  - [ ] Decision rationale documented

### Step 5: Update Task Completion Template (optional, if time)
- Add skill tracking section to `.templates/tasks/task-completion.md.template`
- Ensure skill usage is tracked in task completion workflow

---

## Files to Modify

- `2-engine/.autonomous/prompts/system/executor/variations/v2-legacy-based.md`
  - Insert Phase 1.5 between Phase 1 and Phase 2
  - Add skill checking workflow
  - Update validation checklist

- `.templates/tasks/THOUGHTS.md.template`
  - Add "Skill Usage for This Task" section
  - Make it mandatory (not optional)

- `.templates/tasks/task-completion.md.template` (optional)
  - Ensure skill tracking section exists
  - Add to completion workflow

---

## Expected Outcomes

1. **100% skill consideration rate** - Every task will check for skills
2. **10-30% skill invocation rate** - Complex tasks will use skills
3. **Better code quality** - Skill guidance for complex implementations
4. **Faster execution** - Skills provide proven patterns and approaches

---

## Testing Plan

After implementation, verify with next 3 tasks:

**Run 45 (TASK-1769916002):**
- [ ] Phase 1.5 present in executor prompt
- [ ] THOUGHTS.md has "Skill Usage for This Task" section
- [ ] Skill evaluation documented

**Run 46 (next task):**
- [ ] Skills considered (even if not invoked)
- [ ] Decision documented in THOUGHTS.md
- [ ] Confidence calculated if applicable

**Run 47 (next task):**
- [ ] Same validation as Run 46
- [ ] Calculate consideration rate for 3 runs (target: 100%)

---

## Notes

**Priority:** HIGH - Critical bug fix
**Effort:** LOW (20 minutes) - Additive change, no breaking changes
**Risk:** LOW - Well-defined workflow, existing framework
**Impact:** HIGH - Unlocks skill system investment (13 runs of work)

**This is a BUG FIX, not a feature:**
- Framework exists (skill-selection.yaml)
- Workflow integration missing (executor prompt)
- Fix: Add Phase 1.5 to make skills usable

**Reversibility:** HIGH - Can remove Phase 1.5 if issues arise

---

## Related Work

- TASK-1769916000 (Run 44): Skill usage gap analysis - identified this bug
- TASK-1769909000 (Run 24): Created skill-selection.yaml framework
- TASK-1769909001 (Run 25): Incorrectly claimed "Phase 1.5 compliance confirmed"
- TASK-1769910000 (Run 20): Skill system recovery analysis
- TASK-1769911000 (Run 26): Confidence threshold tuning (80% → 70%)
- IMP-1769903003: Duplicate task detection (completed)

---

## Dependencies

None - standalone fix

---

## Estimated Time

20 minutes
- Step 1: 5 min (read executor prompt)
- Step 2: 10 min (insert Phase 1.5)
- Step 3: 3 min (update THOUGHTS.md template)
- Step 4: 2 min (update validation checklist)
