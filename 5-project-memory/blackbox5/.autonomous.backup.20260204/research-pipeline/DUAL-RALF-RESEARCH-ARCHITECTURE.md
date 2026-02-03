# Dual-RALF Research Pipeline Architecture

**Version:** 1.0.0
**Status:** Design Complete
**Last Updated:** 2026-02-04

---

## Overview

Dual-RALF Research Pipeline is a 6-agent parallel architecture where specialized worker-validator pairs collaborate to discover, analyze, and plan implementation of patterns from external sources.

**Worker-Validator Pairs:**
- **Scout Pair:** Discovers and extracts patterns from GitHub/YouTube/docs
- **Analyst Pair:** Ranks patterns by value/complexity for BB5 integration
- **Planner Pair:** Creates BB5 tasks from approved recommendations

All 6 agents run simultaneously in the same project space, communicating via shared files in project memory.

---

## Core Philosophy

**"Workers execute, validators elevate."**

- Workers focus on doing the work
- Validators focus on learning, logging, and improving worker strategies
- Both read/write to shared project memory
- Agents can self-modify their context and long-term memory mid-run

---

## Directory Structure

```
5-project-memory/blackbox5/
└── .autonomous/
    └── research-pipeline/           # NEW: Research Pipeline System
        ├── README.md                # This documentation
        ├── DUAL-RALF-RESEARCH-ARCHITECTURE.md  # This file
        ├── agents/
        │   ├── scout-worker/        # Scout extraction agent
        │   │   ├── state/           # Current operational state
        │   │   ├── metrics/         # Performance metrics
        │   │   ├── memory/          # Long-term memory (self-modifiable)
        │   │   │   ├── patterns-learned.md
        │   │   │   ├── extraction-strategies.md
        │   │   │   └── source-history.yaml
        │   │   └── runs/            # Historical runs
        │   │       └── run-XXXX/
        │   │           ├── THOUGHTS.md
        │   │           ├── RESULTS.md
        │   │           ├── DECISIONS.md
        │   │           ├── ASSUMPTIONS.md
        │   │           ├── LEARNINGS.md
        │   │           └── metadata.yaml
        │   │
        │   ├── scout-validator/     # Scout validation & learning agent
        │   │   ├── state/
        │   │   ├── metrics/
        │   │   ├── memory/          # Long-term memory (self-modifiable)
        │   │   │   ├── worker-patterns.md
        │   │   │   ├── quality-metrics.md
        │   │   │   └── improvement-suggestions.yaml
        │   │   └── runs/
        │   │
        │   ├── analyst-worker/      # Analyst ranking agent
        │   │   ├── state/
        │   │   ├── metrics/
        │   │   ├── memory/          # Long-term memory (self-modifiable)
        │   │   │   ├── scoring-models.md
        │   │   │   ├── value-patterns.md
        │   │   │   └── complexity-history.yaml
        │   │   └── runs/
        │   │
        │   ├── analyst-validator/   # Analyst validation & learning agent
        │   │   ├── state/
        │   │   ├── metrics/
        │   │   ├── memory/          # Long-term memory (self-modifiable)
        │   │   │   ├── ranking-accuracy.md
        │   │   │   ├── feedback-loop.md
        │   │   │   └── model-improvements.yaml
        │   │   └── runs/
        │   │
        │   ├── planner-worker/      # Planner task creation agent
        │   │   ├── state/
        │   │   ├── metrics/
        │   │   ├── memory/          # Long-term memory (self-modifiable)
        │   │   │   ├── task-templates.md
        │   │   │   ├── estimation-models.md
        │   │   │   └── dependency-patterns.yaml
        │   │   └── runs/
        │   │
        │   └── planner-validator/   # Planner validation & learning agent
        │       ├── state/
        │       ├── metrics/
        │       ├── memory/          # Long-term memory (self-modifiable)
        │       │   ├── plan-quality.md
        │       │   ├── success-patterns.md
        │       │   └── strategy-evolution.yaml
        │       └── runs/
        │
        ├── communications/          # Shared coordination files
        │   ├── queue.yaml           # Task queue (Planner -> BB5 Executor)
        │   ├── events.yaml          # Pipeline events (all agents)
        │   ├── chat-log.yaml        # Bidirectional chat (all agents)
        │   ├── heartbeat.yaml       # Health checks (all agents)
        │   ├── protocol.yaml        # Rules of engagement
        │   ├── scout-state.yaml     # Scout phase state
        │   ├── analyst-state.yaml   # Analyst phase state
        │   ├── planner-state.yaml   # Planner phase state
        │   └── pipeline-state.yaml  # Overall pipeline state
        │
        ├── context/                 # Shared context
        │   ├── routes.yaml          # Path configurations
        │   ├── sources.yaml         # Source configurations (GitHub, YouTube)
        │   └── patterns-index.yaml  # Index of discovered patterns
        │
        ├── data/                    # Shared data
        │   ├── patterns/            # Extracted pattern storage
        │   ├── analysis/            # Analysis results
        │   └── tasks/               # Planned tasks
        │
        ├── logs/                    # Centralized logging
        │   ├── scout/
        │   ├── analyst/
        │   ├── planner/
        │   └── pipeline/
        │
        └── operations/              # Operational data
            ├── skill-usage.yaml
            └── token-usage.yaml
```

