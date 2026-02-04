# Blackbox5 Hindsight Integration Action Plan

**Plan ID:** PLAN-HINDSIGHT-001
**Created:** 2026-02-04
**Status:** Draft
**Priority:** CRITICAL
**Estimated Duration:** 6 weeks
**Owner:** RALF / Agent System

---

## Executive Summary

This action plan details the integration of Hindsight's 4-network memory architecture and 3-core-operations into Blackbox5's existing project memory structure. The integration will enhance BB5's memory system from basic file-based storage to a sophisticated, queryable, and evolving memory substrate.

**Key Integration Points:**
- Add Hindsight's 4 networks (World, Experience, Opinion, Observation) as new file types
- Implement RETAIN/RECALL/REFLECT operations as automated pipelines
- Leverage existing PostgreSQL (add pgvector) and Neo4j infrastructure
- Maintain backward compatibility with existing THOUGHTS.md/DECISIONS.md structure

---

## Current Architecture Understanding

### Blackbox5 Memory Hierarchy

```
GOALS → PLANS → TASKS → RUNS
  ↓       ↓       ↓       ↓
Journal  Research Timeline  Agent Sessions
```

**Per-Task Memory Files:**
```
tasks/active/TASK-XXX/
├── task.md              # Specification
├── THOUGHTS.md          # Reasoning
├── DECISIONS.md         # Decisions
├── LEARNINGS.md         # Insights
├── RESULTS.md           # Outcomes
├── ASSUMPTIONS.md       # Validated assumptions
├── timeline/            # Daily progress
├── subtasks/            # Child tasks
└── artifacts/           # Generated files
```

**Per-Run Memory Files:**
```
.autonomous/agents/{planner|executor|architect}/runs/run-XXXX/
├── metadata.yaml        # Loop metadata
├── THOUGHTS.md          # Agent analysis
├── DECISIONS.md         # Decisions made
└── RESULTS.md           # Outcomes
```

**Existing Infrastructure:**
- PostgreSQL (TaskRegistry)
- Neo4j (for RAPS concept graph)
- Redis (agent coordination)
- File system (markdown files)

---

## Phase 1: Foundation - Add 4-Network File Structure

**Duration:** Week 1
**Priority:** CRITICAL
**Dependencies:** None

### 1.1 Create New Memory File Templates

**Location:** `.templates/memory/`

#### FACTS.md (World Network)
```markdown
# FACTS: {Task/Run Name}
**Created:** YYYY-MM-DD
**Source:** {THOUGHTS.md|DECISIONS.md|LEARNINGS.md}

## Entities

### {Entity Name} ({Entity Type})
- **Current State:** {fact}
- **Valid From:** {date}
- **Valid Until:** {date|null}
- **Source:** {DEC-XXX|THOUGHT-XXX}
- **Confidence:** 0.XX

## Relationships

- {Entity A} → {relationship} → {Entity B}
  - **Established:** {date}
  - **Source:** {reference}
```

#### EXPERIENCES.md (Experience Network)
```markdown
# EXPERIENCES: {Task/Run Name}
**Created:** YYYY-MM-DD

## EXP-XXX: {Experience Title}

**Date:** YYYY-MM-DD
**Agent:** {planner|executor|architect|unknown}
**Type:** {action|observation|decision}

**Description:**
{First-person description of what was done}

**Related Entities:**
- {Entity 1}
- {Entity 2}

**Links:**
- World: {FACT-XXX}
- Opinion: {OP-XXX}
- Decision: {DEC-XXX}
```

#### OPINIONS.md (Opinion Network)
```markdown
# OPINIONS: {Task/Run Name}
**Created:** YYYY-MM-DD

## OP-XXX: {Opinion Statement}

**Formed:** YYYY-MM-DD
**Confidence:** 0.XX
**Status:** {active|revised|deprecated}

**Belief:**
{Clear statement of belief/opinion}

**Evidence For:**
- {evidence 1}
- {evidence 2}

**Evidence Against:**
- {evidence 1}

**Updates:**
- YYYY-MM-DD: Initial confidence 0.XX
- YYYY-MM-DD: Revised to 0.XX (reason)

**Related:**
- Contradicts: {OP-YYY}
- Supports: {OP-ZZZ}
```

#### OBSERVATIONS.md (Observation Network)
```markdown
# OBSERVATIONS: {Task/Run Name}
**Created:** YYYY-MM-DD
**Synthesized From:** {list of sources}

## OBS-XXX: {Observation Title}

**Last Updated:** YYYY-MM-DD
**Update Count:** {N}

**Observation:**
{Neutral, synthesized summary}

**Sources:**
- {source 1}
- {source 2}

**Pattern Strength:** {high|medium|low}
**Contradictions:** {none|listed}
```

### 1.2 Update Task Template

**Location:** `.templates/task/`

Add to task folder structure:
```
tasks/active/TASK-XXX/
├── task.md              # (existing)
├── THOUGHTS.md          # (existing)
├── DECISIONS.md         # (existing)
├── LEARNINGS.md         # (existing)
├── RESULTS.md           # (existing)
├── ASSUMPTIONS.md       # (existing)
├── FACTS.md            # NEW
├── EXPERIENCES.md      # NEW
├── OPINIONS.md         # NEW
├── OBSERVATIONS.md     # NEW
├── entities/           # NEW
│   └── {entity-name}.md
├── timeline/           # (existing)
├── subtasks/           # (existing)
└── artifacts/          # (existing)
```

### 1.3 Update Run Template

**Location:** `.templates/run/`

Add to run folder structure:
```
.autonomous/agents/{agent}/runs/run-XXXX/
├── metadata.yaml       # (existing)
├── THOUGHTS.md         # (existing)
├── DECISIONS.md        # (existing)
├── RESULTS.md          # (existing)
├── FACTS.md           # NEW
├── EXPERIENCES.md     # NEW
├── OPINIONS.md        # NEW
├── OBSERVATIONS.md    # NEW
└── entities/          # NEW
    └── {entity-name}.md
```

### 1.4 Create Project-Level Memory Structure

**Location:** `.autonomous/memory/`

