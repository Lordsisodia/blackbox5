# Unified Agent Communication System

## Overview

The Unified Agent Communication System consolidates the previously dual communication mechanisms into a single, consistent protocol that both Python and Bash agents can use.

## Problem Solved

**Before (Dual System):**
- Python agents (engine): Wrote JSON/YAML report files to `.autonomous/analysis/`
- Bash agents (project): Appended events to `events.yaml`
- No cross-system event visibility
- Fragmented workflow tracing

**After (Unified System):**
- All agents (Python and Bash) write to `events.yaml`
- Consistent event schema
- Full workflow traceability
- Single source of truth

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│  Python Agents  │     │   Bash Agents   │
│  (scout, etc)   │     │  (planner, etc) │
└────────┬────────┘     └────────┬────────┘
         │                       │
         │  Unified API          │  Direct YAML
         │  (storage.py)         │  (shell commands)
         │                       │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │    events.yaml        │
         │  (Canonical Log)      │
         └───────────────────────┘
```

## Components

### 1. CommunicationRepository (storage.py)

The `CommunicationRepository` class provides a unified interface for logging and querying events.

**Location:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/lib/storage.py`

**Key Methods:**

```python
# Log events
storage.communication.log_event(event_type, agent_id, data, task_id, message)
storage.communication.log_agent_start(agent_id, message, task_id, data)
storage.communication.log_agent_complete(agent_id, message, task_id, data)
storage.communication.log_agent_error(agent_id, message, task_id, error_details)
storage.communication.log_task_started(agent_id, task_id, message, data)
storage.communication.log_task_completed(agent_id, task_id, message, data)
storage.communication.log_task_failed(agent_id, task_id, message, error_details)
storage.communication.log_task_blocked(agent_id, task_id, message, reason)
storage.communication.log_discovery(agent_id, message, data, task_id)
storage.communication.log_decision(agent_id, message, decision, rationale, task_id)

# Query events
storage.communication.get_events(agent_id=None, event_type=None, task_id=None, since=None)
storage.communication.get_recent_events(count=10)
storage.communication.get_event_count(agent_id=None, event_type=None)
```

### 2. Convenience Functions

For simple use cases, use the convenience functions:

```python
from storage import (
    log_event,
    log_agent_start,
    log_agent_complete,
    log_agent_error,
    log_task_started,
    log_task_completed,
    log_task_failed,
    get_events,
    get_recent_events
)

# Log an event
log_agent_start("scout-intelligent", "Starting analysis")

# Log task progress
log_task_started("executor", "TASK-001")
log_task_completed("executor", "TASK-001", data={"files_modified": 3})

# Query events
recent = get_recent_events(count=5)
executor_events = get_events(agent_id="executor")
```

### 3. Event Logger Module (event_logger.py)

Legacy compatibility module for existing agents.

**Location:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/lib/event_logger.py`

Provides the same interface as the engine's event_logger for backward compatibility.

## Event Schema

All events follow a consistent schema:

```yaml
- timestamp: "2026-02-07T12:00:00Z"     # ISO 8601 format
  type: "agent_start"                   # Event type
  agent: "scout-intelligent"            # Agent ID
  task_id: "TASK-001"                   # Related task (optional)
  message: "Analysis started"           # Human-readable message (optional)
  data:                                 # Structured data (optional)
    report_id: "20260207-120000"
    parallel: true
```

### Event Types

| Type | Description | Used By |
|------|-------------|---------|
| `agent_start` | Agent began execution | All agents |
| `agent_complete` | Agent finished successfully | All agents |
| `agent_error` | Agent encountered an error | All agents |
| `task_started` | Task execution began | Executor |
| `task_completed` | Task finished successfully | Executor |
| `task_failed` | Task failed | Executor |
| `task_blocked` | Task hit a blocker | Executor |
| `discovery` | New information found | Scout |
| `decision_made` | Significant decision recorded | Planner |

## Migration Guide

### For Python Agents

**Before:**
```python
# Old way - write report files only
def save_report(report, output_dir):
    yaml_file = output_dir / f"report-{report.id}.yaml"
    with open(yaml_file, 'w') as f:
        yaml.dump(asdict(report), f)
```

**After:**
```python
# New way - write report AND log events
from storage import log_agent_start, log_agent_complete

def main():
    # Log start
    log_agent_start("my-agent", "Starting work", data={"task_id": "TASK-001"})

    # Do work...
    report = generate_report()

    # Save report (for detailed data)
    save_report(report, output_dir)

    # Log completion
    log_agent_complete("my-agent", "Work complete", data={"report_id": report.id})
```

### For Bash Agents

No changes required. Bash agents continue to append to events.yaml directly:

```bash
# Bash agent event logging (unchanged)
echo "- timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> events.yaml
echo "  type: agent_start" >> events.yaml
echo "  agent: planner" >> events.yaml
```

## Canonical Event Location

**Primary:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml`

This is the single source of truth for all agent communication.

## Backward Compatibility

- Old report files in `.autonomous/analysis/` are still supported
- The `event_logger.py` module provides API compatibility
- Both systems can coexist during migration

## Testing

Test the unified communication:

```python
from storage import get_storage, log_agent_start, get_events

# Test logging
storage = get_storage()
storage.communication.log_agent_start("test-agent", "Test message")

# Test querying
events = storage.communication.get_events(agent_id="test-agent")
print(f"Found {len(events)} events")
```

## Benefits

1. **Unified Visibility**: All agent activity in one place
2. **Workflow Tracing**: Complete audit trail from scout to verifier
3. **Simplified Debugging**: Single log to check for issues
4. **Consistent API**: Same interface for Python and Bash agents
5. **Extensible**: Easy to add new event types and agents

## Future Enhancements

- SQLite backend for high-volume event storage
- Event subscriptions for real-time monitoring
- Event aggregation and analytics
- Integration with external monitoring systems
