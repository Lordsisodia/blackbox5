# Database Migration Task (For Later)

**Status:** Deferred until folder structure stabilizes
**Priority:** Medium
**Blocked by:** Ongoing refactoring

---

## Overview

When the folder structure stabilizes after IG-006 completes, migrate from JSON + in-memory vectors to proper databases.

---

## Current State (Working Now)

**Storage:** JSON files + in-memory vectors
- `memories.json` - All memories with embeddings
- `entities.json` - Extracted entities
- `relationships.json` - Entity relationships
- Vectors kept in memory for fast search

**Pros:**
- ✅ Works immediately
- ✅ Refactor-proof
- ✅ No setup required
- ✅ Easy to migrate

**Cons:**
- ❌ No persistent vector index
- ❌ Limited to ~10K memories
- ❌ No graph traversal
- ❌ Query time grows with size

---

## Target State (Future)

### PostgreSQL + pgvector

**Tables:**
```sql
-- Memories table with vector embedding
CREATE TABLE memories (
    id UUID PRIMARY KEY,
    content TEXT NOT NULL,
    network VARCHAR(20) NOT NULL,
    embedding VECTOR(1536),  -- OpenAI text-embedding-3-small
    confidence FLOAT,
    source VARCHAR(255),
    source_type VARCHAR(50),
    category VARCHAR(50),
    entities TEXT[],
    created_at TIMESTAMP,
    metadata JSONB
);

-- Create vector index for fast similarity search
CREATE INDEX ON memories USING ivfflat (embedding vector_cosine_ops);

-- Full-text search index
CREATE INDEX ON memories USING gin(to_tsvector('english', content));
```

**Migration:**
```python
# Load from JSON
with open('memories.json') as f:
    memories = json.load(f)

# Insert into PostgreSQL
for memory in memories:
    db.execute("""
        INSERT INTO memories (id, content, network, embedding, ...)
        VALUES (...)
    """)
```

### Neo4j Graph Database

**Schema:**
```cypher
// Entities
CREATE (e:Entity {
    name: "PostgreSQL",
    type: "technology",
    first_seen: datetime(),
    mention_count: 5
})

// Relationships
CREATE (e1:Entity {name: "Hindsight"})
CREATE (e2:Entity {name: "PostgreSQL"})
CREATE (e1)-[:USES]->(e2)
```

**Migration:**
```python
# Load from JSON
with open('entities.json') as f:
    entities = json.load(f)

with open('relationships.json') as f:
    relationships = json.load(f)

# Insert into Neo4j
for entity in entities:
    neo4j.run("CREATE (e:Entity {...})")

for rel in relationships:
    neo4j.run("""
        MATCH (s:Entity {name: $subject})
        MATCH (o:Entity {name: $object})
        CREATE (s)-[:USES {confidence: $confidence}]->(o)
    """, rel)
```

---

## Migration Steps

### Phase 1: Setup (1 day)
1. Start PostgreSQL + pgvector Docker
2. Start Neo4j Docker
3. Create schemas
4. Test connections

### Phase 2: Migrate Data (1 day)
1. Export from JSON
2. Import to PostgreSQL
3. Import to Neo4j
4. Validate counts match

### Phase 3: Update Code (1 day)
1. Update RETAIN to use PostgreSQL
2. Update RECALL to use pgvector
3. Update entity extraction to use Neo4j
4. Test end-to-end

### Phase 4: Optimize (1 day)
1. Add connection pooling
2. Add caching layer
3. Benchmark performance
4. Tune indexes

**Total: 4 days when ready**

---

## Docker Compose (Ready to Use)

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_USER: blackbox5
      POSTGRES_PASSWORD: blackbox5_pass
      POSTGRES_DB: memory
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  neo4j:
    image: neo4j:5
    environment:
      NEO4J_AUTH: neo4j/blackbox5_pass
      NEO4J_PLUGINS: '["apoc", "gds"]'
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - neo4j_data:/data

volumes:
  postgres_data:
  neo4j_data:
```

**Start:** `docker-compose up -d`

---

## Trigger for Migration

**Migrate when:**
- ✅ IG-006 completes (folder structure stable)
- ✅ Memory count > 1000 (performance degrades)
- ✅ Need graph traversal (entity relationships)
- ✅ Need persistent vector index

**Don't migrate yet because:**
- 🔄 Refactoring may break paths
- 🔄 JSON works fine for current scale
- 🔄 Easy to migrate later (batch import)

---

## Files to Update

| File | Current | Future |
|------|---------|--------|
| `retain.py` | JSON storage | PostgreSQL + Neo4j |
| `recall.py` | In-memory vectors | pgvector similarity |
| `vector_store.py` | JSON + numpy | SQLAlchemy + pgvector |

---

## Notes

- Migration is **one-way** (JSON → DB)
- Keep JSON as **backup** after migration
- Test migration on **copy** of data first
- Plan for **downtime** during switchover

---

*Documented: 2026-02-04*
*Execute when: IG-006 complete + refactoring stable*
