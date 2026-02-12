# Skill Comparison Framework

## Overview

The Skill Comparison Framework provides a systematic way to measure the effectiveness of skills by comparing task completion times between skill-enhanced tasks and baseline tasks (completed without skills).

## Purpose

Since true A/B testing is impossible (the same task cannot be completed both ways), this framework uses:

1. **Historical baselines** - Track tasks completed without skills
2. **Estimated baselines** - Executor estimates time without a skill
3. **Task type grouping** - Compare similar tasks (e.g., "git-commit", "documentation")

## Components

### 1. Comparison Pairs (Data Structure)

Stored in `operations/skill-registry.yaml` under `comparison_pairs`:

```yaml
comparison_pairs:
  - task_type: "git-commit"
    baseline_tasks:
      - task_id: "TASK-001"
        duration_minutes: 30
        date: "2026-02-01T00:00:00Z"
    skill_tasks:
      - task_id: "TASK-002"
        skill_used: "git-automation"
        duration_minutes: 15
        date: "2026-02-02T00:00:00Z"
    time_saved_minutes: 15
    time_saved_percent: 50
    sample_size: 1
    confidence: low
```

**Fields:**
- `task_type`: Category of task for grouping
- `baseline_tasks`: Tasks completed without skills
  - `task_id`: Task identifier
  - `duration_minutes`: Time to complete (in minutes)
  - `date`: When task was completed
- `skill_tasks`: Tasks completed with skills
  - `task_id`: Task identifier
  - `skill_used`: Skill that was used
  - `duration_minutes`: Time to complete (in minutes)
  - `date`: When task was completed
- `time_saved_minutes`: Difference between baseline and skill time
- `time_saved_percent`: Percentage of time saved
- `sample_size`: Number of comparisons in this pair
- `confidence`: Data quality indicator (low/medium/high)

### 2. Report Generator

Script: `/opt/blackbox5/bin/skill-comparison-report.py`

**Usage:**
```bash
# Generate summary report for all skills
python3 /opt/blackbox5/bin/skill-comparison-report.py

# Generate report for specific skill
python3 /opt/blackbox5/bin/skill-comparison-report.py --skill git-automation

# Save report to file
python3 /opt/blackbox5/bin/skill-comparison-report.py --output /tmp/report.md

# Calculate time savings
python3 /opt/blackbox5/bin/skill-comparison-report.py --calculate 30 15
```

**Output:**
- Overall summary statistics
- Per-skill breakdown
- Detailed comparison by task type

### 3. Task Tagging System

Tasks should be tagged during completion:

**Baseline Tags (no skill):**
- Task marked as `baseline` in metadata
- Duration recorded
- Task type/category noted

**Skill-Enhanced Tags:**
- Task marked as `skill-enhanced` in metadata
- Skill used recorded
- Duration recorded
- Baseline estimate provided

## Workflow

### Adding Comparison Data

1. **Identify comparable tasks**
   - Find tasks of the same type (e.g., git-commit, documentation)
   - Ensure one was completed with a skill, one without

2. **Create comparison pair**
   - Add entry to `comparison_pairs` in skill-registry.yaml
   - Include all required fields

3. **Calculate time savings**
   ```python
   time_saved = baseline_duration - skill_duration
   percent_saved = (time_saved / baseline_duration) * 100
   ```

4. **Set confidence level**
   - `low`: Single comparison, estimated baseline
   - `medium`: 2-3 comparisons, mixed estimation/actual
   - `high`: 3+ comparisons, all actual baselines

### Generating Reports

1. **Summary Report**
   - Shows overall statistics across all skills
   - Per-skill breakdown
   - Detailed comparisons by task type

2. **Skill-Specific Report**
   - Focuses on a single skill
   - Shows all comparisons for that skill
   - Calculates averages across comparisons

### Using Reports for ROI Calculation

The report generator provides the data needed for ROI calculations:

- **Total Time Saved:** Sum of time saved across all comparisons
- **Average Time Saved:** Mean time saved per comparison
- **Percent Saved:** Efficiency improvement percentage

This data can be used to update skill effectiveness scores in the registry.

