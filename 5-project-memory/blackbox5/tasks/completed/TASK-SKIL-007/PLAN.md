# PLAN.md: All Skills Have Null Effectiveness Metrics

**Task ID:** TASK-SKIL-007  
**Status:** Planning  
**Priority:** HIGH  
**Category:** Skills  
**Estimated Effort:** 10 days  
**Importance Rating:** 85/100

---

## 1. First Principles Analysis

### Why Are Effectiveness Metrics Important?

**Decision Quality**: Enable data-driven skill selection
**Resource Allocation**: Identify which skills deserve investment
**Continuous Improvement**: Create feedback loop
**ROI Justification**: Demonstrate value quantitatively

### What Happens When Metrics Are Null?

**Current Impact:**
- All 22 skills show `effectiveness_score: null`
- All recommendations have `confidence: low`
- Category averages are null
- ROI shows zero time saved
- Skill selection is random

### How Can We Track Effectiveness?

**Data Collection Points:**
1. Task Start: Record skill selection
2. Task Execution: Track duration, complexity
3. Task Completion: Record outcome, quality
4. Periodic: Aggregate metrics

---

## 2. Current State Assessment

### Existing Infrastructure

**Metrics Schema:**
- 22 skills across 5 categories
- Weighted composite formula:
  - Success Rate: 35%
  - Time Efficiency: 25%
  - Trigger Accuracy: 20%
  - Quality Score: 15%
  - Reuse Rate: 5%

**Tracking Infrastructure:**
- `calculate-skill-metrics.py` (580 lines)
- `log-skill-usage.py` (361 lines)
- `validate-skill-usage.py` (432 lines)
- `task_completion_skill_recorder.py` (hook)

### Root Cause

**The Problem:** Skills are defined but not invoked.

**Evidence:**
```yaml
task_outcomes:
  - task_id: TASK-XXX
    skill_used: null  # All entries
```

**Why:**
1. Confidence threshold too high
2. Skill awareness low
3. No enforcement
4. No visible benefit

---

## 3. Proposed Solution

### Effectiveness Tracking Schema

```yaml
task_outcomes:
  - task_id: "TASK-XXX"
    skill_used: "bmad-dev"
    duration_minutes: 25
    baseline_minutes: 35
    outcome: "success"
    quality_rating: 4
    trigger_was_correct: true
    would_use_again: true
    confidence_at_selection: 85
```

### Automatic Metrics Collection

**Collection Points:**
1. Pre-Execution (THOUGHTS.md)
2. Post-Execution (RESULTS.md)
3. Task Completion Hook

### Reporting Dashboard

**Real-time Dashboard:**
```bash
$ bb5 skill-dashboard
Top Skills: bmad-dev 85%, bmad-architect 82%
Category: agent 72%, protocol 68%
ROI: 450 minutes saved, 3.2x benefit
```

---

## 4. Implementation Plan

### Phase 1: Define Metrics (Day 1)

1. Review and finalize schema
2. Validate baseline minutes
3. Document methodology

### Phase 2: Create Infrastructure (Days 2-3)

1. Enhance task outcome schema
2. Create skill usage logging hook
3. Implement metrics scheduler
4. Create validation script

### Phase 3: Implement Collection (Days 4-5)

1. Integrate logging into workflow
2. Create skill invocation tracking
3. Implement baseline tracking
4. Add quality rating capture

### Phase 4: Create Dashboard (Days 6-7)

1. Create `bb5 skill-dashboard`
2. Implement trend visualization
3. Create automated reporting
4. Add anomaly alerting

### Phase 5: Test and Refine (Days 8-10)

1. End-to-end testing
2. Threshold calibration
3. Documentation updates
4. Rollout and training

---

## 5. Success Criteria

### Phase 1
- [ ] All 5 component metrics documented
- [ ] Weighted formula validated
- [ ] Baseline minutes validated

### Phase 2-3
- [ ] `task_outcomes` include non-null `skill_used`
- [ ] Automatic logging working
- [ ] Phase 1.5 compliance validation

### Phase 4
- [ ] `bb5 skill-dashboard` functional
- [ ] Trend visualization working
- [ ] Weekly reports auto-generated

### Phase 5
- [ ] 50+ tasks tracked
- [ ] All 22 skills have scores
- [ ] No null values

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Define | 1 day | Day 1 |
| Phase 2: Infrastructure | 2 days | Day 3 |
| Phase 3: Collection | 2 days | Day 5 |
| Phase 4: Dashboard | 2 days | Day 7 |
| Phase 5: Test | 3 days | Day 10 |
| **Total** | **10 days** | **2 weeks** |

---

*Plan created based on skill metrics analysis*
