# Plans

> Strategic plans and roadmaps for BlackBox5

## Overview

This directory contains strategic plans, roadmaps, and high-level planning documents for the BlackBox5 project. Plans decompose into tasks for execution.

## Directory Structure

```
plans/
├── active/        # Currently executing plans
├── completed/     # Finished plans
├── roadmap/       # Long-term roadmaps
├── proposals/     # Proposed plans (not yet approved)
└── archive/       # Historical plans
```

## Plan Format

```yaml
id: PLAN-001
title: "Plan Title"
status: draft | approved | active | completed | cancelled
priority: CRITICAL | HIGH | MEDIUM | LOW
created: 2026-01-30T12:00:00Z
target_completion: 2026-03-30

objective: |
  What this plan aims to achieve.

success_criteria:
  - Measurable outcome 1
  - Measurable outcome 2

phases:
  - name: "Phase 1"
    tasks:
      - TASK-001
      - TASK-002
  - name: "Phase 2"
    tasks:
      - TASK-003

dependencies:
  - PLAN-000 (must complete first)

risks:
  - description: "Risk description"
    mitigation: "How to mitigate"
```

## Plan Lifecycle

1. **Draft** - Initial plan creation
2. **Review** - Stakeholder review
3. **Approved** - Ready to execute
4. **Active** - Currently executing
5. **Completed** - All phases done
6. **Cancelled** - Abandoned

## Related Documentation

- [../tasks/README.md](../tasks/README.md) - Tasks within plans
- [../../1-docs/01-theory/03-patterns/hierarchical-planning.md](../../1-docs/01-theory/03-patterns/hierarchical-planning.md) - Planning theory

## Usage

Create plans using `bb5 plan:create "Plan Name"` or manually in active/.
