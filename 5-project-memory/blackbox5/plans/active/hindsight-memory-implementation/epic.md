# Epic: Hindsight Memory Architecture Implementation

**Plan ID:** PLAN-HINDSIGHT-001
**Goal:** IG-008 - Implement Hindsight Memory Architecture for Persistent Agent Memory
**Status:** in_progress
**Created:** 2026-02-04
**Target Completion:** 2026-03-18

---

## Problem Statement

Blackbox5 currently uses file-based memory (THOUGHTS.md, DECISIONS.md, LEARNINGS.md) per run. This provides basic continuity but lacks:

1. **Semantic search** across all historical runs
2. **Structured relationship tracking** between decisions
3. **Subjective memory** (continuity of self/identity)
4. **Cross-session learning** and pattern recognition
5. **Efficient token usage** through smart retrieval

The field has converged on hybrid architectures: Vector DB (fuzzy recall) + Structured Store (relationships) + LLM consolidation.

---

## Goals

1. **Establish 4-Network Memory Foundation** - Create FACTS.md, EXPERIENCES.md, OPINIONS.md, OBSERVATIONS.md templates
2. **Build Memory Infrastructure** - Set up pgvector in PostgreSQL, extend Neo4j schema, implement embedding pipeline
3. **Implement RETAIN Operation** - Build automated extraction pipeline that processes tasks/runs and populates 4 networks
4. **Implement RECALL Operation** - Build multi-strategy retrieval system (semantic, keyword, graph, temporal) with RRF merging
5. **Implement REFLECT Operation** - Build preference-conditioned reasoning system with belief updating
6. **Integrate and Validate** - Full pipeline integration, testing, benchmarking, and documentation

---

## Success Criteria

- [ ] All 4 memory networks functional (World, Experience, Opinion, Observation)
- [ ] RETAIN operation automatically extracts memory from 90%+ of tasks/runs
- [ ] RECALL operation enables semantic search with <500ms latency
- [ ] REFLECT operation enables belief updating with confidence tracking
- [ ] 70% of Hindsight capabilities implemented
- [ ] Existing THOUGHTS.md/DECISIONS.md remain backward compatible
- [ ] Agents demonstrate continuity of self across sessions
- [ ] Cross-task pattern detection working

---

## Architecture

### Hindsight's 4 Networks

| Network | Stores | BB5 Equivalent |
|---------|--------|----------------|
| World (W) | Objective facts | `FACTS.md` |
| Experience (B) | First-person actions | `EXPERIENCES.md` |
| Opinion (O) | Beliefs with confidence | `OPINIONS.md` |
| Observation (S) | Synthesized summaries | `OBSERVATIONS.md` |

### Hindsight's 3 Operations

| Operation | Purpose | BB5 Implementation |
|-----------|---------|-------------------|
| RETAIN | Structured ingestion | Automated extraction pipeline |
| RECALL | Multi-strategy retrieval | Semantic + keyword + graph + temporal |
| REFLECT | Preference-conditioned reasoning | Belief updating system |

---

## Timeline

| Phase | Duration | Focus | Milestone |
|-------|----------|-------|-----------|
| Phase 1 | Week 1 | File structure | Templates created |
| Phase 2 | Week 2 | Infrastructure | Databases ready |
| Phase 3 | Week 3 | RETAIN | Extraction working |
| Phase 4 | Week 4 | RECALL | Search working |
| Phase 5 | Week 5 | REFLECT | Beliefs updating |
| Phase 6 | Week 6 | Integration | Full pipeline |

---

## Dependencies

### External
- PostgreSQL 14+ with pgvector extension
- Neo4j 5+ (already in use for RAPS)
- OpenAI API (for embeddings)
- Python 3.11+

### Internal
- Existing PostgreSQL TaskRegistry
- Existing Neo4j graph (RAPS)
- Existing task/run folder structure
- RALF hook system

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| pgvector performance issues | Medium | High | Benchmark early, consider Pinecone fallback |
| Embedding costs | Medium | Medium | Use text-embedding-3-small, cache aggressively |
| Complexity overrun | High | High | Phase-gate reviews, MVP first |
| Neo4j schema conflicts | Low | High | Test against existing RAPS graph |
| Backward compatibility | Low | Medium | Keep existing files untouched |

---

## Research Foundation

This plan is based on extensive research documented in:

- `knowledge/research/agent-memory-systems/hindsight-deep-dive.md`
- `knowledge/research/agent-memory-systems/two-buffers-theory.md`
- `knowledge/research/agent-memory-systems/memory-system-comparison.md`
- `knowledge/research/agent-memory-systems/blackbox5-memory-analysis.md`
- `knowledge/research/agent-memory-systems/hindsight-first-principles-analysis.md`

---

## Related Documents

- **Goal:** `goals/active/IG-008/goal.yaml`
- **Research:** `knowledge/research/agent-memory-systems/`
- **Action Plan:** `action-plans/hindsight-memory-integration/`
- **Integration Guide:** `plans/active/hindsight-memory-implementation/INTEGRATION.md`

## Related Systems

| System | Relationship | Integration |
|--------|--------------|-------------|
| Agent Swarm Memory | Hindsight extends the 3-layer architecture | Swarm orchestrator uses RECALL for pattern detection |
| Navigation System (bb5) | Hindsight adds memory commands | `bb5 memory:recall`, `bb5 memory:facts` |
| SessionStart Hook | Hindsight injects relevant memories | Layer 4: Relevant memories from RECALL |
| Continuous Architecture Evolution | Hindsight enables memory-driven improvements | Query past patterns to guide improvements |
| IG-006 (Restructure) | Must complete before Hindsight rollout | New templates must fit restructured layout |