```
.autonomous/memory/
├── world/              # Global facts (World Network)
│   ├── entities/       # Entity definitions
│   ├── facts.yaml      # Fact database
│   └── index.yaml      # Entity index
├── experiences/        # Cross-run experiences
│   ├── by-date/        # Chronological
│   ├── by-entity/      # Entity-linked
│   └── index.yaml
├── opinions/           # Evolving beliefs
│   ├── active/         # Current opinions
│   ├── revised/        # Updated opinions
│   └── deprecated/     # Discarded opinions
├── observations/       # Synthesized insights
│   ├── patterns/       # Detected patterns
│   ├── synthesis.md    # Living synthesis doc
│   └── index.yaml
└── graph/              # Neo4j graph data
    ├── schema.cypher   # Graph schema
    ├── entities.cypher # Entity nodes
    └── relationships/  # Relationship definitions
```

### Phase 1 Deliverables

- [ ] 4 new memory file templates created
- [ ] Task template updated
- [ ] Run template updated
- [ ] Project-level memory structure created
- [ ] Documentation written

### Phase 1 Success Criteria

- Templates are usable
- Structure is clear
- Documentation is complete
- Backward compatibility maintained

---

## Phase 2: Infrastructure - Database Setup

**Duration:** Week 2
**Priority:** CRITICAL
**Dependencies:** Phase 1

### 2.1 PostgreSQL + pgvector Setup

**Purpose:** Enable semantic search across memory files

#### 2.1.1 Install pgvector Extension

```sql
-- Run on PostgreSQL
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify installation
SELECT * FROM pg_extension WHERE extname = 'vector';
```

#### 2.1.2 Create Memory Tables

```sql
-- Memory content table with embeddings
CREATE TABLE memory_contents (
    id SERIAL PRIMARY KEY,
    source_type VARCHAR(50),      -- 'task', 'run', 'goal', 'plan'
    source_id VARCHAR(100),       -- TASK-XXX, run-XXXX
    file_type VARCHAR(50),        -- 'THOUGHTS', 'DECISIONS', 'FACTS', etc.
    content TEXT,                 -- Full content
    content_vector VECTOR(1536),  -- Embedding
    entities JSONB,               -- Extracted entities
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Entity table
CREATE TABLE memory_entities (
    id SERIAL PRIMARY KEY,
    entity_name VARCHAR(200),
    entity_type VARCHAR(100),     -- 'person', 'technology', 'concept', etc.
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    occurrences INTEGER DEFAULT 1,
    related_entities JSONB,
    facts JSONB                   -- Associated facts
);

-- Opinions table with confidence tracking
CREATE TABLE memory_opinions (
    id SERIAL PRIMARY KEY,
    opinion_hash VARCHAR(64),     -- Hash of belief statement
    belief_statement TEXT,
    confidence DECIMAL(3,2),      -- 0.00 to 1.00
    formed_at TIMESTAMP,
    revised_at TIMESTAMP,
    status VARCHAR(20),           -- 'active', 'revised', 'deprecated'
    evidence_for JSONB,
    evidence_against JSONB,
    source_task VARCHAR(100)
);

-- Create indexes
CREATE INDEX idx_memory_source ON memory_contents(source_type, source_id);
CREATE INDEX idx_memory_vector ON memory_contents USING ivfflat (content_vector vector_cosine_ops);
CREATE INDEX idx_memory_entities ON memory_contents USING GIN (entities);
CREATE INDEX idx_entities_name ON memory_entities(entity_name);
CREATE INDEX idx_opinions_hash ON memory_opinions(opinion_hash);
```

#### 2.1.3 Create Embedding Pipeline

**File:** `2-engine/memory/embedder.py`

```python
"""Embedding pipeline for memory content."""

import os
from typing import List, Dict
import openai
from psycopg2.extras import execute_values

class MemoryEmbedder:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "text-embedding-3-small"
        self.dimensions = 1536

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text."""
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=self.dimensions
        )
        return response.data[0].embedding

    def embed_memory_file(self, file_path: str, file_type: str) -> Dict:
        """Process a memory file and generate embedding."""
        with open(file_path, 'r') as f:
            content = f.read()

        embedding = self.embed_text(content)

        return {
            'content': content,
            'embedding': embedding,
            'file_type': file_type,
            'entities': self.extract_entities(content)
        }

    def extract_entities(self, text: str) -> List[str]:
        """Extract entities from text using LLM."""
        # Implementation using LLM call
        pass
```

### 2.2 Neo4j Graph Schema Extension

**Purpose:** Track entity relationships across runs

#### 2.2.1 Extend Existing Schema

**File:** `.autonomous/memory/graph/schema.cypher`

```cypher
// Entity nodes (already exist for RAPS, extend for memory)
CREATE CONSTRAINT entity_name IF NOT EXISTS
FOR (e:Entity) REQUIRE e.name IS UNIQUE;

// Memory-specific node types
CREATE CONSTRAINT fact_id IF NOT EXISTS
FOR (f:Fact) REQUIRE f.id IS UNIQUE;

CREATE CONSTRAINT opinion_id IF NOT EXISTS
FOR (o:Opinion) REQUIRE o.id IS UNIQUE;

CREATE CONSTRAINT experience_id IF NOT EXISTS
FOR (exp:Experience) REQUIRE exp.id IS UNIQUE;

// Memory-specific relationship types
// (:Entity)-[:IS_A]->(:EntityType)
// (:Entity)-[:RELATED_TO]->(:Entity)
// (:Fact)-[:ABOUT]->(:Entity)
// (:Fact)-[:VALID_FROM]->(:Time)
// (:Opinion)-[:ABOUT]->(:Entity)
// (:Opinion)-[:CONTRADICTS]->(:Opinion)
// (:Opinion)-[:SUPPORTS]->(:Opinion)
// (:Experience)-[:INVOLVES]->(:Entity)
// (:Experience)-[:RESULTED_IN]->(:Decision)
```

#### 2.2.2 Create Graph Population Scripts

**File:** `2-engine/memory/graph_populator.py`

