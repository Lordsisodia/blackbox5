# BB5 Existing RALF Infrastructure Analysis

## Overview

BlackBox5 (BB5) has a sophisticated, multi-layered autonomous execution framework called RALF (Recursive Autonomous Learning Framework). The system is designed for continuous self-improvement through autonomous task execution, agent teams, and structured communication protocols.

**Current Version:** Agent-2.5 (The Simplification Release)
**Core Philosophy:** One task per loop, high signal/low noise, integration-first
**Deployment Status:** Partially deployed to VPS with systemd service

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BB5 RALF Architecture                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        RALF Executor Layer                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │   ralf-core  │  │   ralf-docs  │  │    ralf-research         │  │   │
│  │  │   .sh        │  │   .sh        │  │    .sh                   │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  │  ┌──────────────┐  ┌─────────────────────────────────────────────┐ │   │
│  │  │  ralf-maint  │  │  ralf-core-with-agent-teams.sh              │ │   │
│  │  │   .sh        │  │  (Multi-agent orchestration)                │ │   │
│  │  └──────────────┘  └─────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Agent Spawner Layer                              │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐ │   │
│  │  │ bb5-context-    │  │ bb5-superintel- │  │    bb5-scribe       │ │   │
│  │  │   collector     │  │   ligence       │  │                     │ │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘ │   │
│  │  ┌─────────────────┐  ┌─────────────────┐                          │   │
│  │  │   bb5-planner   │  │  bb5-verifier   │                          │   │
│  │  └─────────────────┘  └─────────────────┘                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Communication Layer                               │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │   │
│  │  │ queue.yaml  │  │ events.yaml │  │heartbeat.yml│  │chat-log.yml│ │   │
│  │  │ (planner    │  │ (executor   │  │ (bidirect.) │  │ (both)     │ │   │
│  │  │  writes)    │  │  writes)    │  │             │  │            │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │              protocol.yaml (Dual-RALF spec)                  │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Task Management Layer                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │    Task      │  │    Task      │  │       task_scanner       │  │   │
│  │  │   Scanner    │  │   Queue      │  │         .py              │  │   │
│  │  │              │  │              │  │  (Priority scoring)      │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │   executor   │  │  agent-      │  │    Spawn Queue           │  │   │
│  │  │    .py       │  │  spawner.py  │  │    (agent activation)    │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Supporting Tools Layer                          │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │ralf-thought│ │ralf-check│ │ralf-task │ │ralf-verify│ │ralf-dashboard│ │   │
│  │  │          │ │  -docs   │ │  -init   │ │  -run    │ │          │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### RALF Executor

**Location:** `/Users/shaansisodia/.blackbox5/bin/ralf-executor/`

| File | Purpose |
|------|---------|
| `ralf-core.sh` | Main autonomous execution loop for VPS deployment. Handles task discovery, execution via Claude Code, git operations, and status tracking. |
| `ralf-executor.sh` | Unified service wrapper that integrates task scanner, executor engine, and agent spawner. Runs as continuous service. |
| `executor.py` | Python-based task execution engine with full lifecycle management: acquire → lock → execute → verify → complete. |
| `task_scanner.py` | Scans task directories, parses task.md files, calculates priority scores using (impact/effort) * confidence formula. |
| `agent-spawner.py` | Spawns BB5 Core Agent Team members (context-collector, planner, verifier, scribe, executor) using Task tool. |
| `ralf-wrapper.sh` | Privilege-dropping wrapper for systemd (runs as bb5-runner user) |
| `bb5-ralf-executor.service` | systemd service definition for VPS deployment |

**Key Features:**
- Task status flow: `pending → claimed → in_progress → [completed | partial | failed]`
- Priority scoring based on impact/effort ratio
- Automatic run documentation (THOUGHTS.md, DECISIONS.md, LEARNINGS.md, RESULTS.md, CHANGES.md)
- Git integration with auto-commit and push to vps branch
- Completion signal detection (`<promise>COMPLETE</promise>`)
- Dry-run mode for testing

### RALF Loops

