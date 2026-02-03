# Architecture Map - BlackBox 5

**Last Updated:** 2026-02-02
**Updated By:** Claude

This document maps the system architecture. Update this file when the architecture changes.

## System Overview

BlackBox 5 is a multi-agent autonomous execution system with:
- **Planner Agent:** Analyzes, plans, prioritizes
- **Executor Agent:** Executes tasks, writes code
- **Architect Agent:** (Future) Designs system architecture

## Core Components

### 1. RALF Engine (`2-engine/.autonomous/`)

```
2-engine/.autonomous/
├── prompts/           # Agent prompts
│   ├── ralf-executor.md
│   ├── system/
│   │   ├── executor-identity.md
│   │   └── planner-identity.md
│   └── procedures/
├── skills/            # Agent skills (23+)
├── workflows/         # Workflow definitions
├── lib/               # Python libraries
│   ├── phase_gates.py
│   ├── context_budget.py
│   └── decision_registry.py
├── shell/             # Shell scripts
│   └── ralf-loop.sh
└── config/            # Configuration
    └── default.yaml
```

### 2. Project Memory (`5-project-memory/blackbox5/`)

```
5-project-memory/blackbox5/
├── .autonomous/
│   ├── tasks/         # Task management
│   ├── communications/# Planner-executor comms
│   └── runs/          # Run history
├── runs/              # Run history (legacy)
├── decisions/         # Architectural decisions
├── knowledge/         # Documentation
└── operations/        # Operations docs
```

### 3. Hooks System (`.claude/`)

```
.claude/
└── settings.json      # Hook configuration
```

Hooks:
- `SessionStart`: Creates run folder
- `Stop`: Handles completion

### 4. Scripts (`bin/`)

```
bin/
├── ralf-build-prompt.sh    # Dynamic prompt builder
├── ralf-session-start-hook.sh
├── ralf-planner
├── ralf-executor
└── ralf-loop.sh
```

## Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Planner   │────▶│  Queue.yaml │────▶│  Executor   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                                    │
       │                                    ▼
       │                              ┌─────────────┐
       │                              │   Execute   │
       │                              └─────────────┘
       │                                    │
       ▼                                    ▼
┌─────────────┐                      ┌─────────────┐
│  Analyze    │◀─────────────────────│   Report    │
└─────────────┘                      └─────────────┘
```

## Communication Protocol

- **queue.yaml:** Planner → Executor (task assignments)
- **events.yaml:** Executor → Planner (status updates)
- **chat-log.yaml:** Bidirectional communication
- **heartbeat.yaml:** Health checks

## Agent Execution Flow (7 Phases)

1. **Runtime Initialization** (Hook-enforced)
2. **Read Prompt** (Dynamic context loaded)
3. **Task Selection**
4. **Task Folder Creation**
5. **Context & Execution**
6. **Logging & Completion**
7. **Archive** (Hook-enforced)

## Update This File When...

- New components are added
- Architecture patterns change
- Data flow changes
- New agent types are introduced
