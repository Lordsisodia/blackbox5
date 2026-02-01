# Black Box 5 Critical Paths Reference

**Purpose**: Comprehensive reference of all critical paths in the Black Box 5 ecosystem for Agent-2.3.
**Version**: 1.0.0
**Last Updated**: 2026-01-30

---

## Table of Contents

1. [Root Paths](#root-paths)
2. [Project Memories](#project-memories)
3. [Engine Components](#engine-components)
4. [BMAD Skills](#bmad-skills)
5. [Documentation](#documentation)
6. [Roadmap & Planning](#roadmap--planning)
7. [GUI & Interface](#gui--interface)
8. [Version History](#version-history)

---

## Root Paths

| Path | Description |
|------|-------------|
| `~/~/.blackbox5/` | Black Box 5 root directory |
| `~/~/.blackbox5/1-docs/` | All documentation |
| `~/~/.blackbox5/2-engine/` | Core engine |
| `~/~/.blackbox5/3-gui/` | GUI components |
| `~/~/.blackbox5/3-knowledge/` | Knowledge base |
| `~/~/.blackbox5/5-project-memory/` | All project memories |
| `~/~/.blackbox5/5-tools/` | Tools and utilities |
| `~/~/.blackbox5/6-integrations/` | External integrations |
| `~/~/.blackbox5/6-roadmap/` | Roadmaps and plans |

---

## Project Memories

### RALF-CORE (Self-Improvement)

| Path | Description |
|------|-------------|
| `~/.blackbox5/5-project-memory/ralf-core/.autonomous/` | RALF-CORE project memory root |
| `~/.blackbox5/5-project-memory/ralf-core/.autonomous/routes.yaml` | Full route configuration |
| `~/.blackbox5/5-project-memory/ralf-core/.autonomous/tasks/active/` | Pending tasks |
| `~/.blackbox5/5-project-memory/ralf-core/.autonomous/tasks/completed/` | Completed tasks |
| `~/.blackbox5/5-project-memory/ralf-core/.autonomous/runs/` | Execution history |
| `~/.blackbox5/5-project-memory/ralf-core/.autonomous/memory/decisions/` | Decision records |
| `~/.blackbox5/5-project-memory/ralf-core/.autonomous/memory/insights/` | Learned insights |
| `~/.blackbox5/5-project-memory/ralf-core/.autonomous/timeline/` | Project timeline |
| `~/.blackbox5/5-project-memory/ralf-core/.autonomous/workspaces/` | Active workspaces |
| `~/.blackbox5/5-project-memory/ralf-core/.autonomous/feedback/incoming/` | Incoming feedback |
| `~/.blackbox5/5-project-memory/ralf-core/.autonomous/feedback/processed/` | Processed feedback |
| `~/.blackbox5/5-project-memory/ralf-core/.autonomous/feedback/actions/` | Feedback actions |

### Blackbox5 (Core System)

| Path | Description |
|------|-------------|
| `~/.blackbox5/5-project-memory/blackbox5/.autonomous/` | Blackbox5 project memory |
| `~/.blackbox5/5-project-memory/blackbox5/.autonomous/tasks/` | Blackbox5 tasks |
| `~/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/` | Blackbox5 memories |

### SISO-INTERNAL

| Path | Description |
|------|-------------|
| `~/.blackbox5/5-project-memory/siso-internal/` | SISO-INTERNAL project root |
| `~/.blackbox5/5-project-memory/siso-internal/STATE.yaml` | Single source of truth |
| `~/.blackbox5/5-project-memory/siso-internal/ACTIVE.md` | Dashboard of active work |
| `~/.blackbox5/5-project-memory/siso-internal/WORK-LOG.md` | Activity log |
| `~/.blackbox5/5-project-memory/siso-internal/FEATURE-BACKLOG.yaml` | Feature queue |
| `~/.blackbox5/5-project-memory/siso-internal/decisions/` | Decision records |
| `~/.blackbox5/5-project-memory/siso-internal/knowledge/` | Knowledge base |
| `~/.blackbox5/5-project-memory/siso-internal/operations/` | System operations |
| `~/.blackbox5/5-project-memory/siso-internal/plans/` | Project plans |
| `~/.blackbox5/5-project-memory/siso-internal/project/` | Project identity |
| `~/.blackbox5/5-project-memory/siso-internal/tasks/` | Active tasks |

### Management

| Path | Description |
|------|-------------|
| `~/.blackbox5/5-project-memory/management/.autonomous/` | Management project memory |

---

## Engine Components

### Core Engine

| Path | Description |
|------|-------------|
| `~/.blackbox5/2-engine/.autonomous/` | RALF engine root |
| `~/.blackbox5/2-engine/.autonomous/routes.yaml` | BMAD command routing |
| `~/.blackbox5/2-engine/core/` | Core engine components |
| `~/.blackbox5/2-engine/runtime/` | Runtime systems |
| `~/.blackbox5/2-engine/skills/` | All skills |

### Libraries

| Path | Description |
|------|-------------|
| `~/.blackbox5/2-engine/.autonomous/lib/phase_gates.py` | Phase gate enforcement |
| `~/.blackbox5/2-engine/.autonomous/lib/context_budget.py` | Context budget management |
| `~/.blackbox5/2-engine/.autonomous/lib/` | All library modules |

### Shell Scripts

| Path | Description |
|------|-------------|
| `~/.blackbox5/2-engine/.autonomous/shell/` | Shell scripts directory |
| `~/.blackbox5/2-engine/.autonomous/shell/telemetry.sh` | Telemetry initialization |

### BMAD Components

| Path | Description |
|------|-------------|
| `~/.blackbox5/2-engine/.autonomous/bmad/` | BMAD methodology |
| `~/.blackbox5/2-engine/.autonomous/workflows/` | Workflow definitions |
| `~/.blackbox5/2-engine/.autonomous/wip/` | Work in progress |

### Prompts & Skills

| Path | Description |
|------|-------------|
| `~/.blackbox5/2-engine/.autonomous/prompts/` | Prompt templates |
| `~/.blackbox5/2-engine/.autonomous/skills/` | BMAD skills directory |
| `~/.blackbox5/2-engine/.autonomous/prompt-progression/` | Agent version history |

---

## BMAD Skills

### Skill Files

| Path | Role | Description |
|------|------|-------------|
| `~/.blackbox5/2-engine/.autonomous/skills/bmad-pm.md` | John | Product Manager |
| `~/.blackbox5/2-engine/.autonomous/skills/bmad-architect.md` | Winston | Architect |
| `~/.blackbox5/2-engine/.autonomous/skills/bmad-analyst.md` | Mary | Analyst |
| `~/.blackbox5/2-engine/.autonomous/skills/bmad-sm.md` | Bob | Scrum Master |
| `~/.blackbox5/2-engine/.autonomous/skills/bmad-ux.md` | Sally | UX Designer |
| `~/.blackbox5/2-engine/.autonomous/skills/bmad-dev.md` | Amelia | Developer |
| `~/.blackbox5/2-engine/.autonomous/skills/bmad-qa.md` | Quinn | QA Engineer |
| `~/.blackbox5/2-engine/.autonomous/skills/bmad-tea.md` | TEA | Test Architect |
| `~/.blackbox5/2-engine/.autonomous/skills/bmad-quick-flow.md` | Barry | Quick Flow |

### Command Reference

| Command | Skill | Description |
|---------|-------|-------------|
| `CP`, `VP`, `EP`, `CE` | PM (John) | Product management commands |
| `CA`, `VA`, `EA` | Architect (Winston) | Architecture commands |
| `BP`, `RS`, `CB`, `DP` | Analyst (Mary) | Analysis commands |
| `SP`, `CS`, `ER` | SM (Bob) | Scrum master commands |
| `CU`, `VU`, `EU` | UX (Sally) | UX design commands |
| `DS`, `CR` | Dev (Amelia) | Development commands |
| `QA`, `VT`, `RT` | QA (Quinn) | Quality assurance commands |
| `TS`, `QD` | Quick Flow (Barry) | Quick flow commands |
| `IR`, `CC` | Shared | Shared commands |

---

## Documentation

### Theory & Concepts

| Path | Description |
|------|-------------|
| `~/.blackbox5/1-docs/01-theory/` | Theory and concepts |

### Implementation Guides

| Path | Description |
|------|-------------|
| `~/.blackbox5/1-docs/02-implementation/` | Implementation guides |

### User Guides

| Path | Description |
|------|-------------|
| `~/.blackbox5/1-docs/03-guides/` | User guides |

### Project Documentation

| Path | Description |
|------|-------------|
| `~/.blackbox5/1-docs/04-project/` | Project-specific docs |
| `~/.blackbox5/1-docs/04-project/critical-paths.md` | This file |

### Examples

| Path | Description |
|------|-------------|
| `~/.blackbox5/1-docs/05-examples/` | Example implementations |

### Development Reference

| Path | Description |
|------|-------------|
| `~/.blackbox5/1-docs/development/reference/templates/specs/` | Specification templates |
| `~/.blackbox5/1-docs/decisions/` | Decision documentation |
| `~/.blackbox5/1-docs/engine-guides/` | Engine-specific guides |

### Key Documentation Files

| Path | Description |
|------|-------------|
| `~/.blackbox5/1-docs/README.md` | Documentation index |
| `~/.blackbox5/5-project-memory/README.md` | Project memory guide |
| `~/.blackbox5/5-project-memory/AI-AGENT-GUIDE.md` | AI agent guide |
| `~/.blackbox5/2-engine/.autonomous/BMAD-INTEGRATION-SUMMARY.md` | BMAD integration summary |
| `~/.blackbox5/2-engine/.autonomous/BMAD-INTEGRATION-PLAN.md` | BMAD integration plan |
| `~/.blackbox5/2-engine/.autonomous/BMAD-COMPARISON-ANALYSIS.md` | BMAD comparison analysis |

---

## Roadmap & Planning

### Roadmap Structure

| Path | Description |
|------|-------------|
| `~/.blackbox5/6-roadmap/` | All roadmaps and plans |
| `~/.blackbox5/6-roadmap/00-proposed/` | Proposed plans |
| `~/.blackbox5/6-roadmap/01-research/` | Research phase |
| `~/.blackbox5/6-roadmap/02-design/` | Design phase |
| `~/.blackbox5/6-roadmap/03-planned/` | Planned implementations |
| `~/.blackbox5/6-roadmap/04-active/` | Active work |
| `~/.blackbox5/6-roadmap/05-completed/` | Completed work |

---

## GUI & Interface

### GUI Components

| Path | Description |
|------|-------------|
| `~/.blackbox5/3-gui/` | All GUI components |
| `~/.blackbox5/3-gui/apps/vibe-kanban/` | Vibe Kanban app |

---

## Version History

### Agent Versions

| Path | Version | Description |
|------|---------|-------------|
| `~/.blackbox5/2-engine/.autonomous/prompt-progression/versions/v1/` | Agent-1.x | Early agent versions |
| `~/.blackbox5/2-engine/.autonomous/prompt-progression/versions/v2/` | Agent-2.0/2.1 | Foundation releases |
| `~/.blackbox5/2-engine/.autonomous/prompt-progression/versions/v2.2/` | Agent-2.2 | Enforcement release |
| `~/.blackbox5/2-engine/.autonomous/prompt-progression/versions/v2.3/` | Agent-2.3 | Integration release (current) |

### Current Agent Definition

| Path | Description |
|------|-------------|
| `~/.blackbox5/2-engine/.autonomous/prompt-progression/versions/v2.3/AGENT.md` | Current agent definition |
| `~/.blackbox5/2-engine/.autonomous/prompt-progression/versions/v2.2/AGENT.md` | Previous version (2.2) |

---

## GitHub Configuration

| Config | Value |
|--------|-------|
| Repository | `https://github.com/Lordsisodia/blackbox5` |
| Branch | `feature/tier2-skills-integration` |

---

## Quick Reference

### Most Accessed Paths

```bash
# Project memories
~/.blackbox5/5-project-memory/ralf-core/.autonomous/
~/.blackbox5/5-project-memory/siso-internal/

# Engine
~/.blackbox5/2-engine/.autonomous/
~/.blackbox5/2-engine/.autonomous/lib/
~/.blackbox5/2-engine/.autonomous/skills/

# Documentation
~/.blackbox5/1-docs/04-project/
~/.blackbox5/5-project-memory/siso-internal/WORK-LOG.md

# State
~/.blackbox5/5-project-memory/siso-internal/STATE.yaml
~/.blackbox5/5-project-memory/siso-internal/ACTIVE.md
```

---

## Maintenance Notes

- This file should be kept in sync with `AGENT.md` critical paths
- Update when new project memories are added
- Update when engine structure changes
- Version bump on significant changes
