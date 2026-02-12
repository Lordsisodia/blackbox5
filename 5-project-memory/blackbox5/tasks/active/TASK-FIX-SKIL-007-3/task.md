# TASK-FIX-SKIL-007-3: Update task outcome logging to record skill_used

**Status:** in_progress
**Priority:** HIGH
**Created:** 2026-02-09T12:00:00Z
**Parent:** TASK-SKIL-007

## Objective
Fix task outcome logging mechanism to properly record which skill was used when a task is completed, so that metrics calculations can attribute outcomes to correct skills.

## Root Cause
Currently, task outcomes in `skill-registry.yaml` have `skill_used: null` because task completion logging doesn't capture which skill was actually invoked. Looking at the task_outcomes section, all entries show `skill_used: null` even though skills were considered and sometimes invoked. Without this data, metrics calculations cannot attribute success/failure to specific skills.

## Success Criteria
- [x] Identify where task outcomes are logged (task completion hooks/scripts)
- [x] Modify logging to capture skill that was actually used
- [x] Ensure `skill_used` field is populated in task_outcomes entries
- [ ] If multiple skills were applicable, record the one that was actually invoked
- [ ] If no skill was invoked, record `skill_used: null` with a note explaining why
- [ ] Update existing null skill_used entries if possible (backfill)
- [ ] Test that new task completions record skill_used correctly

## Files to Modify
- [x] Identify and modify: Task completion hook scripts (likely in `~/.blackbox5/5-project-memory/blackbox5/.claude/hooks/`)
- [x] Check: `~/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/hooks/task_completion_skill_recorder.py`
- [x] Check: `~/.blackbox5/5-project-memory/blackbox5/.claude/hooks/log-skill-on-complete.py`
- [x] Check: TaskCompleteCommand in `2-engine/interface/cli/task_commands.py`
- [ ] Modify: `~/.blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml` (backfill existing entries if possible)

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

## Investigation Results (2026-02-12)

### 1. Found task completion hook
**File:** `/opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/task_completion_skill_recorder.py`

This hook exists and is designed to:
- Accept `--skill` parameter (or `BB5_SKILL_USED` environment variable)
- Record skill usage to both:
  - `skill-registry.yaml` task_outcomes section
  - `.autonomous/operations/skill-usage.yaml` usage_log
- Update skill aggregate statistics
- Record events in `events.yaml`

### 2. Found bb5 task:complete command
**File:** `/opt/blackbox5/2-engine/interface/cli/task_commands.py`

The `TaskCompleteCommand`:
- Moves task from working/ to completed/
- Generates a final report
- **Does NOT call the skill recorder hook** ← MISSING INTEGRATION

### 3. Found sync-skill-usage.py script
**File:** `/opt/blackbox5/5-project-memory/blackbox5/bin/sync-skill-usage.py`

This script already has logic to:
- Backfill `skill_used` from usage_log to task_outcomes
- Map task_id to existing outcomes
- Update skill_used if currently null

**Issue:** It only has data for TASK-SSOT-025 (the only entry in usage_log). Older tasks don't have usage_log entries.

### 4. Flow when a skill is invoked
```
1. Skill selection (Phase 1.5) → skill_name identified
2. Skill execution (Phase 2) → skill invoked (or not)
3. Task completion (end of session)
4. ❌ MISSING: Skill recorder hook NOT called automatically
5. Task archived to completed/
```

## Approach

### Option A: Update task completion logging (IMPLEMENTING)
1. ✅ Find the script that appends to task_outcomes → TaskCompleteCommand
2. Modify TaskCompleteCommand to call task_completion_skill_recorder.py
3. Add skill_used parameter to task:complete command
4. Backfill existing entries from usage_log data (sync-skill-usage.py already does this)

### Option B: Merge during sync (already exists)
1. ✅ sync-skill-usage.py already has backfill logic
2. ✅ Matches entries by task_id
3. ✅ Copies `skill` field from usage_log to `skill_used` in task_outcomes

## Implementation Plan

### Step 1: Modify TaskCompleteCommand
Add integration to call `task_completion_skill_recorder.py` with skill_used parameter.

**Location:** `/opt/blackbox5/2-engine/interface/cli/task_commands.py`

Changes needed:
1. Add `--skill` parameter to TaskCompleteCommand
2. Call the skill recorder hook when task completes
3. Pass skill_used, outcome, duration, quality, etc.

### Step 2: Backfill existing entries
Run `sync-skill-usage.py` to backfill skill_used from usage_log to task_outcomes.
- Already has logic for this
- Only TASK-SSOT-025 has usage_log entry
- Older tasks will remain null (acceptable for historical data)

### Step 3: Test
Complete a test task to verify skill_used is populated correctly.

## Rollback Strategy
- Keep backup of any modified files
- Test with a single task completion first
- Ensure existing task_outcomes data is not corrupted

## Estimated Effort
45-60 minutes (including investigation) - Currently at 30 minutes

## Related Tasks
- TASK-FIX-SKIL-007-1: Sync skill-usage.yaml to skill-registry.yaml
- TASK-FIX-SKIL-007-2: Fix calculate-skill-metrics.py target file

## Notes
- This task may need to be done after or in conjunction with TASK-FIX-SKIL-007-1
- Consider if the solution should be a unified logging approach rather than fixing the disconnect

### Progress Log (2026-02-12)
- 05:55 UTC - Started investigation
- 05:57 UTC - Found task_completion_skill_recorder.py hook
- 05:58 UTC - Found TaskCompleteCommand in task_commands.py
- 05:59 UTC - Found sync-skill-usage.py script
- 06:00 UTC - Ran sync-skill-usage.py (0 updates, only TASK-SSOT-025 has usage_log entry)
- 06:05 UTC - Updated task.md with investigation results
- Next: Implement TaskCompleteCommand integration with skill recorder
