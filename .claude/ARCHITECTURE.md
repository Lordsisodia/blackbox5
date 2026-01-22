# Claude Code Hooks: Architecture & Position

**Version**: 1.0.0
**Date**: 2026-01-21
**Location**: `.claude/` (Project Root)

---

## Where Hooks Belong

```
blackbox5/
│
├── .claude/                              ← CLAUDE CODE CONFIGURATION (NOT ENGINE)
│   ├── settings.json                      # Hook configuration
│   ├── hooks/                             # Hook scripts (20 files)
│   │   ├── reflect-on-completion.sh       # Next-steps planning
│   │   ├── auto-log-activity.sh
│   │   ├── extract-memories.sh
│   │   └── [17 more hooks...]
│   ├── check-status.sh                    # Verification
│   ├── verify-hooks.sh                    # Verification
│   └── IMPLEMENTATION-SUMMARY.md          # Documentation
│
├── 2-engine/                              ← BLACKBOX5 ENGINE
│   └── 07-operations/                     # Engine operations
│       └── runtime/                       # Runtime execution
│           ├── autonomous-agent/
│           ├── mcp-mux/
│           └── overnight/
│
└── 5-project-memory/                      ← MEMORY PERSISTENCE
    └── siso-internal/
        ├── decisions/
        ├── knowledge/
        └── operations/
            └── reflections/               # Hook output storage
```

---

## Correct Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT WORKSTATION                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Claude Code (CLI Tool)                                        │ │
│  │  - Reads .claude/settings.json                                │ │
│  │  - Executes hooks on events                                    │ │
│  │  - Coordinates with engine                                     │ │
│  └────────┬───────────────────────────────────────────────────────┘ │
│           │                                                         │
│           │ Hooks bridge Claude Code → Blackbox5                   │
│           │                                                         │
│  ┌────────▼─────────────────────────────────────────────────────┐ │
│  │  .claude/ (Configuration Layer)                                │ │
│  │  ├── settings.json  ← Hook definitions                        │ │
│  │  └── hooks/        ← Hook scripts                             │ │
│  └────────┬───────────────────────────────────────────────────────┘ │
│           │                                                         │
│           ↓                                                         │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  2-engine/ (Blackbox5 Engine)                                  │ │
│  │  - Agents, orchestration, routing                              │ │
│  │  - Runtime operations                                         │ │
│  └────────┬───────────────────────────────────────────────────────┘ │
│           │                                                         │
│           ↓                                                         │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  5-project-memory/ (Persistence Layer)                         │ │
│  │  - Decisions, knowledge, reflections                          │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Key Insight

**`.claude/` is NOT part of the Blackbox5 engine.**

It's the **Claude Code configuration layer** that:
- Lives at project root (standard Claude Code location)
- Configures how Claude Code behaves in this project
- Contains hooks that integrate Claude Code with Blackbox5
- Bridges between Claude Code (tool) and Blackbox5 (system)

---

## What Goes Where

| Location | Purpose | Example |
|----------|---------|---------|
| `.claude/` | Claude Code configuration | settings.json, hooks/, CLAUDE.md |
| `2-engine/` | Blackbox5 engine code | Agents, orchestrator, runtime |
| `5-project-memory/` | Persistent data | Decisions, knowledge, reflections |

---

## Hooks System Summary

**Location**: `.claude/hooks/` (20 scripts)

**Purpose**: Integrate Claude Code with Blackbox5 workflow

**Key Innovation**: `reflect-on-completion.sh` ensures every completion triggers next-steps planning

**Memory Output**: `5-project-memory/siso-internal/operations/reflections/`

---

## Documentation

| Document | Location | Purpose |
|----------|---------|---------|
| IMPLEMENTATION-SUMMARY.md | `.claude/` | Complete implementation guide |
| ARCHITECTURE.md | `.claude/` | This file |
| HOOKS-ARCHITECTURE.md | `2-engine/07-operations/` | Engine-level documentation |
| README.md | `.claude/hooks/` | Hook-specific documentation |
