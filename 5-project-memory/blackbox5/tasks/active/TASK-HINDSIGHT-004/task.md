---
task_id: TASK-HINDSIGHT-004
title: "Implement RECALL Operation"
linked_goal: IG-008
linked_sub_goal: SG-008-4
linked_plan: PLAN-HINDSIGHT-001
status: pending
priority: high
created: "2026-02-04"
---

# TASK-HINDSIGHT-004: Implement RECALL Operation

**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-04

---

## Objective

Build multi-strategy retrieval system (RECALL operation) with semantic, keyword, graph, and temporal search strategies, plus RRF merging for result ranking.

---

## Context

RECALL is Hindsight's retrieval operation. It uses 4 strategies:
1. **Semantic** - Vector similarity via pgvector
2. **Keyword** - BM25 via PostgreSQL full-text search
3. **Graph** - Entity traversal via Neo4j
4. **Temporal** - Recency-weighted results

Results are merged using Reciprocal Rank Fusion (RRF) for optimal ranking.

---

## Success Criteria

- [ ] Semantic search working (vector similarity via pgvector)
- [ ] Keyword search working (BM25 full-text search)
- [ ] Graph search working (entity traversal via Neo4j)
- [ ] Temporal search working (recency-weighted)
- [ ] RRF merging working for result combination
- [ ] Task loader integration working (inject relevant memory into new tasks)
- [ ] CLI interface for memory queries
- [ ] <500ms average latency
- [ ] >80% relevance score (human-rated)

---

## Approach

1. **Search Strategies:**
   - Implement semantic_search() using pgvector cosine similarity
   - Implement keyword_search() using PostgreSQL tsvector/tsquery
   - Implement graph_search() using Neo4j relationship traversal
   - Implement temporal_search() with recency weighting

2. **RRF Merging:**
   - Implement Reciprocal Rank Fusion algorithm
   - Configurable weights for each strategy
   - Deduplication of results
   - Ranking by fused score

3. **Integration:**
   - Task loader: inject relevant memories into new task context
   - CLI: query interface for manual memory search
   - API: programmatic access for agents

4. **Optimization:**
   - Query caching
   - Index optimization
   - Connection pooling
   - Performance benchmarking

---

## Files to Create/Modify

- `.autonomous/memory/operations/recall.py` (new)
- `.autonomous/memory/search/semantic.py` (new)
- `.autonomous/memory/search/keyword.py` (new)
- `.autonomous/memory/search/graph.py` (new)
- `.autonomous/memory/search/temporal.py` (new)
- `.autonomous/memory/search/rrf.py` (new)
- `.autonomous/memory/cli.py` (new)
- Task loader integration (modify)

---

## Dependencies

- [ ] TASK-HINDSIGHT-003 (RETAIN must be working to have data to search)

---

## Notes

- Start with semantic search as primary, add others incrementally
- Benchmark latency early and optimize
- Use caching for common queries
- Consider user feedback for relevance scoring
