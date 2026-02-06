# Skill Registry Migration Guide

**Task:** TASK-SSOT-001
**Date:** 2026-02-06
**Status:** Completed

---

## Overview

As part of the Single Source of Truth (SSOT) initiative, we have consolidated 4 separate skill metrics files into a unified `skill-registry.yaml`.

### Files Consolidated

| Old File | Purpose | Status |
|----------|---------|--------|
| `skill-metrics.yaml` | Effectiveness tracking | Deprecated |
| `skill-usage.yaml` | Usage patterns | Deprecated |
| `skill-selection.yaml` | Selection criteria | Deprecated |
| `improvement-metrics.yaml` | Improvement data | Deprecated |

### New Unified File

| File | Purpose | Status |
|------|---------|--------|
| `skill-registry.yaml` | Single Source of Truth | Active |
| `skill-registry-schema.yaml` | Validation schema | Active |

---

## Unified Registry Structure

```yaml
metadata:
  version: "2.0.0"
  created: "2026-02-06T00:00:00Z"
  last_updated: "2026-02-06T00:00:00Z"
  total_skills: 23

metrics_schema:
  version: "1.0.0"
  calculation_method: weighted_composite
  components:
    - name: success_rate
      weight: 0.35
    - name: time_efficiency
      weight: 0.25
    - name: trigger_accuracy
      weight: 0.20
    - name: quality_score
      weight: 0.15
    - name: reuse_rate
      weight: 0.05

skills:
  <skill-id>:
    # Metadata
    name: "Display Name"
    description: "Skill description"
    category: agent|protocol|utility|core|infrastructure
    agent: "Agent Name" or null
    version: "1.0"
    created: "2026-01-15"

    # Current Metrics
    metrics:
      effectiveness_score: 0-100 or null
      success_rate: 0-100 or null
      time_efficiency: number or null
      trigger_accuracy: 0-100 or null
      quality_score: 0-100 or null
      reuse_rate: 0-100 or null

    # Usage Statistics
    usage:
      usage_count: integer
      success_count: integer
      failure_count: integer
      first_used: ISO timestamp or null
      last_used: ISO timestamp or null
      avg_execution_time_ms: integer or null

    # ROI Data
    roi:
      baseline_minutes: integer
      time_saved_minutes: number or null
      quality_improvement: number or null
      cost_benefit_ratio: number or null

    # Selection Criteria
    selection:
      triggers: [list of keywords]
      confidence_threshold: 70
      priority: 1-5
      when_to_use: "description"
      when_to_avoid: "description"
      confidence: low|medium|high

usage_history:
  - timestamp: ISO timestamp
    task_id: "TASK-XXX"
    skill: "skill-id" or null
    confidence: 0-100 or null
    result: success|failure|partial|unknown
    notes: "description"

task_outcomes:
  - task_id: "TASK-XXX"
    timestamp: ISO timestamp
    skill_used: "skill-id" or null
    outcome: success|failure|partial
    quality_rating: 1-5
    trigger_was_correct: boolean
    would_use_again: boolean

selection_framework:
  version: "1.2.0"
  confidence_threshold: 70
  auto_trigger_rules:
    - rule_id: "ATR-XXX"
      name: "Rule Name"
      condition: "description"
      keywords: [list]
      action: "description"
      priority: critical|high|medium|low
  confidence_calculation:
    factors:
      - factor: name
        weight: percentage
    formula: "calculation formula"

analysis:
  last_calculated: ISO timestamp
  top_skills: [list]
  underperforming_skills: [list]
  category_performance: [list]
  roi_summary: {}
  skill_selection_recommendations: [list]
  trigger_insights: {}

recovery_metrics:
  analysis_date: ISO timestamp
  runs_analyzed: [list]
  summary: {}
  threshold_analysis: {}
  recommendations: [list]

improvement_pipeline:
  pipeline: {}
  conversion_metrics: {}
  completed_improvements: [list]
```

---

## Python API

### Using the SkillRegistry Class

```python
from skill_registry import SkillRegistry

# Initialize registry
registry = SkillRegistry()

# Get all skills
skills = registry.get_all_skills()

# Get specific skill
skill = registry.get_skill("bmad-dev")

# Get skills by category
agents = registry.get_skills_by_category("agent")

# Get metrics
metrics = registry.get_skill_metrics("bmad-dev")
effectiveness = registry.get_effectiveness_score("bmad-dev")

# Get selection criteria
criteria = registry.get_selection_criteria("bmad-dev")
rules = registry.get_auto_trigger_rules()

# Find matching skills
matches = registry.find_matching_skills("implement git workflow")

# Log usage
registry.log_usage(
    task_id="TASK-001",
    skill_id="bmad-dev",
    confidence=85,
    outcome="success",
    duration_minutes=30
)

# Add task outcome
registry.add_task_outcome({
    "task_id": "TASK-001",
    "skill_used": "bmad-dev",
    "outcome": "success",
    "quality_rating": 4
})
```

### CLI Usage

```bash
# List all skills
python3 bin/skill_registry.py list

# List skills by category
python3 bin/skill_registry.py list --category agent

# Get skill details
python3 bin/skill_registry.py get bmad-dev

# Show all metrics
python3 bin/skill_registry.py metrics

# Show metrics for specific skill
python3 bin/skill_registry.py metrics --skill bmad-dev

# Find matching skills
python3 bin/skill_registry.py match "implement git workflow"
```

---

## Backward Compatibility

### For Scripts Using Old Files

The old files remain in place with deprecation headers. Scripts can continue to use them, but they will not receive updates.

### Migration Path

1. **Import the new module:**
   ```python
   from skill_registry import SkillRegistry, load_skill_metrics
   ```

2. **Replace file reads:**
   ```python
   # Old way
   with open('operations/skill-metrics.yaml') as f:
       data = yaml.safe_load(f)

   # New way
   registry = SkillRegistry()
   skill = registry.get_skill("bmad-dev")
   ```

3. **Update write operations:**
   ```python
   # Old way
   with open('operations/skill-metrics.yaml', 'w') as f:
       yaml.dump(data, f)

   # New way
   registry.update_skill_metrics("bmad-dev", new_metrics)
   ```

---

## Data Verification

### Statistics

| Metric | Count |
|--------|-------|
| Total Skills | 23 |
| Categories | 5 (agent, protocol, utility, core, infrastructure) |
| Usage History Entries | 1 |
| Task Outcomes | 4 |
| Auto-Trigger Rules | 10 |
| Completed Improvements | 10 |

### Validation

The registry includes a JSON Schema for validation:

```bash
# Validate against schema (requires jsonschema package)
python3 -c "
import yaml
import jsonschema

with open('operations/skill-registry.yaml') as f:
    data = yaml.safe_load(f)

with open('operations/skill-registry-schema.yaml') as f:
    schema = yaml.safe_load(f)

jsonschema.validate(data, schema)
print('✅ Registry is valid')
"
```

---

## Benefits

1. **Single Source of Truth**: All skill data in one location
2. **Consistent Schema**: Unified structure across all skill data
3. **Better Query Performance**: Single file read instead of multiple
4. **Easier Maintenance**: One file to update instead of four
5. **Clear API**: Python module provides clean interface
6. **Backward Compatible**: Old files remain for reference

---

## Rollback

If issues arise:

1. Remove deprecation headers from old files
2. Update scripts to use old file paths
3. The unified registry can be deleted if needed

All original data was preserved during migration.
