# TASK-BUILD-AUTOMATED-RESEARCH-PIPELINE-001: Build Automated Research Pipeline Agentic Team

**Task ID:** TASK-BUILD-AUTOMATED-RESEARCH-PIPELINE-001
**Type:** epic
**Priority:** critical
**Status:** in_progress
**Created:** 2026-02-04T01:30:00Z
**Agent:** Any (Multi-agent collaboration)

---

## Objective

Build a continuous multi-agent research pipeline system that automatically scans external sources (GitHub, YouTube, documentation), extracts patterns, ranks by complexity/value, and generates implementation tasks. This system leverages existing BB5 infrastructure (Redis, orchestrator, task registry, BMAD skills) with minimal new components.

---

## Core Philosophy

**Best of Both Worlds:** Combine Dual-RALF's proven file-based coordination with BB5's production-ready Redis infrastructure for a hybrid approach:
- **File-based:** Human-readable, auditable, persistent state
- **Redis:** Fast coordination (1ms), event streaming, agent status
- **Neo4j:** Graph relationships for concept mapping

**Compute Efficiency & Token Prioritization:**
- **Scout:** High frequency, low token cost per run (API calls, pattern extraction)
- **Analyst:** Medium frequency, HIGH token cost (complex reasoning, ranking algorithms)
- **Planner:** Low frequency, medium token cost (triggered on approval)
- **Executor:** Lowest frequency, variable token cost (one task at a time, quality focus)

**Optimal Ratio:** 10:3:1:0.3 (Scout:Analyst:Planner:Executor runs)

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    RESEARCH PIPELINE SYSTEM (RAPS)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   PHASE 1: DISCOVERY          PHASE 2: ANALYSIS                            │
│   ┌──────────────┐            ┌──────────────┐                             │
│   │   SCOUT      │───────────▶│   ANALYST    │                             │
│   │  (Continuous)│  Redis     │  (Continuous)│                             │
│   └──────────────┘  Events    └──────┬───────┘                             │
│          │                           │                                      │
│          ▼                           ▼                                      │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    SHARED STORAGE LAYER                        │      │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │      │
│   │  │ Concept Graph│  │  Rankings    │  │   Task Registry      │  │      │
│   │  │   (Neo4j)    │  │  (Redis)     │  │   (BB5 + Files)      │  │      │
│   │  └──────────────┘  └──────────────┘  └──────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                      │                                      │
│   PHASE 3: PLANNING                  │         PHASE 4: EXECUTION          │
│   ┌──────────────┐                   │         ┌──────────────┐            │
│   │   PLANNER    │◄──────────────────┘         │   EXECUTOR   │            │
│   │  (Triggered) │  Human Approval             │  (Selective) │            │
│   └──────┬───────┘                             └──────┬───────┘            │
│          │                                            │                     │
│          ▼                                            ▼                     │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                 COMMUNICATION LAYER                            │      │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │      │
│   │  │  Redis   │  │  Files   │  │  Events  │  │  Queue   │       │      │
│   │  │  Pub/Sub │  │  (YAML)  │  │  (YAML)  │  │  (YAML)  │       │      │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Agent Definitions

### Agent 1: Research Scout (raps-scout)

**Role:** Continuous discovery of patterns from external sources
**Type:** Continuous, parallel (max 10 concurrent sources)
**Location:** `.autonomous/research-pipeline/agents/scout/`

**Responsibilities:**
- Scan GitHub repos for patterns
- Process YouTube videos (transcripts)
- Crawl documentation sites
- Extract concepts and relationships
- Store in Neo4j concept graph

**Inputs:**
- Source configurations (GitHub URLs, YouTube channels, RSS feeds)
- Scan intervals and priorities
- Extraction rules per source type

**Outputs:**
- Concept nodes in Neo4j
- Source metadata in Redis
- Events: `research:new_source`, `pattern:extracted`

**Triggers:**
- Scheduled (every N minutes)
- Event-driven (on source addition)
- Adaptive (based on queue depth)