```python
"""Populate Neo4j with memory graph data."""

from neo4j import GraphDatabase

class MemoryGraphPopulator:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def add_entity(self, name, entity_type, properties=None):
        """Add or update entity node."""
        with self.driver.session() as session:
            session.run("""
                MERGE (e:Entity {name: $name})
                SET e.type = $type,
                    e.updated = datetime(),
                    e.properties = $props
                RETURN e
            """, name=name, type=entity_type, props=properties or {})

    def add_fact(self, fact_id, statement, entity_name, confidence=1.0):
        """Add fact about entity."""
        with self.driver.session() as session:
            session.run("""
                MATCH (e:Entity {name: $entity})
                CREATE (f:Fact {id: $id, statement: $stmt, confidence: $conf})
                CREATE (f)-[:ABOUT]->(e)
                RETURN f
            """, id=fact_id, stmt=statement, entity=entity_name, conf=confidence)

    def link_opinions(self, opinion1_id, opinion2_id, relationship):
        """Link opinions (CONTRADICTS or SUPPORTS)."""
        with self.driver.session() as session:
            session.run(f"""
                MATCH (o1:Opinion {{id: $id1}})
                MATCH (o2:Opinion {{id: $id2}})
                CREATE (o1)-[:{relationship}]->(o2)
            """, id1=opinion1_id, id2=opinion2_id)
```

### 2.3 Create Memory Configuration

**File:** `.autonomous/memory/config.yaml`

```yaml
memory_system:
  version: "1.0.0"

  # Database connections
  databases:
    postgresql:
      host: "${PG_HOST:localhost}"
      port: "${PG_PORT:5432}"
      database: "${PG_DATABASE:blackbox5}"
      user: "${PG_USER:bb5}"
      password: "${PG_PASSWORD}"

    neo4j:
      uri: "${NEO4J_URI:bolt://localhost:7687}"
      user: "${NEO4J_USER:neo4j}"
      password: "${NEO4J_PASSWORD}"

  # Embedding settings
  embedding:
    model: "text-embedding-3-small"
    dimensions: 1536
    batch_size: 100

  # RETAIN operation settings
  retain:
    auto_extract: true
    extract_entities: true
    extract_facts: true
    extract_opinions: true
    min_confidence: 0.7

  # RECALL operation settings
  recall:
    strategies:
      - semantic
      - keyword
      - graph
      - temporal
    merge_method: "reciprocal_rank_fusion"
    top_k: 10
    context_budget: 4000

  # REFLECT operation settings
  reflect:
    dispositions:
      skepticism: 0.7
      literalism: 0.3
      empathy: 0.6
      bias_strength: 0.5
```

### Phase 2 Deliverables

- [ ] pgvector extension installed
- [ ] Memory tables created in PostgreSQL
- [ ] Neo4j schema extended
- [ ] Embedding pipeline implemented
- [ ] Graph populator implemented
- [ ] Configuration file created

### Phase 2 Success Criteria

- Databases are queryable
- Embedding generation works
- Graph population works
- Configuration is valid

---

## Phase 3: RETAIN Operation - Automated Ingestion

**Duration:** Week 3
**Priority:** HIGH
**Dependencies:** Phase 2

### 3.1 Implement RETAIN Pipeline

**Purpose:** Automatically extract and store memory from runs/tasks

**File:** `2-engine/memory/operations/retain.py`

