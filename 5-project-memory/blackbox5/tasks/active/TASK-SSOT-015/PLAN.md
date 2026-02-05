# PLAN.md: Create Central Trigger Rules Registry

**Task:** TASK-SSOT-015 - Trigger rules scattered in multiple files
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 65 (Medium-High)

---

## 1. First Principles Analysis

### The Core Problem
Trigger rules (when to run what) are scattered across:
- `5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml`
- `5-project-memory/blackbox5/.autonomous/context/routes.yaml`
- Various agent configuration files
- Hook scripts with embedded logic

This creates:
1. **Discovery Difficulty**: Hard to find all triggers
2. **Inconsistent Logic**: Same event triggers different actions
3. **Maintenance Overhead**: Updates needed in multiple places
4. **Debugging Complexity**: Hard to trace trigger chains

### First Principles Solution
- **Central Registry**: Single location for all trigger rules
- **Explicit Rules**: Clear condition → action mappings
- **Priority System**: Well-defined rule precedence
- **Validation**: Check for conflicts and duplicates

---

## 2. Current State Analysis

### Trigger Locations

| Location | Trigger Type | Examples |
|----------|--------------|----------|
| events.yaml | Event-based | on_task_complete, on_error |
| routes.yaml | Route-based | path patterns |
| agent configs | Agent-specific | scout triggers |
| hook scripts | Script-based | pre-task, post-task |

### Issues

1. **Scattered Logic**: Triggers defined in 4+ places
2. **No Overview**: Can't see all triggers at once
3. **Conflicts Possible**: Same event handled differently

---

## 3. Proposed Solution

### Decision: Central Trigger Registry

**File:** `5-project-memory/blackbox5/.autonomous/triggers.yaml`

```yaml
version: "1.0"
description: "Central trigger rules registry"

# Event-based triggers
event_triggers:
  - id: "trigger-001"
    name: "On Task Complete"
    event: "task.completed"
    conditions:
      - "task.status == 'completed'"
    actions:
      - type: "update_timeline"
      - type: "notify"
        target: "telegram"
    priority: 1

  - id: "trigger-002"
    name: "On High Priority Task"
    event: "task.created"
    conditions:
      - "task.priority == 'CRITICAL'"
    actions:
      - type: "notify"
        target: "telegram"
      - type: "escalate"
    priority: 2

# Route-based triggers
route_triggers:
  - id: "trigger-003"
    pattern: "/tasks/active/*/PLAN.md"
    action: "validate_plan"

# Schedule-based triggers
schedule_triggers:
  - id: "trigger-004"
    name: "Daily Health Check"
    schedule: "0 9 * * *"  # 9 AM daily
    action: "run_health_check"

# Agent-specific triggers
agent_triggers:
  scout:
    - id: "trigger-005"
      condition: "task.type == 'analysis'"
      action: "run_scout"
```

### Implementation Plan

#### Phase 1: Audit Existing Triggers (1 hour)

1. Read all current trigger definitions
2. Document each trigger's:
   - Condition/event
   - Action
   - Current location
3. Identify conflicts and duplicates

#### Phase 2: Design Registry Schema (1 hour)

1. Define trigger types (event, route, schedule, agent)
2. Define condition syntax
3. Define action types
4. Define priority system

#### Phase 3: Create Registry (1 hour)

**File:** `5-project-memory/blackbox5/.autonomous/triggers.yaml`

Migrate all triggers to central registry with:
- Unique IDs
- Clear conditions
- Explicit actions
- Priority levels

#### Phase 4: Update Trigger Engine (1 hour)

**Update:** Trigger execution system

```python
def evaluate_triggers(event: dict) -> list:
    """Evaluate all triggers for an event."""
    registry = load_trigger_registry()
    triggered = []

    for trigger in registry['event_triggers']:
        if matches_conditions(event, trigger['conditions']):
            triggered.append(trigger)

    # Sort by priority
    triggered.sort(key=lambda t: t.get('priority', 0))

    return triggered
```

---

## 4. Files to Modify

### New Files
1. `5-project-memory/blackbox5/.autonomous/triggers.yaml` - Central registry

### Modified Files
1. Event handling code
2. Route handling code
3. Agent initialization

---

## 5. Success Criteria

- [ ] Central triggers.yaml created
- [ ] All triggers migrated from scattered locations
- [ ] Trigger engine updated to use registry
- [ ] No duplicate trigger definitions
- [ ] Documentation updated

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore original trigger definitions
2. **Fix**: Debug registry loading
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Audit | 1 hour | 1 hour |
| Phase 2: Schema | 1 hour | 2 hours |
| Phase 3: Registry | 1 hour | 3 hours |
| Phase 4: Engine | 1 hour | 4 hours |
| **Total** | | **3-4 hours** |

---

*Plan created based on SSOT violation analysis - Trigger rules scattered*
