# TASK-FIX-SKIL-007-3: Update task outcome logging to record skill_used

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-09T12:00:00Z
**Parent:** TASK-SKIL-007

## Objective
Fix the task outcome logging mechanism to properly record which skill was used when a task is completed, so that metrics calculations can attribute outcomes to the correct skills.

## Root Cause
Currently, task outcomes in `skill-registry.yaml` have `skill_used: null` because the task completion logging doesn't capture which skill was actually invoked. Looking at the task_outcomes section (lines 891-935), all entries show `skill_used: null` even though skills were considered and sometimes invoked. Without this data, metrics calculations cannot attribute success/failure to specific skills.

## Success Criteria
- [ ] Identify where task outcomes are logged (task completion hooks/scripts)
- [ ] Modify logging to capture the skill that was actually used
- [ ] Ensure `skill_used` field is populated in task_outcomes entries
- [ ] If multiple skills were applicable, record the one that was actually invoked
- [ ] If no skill was invoked, record `skill_used: null` with a note explaining why
- [ ] Update existing null skill_used entries if possible (backfill)
- [ ] Test that new task completions record skill_used correctly

## Files to Modify
- Identify and modify: Task completion hook scripts (likely in `~/.blackbox5/5-project-memory/blackbox5/.claude/hooks/`)
- Check: `~/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/hooks/task_completion_skill_recorder.py`
- Check: `~/.blackbox5/5-project-memory/blackbox5/.claude/hooks/log-skill-on-complete.py`
- Modify: `~/.blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml` (backfill existing entries if possible)

## Context

### Current task_outcomes entries (from skill-registry.yaml):
```yaml
task_outcomes:
  - task_id: TASK-1769909000
    timestamp: "2026-02-01T08:00:00Z"
    skill_used: null  # <- PROBLEM: Should be populated
    task_type: implement
    duration_minutes: 40
    outcome: success
    quality_rating: 4
    trigger_was_correct: true
    would_use_again: true
    notes: "First task with skill selection framework. No skill invoked..."
```

### Usage log shows skill was recorded (from skill-usage.yaml):
```yaml
usage_log:
  - timestamp: '2026-02-07T16:08:38.955055+00:00'
    task_id: TASK-SSOT-025
    result: unknown
    skill: bmad-dev  # <- Skill IS recorded here
    applicable_skills: [bmad-dev, continuous-improvement]
    confidence: 85
```

### The disconnect:
- `skill-usage.yaml` records which skill was used
- `skill-registry.yaml` task_outcomes doesn't get this information
- The sync between these needs to happen OR the logging needs to be unified

## Investigation Required

Before implementing, investigate:
1. Where is `task_outcomes` data written?
   - Search for "task_outcomes" in codebase
   - Check task completion scripts
   - Check bb5 CLI commands

2. How does skill invocation get recorded?
   - Check `log-skill-usage.py`
   - Check `task_completion_skill_recorder.py`
   - Check if there's a hook that runs on task completion

3. What's the flow when a skill is invoked?
   - Skill selection happens in Phase 1.5
   - Skill execution happens in Phase 2
   - Task completion happens at end
   - Where is the bridge?

## Approach

### Option A: Update task completion logging (recommended)
1. Find the script that appends to task_outcomes
2. Modify it to accept a `skill_used` parameter
3. Update the task completion workflow to pass the skill name
4. Backfill existing entries from usage_log data

### Option B: Merge during sync (alternative)
1. When syncing skill-usage.yaml to skill-registry.yaml
2. Match entries by task_id
3. Copy `skill` field from usage_log to `skill_used` in task_outcomes

## Files to Investigate
```bash
# Search for task outcome logging
grep -r "task_outcomes" ~/.blackbox5/5-project-memory/blackbox5/bin/
grep -r "task_outcome" ~/.blackbox5/5-project-memory/blackbox5/.claude/hooks/

# Search for skill logging
grep -r "skill_used" ~/.blackbox5/5-project-memory/blackbox5/

# Check existing hooks
ls -la ~/.blackbox5/5-project-memory/blackbox5/.claude/hooks/
ls -la ~/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/hooks/
```

## Rollback Strategy
- Keep backup of any modified hook scripts
- Test with a single task completion first
- Ensure existing task_outcomes data is not corrupted

## Estimated Effort
45-60 minutes (including investigation)

## Related Tasks
- TASK-FIX-SKIL-007-1: Sync skill-usage.yaml to skill-registry.yaml
- TASK-FIX-SKIL-007-2: Fix calculate-skill-metrics.py target file

## Notes
- This task may need to be done after or in conjunction with TASK-FIX-SKIL-007-1
- Consider if the solution should be a unified logging approach rather than fixing the disconnect
