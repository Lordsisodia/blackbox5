# BB5 Hindsight Memory Hooks - Research Report

**Date:** 2026-02-06
**Researcher:** Memory Systems Engineer
**Goal:** IG-008 - Hindsight Memory Architecture

---

## Executive Summary

This document analyzes the hook requirements for BB5's Hindsight memory architecture (RETAIN/RECALL/REFLECT operations). It identifies what hooks are needed, when they should fire, and how memories flow through the 3-layer memory system.

**Key Finding:** BB5 needs 12+ hooks across 4 lifecycle phases to fully implement the Hindsight memory architecture.

---

## 1. Memory Architecture Overview

### 1.1 The 4-Network Memory System

| Network | File | Epistemic Type | Stores |
|---------|------|----------------|--------|
| **World (W)** | `FACTS.md` | "What is true?" | Objective facts, entities, relationships |
| **Experience (B)** | `EXPERIENCES.md` | "What did I do?" | First-person actions, learning moments |
| **Opinion (O)** | `OPINIONS.md` | "What do I believe?" | Beliefs with confidence scores |
| **Observation (S)** | `OBSERVATIONS.md` | "What does it mean?" | Synthesized insights, patterns |

### 1.2 The 3-Core Operations

| Operation | Purpose | Trigger |
|-----------|---------|---------|
| **RETAIN** | Extract and store memories | Task completion, file changes |
| **RECALL** | Retrieve relevant memories | Session start, context loading |
| **REFLECT** | Detect conflicts and patterns | Periodic, on-demand, or threshold-based |

### 1.3 The 3-Layer Memory Hierarchy

```
Layer 3: Vector Store (PostgreSQL/pgvector)
    ↑ RETAIN writes here
    ↓ RECALL reads from here

Layer 2: Markdown Files (FACTS.md, EXPERIENCES.md, etc.)
    ↑ Populated by RETAIN extraction
    ↓ Read by humans and REFLECT

Layer 1: Working Memory (THOUGHTS.md, DECISIONS.md, RESULTS.md)
    ↑ Written during task execution
    ↓ Processed by RETAIN on completion
```

---

## 2. RETAIN Hooks (Memory Extraction)

### 2.1 When Should RETAIN Fire?

RETAIN extracts learnings from completed work. It should fire:

1. **On Task Completion** - Primary trigger
2. **On Run Completion** - Extract from THOUGHTS.md, DECISIONS.md, RESULTS.md
3. **On File Save** - For continuous capture (optional)
4. **On Demand** - Manual invocation via CLI
5. **Batch/Backfill** - Process historical tasks

### 2.2 Existing RETAIN Implementation

**File:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/hooks/retain-on-complete.py`

```python
# Current implementation processes:
# - DECISIONS.md → Facts + Opinions
# - THOUGHTS.md → Experiences
# - RESULTS.md → Observations
# - LEARNINGS.md → Observations

async def retain_from_run(run_dir: Path, task_id: str = None):
    """Extract memories from a completed run"""
    files_to_process = [
        "DECISIONS.md",
        "THOUGHTS.md",
        "RESULTS.md",
        "LEARNINGS.md"
    ]
    # Uses LLM (gpt-4o-mini) for extraction
    # Stores in vector store with embeddings
```

### 2.3 Required RETAIN Hooks

| Hook Name | Event | Purpose | Status |
|-----------|-------|---------|--------|
| `retain-on-task-complete` | Task completion | Extract from task files | ✅ Implemented |
| `retain-on-run-complete` | Run finalization | Extract from run docs | ✅ Implemented |
| `retain-on-file-save` | File write (optional) | Continuous capture | 📝 Needed |
| `retain-batch-backfill` | Manual/scheduled | Process historical data | 📝 Needed |
| `retain-on-decision` | Decision recorded | Immediate fact extraction | 📝 Needed |

### 2.4 RETAIN Hook Flow

```
Task/Run Completion
    ↓
retain-on-complete.py
    ↓
├─ Read THOUGHTS.md → Extract experiences
├─ Read DECISIONS.md → Extract facts + opinions
├─ Read RESULTS.md → Extract observations
└─ Read LEARNINGS.md → Extract observations
    ↓
LLM Extraction (gpt-4o-mini)
    ↓
