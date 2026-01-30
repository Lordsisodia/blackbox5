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

This project follows the standard **7-Folder Project Memory Structure**:

```
blackbox5/
├── project/           # Project identity & direction
│   └── context.yaml   # Project goals, constraints, current state
│
├── plans/             # What we're building
│   ├── active/        # Active plans (epics, features)
│   ├── archived/      # Completed/archived plans
│   ├── briefs/        # Product briefs
│   ├── features/      # Feature management
│   └── prds/          # Product requirements
│
├── decisions/         # Why we're doing it this way
│   ├── architectural/ # Architecture decisions
│   ├── scope/         # Scope decisions
│   └── technical/     # Technical decisions
│
├── knowledge/         # How it works + what we've learned
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
├── tasks/             # What we're working on
│   ├── active/        # Active task files
│   ├── completed/     # Completed tasks
│   ├── working/       # Working task folders
│   └── backlog/       # Backlogged tasks
│
├── domains/           # How it's organized (by domain)
│   ├── auth/          # Authentication domain
│   ├── integrations/  # Integration domain
│   ├── supabase/      # Supabase domain
│   └── ui/            # UI domain
│
└── operations/        # System operations
    ├── agents/        # Agent memory
    ├── architecture/  # Architecture validation
    ├── docs/          # System documentation
    ├── logs/          # System logs
    ├── sessions/      # Session transcripts
    └── workflows/     # Workflow execution
```

---

## Quick Links

### Current State
- [Project Context](./project/context.yaml) - Goals, constraints, current progress
- [Migration Status](./project/context.yaml) - 47% complete, see remaining work

### Active Work
- [Active Plans](./plans/active/) - Current epics and features in development
- [Active Tasks](./tasks/active/) - Tasks being worked on now
- [Working Tasks](./tasks/working/) - Task work-in-progress folders

### Key Decisions
- [Architectural Decisions](./decisions/architectural/) - System architecture choices
- [Technical Decisions](./decisions/technical/) - Technology and implementation choices
- [Scope Decisions](./decisions/scope/) - In/out of scope decisions

### Knowledge Base
- [Architecture](./knowledge/architecture/) - System architecture documentation
- [Codebase](./knowledge/codebase/) - Code patterns, gotchas, index
- [Research](./knowledge/research/) - Framework and technology research
- [Frameworks](./knowledge/frameworks/) - Integrated frameworks (BMAD, SpecKit, MetaGPT, Swarm)

### Operations
- [Agents](./operations/agents/) - Agent-specific memory
- [Sessions](./operations/sessions/) - Session transcripts
- [Workflows](./operations/workflows/) - Workflow definitions
- [Logs](./operations/logs/) - System logs

---

## Project Status

### Migration Progress: 47%

**Completed**:
- Basic directory structure
- 33/70 skills verified
- 4 frameworks integrated, 11 researched
- 50 agents across 5 major types

**In Progress**:
- Memory system integration
- Agent type migration
- Skills verification

**Critical Gaps**:
- Memory compression not implemented
- Agent discovery and routing missing
- Learning system not functional
- Safety guardrails incomplete

See [Project Context](./project/context.yaml) for full details.

---

## Related Projects

| Project | Relationship | Location |
|---------|-------------|----------|
| **SISO Internal** | Parent project | `../siso-internal/` |
| **Ralf Core** | Integration | `../ralf-core/` |
| **DeerFlow** | Research source | Referenced in context |
| **Vibe Kanban** | Integration | Referenced in context |

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
