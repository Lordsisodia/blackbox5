# SUBTASK-004A: Create Health Monitor Core Library

**Parent Task:** TASK-AUTONOMY-004
**Status:** in_progress
**Priority:** CRITICAL
**Estimated Tokens:** 40K

---

## Objective

Build the foundational Python library that all health monitoring tools will use. This includes data collectors, health calculators, database interface, and stuck task detection.

---

## Success Criteria

- [ ] Data collectors read all YAML/JSON sources correctly
- [ ] Health score calculator produces 0-100 score matching metrics-dashboard.yaml
- [ ] Stuck task detector identifies tasks >2x estimated time
- [ ] SQLite database schema created with proper indexes
- [ ] All components have unit tests

---

## Implementation Plan

### Step 1: Project Structure (5K tokens)
Create directory structure and __init__.py files

```
~/.blackbox5/bin/lib/health_monitor/
├── __init__.py
├── config.py          # Paths and constants
├── collectors.py      # Data collection from YAML/JSON
├── calculators.py     # Health score and metric calculations
├── database.py        # SQLite interface
├── models.py          # Data classes (Task, Agent, Event)
└── utils.py           # Helper functions
```

### Step 2: Configuration Module (3K tokens)
Create `config.py` with all file paths:
- BB5 base directory detection
- All data source paths
- Default thresholds (heartbeat timeout, stuck task multiplier)
- Database path

### Step 3: Data Models (5K tokens)
Create `models.py` with dataclasses:
- `Task` (id, status, priority, estimated_minutes, etc.)
- `Agent` (name, last_seen, status, loop_number)
- `Event` (timestamp, type, task_id, agent)
- `HealthSnapshot` (overall score, components, timestamp)
- `Metric` (name, value, unit, timestamp)

### Step 4: Data Collectors (10K tokens)
Create `collectors.py` with functions:
- `collect_queue()` - Parse queue.yaml into Task objects
- `collect_heartbeat()` - Parse heartbeat.yaml into Agent objects
- `collect_events(limit=100)` - Parse events.yaml into Event objects
- `collect_metrics()` - Parse metrics-dashboard.yaml
- `collect_skills()` - Parse skill-registry.yaml
- `collect_run_metrics()` - Scan runs/*/metrics.json

Each collector should:
- Handle missing files gracefully
- Validate data structure
- Return typed objects
- Log errors but not fail

### Step 5: Health Calculators (8K tokens)
Create `calculators.py` with functions:
- `calculate_health_score()` - Composite 0-100 score
  - throughput: 25% (tasks/day vs target)
  - quality: 25% (success rate)
  - efficiency: 20% (time saved)
  - reliability: 15% (uptime)
  - roi: 15% (value/cost)
- `calculate_queue_health()` - Pending/in_progress ratio
- `calculate_agent_health()` - Heartbeat freshness
- `calculate_throughput()` - Tasks completed per day

### Step 6: Stuck Task Detector (5K tokens)
Create detection logic in `calculators.py`:
- `detect_stuck_tasks(tasks, events)` - Find in_progress tasks with no recent activity
- Logic:
  1. Find all tasks with status="in_progress"
  2. Find last event for each task
  3. Calculate elapsed time since last event
  4. Compare to estimated_minutes * 2
  5. Return list of stuck Task objects with reason

### Step 7: Database Module (8K tokens)
Create `database.py` with SQLite interface:
- `init_database()` - Create tables and indexes
- `save_snapshot(snapshot)` - Store health snapshot
- `save_metric(metric)` - Store time-series metric
- `get_recent_snapshots(hours=24)` - Query history
- `get_metrics_range(start, end)` - Query metrics

Schema:
```sql
CREATE TABLE snapshots (
    id INTEGER PRIMARY KEY,
    timestamp INTEGER NOT NULL,
    health_score INTEGER NOT NULL,
    queue_pending INTEGER,
    queue_in_progress INTEGER,
    queue_completed INTEGER,
    agents_online INTEGER,
    agents_stale INTEGER
);

CREATE TABLE metrics (
    id INTEGER PRIMARY KEY,
    timestamp INTEGER NOT NULL,
    name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT
);

CREATE INDEX idx_snapshots_time ON snapshots(timestamp);
CREATE INDEX idx_metrics_time_name ON metrics(timestamp, name);
```

### Step 8: Unit Tests (6K tokens)
Create `tests/test_health_monitor.py`:
- Test each collector with sample data
- Test calculator functions
- Test database operations
- Mock file system for isolated tests

---

## Files to Create

1. `~/.blackbox5/bin/lib/health_monitor/__init__.py`
2. `~/.blackbox5/bin/lib/health_monitor/config.py`
3. `~/.blackbox5/bin/lib/health_monitor/models.py`
4. `~/.blackbox5/bin/lib/health_monitor/collectors.py`
5. `~/.blackbox5/bin/lib/health_monitor/calculators.py`
6. `~/.blackbox5/bin/lib/health_monitor/database.py`
7. `~/.blackbox5/bin/lib/health_monitor/utils.py`
8. `~/.blackbox5/bin/lib/health_monitor/tests/test_collectors.py`
9. `~/.blackbox5/bin/lib/health_monitor/tests/test_calculators.py`
10. `~/.blackbox5/bin/lib/health_monitor/tests/test_database.py`

---

## Testing

```python
# Test the core library
from health_monitor import collect_queue, calculate_health_score, detect_stuck_tasks

# Should work without errors
tasks = collect_queue()
score = calculate_health_score()
stuck = detect_stuck_tasks(tasks, events)

print(f"Health Score: {score}/100")
print(f"Stuck Tasks: {len(stuck)}")
for task in stuck:
    print(f"  - {task.id}: {task.reason}")
```

---

## Definition of Done

- [ ] All 10 files created
- [ ] Unit tests pass
- [ ] Can import and use library from Python
- [ ] Handles missing files gracefully
- [ ] Stuck task detection finds actual stuck tasks in current queue
- [ ] Health score matches metrics-dashboard.yaml calculation