├─ Generate embeddings (OpenAI text-embedding-3-small)
├─ Store in vector_store.py
└─ Update FACTS.md, EXPERIENCES.md, OPINIONS.md, OBSERVATIONS.md
    ↓
Vector Store (JSON + in-memory)
    ↓
Future: PostgreSQL + pgvector
```

---

## 3. RECALL Hooks (Memory Injection)

### 3.1 When Should RECALL Fire?

RECALL injects relevant context into active sessions. It should fire:

1. **On Session Start** - Load relevant memories for current context
2. **On Task Switch** - Load memories for new task
3. **On Context Change** - When project/task changes
4. **On Demand** - Manual search via CLI
5. **Pre-Decision** - Before making significant decisions

### 3.2 Existing RECALL Implementation

**File:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/session_memory_loader.py`

```python
def recall_memories_for_session(project_dir: Path, top_k: int = 5):
    """Recall relevant memories for the current session"""
    # 1. Build search queries from context
    queries = build_search_queries(project_dir)
    #    - Project name
    #    - Active task titles
    #    - Current work context

    # 2. Search vector store
    results = store.search(query, top_k=top_k)

    # 3. Format for AGENT_CONTEXT.md
    return format_memory_context(results)
```

**File:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/research-pipeline/.claude/hooks/session-start-timeline-memory.sh`

```bash
# Existing SessionStart hook for research pipeline
# Injects timeline-memory.md into agent context
# Could be extended to include Hindsight memories
```

### 3.3 Required RECALL Hooks

| Hook Name | Event | Purpose | Status |
|-----------|-------|---------|--------|
| `recall-on-session-start` | SessionStart | Inject relevant memories | 📝 Partial (timeline only) |
| `recall-on-task-load` | Task navigation | Load task-specific memories | 📝 Needed |
| `recall-pre-decision` | Before major decisions | Surface relevant precedents | 📝 Needed |
| `recall-on-search` | User query | Semantic memory search | ✅ Implemented (CLI) |
| `recall-context-window` | 70% context usage | Summarize and inject | 📝 Needed |

### 3.4 RECALL Hook Flow

```
Session Start / Task Load
    ↓
session_memory_loader.py
    ↓
├─ Detect active tasks (tasks/active/)
├─ Extract context terms (task titles, project name)
└─ Build search queries
    ↓
Vector Store Search
    ↓
├─ Semantic search (cosine similarity)
├─ Filter by network (optional)
└─ Rank by relevance score
    ↓
Format for Injection
    ↓
├─ Group by network (World/Experience/Opinion/Observation)
├─ Include confidence scores
└─ Truncate to fit context window
    ↓
Inject into AGENT_CONTEXT.md
    ↓
Agent has relevant memories available
```

---

## 4. REFLECT Hooks (Conflict Detection)

### 4.1 When Should REFLECT Fire?

REFLECT detects conflicts and synthesizes insights. It should fire:

1. **On Memory Threshold** - When N new memories added
2. **On Schedule** - Periodic (daily/weekly) consolidation
3. **On Demand** - Manual invocation
4. **On Contradiction Detected** - Immediate when conflicts found
5. **Pre-Commit** - Before major decisions

### 4.2 Existing REFLECT Implementation

**File:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/operations/reflect.py`

```python
class ReflectEngine:
    async def reflect(self, network: Optional[str] = None, dry_run: bool = True):
        # Phase 1: Detect contradictions (LLM-based)
        contradictions = await self._detect_contradictions(memories)

        # Phase 2: Identify patterns
        patterns = await self._identify_patterns(memories)

        # Phase 3: Synthesize new insights
        new_insights = await self._synthesize_insights(memories, patterns)

        # Phase 4: Update confidences (if not dry-run)
        updates = await self._update_confidences(memories)
```

### 4.3 Required REFLECT Hooks

| Hook Name | Event | Purpose | Status |
|-----------|-------|---------|--------|
| `reflect-on-threshold` | N new memories | Periodic consolidation | 📝 Needed |
| `reflect-on-schedule` | Cron/timer | Daily/weekly reflection | 📝 Needed |
| `reflect-on-demand` | Manual CLI | User-triggered reflection | ✅ Implemented |
| `reflect-pre-commit` | Before major changes | Validate beliefs | 📝 Needed |
| `reflect-post-retain` | After batch extraction | Immediate consolidation | 📝 Needed |