```python
"""RETAIN operation: Structured ingestion of memory."""

import yaml
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class RetainOperation:
    """
    Implements Hindsight's RETAIN operation for Blackbox5.

    Processes task/run folders and extracts:
    - Facts (World Network)
    - Experiences (Experience Network)
    - Opinions (Opinion Network)
    - Observations (Observation Network)
    """

    def __init__(self, config_path: str = ".autonomous/memory/config.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.embedder = MemoryEmbedder()
        self.graph = MemoryGraphPopulator(
            uri=self.config['databases']['neo4j']['uri'],
            user=self.config['databases']['neo4j']['user'],
            password=self.config['databases']['neo4j']['password']
        )

    def process_task(self, task_path: str) -> Dict:
        """
        Process a task folder and extract all memory types.

        Args:
            task_path: Path to task folder (e.g., tasks/active/TASK-XXX)

        Returns:
            Summary of extracted memory
        """
        task_path = Path(task_path)
        task_id = task_path.name

        results = {
            'task_id': task_id,
            'facts_extracted': 0,
            'experiences_extracted': 0,
            'opinions_extracted': 0,
            'observations_extracted': 0,
            'entities_extracted': 0
        }

        # Process each memory file type
        if (task_path / 'THOUGHTS.md').exists():
            exp_count = self._extract_experiences(task_path / 'THOUGHTS.md', task_id)
            results['experiences_extracted'] += exp_count

        if (task_path / 'DECISIONS.md').exists():
            fact_count, op_count = self._extract_from_decisions(
                task_path / 'DECISIONS.md', task_id
            )
            results['facts_extracted'] += fact_count
            results['opinions_extracted'] += op_count

        if (task_path / 'LEARNINGS.md').exists():
            obs_count = self._extract_observations(task_path / 'LEARNINGS.md', task_id)
            results['observations_extracted'] += obs_count

        # Extract entities from all content
        entities = self._extract_entities_from_task(task_path)
        results['entities_extracted'] = len(entities)

        # Store in databases
        self._store_in_postgresql(task_path, task_id)
        self._store_in_neo4j(entities, task_id)

        return results

    def _extract_experiences(self, thoughts_path: Path, task_id: str) -> int:
        """Extract experiences from THOUGHTS.md."""
        with open(thoughts_path) as f:
            content = f.read()

        experiences = []

        # Pattern: Look for first-person statements
        patterns = [
            r'I\s+(decided|chose|implemented|found|discovered|realized)\s+(.+?)(?:\n|$)',
            r'We\s+(should|could|might|need to)\s+(.+?)(?:\n|$)',
        ]

        exp_id = 0
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                exp_id += 1
                experience = {
                    'id': f"EXP-{task_id}-{exp_id:03d}",
                    'action': match.group(1),
                    'description': match.group(2).strip(),
                    'source': str(thoughts_path),
                    'timestamp': datetime.now().isoformat()
                }
                experiences.append(experience)

        # Write to EXPERIENCES.md
        if experiences:
            self._write_experiences_md(thoughts_path.parent, experiences)

        return len(experiences)

    def _extract_from_decisions(self, decisions_path: Path, task_id: str) -> tuple:
        """Extract facts and opinions from DECISIONS.md."""
        with open(decisions_path) as f:
            content = f.read()

        facts = []
        opinions = []

        # Parse decision blocks
        decision_pattern = r'##\s+DEC-\d+:[^#]+?(?=##|\Z)'
        decisions = re.finditer(decision_pattern, content, re.DOTALL)

        for i, decision in enumerate(decisions, 1):
            dec_text = decision.group(0)

            # Extract decision as fact
            fact = {
                'id': f"FACT-{task_id}-{i:03d}",
                'statement': self._extract_decision_statement(dec_text),
                'source': f"DEC-{task_id}-{i:03d}",
                'confidence': 1.0  # Decisions are facts
            }
            facts.append(fact)

            # Extract rationale as opinion
            if 'rationale' in dec_text.lower():
                opinion = {
                    'id': f"OP-{task_id}-{i:03d}",
                    'belief': self._extract_rationale(dec_text),
                    'confidence': 0.85,  # Rationale is opinion
                    'source': f"DEC-{task_id}-{i:03d}"
                }
                opinions.append(opinion)

        # Write to files
        if facts:
            self._write_facts_md(decisions_path.parent, facts)
        if opinions:
            self._write_opinions_md(decisions_path.parent, opinions)

        return len(facts), len(opinions)

    def _extract_observations(self, learnings_path: Path, task_id: str) -> int:
        """Extract observations from LEARNINGS.md."""
        with open(learnings_path) as f:
            content = f.read()

        observations = []

        # Pattern: "What worked/didn't work" sections
        sections = re.findall(
            r'##\s+(What Worked|What Didn\'t|Patterns|Insights)[^#]+?(?=##|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        for i, section in enumerate(sections, 1):
            observation = {
                'id': f"OBS-{task_id}-{i:03d}",
                'content': section,
                'synthesized_from': [str(learnings_path)],
                'timestamp': datetime.now().isoformat()
            }
            observations.append(observation)

        if observations:
            self._write_observations_md(learnings_path.parent, observations)

        return len(observations)

    def _extract_entities_from_task(self, task_path: Path) -> List[Dict]:
        """Extract entities from all files in task."""
        entities = []

        # Read all markdown files
        for md_file in task_path.glob('*.md'):
            with open(md_file) as f:
                content = f.read()

            # Use LLM or NER to extract entities
            # For now, simple pattern matching
            entity_patterns = [
                (r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b', 'technology'),  # CamelCase
                (r'\b(PostgreSQL|Redis|Neo4j|Python|JavaScript)\b', 'technology'),
                (r'\b(TASK-[0-9]+|DEC-[0-9]+)\b', 'reference'),
            ]

            for pattern, entity_type in entity_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    entities.append({
                        'name': match.group(1),
                        'type': entity_type,
                        'source': str(md_file)
                    })

        return entities

    def _write_experiences_md(self, task_path: Path, experiences: List[Dict]):
        """Write experiences to EXPERIENCES.md."""
        output = "# EXPERIENCES\n\n"
        output += f"**Auto-generated:** {datetime.now().isoformat()}\n\n"

        for exp in experiences:
            output += f"## {exp['id']}: {exp['action'].title()}\n\n"
            output += f"**Date:** {exp['timestamp']}\n"
            output += f"**Source:** {exp['source']}\n\n"
            output += f"{exp['description']}\n\n"
            output += "---\n\n"

        with open(task_path / 'EXPERIENCES.md', 'w') as f:
            f.write(output)

    def _write_facts_md(self, task_path: Path, facts: List[Dict]):
        """Write facts to FACTS.md."""
        output = "# FACTS\n\n"
        output += f"**Auto-generated:** {datetime.now().isoformat()}\n\n"

        for fact in facts:
            output += f"## {fact['id']}\n\n"
            output += f"**Statement:** {fact['statement']}\n"
            output += f"**Confidence:** {fact['confidence']}\n"
            output += f"**Source:** {fact['source']}\n\n"
            output += "---\n\n"

        with open(task_path / 'FACTS.md', 'w') as f:
            f.write(output)

    def _write_opinions_md(self, task_path: Path, opinions: List[Dict]):
        """Write opinions to OPINIONS.md."""
        output = "# OPINIONS\n\n"
        output += f"**Auto-generated:** {datetime.now().isoformat()}\n\n"

        for op in opinions:
            output += f"## {op['id']}\n\n"
            output += f"**Belief:** {op['belief']}\n"
            output += f"**Confidence:** {op['confidence']}\n"
            output += f"**Source:** {op['source']}\n"
            output += f"**Status:** active\n\n"
            output += "---\n\n"

        with open(task_path / 'OPINIONS.md', 'w') as f:
            f.write(output)

    def _write_observations_md(self, task_path: Path, observations: List[Dict]):
        """Write observations to OBSERVATIONS.md."""
        output = "# OBSERVATIONS\n\n"
        output += f"**Auto-generated:** {datetime.now().isoformat()}\n\n"

        for obs in observations:
            output += f"## {obs['id']}\n\n"
            output += f"**Synthesized From:** {', '.join(obs['synthesized_from'])}\n"
            output += f"**Timestamp:** {obs['timestamp']}\n\n"
            output += f"{obs['content']}\n\n"
            output += "---\n\n"

        with open(task_path / 'OBSERVATIONS.md', 'w') as f:
            f.write(output)

    def _store_in_postgresql(self, task_path: Path, task_id: str):
        """Store embeddings and content in PostgreSQL."""
        # Implementation using psycopg2
        pass

    def _store_in_neo4j(self, entities: List[Dict], task_id: str):
        """Store entities and relationships in Neo4j."""
        for entity in entities:
            self.graph.add_entity(
                name=entity['name'],
                entity_type=entity['type'],
                properties={'source': entity['source'], 'task': task_id}
            )


# CLI interface
if __name__ == '__main__':
    import sys

    retain = RetainOperation()

    if len(sys.argv) > 1:
        task_path = sys.argv[1]
        results = retain.process_task(task_path)
        print(f"Processed {results['task_id']}:")
        print(f"  - Facts: {results['facts_extracted']}")
        print(f"  - Experiences: {results['experiences_extracted']}")
        print(f"  - Opinions: {results['opinions_extracted']}")
        print(f"  - Observations: {results['observations_extracted']}")
        print(f"  - Entities: {results['entities_extracted']}")
    else:
        print("Usage: python retain.py <task_path>")
```

### 3.2 Create RETAIN Automation

**File:** `.autonomous/memory/workflows/retain.yaml`

