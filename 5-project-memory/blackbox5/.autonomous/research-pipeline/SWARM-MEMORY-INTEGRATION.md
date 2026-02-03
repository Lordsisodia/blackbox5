# Swarm Memory System Integration

**Purpose:** How the BB5 memory frameworks integrate with the Dual-RALF Research Pipeline
**Architecture:** Three-layer memory with swarm coordination
**Status:** Ready for deployment

---

## Memory Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MEMORY HIERARCHY                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LAYER 1: SWARM MEMORY (Global Coordination)                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ swarm/                                                              │   │
│  │ ├── heartbeat.yaml    - All 6 agents' health                       │   │
│  │ ├── events.yaml       - Swarm-wide event bus                       │   │
│  │ ├── state.yaml        - Pipeline state machine                     │   │
│  │ └── ledger.md         - Chronological history                      │   │
│  │                                                                   │   │
│  │ Based on: BB5 heartbeat.yaml + Multi-Agent Ralph event bus         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  LAYER 2: PIPELINE MEMORY (Phase Coordination)                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ communications/                                                     │   │
│  │ ├── scout-state.yaml    - Scout pair coordination                  │   │
│  │ ├── analyst-state.yaml  - Analyst pair coordination                │   │
│  │ ├── planner-state.yaml  - Planner pair coordination                │   │
│  │ ├── chat-log.yaml       - Worker-validator feedback                │   │
│  │ └── pipeline-metrics.yaml - Aggregate statistics                   │   │
│  │                                                                   │   │
│  │ Based on: BB5 communications/ + Research Pipeline state files      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  LAYER 3: AGENT MEMORY (Individual Context)                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ agents/{agent}/                                                     │   │
│  │ ├── timeline-memory.md  - Long-term chronological (NEW)            │   │
│  │ ├── running-memory.md   - Current session state                    │   │
│  │ ├── runs/               - Run directories (THOUGHTS, RESULTS...)   │   │
│  │ └── memory/             - Learning & strategy                      │   │
│  │                                                                   │   │
│  │ Based on: BB5 runs/ structure + Dual memory (running + timeline)   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  INJECTION: SessionStart Hook                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ .claude/hooks/session-start-swarm.sh                                │   │
│  │                                                                   │   │
│  │ Injects ALL THREE LAYERS into agent context at session start       │   │
│  │ Based on: BB5 session-start-ledger.sh pattern                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Framework Integration Matrix

| Component | BB5 Source | Research Pipeline | Integration |
|-----------|------------|-------------------|-------------|
| **Run Memory** | `runs/run-XXXX/{THOUGHTS,RESULTS,DECISIONS}.md` | `agents/{agent}/runs/` | ✅ Direct use |
| **Loop Metadata** | `loop-XXXX-metadata.yaml` | Agent timeline-memory.md | ✅ Enhanced with swarm context |
| **Heartbeat** | `communications/heartbeat.yaml` | `swarm/heartbeat.yaml` | ✅ Extended for 6 agents |
| **Event Bus** | `communications/events.yaml` | `swarm/events.yaml` + pipeline events | ✅ Hierarchical events |
| **State Tracking** | Agent-specific state | `swarm/state.yaml` | ✅ Global state machine |
| **SessionStart Hook** | `session-start-ledger.sh` | `session-start-swarm.sh` | ✅ Three-layer injection |
| **Daily Summary** | `2026-02-01.md` | `swarm/ledger.md` | ✅ Continuous ledger |
| **Chat/Feedback** | `chat-log.yaml` | `communications/chat-log.yaml` | ✅ Direct use |

---

## SessionStart Hook: Three-Layer Injection

### What Gets Injected

```markdown
## Layer 1: Swarm Context (Global Coordination)

### Swarm Health Status
```yaml
swarm_heartbeat:
  active_agents: 6
  healthy_agents: 6
  agents:
    scout-worker:
      status: healthy
      current_work: "github.com/user/repo"
    analyst-worker:
      status: bottleneck  # ⚠️ This agent needs attention
```

### Pipeline State
```yaml
pipeline_state:
  scout_phase:
    status: active
    queue_depth: 12
  analyst_phase:
    status: bottleneck  # ⚠️ Processing slower than input
    queue_depth: 8
```

## Layer 2: Pipeline Context (Phase Coordination)

### scout Phase State
```yaml
worker_status: "scanning"
current_source: "github.com/user/repo"
queue_depth: 12
```

### Recent Events
```yaml
events:
  - event_type: pattern.extracted
    pattern_id: "P-045"
    routing:
      notify: [analyst-worker]  # ← This is for you!