**BB5 Infrastructure Used:**
- `RedisCoordinator` for event publishing
- `bmad-analyst` skill for pattern extraction
- `web-search` skill for discovery

---

### Agent 2: Integration Analyst (raps-analyst)

**Role:** Rank patterns by value-to-cost ratio for BB5 integration
**Type:** Continuous, reactive
**Location:** `.autonomous/research-pipeline/agents/analyst/`

**Responsibilities:**
- Analyze integration complexity
- Estimate maintenance burden
- Assess value to BB5 ecosystem
- Rank by: `value / (integration_cost + maintenance_cost)`
- Generate recommendations with confidence scores

**Inputs:**
- Patterns from Neo4j
- BB5 stack context (current tech, patterns)
- Historical integration data

**Outputs:**
- Ranked recommendations (Redis sorted set)
- Analysis reports (files)
- Events: `analysis:complete`, `recommendation:ready`

**Triggers:**
- Immediate (on pattern extraction)
- Batch (periodic re-analysis)
- Scheduled (daily/weekly rankings)

**BB5 Infrastructure Used:**
- `RedisCoordinator` for rankings storage
- `bmad-architect` skill for complexity analysis
- `TaskRegistry` for historical data

---

### Agent 3: Task Planner (raps-planner)

**Role:** Transform approved recommendations into BB5 task structures
**Type:** Triggered (on human approval)
**Location:** `.autonomous/research-pipeline/agents/planner/`

**Responsibilities:**
- Decompose recommendations into subtasks
- Create BB5 task folder structure
- Generate execution plans
- Set up approval gates

**Inputs:**
- Approved recommendations (Redis)
- BB5 project state
- Task templates

**Outputs:**
- BB5 task packages (filesystem)
- Execution plans (YAML)
- Events: `tasks:new`, `plan:created`

**Triggers:**
- On recommendation approval (human gate)
- On capacity availability
- Scheduled (batch planning)

**BB5 Infrastructure Used:**
- `TaskRegistry` for task creation
- `SupervisorAgent` for task decomposition
- File-based task structure (BB5 standard)

---

### Agent 4: Task Executor (raps-executor)

**Role:** Selective implementation of planned tasks
**Type:** Selective (one task at a time)
**Location:** `.autonomous/research-pipeline/agents/executor/`

**Responsibilities:**
- Claim and execute tasks from queue
- Implement patterns in BB5
- Report results and learnings
- Update concept success rates

**Inputs:**
- Task packages (filesystem)
- BB5 context and capabilities
- Success criteria

**Outputs:**
- Implementation results
- Git commits
- Events: `tasks:claimed`, `tasks:complete`

**Triggers:**
- Task available in queue
- Retry (on failure)
- Manual (human-triggered)

**Constraints:**
- Max concurrent: 1
- Max duration: 4 hours per task
- Daily limit: 3 tasks

**BB5 Infrastructure Used:**
- `AutonomousAgent` for execution loop
- `RedisCoordinator` for task claiming
- `git-commit` skill for version control

---

## Human Approval Gates

### Gate 1: Research Validation
**Trigger:** After Scout identifies new patterns
**Timeout:** 24 hours (auto-approve if no response)
**Action:** Review concept map, validate relevance

### Gate 2: Integration Approval
**Trigger:** After Analyst ranks recommendations
**Timeout:** 48 hours
**Action:** Approve/deny/modify recommendations

### Gate 3: Task Plan Review
**Trigger:** After Planner creates task package
**Timeout:** 24 hours
**Action:** Review task breakdown, approve for execution

### Gate 4: Implementation Review
**Trigger:** After Executor completes task
**Timeout:** 72 hours
**Action:** Review implementation, merge or request changes

---

## Communication Protocol

### Hybrid Approach (Best of Both Worlds)

