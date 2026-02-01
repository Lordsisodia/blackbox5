# Plan Validation Guide

**Version:** 1.0
**Author:** RALF-Executor (TASK-1769913001)
**Created:** 2026-02-01

---

## Overview

The Plan Validation System prevents wasted effort on invalid or stale plans by automatically checking them before execution. This ensures plans are:

- **File-valid**: All referenced files exist
- **Problem-relevant**: The problem statement is still applicable
- **Dependency-sound**: No circular or missing dependencies
- **Current**: Plans are not outdated (> 30 days)

---

## Problem Solved

**Before Plan Validation:**
- Plans referenced non-existent code
- Problems described already-resolved issues
- No validation before execution started
- Executors wasted time on invalid plans

**After Plan Validation:**
- Automatic validation catches issues early
- Invalid plans blocked before execution
- Clear error messages guide fixes
- Stale plans flagged for review

---

## How It Works

### Validation Flow

```
Plan Created → Validation Check → Approval → Ready to Start
                           ↓
                    [If Invalid]
                           ↓
                    Block + Report Error
```

### Validation Checks

#### 1. File Existence (CRITICAL)
- **What**: Checks all files referenced in `plan.md` exist
- **How**: Parses code blocks and text for file paths
- **Failure**: Blocks plan from approval

#### 2. Problem Statement (WARNING)
- **What**: Checks if problem might already be resolved
- **How**: Looks for "resolved" keywords (implemented, fixed, etc.)
- **Failure**: Warns for manual review

#### 3. Dependencies (CRITICAL/WARNING)
- **What**: Validates dependency references
- **How**: Cross-checks against STATE.yaml
- **Failure**: Error for self-dependency, warning for missing deps

#### 4. Plan Age (WARNING)
- **What**: Warns if plan hasn't been updated recently
- **How**: Checks file modification time
- **Failure**: Warning if > 30 days old

---

## Usage

### Command Line

**Validate a single plan:**
```bash
python3 2-engine/.autonomous/lib/plan_validator.py \
  --project-root /workspaces/blackbox5 \
  6-roadmap/03-planned/PLAN-003-implement-planning-agent/plan.md
```

**Validate all ready_to_start plans:**
```bash
python3 2-engine/.autonomous/lib/plan_validator.py \
  --project-root /workspaces/blackbox5 \
  --all
```

**JSON output:**
```bash
python3 2-engine/.autonomous/lib/plan_validator.py \
  --project-root /workspaces/blackbox5 \
  --json \
  PLAN-003/plan.md
```

### Python API

```python
from pathlib import Path
from lib.plan_validator import PlanValidator

# Initialize validator
validator = PlanValidator(
    project_root=Path("/workspaces/blackbox5"),
    roadmap_path=Path("/workspaces/blackbox5/6-roadmap/STATE.yaml")
)

# Validate a plan
result = validator.validate_plan_file(
    Path("6-roadmap/03-planned/PLAN-003/plan.md")
)

if result["valid"]:
    print("✅ Plan is valid")
else:
    print("❌ Plan has errors:")
    for error in result["errors"]:
        print(f"  - {error}")
```

---

## Validation Rules

### Critical (Block Execution)

| Rule | Description | Example |
|------|-------------|---------|
| **File Existence** | All `files_to_change` must exist | Referenced `src/metrics.py` not found |
| **No Self-Dependency** | Plan cannot depend on itself | PLAN-003 depends on PLAN-003 |
| **No Circular Dependencies** | No dependency loops | PLAN-001 → PLAN-002 → PLAN-001 |

### Warnings (Review Required)

| Rule | Description | Example |
|------|-------------|---------|
| **Stale Problem** | Problem may already be solved | Problem says "X not implemented" but X exists |
| **Old Plan** | Plan not updated recently | Plan is 45 days old |
| **Missing Dependency** | Dependency not in STATE.yaml | Depends on PLAN-999 (not found) |

---

## Integration Points

