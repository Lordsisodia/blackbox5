# Tasks

> Task management for BlackBox5 project

## Overview

This directory contains task definitions, tracking, and management for the BlackBox5 project. Tasks represent discrete units of work to be completed by agents.

## Directory Structure

```
tasks/
├── active/        # Currently pending or in-progress tasks
├── completed/     # Finished tasks (archived)
├── templates/     # Task templates for common types
└── backlog/       # Future tasks not yet scheduled
```

## Task Format

Tasks follow this YAML structure:
```yaml
id: TASK-001
title: "Descriptive task title"
status: pending | in_progress | completed
priority: CRITICAL | HIGH | MEDIUM | LOW
created: 2026-01-30T12:00:00Z
assigned_to: agent_name

objective: |
  Clear description of what needs to be done.

success_criteria:
  - Criterion 1
  - Criterion 2

context: |
  Background information needed to complete the task.

approach: |
  1. Step one
  2. Step two

rollback_strategy: |
  How to undo if things go wrong.
```

## Task Lifecycle

1. **Created** - Task defined and added to active/
2. **Assigned** - Agent claims the task
3. **In Progress** - Agent actively working
4. **Completed** - Task finished, moved to completed/
5. **Archived** - Old tasks purged periodically

## Related Documentation

- [../plans/README.md](../plans/README.md) - Plans containing tasks
- [../memory/README.md](../memory/README.md) - Project memory
- [../../1-docs/03-guides/02-common-patterns/task-creation.md](../../1-docs/03-guides/02-common-patterns/task-creation.md) - Task creation guide

## Usage

Create tasks using `bb5 task:create "Task Name"` or manually in active/.