**Redis Channels (Fast Coordination):**
```
research:new_source      → New source discovered
pattern:extracted        → Pattern extracted from source
analysis:complete        → Analysis finished
recommendation:ready     → Recommendation ranked
tasks:new               → New tasks available
tasks:claimed           → Task claimed by executor
tasks:complete          → Task completed
system:heartbeat        → Agent health checks
system:approval         → Human approval events
```

**File-Based (Audit Trail + Human Readable):**
```
.autonomous/research-pipeline/
├── communications/
│   ├── events.yaml       # All events (chronological)
│   ├── queue.yaml        # Task queue state
│   ├── approvals.yaml    # Human approval log
│   └── heartbeat.yaml    # Agent health status
├── state/
│   ├── scout-state.yaml
│   ├── analyst-state.yaml
│   ├── planner-state.yaml
│   └── executor-state.yaml
└── knowledge/
    ├── concepts/         # Neo4j export/backups
    ├── sources/          # Source metadata
    └── patterns/         # Extracted patterns
```

---

## Storage Schema

### Neo4j (Concept Graph)

```cypher
// Nodes
(:Source {id, type, url, title, author, scanned_at})
(:Pattern {id, name, description, domain, complexity_score})
(:Concept {id, name, definition, category})
(:Analysis {id, score, confidence, created_at})
(:Task {id, title, status, priority})
(:ApprovalGate {id, type, status, reviewer})

// Relationships
(:Pattern)-[:EXTRACTED_FROM]->(:Source)
(:Pattern)-[:IMPLEMENTS]->(:Concept)
(:Pattern)-[:RELATED_TO {strength}]->(:Pattern)
(:Analysis)-[:EVALUATES]->(:Pattern)
(:Task)-[:ADDRESSES]->(:Pattern)
(:ApprovalGate)-[:BLOCKS]->(:Task)
```

### Redis (Coordination)

```
# Sorted Sets
raps:rankings                    # Score = value/cost ratio
raps:sources:queue              # Score = priority
raps:tasks:pending              # Score = created_at

# Hashes
raps:agent:{agent_id}           # Agent state
raps:pattern:{pattern_id}       # Pattern metadata
raps:recommendation:{rec_id}    # Full recommendation
raps:gate:{gate_id}             # Approval gate status

# Lists
raps:events:recent              # Last 1000 events
raps:tasks:history              # Completed task IDs

# Pub/Sub Channels
raps:events:{agent_type}        # Agent-specific events
raps:events:human               # Human interaction
raps:events:system              # System events

# Streams
raps:execution:log              # Persistent execution log
```

### Filesystem (BB5 Tasks)

```
5-project-memory/blackbox5/
└── .autonomous/
    └── research-pipeline/
        ├── tasks/
        │   ├── active/
        │   │   └── {task-id}/
        │   │       ├── TASK-{task-id}.md
        │   │       ├── subtasks/
        │   │       ├── runs/
        │   │       └── execution-plan.yaml
        │   └── completed/
        ├── runs/
        │   ├── scout/
        │   ├── analyst/
        │   ├── planner/
        │   └── executor/
        └── knowledge/
            ├── concepts/
            ├── sources/
            └── patterns/
```

---

## BB5 Infrastructure Integration

### What We Reuse (Don't Reinvent)

| Component | BB5 Infrastructure | How We Use It |
|-----------|-------------------|---------------|
| Task Management | `TaskRegistry` + SQLite | Store research tasks |
| Coordination | `RedisCoordinator` | Agent communication |
| Orchestration | `AgentOrchestrator` | Workflow management |
| Event Bus | `EventBus` / `RedisEventBus` | Event streaming |
| Agent Pool | `AutonomousAgentPool` | Agent lifecycle |
| Skills | 22+ BMAD skills | Pattern extraction, analysis |
| State Management | File-based + Redis | Hybrid state storage |
| Communication | `communications/*.yaml` | Audit trail |

### What We Add (New Components)

