# TASK-FIX-SKIL-032-3: Build Automated ROI Calculation Pipeline

**Status:** pending
**Priority:** HIGH
**Category:** skills
**Estimated Effort:** 75 minutes
**Created:** 2026-02-09T12:00:00Z
**Parent:** TASK-SKIL-032

---

## Objective

Build an automated pipeline that calculates skill ROI using the time tracking data and A/B comparisons, producing actionable effectiveness scores.

---

## Success Criteria

- [ ] ROI calculation formula implemented in code
- [ ] Pipeline automatically processes task_outcomes data
- [ ] Effectiveness scores calculated for all skills with usage data
- [ ] Pipeline outputs report with per-skill ROI metrics
- [ ] Underperforming skills (<50% effectiveness) identified
- [ ] Pipeline can run on-demand and incrementally
- [ ] Results are written back to `operations/skill-metrics.yaml`

---

## Context

**Root Cause:** SKIL-032 identified that ROI calculation is impossible without invocation data. This task builds the pipeline to perform the calculation once data is available.

**Current Gap:**
- `bin/calculate-skill-metrics.py` exists but may not integrate with new tracking data
- No automated pipeline to go from raw task data -> ROI metrics
- Effectiveness scores in `skill-metrics.yaml` are all null

**ROI Formula (from skill-metrics.yaml):**
```
effectiveness_score = weighted_average(
  success_rate * 0.35,
  time_efficiency * 0.25,
  trigger_accuracy * 0.20,
  quality_score * 0.15,
  reuse_rate * 0.05
)

time_efficiency = (estimated_baseline - actual_duration) / estimated_baseline * 100
```

**Key Files:**
- `bin/calculate-skill-metrics.py` - Existing calculator
- `operations/skill-metrics.yaml` - Schema and data storage
- `operations/skill-usage.yaml` - Usage tracking

---

## Approach

1. **Review existing calculator**
   - Read `bin/calculate-skill-metrics.py`
   - Understand current calculation logic
   - Identify integration points

2. **Enhance calculator for incremental updates**
   - Add `--incremental` mode to process only new tasks
   - Add `--full` mode to recalculate all metrics
   - Integrate with task_outcomes from skill-metrics.yaml

3. **Implement ROI calculation**
   - Parse task_outcomes array
   - Group by skill_used
   - Calculate per-skill metrics:
     - Average time_saved_minutes
     - Success rate
     - Trigger accuracy (would_use_again)
   - Apply weights to compute effectiveness_score

4. **Create automated pipeline script**
   - `bin/skill-roi-pipeline.py`
   - Reads task_outcomes
   - Calculates metrics
   - Updates skill-metrics.yaml
   - Generates report

5. **Add reporting capabilities**
   - Per-skill effectiveness score
   - Time savings summary
   - Underperforming skills list
   - Recommendations for skill threshold adjustments

6. **Test the pipeline**
   - Run with existing test data
   - Verify calculations are correct
   - Check output format

---

## Files to Modify

| File | Changes |
|------|---------|
| `bin/calculate-skill-metrics.py` | Add incremental mode, integrate with task_outcomes |
| `operations/skill-metrics.yaml` | Update schema if needed for calculated fields |

## Files to Create

| File | Purpose |
|------|---------|
| `bin/skill-roi-pipeline.py` | Main pipeline orchestrator |
| `bin/skill-effectiveness-dashboard.py` | Real-time dashboard display |
| `.docs/skill-roi-calculation.md` | Documentation for ROI methodology |

---

## Rollback Strategy

If changes cause issues:
1. Restore skill-metrics.yaml from git backup
2. Disable pipeline execution
3. Revert to manual metric calculation

---

## Notes

- Pipeline should handle missing data gracefully (null checks)
- Consider adding data validation before calculation
- Document the weighting rationale (why 35% for success_rate, etc.)
- Add logging for pipeline execution
