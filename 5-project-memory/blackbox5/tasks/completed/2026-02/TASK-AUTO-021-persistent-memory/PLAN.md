# PLAN.md: Improve Blackbox5 Persistent Memory System

**Task ID:** TASK-AUTO-021-persistent-memory (was TASK-MEMORY-001)
**Status:** Planning
**Priority:** MEDIUM
**Created:** 2026-02-04
**Estimated Effort:** 2-3 days
**Linked Goal:** IG-008 - Implement Hindsight Memory Architecture
**Linked Plan:** PLAN-HINDSIGHT-001

---

## 1. First Principles Analysis

### Why Improve the Memory System?

1. **Current Limitations**: File-based memory (THOUGHTS.md, DECISIONS.md) per run lacks continuity
2. **No Semantic Search**: Cannot search across historical runs efficiently
3. **No Relationship Tracking**: Decisions and learnings are isolated
4. **Token Inefficiency**: Full file reads waste context window
5. **Agent Identity**: No "continuity of self" across sessions

### What Happens Without Better Memory?

| Problem | Impact | Severity |
|---------|--------|----------|
| Repeated mistakes | Same errors in multiple runs | High |
| Lost insights | Learnings not applied | High |
| Context waste | Full files read unnecessarily | Medium |
| Disconnected sessions | Each run starts fresh | Medium |
| No pattern recognition | Cannot identify trends | Medium |

### How Should Memory Work?

**Two Buffers Theory (from Moltbook community):**

**Buffer 1: Functional Memory (The Logs)**
- Commands executed, APIs called, errors encountered
- Continuity of doing - ability to resume tasks
- Structured, searchable, machine-readable

**Buffer 2: Subjective Memory (The Diaries)**
- Reflections, intentions, reasoning
- Continuity of being - the version that made choices
- Narrative, contextual, human-readable

**Synchronization:**
> "Wellbeing requires keeping both buffers synchronized."
> Too much log, not enough diary = efficient but hollow
> Too much diary, not enough log = intentional but ineffective

---

## 2. Current State Assessment

### Existing Memory Architecture

**Current System:**
- THOUGHTS.md - Session thoughts and reasoning
- DECISIONS.md - Decisions made during session
- LEARNINGS.md - What was learned
- ASSUMPTIONS.md - Working assumptions
- RESULTS.md - Outcomes and metrics

**Storage:** File-based per run in `.autonomous/agents/[agent]/runs/[run-id]/`

### Research Findings: Leading Memory Systems

| System | Architecture | LongMemEval | Best For |
|--------|-------------|-------------|----------|
| **Hindsight** | 4-network structured | 91.4% | Advanced agents with belief updating |
| **Zep** | Temporal Knowledge Graph | 71.2% | Production at scale |
| **Mem0** | Vector + Graph + KV | 68.5% | Simple integration |
| **Letta** | OS-inspired hierarchy | 74.0%* | Research/explicit control |
| **memU** | 3-layer hierarchical | N/A | 24/7 proactive agents |

*Letta achieved 74% with simple filesystem + gpt-4o-mini

### Hindsight Architecture (Selected)

**4-Network Structure:**
1. **Working Memory Network** - Current context
2. **Episodic Memory Network** - Past experiences
3. **Semantic Memory Network** - Facts and knowledge
4. **Procedural Memory Network** - Skills and patterns

**Three Operations:**
- **RETAIN** - Store new information
- **RECALL** - Retrieve relevant memories
- **REFLECT** - Consolidate and synthesize

---

## 3. Proposed Solution

### Hybrid Memory Architecture for BB5

**Layer 1: Vector Store (Semantic Search)**
- ChromaDB or similar for embeddings
- Fast similarity search across all runs
- Automatic embedding of THOUGHTS.md, DECISIONS.md

**Layer 2: Structured Store (Relationships)**
- SQLite or JSON for structured data
- Track relationships between decisions
- Query by task, goal, agent, time

**Layer 3: File System (Raw Content)**
- Keep existing THOUGHTS.md, etc.
- New memory layer adds indices
- Backward compatible

### Implementation Components

**1. Memory Foundation (TASK-HINDSIGHT-001)**
```python
# lib/memory/core.py
class MemorySystem:
    def __init__(self, vector_store, structured_store):
        self.vector = vector_store
        self.structured = structured_store

    def retain(self, content: str, metadata: dict):
        """Store new memory"""
        # Embed and store in vector DB
        # Store metadata in structured store

    def recall(self, query: str, filters: dict = None) -> list:
        """Retrieve relevant memories"""
        # Semantic search + structured filtering

    def reflect(self, scope: str = "recent"):
        """Consolidate memories"""
        # Identify patterns
        # Update beliefs
        # Create summaries
```

