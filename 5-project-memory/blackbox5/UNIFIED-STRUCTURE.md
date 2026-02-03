# BlackBox5 Unified Structure

**Version:** 1.0.0
**Last Updated:** 2026-02-04
**Status:** Migrated

---

## Overview

This document describes the unified hierarchical structure for BlackBox5 project memory. The structure follows a clear hierarchy:

```
GOALS → PLANS → TASKS → SUBTASKS
```

Each level has consistent data layers (timeline, learnings, decisions) and cross-references via symlinks.

---

## Directory Structure

### Root Level Files

| File | Purpose |
|------|---------|
| `STATE.yaml` | Single source of truth for project state |
| `MAP.yaml` | Complete file catalog (10 levels deep) |
| `ACTIVE.md` | Current work dashboard |
| `WORK-LOG.md` | Chronological activity log |
| `timeline.yaml` | Project milestones |
| `goals.yaml` | Goals index |
| `feature_backlog.yaml` | Pending features |
| `README.md` | Project overview |

---

## Hierarchy

### 1. GOALS (`goals/`)

**Purpose:** Define what we want to achieve

**Structure:**
```
goals/
├── active/
│   └── GOAL-XXX/               # Each goal is a folder
│       ├── goal.yaml           # Definition, success criteria
│       ├── timeline.yaml       # Progress tracking
│       ├── journal/            # Daily/weekly reflections
│       │   └── YYYY-MM-DD.md
│       └── plans/              # SYMLINKS to related plans
│           └── PLAN-XXX -> ../../../plans/active/PLAN-XXX
├── completed/
├── core/
│   └── core-goals.yaml
└── templates/
    └── goal-template.yaml
```

**Key Files:**
- `goal.yaml` - Goal definition, sub-goals, linked tasks
- `timeline.yaml` - Progress tracking with dates
- `journal/*.md` - Daily reflections and progress notes

---

### 2. PLANS (`plans/`)

**Purpose:** Define how to achieve goals

**Structure:**
```
plans/
├── active/
│   └── PLAN-XXX/               # Each plan is a folder
│       ├── plan.md             # Technical design
│       ├── metadata.yaml       # Estimates, priorities
│       ├── research/           # Research findings
│       │   └── STACK.md
│       └── tasks/              # SYMLINKS to tasks
│           └── TASK-XXX -> ../../../tasks/active/TASK-XXX
├── archived/
├── briefs/                     # Quick plan ideas
├── features/                   # Feature specifications
│   └── FEATURE-XXX.md
└── prds/                       # Product requirements
```

**Key Files:**
- `plan.md` - Technical design and approach
- `metadata.yaml` - Estimates, priorities, status
- `research/*.md` - Technical research findings

---

### 3. TASKS (`tasks/`)

**Purpose:** Work to be done

**Structure:**
```
tasks/
├── active/
│   └── TASK-XXX/               # Each task is a folder
│       ├── task.md             # Specification
│       ├── THOUGHTS.md         # Execution thinking
│       ├── DECISIONS.md        # Key decisions
│       ├── LEARNINGS.md        # Post-completion insights
│       ├── ASSUMPTIONS.md      # Validated assumptions
│       ├── RESULTS.md          # Outcomes
│       ├── timeline/           # Daily progress
│       │   └── YYYY-MM-DD.md
│       ├── subtasks/           # SUBTASKS
│       │   └── TASK-XXX-001/
│       └── artifacts/          # Generated files
├── completed/
├── backlog/
├── improvements/               # Improvement proposals
│   └── IMP-XXX/
└── working/                    # In-progress work
```

**Key Files:**
- `task.md` - Task specification and acceptance criteria
- `THOUGHTS.md` - Reasoning during execution
- `DECISIONS.md` - Key decisions made
- `LEARNINGS.md` - What we learned
- `timeline/*.md` - Daily progress entries

---

### 4. RUNTIME (`.autonomous/`)

**Purpose:** Agent execution sessions (separate from work hierarchy)

**Structure:**
```
.autonomous/
├── agents/
│   ├── planner/
│   │   └── runs/               # Planner agent runs
│   ├── executor/
│   │   └── runs/               # Executor agent runs
│   └── architect/
│       └── runs/               # Architect agent runs
├── communications/
│   ├── queue.yaml              # Work queue
│   ├── events.yaml             # Event log
│   ├── protocol.yaml           # Communication rules
│   ├── heartbeat.yaml          # Agent health
│   └── agent-state.yaml        # Agent states
├── memory/                     # Agent memory
├── research-pipeline/          # Research pipeline system
├── timeline/                   # Global timeline
└── state.json                  # Global agent state
```

---

### 5. RUNS (`runs/`)

**Purpose:** RALF execution sessions

**Structure:**
```
runs/
├── planner/                    # Planner runs
├── executor/                   # Executor runs
├── unknown/                    # Unclassified runs
│   └── completed/
│       └── run-XXXX/           # Each run is a session
│           ├── run.yaml
│           ├── THOUGHTS.md
│           ├── DECISIONS.md
│           ├── LEARNINGS.md
│           ├── RESULTS.md
│           ├── ASSUMPTIONS.md
│           └── metadata.yaml
├── archived/
├── assets/
└── timeline/
```

