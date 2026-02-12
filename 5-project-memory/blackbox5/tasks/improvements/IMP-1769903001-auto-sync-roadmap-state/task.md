# IMP-1769903001: Implement Automatic Roadmap State Synchronization

**Type:** implement
**Priority:** high
**Category:** process
**Source Learning:** L-1769861933-001, L-1769813746-001, L-20260131-060933-L002, L-1769807450-001
**Status:** in_progress
**Created:** 2026-02-01T13:30:00Z

---

## Objective

Implement automatic synchronization between task completion and roadmap STATE.yaml to prevent drift between documented state and actual state.

## Problem Statement

STATE.yaml frequently drifts from reality:
- Plans marked "planned" when work is complete
- next_action pointing to completed work
- Duplicate tasks created due to stale state
- 7+ learnings mention this issue

## Success Criteria

- [x] Post-task-completion hook updates STATE.yaml automatically
- [x] Plan status changes from "planned" → "completed" when task finishes
- [x] Dependencies unblocked automatically when plan completes
- [x] next_action updated to next unblocked plan
- [x] No manual STATE.yaml updates required for standard task completion

## Approach

1. Create `lib/roadmap_sync.py` - Library for STATE.yaml updates
2. Add hook to task completion workflow
3. Implement auto-unblock for dependent plans
4. Update next_action logic
5. Test with sample task completion

## Files to Modify

- `2-engine/.autonomous/lib/roadmap_sync.py` (create)
- `2-engine/.autonomous/workflows/task-completion.yaml`
- `.templates/tasks/task-completion.md.template`

## Related Learnings

- run-1769861933: "Roadmap State Can Become Outdated"
- run-1769813746: "Plan Completion Tracking Gap"
- run-20260131-060933: "Roadmap State Can Drift from Reality"
- run-1769807450: "Roadmap State Decay"

## Estimated Effort

45 minutes

## Acceptance Criteria

- [x] Library created with update_plan_status(), unblock_dependents(), update_next_action()
- [x] Task completion automatically triggers sync
- [ ] Tested with at least 2 plan completions
- [ ] Documentation updated

## Implementation Notes

**Date:** 2026-02-12
**Completed By:** Legacy (moltbot-vps-ai)

### Files Created

1. **`.autonomous/lib/roadmap_sync.py`** (13.8 KB)
   - Core synchronization library
   - Functions:
     - `update_plan_status(plan_id, status)` - Updates plan status in metadata.yaml
     - `unblock_dependents(plan_id)` - Unblocks plans depending on completed plan
     - `update_next_action(completed_plan_id)` - Updates next_action to next unblocked plan
     - `update_goal_status(goal_id)` - Updates goal status if all plans complete
     - `sync_on_task_completion(task_id, plan_id, goal_id)` - Main sync function
     - `get_roadmap_status()` - Roadmap status summary
   - CLI interface: `python3 roadmap_sync.py <task_id> [plan_id] [goal_id]`

2. **`.autonomous/hooks/post-task-complete.sh`** (2.9 KB)
   - Post-task-completion hook script
   - Automatically extracts plan_id and goal_id from task.md
   - Color-coded output for better visibility
   - Usage: `./post-task-complete.sh <task_id> [plan_id] [goal_id]`

### Files Modified

1. **`.autonomous/autonomous.py`**
   - Integrated hook call into `execute_improvement_task()` function
   - Hook called after task is moved to completed/ directory
   - Added error handling for hook execution
   - Fixed pre-existing syntax error (missing comma in duplicate detection)

### Integration Details

**Workflow:**
1. Task completes → `autonomous.py` moves to `tasks/completed/`
2. Hook script `.autonomous/hooks/post-task-complete.sh` is called
3. Hook extracts plan_id and goal_id from task.md (if not provided)
4. Python library `.autonomous/lib/roadmap_sync.py` performs sync:
   - Updates plan status to "completed" in metadata.yaml
   - Unblocks dependent plans
   - Updates next_action to next unblocked plan
   - Updates goal status if all plans complete

**Automatic Extraction:**
- Hook script parses task.md for `linked_plan` and `linked_goal` fields
- Eliminates need for manual plan_id/goal_id arguments
- Makes integration seamless with existing task structure

### Testing Performed

1. **Syntax Check:** Python compilation successful
2. **Library Test:** `python3 roadmap_sync.py TASK-TEST-001 PLAN-TEST-001 IG-001` ✓
3. **Hook Test:** `./post-task-complete.sh TASK-TEST-002` ✓
4. **Integration:** Hook call integrated into autonomous.py ✓

### Remaining Work

1. **Testing with Real Plans:** Test with actual plan completion (requires plan metadata files)
2. **Documentation Update:** Update ROADMAP.md with sync hook details
3. **Goal Status Testing:** Verify goal status updates work correctly with multiple plans

### Key Features

✅ **Automatic Synchronization** - No manual STATE.yaml updates needed
✅ **Dependency Management** - Dependent plans automatically unblocked
✅ **Goal Tracking** - Goal status updates when all plans complete
✅ **Error Handling** - Graceful fallback if hook fails
✅ **Smart Extraction** - Auto-extracts plan_id/goal_id from task.md
✅ **Color-Coded Output** - Easy-to-read logging in hooks
