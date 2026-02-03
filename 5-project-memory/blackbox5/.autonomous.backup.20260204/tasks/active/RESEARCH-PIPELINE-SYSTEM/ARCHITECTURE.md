# Multi-Agent Research Pipeline Architecture

**Document ID:** ARCH-20260204000001
**Version:** 1.0
**Status:** Approved
**Created:** 2026-02-04

---

## Executive Summary

This document defines the architecture for a 4-agent research pipeline system that continuously discovers, analyzes, and implements patterns from external sources (GitHub, YouTube, documentation).

**Confidence Score:** 87%

---

## Architecture Overview

### 4-Agent Pipeline

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    SCOUT    │────▶│   ANALYST   │────▶│   PLANNER   │────▶│  EXECUTOR   │
│  (Discover) │     │   (Rank)    │     │  (Plan)     │     │  (Execute)  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                    │                    │                    │
      ▼                    ▼                    ▼                    ▼
   Neo4j               Neo4j               Neo4j               Neo4j
(:Pattern)           (:Analysis)           (:Task)           (:Result)
```

### Infrastructure Stack

- **Coordination:** Redis pub/sub (1ms latency)
- **Persistence:** Neo4j knowledge graph
- **Task Registry:** BB5 task system
- **Communication:** File-based + Redis hybrid

---

## Agent Specifications

### Agent 1: Research Scout

**Purpose:** Continuously scan sources and extract patterns

**Inputs:**
- Source configurations (GitHub repos, YouTube channels, RSS feeds)
- Scan intervals and filters
- Extraction rules

**Outputs:**
- Pattern nodes in Neo4j
- Redis event: `pattern:extracted`

**Triggers:**
- Scheduled (15m, 1h, 6h intervals)
- Event-driven (webhooks, manual requests)
- Adaptive (quality drops, queue empty)

### Agent 2: Integration Analyst

**Purpose:** Rank patterns by complexity and value

**Inputs:**
- Pattern from Scout
- Current stack context
- Historical data

**Outputs:**
- Analysis with complexity/value scores
- Decision: recommend/defer/reject
- Redis event: `analysis:complete`

**Triggers:**
- Immediate (high confidence patterns)
- Batch (10+ patterns accumulated)
- Scheduled (daily digest)

### Agent 3: Task Planner

**Purpose:** Create BB5 tasks from recommendations

**Inputs:**
- Analyst recommendation
- Project state and capacity
- Dependencies

**Outputs:**
- Task breakdown with dependencies
- Human approval gates
- Redis event: `tasks:new`

**Triggers:**
- On recommendation (decision == 'recommend')
- On capacity (executor available)
- Scheduled (sprint planning)

### Agent 4: Executor

**Purpose:** Selectively implement tasks

**Inputs:**
- Task from queue
- Agent capabilities
- Selection criteria

**Outputs:**
- Implementation results
- Artifacts (code, tests, docs)
- Redis event: `tasks:complete`

**Triggers:**
- Task available matching capabilities
- Task retry (failed tasks)
- Manual assignment

---

## Data Flow

### Redis Channels

| Channel | Direction | Payload |
|---------|-----------|---------|
| `research:new_source` | Scout → System | Source metadata |
| `pattern:extracted` | Scout → Analyst | Pattern ID, confidence |
| `analysis:complete` | Analyst → Planner | Decision, scores |
| `tasks:new` | Planner → Executor | Task definitions |
| `tasks:claimed` | Executor → System | Task assignment |
| `tasks:complete` | Executor → System | Results, feedback |
| `system:heartbeat` | All → System | Health checks |
| `system:approval` | Human → System | Approval decisions |

### Neo4j Schema

**Nodes:**
- `(:Source)` - GitHub, YouTube, RSS sources
- `(:Pattern)` - Extracted patterns
- `(:Analysis)` - Analyst outputs
- `(:Task)` - Planned tasks
- `(:Executor)` - Agent instances
- `(:ApprovalGate)` - Human approval points

**Relationships:**
- `(:Pattern)-[:EXTRACTED_FROM]->(:Source)`
- `(:Pattern)-[:ANALYZED_BY]->(:Analysis)`
- `(:Task)-[:IMPLEMENTS]->(:Pattern)`
- `(:Task)-[:DEPENDS_ON]->(:Task)`
- `(:Task)-[:EXECUTED_BY]->(:Executor)`

---

## Human Approval Gates

### Gate 1: Research Validation
- **Trigger:** Scout extracts pattern
- **Approver:** Research lead
- **Auto-approve:** Confidence > 0.9
- **Timeout:** 24h

### Gate 2: Integration Approval
- **Trigger:** Analyst recommends
- **Approver:** Tech lead
- **Auto-approve:** Complexity < 40, Value > 80
- **Timeout:** 48h

### Gate 3: Task Plan Review
- **Trigger:** Planner creates plan
- **Approver:** Product manager
- **Auto-approve:** Hours < 8, Risk < 30
- **Timeout:** 24h

### Gate 4: Implementation Review
- **Trigger:** Executor completes
- **Approver:** Code reviewer
- **Auto-approve:** Coverage > 90%, Quality > 85
- **Timeout:** 72h

---

## Error Handling

### Retry Strategies

| Error Type | Strategy | Max Retries | Fallback |
|------------|----------|-------------|----------|
| Source unavailable | Exponential backoff | 5 | Mark error, continue |
| Extraction failed | Fixed delay | 3 | Skip pattern |
| Rate limited | Exponential backoff | 10 | Pause source |
| Analysis timeout | Immediate | 2 | Simplified scoring |
| Execution failed | Exponential backoff | 3 | Mark failed, notify |

### Circuit Breakers
- Open after 5 failures in 1 hour
- Half-open after 5 minutes
- Closed after 3 successes

---

## Feedback Loop

```
Executor Results → Learning Aggregator → Model Updates → Continuous Improvement
                      ↓
              Knowledge Graph Evolution
