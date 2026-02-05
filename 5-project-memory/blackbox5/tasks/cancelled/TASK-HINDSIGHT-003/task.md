---
task_id: TASK-HINDSIGHT-003
title: "Implement RETAIN Operation"
linked_goal: IG-008
linked_sub_goal: SG-008-3
linked_plan: PLAN-HINDSIGHT-001
status: pending
priority: high
created: "2026-02-04"
---

# TASK-HINDSIGHT-003: Implement RETAIN Operation

**Type:** implement
**Priority:** high
**Status:** cancelled
**Created:** 2026-02-04

---

## Objective

Build automated extraction pipeline (RETAIN operation) that processes tasks/runs and populates the 4 memory networks (World, Experience, Opinion, Observation).

---

## Context

RETAIN is Hindsight's structured ingestion operation. It extracts:
- **Entities** - People, places, concepts mentioned
- **Facts** - Objective statements about the world (World network)
- **Experiences** - First-person actions taken (Experience network)
- **Opinions** - Beliefs formed with confidence (Opinion network)
- **Observations** - Synthesized insights (Observation network)

The RETAIN operation runs automatically when tasks are completed.

---

## Success Criteria

- [ ] Entity extraction working (named entity recognition)
- [ ] Fact extraction working (objective statements)
- [ ] Opinion extraction working (beliefs with confidence)
- [ ] Experience extraction working (first-person actions)
- [ ] PostgreSQL storage working for all memory types
- [ ] Neo4j graph population working for entities and relationships
- [ ] Automation workflow triggered on task completion
- [ ] >90% task coverage achieved (most tasks processed)

---

## Approach

1. **Extraction Pipeline:**
   - Create retain.py with extraction logic
   - Implement entity extraction using LLM
   - Implement fact/opinion/experience/observation classification
   - Use structured output (JSON) for reliability

2. **Storage Pipeline:**
   - Store memories in PostgreSQL with embeddings
   - Store entities and relationships in Neo4j
   - Link memories to source tasks/runs
   - Handle duplicates and updates

3. **Automation:**
   - Hook into task completion workflow
   - Process THOUGHTS.md → EXPERIENCES.md
   - Process DECISIONS.md → FACTS.md + OPINIONS.md
   - Process LEARNINGS.md → OBSERVATIONS.md

4. **Testing:**
   - Unit tests for each extraction type
   - Integration tests for full pipeline
   - Coverage metrics

---

## Files to Create/Modify

- `.autonomous/memory/operations/retain.py` (new)
- `.autonomous/memory/extractors/entity_extractor.py` (new)
- `.autonomous/memory/extractors/fact_extractor.py` (new)
- `.autonomous/memory/extractors/opinion_extractor.py` (new)
- `.autonomous/memory/extractors/experience_extractor.py` (new)
- `.autonomous/memory/models.py` (new - data models)
- RALF hooks for task completion (modify)

---

## Dependencies

- [ ] TASK-HINDSIGHT-002 (Infrastructure must be ready)

---

## Notes

- Use LLM for extraction with structured JSON output
- Maintain confidence scores for extracted information
- Handle contradictions (same entity, different properties)
- Log extraction coverage metrics
