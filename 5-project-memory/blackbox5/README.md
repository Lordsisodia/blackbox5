# BlackBox5 Project Memory

**Project**: BlackBox5 - Autonomous Agent Framework  
**Version**: 5.0.0  
**Status**: Active Development  
**Created**: 2026-01-20  

---

## Overview

This directory contains the project memory for **BlackBox5**, the next-generation autonomous agent system with hierarchical memory, multi-agent orchestration, and self-improvement capabilities.

BlackBox5 serves as the AI agent framework powering SISO Internal operations, enabling AI agents to work autonomously on complex software engineering tasks with minimal human intervention.

---

## Directory Structure

This project follows the **6-Folder Project Memory Structure** (organized by question type):

```
blackbox5/
├── project/           # WHO are we? Project identity & direction
│   └── context.yaml   # Project goals, constraints, current state
│
├── plans/             # WHAT are we building?
│   ├── active/        # Active plans (epics, features)
│   ├── archived/      # Completed/archived plans
│   ├── briefs/        # Product briefs
│   ├── features/      # Feature management
│   └── prds/          # Product requirements
│
├── decisions/         # WHY are we doing it this way?
│   ├── architectural/ # Architecture decisions
│   ├── scope/         # Scope decisions
│   └── technical/     # Technical decisions
│
├── knowledge/         # HOW does it work?
│   ├── architecture/  # System architecture docs
│   ├── archives/      # Archived knowledge
│   ├── codebase/      # Code patterns and gotchas
│   ├── first-principles/  # First principles analysis
│   ├── frameworks/    # Framework research
│   ├── ralph-integration/ # Ralph integration docs
│   ├── ralph-loop/    # Ralph loop documentation
│   ├── research/      # Research findings
│   └── validation/    # Validation results
│
├── tasks/             # WHAT needs to be done?
│   ├── active/        # Active task files
│   ├── completed/     # Completed tasks
│   ├── working/       # Working task folders
│   └── backlog/       # Backlogged tasks
│
└── operations/        # System operations
    ├── agents/        # Agent memory
    ├── architecture/  # Architecture validation
    ├── docs/          # System documentation
    ├── logs/          # System logs
    ├── sessions/      # Session transcripts
    └── workflows/     # Workflow execution
```

### Root State Files

| File | Purpose |
|------|---------|
| `STATE.yaml` | Single source of truth - tasks, features, decisions |
| `ACTIVE.md` | Dashboard of current work |
| `WORK-LOG.md` | Chronological activity log |
| `timeline.yaml` | Milestones and timeline |
| `feature_backlog.yaml` | Pending features |
| `test_results.yaml` | Test outcomes |
| `_NAMING.md` | Naming conventions |
| `QUERIES.md` | Common queries for AI agents |

---

## Quick Links

### Current State
- [STATE.yaml](./STATE.yaml) - Single source of truth
- [ACTIVE.md](./ACTIVE.md) - Dashboard of current work
- [Project Context](./project/context.yaml) - Goals, constraints, current progress

### Active Work
- [Active Plans](./plans/active/) - Current epics and features in development
- [Active Tasks](./tasks/active/) - Tasks being worked on now

### Key Decisions
- [Architectural Decisions](./decisions/architectural/) - System architecture choices
- [Technical Decisions](./decisions/technical/) - Technology and implementation choices
- [Scope Decisions](./decisions/scope/) - In/out of scope decisions

### Knowledge Base
- [Architecture](./knowledge/architecture/) - System architecture documentation
- [Codebase](./knowledge/codebase/) - Code patterns, gotchas, index
- [Research](./knowledge/research/) - Framework and technology research

### Templates
- [.templates/](./.templates/) - 26 templates for consistent documentation

---

## Project Status

### Project Memory Reorganization: 75% Complete

**Completed**:
- 26 templates created in `.templates/`
- 8 root state files (STATE.yaml, ACTIVE.md, WORK-LOG.md, etc.)
- 6-folder structure implemented (removed deprecated domains/)
- `.docs/` folders created in each main folder
- 40 tasks migrated from RALF-Core
- 45+ runs archived to `.archived/runs/`

**In Progress**:
- Phase 4: Integration and documentation

**Architecture**:
- 6-Folder Structure: project/, plans/, decisions/, knowledge/, tasks/, operations/
- Question-based organization (WHO, WHAT, WHY, HOW)
- STATE.yaml as single source of truth
- Template-driven documentation

---

## Related Projects

| Project | Relationship | Location |
|---------|-------------|----------|
| **SISO Internal** | Reference project | `../siso-internal/` |
| **RALF Engine** | Autonomous agent engine | `../../2-engine/` |

---

## Creating New Projects

To create a new project with this structure:

1. Copy the `_template/` folder from the parent directory
2. Rename it to your project name
3. Fill in `project/context.yaml`, `project/project.yaml`
4. Start working!

See: `../_template/README.md` for detailed template documentation.

---

## Memory System

This project implements the three-tier memory system:

1. **Working Memory** (`operations/sessions/`) - Session-only
2. **Extended Memory** (all folders) - Permanent project knowledge
3. **Archival Memory** (`knowledge/archives/`) - Long-term storage

---

## Framework Integration

BlackBox5 integrates research from multiple frameworks:

- **BMAD** - Business Model Analysis and Design
- **SpecKit** - Specification toolkit
- **MetaGPT** - Multi-agent collaboration patterns
- **Swarm** - Agent orchestration patterns

Research documentation is in `knowledge/frameworks/` and `knowledge/research/`.

---

*Last updated: 2026-01-30*
