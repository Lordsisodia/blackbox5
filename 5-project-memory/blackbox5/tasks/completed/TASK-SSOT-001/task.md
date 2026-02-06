# TASK-SSOT-001: Consolidate Skill Metrics Files

**Status:** completed
**Priority:** CRITICAL
**Created:** 2026-02-06
**Completed:** 2026-02-06
**Parent:** Issue #12 - SSOT Configuration Violations

## Objective
Merge skill-metrics.yaml, skill-usage.yaml, skill-selection.yaml, and improvement-metrics.yaml into a single canonical skill-registry.yaml file.

## Success Criteria
- [x] Create unified skill-registry.yaml with all skill data
- [x] Merge effectiveness scores from skill-metrics.yaml
- [x] Merge usage tracking from skill-usage.yaml
- [x] Merge selection criteria from skill-selection.yaml
- [x] Merge improvement data from improvement-metrics.yaml
- [x] Add deprecation headers to old files
- [x] Update all scripts to use new registry
- [x] Document the new schema

## Summary
Successfully consolidated 4 skill metrics files into a single unified registry:

### Files Created
1. **operations/skill-registry.yaml** - Unified registry with all skill data
2. **operations/skill-registry-schema.yaml** - Validation schema
3. **bin/skill_registry.py** - Python module for registry access

### Files Modified (Deprecated)
1. **operations/skill-metrics.yaml** - Added deprecation header
2. **operations/skill-usage.yaml** - Added deprecation header
3. **operations/skill-selection.yaml** - Added deprecation header
4. **operations/improvement-metrics.yaml** - Added deprecation header

### Scripts Updated
1. **bin/calculate-skill-metrics.py** - Now uses unified registry
2. **bin/log-skill-usage.py** - Now logs to unified registry
3. **bin/collect-skill-metrics.py** - Now uses unified registry

### Unified Registry Structure
```yaml
metadata:           # Registry metadata
metrics_schema:     # Metrics calculation schema
skills:            # All 23 skills with complete data
  - metadata
  - metrics
  - usage stats
  - ROI data
  - selection criteria
usage_history:     # Time series usage data
task_outcomes:     # Task outcome records
selection_framework:  # Auto-trigger rules & confidence calculation
analysis:          # Aggregated analysis
recovery_metrics:  # Recovery tracking data
improvement_pipeline:  # Improvement tracking
```

## Data Migrated
- 23 skills with complete metadata
- 1 usage history entry
- 4 task outcomes
- 10 auto-trigger rules
- 10 completed improvements
- All selection criteria and confidence thresholds

## Backward Compatibility
- Old files kept with deprecation headers for reference
- Scripts maintain backward compatibility via --use-legacy flag
- skill_registry.py provides compatible load/save functions

## Related Files
- operations/skill-registry.yaml (NEW - Single Source of Truth)
- operations/skill-registry-schema.yaml (NEW)
- bin/skill_registry.py (NEW)
- operations/skill-metrics.yaml (DEPRECATED)
- operations/skill-usage.yaml (DEPRECATED)
- operations/skill-selection.yaml (DEPRECATED)
- operations/improvement-metrics.yaml (DEPRECATED)

## Rollback Strategy
If issues arise, the original files remain in place with deprecation headers. Simply remove the deprecation notices to restore previous functionality.
