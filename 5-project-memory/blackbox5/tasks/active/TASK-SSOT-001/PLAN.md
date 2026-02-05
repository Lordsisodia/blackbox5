# PLAN.md: Consolidate Skill Metrics into Single Source of Truth

**Task:** TASK-SSOT-001 - Skill metrics scattered across multiple files
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 4-6 hours
**Importance:** 75 (High)

---

## 1. First Principles Analysis

### The Core Problem
Skill metrics data is currently fragmented across multiple files:
- `5-project-memory/blackbox5/operations/skill-metrics.yaml` - Primary metrics
- `5-project-memory/blackbox5/operations/skill-usage.yaml` - Usage tracking
- `5-project-memory/blackbox5/operations/skill-selection.yaml` - Selection criteria
- `5-project-memory/blackbox5/operations/improvement-metrics.yaml` - Improvement data

This fragmentation creates:
1. **Update Inconsistency**: Changes must be made in multiple places
2. **Query Complexity**: Aggregating metrics requires reading multiple files
3. **Maintenance Overhead**: Four files to maintain for one concern
4. **Data Drift**: Files can become out of sync

### First Principles Solution
- **Single Source of Truth**: One canonical location for all skill metrics
- **Clear Schema**: Well-defined structure for all skill data
- **Query Interface**: Simple API for accessing metrics
- **Backward Compatibility**: Existing references continue to work

---

## 2. Current State Analysis

### Files Involved

| File | Purpose | Size | Last Updated |
|------|---------|------|--------------|
| skill-metrics.yaml | Effectiveness tracking | ~200 lines | 2026-02-05 |
| skill-usage.yaml | Usage patterns | ~150 lines | 2026-02-05 |
| skill-selection.yaml | Selection criteria | ~180 lines | 2026-02-05 |
| improvement-metrics.yaml | Improvement data | ~120 lines | 2026-02-05 |

### Data Overlap

All four files contain:
- Skill identifiers and names
- Timestamps and version info
- Task outcome references
- Effectiveness scores

### Query Patterns

1. **Get skill effectiveness** → Check skill-metrics.yaml
2. **Get skill usage** → Check skill-usage.yaml
3. **Select best skill** → Check skill-selection.yaml
4. **Track improvement** → Check improvement-metrics.yaml

---

## 3. Proposed Solution: Unified Skill Registry

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Unified Skill Registry                      │
│              (Single Source of Truth)                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Skills    │  │   Metrics   │  │   Usage History     │  │
│  │   (Index)   │  │  (Current)  │  │   (Time Series)     │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                    │             │
│         └────────────────┼────────────────────┘             │
│                          │                                  │
│                   ┌──────┴──────┐                          │
│                   │   Query     │                          │
│                   │   Engine    │                          │
│                   └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### New File Structure

**Primary:** `5-project-memory/blackbox5/operations/skill-registry.yaml`

```yaml
version: "2.0"
last_updated: "2026-02-06T00:00:00Z"

# Skill Index - All skills with metadata
skills:
  git-commit:
    name: "Git Commit"
    description: "Standardized git commit workflow"
    category: "git"
    version: "1.0"
    created: "2026-01-15"

# Current Metrics - Latest effectiveness data
metrics:
  git-commit:
    effectiveness_score: 0.92
    success_rate: 0.95
    usage_count: 47
    last_used: "2026-02-05"

# Usage History - Time series data
usage_history:
  git-commit:
    - date: "2026-02-05"
      task_id: "TASK-001"
      outcome: "success"
      duration_minutes: 5

# Selection Criteria - When to use each skill
selection_criteria:
  git-commit:
    triggers: ["commit", "git workflow"]
    confidence_threshold: 0.70
    priority: 1
```

---

## 4. Implementation Plan

### Phase 1: Create Unified Schema (1 hour)

**File:** `5-project-memory/blackbox5/operations/skill-registry.yaml`

1. Design comprehensive schema covering all four files
2. Define migration path from old files
3. Create validation schema

### Phase 2: Data Migration (2 hours)

1. Extract data from all four source files
2. Merge and deduplicate entries
3. Validate data integrity
4. Write to new unified file

### Phase 3: Update References (2 hours)

**Files to Update:**
- `bin/bb5-*` scripts that read skill data
- `2-engine/.autonomous/bin/*.py` agents
- Any documentation referencing old files

**Changes:**
- Replace multiple file reads with single registry read
- Update query logic
- Add fallback for backward compatibility

### Phase 4: Deprecation (1 hour)

1. Add deprecation headers to old files
2. Create symlinks or wrappers if needed
3. Document migration in CHANGELOG

---

## 5. Files to Modify/Create

### New Files
1. `5-project-memory/blackbox5/operations/skill-registry.yaml` - Unified registry
2. `5-project-memory/blackbox5/operations/skill-registry-schema.yaml` - Validation schema

### Modified Files
1. `5-project-memory/blackbox5/operations/skill-metrics.yaml` - Add deprecation notice
2. `5-project-memory/blackbox5/operations/skill-usage.yaml` - Add deprecation notice
3. `5-project-memory/blackbox5/operations/skill-selection.yaml` - Add deprecation notice
4. `5-project-memory/blackbox5/operations/improvement-metrics.yaml` - Add deprecation notice

### Scripts to Update
1. `bin/bb5-metrics-collector.py` - Use unified registry
2. `bin/bb5-*` - Update skill queries

---

## 6. Success Criteria

- [ ] Single skill-registry.yaml contains all skill data
- [ ] All four old files marked as deprecated
- [ ] All scripts updated to use unified registry
- [ ] Data migration verified (no data loss)
- [ ] Query performance improved (single file read)
- [ ] Backward compatibility maintained
- [ ] Documentation updated

---

## 7. Rollback Strategy

If issues arise:

1. **Immediate**: Restore old file reads in scripts
2. **Short-term**: Revert to using individual files
3. **Full**: Delete unified registry, restore original structure

---

## 8. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Schema Design | 1 hour | 1 hour |
| Phase 2: Data Migration | 2 hours | 3 hours |
| Phase 3: Update References | 2 hours | 5 hours |
| Phase 4: Deprecation | 1 hour | 6 hours |
| **Total** | | **4-6 hours** |

---

*Plan created based on SSOT violation analysis - Skill metrics scattered across multiple files*
