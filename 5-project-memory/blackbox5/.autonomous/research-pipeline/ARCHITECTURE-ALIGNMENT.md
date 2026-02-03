# Architecture Alignment: Research Pipeline ↔ BB5

**Purpose:** Verify swarm memory system fits with existing BB5 architecture
**Status:** ✅ Aligned with minor integration points
**Date:** 2026-02-04

---

## Current BB5 Architecture (Existing)

```
.autonomous/
├── agents/
│   ├── planner/                    # BB5 Planner Agent
│   │   ├── 2026-02-01.md          # Daily summary
│   │   ├── loop-metadata-template.yaml
│   │   ├── metrics/               # Performance metrics
│   │   ├── runs/                  # Run directories
│   │   │   ├── loop-0045-metadata.yaml  # Loop aggregation
│   │   │   ├── loop-0046-metadata.yaml
│   │   │   ├── run-0001/          # Individual run
│   │   │   │   ├── THOUGHTS.md
│   │   │   │   ├── RESULTS.md
│   │   │   │   └── DECISIONS.md
│   │   │   ├── run-0002/
│   │   │   └── ... (89 runs)
│   │   └── state/                 # Agent state
│   │
│   ├── executor/                   # BB5 Executor Agent
│   │   └── runs/                  # Same structure
│   │
│   └── architect/
│       └── runs/archived/
│
├── communications/
│   └── heartbeat.yaml             # Global health
│       # planner + executor only
│
├── memory/
│   └── decisions/
│       └── registry.md
│
└── tasks/
    ├── active/
    └── completed/
```

**Key BB5 Patterns:**
1. **Daily Summary:** `2026-02-01.md` - Aggregated daily activity
2. **Loop Metadata:** `loop-XXXX-metadata.yaml` - Cross-run state
3. **Run Isolation:** `runs/run-XXXX/` - THOUGHTS, RESULTS, DECISIONS
4. **Heartbeat:** `communications/heartbeat.yaml` - Health status
5. **No SessionStart Hook:** BB5 doesn't use hooks for memory injection

---

## Research Pipeline Architecture (New)

```
research-pipeline/
├── .claude/hooks/                  # NEW: Hook-based memory injection
│   ├── session-start-swarm.sh     # Three-layer injection
│   └── session-start-timeline-memory.sh
│
├── .templates/
│   ├── communications/            # Templates for comms
│   ├── prompts/                   # 6 agent prompts
│   └── runs/                      # Run file templates
│
├── agents/                        # 6 agents (not 2 like BB5)
│   ├── scout-worker/
│   │   ├── memory/                # Learning & strategy
│   │   ├── metrics/               # Performance tracking
│   │   ├── runs/                  # Run directories (like BB5)
│   │   ├── state/                 # Agent state
│   │   ├── running-memory.md      # Session state
│   │   └── timeline-memory.md     # Long-term memory (NEW)
│   │
│   ├── scout-validator/           # Validator pair
│   ├── analyst-worker/            # Analysis phase
│   ├── analyst-validator/
│   ├── planner-worker/            # Planning phase
│   └── planner-validator/
│
├── communications/                # Phase coordination
│   # Empty - will be populated from templates
│
├── context/
│   ├── routes.yaml               # Directory routing
│   ├── sources.yaml
│   └── patterns-index.yaml
│
├── data/                         # Shared data
│   ├── analysis/                 # Analyst output
│   ├── patterns/                 # Scout output
│   └── tasks/                    # Planner output
│
├── logs/                         # Log directories
│
├── operations/                   # Tracking
│   ├── skill-usage.yaml
│   └── token-usage.yaml
│
├── swarm/                        # NEW: Global coordination
│   ├── heartbeat.yaml           # 6 agents (vs 2 in BB5)
│   ├── events.yaml              # Swarm-wide events
│   ├── state.yaml               # Pipeline state machine
│   └── ledger.md                # Chronological history
│
└── STATE.yaml                    # Pipeline state
```

---

## Alignment Analysis

### ✅ Perfectly Aligned

| Component | BB5 Pattern | Research Pipeline | Match |
|-----------|-------------|-------------------|-------|
| **Run isolation** | `runs/run-XXXX/` | `agents/{agent}/runs/` | ✅ Same pattern |
| **Four-file structure** | THOUGHTS, RESULTS, DECISIONS | Same + metadata.yaml | ✅ Enhanced |
| **Daily aggregation** | `2026-02-01.md` | `swarm/ledger.md` | ✅ Equivalent |
| **Heartbeat** | `communications/heartbeat.yaml` | `swarm/heartbeat.yaml` | ✅ Extended |
| **State tracking** | `state/` directories | `agents/{agent}/state/` | ✅ Same |
| **Metrics** | `metrics/` directories | `agents/{agent}/metrics/` | ✅ Same |

### 🔧 Integration Points (Minor)

