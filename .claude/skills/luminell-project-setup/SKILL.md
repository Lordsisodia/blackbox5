---
name: luminell-project-setup
description: Initialize Luminell project memory structure in BB5
tags: [luminell, project-setup, memory, siso-internal]
tier: 2
author: BB5
version: 1.0.0
---

# Luminell Project Setup

Initialize a complete Luminell project memory structure within BB5 for SISO Internal.

## Usage

```
Activate luminell-project-setup for Luminell project
```

## What It Creates

### 1. Project Directory Structure
```
5-project-memory/luminell/
├── .autonomous/
│   ├── tasks/active/
│   ├── tasks/completed/
│   ├── memory/data/
│   └── agents/communications/
├── runs/
├── goals.yaml
├── CLAUDE.md
├── THOUGHTS.md
├── DECISIONS.md
├── LEARNINGS.md
└── context/
    ├── stakeholders.md
    ├── tech-stack.md
    ├── architecture.md
    └── requirements.md
```

### 2. Goals Template

Creates `goals.yaml`:

```yaml
project: Luminell
description: AI-powered business intelligence platform
status: active

core_goals:
  - id: LG-001
    title: Build Core Platform
    description: Develop the foundational Luminell platform
    status: active
    priority: critical

improvement_goals:
  - id: LI-001
    title: Optimize Performance
    description: Improve query response times
    status: pending
    priority: high

data_goals:
  - id: LD-001
    title: Data Pipeline
    description: Establish data ingestion pipeline
    status: pending
    priority: high
```

### 3. CLAUDE.md Template

Project-specific guidance for Luminell work.

### 4. Context Files

- **stakeholders.md** - Key people and roles
- **tech-stack.md** - Technologies used
- **architecture.md** - System design
- **requirements.md** - Feature requirements

## Integration

Once created, Luminell project:
- Appears in BB5 project router
- Gets its own agent team activation
- Shares BB5 infrastructure (skills, memory, hooks)
- Can spawn Luminell-specific sub-agents

## Next Steps After Setup

1. Populate context files with project details
2. Set initial goals and priorities
3. Create first tasks in `.autonomous/tasks/active/`
4. Begin work - agent teams will auto-activate
