# DECISIONS - TASK-001-B: Design Agent Interfaces

**Date:** 2026-02-10
**Agent:** bmad-architect

---

## Decision 1: Four-Worker Agent Design

**Decision:** Focus on 4 worker agents (Scout, Analyst, Planner, Executor) rather than 6 agents.

**Rationale:**
- Task specifically asks for "4-agent research pipeline"
- Worker-Validator pairs: Validators are coordination agents, not execution agents
- Workers have public-facing input/output contracts that need specification
- Validators use private feedback mechanisms

**Impact:**
- Interface specifications document only workers
- Executors are the BB5 executor, already defined in BB5 architecture
- Communication patterns work the same for workers and validators

---

## Decision 2: YAML Frontmatter Schema Format

**Decision:** Use YAML frontmatter-style schemas for all interface specifications.

**Format:**
```yaml
# scout-agent-interface.yaml
version: "1.0.0"

# Input Contracts
inputs:
  work_queue:
    type: array
    items:
      type: object
      properties:
        source_url: {type: string}

# Output Contracts
outputs:
  pattern:
    type: object
    properties:
      id: {type: string}
      name: {type: string}
      ...
```

**Rationale:**
- Easy for humans to read and write
- Machine-readable (can be validated)
- Consistent with existing BB5 file formats (queue.yaml, events.yaml, metadata.yaml)
- Simple to extend with new fields

---

## Decision 3: Event-Driven Communication Protocol

**Decision:** Use event-driven communication via `communications/events.yaml` rather than direct messaging.

**Rationale:**
- Decouples agents - they don't need to know who's listening
- Enables multiple subscribers to events
- Easy to debug (events are loggable)
- Supports async processing

**Event Types Defined:**
- `source.discovered` - Scout worker
- `pattern.extracted` - Scout worker
- `analysis.complete` - Analyst worker
- `tasks.new` - Planner worker
- `task.started` - Executor agent
- `task.completed` - Executor agent
- `task.failed` - Executor agent

---

## Decision 4: Timeline Memory as State Source

**Decision:** Each agent reads its work queue from `timeline-memory.md` rather than centralized state files.

**Rationale:**
- Agents own their work state
- Reduces coordination overhead
- Enables local decision making
- Validators still get feedback via chat-log.yaml

**Timeline Memory Structure:**
```yaml
work_queue:
  priority_sources: []
  backlog: []
  in_progress: null
  completed_today: 0

scoring_model:
  value_factors: {}
  complexity_factors: {}
  thresholds: {}

swarm_context:
  agent: scout-worker
  pipeline_phase: scout
  pair_agent: scout-validator
  upstream_agents: []
  downstream_agents: [analyst-worker]
```

---

## Decision 5: Storage Interface Design

**Decision:** Three-tier storage approach with independent concerns.

### 5.1 Neo4j Graph Schema
**Purpose:** Store concept relationships and pattern graph

**Node Types:**
- `PatternNode` - Extracted patterns
- `ConceptNode` - Atomic concepts
- `SourceNode` - GitHub/YouTube sources
- `RelationshipNode` - Connections between patterns

**Edge Types:**
- `IMPLEMENTS` - Pattern implements concept
- `USES` - Pattern uses concept
- `DERIVED_FROM` - Pattern derived from another
- `APPROVED` - Analyst approved pattern

### 5.2 Redis Data Structures
**Purpose:** Caching, session state, quick lookups

**Key Patterns:**
- `pattern:{id}` - Pattern data (string, JSON)
- `queue:priority` - Priority work queue (list)
- `queue:backlog` - Backlog work queue (list)
- `cache:extraction:{url}` - Source extraction cache (string, TTL)
- `agent:{agent_name}:last_seen` - Heartbeat (string, TTL)

### 5.3 File System Layout
**Purpose:** Persistent storage, versioning

