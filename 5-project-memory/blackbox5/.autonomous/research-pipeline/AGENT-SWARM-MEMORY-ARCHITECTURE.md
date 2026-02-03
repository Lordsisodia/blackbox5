# Agent Swarm Memory Architecture

**Purpose:** Unified memory system for managing 6+ agents in the Dual-RALF Research Pipeline
**Based on:** BB5 Planner/Executor memory frameworks + Multi-Agent Ralph patterns
**Approach:** Hierarchical memory with swarm coordination

---

## Current BB5 Memory Framework (What We're Building On)

### 1. Planner/Executor Memory System

```
┌─────────────────────────────────────────────────────────────┐
│                 BB5 AGENT MEMORY HIERARCHY                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  LAYER 1: RUN MEMORY (Per-Run Isolation)                    │
│  ┌─────────────────────────────────────┐                    │
│  │ runs/run-XXXX/                      │                    │
│  │ ├── THOUGHTS.md    - Reasoning     │                    │
│  │ ├── DECISIONS.md   - Decisions     │                    │
│  │ ├── RESULTS.md     - Outcomes      │                    │
│  │ └── metadata.yaml  - Structured    │                    │
│  └─────────────────────────────────────┘                    │
│                                                              │
│  LAYER 2: LOOP MEMORY (Cross-Run Aggregation)               │
│  ┌─────────────────────────────────────┐                    │
│  │ loop-XXXX-metadata.yaml             │                    │
│  │ ├── Loop number & timestamps       │                    │
│  │ ├── State (tasks, queue depth)     │                    │
│  │ ├── Actions taken                  │                    │
│  │ ├── Discoveries                    │                    │
│  │ └── Next steps                     │                    │
│  └─────────────────────────────────────┘                    │
│                                                              │
│  LAYER 3: COMMUNICATION (Inter-Agent)                       │
│  ┌─────────────────────────────────────┐                    │
│  │ communications/                     │                    │
│  │ ├── heartbeat.yaml - Health status │                    │
│  │ ├── events.yaml    - Event bus     │                    │
│  │ ├── queue.yaml     - Task queue    │                    │
│  │ └── chat-log.yaml  - Messages      │                    │
│  └─────────────────────────────────────┘                    │
│                                                              │
│  LAYER 4: DAILY MEMORY (Temporal Aggregation)               │
│  ┌─────────────────────────────────────┐                    │
│  │ 2026-02-01.md - Daily summary      │                    │
│  │ ├── Loop summaries                 │                    │
│  │ ├── Key decisions                  │                    │
│  │ └── System state                   │                    │
│  └─────────────────────────────────────┘                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2. Key BB5 Memory Patterns

**Pattern 1: Four-File Run Structure**
- `THOUGHTS.md` - Cognitive process (reasoning, analysis)
- `DECISIONS.md` - Decision records (options, rationale)
- `RESULTS.md` - Outcomes (data, metrics, findings)
- `metadata.yaml` - Machine-readable state

**Pattern 2: Loop Metadata Aggregation**
- Tracks state ACROSS runs
- Maintains queue depth
- Records discoveries
- Links related runs

**Pattern 3: Heartbeat Health System**
- Real-time agent status
- Last seen timestamps
- Current action tracking
- Loop/run number sync

**Pattern 4: Event-Driven Communication**
- Append-only event log
- Event types with schemas
- Publisher/subscriber pattern
- Replay capability

---

## Agent Swarm Memory Architecture

### Design Principles

1. **Hierarchical Memory** - From individual runs to swarm coordination
2. **Event-Driven** - Loose coupling via event bus
3. **Heartbeat Health** - Real-time swarm visibility
4. **Dual Memory** - Running (short-term) + Timeline (long-term)
5. **Shared State** - Centralized coordination files

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AGENT SWARM MEMORY ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SWARM COORDINATION LAYER (Global)                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ swarm/                                                              │   │
│  │ ├── heartbeat.yaml       - All agent health (6+ agents)            │   │
│  │ ├── events.yaml          - Swarm-wide event bus                    │   │
│  │ ├── state.yaml           - Shared state machine                    │   │
│  │ ├── queue.yaml           - Cross-pipeline work queue               │   │
│  │ ├── handoffs.yaml        - Agent-to-agent transfers                │   │
│  │ └── ledger.md            - Chronological swarm history             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  PIPELINE COORDINATION LAYER (Per-Pipeline)                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ communications/                                                     │   │
│  │ ├── scout-state.yaml     - Scout pair coordination                 │   │
│  │ ├── analyst-state.yaml   - Analyst pair coordination               │   │
│  │ ├── planner-state.yaml   - Planner pair coordination               │   │
│  │ ├── chat-log.yaml        - Worker-validator feedback               │   │
│  │ └── pipeline-metrics.yaml - Aggregate statistics                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  AGENT MEMORY LAYER (Per-Agent)                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ agents/{agent}/                                                     │   │
│  │ ├── timeline-memory.md   - Long-term chronological memory          │   │
│  │ ├── running-memory.md    - Current session state                   │   │
│  │ ├── runs/                - Run directories (THOUGHTS, RESULTS...)  │   │
│  │ ├── memory/              - Learning & strategy                     │   │
│  │ └── metrics/             - Performance tracking                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  DATA LAYER (Shared)                                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ data/                                                               │   │
│  │ ├── patterns/            - Extracted patterns (scout output)       │   │
│  │ ├── analysis/            - Pattern analysis (analyst output)       │   │
│  │ └── recommendations/     - Approved recommendations                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Swarm Coordination Layer (NEW)

### swarm/heartbeat.yaml

Global health monitoring for all 6+ agents:

```yaml
swarm_heartbeat:
  version: "1.0.0"
  timestamp: "2026-02-04T10:00:00Z"
  active_agents: 6
  healthy_agents: 6

