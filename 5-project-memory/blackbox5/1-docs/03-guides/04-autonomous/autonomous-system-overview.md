# Blackbox5 Autonomous System

> **Multi-Agent Autonomous Coordination System** - Research & Implementation

## Overview

This folder contains research, design, and implementation details for Blackbox5's autonomous agent system. The system enables multiple AI agents to coordinate, execute tasks, and track progress autonomously with minimal human intervention.

## Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    REDIS (Event Bus)                         │
│  Instant agent coordination via pub/sub and streams          │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    ┌─────────┐        ┌──────────┐        ┌─────────┐
    │Supervisor│        │Interface │        │ Autonomous │
    │  Agent   │        │  Agent   │        │  Agents    │
    │(Task     │        │(Your     │        │(Workers)  │
    │ Creator) │        │Interface) │        │           │
    └────┬─────┘        └────┬─────┘        └─────┬─────┘
         │                   │                   │
         └───────────────────┴───────────────────┘
                             │
                    ┌────────▼────────┐
                    │ PROJECT_STATE.YAML │
                    │  (Per Project)     │
                    │  - Tasks           │
                    │  - State           │
                    │  - History         │
                    └─────────────────────┘
```

## Key Components

### 1. Redis (Event Bus)
- **Pub/Sub**: Instant agent notifications
- **Streams**: Event log for replayability
- **Sorted Sets**: Priority task queues
- **Hashes**: Fast task lookup

### 2. Supervisor Agent (Task Creator)
- Breaks down goals into tasks
- Creates task dependencies
- Manages task priorities
- Never executes - only orchestrates

### 3. Interface Agent (Your Liaison)
- Reports status from all agents
- Takes your commands and routes them
- Escalates blockers
- Makes decisions when delegated

### 4. Autonomous Agents (Workers)
- Subscribe to task events
- Claim appropriate tasks
- Execute work independently
- Update state on completion

## How Autonomy Works

### The OODA Loop
```
OBSERVE → Check PROJECT_STATE.yaml and Redis events
ORIENT → Understand what needs to be done
DECIDE  → Choose next appropriate task
ACT     → Execute the task
CHECK   → Verify success, update state
REPEAT  → Continue forever
```

### Event Flow
```
1. You say: "Build authentication system"

2. Supervisor Agent:
   - Publishes: "tasks:new" with task details
   - Updates: PROJECT_STATE.yaml with task list

3. Autonomous Agents:
   - Receive notification instantly (1ms via Redis)
   - Check if they can handle the task
   - Claim task if capable

4. Agent completes task:
   - Publishes: "tasks:complete"
   - Updates: PROJECT_STATE.yaml with result

5. Other agents see completion:
   - Dependent tasks become available
   - Next agent claims and continues

6. Interface Agent:
   - Monitors all events
   - Reports status to you when asked
   - Alerts you to blockers
```

## Why Redis?

### Without Redis (Polling)
```python
while True:
    check_for_tasks()  # Every 10 seconds
    sleep(10)
```
- **Latency**: 10+ seconds
- **Waste**: Checks even when no work
- **Scalability**: 100 agents × 10 checks = 1000 ops/min

### With Redis (Pub/Sub)
```python
for message in redis.subscribe("tasks:new"):
    # React instantly when task published
    handle_task(message)
```
- **Latency**: 1 millisecond
- **Efficiency**: Only react when needed
- **Scalability**: One notification, all agents see it

**That's 10,000x faster and infinitely more scalable.**

## Folder Structure

```
8-autonomous-system/
├── README.md (this file)
├── architecture.md          # System architecture and design
├── redis-guide.md           # Complete Redis guide for autonomous agents
├── task-tracking.md         # How tasks are tracked and managed
├── research/                # Research findings and analysis
│   ├── plandex-research.md  # Plandex tool analysis
│   ├── production-patterns.md # Production systems research
│   └── alternatives.md      # Alternative frameworks comparison
├── implementation/          # Implementation code and configs
│   ├── schemas/             # Data schemas (Task, Agent, State)
│   ├── agents/              # Agent implementations
│   └── redis/               # Redis configuration and setup
└── examples/                # Working examples and demos
```

## Design Principles

1. **Event-Driven**: Agents react to events, not polling
2. **Stateless Agents**: Agent logic in code, state in Redis/YAML
3. **Git-Tracked**: All state changes committed to Git
4. **Observable**: Everything logged and replayable
5. **Resilient**: No single point of failure
6. **Scalable**: Add agents without re-architecture

## Getting Started

1. Read `redis-guide.md` to understand Redis for autonomous agents
2. Read `task-tracking.md` to understand task management
3. Read `research/plandex-research.md` to see what we can learn from Plandex
4. Check `implementation/` for code examples

## Research Sources

- Production autonomous systems (LangGraph, CrewAI, AutoGen)
- Redis pub/sub patterns for agent coordination
- Task tracking in distributed systems
- Plandex AI tool architecture and patterns
- Real-world case studies from 2025-2026

## Status

📊 **Research Phase**: Complete
🏗️ **Implementation**: In Progress
🧪 **Testing**: Pending

---

**Last Updated**: 2026-01-28
**Version**: 1.0.0
