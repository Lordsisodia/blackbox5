# Learning: Communication Unification

**Task:** TASK-ARCH-066
**Date:** 2026-02-06
**Category:** Architecture

---

## What Worked Well

- Event-driven architecture was the right choice
- Creating `event_logger.py` module provided clean abstraction
- Python agents could easily emit events in same format as bash agents
- Unified event schema enabled traceability across agent workflows

## What Was Harder Than Expected

- Migrating multiple Python agents (scout, executor, improvement-loop) took coordination
- Ensuring events were visible to bash agents required careful path handling
- Maintaining consistency between Python dicts and YAML event format

## What Would You Do Differently

- Design the event schema first before implementing
- Create the CommunicationBus class earlier (was in plan but simplified)
- Add trace IDs from the start for better workflow tracking

## Technical Insights

```yaml
# Effective unified event format
- timestamp: "2026-02-06T12:00:00Z"
  agent: scout-intelligent
  type: start|complete|error|task_started|task_completed|task_failed|in_progress
  message: "..."
  run_dir: "..."
  task_id: "..."
  data: {}
```

## Process Improvements

- Standardize on events.yaml as single source of truth for agent activity
- Create helper functions for common event types (start, complete, error)
- Document the event schema for future agent developers

## Key Takeaway

A unified communication protocol enables better observability and coordination across heterogeneous agent systems.
