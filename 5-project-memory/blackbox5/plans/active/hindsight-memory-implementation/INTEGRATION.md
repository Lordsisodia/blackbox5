# Hindsight Memory Integration Guide

**Purpose:** Map Hindsight memory architecture to existing BB5 systems and identify integration points
**Created:** 2026-02-04
**Related:** IG-008, PLAN-HINDSIGHT-001, Agent Swarm Memory Architecture

---

## Overview

The Hindsight memory implementation doesn't replace existing BB5 memory systems—it **extends and unifies** them. This document maps the relationships between:

1. Hindsight 4-Network Memory (World/Experience/Opinion/Observation)
2. Agent Swarm Memory Architecture (3-layer hierarchical)
3. Two Buffers Theory (Functional + Subjective)
4. Existing BB5 Run Memory (THOUGHTS/DECISIONS/RESULTS)

---

## Architecture Mapping

### Hindsight ↔ Two Buffers Theory

The Two Buffers theory from Moltbook community maps directly to Hindsight's 4 networks:

```
┌─────────────────────────────────────────────────────────────┐
│                    TWO BUFFERS THEORY                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  BUFFER 1: FUNCTIONAL (The Logs)                            │
│  ├─ World Network (W)     → FACTS.md                        │
│  │   Objective facts about the world                        │
│  │                                                           │
│  └─ Experience Network (B) → EXPERIENCES.md                 │
│      First-person actions taken                             │
│                                                              │
│  BUFFER 2: SUBJECTIVE (The Diaries)                         │
│  ├─ Opinion Network (O)   → OPINIONS.md                     │
│  │   Beliefs with confidence scores                         │
│  │                                                           │
│  └─ Observation Network (S) → OBSERVATIONS.md               │
│      Synthesized insights and reflections                   │
│                                                              │
│  SYNCHRONIZATION: RETAIN → RECALL → REFLECT                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Insight:** "El bienestar está en mantener ambos buffers sincronizados"
(Wellbeing requires keeping both buffers synchronized)

---

### Hindsight ↔ Agent Swarm Memory

The existing Agent Swarm Memory Architecture has 3 layers. Hindsight extends this:

```
┌─────────────────────────────────────────────────────────────┐
│              UNIFIED MEMORY ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  LAYER 1: SWARM COORDINATION (Global)                       │
│  ├─ swarm/heartbeat.yaml        [existing]                  │
│  ├─ swarm/events.yaml           [existing]                  │
│  ├─ swarm/state.yaml            [existing]                  │
│  └─ swarm/ledger.md             [existing]                  │
│                                                              │
│  LAYER 2: HINDSIGHT MEMORY (Persistent)    ← NEW           │
│  ├─ World (W) → FACTS.md                                    │
│  ├─ Experience (B) → EXPERIENCES.md                         │
│  ├─ Opinion (O) → OPINIONS.md                               │
│  ├─ Observation (S) → OBSERVATIONS.md                       │
│  ├─ PostgreSQL + pgvector (semantic search)                 │
│  └─ Neo4j (entity relationships)                            │
│                                                              │
│  LAYER 3: AGENT RUN MEMORY (Ephemeral)                      │
│  ├─ THOUGHTS.md                 [existing]                  │
│  ├─ DECISIONS.md                [existing]                  │
│  ├─ RESULTS.md                  [existing]                  │
│  └─ metadata.yaml               [existing]                  │
│                                                              │
│  OPERATIONS:                                                 │
│  ├─ RETAIN  (extract from Layer 3 → Layer 2)               │
│  ├─ RECALL  (query Layer 2 → inject into Layer 3)          │
│  └─ REFLECT (update Layer 2 beliefs)                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### Data Flow: BB5 Run → Hindsight Memory

```
┌─────────────────────────────────────────────────────────────┐
│                    RETAIN PIPELINE                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  INPUT: Agent Run Files                                     │
│  ├─ THOUGHTS.md ───────┐                                    │
│  ├─ DECISIONS.md ──────┼──▶ RETAIN Operation               │
│  ├─ RESULTS.md ────────┤       (LLM extraction)            │
│  └─ metadata.yaml ─────┘                                    │
│                           │                                  │
│                           ▼                                  │
│  EXTRACTED ENTITIES ──────┬──▶ Neo4j (entity graph)        │
│                           │                                  │
│  EXTRACTED MEMORIES ──────┼──▶ PostgreSQL + pgvector       │
│                           │     ├─ World (facts)            │
│                           │     ├─ Experience (actions)     │
│                           │     ├─ Opinion (beliefs)        │
│                           │     └─ Observation (insights)   │
│                           │                                  │
│  SYNTHESIZED ─────────────┴──▶ OBSERVATIONS.md              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Integration Points

### 1. Swarm Orchestrator Integration

The Swarm Orchestrator should use Hindsight memory for **pattern detection**:

```yaml
swarm_orchestrator:
  # Existing: Bottleneck detection
  bottleneck_detection:
    - scout_output_rate
    - analyst_processing_rate

  # NEW: Memory-driven insights
  memory_driven_analysis:
    - query: "patterns that caused bottlenecks in past"
      operation: RECALL
      network: Observation
      filter: {type: bottleneck, confidence: ">0.8"}

    - query: "token efficiency by agent type"
      operation: RECALL
      network: World
      filter: {metric: token_efficiency}