| Component | BB5 | Research Pipeline | Action Needed |
|-----------|-----|-------------------|---------------|
| **Routes** | Hardcoded | `context/routes.yaml` | ✅ Already exists |
| **Agent location** | `.autonomous/agents/` | `.autonomous/research-pipeline/agents/` | ✅ Isolated |
| **Heartbeat scope** | 2 agents | 6 agents | ✅ Separate file |
| **Memory injection** | None (manual) | SessionStart hook | ✅ New capability |

### ⚠️ Potential Conflicts

| Issue | Risk | Mitigation |
|-------|------|------------|
| **Hook collision** | Medium | Use distinct hook script names |
| **Heartbeat confusion** | Low | BB5 uses `communications/heartbeat.yaml`, Research uses `swarm/heartbeat.yaml` |
| **Event bus overlap** | Low | Different event types and scopes |
| **Routes.yaml** | Low | Research pipeline has its own routes file |

---

## Directory Structure Comparison

### BB5 Planner Agent
```
.autonomous/agents/planner/
├── 2026-02-01.md                 # Daily summary
├── loop-metadata-template.yaml   # Loop template
├── metrics/                      # Empty
├── runs/                         # 89 run directories
│   ├── loop-0045-metadata.yaml  # Loop aggregation
│   ├── run-0001/
│   │   ├── THOUGHTS.md
│   │   ├── RESULTS.md
│   │   └── DECISIONS.md
│   └── ...
└── state/                        # Empty
```

### Research Pipeline Scout Worker
```
.autonomous/research-pipeline/agents/scout-worker/
├── memory/                       # Empty (for learning)
├── metrics/                      # Empty (for performance)
├── runs/                         # Empty (will populate)
├── state/                        # Empty (for state)
├── running-memory.md            # Session state (NEW)
└── timeline-memory.md           # Long-term (NEW)
```

**Alignment:**
- ✅ Same directory structure (metrics/, runs/, state/)
- ✅ Same run isolation pattern
- ✅ Enhanced with dual memory (running + timeline)
- ✅ No daily summary file (use swarm/ledger.md instead)

---

## Memory System Comparison

### BB5 Memory (2 Agents)

```yaml
# BB5 Pattern - Loop Metadata
loop:
  number: 46
  timestamp_start: "2026-02-01T12:37:51Z"
  timestamp_end: "2026-02-01T15:50:00Z"

state:
  active_tasks_count: 5
  completed_tasks_count: 100
  executor_status: "healthy"
  queue_depth: 5

actions_taken:
  - type: "research"
    description: "What was done"

discoveries:
  - type: "pattern"
    description: "What was discovered"
    impact: "high"
```

### Research Pipeline Memory (6 Agents)

```yaml
# Timeline Memory - Enhanced with swarm context
timeline_memory:
  version: "1.0.0"
  agent: scout-worker
  total_runs: 0

# NEW: Swarm coordination
swarm_context:
  swarm_role: worker
  pipeline_phase: scout
  pair_agent: scout-validator
  upstream_agents: []
  downstream_agents: [analyst-worker]

# BB5-equivalent: Loop metadata → History
history: []

# BB5-equivalent: State tracking
work_queue:
  priority_sources: []
  in_progress: null

# BB5-equivalent: Discoveries → Learning
skill_progression:
  extraction_accuracy: 0.0
  common_mistakes: []
```

**Enhancements over BB5:**
1. **Swarm context** - Knows role in pipeline
2. **Pair coordination** - Links worker to validator
3. **Work routing** - Input/output specifications
4. **Resource tracking** - Token usage monitoring

---

## Communication Comparison

### BB5 Communications
```yaml
# .autonomous/agents/communications/heartbeat.yaml
heartbeats:
  planner:
    last_seen: '2026-02-03T23:43:34+07:00'
    status: in_progress_TASK-XXX
    loop_number: 30
    run_number: 79
  executor:
    last_seen: '2026-02-03T23:43:34+07:00'
    status: in_progress_TASK-XXX
    loop_number: 65
    run_number: 65
```

### Research Pipeline Communications
```yaml
# swarm/heartbeat.yaml (NEW - Global layer)
swarm_heartbeat:
  active_agents: 6
  healthy_agents: 6

agents:
  scout-worker:
    status: idle
    current_work: null
  scout-validator:
    status: idle
  analyst-worker:
    status: idle
  analyst-validator:
    status: idle
  planner-worker:
    status: idle
  planner-validator:
    status: idle

# communications/scout-state.yaml (Pipeline layer)
# communications/analyst-state.yaml
# communications/planner-state.yaml
```

**Design Decision:**
- BB5: Single `communications/heartbeat.yaml` (2 agents)
- Research: `swarm/heartbeat.yaml` (6 agents) + phase-specific state files
- **Rationale:** Research pipeline needs more granular coordination

---

## Hook Integration Assessment

### BB5 Hook Usage
- **None detected** in current BB5 architecture
- BB5 relies on manual file reading

### Research Pipeline Hook Usage
```bash
.claude/hooks/
├── session-start-swarm.sh           # NEW
└── session-start-timeline-memory.sh # NEW
```