```

**Weekly Updates:**
- Scout: Adjust source priorities
- Analyst: Retrain scoring models
- Planner: Update estimation model
- Executor: Adjust capability matching

**Monthly Reviews:**
- Deprioritize underperforming sources
- Prioritize high-value pattern types
- Refine approval thresholds
- Generate improvement recommendations

---

## Implementation Phases

### Phase 1: Core Infrastructure (Weeks 1-2)
- Redis schema setup
- Neo4j schema setup
- Base agent framework

### Phase 2: Agent Implementation (Weeks 3-4)
- Research Scout
- Integration Analyst
- Task Planner
- Executor

### Phase 3: Integration & Testing (Weeks 5-6)
- End-to-end pipeline
- Testing (unit, integration, load)
- Human approval UI

### Phase 4: Production Hardening (Weeks 7-8)
- Reliability (circuit breakers, DLQ)
- Observability (metrics, tracing)
- Documentation

---

## Key Assumptions

1. Redis maintains sub-millisecond latency
2. Neo4j handles 10K+ pattern nodes
3. GitHub/YouTube APIs support continuous polling
4. Human approval adds <24hr latency
5. Task execution success rate >70%

## Risks & Mitigations

| Risk | Level | Mitigation |
|------|-------|------------|
| API rate limits | High | Exponential backoff, source rotation |
| Complexity scoring inaccurate | High | Start rule-based, evolve to ML |
| Human approval bottlenecks | Medium | Auto-approval for low-risk tasks |
| Neo4j performance degradation | Medium | Time-based partitioning |
| Redis single point of failure | Low | Redis Sentinel for HA |

---

## Success Metrics

- Scout: 10+ sources processed in parallel
- Analyst: 80%+ recommendation accuracy
- Planner: Tasks created with <10% estimation error
- Executor: 70%+ task completion rate
- Pipeline: End-to-end <1 week from discovery to implementation

---

## Files Referenced

- `core/autonomous/redis/coordinator.py`
- `core/autonomous/schemas/task.py`
- `core/autonomous/agents/supervisor.py`
- `core/autonomous/agents/autonomous.py`
- `runtime/memory/brain/ingest/graph_ingester.py`
