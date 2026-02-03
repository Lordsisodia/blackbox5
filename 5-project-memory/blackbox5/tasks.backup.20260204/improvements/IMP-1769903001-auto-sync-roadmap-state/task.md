# IMP-1769903001: Implement Automatic Roadmap State Synchronization

**Type:** implement
**Priority:** high
**Category:** process
**Source Learning:** L-1769861933-001, L-1769813746-001, L-20260131-060933-L002, L-1769807450-001
**Status:** pending
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

- [ ] Post-task-completion hook updates STATE.yaml automatically
- [ ] Plan status changes from "planned" → "completed" when task finishes
- [ ] Dependencies unblocked automatically when plan completes
- [ ] next_action updated to next unblocked plan
- [ ] No manual STATE.yaml updates required for standard task completion

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

- [ ] Library created with update_plan_status(), unblock_dependents(), update_next_action()
- [ ] Task completion automatically triggers sync
- [ ] Tested with at least 2 plan completions
- [ ] Documentation updated