**Location:** `/Users/shaansisodia/.blackbox5/bin/ralf-loops/`

| Loop | Purpose | Trigger |
|------|---------|---------|
| `ralf-core.sh` | Engine improvement (2-engine/) | Continuous (10s interval) |
| `ralf-docs.sh` | Documentation maintenance (1-docs/) | Continuous (10s interval) |
| `ralf-maint.sh` | System health & hygiene | Continuous (10s interval) |
| `ralf-research.sh` | External technology research | Continuous (10s interval) |
| `ralf-core-with-agent-teams.sh` | Multi-agent orchestration | On-demand |
| `ralf-core-single-cycle.sh` | Single execution for Moltbot | Per-cycle |

**Loop Structure:**
1. Pull latest from GitHub
2. Check for pending tasks in queue
3. Create run folder with documentation templates
4. Execute via Claude Code with prompt
5. Check for completion signal
6. Commit and push changes
7. Brief pause, repeat

### RALF Tools

**Location:** `/Users/shaansisodia/.blackbox5/bin/ralf-tools/`

| Tool | Purpose |
|------|---------|
| `ralf-thought` | Append thought to THOUGHTS.md |
| `ralf-check-docs` | Validate all documentation files filled |
| `ralf-task-init.sh` | Initialize task working directory |
| `ralf-verify-run.sh` | Verify run completion |
| `ralf-dashboard` | View system status |
| `ralf-build-prompt.sh` | Build execution prompts |
| `ralf-keepalive` / `ralf-keepalive-http` | Keep services alive |
| `ralf-branch` | Branch management |
| `ralf-improve` | Trigger improvement cycles |

### Agent System

**Agent Definitions:** `/Users/shaansisodia/.blackbox5/.claude/agents/`

| Agent | Model | Timeout | Purpose |
|-------|-------|---------|---------|
| `bb5-context-collector` | claude-opus-4-6 | 10 min | Gather comprehensive BB5 state |
| `bb5-planner` | claude-opus-4-6 | 15 min | Create implementation plans |
| `bb5-verifier` | claude-opus-4-6 | 10 min | Validate task completion |
| `bb5-scribe` | claude-opus-4-6 | 5 min | Document thinking, decisions, learnings |
| `bb5-executor` | claude-opus-4-6 | 30 min | Execute tasks and implement solutions |

**Agent Spawner Capabilities:**
- Spawn agents with context-aware prompts
- Track agent status (pending → running → completed/failed/timeout)
- Retry failed agents with context preservation
- Wait for completion with polling
- Generate execution summaries

### Task Management

**Task Structure:**
```
5-project-memory/blackbox5/.autonomous/tasks/
├── active/
│   └── [TASK-DIR]/
│       ├── task.md              # Task definition
│       ├── subtasks/            # Subtask definitions
│       └── runs.migrated/       # Run history
├── completed/
│   └── [TASK-DIR]/
└── working/                     # Active execution contexts
```

**Task File Format:**
```markdown
# TASK-XXX: Title

**Status:** pending|in_progress|completed
**Priority:** CRITICAL|HIGH|MEDIUM|LOW
**Type:** architecture|process|skill|infrastructure|documentation|development
**Created:** ISO timestamp

## Description
Task description...

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Dependencies
- TASK-XXX-001
```

**Priority Scoring Formula:**
```
score = (impact / effort) * confidence
impact = (business_value * 0.4) + (technical_debt * 0.35) + (unblock_factor * 0.25)
```

### Communication Queue