---

## Communication System

### File-Based Protocol

Located in `.autonomous/research-pipeline/communications/`:

| File | Purpose | Written By | Read By | Update Frequency |
|------|---------|------------|---------|------------------|
| `queue.yaml` | Task assignments | Planner Worker | BB5 Executor | On task creation |
| `events.yaml` | Pipeline events | All Agents | All Agents | Every event |
| `chat-log.yaml` | Rich communication | All Agents | All Agents | As needed |
| `heartbeat.yaml` | Health checks | All Agents | All Agents | Every 30 seconds |
| `protocol.yaml` | Rules of engagement | Human | All Agents | Rarely |
| `scout-state.yaml` | Scout phase state | Scout Worker/Validator | Scout Pair | Every iteration |
| `analyst-state.yaml` | Analyst phase state | Analyst Worker/Validator | Analyst Pair | Every iteration |
| `planner-state.yaml` | Planner phase state | Planner Worker/Validator | Planner Pair | Every iteration |
| `pipeline-state.yaml` | Overall state | All Agents | All Agents | Every iteration |

### Communication Patterns

#### Worker -> Validator (via shared memory/)

**Scout Worker writes:**
```yaml
# scout-worker/runs/run-001/THOUGHTS.md
## Current Extraction
Source: github.com/user/auth-system
Progress: 3/10 files analyzed
Patterns found: 2 (JWT middleware, Role decorator)
Tokens used: 1,200 / 3,000 (40%)
```

**Scout Validator reads and responds:**
```yaml
# scout-validator/memory/improvement-suggestions.yaml
suggestions_for_worker:
  - run_id: "run-001"
    timestamp: "2026-02-04T12:00:00Z"
    observation: "Worker focused on middleware, missed auth decorators"
    suggestion: "Check auth/decorators.py for @require_role pattern"
    based_on: "Previous 5 similar repos all had decorator patterns"
```

#### Phase-to-Phase (via events.yaml)

**Scout Worker publishes:**
```yaml
# communications/events.yaml
- timestamp: "2026-02-04T12:05:00Z"
  event_type: pattern.extracted
  source: scout-worker
  data:
    pattern_id: "P-001"
    source_url: "github.com/user/auth-system"
    confidence: 0.92
    concepts: ["JWT", "middleware", "authentication"]
```

**Analyst Worker subscribes and processes:**
- Reads event from events.yaml
- Claims pattern for analysis
- Publishes analysis:complete event

#### Bidirectional Chat (via chat-log.yaml)

```yaml
# communications/chat-log.yaml
messages:
  - from: scout-worker
    to: scout-validator
    timestamp: "2026-02-04T12:03:00Z"
    type: question
    content: "Should I extract test files or just production code?"

  - from: scout-validator
    to: scout-worker
    timestamp: "2026-02-04T12:04:00Z"
    type: answer
    content: "Extract both. Tests reveal usage patterns. Focus on test_auth.py for examples."

  - from: analyst-worker
    to: planner-worker
    timestamp: "2026-02-04T12:30:00Z"
    type: discovery
    content: "High-value pattern found: JWT refresh token rotation. Complexity: medium."

  - from: planner-validator
    to: planner-worker
    timestamp: "2026-02-04T12:35:00Z"
    type: context
    content: "Similar pattern implemented in TASK-176. Reuse that task structure."
```

---

## Agent Responsibilities

### Scout Worker

**Primary Functions:**
1. **Source Discovery** — Find repos, videos, docs to analyze
2. **Pattern Extraction** — Use Claude to extract core concepts, code, hooks
3. **Concept Mapping** — Identify relationships between concepts
4. **Storage** — Save structured data to data/patterns/

