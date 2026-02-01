# Target Architecture Structure
# =============================================================================
# Purpose: Clean, intuitive layout for BlackBox5
# Status: Target state - not yet implemented
# =============================================================================

## Overview

This document describes the clean target architecture for BlackBox5.
Use this as the guide for all migration and improvement work.

## Principles

1. **Clear Separation**: Engine (shared) vs Project (specific)
2. **Intuitive Names**: Folders named by what they contain
3. **No Duplicates**: Each concept lives in one place
4. **AI-Friendly**: Structure is machine-navigable

## Target Structure

### Root Level

```
5-project-memory/blackbox5/
├── README.md                 # Project overview
├── STATE.yaml               # Current project state
├── goals.yaml               # Project goals
│
├── architecture/            # Architecture documentation
│   ├── README.md
│   ├── ADR.md              # Architecture decisions
│   ├── decisions/          # Individual decision docs
│   ├── knowledge/          # Architectural patterns
│   ├── context/            # Current system state
│   │   ├── ROOT_LAYOUT.yaml
│   │   └── DEPENDENCIES.md
│   └── plans/              # Future improvements
│       └── TARGET_STRUCTURE.md  # This file
│
├── autonomous/              # Project agent data
│   ├── tasks/
│   │   ├── autonomous/     # Agent-created tasks
│   │   └── manual/         # Human-created tasks
│   ├── communications/     # Agent coordination
│   ├── runs/              # Run history
│   └── context/           # ARCHITECTURE_CONTEXT.md
│
├── decisions/              # Non-architectural decisions
│   ├── infrastructure/
│   ├── scope/
│   └── technical/
│
├── knowledge/              # Knowledge base
│   ├── analysis/
│   ├── codebase/
│   ├── frameworks/
│   └── research/
│
├── memory/                 # Project memory
├── operations/             # Operations docs
├── plans/                  # Project plans
│   ├── features/
│   ├── prds/
│   └── briefs/
│
├── project/                # Project metadata
└── runs/                   # Run history (legacy)
    ├── planner/
    ├── executor/
    └── timeline/
```

### Engine (Outside Project Memory)

```
2-engine/
└── autonomous-core/        # WAS: .autonomous
    ├── prompts/           # Agent prompts
    ├── skills/            # BMAD skills
    ├── lib/               # Core libraries
    ├── config/            # Default configs
    └── workflows/         # Reusable workflows
```

## What Changed

### Deleted
- `.autonomous/` (root) - Duplicate, merged into `autonomous/`
- `tasks/` (legacy) - Merged into `autonomous/tasks/manual/`
- `ARCHITECTURE_DECISIONS.md` - Moved to `architecture/ADR.md`
- `decisions/architectural/` - Moved to `architecture/decisions/`
- `knowledge/architecture/` - Moved to `architecture/knowledge/`

### Renamed
- `2-engine/.autonomous/` → `2-engine/autonomous-core/`

### Created
- `architecture/` - Central architecture documentation
- `autonomous/tasks/manual/` - Human tasks (from legacy `tasks/`)

## Migration Path

See `../autonomous/MIGRATION-PLAN.md` for detailed steps.

## Success Criteria

- [ ] Only 2 autonomous locations exist
- [ ] All agents work without path confusion
- [ ] New developers understand structure in 5 minutes
- [ ] No duplicate folders
- [ ] Clear separation between engine and project