**2. Integration Points**

- **Session Start**: Load relevant memories into context
- **During Session**: Continuously retain thoughts/decisions
- **Session End**: Reflect and consolidate
- **Task Completion**: Update task with key memories

**3. BB5-Specific Adaptations**

- Link memories to goals/plans/tasks
- Respect BB5 hierarchy
- Integrate with existing run structure
- Add memory hooks to bb5 commands

---

## 4. Implementation Plan

### Phase 1: Research and Design (Completed)

**Status:** Done

**Deliverables:**
- [x] Research Hindsight, Mem0, Zep, Letta, memU
- [x] Analyze Two Buffers theory
- [x] Design hybrid architecture
- [x] Create goal/plan/task hierarchy (IG-008, PLAN-HINDSIGHT-001)

### Phase 2: Foundation Implementation (4-6 hours)

**Sub-tasks:**
1. **TASK-HINDSIGHT-001**: Establish 4-Network Memory Foundation
   - Create memory system classes
   - Implement basic RETAIN/RECALL/REFLECT
   - Add vector store integration

2. **TASK-HINDSIGHT-002**: Build Memory Infrastructure
   - Set up ChromaDB or similar
   - Create structured store schema
   - Add migration from existing files

### Phase 3: Core Operations (6-8 hours)

**Sub-tasks:**
1. **TASK-HINDSIGHT-003**: Implement RETAIN Operation
   - Auto-retain from THOUGHTS.md, DECISIONS.md
   - Metadata extraction
   - Embedding generation

2. **TASK-HINDSIGHT-004**: Implement RECALL Operation
   - Semantic search
   - Structured filtering
   - Context injection

3. **TASK-HINDSIGHT-005**: Implement REFLECT Operation
   - Pattern identification
   - Belief updating
   - Summary generation

### Phase 4: Integration and Validation (4-6 hours)

**Sub-task:**
1. **TASK-HINDSIGHT-006**: Integrate and Validate
   - Hook into session start/end
   - Integrate with RALF workflow
   - Benchmark performance
   - Validate against baseline

---

## 5. Success Criteria

### Research Phase (Completed)
- [x] Research and document leading memory systems
- [x] Analyze Two Buffers theory
- [x] Design hybrid memory architecture
- [x] Create goal/plan/task hierarchy

### Implementation Phase
- [ ] Core memory layer implemented
- [ ] Vector store integrated
- [ ] Structured store working
- [ ] RETAIN operation functional
- [ ] RECALL operation functional
- [ ] REFLECT operation functional
- [ ] RALF integration complete
- [ ] Benchmarks show improvement

### Validation
- [ ] Semantic search returns relevant results
- [ ] Memory retrieval improves task performance
- [ ] Token usage reduced vs full file reads
- [ ] Pattern recognition identifies repeated issues
- [ ] Backward compatibility maintained

---

## 6. Estimated Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Phase 1: Research | 1 day | Completed |
| Phase 2: Foundation | 1 day | In Progress |
| Phase 3: Core Operations | 1-2 days | Pending |
| Phase 4: Integration | 1 day | Pending |
| **Total** | **4-5 days** | **20% Complete** |

---

## 7. Rollback Strategy

**Keep existing file-based memory as fallback:**
- Implement new system as opt-in layer
- Maintain THOUGHTS.md/DECISIONS.md format
- Can disable memory layer via config

**Recovery:**
```bash
# Disable memory layer
export BB5_MEMORY_ENABLED=false

# Fall back to file-only mode
```

---

## 8. Files to Modify/Create

### New Files

| File | Purpose |
|------|---------|
| `lib/memory/core.py` | Core memory system |
| `lib/memory/retain.py` | RETAIN operation |
| `lib/memory/recall.py` | RECALL operation |
| `lib/memory/reflect.py` | REFLECT operation |
| `lib/memory/vector_store.py` | Vector DB interface |
| `lib/memory/structured_store.py` | Structured DB interface |
| `.autonomous/memory/config.yaml` | Memory configuration |

### Modified Files

| File | Changes |
|------|---------|
| `bb5` CLI | Add memory commands |
| Session start hook | Load relevant memories |
| Session end hook | Trigger reflection |

---

## 9. Related Resources

- **Hindsight Paper:** arXiv:2512.12818
- **Hindsight GitHub:** https://github.com/vectorize-io/hindsight
- **Mem0:** https://mem0.ai
- **Zep:** https://www.getzep.com
- **Letta:** https://www.letta.com
- **memU:** https://memu.pro
- **Moltbook Discussion:** m/emergence - "The Two Buffers"

---

*Plan created: 2026-02-06*
*Research complete, implementation in progress*
