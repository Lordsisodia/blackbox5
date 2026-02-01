# Roadmap State Synchronization Guide

**Purpose:** Automatically keep roadmap STATE.yaml in sync with actual task completion
**Library:** `2-engine/.autonomous/lib/roadmap_sync.py`
**Version:** 1.0.0
**Status:** Production

---

## Overview

The roadmap sync system automatically updates the roadmap STATE.yaml when tasks complete. This prevents the chronic issue of roadmap drift where plans remain marked as "planned" even after work is completed.

### Problem Solved

**Before:** STATE.yaml frequently drifted from reality
- Plans marked "planned" when work was complete
- `next_action` pointing to completed work
- Duplicate tasks created due to stale state
- Manual STATE.yaml updates required

**After:** Automatic synchronization on every task completion
- Plans automatically marked "completed" when tasks finish
- Dependent plans automatically unblocked
- `next_action` updated to next unblocked plan
- Zero manual intervention required

---

## How It Works

### Automatic Execution

The roadmap sync is automatically called by the Executor after every task completion:

```bash
# In Executor task completion workflow:
python3 $RALF_ENGINE_DIR/lib/roadmap_sync.py [TASK-ID] /workspaces/blackbox5/6-roadmap/STATE.yaml
```

### What Gets Updated

1. **Plan Status:** Moves plan from `ready_to_start` or `blocked` to `completed`
2. **Dependencies:** Removes completed plan from dependencies of blocked plans
3. **Next Action:** Updates `next_action` to first unblocked plan
4. **Metadata:** Updates `system.updated` and `stats` in STATE.yaml

### Plan Association

The sync system finds plans by:
1. Searching task file content for "PLAN-XXX" patterns
2. Extracting plan ID from task ID (e.g., `TASK-XXX-plan-YYY`)
3. Pattern matching on task filenames

**Example:**
- Task: `TASK-1769862394-continue-plan-003-planning-agent-tests.md`
- Plan Found: `PLAN-003`
- Action: Mark PLAN-003 as completed

---

## Usage

### Automatic (Executor)

No action required. The Executor automatically calls roadmap sync after every task completion.

### Manual (CLI)

For manual testing or updates:

```bash
# Test without making changes (dry-run)
python3 2-engine/.autonomous/lib/roadmap_sync.py TASK-1769911101 /workspaces/blackbox5/6-roadmap/STATE.yaml --dry-run

# Actually update STATE.yaml
python3 2-engine/.autonomous/lib/roadmap_sync.py TASK-1769911101 /workspaces/blackbox5/6-roadmap/STATE.yaml
```

### Python API

```python
from roadmap_sync import sync_roadmap_on_task_completion

result = sync_roadmap_on_task_completion(
    task_id="TASK-1769911101",
    state_yaml_path="/workspaces/blackbox5/6-roadmap/STATE.yaml",
    executed_by="RALF Executor"
)

if result["success"]:
    print(f"Updated plan {result['plan_id']}")
    for change in result['changes']:
        print(f"  - {change}")
else:
    print(f"Error: {result['error']}")
```

---

## STATE.yaml Structure

The sync system works with this STATE.yaml structure:

```yaml
system:
  name: "blackbox5-roadmap"
  version: "2.0"
  updated: "2026-02-01T00:00:00Z"
  status: "active-development"

next_action: "PLAN-003"

plans:
  ready_to_start:
    - id: "PLAN-003"
      name: "Implement Planning Agent"
      priority: "high"
      dependencies: []

  blocked:
    - id: "PLAN-007"
      name: "Some Future Plan"
      dependencies: ["PLAN-003"]

  completed:
    - id: "PLAN-002"
      name: "Fix YAML Agent Loading"
      completed_at: "2026-01-31"
      executed_by: "RALF (Agent-2.5)"
```

---

## Behavior

### Success Case

**Task completes:**
```
TASK-1769862609 completed
```

**Sync actions:**
1. Finds associated plan: `PLAN-002`
2. Moves PLAN-002 from `ready_to_start` to `completed`
3. Removes PLAN-002 from dependencies of PLAN-003
4. Updates `next_action` to PLAN-003 (if now unblocked)
5. Creates backup: `STATE.yaml.backup.20260201_120000`
6. Writes updated STATE.yaml

### No Plan Found

If task is not associated with any plan:
- Sync returns success (no error)
- Logs warning: "No plan found associated with task {task_id}"
- No changes to STATE.yaml
- Task completion proceeds normally

### Already Completed

If plan is already marked as completed:
- Sync returns success
- Logs warning: "Plan {plan_id} is already marked as completed"
- No changes to STATE.yaml

---

## Safety Features

### 1. Non-Blocking

