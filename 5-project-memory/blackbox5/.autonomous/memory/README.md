# BB5 Project Memory System

**Location:** `.autonomous/memory/`

The BB5 Project Memory System implements the Hindsight Memory Architecture for persistent knowledge storage and retrieval across sessions.

---

## Overview

This memory system uses a 4-network architecture to organize knowledge:

| Network | Purpose | Storage |
|---------|---------|---------|
| **World** | Objective facts about technologies, systems, codebase | `data/memories.json` |
| **Experience** | First-person actions and outcomes | `data/memories.json` |
| **Opinion** | Beliefs with confidence levels | `data/memories.json` |
| **Observation** | Synthesized insights and patterns | `data/memories.json` |

---

## Directory Structure

```
.autonomous/memory/
├── README.md                    # This file
├── IMPLEMENTATION_STATUS.md     # Implementation progress tracking
├── VECTOR_STORE_SUMMARY.md      # Vector store documentation
├── DATABASE_MIGRATION_TASK.md   # Database migration plan
├── cli.py                       # Memory CLI commands
├── session_memory_loader.py     # Session memory loading
├── vector_store.py              # Vector store implementation
├── models/
│   └── memory.py               # Data models (Memory, Entity, Relationship)
├── operations/
│   ├── retain.py               # RETAIN operation - store memories
│   ├── recall.py               # RECALL operation - retrieve memories
│   └── reflect.py              # REFLECT operation - analyze patterns
├── extraction/
│   ├── learning_extractor.py   # Extract learnings from runs
│   ├── backfill_learnings.py   # Backfill historical runs
│   ├── check_learning_index.py # Health check for learning index
│   └── README.md               # Extraction module docs
├── hooks/
│   ├── retain-on-complete.py   # Auto-retain on task completion
│   ├── log-skill-on-complete.py # Skill logging hook
│   └── task_completion_skill_recorder.py # Skill recorder
├── prompts/
│   └── retain_extraction.py    # LLM prompts for extraction
├── prototype/
│   ├── retain.py               # Prototype RETAIN
│   ├── recall.py               # Prototype RECALL
│   └── README.md               # Prototype docs
├── data/
│   ├── memories.json           # Stored memories
│   ├── memories.msgpack        # Binary memory format
│   └── .embedding_cache.json   # Embedding cache
├── decisions/
│   └── registry.md             # Decision registry (deprecated)
└── chat-logs/                  # Chat log storage
    └── *.jsonl                 # Chat log files
```

---

## Core Operations

### RETAIN
Store new memories from task completions.

**Usage:**
```python
from operations.retain import retain_memories

memories = retain_memories(content, source_id="TASK-001")
```

### RECALL
Retrieve relevant memories using semantic search.

**Usage:**
```python
from operations.recall import recall_memories

results = recall_memories(query="database connection", limit=5)
```

### REFLECT
Analyze memory patterns and generate insights.

**Usage:**
```python
from operations.reflect import reflect_on_memories

insights = reflect_on_memories(timeframe="7d")
```

---

## Learning Extraction

The learning extraction module automatically extracts structured learnings from task runs.

**Key Files:**
- `extraction/learning_extractor.py` - Core extraction logic
- `extraction/backfill_learnings.py` - Historical backfill
- `extraction/check_learning_index.py` - Health monitoring

**Index Location:**
```
.autonomous/memory/insights/learning-index.yaml
```

---

## Integration Points

### Task Completion Hook
The `retain-on-complete.py` hook automatically:
1. Extracts learnings from THOUGHTS.md, DECISIONS.md, RESULTS.md
2. Stores memories in the vector store
3. Updates the learning index

### Session Start
The `session_memory_loader.py` loads relevant memories at session start based on current context.

---

## Data Models

### Memory
```python
class Memory:
    id: str                    # Unique identifier
    content: str               # Memory content
    network: Network           # World|Experience|Opinion|Observation
    embedding: List[float]     # Vector embedding
    entities: List[Entity]     # Related entities
    relationships: List[Relationship]  # Entity relationships
    metadata: Dict             # Additional metadata
    timestamp: datetime        # Creation time
    source_id: str            # Source task/run ID
```

### Entity
```python
class Entity:
    name: str                  # Entity name
    type: str                  # Entity type (person, tech, concept)
    mentions: int             # Mention count
```

### Relationship
```python
class Relationship:
    source: str               # Source entity
    target: str               # Target entity
    type: str                 # Relationship type
```

---

## Configuration

Environment variables for memory system:

```bash
# OpenAI (for embeddings and extraction)
OPENAI_API_KEY=sk-...

# Database (future)
DATABASE_URL=postgresql://...
NEO4J_URI=bolt://...
```

---

## Usage Examples

### Extract from Single Run
```bash
python extraction/learning_extractor.py --run-dir /path/to/run-0001
```

### Backfill All Historical Runs
```bash
python extraction/backfill_learnings.py
```

### Health Check
```bash
python extraction/check_learning_index.py
```

### Query Memories
```bash
python cli.py recall "database optimization"
```

---

## Status

**Phase 1 (Foundation):** 80% Complete

- [x] 4-network templates
- [x] Data models
- [x] RETAIN operation
- [x] Learning extraction
- [ ] RECALL operation (partial)
- [ ] SessionStart integration
- [ ] Database storage

---

## References

- **Goal:** `goals/active/IG-008/`
- **Plan:** `plans/active/hindsight-memory-implementation/`
- **Architecture:** `DUAL-RALF-ARCHITECTURE.md`
