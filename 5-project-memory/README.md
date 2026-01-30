# Project Memory

This folder contains project-specific memory structures for BlackBox5.

---

## Quick Navigation

| Directory | Purpose | Status |
|-----------|---------|--------|
| [**blackbox5/**](./blackbox5/) | BlackBox5 framework project memory | Active |
| [**siso-internal/**](./siso-internal/) | SISO Internal main project | Active |
| [**ralf-core/**](./ralf-core/) | Autonomous daemon for codebase analysis | Active |
| [**management/**](./management/) | Project management utilities | Active |
| [**_template/**](./_template/) | Template for new projects | Reference |

---

## Directory Structure

```
5-project-memory/
├── _template/           # Template for new projects
│   ├── decisions/       # Decision log templates
│   ├── domains/         # Domain structure templates
│   ├── knowledge/       # Knowledge base templates
│   ├── operations/      # Operations templates
│   ├── plans/           # Plan templates (PRDs, epics, tasks)
│   ├── project/         # Project metadata templates
│   ├── tasks/           # Task templates
│   └── README.md        # Template documentation
│
├── blackbox5/           # BlackBox5 framework memory
│   ├── decisions/       # Architecture, scope, technical decisions
│   ├── domains/         # Auth, integrations, supabase, UI domains
│   ├── knowledge/       # Architecture, codebase, research, frameworks
│   ├── operations/      # Agents, sessions, workflows, logs
│   ├── plans/           # Active plans, PRDs, features
│   ├── project/         # Project context and metadata
│   ├── tasks/           # Active and completed tasks
│   └── README.md        # Project documentation
│
├── siso-internal/       # SISO Internal project memory
│   ├── agents/          # Agent-specific memory
│   ├── architecture/    # Architecture documentation
│   ├── artifacts/       # Build artifacts and outputs
│   ├── codebase/        # Code index and navigation
│   ├── context/         # High-level project context
│   ├── domains/         # Domain-specific memory
│   ├── github/          # GitHub integration memory
│   ├── knowledge/       # Knowledge base
│   ├── legacy/          # Legacy project memory
│   ├── logs/            # Execution logs
│   ├── sessions/        # Session history
│   ├── tasks/           # Active and archived tasks
│   ├── workflows/       # Workflow definitions
│   └── working/         # Active working memory
│
├── ralf-core/           # Ralf autonomous daemon
│   └── .autonomous/     # Daemon data and configuration
│
├── management/          # Project management utilities
│
├── .docs/               # Memory system documentation
│
├── code_index.md        # Global code index
├── INDEX.yaml           # Memory index
├── AI-AGENT-GUIDE.md    # Guide for AI agents using this memory
└── README.md            # This file
```

---

## Active Projects

### 1. BlackBox5 Framework
**Location**: [`blackbox5/`](./blackbox5/)  
**Status**: In Development (47% migrated)  
**Description**: Next-generation autonomous agent framework

**Quick Links**:
- [Project Context](./blackbox5/project/context.yaml) - Goals, constraints, progress
- [Active Plans](./blackbox5/plans/active/) - Current epics and features
- [Knowledge Base](./blackbox5/knowledge/) - Architecture, research, patterns

### 2. SISO Internal
**Location**: [`siso-internal/`](./siso-internal/)  
**Status**: Active  
**Description**: Main SISO Internal application

**Quick Links**:
- [Context](./siso-internal/context/) - Project context
- [Domains](./siso-internal/domains/) - Domain-specific memory
- [Tasks](./siso-internal/tasks/) - Active tasks

### 3. Ralf Core
**Location**: [`ralf-core/`](./ralf-core/)  
**Status**: Active  
**Description**: Autonomous codebase analysis daemon

**Quick Links**:
- [Daemon Script](./ralf-core/.autonomous/ralf-daemon.sh)
- [Routes Config](./ralf-core/.autonomous/routes.yaml)

---

## Usage

### Creating a New Project

1. Copy the `_template/` folder
2. Rename it to your project name (e.g., `my-project/`)
3. Fill in the project metadata files:
   - `project/context.yaml`
   - `project/project.yaml`
   - `project/timeline.yaml`
4. Start working!

See [`_template/README.md`](./_template/README.md) for detailed documentation.

### Project Memory Types

- **project/**: High-level project context (goals, directions, PRDs, features)
- **plans/**: Implementation plans (PRDs, epics, tasks, checklists)
- **tasks/**: Active tasks and their contexts
- **decisions/**: Architectural decision records
- **knowledge/**: Research findings and analysis
- **operations/**: System operations (agents, sessions, workflows)
- **domains/**: Domain-specific organization

---

## Memory Tiers

This implements the three-tier memory system:

1. **Working Memory** (`working/`, `sessions/`) - Session-only, ~10MB
2. **Extended Memory** (project folders) - Permanent, ~500MB
3. **Archival Memory** (`legacy/`, `artifacts/`, `archives/`) - Permanent, ~5GB

See: `.blackbox/.docs/3-components/memory/MEMORY-ARCHITECTURE.md`

---

## Framework vs Project

- **Framework Level**: `_template/`, `code_index.md`, `INDEX.yaml`, `AI-AGENT-GUIDE.md`
- **Project Level**: `blackbox5/`, `siso-internal/`, `ralf-core/`

Each project has its own isolated memory structure following the 7-folder pattern.

---

## Key Files

| File | Purpose |
|------|---------|
| `code_index.md` | Global code index for navigation |
| `INDEX.yaml` | Memory index with project listings |
| `AI-AGENT-GUIDE.md` | Guide for AI agents using this system |
| `MIGRATION-SCRIPT.sh` | Script for migrating old memory structures |

---

*Last updated: 2026-01-30*