**Structure:**
```
data/
├── patterns/           # Extracted patterns
│   ├── P-001.yaml
│   └── ...
├── analysis/           # Analyst rankings
│   ├── P-001.yaml
│   └── ...
└── tasks/              # Planned tasks
    ├── TASK-RAPS-001/
    │   ├── TASK-RAPS-001.md
    │   ├── subtasks/
    │   └── context/
    └── ...

agents/{agent}/memory/ # Long-term learning
agents/{agent}/runs/   # Run history
```

---

## Decision 6: Error Handling Strategy

**Decision:** Three-tier error handling with different recovery strategies.

### Tier 1: Transient Errors (Retry)
**Examples:** Network timeout, API rate limit
**Strategy:** Auto-retry with exponential backoff
**Max retries:** 3
**Backoff:** 1s, 2s, 4s

### Tier 2: Recoverable Errors (Checkpoint)
**Examples:** Token limit reached, partial extraction
**Strategy:** Save progress, exit PARTIAL, resume later
**Checkpoint files:** THOUGHTS.md, RESULTS.md, DECISIONS.md, metadata.yaml

### Tier 3: Fatal Errors (Fail-closed)
**Examples:** Invalid source URL, corrupted data, validation failure
**Strategy:** Exit BLOCKED, log error, notify human/validator
**Recovery:** Manual intervention required

---

## Decision 7: Token Budget Enforcement

**Decision:** All agents must enforce token budgets with checkpoint support.

**Budgets:**
| Agent | Target/Run | Context Limit | Trigger |
|-------|-----------|---------------|---------|
| Scout Worker | 3,000 | 7,500 (40%) | At 60% trigger PARTIAL |
| Analyst Worker | 4,800 | 12,000 (40%) | At 60% trigger PARTIAL |
| Planner Worker | 3,600 | 9,000 (40%) | At 60% trigger PARTIAL |
| Executor Agent | Variable | ~7,500 | Auto-scaling |

**Checkpoint Format:**
```yaml
# scout-worker/runs/run-XXX/RESULTS.md
status: PARTIAL
extracted_patterns: 2
remaining_patterns: 1
checkpoint_at: "2026-02-10T12:00:00Z"
next_steps: |
  Continue extraction from pattern P-003
```

---

## Decision 8: Integration with BB5

**Decision:** Research pipeline uses BB5's existing structures for tasks, runs, and metrics.

**Integration Points:**
1. `communications/queue.yaml` - Research pipeline writes tasks here, BB5 executor reads
2. `agents/executor/runs/` - BB5 executor run directory (already exists)
3. `agents/executor/metrics/` - Performance tracking
4. BB5 task structure - Research pipeline creates tasks in `tasks/active/TASK-XXX/`

**Alignment:**
- Same run directory structure (runs/run-XXX/)
- Same metrics/ directory
- Same state/ directory
- BB5 uses BB5's agent loop for execution

---

## Decision Summary

| Decision | Value |
|----------|-------|
| 4 Worker Agents | Clear responsibility boundaries |
| YAML Schema Format | Human-readable + machine-validated |
| Event-Driven Comms | Decoupled, scalable |
| Timeline Memory | Agent-owned work state |
| 3-Tier Storage | Separate concerns, flexible |
| 3-Tier Error Handling | Appropriate recovery for each error type |
| Token Budget Enforcement | Predictable resource usage |
| BB5 Alignment | Consistent patterns with BB5 |

---

## Open Questions

1. **Neo4j integration timing:** Should Neo4j be available from day 1 or added later?
   - *Decision:* Document schema but don't enforce immediate implementation. Optional for Phase 2.

2. **Validator agent interfaces:** Should validators have formal input/output contracts?
   - *Decision:* No. Validators use private feedback via chat-log.yaml and memory files. Only workers have public interfaces.

3. **Executor Agent frequency:** How often does BB5 executor check queue.yaml?
   - *Decision:* Executor uses BB5's existing loop (every 30-60 minutes). Research pipeline adds to queue, executor picks up when it next loops.

---

## Approval Required

These decisions enable the interface specifications document. Review and approve before proceeding to interface schema definitions.