```

## Layer 3: Agent Context (Individual Memory)

### Timeline Memory (Long-Term)
```yaml
history:
  - run_id: "run-20260204-001"
    source: "github.com/repo1"
    patterns_extracted: 3

work_queue:
  priority_sources: ["github.com/repo2"]
  in_progress: null
```

### Work Assignment Instructions
**Your Role:** Extract patterns from external sources
**Work Flow:**
1. Check timeline-memory.md work_queue.priority_sources
2. If empty, check swarm/events.yaml
...
```

---

## Swarm Coordination Features

### 1. Bottleneck Detection

**Automatic detection based on:**
- Input rate vs output rate ratio
- Queue depth thresholds
- Processing rate trends

**Example from `swarm/state.yaml`:**
```yaml
pipeline_state:
  analyst_phase:
    status: bottleneck
    queue_depth: 8
    processing_rate: 3.2  # patterns/hour
    output_rate: 2.1      # recommendations/hour
```

**Action triggered:**
```yaml
events:
  - event_type: swarm.rebalance
    data:
      action: scale_up_analyst
      reason: "scout output (4.5/hr) exceeding analyst capacity (3.2/hr)"
```

### 2. Work Routing

**Automatic distribution based on:**
- Agent health status
- Current workload
- Priority rules

**Example from `swarm/state.yaml`:**
```yaml
work_routing:
  scout_output:
    target: analyst-worker
    distribution: priority  # Route by pattern confidence
    priority_field: confidence
```

### 3. Resource Allocation

**Token budget management:**
```yaml
resource_allocation:
  scout-worker:
    budget_per_run: 3000
    max_runs_per_hour: 6
    current_runs_this_hour: 4
```

**Auto-scaling when near limits:**
- Scale up at 80% capacity
- Scale down at 30% capacity
- Max 2x scaling factor

### 4. Health Monitoring

**From `swarm/heartbeat.yaml`:**
```yaml
agents:
  scout-worker:
    status: healthy
    last_seen: "2026-02-04T10:00:00Z"
    tokens_used_session: 45000
    work_completed_today: 12
```

**Automatic alerts:**
- Warning: 30 minutes idle
- Critical: 60 minutes idle
- Critical: 3 consecutive failures

---

## Agent Swarm vs BB5 Planner/Executor

### Similarities (What We Kept)

| Feature | BB5 | Agent Swarm |
|---------|-----|-------------|
| Run isolation | `runs/run-XXXX/` | `agents/{agent}/runs/` |
| Four-file structure | THOUGHTS, RESULTS, DECISIONS, metadata | Same pattern |
| Heartbeat health | Per-agent status | Extended to 6 agents |
| Event bus | `events.yaml` | Hierarchical: swarm + pipeline |
| SessionStart injection | Ledger loading | Three-layer injection |
| Chat/Feedback | `chat-log.yaml` | Direct use |

### Enhancements (What's New)

| Feature | BB5 | Agent Swarm | Why |
|---------|-----|-------------|-----|
| **Memory layers** | 2 (run + loop) | 3 (swarm + pipeline + agent) | Coordination at scale |
| **Timeline memory** | Loop metadata | Per-agent timeline-memory.md | Long-term learning |
| **Swarm orchestration** | None | `swarm/state.yaml` with rules | Auto-scaling |
| **Bottleneck detection** | Manual | Automatic with thresholds | Self-healing |
| **Work routing** | Direct assignment | Event-driven routing | Loose coupling |
| **Resource tracking** | Per-loop | Per-session + daily | Budget management |
| **Pair coordination** | N/A | Worker-validator pairs | Quality assurance |
| **Pipeline phases** | Single | Scout → Analyst → Planner | Specialization |

---

## Usage Examples

### Example 1: Scout Worker First Run

```bash
# 1. RALF loop starts
# 2. SessionStart hook triggers
# 3. Hook injects three-layer context
```

**Agent sees:**
```markdown
## Layer 1: Swarm Context
All agents idle, queues empty

## Layer 2: Pipeline Context
scout phase: idle, queue_depth: 0

## Layer 3: Agent Context
work_queue:
  priority_sources: []  # Empty!
```

**Decision:** Check `swarm/events.yaml` for `source.added` events

### Example 2: Bottleneck Detection

```yaml
# swarm/state.yaml
pipeline_state:
  analyst_phase:
    status: bottleneck
    processing_rate: 3.2
    queue_depth: 15
```

