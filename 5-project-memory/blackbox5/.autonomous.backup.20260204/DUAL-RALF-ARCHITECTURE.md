# Dual-RALF Architecture

**Version:** 1.0.0
**Status:** Design Complete, Ready for Implementation
**Last Updated:** 2026-02-01

---

## Overview

Dual-RALF is a parallel agent architecture where two specialized agents collaborate to ship features autonomously:

- **RALF-Planner** (Analyst/Architect Mode): Analyzes codebase, plans tasks, organizes structure
- **RALF-Executor** (Developer Mode): Executes tasks, commits code, reports status

Both agents run simultaneously in the same GitHub Codespace, communicating via shared files.

---

## Core Philosophy

**Planner stays ahead, Executor stays busy.**

- Planner maintains a queue of 3-5 tasks ahead of Executor
- Planner uses idle CPU for codebase analysis and organization
- Executor never waits for tasks
- Both adapt to each other's discoveries in real-time

---

## Communication System

### File-Based Protocol

Located in `.autonomous/communications/`:

| File | Purpose | Written By | Read By | Update Frequency |
|------|---------|------------|---------|------------------|
| `queue.yaml` | Task assignments | Planner | Executor | Every planning cycle |
| `events.yaml` | Execution status | Executor | Planner | Every event |
| `chat-log.yaml` | Rich communication | Both | Both | As needed |
| `heartbeat.yaml` | Health checks | Both | Both | Every 30 seconds |
| `protocol.yaml` | Rules of engagement | Human | Both | Rarely |

### Communication Patterns

**Planner → Executor (via queue.yaml):**
```yaml
queue:
  - id: task-001
    type: implement
    title: "Add auth middleware"
    priority: high
    estimated_minutes: 30
    context_level: 2

metadata:
  last_updated: "2026-02-01T03:00:00Z"
  queue_depth_target: 5
  current_depth: 3
```

**Executor → Planner (via events.yaml):**
```yaml
events:
  - timestamp: "2026-02-01T03:25:00Z"
    task_id: task-001
    type: completed
    result: success
    commit_hash: "abc123"
```

**Bidirectional (via chat-log.yaml):**
```yaml
messages:
  - from: executor
    to: planner
    timestamp: "2026-02-01T03:20:00Z"
    type: question
    content: "Should I use JWT or session tokens?"

  - from: planner
    to: executor
    timestamp: "2026-02-01T03:21:00Z"
    type: answer
    content: "Use JWT. Add TODO to migrate sessions later."
```

---

## Agent Responsibilities

### RALF-Planner

**Primary Functions:**
1. **Task Planning** — Analyze STATE.yaml, plan next 3-5 tasks
2. **Codebase Analysis** — First principles analysis of structure, patterns, tech debt
3. **Organization** — Reorganize files, consolidate duplicates, archive stale content
4. **Pattern Recognition** — Analyze runs, identify recurring issues
5. **Documentation** — Keep docs current, generate from code

**Writes To:**
- `communications/queue.yaml`
- `communications/chat-log.yaml` (answers, warnings)
- `STATE.yaml` (planning section, next_action)
- `knowledge/analysis/`

**Reads From:**
- `communications/events.yaml`
- `communications/chat-log.yaml` (questions)
- `communications/heartbeat.yaml`
- `STATE.yaml`

**Loop:** Every 30 seconds

### RALF-Executor

**Primary Functions:**
1. **Task Execution** — Pull from queue, execute tasks
2. **Git Operations** — Commit changes safely
3. **Status Reporting** — Write events, ask questions
4. **State Updates** — Mark tasks complete in STATE.yaml

**Writes To:**
- `communications/events.yaml`
- `communications/chat-log.yaml` (questions, discoveries)
- `communications/heartbeat.yaml`
- `STATE.yaml` (execution section, completed tasks)
- `runs/executor/`

**Reads From:**
- `communications/queue.yaml`
- `communications/chat-log.yaml` (answers)
- `communications/protocol.yaml`

**Loop:** Every 30 seconds

---

## Directory Structure

```
.autonomous/
├── communications/          # Shared communication files
│   ├── queue.yaml          # Task queue (Planner → Executor)
│   ├── events.yaml         # Execution events (Executor → Planner)
│   ├── chat-log.yaml       # Bidirectional chat
│   ├── heartbeat.yaml      # Health checks
│   └── protocol.yaml       # Rules and configuration
│
├── runs/                   # Unified runtime directory
│   ├── planner/            # Planner run logs
│   │   ├── run-0001/
│   │   │   ├── THOUGHTS.md
│   │   │   ├── RESULTS.md
│   │   │   ├── DECISIONS.md
│   │   │   └── metadata.yaml   # Loop tracking (agent, timestamps, actions)
│   │   └── ...
│   ├── executor/           # Executor run logs
│   │   ├── run-0001/
│   │   │   ├── THOUGHTS.md
│   │   │   ├── RESULTS.md
│   │   │   ├── DECISIONS.md
│   │   │   └── metadata.yaml   # Loop tracking (agent, timestamps, actions)
│   │   └── ...
│   ├── timeline/           # Shared chronological timeline
│   │   └── YYYY-MM-DD.md   # All agent activity for the day
│   └── assets/             # Shared research and analysis
│       └── research-[topic]-[timestamp].md
│
├── planner/                # Planner agent scripts
│   ├── ralf-planner.sh     # Main loop script
│   └── skills/             # Planner-specific skills
│       ├── codebase-analysis.sh
│       ├── pattern-recognition.sh
│       ├── task-generation.sh
│       └── reorganization-planning.sh
│
├── executor/               # Executor agent scripts
│   ├── ralf-executor.sh    # Main loop script
│   └── skills/             # Execution skills
│
├── shared/                 # Common resources
│   ├── skills/             # Shared skills (git-commit, state-management)
│   └── STATE.yaml          # Ground truth (read/write both)
│
└── DUAL-RALF-ARCHITECTURE.md  # This file
```