| Component | Purpose | Location |
|-----------|---------|----------|
| Neo4j | Concept graph storage | External service |
| Scout Agent | Source scanning | `agents/scout/` |
| Analyst Agent | Pattern ranking | `agents/analyst/` |
| RAPS Planner | Task planning | `agents/planner/` |
| RAPS Executor | Task execution | `agents/executor/` |
| Research Pipeline Config | Source configs | `config/sources.yaml` |

---

## BB5 Infrastructure Deep Dive

### 1. RALF Loop Pattern (For Scout/Analyst Continuous Execution)

**Location:** `/2-engine/.autonomous/shell/ralf-loop.sh`

**What it provides:**
- Continuous execution loop with checkpointing
- Context budget management (prevents runaway agents)
- Phase gate checking for controlled progression
- Post-execution analysis hooks
- Completion detection via `<promise>COMPLETE</promise>`

**How we use it:**
```python
# Scout Continuous Loop (adapted from RALF)
class ScoutContinuousLoop:
    def run(self):
        while True:
            # Check context budget (from ralf-loop.sh)
            if self.context_budget_exceeded():
                self.checkpoint_and_exit()

            # Execute discovery iteration
            result = self.scout.execute_discovery_iteration()

            # Publish events to EventBus
            self.event_bus.publish(Event(
                type="scout.discovery.completed",
                data=result
            ))

            # Check completion signals
            if result.status == "COMPLETE":
                break
            if result.status == "BLOCKED":
                self.handle_blocked()

            sleep(10)  # Configurable interval
```

**Token Efficiency:** RALF loops have built-in context management to prevent token overflow.

---

### 2. AgentOrchestrator (For Pipeline Coordination)

**Location:** `/2-engine/core/orchestration/Orchestrator.py`

**What it provides:**
- Wave-based parallelization (Scout scans 10 sources in parallel)
- Dependency management (Analyst waits for Scout events)
- Retry logic with `max_retries` per step
- Checkpointing and resume capability
- Deadlock detection using DFS

**How we use it:**
```python
# Research Pipeline Orchestration
orchestrator = AgentOrchestrator(
    event_bus=event_bus,
    max_concurrent_agents=5,
    enable_checkpoints=True
)

# Wave 1: Scout discovers sources (parallel)
scout_wave = orchestrator.create_parallel_workflow(
    tasks=[scout_task_1, scout_task_2, ...],
    agent_mapping={task: scout_agent for task in scout_tasks}
)

# Wave 2: Analyst processes discoveries (triggered by events)
analyst_wave = orchestrator.create_workflow(
    steps=[analyst_step],
    depends_on=[scout_wave]
)
```

---

### 3. Feature Pipeline (As Our Architectural Model)

**Location:** `/2-engine/core/orchestration/pipeline/feature_pipeline.py`

**What it provides:**
- Complete pipeline: Discovery → Review → Breakdown → Implementation → Validation
- `FeatureReviewAgent` for AI-powered review
- `FeatureBreakdownAgent` for task decomposition
- State management through Feature lifecycle

**How we map our pipeline:**
| Feature Pipeline | Research Pipeline | Agent |
|-----------------|-------------------|-------|
| Discovery | Source Scanning | Scout |
| Review | Pattern Analysis | Analyst |
| Breakdown | Task Planning | Planner |
| Implementation | Task Execution | Executor |
| Validation | Human Review | Gates |

**Code pattern to reuse:**
```python
# Instead of building from scratch, extend FeaturePipeline
class ResearchPipeline(FeaturePipeline):
    def __init__(self):
        super().__init__()
        self.scout_agent = ScoutAgent()
        self.analyst_agent = AnalystAgent()

    async def discover_patterns(self, sources):
        # Use FeaturePipeline's discovery pattern
        features = await self.propose_features_from_sources(sources)
        return features
```

---

### 4. VibeKanban + Task Lifecycle (For Task Queue Management)

**Location:** `/2-engine/core/agents/definitions/managerial/skills/vibe_kanban_manager.py`

