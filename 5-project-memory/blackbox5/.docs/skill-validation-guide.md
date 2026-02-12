# Skill Validation Guide

## Overview

The Skill Validation System enables post-task evaluation of skill decisions to improve trigger accuracy over time. By recording whether skill invocations (or overrides) were correct, the system can calculate and refine `trigger_accuracy` metrics for each skill.

## Why Skill Validation Matters

**Problem:**
- Skills have `trigger_accuracy` metrics that were always at 0.0%
- No mechanism existed to evaluate if skill decisions were correct
- Continuous improvement of skill triggers was impossible

**Solution:**
- Post-task validation workflow to assess skill decision quality
- Automated calculation of `trigger_accuracy` based on validation data
- Evidence-based refinement of confidence thresholds and trigger keywords

## Validation Workflow

### 1. Before Task Execution (Pre-Task)

When a task requires a skill decision:

1. **Check for applicable skills** (Phase 1.5 skill checking)
2. **Calculate confidence score** based on keywords and context
3. **Make decision:**
   - **Clear trigger (≥85%):** MUST invoke skill
   - **Discretionary (70-84%):** SHOULD invoke skill (can override with justification)
   - **Low confidence (<70%):** MAY check skill

4. **Document decision in THOUGHTS.md:**
   ```markdown
   ## Skill Usage for This Task
   - Applicable skills: git-commit (87%)
   - Skill invoked: Yes
   - Rationale: Clear trigger - task requires git commit workflow
   ```

5. **If overriding discretionary trigger:**
   - Create override justification: `cp .templates/skill-override-justification.md ./skill-override-justification.md`
   - Fill out all required fields

### 2. After Task Completion (Post-Task)

When task is complete, validate the skill decision:

1. **Copy validation template:**
   ```bash
   cp .templates/skill-validation-post-task.md ./skill-validation.md
   ```

2. **Fill out required fields:**
   - **Task outcome** - Was the task completed successfully?
   - **Skill effectiveness** - Did the skill help, hinder, or have no impact?
   - **Decision type** - CORRECT, INCORRECT, PARTIAL, or UNCLEAR
   - **Detailed rationale** - Evidence for your assessment

3. **Record validation:**
   ```bash
   bb5 skill:validate --file ./skill-validation.md
   ```

   Or manually:
   ```bash
   bb5 skill:validate --task TASK-ID --skill SKILL-NAME --decision CORRECT
   ```

4. **Review trigger accuracy:**
   ```bash
   bb5 skill:validate --by-skill SKILL-NAME
   bb5 skill:validate --summary
   ```

## Decision Types

### CORRECT
**The skill decision was the right choice.**

**Criteria:**
- Task completed successfully
- Skill contributed positively to outcome
- No better alternative would have been better

**Example:**
```
Skill: git-commit (87% confidence)
Decision: Invoked skill
Validation: CORRECT

Rationale:
Task was "implement git commit workflow for feature branch". Skill provided
complete commit message structure, branch naming, and push workflow. Completed
in 5 minutes with no errors. Without skill, would have taken 15 minutes.
```

### INCORRECT
**The skill decision was wrong.**

**Criteria:**
- Wrong skill was invoked (should have used different skill or none)
- Override was incorrect (should have invoked the skill)
- Task was hindered or required rework due to bad decision

**Example:**
```
Skill: bmad-architect (72% confidence)
Decision: Override (reason: "I can handle this")
Validation: INCORRECT

Rationale:
Task was "design authentication system for multi-tenant app". Override
justification was insufficient. Implementation had critical flaws:
- No token rotation consideration
- Missing rate limiting architecture
- Incorrect session management

Result: Complete redesign required (2 days). Skill would have caught these issues.
```

### PARTIAL
**The skill helped but wasn't optimal.**

**Criteria:**
- Skill provided some benefit
- Better approach would have been more effective
- Learnings for skill improvement identified

**Example:**
```
Skill: test-generator (78% confidence)
Decision: Invoked skill
Validation: PARTIAL

Rationale:
Skill generated basic unit tests for API endpoints, which was helpful.
However:
- Tests didn't cover edge cases
- No integration tests for multi-endpoint workflows
- Missing performance tests
- Test coverage only 45% vs target 70%

Result: Tests provided basic safety but missed 3 bugs in production.
Combined approach (skill + manual) would have been better.
```

### UNCLEAR
**Cannot determine if decision was correct.**

**Criteria:**
- Insufficient evidence to assess
- Task outcome is ambiguous
- Requires more information to evaluate

**Example:**
```
Skill: bmad-analyst (65% confidence)
Decision: Did not invoke skill (low confidence)
Validation: UNCLEAR

Rationale:
Task was "analyze user feedback from beta test". Analysis was completed
manually, but without baseline comparison it's unclear if the skill would
have improved quality. Need to run similar task with skill invoked for
comparison.
```

## Trigger Accuracy Calculation

```
trigger_accuracy = (correct + 0.5 * partial) / (total - unclear) * 100
```

**Components:**
- **correct** - Number of CORRECT validations
- **partial** - Number of PARTIAL validations (weighted at 0.5)
- **unclear** - Number of UNCLEAR validations (excluded from denominator)
- **total** - Total number of validations

**Interpretation:**
- **>80%** - Skill triggers are highly accurate, consider increasing confidence threshold
- **60-80%** - Acceptable accuracy, monitor trends
- **<60%** - Low accuracy, consider decreasing threshold or improving skill content
- **<40%** - Critical issue, immediate attention required

## CLI Tool Usage

### Record a Validation
```bash
bb5 skill:validate --task TASK-SKIL-018 --skill git-commit --decision CORRECT
```

