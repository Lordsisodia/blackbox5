# TASK-PROC-030: Validation Checklist Usage Log Implementation

**Type:** implement
**Priority:** medium
**Status:** in_progress
**Created:** 2026-02-06
**Estimated Effort:** 4-6 hours

## Objective

Implement validation checklist usage logging to track which checks are performed and their outcomes, creating an audit trail for validation compliance and enabling improvement of the validation process.

## Context

The `operations/validation-checklist.yaml` file defines pre-execution validation checks but currently has an empty `usage_log: []` array. This task implements a validation runner script that:

1. Executes validation checks from the checklist
2. Logs each validation run to the usage_log
3. Returns appropriate exit codes for workflow control
4. Integrates with the RALF executor workflow

## Success Criteria

### Must-Have (P0)
- [x] Create `/opt/blackbox5/bin/bb5-validate-task` script ✅ IMPLEMENTED
- [x] Implement all pre_execution checks from validation-checklist.yaml ✅ IMPLEMENTED
- [x] Log validation runs to usage_log in validation-checklist.yaml ✅ IMPLEMENTED
- [x] Return exit codes (0=passed, 1=warnings, 2=failed) ✅ IMPLEMENTED
- [x] Support task-specific validation (e.g., `bb5 validate TASK-XXX`) ✅ IMPLEMENTED
- [x] Validate YAML structure before logging ✅ IMPLEMENTED

### Should-Have (P1)
- [x] Quick validation mode for common checks ✅ IMPLEMENTED (--quick)
- [x] JSON output option for automation ✅ IMPLEMENTED (--output json)
- [x] Summary statistics from usage_log ✅ FIXED (timezone bug resolved)
- [ ] Integration with events.yaml
- [x] Command-line args to override required checks ✅ IMPLEMENTED (--check, --required-only)

### Nice-to-Have (P2)
- [ ] Interactive mode with prompts for missing info
- [ ] Validation report generation
- [ ] Integration with Claude context
- [ ] Web dashboard visualization

## Approach

### Phase 1: Audit Checklists (30 min)
1. Review validation-checklist.yaml structure
2. Verify check commands are valid
3. Document any gaps or missing checks

### Phase 2: Create Validation Script (90 min)
1. Create `bb5-validate-task` in `/opt/blackbox5/bin/`
2. Implement check execution with error handling
3. Add YAML parsing and output formatting
4. Handle exit codes correctly

### Phase 3: Implement Usage Logging (60 min)
1. Define log entry schema (timestamp, task_id, run_id, checks)
2. Implement YAML append with timestamp
3. Add metadata (validator, duration)

### Phase 4: Create Enforcement (90 min)
1. Modify executor workflow to call validation script
2. Handle exit codes for abort/warn/pass
3. Pass validation results to Claude context
4. Update events.yaml

### Phase 5: Test and Document (60 min)
1. Test with sample tasks
2. Verify integration with executor
3. Update documentation

## Files to Create/Modify

### New Files
- `/opt/blackbox5/bin/bb5-validate-task` - Main validation runner script (~400 lines)

### Modified Files
- `/opt/blackbox5/5-project-memory/blackbox5/operations/validation-checklist.yaml` - Usage logging
- `/opt/blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml` - Event logging

## Implementation Notes

**Log Entry Schema:**
```yaml
usage_log:
  - timestamp: "2026-02-06T12:00:00Z"
    task_id: "TASK-XXX"
    run_id: "run-0001"
    validator: "executor-v2"
    checks_performed:
      - check_id: "duplicate_task_check"
        status: "passed"
        required: true
        duration_seconds: 3.2
    overall_result: "passed"
    exit_code: 0
```

**Exit Codes:**
- `0` - All required checks passed, proceed with task
- `1` - Warnings present, review but may proceed
- `2` - Critical check failed, abort task execution

**Usage:**
```bash
# Full validation for a task
bb5 validate TASK-PROC-030

# Quick duplicate check
bb5 validate --quick --check duplicate_task_check TASK-PROC-030

# Show validation summary
bb5 validate --summary

# Validate specific paths
bb5 validate --paths /opt/blackbox5/2-engine/core/
```

## Dependencies

- PyYAML for YAML parsing
- Existing validation-checklist.yaml structure

## Notes

**2026-02-13 02:25 UTC - Timezone Bug Fixed**

Problem: The `--summary` function was using `datetime.utcnow()` which creates timezone-naive datetime objects, but when parsing timestamps from the usage_log, the code converted 'Z' suffix to '+00:00' creating timezone-aware datetimes. This caused potential comparison issues when filtering runs by time (e.g., "Last 24 hours").

Fix Applied:
1. Changed all `datetime.utcnow()` calls to `datetime.now(timezone.utc)`
2. Added `timezone` import to both Python sections of the script
3. Updated locations:
   - Line 149: Summary statistics "Last 24 hours" calculation
   - Line 284: Check execution start_time
   - Line 296: Duration calculation
   - Lines 360-361: Log entry timestamp and run_id

Result: Summary statistics now correctly filter validation runs by time using timezone-aware datetime objects consistently.

**Testing:**
```bash
$ bb5 validate --summary
[VALIDATE] Validation Summary

Total validation runs: 5
Last 24 hours: 5

Results:
  Passed:  0 (0.0%)
  Warnings: 0 (0.0%)
  Failed:  5 (100.0%)

Check Statistics:
  active_tasks_check: 100.0% pass rate
  duplicate_task_check: 0.0% pass rate
  file_history_check: 100.0% pass rate
  path_validation: 0.0% pass rate
  recent_commits_check: 0.0% pass rate
  state_freshness: 100.0% pass rate
```

All Should-Have (P1) features now complete except integration with events.yaml.
