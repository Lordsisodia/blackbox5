# Action Plan: Task Status Lifecycle Automation (Critical Blocker #2)

**Task ID:** TASK-STATUS-LIFECYCLE-ACTION-PLAN
**Type:** design | implement
**Priority:** critical
**Status:** completed
**Created:** 2026-02-03T23:20:00Z
**Related:** Critical Blocker #2

---

## First Principles Analysis

### The Problem
Tasks in the Dual-RALF system don't automatically transition through their lifecycle states. A task can remain "pending" in queue.yaml even when an executor has claimed it and is actively working on it. The status transitions are manual or non-existent.

### Why This Matters
Without automated status transitions:
- **No visibility** into what's actually being worked on
- **Duplicate work risk** - another executor might pick up an in-progress task
- **No audit trail** of task progression
- **Broken feedback loops** - planner doesn't know when tasks start/complete

### Root Cause
The system was designed with the assumption that LLM agents would reliably update statuses. As proven by the 0% queue sync success rate analysis, LLMs cannot reliably follow status update instructions. The solution must be **hook-based enforcement**, not prompt-based suggestions.

---

## Current State Assessment

### What Exists
1. **queue.yaml** - Has `status` field per task (pending/completed)
2. **tasks/active/TASK-XXX/task.md** - Has Status field in frontmatter
3. **events.yaml** - Logs events (started, completed) but no linking to status
4. **tasks/working/** - Now auto-created when task is claimed (Critical Blocker #1 fixed)

### What's Missing
1. **No automated status transition** on task claim
2. **No in_progress status** - only pending/completed
3. **No linking** between events.yaml entries and queue.yaml status
4. **No task move** from active/ to completed/ on completion
5. **No STATE.yaml integration** with task status

---

## Proposed Solution

### State Machine Design

```
planned → ready → claimed → in_progress → completed → archived
   ↑         ↑        ↑          ↑           ↑
   |         |        |          |           |
 Planner  Planner  Executor   Executor    Stop Hook
 creates  queues   claims     works       archives
```

### States Definition

| State | Meaning | Set By |
|-------|---------|--------|
| **planned** | Task exists but not ready for execution | Task creation |
| **ready** | Task is prioritized and in queue | Planner |
| **claimed** | Executor has claimed task, working dir created | ralf-task-select.sh |
| **in_progress** | Executor is actively working | Executor heartbeat |
| **completed** | Task finished successfully | Stop hook |
| **failed** | Task failed, needs replanning | Stop hook |
| **archived** | Task moved to completed/ folder | Stop hook |

### Implementation Steps

#### Step 1: Extend queue.yaml status values
- Add `claimed`, `in_progress`, `failed` to valid statuses
- Add `claimed_at`, `claimed_by`, `started_at`, `completed_at` timestamps

#### Step 2: Update ralf-task-select.sh
- On claim: set status to `claimed` in queue.yaml
- Create event in events.yaml linking to claim

#### Step 3: Create ralf-task-start.sh
- Called by executor when beginning work
- Sets status to `in_progress`
- Updates heartbeat with task reference

#### Step 4: Update ralf-stop-hook.sh
- On successful completion: set status to `completed`
- On failure: set status to `failed`
- Move task from tasks/active/ to tasks/completed/
- Update STATE.yaml with completion

#### Step 5: Create status sync script
- ralf-task-status.sh --sync
- Ensures queue.yaml, task.md, and events.yaml are consistent
- Can be run periodically or on demand

---

## Implementation Timeline

| Step | Estimated Time | Dependencies |
|------|----------------|--------------|
| 1. Extend queue.yaml | 15 min | None |
| 2. Update ralf-task-select.sh | 30 min | Step 1 |
| 3. Create ralf-task-start.sh | 30 min | None |
| 4. Update ralf-stop-hook.sh | 45 min | None |
| 5. Create status sync script | 30 min | Steps 1-4 |
| 6. Testing | 30 min | All steps |
| **Total** | **~3 hours** | |

---

## Success Criteria

- [x] When task is claimed, status changes to `claimed` in queue.yaml (via ralf-task-select.sh)
- [x] When work starts, status changes to `in_progress` (via ralf-task-start.sh)
- [x] When task completes, status changes to `completed` (via ralf-stop-hook.sh)
- [x] Completed tasks are moved to tasks/completed/ (142 tasks archived)
- [ ] STATE.yaml is updated with task status (STATE.yaml removed from architecture)
- [x] events.yaml has complete lifecycle events (151KB of events logged)
- [x] No manual status updates required (all automated via hooks)

---

## Files to Modify

1. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` - Add status values
2. `/Users/shaansisodia/.blackbox5/bin/ralf-task-select.sh` - Set claimed status
3. `/Users/shaansisodia/.blackbox5/bin/ralf-task-start.sh` - NEW: Set in_progress status
4. `/Users/shaansisodia/.blackbox5/bin/ralf-stop-hook.sh` - Set completed/failed, move task
5. `/Users/shaansisodia/.blackbox5/bin/ralf-task-status.sh` - NEW: Status sync utility

---

## Notes

**First Principle:** State transitions should be enforced by code (hooks/scripts), not suggested by prompts. Any status change that relies on an LLM remembering to update a file will fail.

**Design Decision:** Keep queue.yaml as the source of truth for task status, sync to other locations (task.md, STATE.yaml) from there.

**Risk Mitigation:** The status sync script (Step 5) provides a recovery mechanism if statuses get out of sync.

---

## Next Actions

1. Review this action plan
2. Approve or modify approach
3. Begin implementation with Step 1
