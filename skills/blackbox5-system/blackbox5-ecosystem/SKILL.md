---
name: blackbox5-ecosystem
description: Complete guide to BlackBox5 ecosystem - agents, memory, knowledge base, dashboard, automation
category: training
version: 1.0
auto-invoke: false
confidence-threshold: 0.8
---

# BlackBox5 Ecosystem Guide

## Purpose

This is the master guide to understanding and using the BlackBox5 system, including all its autonomous agents, memory systems, and automation frameworks.

## System Overview

### Core Components

```
┌─────────────────────────────────────────────┐
│                                     │
│  ┌───────────┐          │
│  │  Dashboard  │          │
│  │            │          │
│  │  ┌─────────┴─────────┐ │
│  │ │  Main      │  │          │
│  │ │ (Orchestrator)   │          │
│  │ └───┼───────────┘ │
│  │            │          │
│  └────────────────────────────────────┘ │
│                                     │
│  ┌─────────────────────────────────────┐
│  │          │                │
│  │   Agents  │               │
│  │   Scribe   │               │
│  │   Task Mgr  │               │
│  │ └─────────┴─────────┘ │
│  │          │                │
│  ┌───────────┐          │
│  │  Agents   │          │
│  │ └─────────┘ │
│  │          │                │
│  └─────────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────────────┘
```

- **Dashboard**: Fresh Mind-style UI at `http://77.42.66.40:8001/`
- **BlackBox5 Memory**: Task documentation, knowledge base, scribe system
- **Autonomous Agents**: 5 specialized agents running in parallel
- **Frameworks**: BMAD, RALF, custom agents for complex workflows
- **Communication**: OpenClaw session management, agent spawning, cross-agent coordination

## BlackBox5 Directory Structure

```
/opt/blackbox5/
├── 5-project-memory/blackbox5/         # All your project data
│   ├── tasks/                        # Task management (active, completed, etc.)
│   │   └── ROADMAP-COMPREHENSIVE-IMPLEMENTATION.md
│   ├── knowledge/                     # Learnings, patterns, decisions
│   ├── .autonomous/                    # Autonomous agent activity
│   ├── agents/                       # Agent definitions and implementations
│   ├── dashboard-ui/                   # Dashboard UI and gateway
│   ├── youtube-scraper/               # YouTube automation
│   ├── 2-engine/                       # Core engine components
│   └── skills/                          # OpenClaw skills
│
/opt/openclaw/                             # OpenClaw configuration
├── .claude/agents/                        # OpenClaw agent configurations
│   ├── main/                             # Main orchestrator
│   ├── content/                           # Content strategist
│   ├── engineering/                     # Engineering lead
│   ├── general/                         # General assistant
│   └── task-agent/                     # Task manager
│
/root/.openclaw/                           # OpenClaw workspace
├── workspace/                            # Working directory
└── agents/                               # Sub-agent sessions
```

## Dashboard Usage

### Access

**From VPS:**
```
http://77.42.66.40:8001/
```

**From Mac (via SSH tunnel):**
```
http://localhost:8001/
```

### Dashboard Features

### Real-Time Monitoring
- **Agent Status Cards**: Running, idle, completed, error states
- **Task Progress**: Current task and uptime for each agent
- **Token Usage**: Per-agent token consumption
- **Start/Stop Controls**: Instant agent management
- **Create New Task**: Purple button → task generation
- **Create New Agent**: Add custom agents

### Agent Types Available

| Agent | Purpose | Use For |
|--------|----------|---------|
| **main** | Orchestrator | Coordinating all agents |
| **content** | Content Strategy | YouTube, marketing, content planning |
| **engineering** | Engineering Lead | Code review, architecture, development |
| **general** | General Assistant | Research, documentation, questions |
| **task-agent** | Task Management | Task creation, prioritization |
| **conversational-planner** | Natural Tasks | Transform talk → structured tasks |
| **youtube-scraper** | YouTube Automation | Continuous video scraping |
| **kimi-load-balancer** | API Management | Smart rotation of 9 keys |
| **multi-api-manager** | Multi-Provider API | Google, Claude, OpenAI |

### Agent Cards