## Best Practices

### Data Quality

1. **Baseline Accuracy**
   - Prefer actual baseline times over estimates
   - If using estimates, note this in confidence level
   - Update estimates when actual data becomes available

2. **Sample Size**
   - Single comparison: `low` confidence
   - 2-3 comparisons: `medium` confidence
   - 3+ comparisons: `high` confidence

3. **Task Type Consistency**
   - Ensure tasks are truly comparable
   - Similar complexity, scope, and context
   - Document any differences in notes

### Confidence Levels

| Level | Description | Sample Size | Baseline Type |
|-------|-------------|-------------|---------------|
| Low | Preliminary data | 1 | Estimated |
| Medium | Some data available | 2-3 | Mixed |
| High | Reliable data | 3+ | Actual |

### Common Task Types

**Recommended categories for comparison:**
- `git-commit` - Version control operations
- `documentation` - Documentation writing
- `testing` - Test creation/execution
- `refactoring` - Code refactoring
- `research` - Information gathering
- `configuration` - System configuration
- `deployment` - Application deployment

## Integration Points

### 1. Task Completion Workflow

When a task is completed:
1. Mark task as `baseline` or `skill-enhanced`
2. Record actual duration
3. If skill-enhanced, record which skill
4. Provide baseline estimate if needed

### 2. Skill Registry

The `comparison_pairs` section in skill-registry.yaml stores all comparison data. This is the single source of truth for skill effectiveness.

### 3. ROI Calculation

Use comparison data to calculate ROI:
- Time saved per task
- Efficiency improvement percentage
- Cost benefit ratio (development cost vs time savings)

## Example Scenarios

### Scenario 1: Historical Baseline

**Task:** Git commit process

**Baseline:**
- TASK-001 (completed 2026-01-15): 30 minutes (no automation)
- TASK-003 (completed 2026-01-20): 28 minutes (no automation)

**Skill-Enhanced:**
- TASK-002 (completed 2026-01-18): 12 minutes (git-automation skill)
- TASK-004 (completed 2026-01-22): 14 minutes (git-automation skill)

**Calculation:**
- Average baseline: 29 minutes
- Average skill: 13 minutes
- Time saved: 16 minutes (55%)

**Confidence:** High (actual baselines, 2+ comparisons)

### Scenario 2: Estimated Baseline

**Task:** API documentation

**Baseline:**
- Estimated: 60 minutes (based on experience)

**Skill-Enhanced:**
- TASK-010 (completed 2026-02-01): 35 minutes (doc-generator skill)

**Calculation:**
- Time saved: 25 minutes (42%)

**Confidence:** Low (estimated baseline, single comparison)

## Maintenance

### Updating Comparison Data

1. Add new comparison pairs as data becomes available
2. Update confidence levels as sample sizes grow
3. Remove outdated or invalid comparisons
4. Document any changes in notes

### Review Frequency

- **Weekly:** Check for new comparison pairs
- **Monthly:** Review confidence levels and sample sizes
- **Quarterly:** Full audit of comparison data quality

## Limitations

1. **Estimation Bias**
   - Baseline estimates may be subjective
   - Executors may overestimate or underestimate

2. **Task Variability**
   - Not all tasks of same type are identical
   - Complexity, context, and scope can vary

3. **Sample Size**
   - Limited data for new skills
   - May take time to accumulate reliable data

4. **Skill Overlap**
   - Some tasks use multiple skills
   - Difficult to isolate individual skill contribution

## Future Improvements

1. **Automated Baseline Detection**
   - Detect baseline tasks automatically
   - Use historical data to estimate baselines

2. **Task Type Inference**
   - Auto-classify tasks by type
   - Use NLP to identify task categories

3. **Statistical Significance**
   - Calculate confidence intervals
   - Apply statistical tests

4. **Trend Analysis**
   - Track skill improvement over time
   - Identify learning curves

## References

- Task: TASK-FIX-SKIL-032-2
- Related: SKIL-032 (ROI calculation enhancement)
- Registry: `operations/skill-registry.yaml`
- Script: `bin/skill-comparison-report.py`