**Location:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/`

**Files:**
| File | Written By | Read By | Purpose |
|------|------------|---------|---------|
| `queue.yaml` | Planner | Executor | Task queue with priorities |
| `events.yaml` | Executor | Planner | Status updates, discoveries |
| `chat-log.yaml` | Both | Both | Q&A between agents |
| `heartbeat.yaml` | Both | Both | Liveness checks |
| `protocol.yaml` | - | - | Communication specification |
| `spawn-queue.yaml` | System | Agents | Agent activation queue |

**Dual-RALF Protocol:**
- Max 2 agents (current), scalable to 10+
- File-based communication (YAML)
- Atomic writes with validation
- Conflict resolution rules
- Scaling roadmap: file → SQLite → Redis

---

## Current Capabilities

### What Works Well Today

1. **Task Lifecycle Management**
   - Comprehensive task parsing and priority scoring
   - Status tracking through full workflow
   - Automatic documentation generation
   - Git integration with branch management

2. **Agent Team Framework**
   - Well-defined agent roles and responsibilities
   - Context collector for state gathering
   - Superintelligence agent for complex decisions
   - Scribe for automatic documentation

3. **Communication Infrastructure**
   - Structured file-based protocol
   - Clear separation of concerns (planner vs executor)
   - Event-driven updates
   - Heartbeat monitoring

4. **Multi-Loop Architecture**
   - Specialized loops for different domains (core, docs, maint, research)
   - Each loop can run independently
   - Shared queue system

5. **Execution Engine**
   - Python-based executor with proper error handling
   - Dry-run mode for testing
   - Context gathering before execution
   - Completion verification

6. **VPS Deployment**
   - systemd service configuration
   - Privilege dropping (runs as bb5-runner)
   - Log rotation and monitoring
   - Auto-restart on failure

### Strengths

- **Integration-First:** Code must work with existing system
- **Documentation-Heavy:** Every run produces THOUGHTS, DECISIONS, LEARNINGS, RESULTS
- **Git-Native:** All changes tracked, committed, and pushed
- **Modular:** Components can be used independently
- **Rule-Based:** 20+ auto-activation rules for different scenarios
- **Self-Improving:** Designed to improve itself recursively

---

## Current Limitations

### What's Missing or Could Be Improved

1. **Agent Spawner Simulation**
   - Currently simulates Task tool with file-based markers
   - Does not actually spawn sub-agents via Claude Code API
   - Relies on external completion signals

2. **Queue Scalability**
   - File-based YAML has race condition risks
   - No transaction support
   - Planned migration to SQLite for 3-5 agents, Redis for 10+

3. **Limited Error Recovery**
   - Retry logic is basic (fixed count)
   - No exponential backoff
   - Limited circuit breaker patterns

4. **No Centralized Logging**
   - Logs scattered across run folders
   - No unified log aggregation
   - Hard to trace across multiple loops

5. **Missing Monitoring/Alerting**
   - No metrics collection
   - No alerting on failures
   - No dashboard for system health

6. **Task Dependency Resolution**
   - Dependencies tracked but not enforced
   - No automatic dependency ordering
   - No DAG visualization

7. **Resource Management**
   - No CPU/memory limits per task
   - No resource type enforcement (cpu_bound, io_bound, etc.)
   - Parallel groups defined but not utilized

8. **Context Budget Enforcement**
   - Tracking exists but not enforced
   - No automatic context compression
   - Manual threshold checking

9. **No Web Interface**
   - Everything is CLI/file-based
   - No visualization of task queue
   - No run history browser

10. **Testing Gap**
    - Limited test coverage
    - No integration tests for full loop
    - No mock AI provider for testing

---

## Integration Points

### Where External Frameworks Could Plug In

1. **Task Queue Interface**
   - Standardized task.md format
   - YAML queue format with schema
   - Priority scoring formula

2. **Agent Spawner API**
   - Agent configuration schema
   - Spawn/Wait/Retry interface
   - Result handling callbacks

3. **Communication Protocol**
   - File-based YAML protocol
   - Event types and schemas
   - Heartbeat mechanism

4. **Run Documentation Format**
   - Standard THOUGHTS.md, DECISIONS.md, etc. format
   - Template system
   - Validation tools

5. **Skill Integration**
   - Skill selection YAML
   - Auto-activation rules
   - Confidence scoring

6. **Git Integration**
   - Commit message format
   - Branch naming conventions
   - Push/pull workflow

### External Framework Compatibility

| Framework | Integration Path | Notes |
|-----------|-----------------|-------|
| frankbria/ralph-claude-code | Replace ralf-core.sh | Similar loop structure |
| snarktank/ralph | Agent spawner | Could enhance agent spawning |
| michaelshimeles/ralphy | Task management | Could improve task queue |
| mikeyobrien/ralph-orchestrator | Orchestration | Could replace agent-teams.sh |

---

## VPS Deployment Status

### What's Deployed

- **Service:** `bb5-ralf-executor.service` configured
- **User:** `bb5-runner` (non-root for Claude Code)
- **Wrapper:** `ralf-wrapper.sh` for privilege dropping
- **Environment:** ANTHROPIC_API_KEY, BB5_MODE=autonomous
- **Logging:** `/var/log/bb5-ralf-executor.log`

### What's Not Deployed

- **Multi-loop setup:** Only core executor deployed, not separate docs/maint/research loops
- **Agent teams:** Agent spawner not fully integrated in VPS deployment
- **Monitoring:** No health checks or metrics
- **Auto-update:** No automatic code updates from git

### Deployment Commands

```bash
# Install service
sudo cp bb5-ralf-executor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bb5-ralf-executor
sudo systemctl start bb5-ralf-executor

