---
name: bb5-project-setup
description: Initialize a new BB5 (BlackBox5) autonomous project with full memory structure
tags: [bb5, project-setup, memory, autonomous, scaffolding]
tier: 2
author: BB5
version: 1.0.0
---

# BB5 Project Setup

Initialize a complete BB5 autonomous project structure with all necessary directories, configuration files, and templates.

## Usage

```
Activate bb5-project-setup for project <project-name>
```

Or:

```
Set up a new BB5 project called <project-name>
```

## What It Creates

### 1. Project Directory Structure

```
5-project-memory/<project-name>/
├── .autonomous/
│   ├── agents/communications/     # Agent spawn queue and communications
│   ├── memory/
│   │   ├── data/                  # Vector store and embeddings
│   │   └── contexts/              # Conversation contexts
│   ├── tasks/
│   │   ├── active/                # Active tasks
│   │   ├── completed/             # Completed tasks
│   │   └── improvements/          # Pending improvements
│   ├── runs/                      # Run history
│   └── state/                     # Current state files
├── context/
│   ├── stakeholders.md            # Key people and roles
│   ├── tech-stack.md              # Technologies used
│   ├── architecture.md            # System design
│   └── requirements.md            # Feature requirements
├── goals/
│   ├── active/                    # Active goals
│   └── completed/                 # Completed goals
├── runs/                          # Current run folder
├── knowledge/                     # Project knowledge base
├── decisions/                     # Decision log
├── learnings/                     # Learnings and patterns
├── plans/                         # Project plans
├── CLAUDE.md                      # Project-specific guidance
├── goals.yaml                     # Project goals
├── STATE.yaml                     # Current state
└── README.md                      # Project overview
```

### 2. Goals Template

Creates `goals.yaml`:

```yaml
project: <ProjectName>
description: <Project description>
status: active
created: <timestamp>

core_goals:
  - id: <PG>-001
    name: "Project Foundation"
    description: "Establish core project infrastructure"
    priority: critical
    status: active
    success_criteria:
      - "Project structure complete"
      - "Initial goals defined"
      - "Documentation started"

improvement_goals: []

data_goals:
  - id: <PG>-D001
    name: "Capture Learnings"
    description: "Document what works and what doesn't"
    priority: high
    status: active

review_schedule:
  first_principles_review:
    frequency: "every 5 runs"
    auto_trigger: true
```

### 3. CLAUDE.md Template

Creates project-specific guidance:

```markdown
# <ProjectName> - Claude Guidance

## Project Overview
<Brief description>

## Key Context
- **Stakeholders**: See context/stakeholders.md
- **Tech Stack**: See context/tech-stack.md
- **Architecture**: See context/architecture.md
- **Requirements**: See context/requirements.md

## Working Patterns
1. Always check goals.yaml before starting work
2. Document decisions in decisions/
3. Capture learnings in learnings/
4. Use .autonomous/tasks/active/ for task tracking

## Integration with BB5
- This project uses BB5 infrastructure
- Agent teams activate automatically
- Runs are tracked in .autonomous/runs/
```

### 4. State Tracking

Creates `STATE.yaml`:

```yaml
project: <ProjectName>
status: active
last_updated: <timestamp>

current_focus: null
active_tasks: 0
completed_tasks: 0
pending_improvements: 0

metrics:
  runs_completed: 0
  learnings_captured: 0
  decisions_made: 0
```

### 5. Context Files

- **stakeholders.md** - Key people, roles, contact info
- **tech-stack.md** - Technologies, versions, dependencies
- **architecture.md** - System design, diagrams
- **requirements.md** - Feature requirements, user stories

## Integration

Once created, the project:
- Appears in BB5 project router
- Gets its own agent team activation
- Shares BB5 infrastructure (skills, memory, hooks)
- Can spawn project-specific sub-agents
- Is tracked in BB5's goal system

## Next Steps After Setup

1. Populate context files with project details
2. Set initial goals in goals.yaml
3. Create first tasks in `.autonomous/tasks/active/`
4. Begin work - agent teams will auto-activate
5. Run `bb5-context-collector` to establish baseline

## Example

```
User: Set up a new BB5 project called "acme-platform"

Agent: Creates full structure at 5-project-memory/acme-platform/
- All directories initialized
- Template files created
- Goals.yaml with AC-001 goal
- Ready for work to begin
```