```yaml
workflow:
  name: "RETAIN Pipeline"
  description: "Automatically extract memory from completed tasks"

  trigger:
    type: "scheduled"
    schedule: "0 */6 * * *"  # Every 6 hours

  steps:
    - name: "Find completed tasks"
      action: "find_files"
      pattern: "tasks/completed/**/task.md"

    - name: "Filter unprocessed"
      action: "filter"
      condition: "not exists FACTS.md"

    - name: "Run RETAIN"
      action: "execute"
      command: "python 2-engine/memory/operations/retain.py {task_path}"

    - name: "Update index"
      action: "execute"
      command: "python 2-engine/memory/indexer.py --update"

  on_error:
    action: "log"
    destination: ".autonomous/memory/logs/retain-errors.log"
```

### Phase 3 Deliverables

- [ ] RETAIN operation implemented
- [ ] Entity extraction working
- [ ] Fact extraction working
- [ ] Opinion extraction working
- [ ] Experience extraction working
- [ ] PostgreSQL storage working
- [ ] Neo4j graph population working
- [ ] Automation workflow created

### Phase 3 Success Criteria

- Can process a task folder end-to-end
- Generates all 4 memory files
- Stores in databases correctly
- Automation runs without errors

---

## Phase 4: RECALL Operation - Multi-Strategy Retrieval

**Duration:** Week 4
**Priority:** HIGH
**Dependencies:** Phase 3

### 4.1 Implement RECALL Pipeline

**Purpose:** Retrieve relevant memory using multiple strategies

**File:** `2-engine/memory/operations/recall.py`

```python
"""RECALL operation: Multi-strategy memory retrieval."""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class RecallResult:
    """Single recall result."""
    content: str
    source: str
    source_type: str
    score: float
    strategy: str
    metadata: Dict

class RecallOperation:
    """
    Implements Hindsight's RECALL operation for Blackbox5.

    Uses 4 parallel strategies:
    1. Semantic (vector similarity)
    2. Keyword (BM25)
    3. Graph (entity traversal)
    4. Temporal (time-based)

    Merges results with Reciprocal Rank Fusion.
    """

    def __init__(self, config_path: str = ".autonomous/memory/config.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.embedder = MemoryEmbedder()
        self.pg_conn = self._connect_postgresql()
        self.neo4j = self._connect_neo4j()

    def recall(
        self,
        query: str,
        context_budget: int = 4000,
        top_k: int = 10,
        strategies: List[str] = None
    ) -> List[RecallResult]:
        """
        Recall relevant memories using multiple strategies.

        Args:
            query: Search query
            context_budget: Max tokens to return
            top_k: Number of results per strategy
            strategies: List of strategies to use (default: all)

        Returns:
            Merged and ranked list of recall results
        """
        if strategies is None:
            strategies = ['semantic', 'keyword', 'graph', 'temporal']

        all_results = []

        # Run each strategy in parallel (conceptually)
        if 'semantic' in strategies:
            semantic_results = self._semantic_search(query, top_k)
            all_results.extend(semantic_results)

        if 'keyword' in strategies:
            keyword_results = self._keyword_search(query, top_k)
            all_results.extend(keyword_results)

        if 'graph' in strategies:
            graph_results = self._graph_search(query, top_k)
            all_results.extend(graph_results)

        if 'temporal' in strategies:
            temporal_results = self._temporal_search(query, top_k)
            all_results.extend(temporal_results)

        # Merge with Reciprocal Rank Fusion
        merged = self._reciprocal_rank_fusion(all_results)

        # Rerank with cross-encoder (optional)
        reranked = self._rerank(query, merged)

        # Apply token budget
        final_results = self._apply_budget(reranked, context_budget)

        return final_results

    def _semantic_search(self, query: str, top_k: int) -> List[RecallResult]:
        """Vector similarity search."""
        query_embedding = self.embedder.embed_text(query)

        cursor = self.pg_conn.cursor()
        cursor.execute("""
            SELECT content, source_type, source_id, file_type,
                   1 - (content_vector <=> %s::vector) as similarity
            FROM memory_contents
            ORDER BY content_vector <=> %s::vector
            LIMIT %s
        """, (query_embedding, query_embedding, top_k))

        results = []
        for row in cursor.fetchall():
            results.append(RecallResult(
                content=row[0],
                source=f"{row[1]}/{row[2]}/{row[3]}",
                source_type=row[1],
                score=row[4],
                strategy='semantic',
                metadata={'similarity': row[4]}
            ))

        return results

    def _keyword_search(self, query: str, top_k: int) -> List[RecallResult]:
        """BM25 keyword search."""
        cursor = self.pg_conn.cursor()

        # Convert query to tsquery
        cursor.execute("""
            SELECT to_tsquery('english', string_agg(lexeme, ' | '))
            FROM unnest(to_tsvector('english', %s))
        """, (query,))

        tsquery = cursor.fetchone()[0]

        cursor.execute("""
            SELECT content, source_type, source_id, file_type,
                   ts_rank(to_tsvector('english', content), %s) as rank
            FROM memory_contents
            WHERE to_tsvector('english', content) @@ %s
            ORDER BY rank DESC
            LIMIT %s
        """, (tsquery, tsquery, top_k))

        results = []
        for row in cursor.fetchall():
            results.append(RecallResult(
                content=row[0],
                source=f"{row[1]}/{row[2]}/{row[3]}",
                source_type=row[1],
                score=row[4],
                strategy='keyword',
                metadata={'bm25_rank': row[4]}
            ))

        return results

    def _graph_search(self, query: str, top_k: int) -> List[RecallResult]:
        """Graph traversal search."""
        # Extract entities from query
        entities = self.embedder.extract_entities(query)

        results = []

        with self.neo4j.driver.session() as session:
            for entity in entities:
                # Find related entities and facts
                result = session.run("""
                    MATCH (e:Entity {name: $name})<-[:ABOUT]-(f:Fact)
                    RETURN f.statement as content,
                           'fact' as type,
                           0.8 as score
                    LIMIT $limit
                """, name=entity, limit=top_k // len(entities))

                for record in result:
                    results.append(RecallResult(
                        content=record['content'],
                        source=f"graph/entity/{entity}",
                        source_type='fact',
                        score=record['score'],
                        strategy='graph',
                        metadata={'entity': entity}
                    ))

        return results

    def _temporal_search(self, query: str, top_k: int) -> List[RecallResult]:
        """Time-based search (recent memories)."""
        cursor = self.pg_conn.cursor()

        cursor.execute("""
            SELECT content, source_type, source_id, file_type,
                   EXTRACT(EPOCH FROM (NOW() - created_at)) / 86400.0 as days_ago
            FROM memory_contents
            ORDER BY created_at DESC
            LIMIT %s
        """, (top_k,))

        results = []
        for row in cursor.fetchall():
            # Score decays with age (exponential decay)
            days_ago = row[4]
            score = np.exp(-days_ago / 30)  # 30-day half-life

            results.append(RecallResult(
                content=row[0],
                source=f"{row[1]}/{row[2]}/{row[3]}",
                source_type=row[1],
                score=score,
                strategy='temporal',
                metadata={'days_ago': days_ago}
            ))

        return results

    def _reciprocal_rank_fusion(
        self,
        results: List[RecallResult],
        k: int = 60
    ) -> List[RecallResult]:
        """
        Merge results using Reciprocal Rank Fusion.

        RRF score = sum(1 / (k + rank)) for each list
        """
        from collections import defaultdict

        # Group by content
        content_scores = defaultdict(lambda: {'score': 0, 'result': None})

        # Group results by strategy
        by_strategy = defaultdict(list)
        for r in results:
            by_strategy[r.strategy].append(r)

        # Calculate RRF score for each
        for strategy, strategy_results in by_strategy.items():
            # Sort by score within strategy
            sorted_results = sorted(
                strategy_results,
                key=lambda x: x.score,
                reverse=True
            )

            for rank, result in enumerate(sorted_results, 1):
                rrf_score = 1 / (k + rank)
                content_scores[result.content]['score'] += rrf_score
                if content_scores[result.content]['result'] is None:
                    content_scores[result.content]['result'] = result

        # Sort by RRF score
        merged = sorted(
            content_scores.values(),
            key=lambda x: x['score'],
            reverse=True
        )

        return [item['result'] for item in merged]

    def _rerank(
        self,
        query: str,
        results: List[RecallResult]
    ) -> List[RecallResult]:
        """Rerank with cross-encoder (optional, can be skipped for speed)."""
        # For now, skip reranking
        # In production, use sentence-transformers cross-encoder
        return results

    def _apply_budget(
        self,
        results: List[RecallResult],
        budget: int
    ) -> List[RecallResult]:
        """Apply token budget to results."""
        final_results = []
        current_tokens = 0

        # Rough estimate: 4 chars ≈ 1 token
        for result in results:
            estimated_tokens = len(result.content) // 4

            if current_tokens + estimated_tokens <= budget:
                final_results.append(result)
                current_tokens += estimated_tokens
            else:
                break

        return final_results


# CLI interface
if __name__ == '__main__':
    import sys

    recall = RecallOperation()

    if len(sys.argv) > 1:
        query = sys.argv[1]
        results = recall.recall(query)

        print(f"Query: {query}\n")
        print(f"Found {len(results)} results:\n")

        for i, result in enumerate(results, 1):
            print(f"{i}. [{result.strategy}] Score: {result.score:.3f}")
            print(f"   Source: {result.source}")
            print(f"   Content: {result.content[:200]}...")
            print()
    else:
        print("Usage: python recall.py 'your query here'")
```