agents:
  scout-worker:
    status: healthy        # healthy, warning, critical, idle
    last_seen: "2026-02-04T10:00:00Z"
    current_work: "github.com/user/repo"
    run_id: "run-20260204-001"
    loop_number: 45
    tokens_used_session: 45000
    work_completed_today: 12

  scout-validator:
    status: healthy
    last_seen: "2026-02-04T10:00:00Z"
    monitoring: "scout-worker-run-20260204-001"
    validations_today: 12
    feedback_given_today: 8

  analyst-worker:
    status: healthy
    last_seen: "2026-02-04T09:55:00Z"
    current_work: "P-001"
    run_id: "run-20260204-003"
    analyses_completed_today: 8

  analyst-validator:
    status: healthy
    last_seen: "2026-02-04T09:55:00Z"
    monitoring: "analyst-worker-run-20260204-003"
    validations_today: 8

  planner-worker:
    status: healthy
    last_seen: "2026-02-04T09:50:00Z"
    current_work: "P-001"
    run_id: "run-20260204-005"
    tasks_created_today: 5

  planner-validator:
    status: idle
    last_seen: "2026-02-04T09:50:00Z"
    monitoring: null
    validations_today: 5

swarm_metrics:
  total_patterns_extracted: 45
  total_patterns_analyzed: 38
  total_tasks_created: 12
  pipeline_bottleneck: null   # scout|analyst|planner|null
  queue_health: healthy       # healthy, warning, critical
```

### swarm/events.yaml

Swarm-wide event bus for cross-pipeline coordination:

```yaml
swarm_events:
  version: "1.0.0"
  event_count: 1245

events:
  - timestamp: "2026-02-04T10:00:00Z"
    event_type: pattern.extracted
    source_agent: scout-worker
    data:
      pattern_id: "P-045"
      source: "github.com/user/repo"
      confidence: 0.92
    routing:
      notify: [analyst-worker]  # Who should process this
      priority: high

  - timestamp: "2026-02-04T09:58:00Z"
    event_type: analysis.complete
    source_agent: analyst-worker
    data:
      pattern_id: "P-044"
      decision: recommend
      score: 8.5
    routing:
      notify: [planner-worker]
      priority: high

  - timestamp: "2026-02-04T09:55:00Z"
    event_type: task.created
    source_agent: planner-worker
    data:
      task_id: "TASK-RAPS-012"
      pattern_id: "P-042"
      estimated_hours: 7
    routing:
      notify: [bb5-system]
      priority: medium

  - timestamp: "2026-02-04T09:50:00Z"
    event_type: swarm.rebalance
    source_agent: swarm-orchestrator
    data:
      action: scale_up_analyst
      reason: "scout output exceeding analyst capacity"
    routing:
      notify: [all]
      priority: critical