---

## Supporting Systems

### Decisions (`decisions/`)
Cross-cutting decision records:
- `active.md` - Active decisions
- `architectural/` - Architecture decisions
- `infrastructure/` - Infrastructure decisions
- `scope/` - Scope decisions
- `technical/` - Technical decisions

### Learnings (`learnings/`)
Cross-cutting learnings:
- `recent.md` - Recent learnings

### Knowledge (`knowledge/`)
Knowledge base with categories:
- `analysis/` - Analysis results
- `architecture/` - Architecture patterns
- `codebase/` - Codebase knowledge
- `first-principles/` - First principles
- `frameworks/` - Framework guides
- `ralf-patterns/` - RALF patterns
- `research/` - Research findings
- `validation/` - Validation patterns

### Operations (`operations/`)
Operational configurations:
- `agents/` - Agent configurations
- `dashboard/` - Dashboard configs
- `logs/` - Operational logs
- `sessions/` - Session records
- `workflows/` - Workflow definitions
- `*.yaml` - Various operational configs

---

## Cross-Reference Pattern

Data lives in ONE place, referenced elsewhere via symlinks:

```
Goal IG-006
└── plans/
    └── project-memory-reorganization → ../../../plans/active/project-memory-reorganization

Plan project-memory-reorganization
└── tasks/
    └── TASK-GOALS-001 → ../../../tasks/active/TASK-GOALS-001
```

This ensures:
- No data duplication
- Single source of truth
- Clear relationships
- Easy navigation

---

## Data Layer Pattern

Every folder at every level can have these data layers:

```
folder/
├── *.yaml or *.md          # Core definition (REQUIRED)
├── THOUGHTS.md             # Thinking/reasoning (optional)
├── DECISIONS.md            # Key decisions (optional)
├── LEARNINGS.md            # What we learned (optional)
├── ASSUMPTIONS.md          # Validated assumptions (optional)
├── RESULTS.md              # Outcomes (optional)
├── timeline/               # Time-based tracking
│   └── YYYY-MM-DD.md
└── [subitems]/             # Next level down
```

---

## Migration Status

| Component | Status | Notes |
|-----------|--------|-------|
| Goals structure | ✅ Complete | All goals have proper subfolders |
| Plans structure | ✅ Complete | All plans have tasks/ folder |
| Tasks structure | ✅ Complete | All tasks have timeline/, subtasks/, artifacts/ |
| Runs structure | ✅ Complete | Organized by agent type |
| Symlinks | ✅ Complete | Goals → Plans → Tasks linked |
| Backups | ✅ Complete | Backups created before migration |

---

## Usage Guidelines

### Creating a New Goal

1. Create folder: `goals/active/GOAL-XXX/`
2. Copy template: `cp goals/templates/goal-template.yaml goals/active/GOAL-XXX/goal.yaml`
3. Edit `goal.yaml` with goal details
4. Create subfolders: `journal/`, `plans/`
5. Link related plans in `plans/`

### Creating a New Plan

1. Create folder: `plans/active/PLAN-XXX/`
2. Create `plan.md` with technical design
3. Create `metadata.yaml` with estimates
4. Create subfolders: `research/`, `tasks/`
5. Link related tasks in `tasks/`
6. Link plan from relevant goal

### Creating a New Task

1. Create folder: `tasks/active/TASK-XXX/`
2. Create `task.md` with specification
3. Create subfolders: `timeline/`, `subtasks/`, `artifacts/`
4. Link task from relevant plan

### During Execution

1. Update `THOUGHTS.md` with reasoning
2. Update `DECISIONS.md` when making key decisions
3. Add entries to `timeline/YYYY-MM-DD.md`
4. Create subtasks in `subtasks/` as needed
5. Store artifacts in `artifacts/`

### On Completion

1. Update `LEARNINGS.md` with insights
2. Update `RESULTS.md` with outcomes
3. Move task: `mv tasks/active/TASK-XXX tasks/completed/`
4. Update status in parent plan/goal

---

## Backup and Recovery

Backups are created before any migration:
- `goals.backup.YYYYMMDD/`
- `plans.backup.YYYYMMDD/`
- `tasks.backup.YYYYMMDD/`
- `runs.backup.YYYYMMDD/`
- `.autonomous.backup.YYYYMMDD/`

To restore from backup:
```bash
cp -r goals.backup.YYYYMMDD/* goals/
cp -r plans.backup.YYYYMMDD/* plans/
cp -r tasks.backup.YYYYMMDD/* tasks/
```

---

## Questions?

Refer to:
- `goals/README.md` - Goal system documentation
- `plans/README.md` - Plan system documentation
- `tasks/README.md` - Task system documentation
- `.autonomous/README.md` - Agent runtime documentation
