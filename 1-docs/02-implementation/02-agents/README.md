# Agent Implementation

> Agent system implementation documentation

## Overview

This directory documents the implementation of BlackBox5's agent system, including the Planner, Executor, Verifier, and specialized agents.

## Files

| File | Purpose |
|------|---------|
| `planner-implementation.md` | Planner agent internals |
| `executor-implementation.md` | Executor agent internals |
| `verifier-implementation.md` | Verification system |
| `agent-lifecycle.md` | Agent creation and destruction |
| `specialized-agents.md` | Domain-specific agents |

## Agent Types

- **RALF-Planner** - Strategic planning and task decomposition
- **RALF-Executor** - Tactical execution and implementation
- **RALF-Verifier** - Quality assurance and validation
- **Specialized Agents** - Domain experts (BMAD series)

## Communication Protocol

Agents communicate via YAML files:
- `queue.yaml` - Task distribution
- `events.yaml` - Status updates
- `chat-log.yaml` - Q&A between agents
- `heartbeat.yaml` - Health monitoring

## Related Documentation

- [../01-core/README.md](../01-core/README.md) - Core infrastructure
- [../../01-theory/02-concepts/dual-agent-architecture.md](../../01-theory/02-concepts/dual-agent-architecture.md) - Architecture theory

## Usage

Essential reading for understanding or modifying agent behavior.
