# TASK-AUTONOMY-001: Task State Machine Hook Library

**Goal:** IG-AUTONOMY-001 - Close the Feedback Loops
**Plan:** PLAN-AUTONOMY-001
**Status:** completed
**Priority:** CRITICAL
**Created:** 2026-02-06
**Started:** 2026-02-06

---

## Objective

Implement the core state machine for task lifecycle management. This is the foundation of autonomous operation - tasks should transition through states automatically without LLM intervention.

---

## Success Criteria

- [x] States defined: pending → claimed → in_progress → completed → archived
- [x] SessionStart hook auto-claims task, sets status to "in_progress"
- [x] PreToolUse hook blocks TaskUpdate if task not claimed
- [x] SessionEnd hook auto-transitions to completed when criteria met
- [x] All state changes logged to events.yaml

---

## Context

Current BB5 has a task status problem (Critical Blocker #2):
- Tasks don't automatically transition through lifecycle states
- A task can remain "pending" in queue.yaml even when actively being worked on
- Status transitions are manual or non-existent
- No visibility into what's actually being worked on

The solution: **hook-based state machine enforcement**. State changes happen in code, not in LLM prompts.

---

## Approach

1. Create shared library: `.claude/hooks/lib/task-state-machine.sh`
   - Define state constants
   - State transition validation
   - Transition logging

2. Create claim hook: `.claude/hooks/lib/task-claim.sh`
   - Find task from current directory
   - Update status to "claimed"
   - Set claim timestamp, claimer agent

3. Create completion hook: `.claude/hooks/lib/task-complete.sh`
   - Validate success criteria met
   - Update status to "completed"
   - Set completion timestamp

4. Integrate with existing hooks:
   - SessionStart: call task-claim.sh
   - PreToolUse: validate task is claimed
   - SessionEnd: call task-complete.sh if criteria met

---

## Files to Create

```
.claude/hooks/lib/
├── task-state-machine.sh      # Core state machine logic
├── task-claim.sh              # Auto-claim task
├── task-complete.sh           # Auto-complete task
└── task-state-validator.sh    # Validate state transitions
```

---

## State Machine Definition

```
States:
  - pending      # Task created, not started
  - claimed      # Agent has claimed task
  - in_progress  # Actively being worked on
  - completed    # Success criteria met
  - failed       # Failed/com abandoned
  - archived     # Moved to completed/

Transitions:
  pending → claimed        (on SessionStart)
  claimed → in_progress    (on first tool use)
  in_progress → completed  (on SessionEnd if criteria met)
  in_progress → failed     (on explicit failure)
  completed → archived     (on archival)
```

---

## Integration Points

- **SessionStart**: Detect if in task directory, auto-claim
- **PreToolUse**: Validate task state allows tool use
- **Stop**: Checkpoint current state
- **SessionEnd**: Transition to completed if criteria met

---

## Testing

Test with a dummy task:
1. Create test task
2. Start session in task directory
3. Verify auto-claim
4. Do some work
5. End session
6. Verify auto-complete

---

## Rollback Strategy

- Keep backup of any modified files
- State transitions are logged, can be manually reverted
- If automation fails, manual status updates still work

---

## Notes

This is the foundation. Get this right and everything else builds on it.
Coordinate with IG-010 - they may be building similar infrastructure.
