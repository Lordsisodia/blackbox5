# Metrics Dashboard Guide

**Version:** 1.0.0
**Last Updated:** 2026-02-01
**Author:** RALF Executor (TASK-1769916005)

---

## Purpose

The metrics dashboard (`operations/metrics-dashboard.yaml`) provides centralized, real-time visibility into RALF system health and progress. It tracks 5 core metric categories:

1. **System Health** - Overall health score (0-10)
2. **Task Velocity** - Completion speed and efficiency
3. **Queue Metrics** - Task pipeline status
4. **Skill Usage** - Skill system effectiveness
5. **Feature Delivery** - Feature development progress

---

## How to Read the Dashboard

### System Health

```yaml
system_health:
  score: 9.0/10              # Overall health (0-10 scale)
  trend: "stable"            # improving, stable, declining

  components:
    task_completion_rate: 100%        # Success rate (last 10 runs)
    queue_depth: 2                    # Current tasks in queue
    skill_consideration_rate_last_10: 100%  # Skills evaluated
    skill_invocation_rate_last_10: 0%       # Skills actually used
```

**Target ranges:**
- Score: 8.0-10.0 (excellent), 6.0-7.9 (good), <6.0 (needs attention)
- Queue depth: 3-5 tasks (optimal buffer)
- Skill consideration: 100% (every task checks skills)
- Skill invocation: 10-30% (appropriate complexity threshold)

### Task Velocity

```yaml
task_velocity:
  tasks_per_hour: 1.3         # Tasks completed per hour
  avg_task_duration_seconds: 2770   # Average time per task
  avg_task_duration_minutes: 46     # In minutes

  trend: "stable"              # improving, stable, declining
```

**Target ranges:**
- Tasks per hour: >1.0 (good), 0.5-1.0 (adequate), <0.5 (slow)
- Avg duration: <60 min (fast), 60-120 min (normal), >120 min (slow)

### Queue Metrics

```yaml
queue_metrics:
  current_depth: 2            # Current tasks in queue
  target_range: [3, 5]        # Optimal range
  status: "slightly_low"      # optimal, low, slightly_low, high

  buffer_minutes: 90          # How long until queue empty
```

**Status meanings:**
- **optimal:** Queue depth within target range (3-5 tasks)
- **slightly_low:** Queue depth 1-2 tasks (add 1-3 tasks)
- **low:** Queue depth 0 tasks (add 3-5 tasks immediately)
- **high:** Queue depth >5 tasks (healthy, no action needed)

### Skill Usage

```yaml
skill_usage:
  consideration_rate_last_10: 100%   # Skills checked
  invocation_rate_last_10: 0%        # Skills used

  baseline_status: "in_progress"     # establishing, established
  baseline_runs_completed: 5         # Need 10 for baseline
```

**Baseline establishment:**
- Need 10 runs to establish reliable invocation rate
- During baseline: monitor but don't adjust threshold
- After baseline: assess if invocation rate is 10-30%

### Feature Delivery

```yaml
feature_delivery:
  features_completed: 0        # Features delivered
  features_in_progress: 0      # Currently implementing
  feature_backlog_depth: 4     # Planned features

  framework_status: "operational"
  strategic_shift:
    from: "improvements"
    to: "features"
    status: "in_progress"
```

**Strategic shift progress:**
- 100% improvement completion → Feature framework ready → Features being delivered
- Current: 100% improvements complete, framework operational, 0 features delivered

---

## How to Update the Dashboard

### Automatic Updates (Recommended)

The dashboard updates automatically on every task completion via `metrics_updater.py`. Integration point:

```python
# In roadmap_sync.py: sync_all_on_task_completion()
from metrics_updater import update_metrics_on_task_completion

metrics_result = update_metrics_on_task_completion(
    project_dir=project_dir,
    task_id=task_id,
    duration_seconds=duration_seconds,
    result="success",
    run_number=50
)
```

