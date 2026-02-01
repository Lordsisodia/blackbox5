# Queue Management Guide
**BlackBox5 Operations Documentation**
**Version:** 1.0.0
**Last Updated:** 2026-02-01

---

## Overview

The task queue (`queue.yaml`) is the single source of truth for pending tasks in the BlackBox5 autonomous system. It is synchronized automatically with the `.autonomous/tasks/active/` directory to ensure accuracy and prevent manual sync errors.

---

## Queue Structure

### File Location
`.autonomous/communications/queue.yaml`

### YAML Structure
```yaml
queue:
  - id: TASK-XXXXXXXX
    type: implement|analyze|test|refactor|docs
    title: Brief task description
    priority: critical|high|medium|low
    estimated_minutes: 30
    context_level: 1|2|3
    approach: |
      Step-by-step approach
    status: pending|in_progress|completed|failed|blocked
    added_at: '2026-02-01T12:00:00Z'
    dependencies: []
    source: 'Planner Run XXXX'

metadata:
  current_depth: 4
  last_updated: '2026-02-01T12:00:00Z'
  updated_by: 'planner'
  queue_depth_target: '3-5'
  notes: |
    Queue management notes...
```

---

## Automatic Synchronization

### How It Works

When a task completes:
1. Executor moves task from `tasks/active/` → `tasks/completed/`
2. Executor calls `sync_all_on_task_completion()` via roadmap_sync.py
3. Queue sync removes completed task from `queue.yaml`
4. Queue metadata updated (current_depth, last_updated)

### Integration Point

**Library:** `2-engine/.autonomous/lib/queue_sync.py`

**Function:** `sync_queue_on_task_completion()`

**Called from:** `2-engine/.autonomous/lib/roadmap_sync.py:sync_all_on_task_completion()`

**Workflow:**
```python
from roadmap_sync import sync_all_on_task_completion

result = sync_all_on_task_completion(
    task_id="TASK-1769916001",
    state_yaml_path="/path/to/STATE.yaml",
    improvement_backlog_path="/path/to/improvement-backlog.yaml",
    queue_path="/path/to/.autonomous/communications/queue.yaml",
    active_dir="/path/to/.autonomous/tasks/active",
    task_content=task_file_content,
    executed_by="RALF Executor"
)
```

---

## Manual Queue Sync

### CLI Usage

**Sync only queue:**
```bash
python3 2-engine/.autonomous/lib/queue_sync.py \
  .autonomous/communications/queue.yaml \
  .autonomous/tasks/active
```

**Dry run (test without changes):**
```bash
python3 2-engine/.autonomous/lib/queue_sync.py \
  .autonomous/communications/queue.yaml \
  .autonomous/tasks/active \
  --dry-run
```

**Sync everything (roadmap + improvement + queue):**
```bash
python3 2-engine/.autonomous/lib/roadmap_sync.py all \
  TASK-XXXXXXXX \
  /path/to/STATE.yaml \
  /path/to/improvement-backlog.yaml \
  .autonomous/communications/queue.yaml \
  .autonomous/tasks/active \
  .autonomous/tasks/completed/TASK-XXXXXXXX-title.md
```

---

## Queue Depth Management

### Target Depth
- **Optimal:** 3-5 tasks
- **Minimum:** 2 tasks (risk of executor idle)
- **Maximum:** 10 tasks (overhead in planning)

### When to Add Tasks
Planner should add tasks when:
- Queue depth < 3 tasks
- Executor velocity is high (completing tasks quickly)
- Strategic tasks needed (features, improvements)

### When to Remove Tasks
Tasks automatically removed when:
- Task moved from `active/` → `completed/`
- Task marked as failed/blocked (manual intervention)
- Task cancelled (manual intervention)

---

## Troubleshooting

### Queue Shows Completed Tasks

**Symptom:** Queue contains tasks that are already completed.

**Solution:**
```bash
# Run queue sync manually
python3 2-engine/.autonomous/lib/queue_sync.py \
  .autonomous/communications/queue.yaml \
  .autonomous/tasks/active
```

### Queue Depth Incorrect

**Symptom:** Queue depth doesn't match active task count.

**Solution:**
```bash
# Check active task count
ls -1 .autonomous/tasks/active/TASK-*.md | wc -l

# Run queue sync to correct
python3 2-engine/.autonomous/lib/queue_sync.py \
  .autonomous/communications/queue.yaml \
  .autonomous/tasks/active
```

### Sync Errors

**Symptom:** Queue sync fails with error.

**Possible causes:**
1. Invalid YAML syntax in queue.yaml
2. Missing queue.yaml or active/ directory
3. Permission issues

**Solution:**
1. Validate YAML: `python3 -c "import yaml; yaml.safe_load(open('.autonomous/communications/queue.yaml'))"`
2. Check file paths exist
3. Check file permissions

---

## Best Practices

### For Planner
1. **Keep queue depth optimal:** 3-5 tasks
2. **Add diverse task types:** mix of implement, analyze, refactor
3. **Update queue immediately** after creating tasks
4. **Document task dependencies** in queue entries

### For Executor
1. **Always call sync_all_on_task_completion()** after task completion
2. **Verify queue sync success** before marking task complete
3. **Report sync failures** to planner via chat-log.yaml

### For System
1. **Automatic queue sync** via roadmap_sync.py integration
2. **Backup creation** before any queue modification
3. **Non-blocking sync:** Queue sync failure doesn't fail task completion
4. **Idempotent:** Safe to run multiple times

---

## Monitoring

### Queue Health Metrics

**Depth:** Current number of tasks in queue
- Healthy: 3-5 tasks
- Warning: 1-2 or 6-10 tasks
- Critical: 0 or >10 tasks

**Velocity:** Tasks completed per hour
- Good: >2 tasks/hour
- Slow: 0.5-2 tasks/hour
- Stalled: <0.5 tasks/hour

**Sync Accuracy:** Queue vs active directory match
- Target: 100% (queue depth == active task count)
- Warning: <100% (sync needed)

### Check Queue Health
```bash
# Count queue tasks
python3 -c "import yaml; print(len(yaml.safe_load(open('.autonomous/communications/queue.yaml'))['queue']))"

# Count active tasks
ls -1 .autonomous/tasks/active/TASK-*.md | wc -l

# Should match!
```

---

## Reference

### Related Files
- **Queue Sync Library:** `2-engine/.autonomous/lib/queue_sync.py`
- **Roadmap Sync Library:** `2-engine/.autonomous/lib/roadmap_sync.py`
- **Queue File:** `.autonomous/communications/queue.yaml`
- **Active Tasks:** `.autonomous/tasks/active/`
- **Completed Tasks:** `.autonomous/tasks/completed/`

### Related Documentation
- **RALF-Executor Prompt:** `2-engine/.autonomous/prompts/system/executor/variations/v2-legacy-based.md`
- **Task Completion Workflow:** Executor prompt Step 4
- **Roadmap Sync Guide:** `operations/.docs/roadmap-sync-guide.md` (if exists)

---

## Changelog

### v1.0.0 (2026-02-01)
- Initial queue sync library created
- Integrated with roadmap_sync.py
- Automatic synchronization on task completion
- CLI interface for manual sync
- Documentation created

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review queue sync logs for error messages
3. Ask Planner via chat-log.yaml
4. Check git history for recent changes

**Remember:** Queue sync is automatic and non-blocking. If sync fails, the task still completes, but manual intervention may be needed to correct the queue.
