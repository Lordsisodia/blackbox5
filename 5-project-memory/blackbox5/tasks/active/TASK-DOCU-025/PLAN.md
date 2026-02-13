# PLAN.md: Skill Metrics Documentation Drift

**Task:** TASK-DOCU-025 - Skill Metrics Documentation Drift - Zero Usage Data  
**Status:** Draft  
**Created:** 2026-02-06  
**Importance:** 75/100  
**Estimated Effort:** 4-6 hours

---

## 1. First Principles Analysis

### Why Does Documentation Drift Happen?

1. **Implementation Outpaces Documentation**
2. **No Automated Sync**
3. **Unclear Ownership**
4. **Multiple Sources of Truth**
5. **Lack of Validation**

### Impact of Drift

| Impact Area | Consequence | Severity |
|-------------|-------------|----------|
| Trust | Users lose confidence | High |
| Adoption | Skills underutilized | High |
| Decision Quality | Poor skill selection | Medium |
| Compliance | Phase 1.5 skipped | High |

### How to Keep Docs Synchronized

1. **Single Source of Truth**
2. **Automated Derivation**
3. **Validation Scripts**
4. **Integration Points**
5. **Regular Audits**

---

## 2. Current State Assessment

### Documentation Files

| File | Purpose | Status |
|------|---------|--------|
| skill-metrics-guide.md | Understanding metrics | Active |
| skill-tracking-guide.md | Tracking usage | Active |
| skill-selection.yaml | Selection framework | Active |
| CLAUDE.md | User instructions | Active |

### Implementation Files

| File | Purpose | Status |
|------|---------|--------|
| skill-metrics.yaml | **ZERO USAGE DATA** | Empty |
| skill-usage.yaml | **ZERO USAGE DATA** | Empty |
| log-skill-usage.py | Logger | Not integrated |
| validate-skill-usage.py | Validation | Not integrated |

### The Drift

**Documentation Describes:**
- Comprehensive tracking system
- Weekly calculations
- Effectiveness scores
- Automated tracking

**Reality:**
- 22 skills with `usage_count: 0`
- All metrics `null`
- Only 1 test entry
- Automation not integrated

---

## 3. Proposed Solution

### Decision: Implement Automated Tracking

Rather than updating docs to reflect zero usage, **implement the automated system**.

### Solution Components

1. **Integrate Logging Hook**
2. **Enable Validation**
3. **Run Initial Calculation**
4. **Create Sync Process**
5. **Establish Maintenance**

---

## 4. Implementation Plan

### Phase 1: Audit Drift (30 min)

1. Compare documented vs implemented
2. Identify unused automation
3. Document integration gaps

### Phase 2: Integrate Logging (60 min)

1. Find task completion hook point
2. Add call to `log-skill-on-complete.py`
3. Test integration

### Phase 3: Enable Validation (45 min)

1. Add to quality gates
2. Update validation checklist
3. Create report format

### Phase 4: Calculate Metrics (30 min)

1. Run `calculate-skill-metrics.py`
2. Verify calculations
3. Adjust baselines

### Phase 5: Create Sync Process (45 min)

1. Document sync process
2. Define triggers
3. Create verification

### Phase 6: Document Maintenance (30 min)

1. Define responsibilities
2. Create schedule
3. Write troubleshooting

---

## 5. Success Criteria

- [x] Drift documented
- [x] Automation integrated
- [ ] Validation enabled (deferred - future enhancement)
- [ ] Metrics calculated (deferred - need historical THOUGHTS.md files)
- [ ] Sync process established (deferred - needs more historical data)

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Audit | 30 min | 30 min |
| Phase 2: Logging | 60 min | 90 min |
| Phase 3: Validation | 45 min | 135 min |
| Phase 4: Metrics | 30 min | 165 min |
| Phase 5: Sync | 45 min | 210 min |
| Phase 6: Docs | 30 min | 240 min |
| **Total** | **4 hours** | |

---

## 7. Implementation Summary (2026-02-13)

**Completed:** Phase 2 - Integrate Logging

**What Was Done:**
1. ✅ Integrated `log-skill-on-complete.py` into task completion workflow
2. ✅ Updated `post-task-complete.sh` to call skill logging hook
3. ✅ Added optional `run_dir` argument for skill logging
4. ✅ Implemented graceful failure handling (skill logging is non-critical)

**Impact:**
- Skill usage tracking is now automatically called when tasks complete
- System is backward compatible - works with or without run directories
- Failed skill logging doesn't break task completion

**What Was Deferred:**
- Phase 3: Enable Validation (future enhancement)
- Phase 4: Calculate Metrics (needs historical data)
- Phase 5: Create Sync Process (needs more historical data)
- Phase 6: Document Maintenance (can be done as needed)

**Reason for Deferral:**
The core integration is complete. The remaining phases require more historical
THOUGHTS.md files and established workflows before metrics calculation and
validation make sense. The foundation is now in place for future enhancements.

**Next Steps for Future Work:**
1. Enable RALF autonomous system to pass run_dir to post-task-complete hook
2. Add skill usage sections to existing THOUGHTS.md files
3. Implement validation scripts for skill usage data quality
4. Run metrics calculation once sufficient data is collected

---

*Plan created based on documentation drift analysis*