### 4.4 REFLECT Hook Flow

```
Trigger (threshold/schedule/manual)
    ↓
reflect.py
    ↓
[Phase 1] Detect Contradictions
    ↓
├─ Focus on Opinion network
├─ Use LLM to compare beliefs
└─ Identify logical conflicts
    ↓
[Phase 2] Identify Patterns
    ↓
├─ Group by network
├─ Find recurring themes
└─ Detect trends
    ↓
[Phase 3] Synthesize Insights
    ↓
├─ Create new Observation memories
├─ Link to supporting evidence
└─ Store in vector store
    ↓
[Phase 4] Update Confidences
    ↓
├─ Reduce confidence for contradicted beliefs
├─ Increase confidence for reinforced beliefs
└─ Save changes
    ↓
Generate reflection report
```

---

## 5. Memory Lifecycle Management Hooks

### 5.1 Memory State Transitions

```
┌─────────────┐    RETAIN     ┌─────────────┐    RECALL     ┌─────────────┐
│   Working   │ ─────────────→│   Stored    │ ─────────────→│   Active    │
│   Memory    │               │   Memory    │               │   Context   │
│  (Layer 1)  │               │  (Layer 2)  │               │  (Layer 3)  │
└─────────────┘               └─────────────┘               └─────────────┘
       ↑                            │                              │
       └────────────────────────────┘                              │
              REFLECT (consolidation)                              │
                                                                   ↓
                                                            ┌─────────────┐
                                                            │   Applied   │
                                                            │   Memory    │
                                                            │  (Usage)    │
                                                            └─────────────┘
```

### 5.2 Required Lifecycle Hooks

| Hook Name | Event | Purpose | Priority |
|-----------|-------|---------|----------|
| `memory-init` | Project initialization | Create memory infrastructure | High |
| `memory-backup` | Periodic/Pre-commit | Backup memory store | Medium |
| `memory-cleanup` | Schedule | Remove duplicates, decay old memories | Medium |
| `memory-export` | Manual/Schedule | Export for migration/analysis | Low |
| `memory-import` | Manual | Import from other sources | Low |
| `memory-stats` | On demand | Report memory statistics | Low |

---

## 6. Hook Integration Matrix

### 6.1 Claude Code Hook Events

| Claude Event | Memory Hook | Purpose |
|--------------|-------------|---------|
| **SessionStart** | `recall-on-session-start` | Inject relevant memories |
| **PreToolUse** | `retain-on-decision` | Capture decision context |
| **PostToolUse** | `retain-on-file-save` | Capture file changes |
| **Stop** | `retain-on-run-complete` | Finalize memory extraction |
| **PreCommit** | `reflect-pre-commit` | Validate beliefs |

### 6.2 RALF Integration Points

| RALF Phase | Memory Hook | Purpose |
|------------|-------------|---------|
| **Task Start** | `recall-on-task-load` | Load task memories |
| **Task Complete** | `retain-on-task-complete` | Extract learnings |
| **Run Complete** | `retain-on-run-complete` | Extract from run docs |
| **Loop Iteration** | `reflect-on-threshold` | Periodic consolidation |
| **Agent Handoff** | `recall-context-handoff` | Pass memory context |

---

## 7. Implementation Roadmap

### 7.1 Phase 1: Core Hooks (Completed ✅)

- [x] `retain-on-complete.py` - Task/run completion extraction
- [x] `session_memory_loader.py` - Session start memory loading
- [x] `reflect.py` - Belief consolidation (manual)
- [x] Vector store with JSON persistence
- [x] CLI interface (`bb5-memory`)

### 7.2 Phase 2: Integration Hooks (Next)

- [ ] `recall-on-session-start` - Full SessionStart integration
- [ ] `retain-on-decision` - Decision capture hook
- [ ] `reflect-on-threshold` - Automated reflection
- [ ] `memory-init` - Project setup hook

### 7.3 Phase 3: Advanced Hooks (Future)

- [ ] `retain-on-file-save` - Continuous capture
- [ ] `recall-pre-decision` - Decision support
- [ ] `reflect-on-schedule` - Cron-based reflection
- [ ] `memory-cleanup` - Maintenance hooks
- [ ] Cross-task pattern detection
- [ ] Memory decay and archiving

---

## 8. Memory Flow Examples

### 8.1 Example 1: Task Completion Flow

