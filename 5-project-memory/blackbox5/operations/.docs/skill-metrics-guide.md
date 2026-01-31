# Skill Metrics Guide

**Purpose:** Guide for understanding and using the skill effectiveness metrics system.

**Related Files:**
- `operations/skill-metrics.yaml` - Effectiveness tracking data
- `operations/skill-usage.yaml` - Usage tracking data
- `operations/.docs/skill-tracking-guide.md` - Usage tracking guide

---

## Overview

The skill metrics system measures how effectively each skill helps complete tasks. It answers questions like:

- Which skills deliver the best results?
- When should I use skill X vs skill Y?
- Are we selecting the right skills for the right tasks?
- What's the ROI of using skills vs not using them?

---

## Effectiveness Score Calculation

The effectiveness score (0-100) is a weighted composite of five metrics:

| Component | Weight | Description |
|-----------|--------|-------------|
| Success Rate | 35% | % of tasks completed successfully |
| Time Efficiency | 25% | Speed vs baseline (no skill) |
| Trigger Accuracy | 20% | How often skill was the right choice |
| Quality Score | 15% | Average quality rating (1-5 scale) |
| Reuse Rate | 5% | % of tasks where skill was used again |

### Formula

```
Effectiveness Score = (
  (success_rate * 0.35) +
  (time_efficiency * 0.25) +
  (trigger_accuracy * 0.20) +
  (quality_score * 0.15) +
  (reuse_rate * 0.05)
)
```

---

## How to Record Task Outcomes

After completing a task, add an entry to `skill-metrics.yaml` in the `task_outcomes` section:

```yaml
task_outcomes:
  - task_id: "TASK-123"
    timestamp: "2026-02-01T12:00:00Z"
    skill_used: "bmad-architect"
    task_type: "implement"
    duration_minutes: 45
    outcome: "success"
    quality_rating: 4
    trigger_was_correct: true
    would_use_again: true
    notes: "Great for architecture decisions, saved time on design"
```

### Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `task_id` | Yes | The task identifier |
| `timestamp` | Yes | When task was completed (ISO 8601) |
| `skill_used` | Yes | Name of skill from skill-usage.yaml |
| `task_type` | Yes | implement, analyze, fix, refactor, organize |
| `duration_minutes` | Yes | Time taken to complete task |
| `outcome` | Yes | success, failure, or partial |
| `quality_rating` | Yes | 1-5 rating (see scale below) |
| `trigger_was_correct` | Yes | Was this skill the right choice? |
| `would_use_again` | Yes | Would you use this skill for similar tasks? |
| `notes` | No | Observations about effectiveness |

---

## Quality Rating Scale

| Rating | Description |
|--------|-------------|
| 5 | Excellent - Exceeded expectations, reusable solution, no issues |
| 4 | Good - Met all requirements, minor improvements possible |
| 3 | Acceptable - Met core requirements, some issues noted |
| 2 | Below Average - Partial completion, significant issues |
| 1 | Poor - Failed to meet requirements, major issues |

---

## ROI Calculation

### Time Saved

```
time_saved = baseline_minutes - actual_duration_minutes
```

The `baseline_minutes` for each skill represents the estimated time to complete similar tasks without using the skill.

### Cost-Benefit Ratio

```
cost_benefit_ratio = time_saved_minutes / skill_invocation_overhead
```

Where `skill_invocation_overhead` is the time spent setting up and using the skill (typically 2-5 minutes).

---

## How to Use Skill Selection Recommendations

The `analysis.skill_selection_recommendations` section provides guidance on which skill to use for different scenarios.

### Example Decision Flow

```
1. Identify task characteristics:
   - Estimated duration
   - Complexity level
   - Type (implement, analyze, fix, etc.)

2. Check recommendations for matching scenario

3. Review the recommended skill's:
   - effectiveness_score
   - success_rate for similar task_type
   - trigger_accuracy

4. If confidence is "low", use judgment based on task specifics

5. After completion, record outcome to improve future recommendations
```

---

