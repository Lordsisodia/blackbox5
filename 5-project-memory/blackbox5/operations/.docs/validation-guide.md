# Pre-Execution Validation Guide

**Location:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/validation-checklist.yaml`

## Purpose

Prevent wasted work on duplicate tasks and invalid assumptions by running a standardized set of checks before starting any task execution.

## Quick Reference

### Run Full Validation

```bash
# Source the validation functions
source ~/.blackbox5/5-project-memory/blackbox5/bin/validate-task

# Run validation for a task file
validate-task ~/.blackbox5/5-project-memory/blackbox5/.autonomous/tasks/active/TASK-xxx.md
```

### Quick Checks

```bash
# Check for duplicate tasks
grep -r "keyword" ~/.blackbox5/5-project-memory/blackbox5/.autonomous/tasks/completed/

# Check recent commits
cd ~/.blackbox5 && git log --oneline --since="1 week ago" | grep -i "keyword"

# Verify paths exist
ls -la /path/to/check
```

## Validation Checks

### Required Checks (Must Pass)

| Check | Description | Fail Action |
|-------|-------------|-------------|
| `duplicate_task_check` | Search completed/ for similar tasks | abort |
| `path_validation` | Verify all referenced paths exist | warn |
| `active_tasks_check` | Ensure active tasks exist | warn |

### Optional Checks (Warnings Only)

| Check | Description | Fail Action |
|-------|-------------|-------------|
| `state_freshness` | Check if state is stale (> 7 days) | warn |
| `recent_commits_check` | Check for recent similar commits | warn |
| `file_history_check` | Check recent changes to target files | warn |

## Assumption Validation

When a task contains assumptions, validate them:

| Assumption Type | Pattern | Validation Required |
|-----------------|---------|---------------------|
| File existence | "assumes.*exists" | Verify file exists before proceeding |
| State freshness | "assumes.*state" | Check STATE.yaml timestamp |
| Dependency | "assumes.*dependency" | Verify dependency availability |
| API availability | "assumes.*api" | Test API connectivity |

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | All required checks passed | Proceed with task |
| 1 | Warnings present | Review but may proceed |
| 2 | Critical check failed | Abort task execution |

## Workflow

### For Task Executors (RALF-Executor)

1. **Before starting any task:**
   - Read the task file completely
   - Extract keywords from title/objective
   - Run duplicate task check
   - Verify target paths exist

2. **If duplicate found:**
   - Read the completed task
   - Determine: Skip, Continue, or Merge
   - Report to Planner if uncertain

3. **Document validation:**
   - Record checks performed in THOUGHTS.md
   - Note any assumptions validated
   - Include validation result in RESULTS.md

### Example Validation Log

```yaml
# In validation-checklist.yaml usage_log:
- timestamp: "2026-02-01T12:00:00Z"
  task_id: "TASK-123"
  checks_performed:
    - duplicate_task_check: passed
    - path_validation: passed
    - recent_commits_check: warning
  assumptions_validated:
    - file_existence: verified
  result: proceed_with_caution
  notes: "Similar commit found last week, but different approach"
```

## Integration with Task Execution

### Step 1: Pre-Execution Verification (from RALF-Executor)

```bash
# 1. Check for duplicate tasks in completed/
grep -r "[task keyword]" $RALF_PROJECT_DIR/.autonomous/tasks/completed/ 2>/dev/null | head -3
grep -r "[task keyword]" $RALF_PROJECT_DIR/tasks/completed/ 2>/dev/null | head -3

# 2. Check recent commits
cd ~/.blackbox5 && git log --oneline --since="1 week ago" | grep -i "[keyword]" | head -3

# 3. Verify target files exist
ls -la [target paths] 2>/dev/null

# 4. Check file history
git log --oneline --since="1 week ago" -- [target paths] | head -3
```

### Step 2: Handle Duplicate Found

```bash
# If duplicate found:
# - Read the completed task
# - Determine: Skip? Continue? Merge?
# - Report to Planner via chat-log.yaml
# - Do NOT create redundant work
```

## Validation Report Example

```markdown
# Validation Report

**Task:** TASK-1769892004
**Timestamp:** 2026-02-01T06:00:00Z
**Validator:** RALF-Executor

## Checks Performed

| Check | Status | Required | Action |
|-------|--------|----------|--------|
| Duplicate Task Check | passed | true | proceed |
| Path Validation | passed | true | proceed |
| Recent Commits Check | warning | false | review |
| State Freshness | passed | false | proceed |

## Assumptions Validated

| Assumption | Validated | Method |
|------------|-----------|--------|
| bin/verify-task exists | yes | ls -la |
| .templates/tasks/ exists | yes | ls -la |

## Result

**Status:** passed_with_warnings
**Proceed:** yes

Similar work found in commit b44cc53 but different scope.
```

## Automation Roadmap

### Phase 1: Manual (Current)
- Hand-run checks before task execution
- Document validation in THOUGHTS.md

### Phase 2: Semi-Automated
- Wrapper script runs standard checks
- Auto-generates validation report
- Integration with Executor workflow

### Phase 3: Fully Automated
- Pre-commit hooks run validation
- Automatic duplicate detection
- Smart assumption extraction and validation

## Related Files

- `operations/skill-usage.yaml` - Skill tracking
- `.templates/tasks/task-specification.md.template` - Task template with validation section
- `CLAUDE.md` - User instructions with decision framework