Each agent card shows:
- **Agent Name** (e.g., "BlackBox5 Scribe")
- **Status Badge** (running/idle/error)
- **Current Task** (what they're working on)
- **Uptime** (how long they've been running)
- **Tokens Used** (cumulative)
- **Actions**: 
  - 💬 Talk to Agent (creates new session)
  - 📋 View Logs (see agent activity)
  - ▶ Start Agent
  - ⏹ Stop Agent

### Stats Bar

Bottom dashboard shows:
- **Active Tasks**: Number of tasks in progress
- **Running**: Number of currently active agents
- **Idle**: Number of idle agents
- **Errors**: Number of agents in error state
- **Total Tasks Completed**: Cumulative completed task count

## Task Management

### Creating Tasks

1. Click **"Create New Task"** button
2. Fill in:
   - Task Title
   - Priority (🔴 High / 🟡 Medium / 🟢 Low)
   - Description
   - Assign To Agent
3. Click **"Create Task"**
4. Task is created as `TASK-YYYYMMDD-HHMMSS.md`
5. Placed in `/opt/blackbox5/5-project-memory/blackbox5/tasks/active/`
6. Agent is notified and can start working

### Task Status

- **Pending**: Created, waiting for assignment
- **In Progress**: Agent has picked up task
- **Completed**: Agent finished task
- **Failed**: Agent couldn't complete (with error reason)

### Task Files

Tasks are Markdown files with frontmatter:
```yaml
---
title: Task Title
priority: high
assigned: content
description: Full task description

created: 2026-02-10T19:20:00.000Z

## Next Steps

[ ] Initial setup
[ ] Implementation
[ ] Testing
[ ] Completion
---
```

### Task Consolidation

**Current State:**
- 66 active tasks (down from 175)
- 40 completed tasks ready to archive
- 22 tasks marked as completed
- Need to merge duplicates and archive old completed tasks

**Auto-Consolidation:**
The dashboard includes task consolidation analysis that can:
- Identify duplicate tasks by content
- Merge related tasks into parent-child structure
- Archive old completed tasks (move to `tasks/completed/`)
- Clean up task numbering

## BlackBox5 Scribe

### Purpose
Documents all tasks, decisions, and learnings for future reference.

### What It Tracks

- **Task Creation**: Every task created
- **Task Completion**: When agents finish tasks
- **Decisions Made**: Architectural and technical decisions
- **Learnings**: What worked, what didn't
- **Agent Performance**: Which agents perform best

### Knowledge Base Structure

```
/opt/blackbox5/5-project-memory/blackbox5/knowledge/
├── agents/                     # Agent performance and patterns
├── codebase/                # Code architecture and patterns
├── decisions/               # Historical decisions and rationale
└── patterns/                # Reusable patterns and anti-patterns
```

### Daily Summaries

Scribe generates daily summaries including:
- Task Overview (created, completed, in progress)
- Decisions Made
- Learnings from agents
- Agent Performance Metrics
- Next Steps

### Access

**Via BlackBox5 Dashboard:**
- Click on agent card → "View Logs" → See detailed activity
- Monitor stats bar → See overall system performance

## Autonomous Agents

### Currently Running (7 Active)

| Agent | Role | Status | Current Focus |
|--------|------|--------|----------|
| **BlackBox5 Scribe** | Documentation | 🔄 Running | Monitoring task documentation system |
| **Conversational Planner** | Natural Tasks | 🔄 Running | Designing task planning system |
| **Autonomous Improvement** | Self-Improvement | 🔄 Running | Designing 30min cron loops |
| **YouTube Scraper** | YouTube Automation | 🔄 Researching | Building continuous video scraper |
| **Kimi Load Balancer** | API Management | 🔄 Researching | Designing key rotation system |
| **Multi-API Manager** | API Coordination | 🔄 Researching | Integrating Google, Claude, OpenAI |
| **Task Executor** | Task Management | 🔄 Running | Building centralized task queue |
| **Observability** | Monitoring | 🔄 Researching | Building real-time dashboards |

### What They Do

1. **BlackBox5 Scribe**: 
   - Documents all agent activities
   - Creates daily summaries
   - Stores decisions and learnings

2. **Conversational Planner**:
   - Listens to your natural conversation
   - Transforms into structured task plans
   - Creates tasks in BlackBox5 format

3. **Autonomous Improvement**:
   - Runs every 30 minutes (cron-based)
   - Analyzes systems and proposes improvements
   - Spawns sub-agents to implement improvements

4. **YouTube Scraper**:
   - Monitors playlists continuously
   - Scrapes video transcripts
   - Filters and processes transcripts
   - Stores insights in knowledge base

5. **Kimi Load Balancer**:
   - Manages 9 Kimi API keys
   - Rotates keys to avoid rate limits
   - Monitors API usage and costs
   - Distributes compute across tasks

6. **Multi-API Manager**:
   - Coordinates Google, Claude, OpenAI, other free APIs
   - Implements failover strategies
   - Optimizes API selection based on task type

7. **Task Executor**:
   - Centralized task queue system
   - Distributes work to agents
   - Tracks task progress and completion
   - Manages priorities and deadlines

## Getting Started

### For New Users

1. **Access Dashboard**: `http://77.42.66.40:8001/`
2. **View All Agents**: See what's running
3. **Create Task**: Click purple button
4. **Talk to Agent**: Start working with any agent

### Example Workflow

**1. User says:** *"I need to fix YouTube scraper"*
**2. Dashboard:** Shows task created with "youtube-scraper" agent
**3. Agent:** YouTube Scraper picks up task
**4. Execution:** Agent analyzes issue, implements fix
**5. Completion:** Agent reports back, scribe documents

---

**Created:** 2026-02-10
**Skill Version:** 1.0
**Last Updated:** 2026-02-10T20:12:00.000Z
```
