# Scout Report: Lifecycle Management Analysis

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Lifecycles Analyzed

### 1. Task Lifecycle

**Current Flow:**
```
Created → Active → In Progress → Complete/Blocked → Archived
   ↓         ↓          ↓              ↓
task.md   queue.yaml  events.yaml   timeline.yaml
```

**Issues Found:**
- **Orphaned tasks** - Tasks in queue.yaml that don't exist in tasks/active/
- **No cleanup** - Completed tasks accumulate in events.yaml (2830+ events)
- **State inconsistency** - task.md status may not match queue.yaml status
- **No archival process** - Old tasks stay in active/ indefinitely

---

### 2. Run Lifecycle

**Current Flow:**
```
Created → Active → Complete → (No cleanup)
   ↓         ↓         ↓
runs/    THOUGHTS.md  RESULTS.md
```

**Issues Found:**
- **Resource accumulation** - Run folders never cleaned up
- **No retention policy** - All runs kept forever
- **Orphaned runs** - Runs without corresponding tasks

---

### 3. Agent Lifecycle

**Current Flow:**
```
Hook Start → Agent Runs → Hook Stop
    ↓              ↓           ↓
event logged   (work done)  event logged
```

**Issues Found:**
- **No agent state tracking** - Can't tell if agent is running
- **Agent identity lost** - All events show "unknown" agent
- **No cleanup on failure** - Failed agents don't clean up state

---

### 4. Goal/Plan Lifecycle

**Current Flow:**
```
Active → In Progress → Complete
   ↓          ↓            ↓
goals/    plans/      (archived?)
```

**Issues Found:**
- **No automatic progression** - Goals don't update based on task completion
- **Orphaned plans** - Plans without active goals
- **No archival** - Old goals/plans accumulate

---

### 5. Event Lifecycle

**Current Flow:**
```
Created → Logged → (Never cleaned up)
   ↓         ↓
hook     events.yaml
```

**Issues Found:**
- **Unbounded growth** - events.yaml grows forever (2830+ events)
- **No retention policy** - Old events never purged
- **No aggregation** - Raw events, no summaries

---

## Structural Issues Summary

| Resource | Issue | Impact |
|----------|-------|--------|
| Tasks | Orphaned, inconsistent state | Confusion about what's real |
| Runs | No cleanup, unbounded growth | Disk space, clutter |
| Agents | No state tracking | Can't monitor agent health |
| Goals/Plans | No auto-progression | Stale goals |
| Events | Unbounded growth, no retention | Performance, noise |

---

## Recommendations

1. **Implement Resource Cleanup**
   - Automated archival of old tasks/runs
   - Retention policies (e.g., keep 30 days)

2. **Add Lifecycle State Machines**
   - Clear states for each resource type
   - Valid transitions enforced

3. **Create Lifecycle Hooks**
   - on_create, on_complete, on_archive
   - Automated cleanup actions

4. **Implement Event Retention**
   - Aggregate old events
   - Purge after retention period
