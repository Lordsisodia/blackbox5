# Project Structure - BlackBox 5

**Last Updated:** 2026-02-02
**Updated By:** Claude

This document maps the BlackBox 5 project structure. Update this file when the folder organization changes.

## Root Level

```
~/.blackbox5/
├── 5-project-memory/blackbox5/     # Project memory (this project)
├── 2-engine/.autonomous/            # RALF engine
├── bin/                             # Executable scripts
├── prompts/                         # Main prompts
└── .claude/                         # Claude Code configuration
```

## Project Memory Structure

```
5-project-memory/blackbox5/
├── project/          # WHO - Identity, goals, constraints
│   └── context.yaml
├── plans/            # WHAT - Epics, features, PRDs
│   ├── active/
│   ├── briefs/
│   ├── features/
│   └── prds/
├── decisions/        # WHY - Architectural decisions
├── knowledge/        # HOW - Architecture docs, research
├── tasks/            # WHAT - Tasks (legacy location)
│   ├── backlog/
│   ├── completed/
│   └── working/
├── operations/       # System operations
├── .autonomous/      # Autonomous agent files
│   ├── tasks/        # Tasks (current location)
│   │   ├── active/
│   │   ├── completed/
│   │   └── improvements/
│   ├── communications/
│   └── runs/         # Agent run history
└── runs/             # Run history (duplicate?)
```

## Critical Files

| File | Purpose |
|------|---------|
| STATE.yaml | Single source of truth |
| ACTIVE.md | Current work dashboard |
| MAP.yaml | Complete file catalog |
| timeline.yaml | Project timeline |
| WORK-LOG.md | Activity log |

## Task Locations

**Primary:** `.autonomous/tasks/active/`
**Secondary:** `tasks/working/`
**Completed:** `.autonomous/tasks/completed/` and `tasks/completed/`

## Run Locations

**Planner:** `.autonomous/runs/planner/` and `runs/planner/`
**Executor:** `.autonomous/runs/executor/` and `runs/executor/`
