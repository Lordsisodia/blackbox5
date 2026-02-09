# Timeline Architecture

## Overview

The BlackBox5 timeline system uses a **Single Source of Truth (SSOT)** pattern to eliminate duplicate data and ensure consistency.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ROOT TIMELINE                            │
│              ~/blackbox5/timeline.yaml                      │
│                                                             │
│  - All events stored here                                   │
│  - Canonical source of truth                                │
│  - Events tagged with related_items for filtering           │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  GOAL VIEWS     │ │  PLAN VIEWS     │ │  QUERY SYSTEM   │
│                 │ │                 │ │                 │
│ timeline.yaml   │ │ timeline.yaml   │ │ grep, search    │
│ (view def)      │ │ (view def)      │ │ filter tools    │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## File Structure

### Root Timeline (Canonical)
**Location:** `~/blackbox5/timeline.yaml`

Contains:
- `project`: Project metadata
- `milestones`: Major achievements
- `events`: All timeline events with `related_items` for linking
- `progress`: Completion metrics
- `phases`: Project phase tracking

### Goal Timeline Views
**Location:** `~/blackbox5/goals/active/IG-*/timeline.yaml`

Contains:
- `view_definition`: Filter criteria to extract relevant events
- `query_instructions`: How to view events for this goal
- Reference to canonical source

## Event Format

```yaml
events:
  - date: "2026-02-07"
    type: "milestone"          # milestone|decision|process|analysis|infrastructure
    title: "Event Title"
    description: "Detailed description"
    impact: "high"             # high|medium|low
    related_items:             # Links to goals, tasks, plans
      - "IG-001"
      - "TASK-123"
```

## Query/Filter System

### Manual Query
```bash
# View all events for a goal
grep -B 5 -A 10 "IG-001" ~/blackbox5/timeline.yaml

# View events by date
grep -A 8 "2026-02-04" ~/blackbox5/timeline.yaml

# View high-impact events
grep -B 2 -A 8 'impact: "high"' ~/blackbox5/timeline.yaml
```

### Programmatic Access
```python
import yaml

with open('timeline.yaml') as f:
    timeline = yaml.safe_load(f)

# Filter by goal
goal_events = [e for e in timeline['events']
               if 'IG-001' in (e.get('related_items') or [])]
```

## Migration History

**Date:** 2026-02-07
**Task:** TASK-SSOT-020

### Changes Made
1. Merged all goal timeline events into root timeline.yaml
2. Added 16 unique goal events to root timeline
3. Converted 8 goal timeline files to view definitions
4. Documented query/filter system

### Before
- Root timeline.yaml: ~2500 lines
- Goal timelines: Duplicate events in different formats
- Problem: Same events in multiple places

### After
- Root timeline.yaml: ~2600 lines (canonical source)
- Goal timelines: View definitions only (30 lines each)
- Result: Single source of truth

## Best Practices

1. **Always add events to root timeline.yaml**
2. **Tag events with related_items** for proper filtering
3. **Use view definitions** to see goal-specific events
4. **Never add duplicate events** to goal timelines

## Future Enhancements

- [ ] Automated view generation from root timeline
- [ ] CLI command: `bb5 timeline:view IG-001`
- [ ] Web dashboard with filter UI
- [ ] Event validation on commit
