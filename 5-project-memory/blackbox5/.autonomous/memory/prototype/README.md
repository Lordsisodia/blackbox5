# Hindsight Memory Prototypes

**Location:** `.autonomous/memory/prototype/`
**Purpose:** Demonstrate RETAIN and RECALL operations without full infrastructure
**Status:** Working prototypes for Phase 1 validation

---

## Overview

These prototypes demonstrate the core Hindsight memory operations using rule-based extraction and simple keyword matching. They validate the extraction pipeline design before investing in full LLM-based extraction and vector database setup.

---

## Prototypes

### 1. RETAIN (`retain.py`)

Extracts structured memories from markdown files (tasks, runs, thoughts, decisions).

**What it does:**
- Parses markdown structure (frontmatter, sections)
- Extracts 4 network types:
  - **World:** Objectives, decisions
  - **Experience:** Approaches, actions
  - **Opinion:** Insights, beliefs
  - **Observation:** Success criteria, summaries
- Extracts entities (capitalized terms, code, paths)
- Outputs JSON for each network

**Usage:**
```bash
# Process single file
python retain.py --source tasks/active/TASK-XXX/task.md --output ./memories

# Process directory
python retain.py --source runs/unknown/completed/run-XXX/ --output ./memories
```

**Output:**
```
memories/
├── world_memories.json       # Facts
├── experience_memories.json  # Actions
├── opinion_memories.json     # Beliefs
├── observation_memories.json # Insights
└── all_memories.json         # Combined
```

**Limitations:**
- Rule-based (not LLM-based)
- No embeddings generated
- Simple entity extraction
- No PostgreSQL/Neo4j storage

**Full implementation will:**
- Use LLM for extraction (GPT-4 with structured output)
- Generate embeddings via OpenAI
- Store in PostgreSQL + pgvector
- Create Neo4j entity graph
- Run automatically on task completion

---

### 2. RECALL (`recall.py`)

Multi-strategy retrieval system for querying extracted memories.

**What it does:**
- Loads memories from JSON files
- Implements 3 search strategies:
  - **Semantic:** Jaccard similarity (placeholder for vector search)
  - **Keyword:** BM25-style scoring (placeholder for full-text search)
  - **Temporal:** Recency weighting
- Merges results with Reciprocal Rank Fusion (RRF)
- Filters by network type

**Usage:**
```bash
# Basic search
python recall.py --query "authentication patterns" --memories ./memories

# Filter by network
python recall.py --query "Hindsight" --network observation --memories ./memories

# Use specific strategies
python recall.py --query "vector database" --strategies semantic keyword temporal
```

**Output:**
```
============================================================
RECALL RESULTS (5 memories)
============================================================

1. [rrf_merged] Score: 0.033
   Network: OBSERVATION
   Confidence: 0.85
   Source: tasks/active/TASK-XXX/task.md
   Content: Success criterion: Design hybrid memory architecture...
   Entities: Design, Hindsight
```

**Limitations:**
- Keyword-based semantic search (not vector similarity)
- BM25 approximation (not PostgreSQL full-text)
- No graph traversal
- File-based storage (not database)

**Full implementation will:**
- Use pgvector for cosine similarity
- Use PostgreSQL tsvector for full-text search
- Use Neo4j for entity graph traversal
- Support complex filters and aggregations
- Return results in <500ms

---

## Relationship to Full Implementation

```
┌─────────────────────────────────────────────────────────────┐
│                    PROTOTYPE → PRODUCTION                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  RETAIN Prototype          →  RETAIN Production             │
│  ├─ Rule-based extraction  →  LLM-based extraction          │
│  ├─ No embeddings          →  OpenAI text-embedding-3-small │
│  ├─ File output            →  PostgreSQL + Neo4j            │
│  └─ Manual trigger         →  Auto-trigger on task complete │
│                                                              │
│  RECALL Prototype          →  RECALL Production             │
│  ├─ Keyword similarity     →  pgvector cosine similarity    │
│  ├─ BM25 approximation     →  PostgreSQL full-text search   │
│  ├─ No graph search        →  Neo4j entity traversal        │
│  └─ File-based             →  Database query                │
│                                                              │
│  Storage: JSON files       →  Production storage            │
│  ├─ world_memories.json    →  memory_contents table         │
│  ├─ experience_memories... →  with vector column            │
│  ├─ opinion_memories...    →  memory_entities table         │
│  └─ observation_memories.. →  memory_opinions table         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Testing the Prototypes

### Quick Start

```bash
# 1. Extract memories from a task
python retain.py \
  --source ../../tasks/active/TASK-MEMORY-001-improve-persistent-memory/TASK.md \
  --output ./output

# 2. Query the extracted memories
python recall.py --query "Hindsight architecture" --memories ./output

# 3. Filter by network
python recall.py --query "memory systems" --network observation --memories ./output
```

### Batch Processing

```bash
# Extract from all completed runs
python retain.py \
  --source ../../runs/unknown/completed/ \
  --output ./batch_output

# Query all extracted memories
python recall.py --query "agent patterns" --memories ./batch_output --limit 10
```

---

## Validation Checklist

These prototypes validate:

- [x] Memory extraction from markdown structure
- [x] 4-network classification (World/Experience/Opinion/Observation)
- [x] Entity extraction
- [x] Multi-strategy retrieval
- [x] RRF merging
- [x] Network filtering
- [x] JSON output format

Still needed for production:
- [ ] LLM-based extraction
- [ ] Embedding generation
- [ ] PostgreSQL + pgvector storage
- [ ] Neo4j entity graph
- [ ] Sub-500ms query latency
- [ ] Automatic triggering
- [ ] SessionStart integration

---

## Next Steps

1. **Test on more data:** Run RETAIN on all historical tasks/runs
2. **Validate extraction quality:** Review extracted memories manually
3. **Tune RRF weights:** Adjust k parameter for merging
4. **Design LLM prompts:** Create structured extraction prompts
5. **Plan database schema:** Design PostgreSQL/Neo4j tables

---

## Files

```
prototype/
├── README.md              # This file
├── retain.py              # RETAIN operation prototype
├── recall.py              # RECALL operation prototype
└── output/                # Example output (gitignored)
    ├── world_memories.json
    ├── experience_memories.json
    ├── opinion_memories.json
    ├── observation_memories.json
    └── all_memories.json
```

---

## References

- **Goal:** `goals/active/IG-008/`
- **Plan:** `plans/active/hindsight-memory-implementation/`
- **Research:** `knowledge/research/agent-memory-systems/`
- **Integration:** `plans/active/hindsight-memory-implementation/INTEGRATION.md`
