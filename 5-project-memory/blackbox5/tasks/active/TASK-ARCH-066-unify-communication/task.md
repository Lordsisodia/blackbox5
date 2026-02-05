# TASK-ARCH-066: Unify Agent Communication System

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
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
- [ ] Single communication protocol chosen
- [ ] All Python agents migrated to new protocol
- [ ] All Bash agents migrated to new protocol
- [ ] Event/report schema documented
- [ ] Backward compatibility for old reports

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