---

## How Agents Help Each Other

### Planner Helps Executor

| Scenario | Mechanism | Result |
|----------|-----------|--------|
| Discovers tech debt | Chat: "Warning: module X is fragile" | Executor knows to be careful |
| Queue running low | Plans next 3 tasks immediately | Executor never waits idle |
| Analyzes patterns | Updates queue with optimized approach | Executor works more efficiently |
| Reorganizes codebase | Queues reorganization task | Executor executes, benefits from cleaner structure |

### Executor Helps Planner

| Scenario | Mechanism | Result |
|----------|-----------|--------|
| Hits unexpected issue | Event: "failed: import error" + Chat question | Planner pauses queue, fixes plan |
| Discovers better approach | Chat: "Found simpler way: use Z" | Planner updates future tasks |
| Reports real timing | Events show actual vs estimated | Planner improves estimates |
| Asks clarifying question | Chat question reveals plan gap | Planner improves future plans |

---

## Self-Healing Behaviors

| Situation | Response |
|-----------|----------|
| Planner crashes | Executor drains queue, pauses, attempts restart |
| Executor crashes | Planner pauses queue addition, attempts restart |
| Queue empty > 5 min | Planner emergency planning mode (analyze current state) |
| Executor blocked > 10 min | Planner becomes Executor (mode switch) |
| Both disagree on STATE.yaml | Protocol rules: Planner wins planning, Executor wins execution |
| File corruption | Atomic writes (temp + rename), backup and restore |

---

## Scaling Considerations

### Current Design: 2 Agents (Planner + Executor)

**Assumptions:**
- Single codebase
- Single git repo
- Shared filesystem
- Sequential task execution (one Executor)

### Future Scaling: Multiple Executors

If we add Executor-2, Executor-3:

**Option A: Shared Queue (Load Balancing)**
```
Planner ──► queue.yaml ──┬──► Executor-1
                         ├──► Executor-2
                         └──► Executor-3
```
- All Executors pull from same queue
- First to claim executes
- Simple, but no specialization

**Option B: Partitioned Queues (Specialization)**
```
Planner ──► queue-frontend.yaml ──► Executor-Frontend
       ──► queue-backend.yaml  ──► Executor-Backend
       ──► queue-devops.yaml   ──► Executor-DevOps
```
- Planner routes by task type
- Executors specialize
- More efficient, more complex

**Option C: Hierarchical (Teams)**
```
Master Planner
    ├── Team A Planner ──► Executor A1, A2
    ├── Team B Planner ──► Executor B1, B2
    └── Team C Planner ──► Executor C1, C2
```
- Master coordinates teams
- Each team has sub-Planner
- Scales to large codebases

**Communication Scaling:**

| Agents | queue.yaml | events.yaml | chat-log.yaml | Solution |
|--------|-----------|-------------|---------------|----------|
| 2 | Single file | Single file | Single file | Current design |
| 3-5 | Single file | Per-executor | Shared | Add executor ID to events |
| 5-10 | Partitioned | Per-executor | Per-team | Sharded queues |
| 10+ | Database (SQLite/Redis) | Database | Database | Move to proper message queue |

**Current Recommendation:**
- Stay with file-based for 2 agents
- Move to SQLite at 3-5 agents
- Move to Redis at 10+ agents

---

## Implementation Checklist

### Phase 1: Foundation
- [ ] Create `.autonomous/communications/` directory
- [ ] Create `protocol.yaml` with rules
- [ ] Implement atomic file write utilities

### Phase 2: Planner
- [ ] Create `ralf-planner.sh` main loop
- [ ] Implement queue.yaml writer
- [ ] Implement events.yaml reader
- [ ] Implement chat-log.yaml reader/writer
- [ ] Implement heartbeat writer

### Phase 3: Executor
- [ ] Refactor current ralf-loop.sh to `ralf-executor.sh`
- [ ] Implement queue.yaml reader
- [ ] Implement events.yaml writer
- [ ] Implement chat-log.yaml reader/writer
- [ ] Implement heartbeat writer

### Phase 4: Integration
- [ ] Test Planner fills queue
- [ ] Test Executor drains queue
- [ ] Test both running simultaneously
- [ ] Measure throughput vs single agent

### Phase 5: Hardening
- [ ] Implement self-healing behaviors
- [ ] Add monitoring/alerting
- [ ] First principles review after 10 runs

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Queue wait time | < 30 seconds | Time task waits before execution |
| Planner idle time | < 10% | Time with < 2 tasks queued |
| Failure recovery | < 2 minutes | Time from failure to re-plan |
| State consistency | 100% | No STATE.yaml conflicts |
| Throughput improvement | +30% | Tasks/hour vs single RALF |
| Context efficiency | Improved | Less context switching per task |

---

## Key Design Decisions

1. **File-based communication** — Simple, no dependencies, debuggable
2. **Separate run directories** — Planner and Executor each have their own THOUGHTS.md
3. **Shared STATE.yaml** — Single ground truth, atomic updates
4. **Planner stays ahead** — 3-5 task queue depth target
5. **Bidirectional chat** — Rich communication for questions and discoveries
6. **Self-healing** — Agents detect and recover from failures

---

## References

- `LEGACY.md` — Executor agent specification
- `CLAUDE.md` — High-level guidance
- `goals.yaml` — Agent improvement goals
- `communications/protocol.yaml` — Detailed protocol rules

---

**Next Action:** Implement Phase 1 (Foundation)

**Owner:** Legacy autonomous system
**Review Cycle:** Every 10 runs or monthly
