---
task_id: TASK-HINDSIGHT-002
title: "Build Memory Infrastructure"
linked_goal: IG-008
linked_sub_goal: SG-008-2
linked_plan: PLAN-HINDSIGHT-001
status: pending
priority: high
created: "2026-02-04"
---

# TASK-HINDSIGHT-002: Build Memory Infrastructure

**Type:** implement
**Priority:** high
**Status:** cancelled
**Created:** 2026-02-04

---

## Objective

Set up pgvector in PostgreSQL, extend Neo4j schema, and implement the embedding pipeline for the Hindsight memory architecture.

---

## Context

The memory infrastructure requires:
1. **PostgreSQL + pgvector** for vector similarity search (semantic recall)
2. **Neo4j** for entity relationship graphs (graph traversal)
3. **Embedding pipeline** to convert text to vectors for storage and search

This infrastructure will support the RETAIN, RECALL, and REFLECT operations.

---

## Success Criteria

- [ ] pgvector extension installed and working in PostgreSQL
- [ ] Memory tables created (memory_contents, memory_entities, memory_opinions)
- [ ] Neo4j schema extended for memory graph (entities, relationships, temporal links)
- [ ] Embedding pipeline functional (OpenAI text-embedding-3-small)
- [ ] Configuration complete with environment variables
- [ ] Connection pooling and error handling implemented

---

## Approach

1. **PostgreSQL Setup:**
   - Install pgvector extension
   - Create memory_contents table with vector column
   - Create memory_entities table
   - Create memory_opinions table with confidence scores
   - Set up indexes for performance

2. **Neo4j Setup:**
   - Extend schema with Memory nodes
   - Create Entity nodes with properties
   - Add relationships (RELATED_TO, DERIVED_FROM, CONTRADICTS)
   - Add temporal indexing

3. **Embedding Pipeline:**
   - Implement OpenAI embedding client
   - Add caching layer for embeddings
   - Create batch processing for efficiency
   - Add error handling and retries

4. **Configuration:**
   - Create memory config in .autonomous/memory/config.yaml
   - Add environment variables for DB connections
   - Document setup process

---

## Files to Create/Modify

- `.autonomous/memory/db/postgres_schema.sql` (new)
- `.autonomous/memory/db/neo4j_schema.cypher` (new)
- `.autonomous/memory/embedding.py` (new)
- `.autonomous/memory/config.yaml` (update)
- `.env.example` (update with new variables)

---

## Dependencies

- [ ] TASK-HINDSIGHT-001 (Foundation must be complete)

---

## Notes

- Use text-embedding-3-small for cost efficiency
- Consider Pinecone as fallback if pgvector performance issues arise
- Test against existing RAPS Neo4j graph to avoid conflicts