**Auto-update triggers:**
- Task completion (via roadmap_sync.sync_all_on_task_completion())
- Executor writes completion event
- Metrics recalculated from last 10 runs

### Manual Updates

If needed, you can manually update values directly in `metrics-dashboard.yaml`:

1. Open the file
2. Update the values you need
3. Add a note explaining the manual change
4. Save the file

**When to update manually:**
- Correcting anomalous data (e.g., negative durations)
- Adjusting targets after strategic review
- Adding context notes
- Testing threshold changes

---

## How to Use the Dashboard

### For Planning Decisions

**Queue Management:**
```bash
# Check queue depth
cat operations/metrics-dashboard.yaml | grep -A 5 "queue_metrics:"

# If status is "low" or "slightly_low", add tasks
# If status is "high", no action needed
```

**Example:**
- Queue depth: 2 tasks, status: slightly_low
- Action: Add 1-3 tasks to reach 3-5 target

### For Review Preparation

**Loop Reviews:**
1. Check system health score (should be 8.0-10.0)
2. Review task velocity trends (improving/stable/declining)
3. Assess skill usage rates (consideration 100%, invocation 10-30%)
4. Evaluate feature delivery progress

**Strategic Reviews:**
1. Analyze last 10 runs for patterns
2. Compare velocity trends across loops
3. Assess skill system effectiveness
4. Review feature delivery pipeline

### For Performance Monitoring

**Daily Checks:**
```bash
# Quick health check
cat operations/metrics-dashboard.yaml | grep "score:"
# Output: score: 9.0/10

# Check if queue needs replenishment
cat operations/metrics-dashboard.yaml | grep "status:"
# Output: status: "slightly_low"
```

**Weekly Analysis:**
- Review task velocity trends
- Assess skill invocation patterns
- Evaluate feature delivery progress
- Identify anomalies (e.g., negative durations, long tasks)

---

## Metric Definitions

### System Health Score

**Formula:** Weighted average of component scores

| Component | Weight | Calculation |
|-----------|--------|-------------|
| Task completion rate | 30% | successful_runs / total_runs |
| Queue depth | 25% | optimal = 1.0, low = 0.5, high = 0.8 |
| Skill consideration | 20% | consideration_rate / 100% |
| Skill invocation | 15% | closeness to 10-30% target |
| Error rate | 10% | (100% - error_rate) / 100% |

**Score Interpretation:**
- 9.0-10.0: Excellent (all systems optimal)
- 8.0-8.9: Very good (minor issues)
- 6.0-7.9: Good (some areas need attention)
- 4.0-5.9: Fair (multiple issues)
- 0-3.9: Poor (critical issues)

### Task Velocity

**Calculations:**
- `tasks_per_hour` = 3600 / avg_duration_seconds
- `avg_task_duration_seconds` = mean of last 10 valid durations
- `last_10_runs_avg_seconds` = same as above

**Exclusions:**
- Negative durations (timestamp errors)
- Durations >24 hours (anomalies)

### Skill Usage Rates

**Consideration Rate:**
```
consideration_rate = (runs_with_skill_section / total_runs) * 100%
```

**Invocation Rate:**
```
invocation_rate = (runs_with_invoked_skill / total_runs) * 100%
```

**Target:**
- Consideration: 100% (every task should check for skills)
- Invocation: 10-30% (only complex tasks need skills)

### Queue Depth

**Status Logic:**
```
if depth < target_min:
    status = "low"
elif depth == target_min or depth == target_min + 1:
    status = "slightly_low"
elif depth >= target_min and depth <= target_max:
    status = "optimal"
else:
    status = "high"
```

**Target Range:** 3-5 tasks (90-150 minutes buffer)

---

## Troubleshooting

### Dashboard Not Updating

**Symptoms:**
- Old data displayed
- Last updated timestamp stale

**Solutions:**
1. Check if `metrics_updater.py` is being called
2. Verify integration in `roadmap_sync.py`
3. Check for errors in executor logs
4. Try manual update as fallback

### Anomalous Data

