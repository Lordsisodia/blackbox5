# AI Agent Guide to Blackbox5 Project Memory

**Version**: 1.0
**Updated**: 2026-01-20
**Purpose**: Complete guide for AI agents to understand and use the Blackbox5 project memory system

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [System Architecture](#system-architecture)
3. [Framework vs Projects](#framework-vs-projects)
4. [The 6-Folder Organization](#the-6-folder-organization)
5. [How to Find Information](#how-to-find-information)
6. [How to Write Information](#how-to-write-information)
7. [Working with Templates](#working-with-templates)
8. [Integration Points](#integration-points)
9. [Best Practices](#best-practices)
10. [Common Patterns](#common-patterns)

---

## Quick Start

### For New Agents Starting Work

```bash
# 1. Read project context first
cat 5-project-memory/siso-internal/project/_meta/context.yaml

# 2. Check what's being worked on
cat 5-project-memory/siso-internal/tasks/active/

# 3. Read the main README
cat 5-project-memory/siso-internal/README.md

# 4. Check current project state
cat 5-project-memory/siso-internal/STATE.yaml
```

### For Agents Saving Session Data

```python
from pathlib import Path

# Determine project memory path
project_memory = Path("blackbox5/5-project-memory")
project_id = "siso-internal"  # or your project ID

# Session data goes to:
session_path = project_memory / project_id / "operations/agents/history/sessions/{your-agent-name}/"

# Create the directory
session_path.mkdir(parents=True, exist_ok=True)

# Save session
session_file = session_path / "session.json"
```

---

## System Architecture

### Three-Tier Memory System

```
┌─────────────────────────────────────────────────────────────────┐
│                    BLACKBOX5 PROJECT MEMORY                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐                                           │
│  │ FRAMEWORK LEVEL  │  _template/, code_index.md, INDEX.yaml      │
│  │ (Reusable)       │                                           │
│  └──────────────────┘                                           │
│           │                                                       │
│           ▼                                                       │
│  ┌──────────────────┐                                           │
│  │  PROJECT LEVEL   │  siso-internal/, other-project/             │
│  │  (Project-Specific)│                                           │
│  └──────────────────┘                                           │
│                                                                  │
│  Within Each Project:                                            │
│  ┌────────────┬────────────┬────────────┬────────────┐          │
│  │ Working    │ Extended   │ Archival   │ Knowledge  │          │
│  │ Memory     │ Memory     │ Memory     │ Graph      │          │
│  │ (~10MB)    │ (~500MB)    │ (~5GB)     │            │          │
│  └────────────┴────────────┴────────────┴────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Memory Tier Definitions

| Tier | Location | Purpose | Duration | Size |
|------|----------|---------|----------|------|
| **Working** | `tasks/working/` | Active session transient data | Session only | ~10MB |
| **Extended** | Project folders | Persistent project memory | Permanent | ~500MB |
| **Archival** | `legacy/`, `artifacts/` | Historical artifacts | Permanent | ~5GB |

---

## Framework vs Projects

### Framework Level (`_template/`)

**Purpose**: Reusable templates for new projects

**Key Templates**:
- `_template/operations/agents/history/sessions/thought-loop/` - Thought Loop session templates
- `_template/plans/` - Plan templates (PRDs, epics, features, tasks)
- `_template/decisions/` - Decision templates
- `_template/tasks/` - Task templates

**Usage**: When creating a new project, copy `_template/` and rename it.

### Project Level (`siso-internal/`)

**Purpose**: Actual project memory for a specific project

**Structure**:
```
siso-internal/
├── decisions/          # Why we're doing it this way
├── knowledge/          # How it works + learnings
├── operations/         # System operations (including agent memory)
├── plans/              # What we're building
├── project/            # Project identity & direction
└── tasks/              # What we're working on
```

---

## The 6-Folder Organization

Projects are organized by **question type** (how AI agents think), not file type.

### 1. `decisions/` - "Why This Approach?"

**Question**: "Why are we doing it this way?"

**Structure**:
```
decisions/
├── architectural/     # Architectural decisions
├── scope/            # Scope decisions (in/out of scope)
└── technical/         # Technical decisions (tech choices, patterns)
```

**When to use**: Documenting why a specific approach was chosen.

**Example**: `decisions/architectural/DEC-2026-01-20-use-postgres.md`

### 2. `knowledge/` - "How It Works?"

**Question**: "How does it work? What have we learned?"

**Structure**:
```
knowledge/
├── artifacts/         # Completed work outputs
├── codebase/          # Code patterns and gotchas
├── graph/             # Knowledge graph (entities, relationships)
└── research/          # Research findings
    └── active/        # Active research topics
```

**When to use**: Storing learnings, patterns, and research findings.

**Example**: `knowledge/codebase/cache-patterns.md`

### 3. `operations/` - "How Does the AI System Run?"

**Question**: "How does the AI system operate?"

**Structure**:
```
operations/
├── agents/            # Agent memory
│   ├── active/        # Currently running agents
│   └── history/       # Past agent sessions
│       └── sessions/   # Named sessions (including thought-loop)
├── architecture/       # Architecture validation
├── docs/              # System documentation
├── github/            # GitHub integration
├── logs/              # System logs
├── sessions/          # Session transcripts
└── workflows/         # Workflow execution
```

**When to use**: Storing agent sessions, operations data, workflow info.

**Example**: `operations/agents/history/sessions/thought-loop/sessions.json`

### 4. `plans/` - "What Are We Building?"

**Question**: "What are we building?"

**Structure**:
```
plans/
├── active/            # Active epics (user-profile, etc.)
├── archived/          # Completed/cancelled plans
├── briefs/            # Product briefs
├── features/           # Feature management
└── prds/              # Product requirements
    ├── active/        # Active PRDs
    ├── backlog/       # PRD backlog
    └── completed/     # Completed PRDs
```

**When to use**: Planning features, writing PRDs, defining epics.

**Example**: `plans/active/user-profile/epic.md`

### 5. `project/` - "What Is This Project?"

**Question**: "What is this project?"

**Structure**:
```
project/
├── _meta/             # Project metadata
│   ├── context.yaml    # Project context (goals, constraints, scope)
│   ├── project.yaml    # Project metadata (name, version, team)
│   └── timeline.yaml    # Timeline, milestones, events
├── directions/        # Strategic direction
└── goals/             # Current goals and metrics
```

**When to use**: Defining project identity, tracking goals, updating context.

**Example**: `project/_meta/context.yaml`

### 6. `tasks/` - "What Are We Working On?"

**Question**: "What are we working on right now?"

**Structure**:
```
tasks/
├── active/            # Active task files (TASK-YYYY-MM-DD-NNN.md)
├── completed/         # Completed tasks
├── working/           # Working task folders (transient)
└── archived/          # Old completed tasks
```

**When to use**: Creating tasks, tracking progress, updating status.

**Example**: `tasks/active/TASK-2026-01-20-001.md`

---

## How to Find Information

### By Question Type

| Question | Go To |
|----------|--------|
| "What are we building?" | `plans/active/` |
| "Why this approach?" | `decisions/` |
| "How does it work?" | `knowledge/codebase/` |
| "What are we working on?" | `tasks/active/` |
| "What is this project?" | `project/_meta/` |
| "How does the AI system run?" | `operations/` |

### By File Type

| What You Need | File Pattern | Location |
|---------------|--------------|----------|
| PRD | `*prd*.md` | `plans/prds/` |
| Epic | `epic.md` | `plans/active/{feature}/` |
| Task | `TASK-*.md` | `tasks/active/` |
| Decision | `DEC-*.md` | `decisions/{type}/` |
| Research | `{topic}/*.md` | `knowledge/research/` |

### Key Index Files

- **`INDEX.yaml`** - Central metadata index (global)
- **`code_index.md`** - Code structure index (global)
- **`STATE.yaml`** - Single source of truth for project state (project level)
- **`QUERIES.md`** - Query patterns for agents (project level)

---

## How to Write Information

### Task Files

```bash
# Location: tasks/active/TASK-YYYY-MM-DD-NNN.md
cp _template/tasks/_template.yaml tasks/active/TASK-2026-01-20-001.md
```

### PRD Files

```bash
# Location: plans/prds/active/
cp _template/plans/_template-prd.md plans/prds/active/{feature}-prd.md
```

### Decision Files

```bash
# Location: decisions/{type}/
# Naming: DEC-YYYY-MM-DD-{type}-{slug}.md
# Types: architectural, scope, technical
```

### Research Files

```bash
# Location: knowledge/research/{topic}/
# Files: STACK.md, FEATURES.md, ARCHITECTURE.md, PITFALLS.md, SUMMARY.md
```

### Agent Session Files

```python
# For Thought Loop sessions
from thought_loop import ThoughtLoop
loop = ThoughtLoop()  # Auto-saves to operations/agents/history/sessions/thought-loop/

# For other agents, save to:
# operations/agents/history/sessions/{agent-name}/
```

---

## Working with Templates

### Template Locations

```
_template/
├── operations/
│   └── agents/
│       └── history/
│           └── sessions/
│               └── thought-loop/    # Thought Loop templates
├── plans/
│   ├── _template-prd.md
│   ├── _template-epic.md
│   └── _template-task.md
└── tasks/
    └── _template.yaml
```

### Using Templates

1. **Find the template**: Look in `_template/` for the relevant template
2. **Copy to target**: Copy to the appropriate project folder
3. **Customize**: Fill in the template fields
4. **Follow naming**: Use the naming conventions from `_NAMING.md`

---

## Integration Points

### For Thought Loop Framework

```python
from thought_loop import ThoughtLoop, ProjectMemoryIntegration

# Auto-save enabled by default
loop = ThoughtLoop(project_id="siso-internal")
result = await loop.run("Should we add caching?")
# Session automatically saved to:
# operations/agents/history/sessions/thought-loop/sessions.json

# Manual memory operations
memory = ProjectMemoryIntegration(project_id="siso-internal")
sessions = await memory.get_recent_sessions(limit=10)
patterns = await memory.get_patterns()
insights = await memory.get_insights()
metrics = await memory.get_metrics()
```

### For Other Agents

```python
from pathlib import Path
import json

# Save agent session
def save_agent_session(project_id, agent_name, session_data):
    project_memory = Path("blackbox5/5-project-memory")
    session_path = project_memory / project_id / "operations/agents/history/sessions" / agent_name
    session_path.mkdir(parents=True, exist_ok=True)

    session_file = session_path / "session.json"
    with open(session_file, 'w') as f:
        json.dump(session_data, f, indent=2)
```

### For Task Management

```python
# Read active tasks
tasks_dir = Path("blackbox5/5-project-memory/siso-internal/tasks/active")
task_files = list(tasks_dir.glob("TASK-*.md"))

# Update task status
# Edit the task file directly, following the template structure
```

---

## Best Practices

### 1. Read First, Write Second

Before creating new files:
1. Read `project/_meta/context.yaml` to understand the project
2. Check if the file already exists
3. Use templates for consistency
4. Follow naming conventions from `_NAMING.md`

### 2. Single Source of Truth

- Each piece of information lives in ONE place
- Don't duplicate files across folders
- Use links/references when needed

### 3. Question-Based Organization

When deciding where to put a file, ask:
- **"What question does this answer?"**
- Put the file in the folder that matches the question type

### 4. Use Atomic Operations

When saving JSON files:
```python
# Atomic write (prevents corruption)
temp_file = target_file.with_suffix('.tmp')
with open(temp_file, 'w') as f:
    json.dump(data, f, indent=2)
temp_file.replace(target_file)
```

### 5. Update State Files

When completing work:
1. Update task status in `tasks/active/`
2. Move to `tasks/completed/` when done
3. Update `STATE.yaml` if significant progress made

---

## Common Patterns

### Creating a New Feature

1. **Research**: `knowledge/research/{feature}/`
2. **PRD**: `plans/prds/active/{feature}-prd.md`
3. **Epic**: `plans/active/{feature}/epic.md`
4. **Tasks**: `tasks/active/TASK-*.md`

### Recording a Decision

1. Go to `decisions/{type}/`
2. Create `DEC-YYYY-MM-DD-{type}-{slug}.md`
3. Document: Context, Decision, Rationale, Alternatives, Implications

### Agent Session Management

1. **Active Session**: `operations/agents/active/{agent-name}/session.json`
2. **Completed Session**: Archive to `operations/agents/history/sessions/{agent-name}/`

### Working with GitHub Sync

1. Update files locally
2. GitHub integration in `operations/github/` handles syncing
3. Check sync history for status

---

## File Reference

### Essential Files to Read First

| File | Purpose | When to Read |
|------|---------|-------------|
| `siso-internal/README.md` | Project overview | Starting work |
| `siso-internal/project/_meta/context.yaml` | Project context | Before any task |
| `siso-internal/STATE.yaml` | Current state | Checking progress |
| `siso-internal/_NAMING.md` | Naming conventions | Creating files |
| `INDEX.yaml` | Global index | Searching globally |

### Template Files

| Template | For Creating | Location |
|----------|--------------|----------|
| `_template-prd.md` | PRDs | `_template/plans/` |
| `_template-epic.md` | Epics | `_template/plans/` |
| `_template-task.yaml` | Tasks | `_template/tasks/` |
| `sessions.json` | Session data | `_template/operations/agents/history/sessions/thought-loop/` |

---

## Getting Help

### Documentation

- Project memory README: `5-project-memory/README.md`
- SISO Internal README: `5-project-memory/siso-internal/README.md`
- Reorganization docs: `.blackbox5/5-project-memory/REORGANIZATION-COMPLETE.md`

### Quick Commands

```bash
# Find all active tasks
find 5-project-memory/siso-internal/tasks/active/ -name "TASK-*.md"

# Find all active PRDs
find 5-project-memory/siso-internal/plans/prds/active/ -name "*prd*.md"

# Check project state
cat 5-project-memory/siso-internal/STATE.yaml

# List all decisions
find 5-project-memory/siso-internal/decisions/ -name "DEC-*.md"

# Count files by type
find 5-project-memory/siso-internal/ -name "*.md" | wc -l
find 5-project-memory/siso-internal/ -name "*.yaml" | wc -l
find 5-project-memory/siso-internal/ -name "*.json" | wc -l
```

---

**Last Updated**: 2026-01-20
**Maintained By**: Blackbox5 AI Agents
**Version**: 1.0
