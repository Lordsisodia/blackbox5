# TASK-ARCH-066: Unify Agent Communication System

**Status:** completed
**Priority:** HIGH
**Created:** 2026-02-06
**Completed:** 2026-02-06
**Type:** Structural Architecture

## Objective
Unify the two parallel agent communication systems (Python agents use report files, Bash agents use events.yaml/heartbeat.yaml) into a single, consistent protocol.

## Background
Scout analysis found two communication mechanisms:
1. **Python agents** (engine): Use JSON/YAML report files in `.autonomous/analysis/`
2. **Bash agents** (project): Use events.yaml + heartbeat.yaml in `.autonomous/agents/communications/`

This creates fragmentation and makes it hard to trace agent workflows.

## Current State

### Python Agents (Engine)
```
scout-intelligent.py → scout-report-*.yaml
planner-prioritize.py → task.md files
executor-implement.py → executor-report-*.yaml
verifier-validate.py → verifier-report-*.yaml
```

### Bash Agents (Project)
```
scout-agent.sh → events.yaml (event emitted)
analyzer-agent.sh → events.yaml (event emitted)
planner-agent.sh → events.yaml (event emitted)
```

## Proposed Unified Protocol

Option 1: **Event-Driven (Recommended)**
- All agents emit events to events.yaml
- All agents update heartbeat.yaml
- Consistent event schema

Option 2: **Report-Based**
- All agents create report files
- Standardized report schema
- Report registry tracks all reports

Option 3: **MCP Protocol**
- Use Model Context Protocol
- Agents communicate via MCP server
- Most scalable but most complex

## Success Criteria
- [x] Single communication protocol chosen (Event-Driven)
- [x] Python event_logger module created
- [x] scout-intelligent.py updated with event logging
- [x] executor-implement.py updated with event logging
- [x] improvement-loop.py updated with event logging
- [x] Events written in same format as bash agents
- [x] Events visible to bash agents
- [x] Unified communication achieved

## Implementation Summary

### Created
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/event_logger.py` - Python module for events.yaml logging

### Updated Python Agents
1. **scout-intelligent.py** - Added event logging at start, completion, errors
2. **executor-implement.py** - Added event logging for task started, completed, failed
3. **improvement-loop.py** - Added event logging for each phase and overall completion

### Event Format
```yaml
- timestamp: "2026-02-06T12:00:00Z"
  agent: scout-intelligent
  type: start|complete|error|task_started|task_completed|task_failed|in_progress
  message: "..."
  run_dir: "..."
  task_id: "..."
  data:
    ...
```

### Key Functions
- `log_event()` - Generic event logging
- `log_start()` - Agent start event
- `log_complete()` - Agent completion event
- `log_error()` - Error event
- `log_task_started()` - Task started event
- `log_task_completed()` - Task completed event
- `log_task_failed()` - Task failed event
- `log_in_progress()` - In-progress event

## Context
- Scout report: `.autonomous/analysis/scout-agent-architecture.md`
- Events: `5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml`
- Heartbeat: `5-project-memory/blackbox5/.autonomous/agents/communications/heartbeat.yaml`

## Approach
1. Choose protocol (recommend Option 1: Event-Driven)
2. Document event schema
3. Create communication library
4. Migrate Python agents
5. Migrate Bash agents
6. Test end-to-end workflow

## Dependencies
- TASK-ARCH-065 (path library) - for path resolution

## Rollback Strategy
- Keep old communication methods during transition
- Dual-write mode (write to both old and new)

## Estimated Effort
6-8 hours

## Related Tasks
- TASK-ARCH-067: Decouple agents from project structure