If sync fails, task completion still succeeds:
- Errors logged but do not fail task
- Executor continues with commit and push
- No manual intervention required

### 2. Automatic Backups

Every sync creates a timestamped backup:
```
STATE.yaml.backup.20260201_120000
STATE.yaml.backup.20260201_120530
```

### 3. Validation

STATE.yaml is validated before modification:
- Checks required keys exist
- Validates data structure
- Prevents corruption
- Graceful degradation on errors

### 4. Idempotent

Can run multiple times safely:
- Re-running sync is safe
- Already-completed plans detected
- No duplicate entries created

---

## Troubleshooting

### Sync Not Running

**Symptom:** Plans remain in "planned" after tasks complete

**Check:**
1. Verify Executor prompt includes sync call
2. Check `$RALF_ENGINE_DIR/lib/roadmap_sync.py` exists
3. Review Executor logs for sync errors

**Solution:**
```bash
# Verify library exists
ls -la 2-engine/.autonomous/lib/roadmap_sync.py

# Test manually
python3 2-engine/.autonomous/lib/roadmap_sync.py TASK-XXX /path/to/STATE.yaml --dry-run
```

### Plan Not Found

**Symptom:** "No plan found associated with task" in logs

**Causes:**
1. Task not associated with any PLAN-XXX
2. Plan ID pattern not recognized
3. Plan already completed

**Solutions:**
- Verify task content contains "PLAN-XXX" reference
- Check plan ID format: "PLAN-001", "PLAN-002", etc.
- If no plan association needed, this is expected behavior

### STATE.yaml Corruption

**Symptom:** Sync fails with "Invalid STATE.yaml structure"

**Recovery:**
```bash
# Find latest backup
ls -lt /workspaces/blackbox5/6-roadmap/STATE.yaml.backup.*

# Restore from backup
cp STATE.yaml.backup.20260201_120000 STATE.yaml
```

---

## Configuration

### Default Paths

- **Library:** `$RALF_ENGINE_DIR/lib/roadmap_sync.py`
- **STATE.yaml:** `/workspaces/blackbox5/6-roadmap/STATE.yaml`

### Custom Paths

To use a different STATE.yaml path:

```bash
python3 2-engine/.autonomous/lib/roadmap_sync.py TASK-XXX /custom/path/STATE.yaml
```

---

## Monitoring

### Log Messages

Watch for these log messages:

```
[INFO] ROADMAP_SYNC: Reading STATE.yaml from /path/to/STATE.yaml
[INFO] ROADMAP_SYNC: Looking for plan associated with task TASK-XXX
[INFO] ROADMAP_SYNC: Found associated plan: PLAN-003
[INFO] ROADMAP_SYNC: Moving plan PLAN-003 to completed
[INFO] ROADMAP_SYNC: Unblocking dependent plans
[INFO] ROADMAP_SYNC: Unblocked: PLAN-007
[INFO] ROADMAP_SYNC: Updating next_action
[INFO] ROADMAP_SYNC: next_action: PLAN-003 -> PLAN-007
[INFO] ROADMAP_SYNC: Created backup: STATE.yaml.backup.20260201_120000
[INFO] ROADMAP_SYNC: Updated STATE.yaml written successfully
```

### Success Indicators

- ✅ "Roadmap sync completed successfully for plan PLAN-XXX"
- ✅ Changes include "Moved plan PLAN-XXX to completed"
- ✅ "next_action" updated to new plan

---

## Best Practices

1. **Let it run automatically** - Don't manually update plan statuses
2. **Check logs periodically** - Verify sync is working
3. **Keep backups** - Automatic backups are created, but keep them for a while
4. **Test new patterns** - Use `--dry-run` before manual updates
5. **Monitor dependencies** - Ensure dependent plans unblock as expected

---

## Future Enhancements

Potential improvements (not yet implemented):

- [ ] Sync on task creation (block if plan already completed)
- [ ] Webhook notifications on plan completion
- [ ] Dashboard showing sync history
- [ ] Automatic dependency validation
- [ ] Rollback capability for incorrect syncs

---

## Related Documentation

- **Improvement:** IMP-1769903001 (Auto-sync roadmap state)
- **Task:** TASK-1769911101 (Implement roadmap sync)
- **Duplicate Detection:** `operations/.docs/duplicate-detection-guide.md`

---

## Support

For issues or questions:

1. Check logs in Executor run directory: `runs/executor/run-NNNN/`
2. Review STATE.yaml backups for change history
3. Test with `--dry-run` flag first
4. Ask Planner via `chat-log.yaml` if unclear

---

**Last Updated:** 2026-02-01
**Maintained By:** RALF Executor
