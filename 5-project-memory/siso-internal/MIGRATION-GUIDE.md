# BlackBox5 to SISO-Internal Migration Guide

**Version:** 1.0.0
**Last Updated:** 2026-02-09
**Purpose:** Comprehensive guide for migrating BlackBox5 project memory structure to SISO-Internal

---

## Table of Contents

1. [Overview](#overview)
2. [Folder Structure](#folder-structure)
3. [Templates Reference](#templates-reference)
4. [Key Patterns](#key-patterns)
5. [Migration Steps](#migration-steps)
6. [File-by-File Guide](#file-by-file-guide)

---

## Overview

This guide documents the complete BlackBox5 project memory structure and provides step-by-step instructions for replicating it in SISO-Internal. The BlackBox5 structure represents a mature, battle-tested organization system for AI agent project memory.

### Core Philosophy

- **Single Source of Truth (SSOT):** `STATE.yaml` is the canonical project state
- **Hierarchy:** Goals → Plans → Tasks with clear parent-child relationships
- **Folder-per-Entity:** Each task, goal, and plan has its own folder
- **Auto-Generated Indexes:** `INDEX.yaml` files provide quick lookup
- **Templates:** Consistent structure through templates

---

## Folder Structure

### Root Level

| Folder/File | Purpose | Template |
|-------------|---------|----------|
| `STATE.yaml` | Single source of truth for project state | `.templates/root/STATE.yaml.template` |
| `goals.yaml` | Goals definition and hierarchy | N/A (derived from goals/) |
| `MAP.yaml` | Complete file-level project map | N/A (auto-generated) |
| `timeline.yaml` | Project timeline and milestones | `.templates/root/timeline.yaml.template` |
| `ACTIVE.md` | Current work dashboard | `.templates/root/ACTIVE.md.template` |
| `WORK-LOG.md` | Chronological activity log | `.templates/root/WORK-LOG.md.template` |
| `README.md` | Project overview | N/A |
| `_NAMING.md` | Naming conventions | `.templates/root/_NAMING.md.template` |
| `QUERIES.md` | Common queries | `.templates/root/QUERIES.md.template` |
| `feature_backlog.yaml` | Pending features | `.templates/root/feature_backlog.yaml.template` |
| `test_results.yaml` | Test outcomes | `.templates/root/test_results.yaml.template` |

### Main Folders

```
.archived/          # Archived historical content
.autonomous/        # RALF autonomous agent system
.claude/            # Claude-specific configuration
.docs/              # AI-managed documentation
.templates/         # Templates for consistent docs
goals/              # WHAT are we working toward?
plans/              # WHAT are we building?
tasks/              # WHAT needs to be done?
decisions/          # WHY are we doing it this way?
knowledge/          # HOW does it work?
operations/         # System operations
project/            # WHO are we?
data/               # Project data
config/             # Configuration files
action-plans/       # Action plans
bin/                # Executables and scripts
```

---

## Templates Reference

### Root Templates (`/.templates/root/`)

| Template | Output Location | Purpose |
|----------|-----------------|---------|
| `STATE.yaml.template` | `/STATE.yaml` | Project state SSOT |
| `ACTIVE.md.template` | `/ACTIVE.md` | Work dashboard |
| `WORK-LOG.md.template` | `/WORK-LOG.md` | Activity log |
| `timeline.yaml.template` | `/timeline.yaml` | Project timeline |
| `feature_backlog.yaml.template` | `/feature_backlog.yaml` | Feature queue |
| `test_results.yaml.template` | `/test_results.yaml` | Test results |
| `_NAMING.md.template` | `/_NAMING.md` | Naming conventions |
| `QUERIES.md.template` | `/QUERIES.md` | Quick reference |

### Task Templates (`/.templates/tasks/`)

| Template | Purpose |
|----------|---------|
| `task-specification.md.template` | Task definition with acceptance criteria |
| `task-folder.template` | Task folder structure guide |
| `THOUGHTS.md.template` | Execution thinking and progress |
| `DECISIONS.md.template` | Key decisions made |
| `RESULTS.md.template` | Final results and deliverables |
| `LEARNINGS.md.template` | Post-completion insights |

### Goal Templates (`/.templates/goals/`)

| Template | Output Location | Purpose |
|----------|-----------------|---------|
| `INDEX.yaml.template` | `/goals/INDEX.yaml` | Goals index |
| `goal.yaml.template` | `/goals/active/IG-XXX/goal.yaml` | Goal definition |

### Epic Templates (`/.templates/epic/`)

| Template | Output Location | Purpose |
|----------|-----------------|---------|
| `epic.md.template` | `/plans/active/{name}/epic.md` | Epic specification |
| `metadata.yaml.template` | `/plans/active/{name}/metadata.yaml` | Epic metadata |
| `TASK-SUMMARY.md.template` | `/plans/active/{name}/TASK-SUMMARY.md` | Task breakdown |
| `README.md.template` | `/plans/active/{name}/README.md` | Epic overview |

### Decision Templates (`/.templates/decisions/`)

| Template | Output Location | Purpose |
|----------|-----------------|---------|
| `architectural.md.template` | `/decisions/architectural/DEC-*.md` | Architecture decisions |
| `scope.md.template` | `/decisions/scope/DEC-*.md` | Scope decisions |
| `technical.md.template` | `/decisions/technical/DEC-*.md` | Technical decisions |

### Research Templates (`/.templates/research/`)

| Template | Output Location | Purpose |
|----------|-----------------|---------|
| `STACK.md.template` | `/plans/active/{name}/research/STACK.md` | Tech stack research |
| `ARCHITECTURE.md.template` | `/plans/active/{name}/research/ARCHITECTURE.md` | Architecture research |
| `FEATURES.md.template` | `/plans/active/{name}/research/FEATURES.md` | Feature analysis |
| `PITFALLS.md.template` | `/plans/active/{name}/research/PITFALLS.md` | Known pitfalls |
| `SUMMARY.md.template` | `/plans/active/{name}/research/SUMMARY.md` | Research summary |

### Operations Templates (`/.templates/operations/`)

| Template | Output Location | Purpose |
|----------|-----------------|---------|
| `skill-registry.yaml.template` | `/operations/skill-registry.yaml` | Skill definitions |
| `quality-gates.yaml.template` | `/operations/quality-gates.yaml` | Quality gate config |
| `metrics-dashboard.yaml.template` | `/operations/metrics-dashboard.yaml` | Metrics tracking |

---

## Key Patterns

### 1. Folder-per-Task Pattern

Each task gets its own folder in `tasks/active/`:

```
tasks/active/TASK-XXX-{description}/
├── task.md              # REQUIRED: Task specification
├── THOUGHTS.md          # REQUIRED: Execution thinking
├── DECISIONS.md         # REQUIRED: Key decisions
├── RESULTS.md           # REQUIRED: Final results
├── LEARNINGS.md         # OPTIONAL: Post-completion insights
├── ASSUMPTIONS.md       # OPTIONAL: Validated assumptions
├── PLAN.md              # OPTIONAL: Detailed execution plan
├── timeline/            # OPTIONAL: Daily progress
├── subtasks/            # OPTIONAL: Nested subtasks
└── artifacts/           # OPTIONAL: Generated files
```

**When to use:**
- Every task gets a folder
- Move to `tasks/completed/` when done
- Archive to `.archived/runs/` when old

### 2. INDEX.yaml in Every Major Directory

Every major folder has an `INDEX.yaml` for quick lookup:

```yaml
# goals/INDEX.yaml
meta:
  generated_at: "2026-02-09T12:00:00Z"
  version: "1.0.0"

summary:
  by_priority:
    critical: [IG-006, IG-008]
    high: [IG-001, IG-002]
  by_status:
    in_progress: [IG-006, IG-007]
    completed: [IG-009]

goals:
  - id: IG-006
    name: "Restructure BlackBox5 Architecture"
    status: in_progress
    progress: 75%
    priority: critical
```

**When to use:**
- Create INDEX.yaml in goals/, plans/, tasks/ folders
- Auto-generate from folder contents
- Run sync script to regenerate

### 3. README.md in Every Folder

Every folder has a README explaining its purpose:

```markdown
# Tasks

**Purpose:** Track all project tasks

## Subfolders

- `active/` - Active task folders
- `completed/` - Completed tasks
- `backlog/` - Backlogged tasks

## Quick Navigation

```bash
bb5 task:list
bb5 task:current
```
```

**When to use:**
- Every folder gets a README.md
- Explain purpose and contents
- Provide quick navigation

### 4. Backup Naming Convention

Backups use this format:

```
{FILENAME}.backup.{TIMESTAMP}
```

Examples:
- `STATE.yaml.backup.1770341176`
- `STATE.yaml.backup.20260204_093350`
- `INDEX.yaml.backup.20260207_224251`

**When to use:**
- Before significant changes
- Automated backups on state changes
- Keep last 10 backups

### 5. YAML Structure Patterns

Consistent YAML structure:

```yaml
# Header with metadata
meta:
  version: "1.0.0"
  last_updated: "2026-02-09T12:00:00Z"
  generated_by: "agent-name"

# Clear section headers
# =============================================================================
# SECTION NAME
# =============================================================================

section_name:
  key: value

  # Sub-sections with indentation
  sub_section:
    - item1
    - item2
```

**Rules:**
- 2-space indentation
- Clear section headers
- meta: block at top
- Comments explain purpose

### 6. Goal/Plan/Task Hierarchy

Hierarchical linking via symlinks:

```
goals/
└── active/
    └── IG-006/
        └── plans/              # Symlinks to linked plans
            └── user-profile -> ../../../plans/active/user-profile

plans/
└── active/
    └── user-profile/
        └── tasks/              # Symlinks to linked tasks
            └── TASK-001 -> ../../../tasks/active/TASK-001
```

**When to use:**
- Link goals to plans
- Link plans to tasks
- Creates navigable hierarchy

### 7. Run Folder Structure

Each run gets a folder in `.autonomous/runs/`:

```
.autonomous/runs/run-{timestamp}/
├── THOUGHTS.md              # REQUIRED: Session thinking
├── DECISIONS.md             # REQUIRED: Decisions made
├── RESULTS.md               # REQUIRED: Outcomes
├── LEARNINGS.md             # OPTIONAL: Insights
├── ASSUMPTIONS.md           # OPTIONAL: Assumptions
└── metadata.yaml            # Run metadata
```

**When to use:**
- Every RALF session gets a run folder
- Timestamp format: `run-1769978192` or `run-20260209_143052`
- Archive old runs to `.archived/runs/`

---

## Migration Steps

### Phase 1: Create Folder Structure

1. Create main folders:
```bash
mkdir -p goals/{active,core,archived}
mkdir -p plans/{active,archived,briefs,features,prds}
mkdir -p tasks/{active,completed,backlog,cancelled,improvements,working}
mkdir -p decisions/{architectural,scope,technical,infrastructure}
mkdir -p knowledge/{architecture,codebase,frameworks,research,validation,first_principles}
mkdir -p operations/{dashboard,agents,logs,sessions,workflows}
mkdir -p project
mkdir -p data
mkdir -p config
mkdir -p .docs
mkdir -p .archived/runs
```

2. Create templates folder (already done):
```bash
mkdir -p .templates/{root,tasks,goals,epic,decisions,research,operations}
```

### Phase 2: Create Root Files

1. Copy templates to root:
```bash
cp .templates/root/STATE.yaml.template STATE.yaml
cp .templates/root/ACTIVE.md.template ACTIVE.md
cp .templates/root/WORK-LOG.md.template WORK-LOG.md
cp .templates/root/timeline.yaml.template timeline.yaml
cp .templates/root/_NAMING.md.template _NAMING.md
cp .templates/root/QUERIES.md.template QUERIES.md
```

2. Fill in templates with project-specific data

### Phase 3: Create Goals System

1. Create goals.yaml:
```bash
# Use goals.yaml.template or create from scratch
# Define core_goals, improvement_goals, data_goals
```

2. Create first goal:
```bash
mkdir -p goals/active/IG-001-{description}
cp .templates/goals/goal.yaml.template goals/active/IG-001-{description}/goal.yaml
```

3. Generate goals index:
```bash
# Create goals/INDEX.yaml from template
cp .templates/goals/INDEX.yaml.template goals/INDEX.yaml
```

### Phase 4: Create Operations Dashboard

1. Create operations files:
```bash
cp .templates/operations/skill-registry.yaml.template operations/skill-registry.yaml
cp .templates/operations/quality-gates.yaml.template operations/quality-gates.yaml
cp .templates/operations/metrics-dashboard.yaml.template operations/metrics-dashboard.yaml
```

### Phase 5: Create First Task

1. Create task folder:
```bash
mkdir -p tasks/active/TASK-001-{description}
```

2. Copy task templates:
```bash
cp .templates/tasks/task-specification.md.template tasks/active/TASK-001-{description}/task.md
cp .templates/tasks/THOUGHTS.md.template tasks/active/TASK-001-{description}/THOUGHTS.md
cp .templates/tasks/DECISIONS.md.template tasks/active/TASK-001-{description}/DECISIONS.md
cp .templates/tasks/RESULTS.md.template tasks/active/TASK-001-{description}/RESULTS.md
```

3. Fill in task.md with details

---

## File-by-File Guide

### STATE.yaml

**Location:** `/STATE.yaml`
**Template:** `.templates/root/STATE.yaml.template`
**Purpose:** Single source of truth for project state

**Key Sections:**
- `project:` - Metadata (name, version, status)
- `goals:` - Goal status (derived from goals/)
- `tasks:` - Active and completed tasks
- `features:` - Feature status
- `decisions:` - Decision tracking
- `research:` - Active research
- `github_sync:` - Git sync status
- `system:` - System health
- `timeline:` - Milestone tracking
- `activity:` - Recent activity
- `risks:` - Risk tracking

**Usage:**
- Update after every significant change
- Auto-backup on changes
- Reference at session start

### goals.yaml

**Location:** `/goals.yaml`
**Purpose:** Define all project goals

**Key Sections:**
- `core_goals:` - Why we exist
- `improvement_goals:` - How we get better
- `data_goals:` - What we track
- `review_schedule:` - When to review

**Usage:**
- Define goals at project start
- Update monthly
- Reference for prioritization

### goals/INDEX.yaml

**Location:** `/goals/INDEX.yaml`
**Template:** `.templates/goals/INDEX.yaml.template`
**Purpose:** Quick lookup for all goals

**Key Sections:**
- `summary:` - Counts by priority and status
- `by_priority:` - Goals grouped by priority
- `by_status:` - Goals grouped by status
- `goals:` - Detailed goal list

**Usage:**
- Auto-generate from goals/active/
- Run sync script to update
- Use for quick status checks

### goals/active/IG-XXX/goal.yaml

**Location:** `/goals/active/IG-XXX/goal.yaml`
**Template:** `.templates/goals/goal.yaml.template`
**Purpose:** Individual goal definition

**Key Sections:**
- `goal_id:` - Unique identifier
- `name:` - Goal name
- `description:` - Goal description
- `meta:` - Created, target, owner, priority, status
- `sub_goals:` - Breakdown into sub-goals
- `progress:` - Progress tracking
- `links:` - Related items
- `notes:` - Additional notes

**Usage:**
- Create for each goal
- Update progress regularly
- Link to plans and tasks

### tasks/active/TASK-XXX/task.md

**Location:** `/tasks/active/TASK-XXX/task.md`
**Template:** `.templates/tasks/task-specification.md.template`
**Purpose:** Task specification

**Key Sections:**
- Header: Status, Priority, Type, Dates
- `Description:` - What to do
- `Pre-Execution Validation:` - Checks before starting
- `Acceptance Criteria:` - Must-have, Should-have, Nice-to-have
- `Dependencies:` - Requires, Blocks
- `Context:` - Background
- `Approach:` - How to do it
- `Rollback Strategy:` - How to undo
- `Effort:` - Estimated and actual
- `Notes:` - Additional info

**Usage:**
- Create before starting work
- Update status as you go
- Fill RESULTS.md on completion

### operations/skill-registry.yaml

**Location:** `/operations/skill-registry.yaml`
**Template:** `.templates/operations/skill-registry.yaml.template`
**Purpose:** Skill definitions and metrics

**Key Sections:**
- `metadata:` - Registry metadata
- `metrics_schema:` - How metrics are calculated
- `skills:` - All skill definitions
- `usage_history:` - Usage records
- `selection_rules:` - How to select skills
- `improvement_tracking:` - Improvement metrics

**Usage:**
- Define all skills here
- Track usage and effectiveness
- Update selection criteria

---

## Quick Reference

### Naming Conventions

| Item | Format | Example |
|------|--------|---------|
| Tasks | `TASK-{YYYY-MM-DD}-{NNN}` or `TASK-{TIMESTAMP}` | `TASK-2026-02-09-001` |
| Goals | `IG-{NNN}` or `CG-{NNN}` | `IG-006` |
| Plans | `{descriptive-name}` | `user-profile` |
| Decisions | `DEC-{YYYY-MM-DD}-{TYPE}-{slug}` | `DEC-2026-02-09-ARCH-folder-structure` |
| Research | `{DIMENSION}.md` | `STACK.md` |
| Backups | `{FILENAME}.backup.{TIMESTAMP}` | `STATE.yaml.backup.1770341176` |
| Runs | `run-{TIMESTAMP}` | `run-1769978192` |

### Status Values

| Entity | Valid Status Values |
|--------|---------------------|
| Goals | `not_started`, `in_progress`, `completed`, `draft`, `cancelled`, `merged` |
| Tasks | `pending`, `in_progress`, `completed`, `blocked` |
| Plans | `draft`, `active`, `completed`, `archived` |
| Decisions | `proposed`, `accepted`, `deprecated`, `superseded` |
| Features | `planning`, `in_development`, `testing`, `ready` |

### Priority Levels

- `critical` - Must do, blocks other work
- `high` - Important, do soon
- `medium` - Normal priority
- `low` - Do when convenient

---

## Troubleshooting

### "Not in goals/plans/tasks hierarchy"

Run `bb5 root` to go to project root, then navigate from there.

### "Goal/Plan/Task not found"

Use list commands:
```bash
bb5 goal:list
bb5 plan:list
bb5 task:list
```

### "Missing task.md"

Create task properly:
```bash
bb5 task:create "Task Name"
```

### STATE.yaml out of sync

Regenerate from source:
```bash
# Derive task counts from tasks/active/
# Derive goal counts from goals/active/
# Update timestamps
```

---

## Additional Resources

- **BlackBox5 Reference:** `~/.blackbox5/5-project-memory/blackbox5/`
- **Navigation Guide:** `NAVIGATION-GUIDE.md`
- **Folder Structure:** `.templates/folder-structure.template`
- **bb5 CLI:** `~/.blackbox5/bin/bb5*`

---

*This guide is a living document. Update it as the system evolves.*