**Writes To:**
- `scout-worker/runs/*/THOUGHTS.md` (reasoning)
- `scout-worker/runs/*/RESULTS.md` (outcomes)
- `scout-worker/runs/*/DECISIONS.md` (decisions)
- `scout-worker/memory/` (self-modifiable long-term memory)
- `communications/events.yaml` (pattern:extracted events)
- `communications/scout-state.yaml` (current state)
- `data/patterns/` (extracted pattern storage)

**Reads From:**
- `communications/events.yaml` (new source events)
- `communications/chat-log.yaml` (validator feedback)
- `scout-validator/memory/` (improvement suggestions)
- `context/sources.yaml` (source configurations)

**Loop:** Every 10 minutes (configurable)

**Token Target:** 3,000 per run (40% of 7,500 context)

---

### Scout Validator

**Primary Functions:**
1. **Monitor** — Watch Scout Worker output in real-time
2. **Log** — Record all worker decisions and reasoning
3. **Learn** — Detect patterns in worker behavior
4. **Suggest** — Offer improvements to extraction strategy
5. **Plan** — Help worker plan next iterations

**Writes To:**
- `scout-validator/runs/*/THOUGHTS.md` (observations)
- `scout-validator/runs/*/RESULTS.md` (quality metrics)
- `scout-validator/memory/` (self-modifiable learning)
- `communications/chat-log.yaml` (feedback to worker)
- `communications/scout-state.yaml` (validation state)

**Reads From:**
- `scout-worker/runs/*/THOUGHTS.md` (worker reasoning)
- `scout-worker/runs/*/RESULTS.md` (worker outcomes)
- `scout-worker/runs/*/DECISIONS.md` (worker decisions)
- `communications/events.yaml` (all pipeline events)

**Loop:** Every 10 minutes (parallel to worker)

**Token Target:** 1,000 per run (40% of 2,500 context)

---

### Analyst Worker

**Primary Functions:**
1. **Pattern Analysis** — Read Scout output, analyze value to BB5
2. **Complexity Scoring** — Calculate integration + maintenance cost
3. **Value Assessment** — Determine benefit to BB5 ecosystem
4. **Ranking** — Score by value/(cost) ratio
5. **Decision** — Recommend, defer, or reject

**Writes To:**
- `analyst-worker/runs/*/THOUGHTS.md`
- `analyst-worker/runs/*/RESULTS.md`
- `analyst-worker/runs/*/DECISIONS.md`
- `analyst-worker/memory/` (self-modifiable scoring models)
- `communications/events.yaml` (analysis:complete events)
- `communications/analyst-state.yaml`
- `data/analysis/` (analysis results)

**Reads From:**
- `communications/events.yaml` (pattern:extracted events)
- `data/patterns/` (extracted patterns)
- `analyst-validator/memory/` (model improvement suggestions)
- `communications/chat-log.yaml`

**Loop:** Every 15 minutes (or on pattern:extracted event)

**Token Target:** 4,800 per run (40% of 12,000 context)

---

### Analyst Validator

**Primary Functions:**
1. **Monitor** — Watch Analyst Worker scoring and decisions
2. **Validate** — Check if analysis covers all important factors
3. **Learn** — Track ranking accuracy over time
4. **Improve** — Suggest scoring model adjustments
5. **Feedback Loop** — Incorporate Executor results into models

**Writes To:**
- `analyst-validator/runs/*/THOUGHTS.md`
- `analyst-validator/runs/*/RESULTS.md`
- `analyst-validator/memory/` (self-modifiable models)
- `communications/chat-log.yaml`
- `communications/analyst-state.yaml`

**Reads From:**
- `analyst-worker/runs/*/` (all worker output)
- `communications/events.yaml`
- `data/analysis/` (analysis results)

**Loop:** Every 15 minutes (parallel to worker)

**Token Target:** 1,200 per run (40% of 3,000 context)

---

### Planner Worker

**Primary Functions:**
1. **Task Decomposition** — Break recommendations into subtasks
2. **Estimation** — Estimate effort, complexity, risk
3. **Dependency Mapping** — Identify task relationships
4. **BB5 Integration** — Create proper BB5 task structures
5. **Queue Management** — Add tasks to communications/queue.yaml

