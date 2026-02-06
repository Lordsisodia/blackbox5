# PLAN.md: Task System Design References Non-Existent Files

**Task ID:** TASK-DOCU-044  
**Status:** Planning  
**Priority:** LOW  
**Estimated Effort:** 65 minutes  
**Importance Rating:** 45/100  
**Created:** 2026-02-06

---

## 1. First Principles Analysis

### Why is Documentation Accuracy Important?

- **Source of Truth**: Documentation guides system understanding
- **Time Savings**: Accurate docs prevent hunting for phantom files
- **Trust**: Inaccuracies erode confidence in all documentation
- **Prevention**: Stops cascading errors from incorrect assumptions

### What Happens with Broken References?

1. **Wasted Investigation Time**
2. **Broken Trust**
3. **Implementation Errors**
4. **Maintenance Burden**

### How to Prevent Broken References?

1. Automated validation scripts
2. CI/CD integration
3. Regular documentation audits
4. Clear naming conventions

---

## 2. Current State Assessment

### Broken References Found

| Document | Reference | Issue |
|----------|-----------|-------|
| task-system-design.md | `tasks.yaml` | **DOES NOT EXIST** |
| task-system-design.md | `queue.yaml` path | Wrong location |
| blackbox5-architecture.md | `queue.yaml` path | Missing `agents/` |

### File Existence

| File | Expected | Actual | Status |
|------|----------|--------|--------|
| tasks.yaml | `.autonomous/communications/` | **NOT FOUND** | MISSING |
| queue.yaml | `.autonomous/communications/` | `.autonomous/agents/communications/` | WRONG PATH |

**Key Finding:** `task-system-design.md` describes dual-file system that was never implemented.

---

## 3. Proposed Solution

### Option A: Create Missing tasks.yaml (Recommended)

- Implement as designed
- Update all path references
- Maintain dual-file architecture

### Option B: Update Documentation Only

- Remove tasks.yaml references
- Update queue.yaml paths
- Document single-file architecture

**Decision:** Option A - preserve designed architecture.

---

## 4. Implementation Plan

### Phase 1: Audit References (15 min)

1. Search all `.docs/` for `tasks.yaml`
2. Search for `queue.yaml` references
3. Search for `.autonomous/communications/` paths
4. Create list of files needing updates

### Phase 2: Verify Existence (5 min)

1. Confirm tasks.yaml doesn't exist
2. Confirm queue.yaml location
3. Check for script dependencies

### Phase 3: Fix References (20 min)

1. **Create tasks.yaml** at `.autonomous/agents/communications/`
2. Update task-system-design.md (lines 119-120)
3. Update blackbox5-architecture.md (lines 66, 86, 95, 98, 482)
4. Verify task-queue-implementation.md

### Phase 4: Create Validation Script (15 min)

Create `validate-doc-references.py`:
- Scan docs for file references
- Validate existence
- Report broken links

### Phase 5: Document Maintenance (10 min)

1. Add validation to pre-commit hooks
2. Create MAINTENANCE.md
3. Document file location standards

---

## 5. Success Criteria

- [ ] All documentation audited
- [ ] tasks.yaml created at correct location
- [ ] All path references updated
- [ ] Validation script created
- [ ] No broken references remain

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Audit | 15 min | 15 min |
| Phase 2: Verify | 5 min | 20 min |
| Phase 3: Fix | 20 min | 40 min |
| Phase 4: Validation | 15 min | 55 min |
| Phase 5: Docs | 10 min | 65 min |
| **Total** | **65 min** | **~1 hour** |

---

*Plan created based on documentation reference analysis*
