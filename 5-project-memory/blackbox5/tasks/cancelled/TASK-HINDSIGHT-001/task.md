---
task_id: TASK-HINDSIGHT-001
title: "Establish 4-Network Memory Foundation"
linked_goal: IG-008
linked_sub_goal: SG-008-1
linked_plan: PLAN-HINDSIGHT-001
status: pending
priority: high
created: "2026-02-04"
---

# TASK-HINDSIGHT-001: Establish 4-Network Memory Foundation

**Type:** implement
**Priority:** high
**Status:** cancelled
**Created:** 2026-02-04

---

## Objective

Create FACTS.md, EXPERIENCES.md, OPINIONS.md, OBSERVATIONS.md templates and integrate them into the task/run structure. This establishes the foundation for Hindsight's 4-network memory architecture in Blackbox5.

---

## Context

Hindsight's memory architecture uses 4 distinct networks:
- **World (W):** Objective facts about the world
- **Experience (B):** First-person actions and experiences
- **Opinion (O):** Beliefs with confidence scores
- **Observation (S):** Synthesized summaries and insights

BB5 currently has THOUGHTS.md, DECISIONS.md, LEARNINGS.md. We need to add the 4 Hindsight memory files alongside these.

---

## Success Criteria

- [ ] 4 new memory file templates created (FACTS.md, EXPERIENCES.md, OPINIONS.md, OBSERVATIONS.md)
- [ ] Task and run templates updated to include new memory files
- [ ] Project-level memory structure established in `.autonomous/memory/`
- [ ] Documentation complete explaining each memory type
- [ ] Backward compatibility verified with existing THOUGHTS.md/DECISIONS.md

---

## Approach

1. Create `.templates/memory/FACTS.md` - Template for objective facts
2. Create `.templates/memory/EXPERIENCES.md` - Template for first-person experiences
3. Create `.templates/memory/OPINIONS.md` - Template for beliefs with confidence
4. Create `.templates/memory/OBSERVATIONS.md` - Template for synthesized observations
5. Update task template to include new memory files
6. Update run template to include new memory files
7. Create `.autonomous/memory/config.yaml` for memory configuration
8. Document the purpose and usage of each memory type

---

## Files to Create/Modify

- `.templates/memory/FACTS.md` (new)
- `.templates/memory/EXPERIENCES.md` (new)
- `.templates/memory/OPINIONS.md` (new)
- `.templates/memory/OBSERVATIONS.md` (new)
- `.templates/task/TASK.md` (update)
- `.templates/run/RUN.md` (update)
- `.autonomous/memory/config.yaml` (new)

---

## Dependencies

- None (can start immediately)

---

## Notes

- Keep templates simple and consistent with existing BB5 style
- Ensure backward compatibility - existing tasks/runs should work without these files
- Document the relationship between existing files (THOUGHTS.md) and new files (EXPERIENCES.md)
