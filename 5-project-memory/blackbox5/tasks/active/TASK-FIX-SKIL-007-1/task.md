# TASK-FIX-SKIL-007-1: Sync skill-usage.yaml to skill-registry.yaml

**Status:** completed
**Priority:** HIGH
**Created:** 2026-02-09T12:00:00Z
**Completed:** 2026-02-10T22:29:00Z
**Parent:** TASK-SKIL-007

## Objective
Create a sync mechanism that transfers usage data from `skill-usage.yaml` to `skill-registry.yaml` so that metrics calculations have access to current usage statistics.

## Root Cause
The `skill-usage.yaml` file (located at `~/.blackbox5/5-project-memory/blackbox5/.autonomous/operations/skill-usage.yaml`) contains actual usage data (1 entry for bmad-dev) but this data never gets synced to `skill-registry.yaml` (located at `~/.blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml`). The metrics calculation reads from skill-registry.yaml, which has null usage counts, resulting in null metrics.

## Success Criteria
- [x] Create a sync script that reads from skill-usage.yaml and updates skill-registry.yaml
- [x] Sync script updates the `usage` section for each skill in skill-registry.yaml
- [x] Sync script updates the `usage_history` section in skill-registry.yaml
- [x] Sync script preserves all other data in skill-registry.yaml
- [x] Sync can be run manually and returns 0 on success
- [x] After sync, skill-registry.yaml shows non-null usage counts for skills with data

## Files to Modify
- Create: `~/.blackbox5/5-project-memory/blackbox5/bin/sync-skill-usage.py` (new script)
- Read: `~/.blackbox5/5-project-memory/blackbox5/.autonomous/operations/skill-usage.yaml`
- Modify: `~/.blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml`

## Context

### skill-usage.yaml structure:
```yaml
usage_log:
  - timestamp: '2026-02-07T16:08:38.955055+00:00'
    task_id: TASK-SSOT-025
    result: unknown
    skill: bmad-dev
    applicable_skills: [bmad-dev, continuous-improvement]
    confidence: 85
    trigger_reason: "..."
    notes: "..."
skills:
  - name: bmad-dev
    usage_count: 1
    success_count: 0
    failure_count: 0
    last_used: '2026-02-07T16:08:38.955351+00:00'
    first_used: '2026-02-07T16:08:38.955351+00:00'
metadata:
  last_updated: '2026-02-07T16:08:38.955353+00:00'
  total_invocations: 1
```

### skill-registry.yaml target structure (skills.bmad-dev.usage):
```yaml
skills:
  bmad-dev:
    usage:
      usage_count: 0  # <- Should be synced from skill-usage.yaml
      success_count: 0
      failure_count: 0
      first_used: null
      last_used: null
      avg_execution_time_ms: null
```

## Approach
1. Read and parse skill-usage.yaml
2. Read and parse skill-registry.yaml
3. For each skill in skill-usage.yaml:
   - Update corresponding skill in skill-registry.yaml with usage counts
   - Update first_used and last_used timestamps
4. Append usage_log entries to usage_history in skill-registry.yaml
5. Write updated skill-registry.yaml
6. Add logging for sync operations

## Rollback Strategy
- Backup skill-registry.yaml before modifying
- If sync fails, restore from backup
- Script should validate YAML before writing

## Estimated Effort
30-45 minutes

## Related Tasks
- TASK-FIX-SKIL-007-2: Fix calculate-skill-metrics.py target file
- TASK-FIX-SKIL-007-3: Update task outcome logging

## Notes

### Implementation Summary

Created `sync-skill-usage.py` script that:
- Reads skill-usage.yaml for actual usage data
- Updates skill-registry.yaml with current usage statistics
- Merges usage_log entries to usage_history
- Updates first_used/last_used timestamps
- Creates backups before modifying files
- Supports dry-run mode for testing

### Test Results

**Before Sync:**
- bmad-dev usage_count: 0
- Total usage records: 1 (from skill-registry.yaml)

**After Sync:**
- bmad-dev usage_count: 1
- Total usage records: 2 (added TASK-SSOT-025 log entry)

### Files Created/Modified

**Created:**
- `/opt/blackbox5/5-project-memory/blackbox5/bin/sync-skill-usage.py` (executable)

**Modified:**
- `/opt/blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml` (updated with sync data)

**Backups:**
- `/opt/blackbox5/5-project-memory/blackbox5/.autonomous/backups/skill-registry.yaml.backup.20260210_222911`

### Usage

```bash
# Run sync
python3 /opt/blackbox5/5-project-memory/blackbox5/bin/sync-skill-usage.py --verbose

# Dry run (no changes)
python3 /opt/blackbox5/5-project-memory/blackbox5/bin/sync-skill-usage.py --dry-run --verbose
```

### All Success Criteria Met

- [x] Create a sync script that reads from skill-usage.yaml and updates skill-registry.yaml
- [x] Sync script updates the `usage` section for each skill in skill-registry.yaml
- [x] Sync script updates the `usage_history` section in skill-registry.yaml
- [x] Sync script preserves all other data in skill-registry.yaml
- [x] Sync can be run manually and returns 0 on success
- [x] After sync, skill-registry.yaml shows non-null usage counts for skills with data