**Orchestrator action:**
```yaml
# swarm/events.yaml
events:
  - event_type: swarm.rebalance
    data:
      action: scale_up_analyst
      new_budget: 5760  # +20%
```

**Analyst-worker sees in injected context:**
```markdown
## Swarm Context
⚠️ BOTTLENECK DETECTED: analyst phase
Action: Token budget increased +20%
```

### Example 3: Cross-Agent Work Routing

```yaml
# Scout worker publishes:
events:
  - event_type: pattern.extracted
    data:
      pattern_id: "P-001"
    routing:
      notify: [analyst-worker]
```

**Analyst-worker sees in injected context:**
```markdown
## Recent Events
- pattern.extracted: P-001 (waiting for analysis)
- Your queue: 1 pattern waiting
```

**Analyst-worker's decision:**
1. Check `work_queue.priority_patterns` → empty
2. Check `swarm/events.yaml` → found P-001
3. Load `data/patterns/P-001.yaml`
4. Begin analysis

---

## Files Reference

### Swarm Layer (Global)

| File | Purpose | Updated By |
|------|---------|------------|
| `swarm/heartbeat.yaml` | Agent health status | All agents |
| `swarm/events.yaml` | Swarm-wide event bus | All agents |
| `swarm/state.yaml` | Pipeline state machine | Orchestrator |
| `swarm/ledger.md` | Chronological history | All agents |

### Pipeline Layer (Phase)

| File | Purpose | Updated By |
|------|---------|------------|
| `communications/scout-state.yaml` | Scout pair state | Scout agents |
| `communications/analyst-state.yaml` | Analyst pair state | Analyst agents |
| `communications/planner-state.yaml` | Planner pair state | Planner agents |
| `communications/chat-log.yaml` | Worker-validator feedback | Validators |
| `communications/events.yaml` | Pipeline events | All agents |

### Agent Layer (Individual)

| File | Purpose | Updated By |
|------|---------|------------|
| `agents/{agent}/timeline-memory.md` | Long-term memory | Agent itself |
| `agents/{agent}/running-memory.md` | Session state | Agent itself |
| `agents/{agent}/runs/run-XXXX/` | Run isolation | Agent itself |
| `agents/{agent}/memory/` | Learning & strategy | Agent itself |

### Data Layer (Shared)

| File | Purpose | Updated By |
|------|---------|------------|
| `data/patterns/{id}.yaml` | Extracted patterns | Scout-worker |
| `data/analysis/{id}.yaml` | Pattern analysis | Analyst-worker |
| `communications/queue.yaml` | BB5 task queue | Planner-worker |

---

## Migration Path

### Phase 1: Deploy Swarm Layer (Immediate)
- ✅ Create `swarm/` directory with 4 files
- ✅ Deploy `session-start-swarm.sh` hook
- ✅ Test hook injection

### Phase 2: Update Agent Timelines (Week 1)
- Add `swarm_context` section to all timeline-memory.md files
- Update work assignment logic
- Test work routing

### Phase 3: Enable Orchestration (Week 2)
- Implement bottleneck detection
- Add auto-scaling rules
- Create operator alerts

### Phase 4: Optimize (Ongoing)
- Tune token budgets based on data
- Refine routing rules
- Add predictive scaling

---

## Key Benefits Over BB5

1. **Scale:** Handles 6+ agents vs 2 (planner + executor)
2. **Specialization:** Pipeline phases (scout → analyst → planner)
3. **Quality:** Worker-validator pairs with feedback loops
4. **Self-Healing:** Automatic bottleneck detection & resolution
5. **Visibility:** Real-time swarm health monitoring
6. **Coordination:** Event-driven work routing
7. **Learning:** Per-agent timeline memory with skill progression

---

## Next Steps

1. **Install the hook:**
   ```bash
   # Add to ~/.claude/settings.json
   {
     "hooks": {
       "SessionStart": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "$HOME/.blackbox5/5-project-memory/blackbox5/.autonomous/research-pipeline/.claude/hooks/session-start-swarm.sh"
             }
           ]
         }
       ]
     }
   }
   ```

2. **Start the agents:**
   ```bash
   ./launch-all.sh
   ```

3. **Monitor the swarm:**
   ```bash
   cat swarm/heartbeat.yaml
   cat swarm/state.yaml
   ```

4. **View the ledger:**
   ```bash
   cat swarm/ledger.md
   ```
