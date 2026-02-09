# TASK-FIX-SKIL-032-1: Implement Task-Level Time Tracking with Skill Attribution

**Status:** pending
**Priority:** HIGH
**Category:** skills
**Estimated Effort:** 45 minutes
**Created:** 2026-02-09T12:00:00Z
**Parent:** TASK-SKIL-032

---

## Objective

Implement a mechanism to track task execution time with explicit skill attribution, capturing both duration and which skill (if any) was used.

---

## Success Criteria

- [ ] Task start/end times are automatically recorded
- [ ] Skill used (or null) is captured for each task
- [ ] Duration is calculated and stored in task outcomes
- [ ] Data is written to `operations/skill-metrics.yaml` task_outcomes section
- [ ] Existing task completion workflow is modified to include time tracking
- [ ] At least 5 test tasks demonstrate the tracking works

---

## Context

**Root Cause:** SKIL-032 identified that ROI calculation fails because we lack task time data WITH skills vs WITHOUT skills.

**Current Gap:** The `task_outcomes` schema in `operations/skill-metrics.yaml` exists but is not populated with actual task execution data. Tasks complete without recording:
- Start timestamp
- End timestamp
- Duration
- Skill attribution

**Key Files:**
- `operations/skill-metrics.yaml` - Contains schema and task_outcomes array
- `bin/bb5-task` - Task creation/completion workflow
- `.autonomous/memory/hooks/task_completion_skill_recorder.py` - Existing hook (if exists)

**Schema Reference:**
```yaml
task_outcomes:
  - task_id: string
    timestamp: ISO8601
    skill_used: string | null
    duration_minutes: number
    outcome: success | failure | partial
```

---

## Approach

1. **Modify task completion workflow** (`bin/bb5-task` or equivalent)
   - Add start time capture when task begins
   - Add end time capture when task completes
   - Calculate duration in minutes

2. **Capture skill attribution**
   - Read skill used from task context or prompt
   - Store skill name or null if no skill used

3. **Write to skill-metrics.yaml**
   - Append task outcome to task_outcomes array
   - Include all required fields

4. **Test the implementation**
   - Create test tasks with skills
   - Create test tasks without skills
   - Verify data is recorded correctly

---

## Files to Modify

| File | Changes |
|------|---------|
| `bin/bb5-task` | Add time tracking hooks at start/end |
| `operations/skill-metrics.yaml` | Ensure schema supports new fields |

## Files to Create

| File | Purpose |
|------|---------|
| `.autonomous/memory/hooks/task_time_tracker.py` | Unified time tracking hook |

---

## Rollback Strategy

If changes cause issues:
1. Restore `operations/skill-metrics.yaml` from git
2. Disable time tracking hooks
3. Document failure mode in task notes

---

## Notes

- Keep changes minimal to avoid disrupting existing workflows
- Ensure backward compatibility with existing task outcomes
- Consider adding environment variable to disable tracking if needed