### 4.2 Create RECALL Integration Points

**File:** `2-engine/memory/integration/task_loader.py`

```python
"""Integration: Load relevant memory when starting tasks."""

from pathlib import Path

class TaskMemoryLoader:
    """Loads relevant memory when starting a new task."""

    def __init__(self):
        self.recall = RecallOperation()

    def load_for_task(self, task_description: str) -> str:
        """
        Load relevant memory for a new task.

        Args:
            task_description: Description of the task being started

        Returns:
            Formatted context string for injection into THOUGHTS.md
        """
        # Recall relevant memories
        results = self.recall.recall(
            query=task_description,
            context_budget=3000,  # Leave room for other context
            top_k=10
        )

        if not results:
            return ""

        # Format as context
        context = "## Relevant Previous Work\n\n"
        context += "Based on analysis of previous tasks, the following may be relevant:\n\n"

        for result in results:
            context += f"### From {result.source}\n"
            context += f"**Relevance:** {result.score:.2f} ({result.strategy} search)\n\n"
            context += f"{result.content[:500]}...\n\n"
            context += "---\n\n"

        return context

    def inject_into_task(self, task_path: str):
        """Inject relevant memory into task's THOUGHTS.md."""
        task_path = Path(task_path)

        # Read task description
        with open(task_path / 'task.md') as f:
            task_content = f.read()

        # Extract description (first paragraph)
        description = task_content.split('\n\n')[0]

        # Load relevant memory
        relevant = self.load_for_task(description)

        if not relevant:
            return

        # Read existing THOUGHTS.md or create
        thoughts_path = task_path / 'THOUGHTS.md'
        if thoughts_path.exists():
            with open(thoughts_path) as f:
                existing = f.read()
        else:
            existing = "# THOUGHTS\n\n"

        # Insert relevant memory after header
        if '## Relevant Previous Work' not in existing:
            parts = existing.split('\n\n', 1)
            new_content = parts[0] + '\n\n' + relevant
            if len(parts) > 1:
                new_content += '\n\n' + parts[1]

            with open(thoughts_path, 'w') as f:
                f.write(new_content)
```

### Phase 4 Deliverables

- [ ] RECALL operation implemented
- [ ] Semantic search working
- [ ] Keyword search working
- [ ] Graph search working
- [ ] Temporal search working
- [ ] RRF merging working
- [ ] Task loader integration working

### Phase 4 Success Criteria

- Can recall memories from query
- Multiple strategies return results
- Merging produces good ranking
- Integration injects context correctly

---

## Phase 5: REFLECT Operation - Preference-Conditioned Reasoning

**Duration:** Week 5
**Priority:** MEDIUM
**Dependencies:** Phase 4

### 5.1 Implement REFLECT Pipeline

**Purpose:** Enable belief updating and consistent reasoning

**File:** `2-engine/memory/operations/reflect.py`

