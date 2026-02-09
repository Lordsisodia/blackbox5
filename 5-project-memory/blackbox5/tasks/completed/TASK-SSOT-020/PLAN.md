# PLAN.md: Single Timeline Source

**Task:** TASK-SSOT-020 - Timeline data in timeline.yaml and run folders
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 65 (Medium-High)

---

## 1. First Principles Analysis

### The Core Problem
Timeline data exists in multiple places:
- `5-project-memory/blackbox5/timeline.yaml` - High-level timeline
- `5-project-memory/blackbox5/runs/**/timeline.yaml` - Per-run timelines
- `5-project-memory/blackbox5/runs/**/THOUGHTS.md` - Implicit timeline
- Task files with timestamps

This creates:
1. **Fragmented History**: Timeline spread across files
2. **Inconsistency**: Different events in different timelines
3. **Maintenance Overhead**: Updates needed in multiple places
4. **Query Complexity**: Hard to get complete timeline

### First Principles Solution
- **Central Timeline**: Single canonical timeline
- **Event Sourcing**: Timeline derived from events
- **Immutable Entries**: Timeline entries never modified
- **Indexed Access**: Efficient querying by date, type, entity

---

## 2. Current State Analysis

### Timeline Locations

| Location | Content Type |
|----------|-------------|
| `timeline.yaml` | Milestones, goals, phases |
| `runs/**/timeline.yaml` | Run-specific events |
| `runs/**/THOUGHTS.md` | Timestamped thoughts |
| Task files | Task lifecycle events |

### Issues

1. **Multiple Timelines**: 3+ timeline sources
2. **No Aggregation**: Can't see complete project timeline
3. **Manual Updates**: timeline.yaml manually maintained

---

## 3. Proposed Solution

### Decision: Central Timeline with Event Sourcing

**File:** `5-project-memory/blackbox5/timeline.yaml` (restructured)

```yaml
version: "2.0"
description: "Central project timeline - generated from events"
last_updated: "2026-02-05T10:00:00Z"

# Timeline entries (sorted by timestamp)
entries:
  - id: "tl-2026020501"
    timestamp: "2026-02-05T09:00:00Z"
    type: "task.created"
    entity_id: "TASK-001"
    entity_type: "task"
    title: "Task created"
    description: "Task TASK-001 created by user"
    source: "event.evt-2026020501"

  - id: "tl-2026020502"
    timestamp: "2026-02-05T09:05:00Z"
    type: "task.started"
    entity_id: "TASK-001"
    entity_type: "task"
    title: "Task started"
    description: "Task TASK-001 started by agent"
    source: "event.evt-2026020502"

  - id: "tl-2026020503"
    timestamp: "2026-02-05T09:30:00Z"
    type: "task.completed"
    entity_id: "TASK-001"
    entity_type: "task"
    title: "Task completed"
    description: "Task TASK-001 completed successfully"
    source: "event.evt-2026020503"

  - id: "tl-2026020504"
    timestamp: "2026-02-05T10:00:00Z"
    type: "milestone.reached"
    entity_id: "M-001"
    entity_type: "milestone"
    title: "Phase 1 Complete"
    description: "All Phase 1 tasks completed"
    source: "derived"

# Views (generated from entries)
views:
  milestones:
    - id: "M-001"
      title: "Phase 1 Complete"
      completed_at: "2026-02-05T10:00:00Z"

  phases:
    - name: "Phase 1"
      started_at: "2026-02-01T00:00:00Z"
      completed_at: "2026-02-05T10:00:00Z"
      status: "completed"

# Statistics (generated)
stats:
  total_events: 150
  tasks_completed_this_week: 12
  current_phase: "Phase 2"
```

### Implementation Plan

#### Phase 1: Create Timeline Generator (2 hours)

**File:** `2-engine/.autonomous/bin/generate-timeline.py`

```python
#!/usr/bin/env python3
"""Generate timeline from events and run data."""

import yaml
from pathlib import Path
from datetime import datetime

def generate_timeline(project_path: Path) -> dict:
    """Generate timeline from events and run data."""
    timeline = {
        'version': '2.0',
        'description': 'Central project timeline',
        'last_updated': datetime.now().isoformat(),
        'entries': [],
        'views': {'milestones': [], 'phases': []},
        'stats': {}
    }

    # Load central event log
    events = load_events(project_path)

    # Convert events to timeline entries
    for event in events:
        entry = {
            'id': f"tl-{event['id']}",
            'timestamp': event['timestamp'],
            'type': event['type'],
            'entity_id': event.get('entity_id'),
            'entity_type': event.get('entity_type'),
            'title': generate_title(event),
            'description': generate_description(event),
            'source': f"event.{event['id']}"
        }
        timeline['entries'].append(entry)

    # Sort by timestamp
    timeline['entries'].sort(key=lambda e: e['timestamp'])

    # Generate views
    timeline['views'] = generate_views(timeline['entries'])

    # Calculate stats
    timeline['stats'] = calculate_stats(timeline['entries'])

    return timeline

def generate_title(event: dict) -> str:
    """Generate human-readable title for event."""
    event_type = event['type']
    entity_id = event.get('entity_id', 'unknown')

    titles = {
        'task.created': f"Task {entity_id} created",
        'task.started': f"Task {entity_id} started",
        'task.completed': f"Task {entity_id} completed",
        'task.failed': f"Task {entity_id} failed",
        'goal.created': f"Goal {entity_id} created",
        'goal.completed': f"Goal {entity_id} achieved"
    }

    return titles.get(event_type, f"{event_type}: {entity_id}")

def generate_views(entries: list) -> dict:
    """Generate timeline views from entries."""
    views = {'milestones': [], 'phases': []}

    # Extract milestones
    for entry in entries:
        if entry['type'] == 'milestone.reached':
            views['milestones'].append({
                'id': entry['entity_id'],
                'title': entry['title'],
                'completed_at': entry['timestamp']
            })

    return views

def calculate_stats(entries: list) -> dict:
    """Calculate timeline statistics."""
    return {
        'total_events': len(entries),
        'tasks_completed_this_week': count_recent_tasks(entries, days=7),
        'current_phase': determine_current_phase(entries)
    }
```

#### Phase 2: Migrate Existing Data (1 hour)

1. Run generator on existing data
2. Verify timeline accuracy
3. Handle edge cases

#### Phase 3: Update Event Publishing (1 hour)

Ensure all events are published to central event log:
- Task lifecycle events
- Goal events
- Run events
- System events

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/bin/generate-timeline.py` - Timeline generator

### Modified Files
1. `5-project-memory/blackbox5/timeline.yaml` - Replace with generated version
2. Event publishing code

---

## 5. Success Criteria

- [ ] Timeline generator created
- [ ] timeline.yaml generated from events
- [ ] All historical events included
- [ ] Views generated correctly
- [ ] Stats calculated accurately
- [ ] Documentation updated

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore manual timeline.yaml
2. **Fix**: Debug generator script
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Generator | 2 hours | 2 hours |
| Phase 2: Migration | 1 hour | 3 hours |
| Phase 3: Event Publishing | 1 hour | 4 hours |
| **Total** | | **3-4 hours** |

---

*Plan created based on SSOT violation analysis - Timeline data fragmented*