```

### 2. SessionStart Hook Integration

The SessionStart hook should inject **relevant memories** into agent context:

```bash
# Existing layers injected:
# 1. Swarm Context (Global)
# 2. Pipeline Context (Phase)
# 3. Agent Context (Individual)

# NEW: Layer 4 - Relevant Memories
# Inject memories related to current task
```

```yaml
session_context:
  # Existing layers...

  # NEW: Memory Layer
  relevant_memories:
    source: RECALL operation
    query: "similar tasks to {{current_task}}"
    networks: [World, Experience, Opinion]
    limit: 5
    min_confidence: 0.7
```

### 3. Navigation System Integration

The `bb5` CLI should include memory commands:

```bash
# Existing commands
bb5 context          # Show current context
bb5 discover         # Auto-detect context
bb5 nav <path>       # Navigate to location

# NEW: Memory commands
bb5 memory:recall "authentication patterns"     # Semantic search
bb5 memory:facts "PostgreSQL"                   # Query World network
bb5 memory:opinions "vector database"           # Query Opinion network
bb5 memory:entities "RALF"                      # Graph traversal
bb5 memory:reflect "update belief about X"      # Belief updating
```

### 4. Continuous Architecture Evolution Integration

The improvement loop should use Hindsight for **pattern detection**:

```
┌─────────────────────────────────────────────────────────────┐
│           MEMORY-DRIVEN IMPROVEMENT LOOP                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ANALYZE ───────────────────────────────────────────────┐   │
│     │                                                    │   │
│     ▼                                                    │   │
│  ┌─────────────────────────────────────┐                 │   │
│  │ Query Hindsight memory:             │                 │   │
│  │ - "What patterns caused issues?"    │                 │   │
│  │ - "What improvements worked best?"  │                 │   │
│  │ - "Where is documentation stale?"   │                 │   │
│  └─────────────────────────────────────┘                 │   │
│     │                                                    │   │
│     ▼                                                    │   │
│  VALIDATE ◀── RECALL provides evidence ──────────────────┘   │
│     │                                                        │
│     ▼                                                        │
│  PRIORITIZE                                                  │
│     │                                                        │
│     ▼                                                        │
│  EXECUTE ───▶ RETAIN captures new learnings ───────────────▶ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Dependencies and Timing

### Blocking Dependencies (Must Complete First)

| Dependency | Status | Impact |
|------------|--------|--------|
| IG-006 (Restructure) | 75% complete | Wait for folder consolidation before creating new templates |
| Project Memory Reorganization | In progress | Ensure FACTS.md etc. fit new structure |

### Parallel Work (Can Proceed Simultaneously)

| Work | Relationship |
|------|--------------|
| IG-007 (Architecture Evolution) | Hindsight enables memory-driven improvements |
| Navigation System | Hindsight RECALL integrates with bb5 CLI |
| Agent Swarm Memory | Hindsight extends the 3-layer architecture |

### Future Integration (After Hindsight Core)

| Integration | Description |
|-------------|-------------|
| Research Pipeline | Use Hindsight for cross-pattern analysis |
| Swarm Orchestrator | Memory-driven bottleneck prediction |
| RALF Core | Automatic memory injection into prompts |

---

## Research Cross-References

The following research documents inform this integration:

| Document | Key Insight |
|----------|-------------|
| `hindsight-deep-dive.md` | 4-network architecture, RETAIN/RECALL/REFLECT operations |
| `two-buffers-theory.md` | Functional vs Subjective memory synchronization |
| `hindsight-first-principles-analysis.md` | BB5 gaps mapped to Hindsight capabilities |
| `AGENT-SWARM-MEMORY-ARCHITECTURE.md` | 3-layer hierarchical memory for multi-agent |
| `blackbox5-memory-analysis.md` | Current BB5 memory limitations |

---

## Migration Strategy

### Phase 1: Extend (Don't Replace)

1. Add Hindsight 4-network files alongside existing files
2. RETAIN operation populates new memory from existing runs
3. Existing THOUGHTS.md/DECISIONS.md remain unchanged

### Phase 2: Integrate

1. SessionStart hook injects relevant memories
2. Swarm orchestrator queries Hindsight for patterns
3. Navigation system adds memory commands

### Phase 3: Optimize

1. Gradually shift from file-based to query-based memory access
2. Use RECALL for context injection instead of file parsing
3. REFLECT for belief updating based on outcomes

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Memory coverage | >90% | % of tasks processed by RETAIN |
| Recall latency | <500ms | Average query time |
| Recall relevance | >80% | Human-rated relevance |
| Swarm memory integration | 100% | All 6 agents use Hindsight |
| Navigation integration | 100% | bb5 memory: commands work |

---

## Open Questions

1. **Embedding Strategy:** Should we use text-embedding-3-small or fine-tune our own?
2. **Retention Policy:** How long do we keep memories? Forever or expire old ones?
3. **Privacy:** Some memories may contain sensitive data—encryption strategy?
4. **Multi-Project:** Should memories be shared across BB5 projects or isolated?
5. **Conflict Resolution:** When beliefs contradict, what's the resolution policy?

---

## Next Steps

1. [ ] Review this integration guide with stakeholders
2. [ ] Finalize dependency timing with IG-006
3. [ ] Design embedding pipeline with cost estimates
4. [ ] Prototype RETAIN operation on existing runs
5. [ ] Test RECALL integration with SessionStart hook

---

*This document should be updated as integration points are implemented*