```python
"""REFLECT operation: Preference-conditioned reasoning."""

from dataclasses import dataclass
from typing import Dict, List, Optional
import yaml

@dataclass
class DispositionProfile:
    """Behavioral disposition parameters."""
    skepticism: float = 0.7      # Question new information
    literalism: float = 0.3      # Prefer exact meaning
    empathy: float = 0.6         # Weight emotional context
    bias_strength: float = 0.5   # Hold existing opinions

class ReflectOperation:
    """
    Implements Hindsight's REFLECT operation for Blackbox5.

    Provides:
    1. Preference-conditioned response generation
    2. Belief updating based on evidence
    3. Consistent agent personality
    """

    def __init__(
        self,
        dispositions: Optional[DispositionProfile] = None,
        config_path: str = ".autonomous/memory/config.yaml"
    ):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.dispositions = dispositions or DispositionProfile()
        self.recall = RecallOperation()

    def reflect(
        self,
        query: str,
        context: List[str] = None,
        update_beliefs: bool = True
    ) -> Dict:
        """
        Generate reflection on query with preference conditioning.

        Args:
            query: Question or topic to reflect on
            context: Additional context (optional)
            update_beliefs: Whether to update beliefs based on reflection

        Returns:
            Dictionary with reflection results
        """
        # Recall relevant opinions and facts
        relevant = self.recall.recall(
            query=query,
            strategies=['semantic', 'graph'],
            top_k=5
        )

        # Filter by disposition
        if self.dispositions.skepticism > 0.5:
            relevant = self._apply_skepticism(relevant)

        # Generate reflection
        reflection = self._generate_reflection(query, relevant, context)

        # Update beliefs if enabled
        if update_beliefs:
            self._update_beliefs(query, reflection)

        return {
            'query': query,
            'reflection': reflection,
            'relevant_memories': len(relevant),
            'dispositions_applied': self._get_applied_dispositions(),
            'beliefs_updated': update_beliefs
        }

    def _apply_skepticism(
        self,
        memories: List[RecallResult]
    ) -> List[RecallResult]:
        """Filter memories based on skepticism."""
        # Reduce confidence of low-certainty memories
        for memory in memories:
            if memory.score < 0.7:
                memory.score *= 0.8  # Penalize uncertain memories

        # Sort by adjusted score
        return sorted(memories, key=lambda x: x.score, reverse=True)

    def _generate_reflection(
        self,
        query: str,
        relevant: List[RecallResult],
        context: List[str]
    ) -> str:
        """Generate reflection text."""
        # In production, this would use an LLM
        # For now, template-based

        reflection = f"## Reflection: {query}\n\n"

        # Include relevant context
        if relevant:
            reflection += "### Relevant Previous Work\n\n"
            for mem in relevant[:3]:
                reflection += f"- {mem.content[:200]}...\n"
            reflection += "\n"

        # Add disposition-influenced analysis
        if self.dispositions.skepticism > 0.6:
            reflection += "### Critical Analysis\n\n"
            reflection += "Given my skeptical disposition, I should note:\n"
            reflection += "- The evidence for this approach is limited\n"
            reflection += "- Alternative approaches should be considered\n"
            reflection += "- More validation is needed\n\n"

        if self.dispositions.bias_strength > 0.6:
            reflection += "### Consistency Check\n\n"
            reflection += "This aligns with my existing beliefs about:\n"
            reflection += "- Preference for simple solutions\n"
            reflection += "- Value of explicit documentation\n\n"

        return reflection

    def _update_beliefs(self, query: str, reflection: str):
        """Update beliefs based on reflection."""
        # Extract opinions from reflection
        # Check for contradictions with existing opinions
        # Update confidence scores
        pass

    def _get_applied_dispositions(self) -> Dict[str, float]:
        """Get dispositions that influenced this reflection."""
        applied = {}

        if self.dispositions.skepticism > 0.5:
            applied['skepticism'] = self.dispositions.skepticism

        if self.dispositions.bias_strength > 0.5:
            applied['bias_strength'] = self.dispositions.bias_strength

        return applied

    def update_opinion_confidence(
        self,
        opinion_id: str,
        new_evidence: str,
        supports: bool
    ):
        """
        Update confidence of an opinion based on new evidence.

        Args:
            opinion_id: ID of opinion to update
            new_evidence: Description of new evidence
            supports: Whether evidence supports or contradicts
        """
        # Query current opinion
        cursor = self.pg_conn.cursor()
        cursor.execute("""
            SELECT confidence, evidence_for, evidence_against
            FROM memory_opinions
            WHERE id = %s
        """, (opinion_id,))

        row = cursor.fetchone()
        if not row:
            return

        current_confidence = row[0]
        evidence_for = row[1] or []
        evidence_against = row[2] or []

        # Update based on evidence
        if supports:
            new_confidence = min(1.0, current_confidence + 0.05)
            evidence_for.append({
                'date': datetime.now().isoformat(),
                'evidence': new_evidence
            })
        else:
            new_confidence = max(0.0, current_confidence - 0.1)
            evidence_against.append({
                'date': datetime.now().isoformat(),
                'evidence': new_evidence
            })

        # Update database
        cursor.execute("""
            UPDATE memory_opinions
            SET confidence = %s,
                evidence_for = %s,
                evidence_against = %s,
                revised_at = NOW()
            WHERE id = %s
        """, (new_confidence, evidence_for, evidence_against, opinion_id))

        self.pg_conn.commit()


# CLI interface
if __name__ == '__main__':
    import sys

    reflect = ReflectOperation()

    if len(sys.argv) > 1:
        query = sys.argv[1]
        result = reflect.reflect(query)

        print(f"Query: {result['query']}\n")
        print(f"Relevant memories: {result['relevant_memories']}")
        print(f"Dispositions applied: {result['dispositions_applied']}")
        print(f"\nReflection:\n{result['reflection']}")
    else:
        print("Usage: python reflect.py 'your question here'")
```

### Phase 5 Deliverables

- [ ] REFLECT operation implemented
- [ ] Disposition profiles working
- [ ] Belief updating working
- [ ] Integration with RECALL working

### Phase 5 Success Criteria

- Can generate reflections
- Dispositions influence output
- Beliefs update correctly

---

## Phase 6: Integration & Testing

**Duration:** Week 6
**Priority:** HIGH
**Dependencies:** Phases 1-5

### 6.1 Integration Points

#### 6.1.1 Task Creation Hook

**File:** `2-engine/hooks/task_created.py`

```python
"""Hook: Inject relevant memory when task is created."""

from memory.integration.task_loader import TaskMemoryLoader

def on_task_created(task_path: str):
    """Called when new task is created."""
    loader = TaskMemoryLoader()
    loader.inject_into_task(task_path)
```

#### 6.1.2 Task Completion Hook