```

### swarm/state.yaml

Shared state machine for swarm coordination:

```yaml
swarm_state:
  version: "1.0.0"
  timestamp: "2026-02-04T10:00:00Z"

pipeline_state:
  scout_phase:
    status: active           # active, paused, complete
    queue_depth: 12          # sources waiting
    processing_rate: 4.5     # sources/hour
    bottleneck: false

  analyst_phase:
    status: active
    queue_depth: 8           # patterns waiting
    processing_rate: 3.2     # patterns/hour
    bottleneck: true         # Flagged as bottleneck

  planner_phase:
    status: active
    queue_depth: 3           # recommendations waiting
    processing_rate: 2.1     # tasks/hour
    bottleneck: false

work_routing:
  # Automatic work distribution
  scout_output:
    target: analyst-worker
    distribution: round_robin  # round_robin, load_balanced, priority

  analyst_output:
    target: planner-worker
    distribution: priority

resource_allocation:
  # Token budget allocation across agents
  scout-worker:
    budget_per_run: 3000
    runs_per_hour: 6
  scout-validator:
    budget_per_run: 1000
    runs_per_hour: 6
  analyst-worker:
    budget_per_run: 4800
    runs_per_hour: 4
  analyst-validator:
    budget_per_run: 1200
    runs_per_hour: 4
  planner-worker:
    budget_per_run: 3600
    runs_per_hour: 3
  planner-validator:
    budget_per_run: 600
    runs_per_hour: 3
```

### swarm/ledger.md

Chronological history of all swarm activity:

```markdown
# Swarm Ledger

## 2026-02-04

### 10:00 UTC - Pattern Extraction Surge
- Scout-worker extracted 3 patterns from github.com/user/auth-repo
- Patterns: P-043, P-044, P-045
- Queue depth now at 12 (warning threshold)
- Action: Auto-scaling analyst-worker runs

### 09:55 UTC - Analysis Bottleneck Detected
- Analyst phase processing rate: 3.2/hour
- Scout phase output rate: 4.5/hour
- Bottleneck: analyst-worker capacity
- Action: Increased analyst-worker token budget +20%

### 09:50 UTC - Task Created
- Planner-worker created TASK-RAPS-012
- Pattern: P-042 (authentication middleware)
- Estimated: 7 hours
- Added to BB5 queue

## 2026-02-03

### 23:45 UTC - Daily Summary
- Patterns extracted: 45
- Patterns analyzed: 38
- Tasks created: 12
- Success rate: 94%
- Bottleneck: None
```

---

## Pipeline Coordination Layer

### communications/pipeline-metrics.yaml

Aggregate statistics across all pairs:

```yaml
pipeline_metrics:
  version: "1.0.0"
  timestamp: "2026-02-04T10:00:00Z"

scout_pair:
  worker:
    runs_today: 12
    patterns_extracted: 45
    avg_patterns_per_run: 3.75
    token_efficiency: 0.85
    success_rate: 0.94
  validator:
    validations_today: 12
    feedback_given: 28
    feedback_implementation_rate: 0.82
  coordination_health: 0.91  # 0-1 scale

analyst_pair:
  worker:
    runs_today: 8
    patterns_analyzed: 38
    avg_time_per_analysis: 12min
    recommendation_rate: 0.73
    token_efficiency: 0.78
  validator:
    validations_today: 8
    scoring_accuracy: 0.88
    model_calibrations: 3
  coordination_health: 0.89

planner_pair:
  worker:
    runs_today: 5
    tasks_created: 12
    avg_subtasks_per_task: 3.2
    estimation_accuracy: 0.85
  validator:
    validations_today: 5
    plan_quality_score: 0.91
    strategy_adjustments: 2
  coordination_health: 0.93

end_to_end_metrics:
  sources_to_tasks_rate: 0.27  # 12 tasks / 45 sources
  avg_pipeline_time: 45min     # source -> task
  bottleneck_phase: analyst    # scout|analyst|planner
