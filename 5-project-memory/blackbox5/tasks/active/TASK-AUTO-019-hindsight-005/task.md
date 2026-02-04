---
task_id: TASK-HINDSIGHT-005
title: "Implement REFLECT Operation"
linked_goal: IG-008
linked_sub_goal: SG-008-5
linked_plan: PLAN-HINDSIGHT-001
status: pending
priority: high
created: "2026-02-04"
---

# TASK-HINDSIGHT-005: Implement REFLECT Operation

**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-04

---

## Objective

Build preference-conditioned reasoning system (REFLECT operation) with disposition profiles, belief updating, and confidence tracking.

---

## Context

REFLECT is Hindsight's reasoning operation. It enables:
- **Disposition profiles** - Skepticism, literalism, empathy, bias settings
- **Belief updating** - Update opinions based on new evidence
- **Confidence tracking** - Adjust confidence scores as evidence accumulates
- **Consistent personality** - Agent behaves consistently across sessions

This is what gives agents "continuity of self" - they maintain and evolve their beliefs.

---

## Success Criteria

- [ ] Disposition profiles working (skepticism, literalism, empathy, bias)
- [ ] Belief updating working (update opinions with new evidence)
- [ ] Confidence tracking working (adjust scores based on evidence quality)
- [ ] Integration with RECALL working (context-aware reasoning)
- [ ] Consistent agent personality demonstrated across sessions
- [ ] Contradiction detection and resolution working

---

## Approach

1. **Disposition Profiles:**
   - Create profile system in `.autonomous/memory/profiles/`
   - Implement skepticism (evidence threshold)
   - Implement literalism (interpretation strictness)
   - Implement empathy (user preference weighting)
   - Implement bias (confirmation vs exploration)

2. **Belief Updating:**
   - Create belief.py with update logic
   - Evidence accumulation tracking
   - Confidence score calculation
   - Contradiction detection

3. **Integration:**
   - Hook into RECALL for context-aware reasoning
   - Update OPINIONS.md when beliefs change
   - Log belief evolution in journal

4. **Personality:**
   - Persist disposition preferences
   - Apply profiles to all reasoning
   - Demonstrate consistency across tasks

---

## Files to Create/Modify

- `.autonomous/memory/operations/reflect.py` (new)
- `.autonomous/memory/belief.py` (new)
- `.autonomous/memory/profiles/disposition.py` (new)
- `.autonomous/memory/profiles/default.yaml` (new)
- OPINIONS.md template (update with confidence format)

---

## Dependencies

- [ ] TASK-HINDSIGHT-004 (RECALL must be working for context)

---

## Notes

- Start with simple confidence tracking, add complexity incrementally
- Document how disposition profiles affect behavior
- Allow users to configure agent personality
- Track belief evolution over time