**What it provides:**
- Complete task lifecycle: plan → create → assign → monitor → review → merge
- Wave execution for batch processing
- Dependency tracking (tasks block on other tasks)
- Task states: TODO, IN_PROGRESS, IN_REVIEW, DONE

**How we use it:**
```python
# Task queue management for Executor
vkb = VibeKanbanManager()

# Planner creates tasks
for recommendation in approved_recommendations:
    task = vkb.create_task(
        title=recommendation.title,
        description=recommendation.description,
        priority=recommendation.priority
    )

# Executor claims and executes
task_info = vkb.start_agent(
    task_id=task.id,
    executor="RAPS_EXECUTOR",
    branch=generate_branch_name(task.title)
)

# Monitor until completion
result = vkb.monitor_task(
    task_id=task.id,
    poll_interval=5,
    timeout=14400  # 4 hours max
)
```

---

### 5. EventBus (For Agent Communication)

**Location:** `/2-engine/core/orchestration/state/event_bus.py`

**What it provides:**
- Redis-backed pub/sub with fallback to in-memory
- Standard event types: AGENT_STARTED, TASK_COMPLETED, etc.
- Correlation IDs for request tracing
- Auto-reconnection on failure

**Our Event Types (extending standard):**
```python
# Scout events
RESEARCH_SOURCE_DISCOVERED = "research.source.discovered"
PATTERN_EXTRACTED = "pattern.extracted"

# Analyst events
ANALYSIS_COMPLETED = "analysis.completed"
RECOMMENDATION_RANKED = "recommendation.ranked"

# Pipeline events
HUMAN_APPROVAL_REQUIRED = "human.approval.required"
HUMAN_APPROVAL_GRANTED = "human.approval.granted"
TASK_PLANNED = "task.planned"
TASK_EXECUTED = "task.executed"
```

---

### 6. BaseAgent (For Agent Implementation)

**Location:** `/2-engine/core/agents/definitions/core/base_agent.py`

**What it provides:**
- Well-defined lifecycle: validate → before_execution → execute → after_execution
- Tier 2 skills support (load/unload to manage tokens)
- Task capability checking
- Token usage tracking

**How we implement our agents:**
```python
class ScoutAgent(BaseAgent):
    def __init__(self):
        config = AgentConfig(
            name="raps-scout",
            role="research_scout",
            capabilities=["source_scanning", "pattern_extraction"],
            tools=["github-api", "youtube-api", "web-crawler"],
            max_tokens=2000  # Low token limit for Scout
        )
        super().__init__(config)

    async def execute(self, task: AgentTask) -> AgentResult:
        # Load skills on-demand (saves tokens)
        await self.load_skill("pattern-extraction", force_full=False)

        # Execute with token tracking
        result = await self.scan_source(task.context["source"])

        return AgentResult(
            success=True,
            output=result.patterns,
            token_usage=self.get_token_usage()
        )
```

---

## Token Prioritization Strategy

### Agent Token Cost Analysis

| Agent | Token Cost/Run | Frequency | Daily Tokens | Priority |
|-------|---------------|-----------|--------------|----------|
| **Scout** | ~500-1000 | Every 2 min | ~360K | HIGH |
| **Analyst** | ~3000-5000 | Every 10 min | ~432K | HIGHEST |
| **Planner** | ~2000-3000 | On approval (~5/day) | ~15K | MEDIUM |
| **Executor** | ~4000-8000 | 3 tasks/day | ~24K | MEDIUM |

**Total Daily Budget: ~830K tokens**

### Optimal Agent Ratio

Based on value-per-token analysis:

```
Ratio: 10 Scout : 3 Analyst : 1 Planner : 0.3 Executor

For every 10 Scout discoveries:
- 3 get analyzed in depth (Analyst)
- 1 generates a task (Planner)
- 0.3 get executed (Executor)

This creates a natural funnel:
100 sources scanned → 30 analyzed → 10 planned → 3 executed
```

### Token Allocation Strategy

**Tier 1 - Always Running (70% of budget):**
- Scout: Continuous scanning (low cost, high volume)
- Analyst: Event-driven analysis (medium cost, high value)