```
Agent completes TASK-001
    ↓
THOUGHTS.md written with reasoning
DECISIONS.md written with choices
RESULTS.md written with outcomes
    ↓
retain-on-complete.py fires
    ↓
LLM extracts:
  - Experience: "Implemented JWT middleware"
  - Fact: "JWT tokens have 3 parts"
  - Opinion: "JWT preferred for APIs (0.75 confidence)"
  - Observation: "Stateless auth better for microservices"
    ↓
Stored in vector store with embeddings
    ↓
FACTS.md, EXPERIENCES.md, OPINIONS.md, OBSERVATIONS.md updated
```

### 8.2 Example 2: Session Start Flow

```
New Claude session starts
    ↓
session_memory_loader.py runs
    ↓
Detects active tasks: TASK-002, TASK-003
    ↓
Builds queries: ["blackbox5", "memory architecture", "hooks"]
    ↓
Searches vector store
    ↓
Finds relevant memories:
  - [WORLD] "JWT has 3 parts" (score: 0.92)
  - [OPINION] "JWT preferred for APIs" (score: 0.85)
  - [EXPERIENCE] "Implemented auth middleware" (score: 0.78)
    ↓
Formats for AGENT_CONTEXT.md
    ↓
Agent has context: "Previously I believed JWT is preferred..."
```

### 8.3 Example 3: Reflection Flow

```
50 new memories added (threshold reached)
    ↓
reflect-on-threshold fires
    ↓
Analyzes Opinion network
    ↓
Detects contradiction:
  - O-001: "JWT is best for APIs" (0.8 confidence)
  - O-023: "Session cookies better for APIs" (0.7 confidence)
    ↓
Suggests resolution:
  - "JWT better for stateless/microservices"
  - "Sessions better for server-rendered"
    ↓
Creates new Observation:
  - "Auth choice depends on architecture"
    ↓
Reduces confidence of contradictory opinions
    ↓
Updates vector store
```

---

## 9. Key Files Reference

| File | Purpose |
|------|---------|
| `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/hooks/retain-on-complete.py` | Task completion extraction |
| `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/session_memory_loader.py` | Session start memory loading |
| `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/operations/retain.py` | RETAIN operation engine |
| `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/operations/recall.py` | RECALL operation engine |
| `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/operations/reflect.py` | REFLECT operation engine |
| `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/vector_store.py` | Vector storage with embeddings |
| `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/models/memory.py` | Data models (Memory, Entity, Relationship) |
| `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/cli.py` | Unified CLI interface |
| `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.templates/memory/FACTS.md` | World network template |
| `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.templates/memory/EXPERIENCES.md` | Experience network template |
| `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.templates/memory/OPINIONS.md` | Opinion network template |
| `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.templates/memory/OBSERVATIONS.md` | Observation network template |

---

## 10. Open Questions

1. **Hook Trigger Thresholds:** What N should trigger `reflect-on-threshold`? (10? 50? 100?)

2. **Memory Decay:** Should old memories lose relevance over time? How to implement?

3. **Deduplication:** How to prevent duplicate memories from multiple RETAIN runs?

4. **Context Window Management:** At what context usage % should we summarize vs. inject?

5. **Cross-Project Memory:** Should memories be shared across BB5 projects?

6. **Privacy:** Should certain memories be marked private/excluded from storage?

7. **Embedding Costs:** How to balance embedding quality vs. API costs at scale?

---

## 11. Recommendations

### Immediate (Next 2 Weeks)

1. **Implement `recall-on-session-start` hook** - Integrate with Claude Code SessionStart
2. **Add `reflect-on-threshold` trigger** - Auto-run REFLECT every 20 new memories
3. **Create `memory-init` project setup** - Auto-create memory files for new tasks

### Short Term (Next Month)

4. **Add `retain-on-decision` hook** - Capture decisions as they're made
5. **Implement memory deduplication** - Prevent duplicate entries
6. **Create memory dashboard** - Visual overview of memory health

### Long Term (Next Quarter)

7. **Cross-task pattern detection** - Find patterns across multiple tasks
8. **Memory decay implementation** - Age out old/irrelevant memories
9. **PostgreSQL migration** - Move from JSON to proper vector database
10. **Neo4j graph integration** - Store entity relationships in graph DB

---

*End of Research Report*
