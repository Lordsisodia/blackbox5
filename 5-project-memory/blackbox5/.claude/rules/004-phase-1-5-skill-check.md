---
name: Phase 1.5 Skill Checking
trigger:
  - before execution
  - phase 2
  - implement
  - analyze
  - refactor
alwaysApply: true
priority: 95
---

# Phase 1.5: Mandatory Skill Checking

## Rule
BEFORE starting Phase 2 (Execution) of ANY task, you MUST check for applicable skills and invoke when confidence is clear.

## Confidence Thresholds

### Clear Triggers (MUST Invoke - No Override)
**Confidence >= 85%**
When confidence is 85% or higher, you MUST invoke the skill. No subjective judgment allowed.

**Examples:**
- "implement" + exact domain match (e.g., "implement git commit")
- "Should we..." + architecture keyword
- "PRD" + feature definition

### Discretionary Triggers (SHOULD Invoke - Agent Judgment)
**Confidence 70-84%**
When confidence is between 70-84%, you SHOULD invoke the skill but may use judgment.

**Examples:**
- "implement" + related domain
- "analyze" + partial match
- "test" + unclear scope

### Low Confidence (MAY Check - Agent Discretion)
**Confidence < 70%**
When confidence is below 70%, you MAY check the skill but invocation is optional.

## Process
1. Read `skill-selection.yaml` at `~/.blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml` (section: selection_framework)
2. Check `domain_mapping` for matching keywords in your task
3. Calculate confidence using the formula in the file
4. **If confidence >= 85% (Clear Trigger): MUST invoke skill** - no override allowed
5. **If confidence 70-84% (Discretionary): SHOULD invoke skill** - agent judgment allowed
   - If you choose to override: **MUST document justification using template**
   - Copy `.templates/skill-override-justification.md` to task folder
   - Fill out all required fields
6. **If confidence < 70%: MAY check skill** - invocation optional

## Documentation
Document in THOUGHTS.md under "## Skill Usage for This Task":
- Applicable skills found (or "None")
- Skill invoked (or "None")
- Confidence percentage
- Rationale for decision (especially if discretion was used)

## Override Documentation Requirement
**For discretionary triggers (70-84% confidence) where you choose NOT to invoke the skill:**

1. Copy the override template:
   ```bash
   cp .templates/skill-override-justification.md ./skill-override-justification.md
   ```

2. Fill out ALL required fields:
   - Override Reason (specific explanation)
   - Confidence Assessment (why calculation is wrong)
   - Expected Outcome (what happens without skill)
   - Risk Acknowledgment (what could go wrong)

3. Mark validity in checklist:
   - If valid override: Check appropriate pattern
   - If invalid override: Explain why override should be reconsidered

4. Log to skill-registry.yaml (automatic via hook or manual):
   - See `skill-registry.yaml > override_analysis` section

**Override without justification = PROTOCOL VIOLATION**

## Post-Task Validation Requirement
**AFTER completing ANY task where a skill decision was made (invoked or overridden):**

You MUST validate whether the skill decision was correct to improve trigger accuracy over time.

### When to Validate

**MUST validate when:**
- A skill was invoked (whether clear or discretionary trigger)
- A discretionary skill was overridden
- Task outcome provides clear evidence about skill quality

**MAY validate when:**
- Low confidence trigger (<70%) and skill was not used
- Task outcome is ambiguous
- Task was abandoned/cancelled

### Validation Process

1. Copy the validation template:
   ```bash
   cp .templates/skill-validation-post-task.md ./skill-validation.md
   ```

2. Fill out ALL required fields:
   - Task outcome documented
   - Skill effectiveness assessed (helped/hindered/no impact)
   - Decision type: CORRECT, INCORRECT, PARTIAL, or UNCLEAR
   - Detailed rationale provided (evidence for your assessment)

3. Record validation in skill registry:
   ```bash
   bb5 skill:validate --file ./skill-validation.md
   ```
   Or manually:
   ```bash
   bb5 skill:validate --task TASK-ID --skill SKILL-NAME --decision CORRECT
   ```

4. Review trigger accuracy trends:
   ```bash
   bb5 skill:validate --by-skill SKILL-NAME
   bb5 skill:validate --summary
   ```

### Decision Types

**CORRECT** - Skill decision was the right choice:
- Task completed successfully
- Skill contributed positively to outcome
- No better alternative would have been better

**INCORRECT** - Skill decision was wrong:
- Wrong skill was invoked (should have used different skill or none)
- Override was incorrect (should have invoked the skill)
- Task was hindered or required rework due to bad decision

**PARTIAL** - Skill helped but wasn't optimal:
- Skill provided some benefit
- Better approach would have been more effective
- Learnings for skill improvement identified

**UNCLEAR** - Cannot determine:
- Insufficient evidence to assess
- Task outcome ambiguous
- Requires more information

### Impact of Validation

Validations directly improve the skill system:

1. **Trigger Accuracy Calculation:**
   ```
   trigger_accuracy = (correct + 0.5 * partial) / (total - unclear) * 100
   ```

2. **Skill Recommendations:**
   - High trigger_accuracy (>80%) → Increase confidence threshold
   - Low trigger_accuracy (<60%) → Decrease threshold or improve skill content

3. **Continuous Improvement:**
   - Track trends over time
   - Identify patterns in incorrect decisions
   - Refine trigger keywords and confidence thresholds

**Validation Failure = Missed Improvement Opportunity**

### Validation Checklist

Before marking a task as complete, ensure:
- [ ] Skill decision documented in THOUGHTS.md (before execution)
- [ ] Override justification created (if skill was overridden)
- [ ] Post-task validation created (after task completion)
- [ ] Validation recorded in skill-registry.yaml
- [ ] Trigger accuracy reviewed for trends

## Auto-Trigger Rules

| Trigger Condition | Confidence Level | Action | Override Allowed |
|-------------------|------------------|--------|------------------|
| "implement" + exact domain match (git commit, PR, etc.) | >= 85% | MUST invoke | NO |
| "Should we..." + architecture keyword | >= 85% | MUST invoke | NO |
| "PRD" + feature definition | >= 85% | MUST invoke | NO |
| "analyze" or "research" | 70-84% | SHOULD invoke | YES |
| "architecture", "design", "refactor" | 70-84% | SHOULD invoke | YES |
| "implement" + related domain | 70-84% | SHOULD invoke | YES |
| "test", "QA", "quality" | 70-84% | SHOULD invoke | YES |
| Multiple files or systems involved | 70-84% | SHOULD invoke | YES |
| General keyword match | < 70% | MAY check | YES |

## Important
- For clear triggers (>= 85%), invocation is MANDATORY - no judgment or override allowed
- For discretionary triggers (70-84%), use your best judgment based on task complexity
- Failure to check for applicable skills is a protocol violation

## Source
- CLAUDE.md Phase 1.5 section
- skill-registry.yaml (selection_framework section)
