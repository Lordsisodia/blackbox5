# SSOT Agent State Violations Report

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Critical Finding: 529 Instances of "agent_type: unknown"

The events.yaml file contains **529 occurrences** of `agent_type: unknown` and `agent_id: unknown`, indicating a fundamental SSOT violation in agent identity tracking.

---

## ALL Places Agent State is Stored

### 1. Agent Identity Storage (VIOLATION: Multiple Sources)

| Location | Purpose | Current State |
|----------|---------|---------------|
| `events.yaml` | Event log | Contains 529 "unknown" agent types |
| `agent-state.yaml` | Agent registry | EMPTY: `agents: {}` |
| `protocol.yaml` | Protocol definition | Defines planner/executor IDs |
| Agent scripts | Hardcoded AGENT_NAME | scout, planner, analyzer |

**VIOLATION:** Agent identity exists in 4+ places with no synchronization:
- Events from hooks show `agent_type: unknown`
- Events from agent scripts show `agent: planner`, `agent: executor`
- agent-state.yaml is completely empty
- Protocol defines IDs that aren't used consistently

---

### 2. Agent Status Storage (VIOLATION: Inconsistent Status)

| Location | Status Type | Data |
|----------|-------------|------|
| `execution-state.yaml` | Slot status | 5 slots (idle/active/paused/error) |
| `agent-state.yaml` | Agent registry | EMPTY |
| `heartbeat.yaml` | Last seen | planner: loop 30, executor: loop 65 |
| `events.yaml` | Lifecycle events | agent_start/agent_stop (530 events) |

**VIOLATION:** Status is tracked in 4 places:
- heartbeat.yaml shows planner on loop 30, executor on loop 65
- execution-state.yaml shows all slots idle
- events.yaml shows recent agent_start/stop events
- These are NOT consistent with each other

---

### 3. Agent Run Data Storage (VIOLATION: Duplicated Run Info)

| Location | Run Data |
|----------|----------|
| `planner/runs/run-*/metadata.yaml` | Loop number, agent, timestamps |
| `executor/runs/run-*/metadata.yaml` | Loop number, agent, timestamps |
| `events.yaml` | References run_id in events |
| `heartbeat.yaml` | References run_number |

**Example Duplication:**
- Run 0074 metadata: `agent: planner`, `loop: 25`
- Same run referenced in heartbeat: `planner: run_number: 79`
- Events reference: `run_id: executor-test-001`

---

### 4. Agent Output Storage (VIOLATION: Multiple Formats)

| Location | Output Type |
|----------|-------------|
| `planner/runs/run-*/THOUGHTS.md` | Agent thoughts |
| `planner/runs/run-*/RESULTS.md` | Agent results |
| `planner/runs/run-*/DECISIONS.md` | Agent decisions |
| `planner/runs/run-*/LEARNINGS.md` | Agent learnings |
| `.autonomous/analysis/scout-reports/` | Scout analysis |
| `events.yaml` | Event stream |

---

## Specific Examples of Inconsistencies

### Example 1: Agent Identity Mismatch
```yaml
# events.yaml (lines 85-92)
- timestamp: '2026-02-04T09:45:04+07:00'
  type: agent_stop
  agent_type: unknown      # <-- From hook
  agent_id: unknown
  source: hook

# vs agent scripts
AGENT_NAME="planner"       # <-- Hardcoded in planner-agent.sh
```

### Example 2: Status Inconsistency
```yaml
# heartbeat.yaml
heartbeats:
  planner:
    status: in_progress_TASK-1738375002
    loop_number: 30
  executor:
    status: in_progress_TASK-1738375002
    loop_number: 65

# execution-state.yaml
execution_slots:
  slot_1:
    status: "idle"        # <-- Says idle
  slot_2:
    status: "idle"
```

### Example 3: Empty Authoritative Source
```yaml
# agent-state.yaml
agents: {}                # <-- Completely empty!
metadata:
  last_updated: '2026-02-01T13:33:22.747638+00:00'
```

---

## Root Cause Analysis

1. **Hook System Doesn't Know Agent Identity**: The hooks logging to events.yaml don't have access to agent context, so they log "unknown"

2. **No Central Agent Registry**: agent-state.yaml should be the SSOT but it's empty

3. **Multiple Write Paths**:
   - Agent scripts write to heartbeat.yaml
   - Hooks write to events.yaml
   - Execution system writes to execution-state.yaml
   - None coordinate

4. **Protocol Defines But Doesn't Enforce**: protocol.yaml defines agent IDs but there's no enforcement mechanism

---

## Recommendations for SSOT

### Immediate (High Priority)
1. **Populate agent-state.yaml** as the single registry of active agents
2. **Update hooks** to read agent identity from environment variable or state file
3. **Create agent registration protocol** - agents must register on start

### Short-term
1. **Consolidate status tracking** - heartbeat.yaml OR execution-state.yaml, not both
2. **Standardize event format** - all events must include valid agent_type/agent_id
3. **Add validation** - reject events with "unknown" agent data

### Long-term
1. **Agent state service** - single API for all agent state operations
2. **Event sourcing** - all state changes flow through events.yaml
3. **Automated reconciliation** - periodic sync checks between state files
