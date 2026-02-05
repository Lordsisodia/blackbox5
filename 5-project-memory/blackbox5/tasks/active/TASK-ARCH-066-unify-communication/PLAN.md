# PLAN.md: Unify Agent Communication

**Task:** TASK-ARCH-066
**Status:** pending
**Created:** 2026-02-06

## Objective
Unify fragmented agent communication (Python agents write reports, Bash agents emit events).

## Current State
- **Python Agents:** Write YAML/JSON reports to `.autonomous/analysis/`
- **Bash Agents:** Append events to `events.yaml` (4,096 lines)
- **Queue:** `queue.yaml` (1,974 lines) - project only
- **No Cross-System Events:** Python agents don't emit events

## Unification Strategy: Event-Driven with Report Registry

### Unified Event Schema (v2.0)
```yaml
- timestamp: "2026-02-06T12:00:00Z"
  event_id: "evt-uuid"
  type: "agent_start|agent_complete|report_generated"
  agent:
    id: "scout|planner|executor|verifier"
    type: "python|bash"
  task:
    id: "TASK-XXX-NNN"
    status: "pending|in_progress|completed"
  data:
    report_file: "path/to/report.yaml"
  context:
    trace_id: "trace-uuid"
```

### Report Registry
New file: `report-registry.yaml`
- Tracks all reports with event linkage
- Enables traceability

## Implementation Steps
1. Create CommunicationBus class (2 hours)
2. Update protocol.yaml to v2.0 (1 hour)
3. Migrate Python agents (scout, planner, executor, verifier) (3 hours)
4. Align Bash agents to v2.0 schema (1 hour)
5. Integration testing (2 hours)

## Timeline
- Total: 6-8 hours

## Success Criteria
- [ ] Single event bus (events.yaml) captures all activity
- [ ] Unified event schema documented
- [ ] All Python agents emit events
- [ ] Report registry tracks all reports
- [ ] Trace IDs enable workflow tracking