**Writes To:**
- `planner-worker/runs/*/THOUGHTS.md`
- `planner-worker/runs/*/RESULTS.md`
- `planner-worker/runs/*/DECISIONS.md`
- `planner-worker/memory/` (self-modifiable templates)
- `communications/queue.yaml` (BB5 task queue)
- `communications/events.yaml` (tasks:new events)
- `communications/planner-state.yaml`
- `data/tasks/` (planned tasks)

**Reads From:**
- `communications/events.yaml` (analysis:complete events)
- `data/analysis/` (approved recommendations)
- `planner-validator/memory/` (template suggestions)
- `communications/chat-log.yaml`

**Loop:** On demand (triggered by approved recommendations)

**Token Target:** 3,600 per run (40% of 9,000 context)

---

### Planner Validator

**Primary Functions:**
1. **Monitor** — Watch Planner Worker task creation
2. **Validate** — Check task breakdown quality
3. **Learn** — Track which plans succeed/fail
4. **Improve** — Suggest better estimation models
5. **Strategy Evolution** — Refine planning approach based on outcomes

**Writes To:**
- `planner-validator/runs/*/THOUGHTS.md`
- `planner-validator/runs/*/RESULTS.md`
- `planner-validator/memory/` (self-modifiable strategies)
- `communications/chat-log.yaml`
- `communications/planner-state.yaml`

**Reads From:**
- `planner-worker/runs/*/` (all worker output)
- `communications/queue.yaml` (created tasks)
- `communications/events.yaml` (tasks:complete events for feedback)

**Loop:** On demand (parallel to worker)

**Token Target:** 600 per run (40% of 1,500 context)

---

## YAML Frontmatter Formats

### queue.yaml (Task Queue for BB5)

```yaml
queue:
  - task_id: TASK-RAPS-001
    pattern_id: P-001
    source: "github.com/user/auth-system"
    title: "Implement JWT Refresh Token Rotation"
    priority: high
    priority_score: 8.5
    estimated_hours: 6
    estimated_complexity: medium
    value_score: 9.0
    status: pending  # pending, in_progress, completed, failed
    created_at: "2026-02-04T12:30:00Z"
    planned_by: planner-worker-run-001
    notes: |
      Detailed implementation notes from planner

metadata:
  last_updated: "2026-02-04T12:35:00Z"
  updated_by: planner-worker
  queue_depth_target: 3-5
  current_depth: 2
  last_completed: null
  notes: |
    Pipeline state notes
```

### events.yaml (Pipeline Events)

```yaml
events:
  - timestamp: "2026-02-04T12:00:00Z"
    event_type: source.discovered
    agent: scout-worker
    run_id: scout-001
    data:
      source_url: "github.com/user/auth-system"
      source_type: github

  - timestamp: "2026-02-04T12:05:00Z"
    event_type: pattern.extracted
    agent: scout-worker
    run_id: scout-001
    data:
      pattern_id: "P-001"
      pattern_name: "JWT Refresh Token Rotation"
      confidence: 0.92
      concepts: ["JWT", "refresh-token", "rotation", "security"]

  - timestamp: "2026-02-04T12:30:00Z"
    event_type: analysis.complete
    agent: analyst-worker
    run_id: analyst-001
    data:
      pattern_id: "P-001"
      decision: recommend
      value_score: 9.0
      complexity_score: 6.0
      total_score: 8.5

  - timestamp: "2026-02-04T12:35:00Z"
    event_type: tasks.new
    agent: planner-worker
    run_id: planner-001
    data:
      task_id: "TASK-RAPS-001"
      pattern_id: "P-001"
      subtasks_count: 4

metadata:
  last_updated: "2026-02-04T12:35:00Z"
  event_count: 4
```

### heartbeat.yaml (Health Checks)

```yaml
heartbeats:
  scout-worker:
    last_seen: "2026-02-04T12:40:00Z"
    status: extracting
    current_action: "analyzing auth-system repo"
    run_number: 45
    tokens_used: 1200
    tokens_budget: 3000

  scout-validator:
    last_seen: "2026-02-04T12:40:00Z"
    status: monitoring
    current_action: "reviewing scout-worker run-045"
    run_number: 45

  analyst-worker:
    last_seen: "2026-02-04T12:35:00Z"
    status: idle
    current_action: waiting_for_patterns
    run_number: 23

  analyst-validator:
    last_seen: "2026-02-04T12:35:00Z"
    status: monitoring
    current_action: reviewing analyst models
    run_number: 23

  planner-worker:
    last_seen: "2026-02-04T12:35:00Z"
    status: planning
    current_action: "creating TASK-RAPS-001"
    run_number: 8

  planner-validator:
    last_seen: "2026-02-04T12:35:00Z"
    status: monitoring
    current_action: reviewing task breakdown
    run_number: 8

metadata:
  timeout_seconds: 120
  last_updated: "2026-02-04T12:40:00Z"
  healthy_agents: 6
  warning_agents: 0
  failed_agents: 0
```