# Check status
sudo systemctl status bb5-ralf-executor
sudo journalctl -u bb5-ralf-executor -f
```

---

## Recommendations for Enhancement

### High Priority

1. **Implement True Agent Spawning**
   - Integrate with Claude Code Task tool API
   - Replace file-based simulation with actual sub-agent spawning
   - Add agent result aggregation

2. **Add SQLite Queue Backend**
   - Replace file-based queue with SQLite
   - Add transaction support
   - Implement proper locking

3. **Create Unified Dashboard**
   - Web-based UI for task queue
   - Run history browser
   - System health metrics
   - Real-time log viewing

4. **Enhance Error Recovery**
   - Exponential backoff for retries
   - Circuit breaker pattern
   - Dead letter queue for failed tasks

### Medium Priority

5. **Add Metrics Collection**
   - Task completion rates
   - Average execution time
   - Success/failure ratios
   - Agent performance metrics

6. **Implement Dependency DAG**
   - Visualize task dependencies
   - Automatic topological sorting
   - Parallel execution of independent tasks

7. **Add Context Compression**
   - Automatic summarization at 70% threshold
   - Key point extraction
   - Archive old context

8. **Create Testing Framework**
   - Mock AI provider
   - Integration tests
   - Task simulation

### Low Priority

9. **Add Redis Backend Option**
   - For 10+ agent scaling
   - Pub/sub for real-time communication
   - Distributed deployment support

10. **Implement Resource Scheduling**
    - CPU/memory limits per task
    - Resource type enforcement
    - Parallel group execution

11. **Add Alerting System**
    - Slack/email notifications
    - Failure alerts
    - Queue depth warnings

12. **Create Plugin System**
    - Allow custom agent types
    - Plugin registry
    - Third-party integrations

---

## File Locations Summary

```
/Users/shaansisodia/.blackbox5/
├── bin/ralf-executor/           # Core executor engine
├── bin/ralf-loops/              # Loop scripts and prompts
├── bin/ralf-tools/              # Utility scripts
├── .claude/agents/              # Agent definitions
├── 5-project-memory/blackbox5/
│   └── .autonomous/
│       ├── agents/communications/  # Queue, events, protocol
│       ├── runs/                 # Execution history
│       └── tasks/                # Task definitions
└── 6-roadmap/_research/external/GitHub/Ralph-Frameworks/
    └── bb5-existing-infrastructure.md  # This file
```

---

## Conclusion

BB5 has a mature, well-architected RALF infrastructure with strong foundations in task management, agent teams, and communication protocols. The system is production-ready for single-executor deployment but has clear scaling limitations that are documented and have planned solutions.

The main gaps are:
1. True sub-agent spawning (currently simulated)
2. Queue backend scalability (file → SQLite → Redis roadmap exists)
3. Monitoring and observability
4. Testing infrastructure

The integration points are well-defined, making it feasible to incorporate improvements from other RALF frameworks or external tools.
