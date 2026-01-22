# Task Registry System - Quick Start Guide

## Overview

The Task Registry System provides execution tracking for hierarchical tasks defined in epic.md and TASK-BREAKDOWN.md files.

## Quick Test

### Option 1: Run the Test Workflow Script

```bash
cd 2-engine/07-operations/runtime
./test-workflow.sh
```

### Option 2: Manual Step-by-Step

```bash
cd 2-engine/07-operations/runtime

# 1. Import tasks from epic
python -m task_registry.cli import-epic \
  ../../../5-project-memory/siso-internal/plans/active/user-profile/epic.md \
  --breakdown ../../../5-project-memory/siso-internal/plans/active/user-profile/TASK-BREAKDOWN.md

# 2. List all tasks
python -m task_registry.cli list

# 3. Show available tasks
python -m task_registry.cli available

# 4. Take a task
python -m task_registry.cli take TASK-1-1 --agent my-agent

# 5. Start working
python -m task_registry.cli start TASK-1-1

# 6. Complete task
python -m task_registry.cli complete TASK-1-1
```

### Option 3: Run Tests

```bash
cd 2-engine/07-operations/runtime
pytest tests/task_registry/ -v
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `task list` | List all tasks |
| `task available` | Show assignable tasks |
| `task take TASK-001` | Assign to yourself |
| `task start TASK-001` | Mark as ACTIVE |
| `task complete TASK-001` | Mark as DONE |
| `task stats` | Show statistics |
| `task import-epic epic.md` | Import from epic |
| `task workspace TASK-001` | Show workspace path |

## File Locations

| File | Location |
|------|----------|
| Registry | `2-engine/07-operations/runtime/data/task_registry.json` |
| Workspaces | `2-engine/07-operations/runtime/workspaces/TASK-XXX/` |
| Epic Files | `5-project-memory/siso-internal/plans/active/*/epic.md` |
| Decision | `5-project-memory/siso-internal/decisions/architectural/DEC-2026-01-21-task-registry-system.md` |