### metadata.yaml (Run Metadata)

```yaml
run:
  id: "scout-001"
  agent: scout-worker
  agent_type: worker
  pair: scout
  phase: extraction
  timestamp_start: "2026-02-04T12:00:00Z"
  timestamp_end: "2026-02-04T12:10:00Z"
  duration_seconds: 600

state:
  source_url: "github.com/user/auth-system"
  files_analyzed: 12
  patterns_found: 3
  concepts_extracted: 8
  status: complete

tokens:
  used: 1200
  budget: 3000
  percentage: 40

results:
  status: success
  patterns:
    - id: "P-001"
      name: "JWT Refresh Token Rotation"
      confidence: 0.92
    - id: "P-002"
      name: "Role-Based Access Control"
      confidence: 0.88
    - id: "P-003"
      name: "Auth Middleware Pattern"
      confidence: 0.85

next_steps:
  - "Publish pattern:extracted events"
  - "Update scout-state.yaml"
  - "Sleep until next iteration"

notes: |
  Free-form notes for future runs
```

---

## Protocol Rules

### Worker Must:
- Maintain token usage below 40% of context limit
- Write THOUGHTS.md, RESULTS.md, DECISIONS.md every run
- Update heartbeat.yaml every 30 seconds
- Publish events to events.yaml
- Read validator feedback from chat-log.yaml
- Self-modify memory/ files to improve over time

### Worker Must Not:
- Write to validator run directories
- Modify other worker's state
- Exceed token budget (hard stop at 60%)

### Validator Must:
- Monitor worker output in real-time
- Write feedback to chat-log.yaml
- Log all observations to memory/
- Suggest improvements based on patterns
- Update heartbeat.yaml every 30 seconds

### Validator Must Not:
- Execute work (only validate)
- Write to worker run directories
- Modify queue.yaml (workers only)

### All Agents Must:
- Respect protocol.yaml rules
- Maintain heartbeat every 30 seconds
- Use YAML frontmatter for all structured data
- Store all run data in project memory (not engine)
- Self-modify context/memory to improve

---

## Token Budget Summary

| Agent | Target/Run | Context Limit | Frequency | Daily Budget |
|-------|-----------|---------------|-----------|--------------|
| Scout Worker | 3,000 | 7,500 (40%) | Every 10 min | 432K |
| Scout Validator | 1,000 | 2,500 (40%) | Every 10 min | 144K |
| Analyst Worker | 4,800 | 12,000 (40%) | Every 15 min | 460K |
| Analyst Validator | 1,200 | 3,000 (40%) | Every 15 min | 115K |
| Planner Worker | 3,600 | 9,000 (40%) | On demand | 36K |
| Planner Validator | 600 | 1,500 (40%) | On demand | 6K |
| **TOTAL** | | | | **~1.2M** |

With 100M daily budget, this leaves 98.8M for retries, spikes, and growth.

---

## How Agents Self-Modify

Agents can modify their own long-term memory mid-run:

```yaml
# scout-worker/memory/extraction-strategies.md
strategies:
  - name: "auth-pattern-extraction"
    developed: "2026-02-04"
    effectiveness: 0.94
    steps:
      1: "Check for JWT libraries in requirements"
      2: "Look for auth/ directory"
      3: "Extract middleware patterns"
      4: "Extract decorator patterns"
    notes: |
      This strategy developed after analyzing 50+ auth repos.
      Most effective when combined with test file analysis.
```

The agent can update this file during a run:
```
"I just discovered that checking tests/ first reveals usage patterns
before diving into implementation. Adding this as step 0."
→ Updates extraction-strategies.md mid-run
```

---

## Files Referenced

- `agents/scout-worker/runs/*/THOUGHTS.md`
- `agents/scout-worker/runs/*/RESULTS.md`
- `agents/scout-worker/runs/*/DECISIONS.md`
- `agents/scout-worker/runs/*/metadata.yaml`
- `agents/scout-worker/memory/*.md`
- `communications/queue.yaml`
- `communications/events.yaml`
- `communications/chat-log.yaml`
- `communications/heartbeat.yaml`
- `communications/protocol.yaml`