**Symptoms:**
- Negative durations
- Extremely long durations (>24 hours)
- Missing run data

**Solutions:**
1. Identify problematic run (check `runs/executor/run-NNNN/metadata.yaml`)
2. Manually correct the duration in metadata.yaml
3. Re-run metrics update: `python3 2-engine/.autonomous/lib/metrics_updater.py <project_dir> <task_id> <duration> success <run_num>`

### Skill Invocation Rate 0%

**Symptoms:**
- Consideration rate: 100%
- Invocation rate: 0%

**This is NORMAL if:**
- Tasks are straightforward (clear requirements)
- All confidence scores <70% threshold
- Task types are simple (implement, fix with clear approach)

**This is a PROBLEM if:**
- Complex tasks (architecture, design) are not invoking skills
- Confidence scores consistently high but no invocation
- Threshold (70%) may be too high

**Action:** Wait for 10-run baseline, then reassess threshold.

---

## Advanced Usage

### Custom Thresholds

To adjust skill invocation threshold (currently 70%):

1. Edit `operations/skill-selection.yaml`
2. Update `confidence_calculation.threshold` value
3. Document rationale in notes
4. Monitor next 10 runs for impact

### Historical Data Analysis

The dashboard tracks two historical windows:
- **Last 10 runs:** Short-term patterns, velocity trends
- **Last 24 hours:** Daily throughput, burst capacity

**Accessing raw data:**
```bash
# Last 10 runs
cat operations/metrics-dashboard.yaml | grep -A 50 "history_last_10_runs:"

# Last 24 hours
cat operations/metrics-dashboard.yaml | grep -A 20 "history_last_24_hours:"
```

### Integration with Other Tools

**Git Commits:**
```bash
# Commit dashboard updates
git add operations/metrics-dashboard.yaml
git commit -m "metrics: Update dashboard after TASK-XXX completion"
```

**Dashboards/Visualization:**
- Export to JSON: `yq eval -o=json operations/metrics-dashboard.yaml`
- Import to Grafana, Datadog, etc.
- Build custom visualizations

---

## Maintenance

### Daily

- Check dashboard accuracy (compare with recent runs)
- Verify queue depth status
- Note any anomalies

### Weekly

- Review trends (velocity, health, skill usage)
- Assess if queue needs replenishment
- Check skill invocation rate against target

### Monthly

- Full metrics audit (validate calculations)
- Review and adjust targets if needed
- Archive old historical data
- Update documentation

---

## FAQ

**Q: Why is skill invocation rate 0%? Is this bad?**

A: Not necessarily. 0% invocation is appropriate if recent tasks are straightforward. The key metric is consideration rate (should be 100%). Wait for 10-run baseline before assessing.

**Q: How often does the dashboard update?**

A: Automatically on every task completion (typically 30-90 minutes). Can also update manually if needed.

**Q: What if I see negative durations?**

A: This is a timestamp error (usually run metadata has incorrect end timestamp). Correct the duration in `runs/executor/run-NNNN/metadata.yaml` and re-run metrics update.

**Q: Can I add custom metrics?**

A: Yes. Add new sections to `metrics-dashboard.yaml` and update `metrics_updater.py` to calculate them. Document in this guide.

**Q: How do I reset the dashboard?**

A: Delete `metrics-dashboard.yaml` and it will be recreated on next task completion. Note: You'll lose historical data.

---

## Contact & Support

**Maintainer:** RALF Executor
**Documentation:** `operations/.docs/metrics-dashboard-guide.md`
**Code:** `2-engine/.autonomous/lib/metrics_updater.py`

**Issues:** Report via task creation or feedback system.

---

## Changelog

### v1.0.0 (2026-02-01)
- Initial dashboard created (TASK-1769916005)
- 5 metric categories: System Health, Task Velocity, Queue Metrics, Skill Usage, Feature Delivery
- Auto-update integration via metrics_updater.py
- Historical tracking (last 10 runs, last 24 hours)
- Documentation complete

---

**End of Metrics Dashboard Guide**