**Tier 2 - Triggered (20% of budget):**
- Planner: On human approval (medium cost, selective)

**Tier 3 - Selective (10% of budget):**
- Executor: One task at a time (high cost, quality focus)

### Frequency Configuration

```yaml
# config/agent-frequencies.yaml
scout:
  mode: continuous
  interval_seconds: 120  # Every 2 minutes
  max_concurrent: 10
  token_budget_per_run: 1000

analyst:
  mode: event_driven
  batch_size: 5  # Analyze 5 patterns at once
  max_frequency: 360  # Every 6 minutes max
  token_budget_per_run: 5000

planner:
  mode: triggered
  trigger: human_approval
  token_budget_per_run: 3000

executor:
  mode: selective
  max_concurrent: 1
  max_daily: 3
  token_budget_per_task: 8000
```

### Dynamic Token Management

```python
class TokenManager:
    def __init__(self):
        self.daily_budget = 1_000_000  # 1M tokens/day
        self.tier_allocations = {
            'scout': 0.40,      # 40% for discovery
            'analyst': 0.30,    # 30% for analysis
            'planner': 0.15,    # 15% for planning
            'executor': 0.15    # 15% for execution
        }

    def should_run_agent(self, agent_type: str) -> bool:
        usage = self.get_daily_usage(agent_type)
        budget = self.daily_budget * self.tier_allocations[agent_type]

        if usage >= budget * 0.9:  # 90% threshold
            return False  # Skip this run
        return True

    def adjust_for_backlog(self):
        # If Executor backlog > 10, reduce Scout frequency
        if self.get_executor_backlog() > 10:
            self.scout_interval *= 1.5  # Slow down discovery

        # If Analyst queue > 50, increase Analyst frequency
        if self.get_analyst_queue() > 50:
            self.analyst_batch_size *= 2  # Process more per run
```

### Cost Optimization Strategies

1. **Scout Caching:**
   - Cache API responses (GitHub, YouTube)
   - Only re-scan if source updated
   - Reduces Scout tokens by ~60%

2. **Analyst Batching:**
   - Analyze 5 patterns in one context window
   - Compare patterns to each other
   - Reduces Analyst tokens by ~40%

3. **Planner Reuse:**
   - Cache similar task plans
   - Reuse planning for similar patterns
   - Reduces Planner tokens by ~30%