### Record with Validation File
```bash
bb5 skill:validate --file ./skill-validation.md
```

### View Summary Statistics
```bash
bb5 skill:validate --summary
```

### View Specific Skill Validations
```bash
bb5 skill:validate --by-skill bmad-pm
```

### Export to CSV
```bash
bb5 skill:validate --export validations.csv
```

### Full Help
```bash
bb5 skill:validate --help
```

## Continuous Improvement

### Weekly Review Process

1. **Run summary:**
   ```bash
   bb5 skill:validate --summary
   ```

2. **Review low-accuracy skills** (<60%):
   - Analyze INCORRECT validations
   - Identify patterns in bad decisions
   - Review trigger keywords and confidence thresholds

3. **Adjust skill triggers:**
   - Increase confidence threshold if accuracy >80%
   - Decrease confidence threshold if accuracy <60%
   - Add/remove trigger keywords based on patterns

4. **Update skill content** (if needed):
   - Improve guidance based on PARTIAL validations
   - Add examples from CORRECT validations
   - Fix issues identified in INCORRECT validations

5. **Document changes:**
   - Update `skill-registry.yaml`
   - Note rationale in skill documentation
   - Communicate changes to team

### Monthly Deep-Dive

1. **Export full validation history:**
   ```bash
   bb5 skill:validate --export validations-$(date +%Y%m).csv
   ```

2. **Analyze trends:**
   - Accuracy trends over time
   - Most common decision types by skill
   - Skills needing most improvement

3. **Identify systemic issues:**
   - Recurring override patterns
   - Conflicting skill recommendations
   - Missing skill coverage

4. **Plan improvements:**
   - Create tasks for skill updates
   - Prioritize high-impact fixes
   - Schedule implementation

## Integration Points

### With Skill Checking (Phase 1.5)
- Skill checking rule now requires post-task validation
- Both pre-task (check) and post-task (validate) are documented

### With Task Completion Workflow
- Validation is part of task completion checklist
- `validate-task-completion.sh` can check for validation files

### With Skill Registry
- `skill-registry.yaml` stores validation history and metrics
- `trigger_accuracy` metric automatically calculated from validations

### With Autonomous Systems
- RALF can auto-validate based on task outcomes
- Patterns in validations can trigger automatic threshold adjustments

## Best Practices

### 1. Validate Consistently
- Validate EVERY task where a skill decision was made
- Don't skip validation for "simple" tasks - all data is valuable
- If truly impossible to validate, use UNCLEAR with explanation

### 2. Be Honest in Assessments
- Don't inflate CORRECT counts to make metrics look good
- Acknowledge INCORRECT decisions - they're learning opportunities
- Use PARTIAL for nuanced cases where something worked but could be better

### 3. Provide Detailed Rationale
- The rationale is more valuable than the decision type alone
- Explain WHY the decision was correct/incorrect/partial
- Include specific evidence from the task execution

### 4. Use High Validation Confidence
- Only use LOW confidence when truly uncertain
- Most validations should be HIGH or MEDIUM confidence
- Low-confidence validations are excluded from some analyses

### 5. Review and Act
- Don't just record validations - review them regularly
- Take action on patterns identified in INCORRECT validations
- Update skills and triggers based on evidence

## Troubleshooting

### Skill Not Found
```
Error: Skill 'git-commit' not found in skill-registry.yaml
```
**Solution:** Check available skills with:
```bash
python3 -c "import yaml; data = yaml.safe_load(open('/opt/blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml')); print('\n'.join(data['skills'].keys()))"
```

### Validation File Parsing Errors
```
Error: Could not extract required fields from validation file
```
**Solution:** Ensure validation file has:
- Task ID (`**Task ID:** TASK-XXX`)
- Skill Recommended (`**Skill Recommended:** skill-name`)
- Decision type (checkbox checked for CORRECT/INCORRECT/PARTIAL/UNCLEAR)

### Trigger Accuracy Not Updating
**Solution:** Check that:
- Validation was recorded successfully (check output)
- Validation decision type is one of the four valid types
- Skill has validations recorded (`bb5 skill:validate --by-skill SKILL-NAME`)

## Examples

### Example 1: Simple CORRECT Validation
**Task:** Fix typo in README.md
**Skill:** git-commit (72%)
**Decision:** Override (simple fix, no commit needed)
**Validation:** INCORRECT

**Learnings:** Even simple fixes should use git workflow for consistency

### Example 2: Complex PARTIAL Validation
**Task:** Implement REST API for user management
**Skill:** bmad-dev (85%)
**Decision:** Invoked
**Validation:** PARTIAL

**Learnings:** Skill provided good structure but missed rate limiting. Add rate limiting guidance to skill.

### Example 3: Systematic INCORRECT Pattern
**Observation:** 5 INCORRECT validations for `bmad-architect` with confidence 70-74%
**Pattern:** All involved "design authentication" tasks
**Action:** Add "authentication" as high-weight keyword for architecture skill
**Result:** Accuracy improved from 45% to 75% after threshold adjustment

## Files

- **Template:** `.templates/skill-validation-post-task.md`
- **CLI Tool:** `bin/bb5-skill-validate`
- **Rule:** `.claude/rules/004-phase-1-5-skill-check.md` (includes validation requirement)
- **Registry:** `operations/skill-registry.yaml` (stores validation data)
- **Guide:** `.docs/skill-validation-guide.md` (this file)

## Support

For questions or issues:
1. Check this guide first
2. Review examples in `.templates/skill-validation-post-task.md`
3. Run `bb5 skill:validate --help`
4. Check recent validations for patterns: `bb5 skill:validate --summary`
