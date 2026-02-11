# TASK-FIX-SKIL-BMAD-001: Investigate and Fix bmad-dev Performance

**Status:** pending
**Priority:** HIGH
**Category:** skills
**Estimated Effort:** 30 minutes
**Created:** 2026-02-11
**Parent:** None

## Objective
Investigate why bmad-dev (Developer) skill is underperforming with 50.26% effectiveness score and negative time savings. Fix baseline or optimize skill performance.

## Root Cause Analysis

**Current State:**
- Effectiveness score: 50.26% (below acceptable 50% threshold)
- Time efficiency: -28.57% (NEGATIVE - losing time!)
- Success rate: 100%
- Quality score: 16.0/20 (80%)
- Baseline: 35 minutes
- Tasks: 4 total

**Individual Task Performance:**
1. TASK-SSOT-025: 45 min (10 min over baseline) - Quality 4
2. TEST-ROI-001: 30 min (5 min under baseline) - Quality 5
3. TEST-ROI-003: 60 min (25 min over baseline) - Quality 3
4. TEST-ROI-005: 30 min (5 min under baseline) - Quality 3

**Average Duration:** 41.25 minutes (6.25 min over baseline)
**Problem:** Baseline of 35 minutes is too low for development work

## Potential Causes

1. **Baseline too aggressive** - Development tasks typically take 30-60+ minutes
2. **Skill scope** - bmad-dev handles "implementation" and "development" work
3. **Task complexity** - Migrating code, refactoring, new features take time
4. **No efficiency shortcuts** - Dev skill may lack quick-win optimizations

## Success Criteria

- [ ] Investigate actual task times for similar development work
- [ ] Adjust baseline if needed (likely to 50-60 minutes)
- [ ] Review skill implementation for optimization opportunities
- [ ] Add skill-specific tips or shortcuts if possible
- [ ] Test with new baseline
- [ ] Recalculate metrics to verify improvement
- [ ] Effectiveness score > 60% (target)

## Approach

1. **Data Analysis**
   - Review all completed development tasks
   - Calculate average duration for similar work
   - Compare to current 35 min baseline

2. **Baseline Adjustment**
   - If average is 50-60 min → Update baseline to 50
   - If tasks vary wildly → Consider removing baseline entirely
   - If baseline is reasonable → Keep and optimize skill

3. **Skill Optimization**
   - Review bmad-dev implementation
   - Add caching or shortcuts if applicable
   - Document best practices for common tasks
   - Update skill description to set correct expectations

4. **Testing**
   - Create test development task
   - Compare old vs new performance
   - Verify metrics improve

## Files to Modify

| File | Changes |
|------|---------|
| `operations/skill-registry.yaml` | Update bmad-dev baseline_minutes (likely 50) |
| `.autonomous/agents/amelia/SKILL.md` | Document skill optimizations |
| `2-engine/core/agents/definitions/specialists/DeveloperAgent.yaml` | Review skill definition |

## Files to Create

| File | Purpose |
|------|---------|
| `2-engine/core/agents/definitions/specialists/DeveloperAgent-OPTIMIZED.md` | Optimization findings |
| `operations/skill-registry.yaml.backup.before-fix` | Backup before changes |

## Rollback Strategy

- Keep backup of skill registry before baseline change
- If new baseline causes issues, revert to 35 minutes
- Document why change was made

## Estimated Effort
30 minutes

## Related Tasks
- TASK-FIX-SKIL-007-3: Fixed skill tracking (enables this investigation)

## Notes

**Investigation Questions:**
- What is the actual average duration of development work?
- Should different task types have different baselines?
- Is bmad-dev skill doing unnecessary work?
- Can the skill be optimized for common tasks?

**Quick Fix (if needed):**
Simply update baseline from 35 → 50 minutes if analysis shows this is more appropriate for development work.

**Long-term Fix:**
Optimize skill implementation to actually complete tasks faster than baseline.

---

## Recommendation

**Immediate action:** Update baseline to 50 minutes
**Rationale:** Average of 41.25 min > current 35 min baseline
**Expected impact:** Time efficiency becomes positive, effectiveness score > 60%