**Compatibility:**
- ✅ Hooks are isolated to research pipeline
- ✅ No collision with BB5 (BB5 doesn't use hooks)
- ✅ Can coexist with future BB5 hooks

**Installation:**
```json
// ~/.claude/settings.json
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

---

## Data Flow Comparison

### BB5 Data Flow
```
Planner → queue.yaml → Executor
   ↑                        ↓
   └─────── results ────────┘
```

**Simple 2-agent loop:**
1. Planner creates tasks
2. Executor processes tasks
3. Results update queue

### Research Pipeline Data Flow
```
Sources → Scout → Analyst → Planner → BB5 Queue
            ↓        ↓         ↓
        Validator Validator Validator
```

**6-agent pipeline:**
1. Scout extracts patterns
2. Analyst scores patterns
3. Planner creates tasks
4. Validators provide feedback
5. Events coordinate flow

**Alignment:**
- Research pipeline feeds INTO BB5 queue
- Planner-worker creates tasks in `communications/queue.yaml`
- BB5 executor can process research pipeline tasks
- **Integration point:** `communications/queue.yaml`

---

## Routes.yaml Alignment

### Current BB5 Routes
BB5 doesn't use a centralized routes file - paths are hardcoded.

### Research Pipeline Routes
```yaml
# context/routes.yaml
routes:
  scout_worker: "agents/scout-worker"
  scout_validator: "agents/scout-validator"
  # ... etc

  communications: "communications"
  queue: "communications/queue.yaml"
  events: "communications/events.yaml"
  heartbeat: "communications/heartbeat.yaml"

  data_patterns: "data/patterns"
  data_analysis: "data/analysis"
```

**Gap:** Routes.yaml doesn't include `swarm/` directory!

**Fix needed:**
```yaml
# Add to context/routes.yaml
swarm: "swarm"
swarm_heartbeat: "swarm/heartbeat.yaml"
swarm_events: "swarm/events.yaml"
swarm_state: "swarm/state.yaml"
swarm_ledger: "swarm/ledger.md"
```

---

## Recommended Integration Steps

### Step 1: Fix routes.yaml (Critical)
Add swarm paths to `context/routes.yaml`:

```yaml
# Add these entries
swarm: "swarm"
swarm_heartbeat: "swarm/heartbeat.yaml"
swarm_events: "swarm/events.yaml"
swarm_state: "swarm/state.yaml"
swarm_ledger: "swarm/ledger.md"
```

### Step 2: Initialize Communications
Copy templates to actual communications:

```bash
cd communications
cp ../.templates/communications/scout-state.yaml.template scout-state.yaml
cp ../.templates/communications/analyst-state.yaml.template analyst-state.yaml
cp ../.templates/communications/planner-state.yaml.template planner-state.yaml
cp ../.templates/communications/events.yaml.template events.yaml
cp ../.templates/communications/heartbeat.yaml.template heartbeat.yaml
cp ../.templates/communications/queue.yaml.template queue.yaml
```

### Step 3: Install Hook
Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/research-pipeline/.claude/hooks/session-start-swarm.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Step 4: Test Integration
1. Start one agent: `./launch-scout.sh`
2. Verify hook injects context
3. Check swarm/heartbeat.yaml updates
4. Verify timeline-memory.md updates

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hook fails to inject | Low | High | Test before launch |
| Routes mismatch | Medium | Medium | Fix routes.yaml |
| BB5 collision | Low | Low | Separate directories |
| Performance (6 agents) | Medium | Medium | Monitor token usage |
| Queue overflow | Medium | High | Auto-scaling rules |

---

## Conclusion

### ✅ Architecture is Aligned

The research pipeline swarm memory system:
- ✅ Uses same patterns as BB5 (runs/, metrics/, state/)
- ✅ Extends BB5 concepts (heartbeat → swarm/heartbeat)
- ✅ Enhances with new capabilities (hooks, swarm layer)
- ✅ Isolates from BB5 (separate directory)
- ✅ Can feed into BB5 (queue.yaml integration)

### 🔧 Minor Fixes Needed

1. **routes.yaml** - Add swarm paths
2. **communications/** - Initialize from templates
3. **Hook testing** - Verify injection works

### 🚀 Ready for Deployment

After the 3 fixes above, the system is ready to run.

---

## Appendix: File Count Summary

| Category | BB5 | Research Pipeline | Notes |
|----------|-----|-------------------|-------|
| **Agents** | 2 | 6 | 3 pairs (worker + validator) |
| **Run directories** | 89+ | 0 | Will populate on launch |
| **Memory files** | 0 | 12 | timeline + running per agent |
| **Hook scripts** | 0 | 2 | SessionStart injection |
| **Swarm files** | 0 | 4 | Global coordination |
| **Templates** | 0 | 21 | 8 comms + 6 prompts + 7 runs |
| **Total files** | ~200 | ~50 | Research pipeline is lean |