```

---

## Agent Memory Layer Integration

Each agent's memory now includes swarm context:

### agents/{agent}/timeline-memory.md (Enhanced)

```yaml
timeline_memory:
  version: "1.0.0"
  agent: scout-worker
  # ... existing fields ...

  # NEW: Swarm context
  swarm_context:
    swarm_role: worker                    # worker|validator
    pipeline_phase: scout                 # scout|analyst|planner
    pair_agent: scout-validator           # Who to coordinate with
    upstream_agents: []                   # Who feeds me work
    downstream_agents: [analyst-worker]   # Who I feed work to

  # NEW: Work routing
  work_routing:
    input_source: swarm_queue             # Where work comes from
    output_target: data/patterns/         # Where output goes
    event_trigger: pattern.extracted      # Event to publish

  # NEW: Resource tracking
  resource_usage:
    tokens_used_session: 45000
    tokens_budget_daily: 100000
    runs_completed_today: 12
    avg_run_duration: 8min
```

---

## SessionStart Hook Integration

The SessionStart hook now injects THREE layers of memory:

```bash
session-start-swarm-memory.sh
```

### Injected Context Structure

```markdown
## Layer 1: Swarm Context (Global)
- Swarm health status
- Pipeline bottleneck info
- Resource allocation
- Work routing rules

## Layer 2: Pipeline Context (Phase)
- Pair coordination state
- Phase metrics
- Queue depths
- Coordination health

## Layer 3: Agent Context (Individual)
- Timeline memory
- Work assignment
- Personal metrics
- Learning history
```

---

## Swarm Orchestrator (NEW COMPONENT)

### Purpose
Monitors swarm health and makes coordination decisions:

```yaml
swarm_orchestrator:
  responsibilities:
    - Detect bottlenecks
    - Rebalance work allocation
    - Scale agent resources
    - Handle agent failures
    - Optimize token budgets

  decisions:
    - scale_up_worker: Increase runs/hour
    - scale_up_validator: Add validation capacity
    - rebalance_work: Redistribute queue
    - alert_operator: Human intervention needed
```

### Example Orchestrator Logic

```python
if scout_output_rate > analyst_processing_rate * 1.5:
    # Bottleneck detected
    trigger_event("swarm.rebalance", {
        "action": "scale_up_analyst",
        "reason": "scout output exceeding analyst capacity",
        "scout_rate": scout_output_rate,
        "analyst_rate": analyst_processing_rate
    })
```

---

## Migration from Current System

### Phase 1: Add Swarm Layer (Immediate)
1. Create `swarm/` directory
2. Implement heartbeat.yaml
3. Add swarm events
4. Create ledger

### Phase 2: Enhance Agents (Week 1)
1. Add swarm_context to timeline-memory.md
2. Update SessionStart hook
3. Implement work routing
4. Add resource tracking

### Phase 3: Orchestrator (Week 2)
1. Build swarm orchestrator
2. Implement bottleneck detection
3. Add auto-scaling logic
4. Create operator alerts

### Phase 4: Optimization (Ongoing)
1. Tune token budgets
2. Optimize routing rules
3. Refine coordination
4. Add predictive scaling

---

## Key Benefits

1. **Visibility** - Real-time swarm health monitoring
2. **Coordination** - Automatic bottleneck detection & resolution
3. **Scalability** - Easy to add more agents to any phase
4. **Resilience** - Handle agent failures gracefully
5. **Optimization** - Data-driven resource allocation
6. **Transparency** - Complete audit trail in ledger

---

## Files to Create

```
research-pipeline/
├── swarm/
│   ├── heartbeat.yaml          # Global agent health
│   ├── events.yaml             # Swarm-wide events
│   ├── state.yaml              # Shared state machine
│   ├── queue.yaml              # Cross-pipeline queue
│   ├── ledger.md               # Chronological history
│   └── orchestrator-rules.yaml # Auto-scaling rules
├── communications/
│   └── pipeline-metrics.yaml   # Aggregate statistics
└── .claude/hooks/
    └── session-start-swarm.sh  # Enhanced hook
```
