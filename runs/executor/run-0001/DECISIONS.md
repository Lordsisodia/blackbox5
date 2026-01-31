# Decisions - Idle Iteration

## Decision: Report Idle Status
**Context:** Queue.yaml contains no tasks
**Selected:** Record idle event, update heartbeat, await tasks
**Rationale:** Executor follows cycle - when no tasks available, report idle and wait for Planner to populate queue. This is normal behavior.
**Reversibility:** LOW - Idle event can be removed if needed, no system impact