## Weekly Review Process

1. **Calculate Metrics** (every Monday)
   ```bash
   # Review task_outcomes from past week
   # Update skill metrics in skill-metrics.yaml
   # Recalculate effectiveness scores
   ```

2. **Identify Patterns**
   - Which skills are trending up/down?
   - Any common false positives?
   - Skills with low trigger accuracy?

3. **Update Recommendations**
   - Adjust `when_to_use` based on data
   - Add new scenarios if needed
   - Update confidence levels

4. **Document Insights**
   - Add findings to `analysis.trigger_insights`
   - Note any skill improvements needed

---

## Interpreting Low Scores

### Low Success Rate
- Skill may be used for wrong task types
- Skill implementation may need improvement
- Baseline expectations may be misaligned

### Low Trigger Accuracy
- Trigger keywords may be too broad
- Documentation needs clarification
- Training/communication issue

### Low Time Efficiency
- Skill overhead too high for task size
- Skill process needs optimization
- Wrong skill for quick tasks

### Low Quality Score
- Skill output needs review process
- Skill may need capability improvements
- Expectations may be unrealistic

---

## Best Practices

1. **Record Every Task** - Even failures provide valuable data
2. **Be Honest** - Accurate ratings improve recommendations
3. **Update Weekly** - Regular analysis catches trends early
4. **Compare Categories** - Agent skills vs utility skills have different baselines
5. **Review Baselines** - Adjust `baseline_minutes` as you learn

---

## Example Workflow

### Before Task

```yaml
# Check skill-metrics.yaml for recommendations
# Scenario: "Implement new feature, estimated 60 minutes"

analysis.skill_selection_recommendations:
  - scenario: "Implementation work"
    recommended_skill: "bmad-dev"
    confidence: "medium"

# Decision: Use bmad-dev skill
```

### After Task

```yaml
# Record outcome in task_outcomes:
- task_id: "TASK-456"
  timestamp: "2026-02-01T15:30:00Z"
  skill_used: "bmad-dev"
  task_type: "implement"
  duration_minutes: 50
  outcome: "success"
  quality_rating: 4
  trigger_was_correct: true
  would_use_again: true
  notes: "Saved 10 minutes vs baseline, good code quality"

# Update skill metrics:
skills:
  - name: bmad-dev
    effectiveness_score: 85  # Recalculated
    metrics:
      success_rate: 95
      time_efficiency: 20
      trigger_accuracy: 90
      quality_score: 80
      reuse_rate: 100
```

---

## Troubleshooting

### No Data Showing
- Check that `task_outcomes` entries are properly formatted
- Verify skill names match between files
- Ensure timestamps are valid ISO 8601 format

### Scores Seem Wrong
- Verify weights sum to 1.0 in `metrics_schema`
- Check for null values in component metrics
- Review `baseline_minutes` are realistic

### Recommendations Not Helpful
- Add more specific scenarios
- Update based on actual task outcomes
- Consider task sub-types (e.g., "quick fix" vs "complex feature")

---

## Integration with Other Systems

### STATE.yaml
- Use effectiveness scores to prioritize skill improvements
- Reference skill metrics in improvement goals

### goals.yaml
- Track IG-004 (Optimize Skill Usage) progress
- Set targets for effectiveness scores

### Run Documentation
- Reference skill effectiveness in DECISIONS.md
- Note skill selection rationale in THOUGHTS.md

---

## Future Enhancements

Planned improvements to the metrics system:

1. **Automated Tracking** - Integrate with run completion to auto-populate task_outcomes
2. **Predictive Recommendations** - ML-based skill selection suggestions
3. **Skill Combinations** - Track effectiveness of multi-skill workflows
4. **A/B Testing** - Compare different skills for same task type
5. **Benchmarking** - Compare against industry standards

---

## Questions?

For questions about skill metrics:
1. Check `operations/skill-metrics.yaml` for current data
2. Review recent `task_outcomes` entries
3. Consult `operations/.docs/skill-tracking-guide.md` for usage tracking
