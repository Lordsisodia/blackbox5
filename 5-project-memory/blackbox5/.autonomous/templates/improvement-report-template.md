# Improvement Validation Report Template

**Report ID:** IMP-VAL-{TIMESTAMP}
**Generated:** {DATE}
**Validator:** {AGENT/USER}
**Improvement ID:** {IMP-XXXX}

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Improvement ID | {IMP-XXXX} |
| Category | {process/infrastructure/guidance/technical} |
| Implementation Date | {YYYY-MM-DD} |
| Validation Date | {YYYY-MM-DD} |
| Overall Status | {improved/stable/degraded/insufficient_data} |
| Effectiveness Score | {0-100}% |

---

## Improvement Details

### Original Problem Statement
{Describe the problem this improvement was meant to solve}

### Expected Impact
{What was the expected outcome?}

### Implementation Summary
{What was actually implemented?}

---

## Before/After Metrics

### Primary Metrics

| Metric | Before | After | Change | Target Met? |
|--------|--------|-------|--------|-------------|
| {Metric 1} | {value} | {value} | {±X%} | {✓/✗} |
| {Metric 2} | {value} | {value} | {±X%} | {✓/✗} |
| {Metric 3} | {value} | {value} | {±X%} | {✓/✗} |

### Secondary Metrics

| Metric | Before | After | Change | Notes |
|--------|--------|-------|--------|-------|
| {Metric 4} | {value} | {value} | {±X%} | |
| {Metric 5} | {value} | {value} | {±X%} | |

---

## Category-Specific Validation

### For Process Improvements

- [ ] Task completion time measured
- [ ] Error rate tracked
- [ ] User workflow efficiency assessed
- [ ] Documentation of time savings

**Time Savings Calculation:**
- Average time per task before: {X} minutes
- Average time per task after: {Y} minutes
- Time saved per task: {X-Y} minutes
- Tasks per week: {Z}
- Weekly time savings: {(X-Y)*Z} minutes

### For Infrastructure Improvements

- [ ] System health metrics captured
- [ ] Error rates compared
- [ ] Performance benchmarks run
- [ ] Reliability metrics tracked

**System Health Impact:**
- Error rate before: {X}%
- Error rate after: {Y}%
- Improvement: {X-Y}%

### For Guidance Improvements

- [ ] Confusion markers tracked
- [ ] Documentation usage measured
- [ ] Support requests analyzed
- [ ] User feedback collected

**Clarity Improvement:**
- Confusion instances before: {X}
- Confusion instances after: {Y}
- Improvement: {X-Y} instances

### For Technical Improvements

- [ ] Code quality metrics measured
- [ ] Performance benchmarks run
- [ ] Bug reports tracked
- [ ] Maintenance effort assessed

**Code Quality Impact:**
- Issues before: {X}
- Issues after: {Y}
- Improvement: {X-Y} issues

---

## Validation Methodology

### Data Collection Period
- **Before Period:** {Start Date} to {End Date}
- **After Period:** {Start Date} to {End Date}
- **Sample Size:** {N} tasks/runs/observations

### Data Sources
- [ ] Run metrics (metrics.json files)
- [ ] Task completion records
- [ ] Error logs
- [ ] Learning files (LEARNINGS.md)
- [ ] User feedback
- [ ] Automated tests

### Statistical Significance
- **Confidence Level:** {95%}
- **P-value:** {if applicable}
- **Effect Size:** {small/medium/large}

---

## Findings

### What Worked Well
1. {Finding 1}
2. {Finding 2}
3. {Finding 3}

### What Didn't Work
1. {Issue 1}
2. {Issue 2}

### Unexpected Outcomes
- {Unexpected positive outcome}
- {Unexpected negative outcome}

---

## Actual vs Estimated Impact

| Aspect | Estimated | Actual | Variance |
|--------|-----------|--------|----------|
| Time Savings | {X} min/task | {Y} min/task | {Y-X} min |
| Implementation Effort | {X} hours | {Y} hours | {Y-X} hours |
| User Impact | {High/Med/Low} | {High/Med/Low} | {match/variance} |
| ROI | {X}x | {Y}x | {Y-X}x |

---

## Recommendations

### For This Improvement
- [ ] Mark as validated and effective
- [ ] Mark as validated but needs refinement
- [ ] Mark as not effective - consider rollback
- [ ] Needs more data - extend validation period

### For Future Improvements
1. {Recommendation 1}
2. {Recommendation 2}
3. {Recommendation 3}

---

## Action Items

- [ ] {Action item 1}
- [ ] {Action item 2}
- [ ] {Action item 3}

---

## Appendix

### Raw Data
```yaml
# Before metrics
before:
  metric_1: value
  metric_2: value

# After metrics
after:
  metric_1: value
  metric_2: value
```

### Supporting Evidence
- {Link to relevant files}
- {Link to related tasks}
- {Link to documentation}

---

**Validation Completed By:** _______________
**Date:** _______________
**Next Review Date:** _______________
