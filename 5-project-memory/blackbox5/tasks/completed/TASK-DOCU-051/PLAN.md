# PLAN.md: Goals System Guide References Non-Existent Files

**Task ID:** TASK-DOCU-051
**Status:** Planning
**Priority:** LOW
**Created:** 2026-02-05
**Estimated Effort:** 30 minutes
**Source:** Scout opportunity docs-010 (Score: 5.0)

---

## 1. First Principles Analysis

### Why Verify Documentation?

1. **Accuracy**: Documentation must match actual structure
2. **Trust**: Broken references reduce confidence
3. **Onboarding**: New users follow documentation
4. **Maintenance**: Clear docs reduce support burden

### What Happens With Broken References?

| Problem | Impact | Severity |
|---------|--------|----------|
| Confusion | Users can't find referenced files | Medium |
| Errors | Scripts fail when files missing | High |
| Wasted time | Searching for non-existent files | Medium |
| Documentation drift | Docs become unreliable | Medium |

### How Should Documentation Be Verified?

**Systematic Audit:**
- Check all file references in documentation
- Verify paths match actual structure
- Update or remove broken references
- Establish validation process

---

## 2. Current State Assessment

### Document Location

**File:** `.docs/goals-system-guide.md`

**Referenced Paths to Verify:**

| Reference | Expected Location | Status |
|-----------|-------------------|--------|
| `goals/INDEX.yaml` | `goals/INDEX.yaml` | TBD |
| `goals/core/core-goals.yaml` | `goals/core/core-goals.yaml` | TBD |
| `goals/active/IG-XXX/goal.yaml` | Pattern check | TBD |
| `goals/templates/goal-template.yaml` | `goals/templates/goal-template.yaml` | TBD |
| `goals/README.md` | `goals/README.md` | TBD |

### Goals Directory Structure

**Expected:**
```
goals/
├── README.md
├── INDEX.yaml
├── core/
│   └── core-goals.yaml
├── active/
│   └── IG-XXX/
│       ├── goal.yaml
│       ├── timeline.yaml
│       └── journal/
├── completed/
│   └── IG-XXX/
└── templates/
    └── goal-template.yaml
```

**Need to verify actual structure matches.**

---

## 3. Proposed Solution

### Verification Strategy

1. **Extract all file references**
   - Parse goals-system-guide.md
   - List all paths mentioned
   - Note line numbers

2. **Verify each reference**
   - Check if file exists
   - Verify content matches description
   - Note any discrepancies

3. **Fix issues**
   - Update paths if files moved
   - Remove references if files deleted
   - Create files if they should exist
   - Update documentation to match reality

---

## 4. Implementation Plan

### Phase 1: Extract References (10 min)

1. **Parse documentation**
   ```bash
   grep -n "goals/" .docs/goals-system-guide.md
   ```

2. **List all referenced paths**
   - File paths
   - Directory patterns
   - Example paths

3. **Categorize references**
   - Critical (required for function)
   - Examples (illustrative)
   - Optional (nice to have)

### Phase 2: Verify Existence (10 min)

1. **Check file existence**
   ```bash
   for file in $(extracted_paths); do
     if [ -e "$file" ]; then echo "EXISTS: $file"
     else echo "MISSING: $file"; fi
   done
   ```

2. **Verify directory structure**
   - Check goals/ structure
   - Verify active/ and completed/ contents
   - Check templates/

3. **Document findings**
   - List of broken references
   - List of missing files
   - Structural differences

### Phase 3: Fix Issues (10 min)

1. **Update documentation**
   - Fix incorrect paths
   - Remove references to deleted files
   - Add notes for optional files

2. **Create missing files (if needed)**
   - goals/README.md if missing
   - goals/INDEX.yaml if missing
   - Template files if missing

3. **Verify fixes**
   - Re-check all references
   - Test any example commands
   - Confirm structure matches docs

---

## 5. Success Criteria

- [ ] All file references extracted
- [ ] Each reference verified against actual structure
- [ ] Broken references fixed or removed
- [ ] Missing files created (if appropriate)
- [ ] Documentation accurately reflects structure
- [ ] Example commands tested and working

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Extract | 10 min | 10 min |
| Phase 2: Verify | 10 min | 20 min |
| Phase 3: Fix | 10 min | 30 min |
| **Total** | **30 min** | **~30 min** |

---

## 7. Rollback Strategy

If changes cause issues:

1. **Immediate:** Restore original from git
   ```bash
   git checkout -- .docs/goals-system-guide.md
   ```

2. **Review:** Compare changes with original
3. **Re-apply:** Make corrected changes

---

## 8. Files to Modify/Create

### Modified Files

| File | Changes | Lines |
|------|---------|-------|
| `.docs/goals-system-guide.md` | Fix broken references | ~10-20 |

### Potentially Created Files

| File | Purpose | If Missing |
|------|---------|------------|
| `goals/README.md` | Goals overview | Create |
| `goals/INDEX.yaml` | Auto-generated index | Create or generate |
| `goals/templates/goal-template.yaml` | Template for new goals | Create |

---

## 9. Verification Checklist

**File References:**
- [ ] goals/INDEX.yaml exists or is generated
- [ ] goals/core/core-goals.yaml exists
- [ ] goals/active/ structure matches docs
- [ ] goals/completed/ structure matches docs
- [ ] goals/templates/goal-template.yaml exists
- [ ] goals/README.md exists

**Example Commands:**
- [ ] `cat goals/INDEX.yaml` works
- [ ] `cd goals/active` works
- [ ] Template copy commands work

---

*Plan created: 2026-02-06*
*Ready for implementation*
