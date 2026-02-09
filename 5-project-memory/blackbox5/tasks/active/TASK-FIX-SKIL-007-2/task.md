# TASK-FIX-SKIL-007-2: Fix calculate-skill-metrics.py to target correct file

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-09T12:00:00Z
**Parent:** TASK-SKIL-007

## Objective
Fix the `calculate-skill-metrics.py` script to read from and write to `skill-registry.yaml` instead of the deprecated `skill-metrics.yaml`.

## Root Cause
The `calculate-skill-metrics.py` script currently targets `skill-metrics.yaml` (line 503: `metrics_file = operations_dir / 'skill-metrics.yaml'`), but this file has been deprecated and replaced by `skill-registry.yaml`. The unified skill registry now contains all skill data including metrics, usage, and selection criteria. The script needs to be updated to work with the new file structure.

## Success Criteria
- [ ] Update script to read from `skill-registry.yaml` instead of `skill-metrics.yaml`
- [ ] Update script to write metrics to correct location in `skill-registry.yaml` structure
- [ ] Update script to read task_outcomes from `skill-registry.yaml` (line 513)
- [ ] Update script to read skills list from `skill-registry.yaml` skills section
- [ ] Update script to save calculated metrics back to `skill-registry.yaml` under correct paths
- [ ] Script runs successfully and produces non-null metrics when data exists
- [ ] Update any hardcoded paths or references to the old file

## Files to Modify
- Modify: `~/.blackbox5/5-project-memory/blackbox5/bin/calculate-skill-metrics.py`
- Reference: `~/.blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml`

## Context

### Current script behavior (lines 502-514):
```python
# Load data files
metrics_file = operations_dir / 'skill-metrics.yaml'  # WRONG - deprecated
usage_file = operations_dir / 'skill-usage.yaml'

print(f"Loading metrics from: {metrics_file}")
metrics_data = load_yaml_file(metrics_file)

print(f"Loading usage data from: {usage_file}")
usage_data = load_yaml_file(usage_file)

# Get task outcomes
outcomes = metrics_data.get('task_outcomes', [])  # Reads from wrong file
```

### skill-registry.yaml structure:
```yaml
# Skills are under 'skills' key, not top-level list
skills:
  bmad-dev:
    name: "Developer"
    metrics:
      effectiveness_score: null  # <- These need to be calculated
      success_rate: null
      time_efficiency: null
      ...
    usage:
      usage_count: 0
      ...

task_outcomes:  # <- Outcomes are here, not in skill-metrics.yaml
  - task_id: TASK-1769909000
    skill_used: null  # <- This is often null (see TASK-FIX-SKIL-007-3)
    ...

analysis:
  last_calculated: "..."
  top_skills: []
  underperforming_skills: []
  category_performance: []
  roi_summary: {}
```

### Key differences from old format:
1. Skills are a dict (keyed by skill name) not a list
2. Metrics are nested under each skill
3. task_outcomes is at root level
4. Analysis section needs to be updated

## Approach
1. Change `metrics_file` path from `skill-metrics.yaml` to `skill-registry.yaml`
2. Update `get_outcomes_for_skill()` to work with new structure
3. Update `update_skill_metrics()` to write to nested skill structure
4. Update `update_skill_usage()` to write to correct location
5. Update `calculate_category_performance()` to iterate over dict values
6. Update `calculate_roi_summary()` to iterate over dict values
7. Update `get_top_skills()` and `get_underperforming_skills()` similarly
8. Test with dry-run mode first

## Key Code Changes Needed

### Line 503 - Change target file:
```python
# OLD
metrics_file = operations_dir / 'skill-metrics.yaml'
# NEW
registry_file = operations_dir / 'skill-registry.yaml'
```

### Line 513 - Read outcomes from correct location:
```python
# OLD
outcomes = metrics_data.get('task_outcomes', [])
# NEW (already correct if reading from registry)
outcomes = registry_data.get('task_outcomes', [])
```

### Line 298 - Skills are now a dict:
```python
# OLD
skills = metrics_data.get('skills', [])
# NEW
skills = list(registry_data.get('skills', {}).values())
```

## Rollback Strategy
- Keep backup of original calculate-skill-metrics.py
- Test with --dry-run flag before saving changes
- Verify YAML structure is valid before writing

## Estimated Effort
45-60 minutes

## Related Tasks
- TASK-FIX-SKIL-007-1: Sync skill-usage.yaml to skill-registry.yaml
- TASK-FIX-SKIL-007-3: Update task outcome logging