4. **Executor Checkpointing:**
   - Save progress every 15 minutes
   - Resume on failure (don't restart)
   - Reduces Executor tokens by ~20%

---

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
**Goal:** Core infrastructure and Scout agent

**Subtasks:**
- [ ] Set up Neo4j instance
- [ ] Configure Redis schema
- [ ] Create agent directory structure
- [ ] Build Scout agent MVP (GitHub scanning)
- [ ] Integrate with BB5 TaskRegistry
- [ ] Set up event bus

**Deliverables:**
- Scout can scan GitHub repos
- Concepts stored in Neo4j
- Events flow through Redis

---

### Phase 2: Analysis (Week 3-4)
**Goal:** Analyst agent and ranking system

**Subtasks:**
- [ ] Build Analyst agent
- [ ] Implement ranking algorithm
- [ ] Create human review UI
- [ ] Build Gate 1 (Research Validation)
- [ ] Build Gate 2 (Integration Approval)

**Deliverables:**
- Analyst produces ranked recommendations
- Human can review and approve
- Approved recommendations trigger events

---

### Phase 3: Planning (Week 5-6)
**Goal:** Task Planner and BB5 integration

**Subtasks:**
- [ ] Build Planner agent
- [ ] Task package generation
- [ ] BB5 task structure creation
- [ ] Build Gate 3 (Task Plan Review)
- [ ] Execution plan generation

**Deliverables:**
- Planner creates valid BB5 task packages
- Task structure follows BB5 conventions
- Human can review task packages

---

### Phase 4: Execution (Week 7-8)
**Goal:** Executor agent and end-to-end flow

**Subtasks:**
- [ ] Build Executor agent
- [ ] Single-task execution
- [ ] Result reporting
- [ ] Build Gate 4 (Implementation Review)
- [ ] Feedback loop to Analyst

**Deliverables:**
- Full pipeline executes end-to-end
- One task can be completed automatically
- Results are documented

---

### Phase 5: Scale & Harden (Week 9-10)
**Goal:** Parallel processing and optimization

**Subtasks:**
- [ ] Scout parallelization (10+ sources)
- [ ] YouTube source support
- [ ] Documentation source support
- [ ] Performance optimization
- [ ] Monitoring and alerting
- [ ] Error handling and retries

**Deliverables:**
- Pipeline processes 10+ sources in parallel
- All source types supported
- System is observable and maintainable

---

## Sub-Tasks

| ID | Task | Status | Priority | Phase | Agent |
|----|------|--------|----------|-------|-------|
| 001-A | Research BB5 Infrastructure | pending | critical | 0 | Analyst |
| 001-B | Design Agent Interfaces | pending | critical | 0 | Architect |
| 001-C | Set Up Neo4j | pending | critical | 1 | Dev |
| 001-D | Configure Redis Schema | pending | critical | 1 | Dev |
| 001-E | Build Scout Agent | pending | critical | 1 | Dev |
| 001-F | Build Analyst Agent | pending | critical | 2 | Dev |
| 001-G | Build Human Gates 1-2 | pending | high | 2 | Dev |
| 001-H | Build Planner Agent | pending | high | 3 | Dev |
| 001-I | Build Human Gate 3 | pending | high | 3 | Dev |
| 001-J | Build Executor Agent | pending | high | 4 | Dev |
| 001-K | Build Human Gate 4 | pending | high | 4 | Dev |
| 001-L | Add YouTube Support | pending | medium | 5 | Dev |
| 001-M | Add Documentation Support | pending | medium | 5 | Dev |
| 001-N | Performance Optimization | pending | medium | 5 | Dev |
| 001-O | Monitoring & Alerting | pending | low | 5 | Dev |

---

## Success Criteria

- [ ] Scout scans 10+ sources in parallel
- [ ] Analyst ranks 100+ patterns/day
- [ ] Planner creates valid BB5 tasks
- [ ] Executor completes 3 tasks/day
- [ ] All 4 human gates functional
- [ ] Pipeline runs end-to-end autonomously
- [ ] Uses existing BB5 infrastructure
- [ ] <1s latency for agent coordination
- [ ] <5min from pattern discovery to task creation

---

## Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Neo4j complexity | Medium | Medium | Start simple, evolve schema |
| API rate limits | High | Medium | Exponential backoff, caching |
| Human bottleneck | High | Medium | Auto-approval thresholds |
| Event ordering | Medium | High | Idempotent operations |
| Compute costs | Medium | Medium | Continuous + triggered hybrid |
| BB5 integration | Low | High | Reuse existing components |

---

## Resources

### BB5 Infrastructure
- `/2-engine/core/autonomous/` - Agent framework
- `/2-engine/core/orchestration/` - Orchestrator
- `/2-engine/core/agents/definitions/` - Agent definitions
- `/2-engine/.autonomous/skills/` - BMAD skills

### External Services
- Neo4j - Concept graph
- Redis - Coordination
- GitHub API - Source scanning
- YouTube API - Video processing

---

## Notes

This system transforms BB5 from manual research to autonomous continuous improvement. It leverages:

1. **Dual-RALF's** proven file-based coordination for auditability
2. **BB5's** production Redis infrastructure for speed
3. **Neo4j** for complex concept relationships
4. **Existing skills** (bmad-analyst, bmad-architect) for intelligence

The result: A research pipeline that discovers, ranks, plans, and executes autonomously while keeping humans in control at key decision points.

---

*Next: Create sub-tasks and begin Phase 0 (Research & Design)*
