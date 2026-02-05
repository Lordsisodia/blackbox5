# PLAN.md: Consolidate Events Storage

**Task:** TASK-SSOT-016 - Events stored in multiple formats/locations
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 60 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Events are stored in multiple formats and locations:
- `5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml`
- `5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` (event-like entries)
- `5-project-memory/blackbox5/runs/**/events.yaml` (per-run events)
- `5-project-memory/blackbox5/timeline.yaml` (timeline events)

This creates:
1. **Fragmented History**: Event history spread across files
2. **Inconsistent Formats**: Different schemas in different files
3. **Query Complexity**: Hard to get complete event history
4. **Duplication**: Same event in multiple places

### First Principles Solution
- **Central Event Log**: Single append-only event log
- **Standard Schema**: Consistent event structure
- **Immutable History**: Events never modified, only appended
- **Indexed Access**: Efficient querying by type, time, entity

---

## 2. Current State Analysis

### Event Storage Locations

| Location | Format | Purpose |
|----------|--------|---------|
| `communications/events.yaml` | YAML | Agent communications |
| `communications/queue.yaml` | YAML | Queue events |
| `runs/**/events.yaml` | YAML | Per-run events |
| `timeline.yaml` | YAML | Timeline events |

### Issues

1. **4+ Event Stores**: Events scattered across files
2. **Different Schemas**: No consistent event format
3. **No Global View**: Can't see all events together

---

## 3. Proposed Solution

### Decision: Central Event Log

**File:** `5-project-memory/blackbox5/.autonomous/events.log.yaml`

```yaml
version: "1.0"
description: "Central event log - append only"

# Event schema definition
schema:
  event:
    required:
      - id
      - timestamp
      - type
      - source
    optional:
      - entity_id
      - entity_type
      - payload
      - metadata

# Events (append only)
events:
  - id: "evt-2026020501"
    timestamp: "2026-02-05T10:00:00Z"
    type: "task.created"
    source: "user"
    entity_id: "TASK-001"
    entity_type: "task"
    payload:
      title: "Fix bug"
      priority: "HIGH"

  - id: "evt-2026020502"
    timestamp: "2026-02-05T10:05:00Z"
    type: "task.started"
    source: "agent"
    entity_id: "TASK-001"
    entity_type: "task"
    payload:
      agent: "claude"
      run_id: "run-20260205_100500"

  - id: "evt-2026020503"
    timestamp: "2026-02-05T10:30:00Z"
    type: "task.completed"
    source: "agent"
    entity_id: "TASK-001"
    entity_type: "task"
    payload:
      status: "completed"
      duration_minutes: 25

# Indexes (generated)
indexes:
  by_type:
    task.created: ["evt-2026020501"]
    task.started: ["evt-2026020502"]
    task.completed: ["evt-2026020503"]
  by_entity:
    TASK-001: ["evt-2026020501", "evt-2026020502", "evt-2026020503"]
```

### Implementation Plan

#### Phase 1: Design Schema (1 hour)

Define:
- Event structure (required/optional fields)
- Event types (task, goal, run, system)
- Indexing strategy
- Migration approach

#### Phase 2: Create Migration Script (1 hour)

**File:** `2-engine/.autonomous/bin/migrate-events.py`

```python
#!/usr/bin/env python3
"""Migrate events from scattered locations to central log."""

import yaml
from pathlib import Path
from datetime import datetime

def migrate_events(project_path: Path):
    """Migrate all events to central log."""
    events = []

    # Migrate from communications/events.yaml
    comm_events = load_communications_events(project_path)
    events.extend(comm_events)

    # Migrate from queue.yaml
    queue_events = load_queue_events(project_path)
    events.extend(queue_events)

    # Migrate from run events
    run_events = load_run_events(project_path)
    events.extend(run_events)

    # Migrate from timeline
    timeline_events = load_timeline_events(project_path)
    events.extend(timeline_events)

    # Sort by timestamp
    events.sort(key=lambda e: e['timestamp'])

    # Assign IDs
    for i, event in enumerate(events, 1):
        event['id'] = f"evt-{event['timestamp'][:10].replace('-', '')}{i:04d}"

    # Write central log
    output = {
        'version': '1.0',
        'description': 'Central event log',
        'schema': {...},
        'events': events,
        'indexes': generate_indexes(events)
    }

    with open(project_path / '.autonomous' / 'events.log.yaml', 'w') as f:
        yaml.dump(output, f, default_flow_style=False)
```

#### Phase 3: Run Migration (1 hour)

1. Run migration script
2. Verify all events migrated
3. Validate event integrity

#### Phase 4: Update Event Publishing (1 hour)

**Update:** All code that publishes events

```python
def publish_event(event_type: str, entity_id: str, payload: dict):
    """Publish event to central log."""
    event = {
        'timestamp': datetime.now().isoformat(),
        'type': event_type,
        'source': get_current_agent(),
        'entity_id': entity_id,
        'entity_type': get_entity_type(entity_id),
        'payload': payload
    }

    append_to_event_log(event)
```

---

## 4. Files to Modify

### New Files
1. `5-project-memory/blackbox5/.autonomous/events.log.yaml` - Central event log
2. `2-engine/.autonomous/bin/migrate-events.py` - Migration script

### Modified Files
1. Event publishing code throughout codebase
2. Event reading/querying code

---

## 5. Success Criteria

- [ ] Central events.log.yaml created
- [ ] All events migrated from scattered locations
- [ ] Event publishing updated to use central log
- [ ] Indexes generated for efficient querying
- [ ] Documentation updated

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Keep old event files
2. **Fix**: Debug migration script
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Schema | 1 hour | 1 hour |
| Phase 2: Migration Script | 1 hour | 2 hours |
| Phase 3: Run Migration | 1 hour | 3 hours |
| Phase 4: Update Publishing | 1 hour | 4 hours |
| **Total** | | **3-4 hours** |

---

*Plan created based on SSOT violation analysis - Events stored in multiple locations*
