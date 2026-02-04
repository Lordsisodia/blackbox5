# TASK-ARCH-010: Implement Skill Metrics Collection

**Status:** in_progress
**Priority:** MEDIUM
**Created:** 2026-02-04
**Estimated:** 60 minutes
**Goal:** IG-007
**Plan:** PLAN-ARCH-001

---

## Objective

Implement automatic population of `operations/skill-metrics.yaml` to measure skill effectiveness.

---

## Success Criteria

- [ ] Create metrics collection mechanism
- [ ] Track success/failure per skill
- [ ] Track time efficiency per skill
- [ ] Track trigger accuracy
- [ ] Generate effectiveness reports

---

## Current State

`operations/skill-metrics.yaml` has null values for all 12 skills.

---

## Metrics to Track

1. **effectiveness_score** (0-100) - Overall usefulness
2. **success_rate** (percentage) - Tasks completed / Total tasks
3. **time_efficiency** (ratio) - Estimated / Actual time
4. **trigger_accuracy** (percentage) - Correct triggers / Total
5. **usage_count** (number) - How many times used
6. **last_used** (date) - Most recent usage

---

## Implementation

Create `bin/collect-skill-metrics.py`:
- Parse task files for skill usage
- Calculate metrics automatically
- Update skill-metrics.yaml

---

## Deliverable

- `bin/collect-skill-metrics.py`
- `bin/generate-skill-report.py`
- Populated skill-metrics.yaml
- Documentation
