# PLAN.md: Inconsistent Directory Structure Documentation

**Task ID:** TASK-DOCU-034  
**Status:** Planning  
**Priority:** MEDIUM  
**Importance Rating:** 75/100  
**Estimated Total Effort:** 4-6 hours  
**Created:** 2026-02-06

---

## 1. First Principles Analysis

### Why is Accurate Directory Documentation Important?

**Cognitive Load Reduction**
- New members rely on README.md
- Inaccurate docs force manual exploration
- Inconsistencies create friction

**Onboarding Efficiency**
- Accurate maps reduce onboarding time 50-70%
- Faster location of relevant code
- Reduced decision paralysis

### What Problems Does Inconsistent Documentation Cause?

| Problem | Impact | Frequency |
|---------|--------|-----------|
| Wasted exploration | 5-15 min/day | High |
| Files in wrong locations | Tech debt | Medium |
| Duplicate folders | Fragmentation | Medium |
| Loss of trust | Ignore docs | High |

### Identified Issues

1. **Missing Top-Level Directories** (7 not documented)
2. **Incorrect References** (`project/` doesn't exist)
3. **Missing Subdirectory Depth** (20 subdirs not documented)

---

## 2. Current State Assessment

### Documented Structure (README.md)

```
blackbox5/
├── project/      # DOES NOT EXIST
├── plans/
├── decisions/
├── knowledge/
├── tasks/
├── runs/
└── operations/
```

### Actual Structure

```
blackbox5/
├── .archived/         # NOT DOCUMENTED
├── .autonomous/       # NOT DOCUMENTED (20 subdirs)
├── .docs/             # NOT DOCUMENTED
├── .logs/             # NOT DOCUMENTED
├── .templates/        # PARTIALLY
├── action-plans/      # NOT DOCUMENTED
├── bin/               # NOT DOCUMENTED
├── [documented folders...]
```

### Inconsistencies

| Severity | Issue |
|----------|-------|
| HIGH | `project/` documented but doesn't exist |
| HIGH | `.autonomous/` completely missing |
| HIGH | `.docs/` completely missing |
| HIGH | `bin/` completely missing |
| MEDIUM | `tasks/cancelled/` missing |
| MEDIUM | `tasks/improvements/` missing |

---

## 3. Proposed Solution

### Hybrid Approach (Recommended)

- Automated generation for structure
- Manual curation for descriptions
- Validation to catch drift
- Regular synchronization

### Directory Documentation Format

```markdown
## Directory Structure

### Core Folders
[Primary organization]

### System Folders
[.autonomous/, .docs/, etc.]

### Supporting Folders
[bin/, action-plans/, etc.]
```

---

## 4. Implementation Plan

### Phase 1: Map Structure (45 min)

1. Run directory scan
2. Document all folders (depth 3)
3. Create `.directory-metadata.yaml` files
4. Define exclusions

### Phase 2: Update README (60 min)

1. Rewrite "Directory Structure" section
2. Organize into logical groups
3. Add missing folders
4. Remove non-existent references

### Phase 3: Create Generation Script (90 min)

1. Create `bb5-generate-directory-docs.py`
2. Implement tree scanner
3. Support metadata files
4. Add CLI arguments

### Phase 4: Add Validation (60 min)

1. Create `bb5-validate-directory-docs.py`
2. Implement comparison logic
3. Create pre-commit hook
4. Test validation

### Phase 5: Document Maintenance (45 min)

1. Add maintenance section to README
2. Create quick reference
3. Update onboarding

---

## 5. Success Criteria

- [ ] Directory structure mapped (complete inventory)
- [ ] README.md updated (all folders, consistent format)
- [ ] Generation script created (functional, tested)
- [ ] Validation working (detects drift)
- [ ] Maintenance documented

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Map | 45 min | 45 min |
| Phase 2: README | 60 min | 1h 45m |
| Phase 3: Script | 90 min | 3h 15m |
| Phase 4: Validation | 60 min | 4h 15m |
| Phase 5: Docs | 45 min | 5h 00m |
| **Buffer** | 60 min | **6h 00m** |

---

*Plan created based on directory structure analysis*