### Planner Integration

**Before queuing a task:**
```python
# In planner workflow
validator = PlanValidator()
result = validator.validate_plan_file(plan_path)

if not result["valid"]:
    # Don't create task for invalid plan
    log_validation_failure(result)
    skip_plan()
```

**Before marking ready_to_start:**
```python
# In plan approval workflow
result = validator.validate_plan_file(plan_path)

if result["valid"]:
    update_state("ready_to_start", plan_id)
else:
    notify_planner(result["errors"])
    keep_status("planned")
```

### Executor Integration

**Before execution:**
```python
# In executor task claim
task_plan = get_plan_from_task(task)
result = validator.validate_plan_file(task_plan)

if not result["valid"]:
    # Skip task, report to planner
    report_invalid_plan(result)
    skip_task()
```

---

## Output Format

### Valid Plan
```
=== Plan Validation Results ===

Plan 1: PLAN-003 - Implement Planning Agent
Status: ✅ VALID

⚠️  WARNINGS:
  - Plan is 25 days old (last updated 2026-01-07). Consider review.
```

### Invalid Plan
```
=== Plan Validation Results ===

Plan 1: PLAN-003 - Implement Planning Agent
Status: ❌ INVALID

❌ ERRORS:
  - Referenced file does not exist: src/agents/PlanningAgent.py
  - Plan depends on itself: PLAN-003

⚠️  WARNINGS:
  - Problem statement may describe already-resolved issue: 'Planning system already exists...'
  - Dependency not found in STATE.yaml: PLAN-999
```

### JSON Output
```json
[
  {
    "valid": false,
    "errors": [
      "Referenced file does not exist: src/agents/PlanningAgent.py"
    ],
    "warnings": [
      "Plan is 45 days old"
    ],
    "plan_id": "PLAN-003",
    "plan_name": "Implement Planning Agent",
    "file_checked": "/path/to/plan.md"
  }
]
```

---

## Best Practices

### For Plan Authors

1. **Verify file paths**: Ensure all referenced files exist
2. **Update problem statements**: Keep problem descriptions current
3. **Check dependencies**: Validate dependency IDs are correct
4. **Update regularly**: Refresh plan if > 30 days old

### For Planner

1. **Run validation**: Always validate before approval
2. **Review warnings**: Even valid plans may have warnings
3. **Fix or block**: Don't approve invalid plans
4. **Update STATE.yaml**: Keep dependency references current

### For Executor

1. **Check validation**: Verify plan validity before starting
2. **Report issues**: Flag invalid plans to planner
3. **Skip gracefully**: Don't fail on invalid plans, just skip

---

## Troubleshooting

### Validator reports file doesn't exist (but it does)

**Cause**: File path in plan.md doesn't match actual location

**Solution**:
- Check file path is relative to project root
- Remove leading slashes from paths
- Use correct directory structure

### Validator says dependency not found

**Cause**: Dependency ID incorrect or not in STATE.yaml

**Solution**:
- Verify dependency ID format (PLAN-XXX)
- Check STATE.yaml for dependency entry
- Update plan with correct dependency

### Problem statement warning (may be resolved)

**Cause**: Problem statement contains "resolved" keywords

**Solution**:
- Review actual problem (still exists?)
- Update problem statement if resolved
- Mark plan as completed if appropriate

---

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | All plans valid | Proceed |
| 1 | Validation failed | Block/fix |
| 2 | Plan file not found | Check path |
| 3 | STATE.yaml not found | Update config |

---

## Related Documentation

- **Plan Template**: `6-roadmap/templates/plan-template.md`
- **STATE.yaml Reference**: `6-roadmap/.docs/STATE-structure.md`
- **Workflow Integration**: `2-engine/.autonomous/workflows/plan-approval.yaml`

---

## Changelog

### v1.0 (2026-02-01)
- Initial implementation
- File existence validation
- Problem statement checking
- Dependency validation
- Plan age warnings
- CLI and Python API