**File:** `2-engine/hooks/task_completed.py`

```python
"""Hook: Run RETAIN when task is completed."""

from memory.operations.retain import RetainOperation

def on_task_completed(task_path: str):
    """Called when task is completed."""
    retain = RetainOperation()
    results = retain.process_task(task_path)

    # Log results
    print(f"RETAIN processed {results['task_id']}:")
    print(f"  Facts: {results['facts_extracted']}")
    print(f"  Experiences: {results['experiences_extracted']}")
    print(f"  Opinions: {results['opinions_extracted']}")
```

#### 6.1.3 RALF Integration

**File:** `2-engine/ralf/memory_integration.py`

```python
"""RALF integration with memory system."""

class RalfMemoryIntegration:
    """Integrates memory system with RALF workflows."""

    def __init__(self):
        self.recall = RecallOperation()
        self.retain = RetainOperation()

    def before_run(self, run_context: dict) -> dict:
        """Load relevant memory before RALF run."""
        query = run_context.get('task_description', '')

        # Recall relevant memories
        memories = self.recall.recall(query, context_budget=2000)

        # Add to run context
        run_context['relevant_memories'] = memories

        return run_context

    def after_run(self, run_path: str, run_results: dict):
        """Process memory after RALF run."""
        # Run RETAIN on the run folder
        self.retain.process_task(run_path)
```

### 6.2 Testing Plan

#### 6.2.1 Unit Tests

**File:** `2-engine/memory/tests/test_retain.py`

```python
"""Tests for RETAIN operation."""

def test_extract_experiences():
    """Test experience extraction from THOUGHTS.md."""
    pass

def test_extract_facts():
    """Test fact extraction from DECISIONS.md."""
    pass

def test_extract_opinions():
    """Test opinion extraction."""
    pass
```

**File:** `2-engine/memory/tests/test_recall.py`

```python
"""Tests for RECALL operation."""

def test_semantic_search():
    """Test vector similarity search."""
    pass

def test_keyword_search():
    """Test BM25 keyword search."""
    pass

def test_rrf_merge():
    """Test Reciprocal Rank Fusion."""
    pass
```

#### 6.2.2 Integration Tests

**File:** `2-engine/memory/tests/test_integration.py`

```python
"""Integration tests for memory system."""

def test_end_to_end_task():
    """Test full pipeline on a task."""
    # 1. Create task
    # 2. Complete task
    # 3. Run RETAIN
    # 4. Query with RECALL
    # 5. Verify results
    pass

def test_cross_task_retrieval():
    """Test retrieving memory from previous tasks."""
    pass
```

#### 6.2.3 Benchmarks

**File:** `2-engine/memory/tests/benchmarks.py`

```python
"""Benchmark memory system performance."""

def benchmark_recall_latency():
    """Measure RECALL operation latency."""
    pass

def benchmark_recall_accuracy():
    """Measure RECALL result relevance."""
    pass

def benchmark_retain_throughput():
    """Measure RETAIN processing speed."""
    pass
```

### 6.3 Documentation

#### 6.3.1 User Guide

**File:** `.autonomous/memory/docs/user-guide.md`

```markdown
# Blackbox5 Memory System User Guide

## Overview

The enhanced memory system provides:
- Automatic extraction of facts, experiences, opinions, observations
- Semantic search across all tasks and runs
- Belief tracking with confidence scores
- Entity relationship graph

## Quick Start

### For Task Execution

1. Create task normally
2. System automatically loads relevant past work
3. Execute task, update THOUGHTS.md, DECISIONS.md
4. On completion, system extracts memory automatically

### For Memory Queries

```bash
# Query memory
python 2-engine/memory/cli.py recall "What did we decide about PostgreSQL?"

# View entity graph
python 2-engine/memory/cli.py graph "PostgreSQL"

# Check opinions
python 2-engine/memory/cli.py opinions --active
```

## File Reference

### New Memory Files

- `FACTS.md` - Objective facts extracted from task
- `EXPERIENCES.md` - First-person experiences
- `OPINIONS.md` - Beliefs with confidence scores
- `OBSERVATIONS.md` - Synthesized observations

### Project-Level Memory

- `.autonomous/memory/world/` - Global facts
- `.autonomous/memory/opinions/` - Cross-task opinions
- `.autonomous/memory/observations/` - Pattern library
```

#### 6.3.2 API Documentation

**File:** `.autonomous/memory/docs/api.md`

Document all public APIs for RETAIN, RECALL, REFLECT operations.

### Phase 6 Deliverables

- [ ] Integration hooks implemented
- [ ] RALF integration working
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Benchmarks run
- [ ] Documentation complete

### Phase 6 Success Criteria

- End-to-end pipeline works
- Tests pass
- Performance acceptable
- Documentation clear

---

## Rollback Plan

If integration fails:

1. **Disable hooks** - Stop automatic memory processing
2. **Revert templates** - Remove new memory files from templates
3. **Keep databases** - Don't delete pgvector/Neo4j data
4. **Document state** - Record what was working

---

## Success Metrics

### Quantitative

| Metric | Target | Measurement |
|--------|--------|-------------|
| RETAIN coverage | >90% | % of tasks processed |
| RECALL latency | <500ms | Average query time |
| RECALL relevance | >80% | Human-rated relevance |
| Memory growth | Linear | Storage per task |

### Qualitative

- Agents can find relevant past work
- Decisions reference previous reasoning
- Beliefs evolve with evidence
- Cross-task patterns emerge

---

## Timeline Summary

| Phase | Duration | Focus | Key Deliverable |
|-------|----------|-------|-----------------|
| 1 | Week 1 | File structure | 4 new memory templates |
| 2 | Week 2 | Infrastructure | pgvector + Neo4j setup |
| 3 | Week 3 | RETAIN | Automated extraction |
| 4 | Week 4 | RECALL | Multi-strategy search |
| 5 | Week 5 | REFLECT | Belief updating |
| 6 | Week 6 | Integration | Full pipeline + tests |

**Total: 6 weeks**

---

## Next Steps

1. **Review this plan** - Get feedback, adjust as needed
2. **Set up tracking** - Create tasks for each phase
3. **Begin Phase 1** - Start with file templates
4. **Weekly reviews** - Check progress, adjust timeline

---

*This action plan provides a complete roadmap for integrating Hindsight's memory architecture into Blackbox5.*
