# TASK-1769916005: Create System Metrics Dashboard

**Type:** implement
**Priority:** medium
**Status:** pending
**Created:** 2026-02-01T17:00:00Z
**Estimated Minutes:** 45

## Objective

Create a centralized, auto-updating metrics dashboard to track system health and feature delivery progress, enabling data-driven planning for the autonomous agent system.

## Context

The system is transitioning from the "fix problems" era (improvements) to the "create value" era (features). Currently, metrics are fragmented across STATE.yaml, improvement-backlog.yaml, and various run logs. There is no centralized, real-time visibility into:

- Task velocity (tasks/hour)
- Queue depth (tasks available)
- Skill usage (consideration + invocation rates)
- System health (overall score)

This makes planning reactive instead of proactive. A metrics dashboard will:

1. Provide real-time visibility into system health
2. Enable data-driven planning decisions
3. Support Loop 10 review and future reviews
4. Track feature delivery velocity (new strategic era)

## Success Criteria

- [ ] Metrics dashboard created at `operations/metrics-dashboard.yaml`
- [ ] Tracks 4 core metrics: task velocity, queue depth, skill usage, system health
- [ ] Auto-updates on task completion (via integration with queue sync)
- [ ] Usage guide documented at `operations/.docs/metrics-dashboard-guide.md`
- [ ] Dashboard is readable by both Planner and Executor
- [ ] Historical data tracked (last 10 runs, last 24 hours)

## Approach

### Phase 1: Dashboard Structure (15 minutes)

1. **Create metrics schema:**
   ```yaml
   metrics:
     system_health:
       score: 9.5/10
       last_updated: "2026-02-01T17:00:00Z"
       components:
         task_completion_rate: 100%
         queue_depth: 4
         skill_consideration_rate: 100%
         error_rate: 0%

     task_velocity:
       tasks_per_hour: 1.3
       avg_task_duration_seconds: 2770
       last_10_runs_avg: 2800
       trend: "stable"  # improving, stable, declining

     queue_metrics:
       current_depth: 4
       target_range: [3, 5]
       buffer_minutes: 165
       accuracy: 100%

     skill_usage:
       consideration_rate_last_10: 100%
       invocation_rate_last_10: 0%
       total_skills_available: 15
       skills_used_last_10_runs: []

     feature_delivery:
       features_completed: 0
       features_in_progress: 0
       feature_backlog_depth: 4
       feature_velocity: 0 features/week
   ```

2. **Create file at `operations/metrics-dashboard.yaml`**
   - Use schema above
   - Initialize with current values from STATE.yaml and events.yaml

### Phase 2: Auto-Update Integration (15 minutes)

1. **Create `2-engine/.autonomous/lib/metrics_updater.py`:**
   ```python
   def update_metrics_on_task_completion(task_id, duration, result):
       """Update metrics dashboard after task completion."""
       # Load current metrics
       # Calculate new velocity
       # Update queue depth (sync with queue.yaml)
       # Update skill usage (check THOUGHTS.md for skill usage)
       # Recalculate system health score
       # Save metrics-dashboard.yaml
   ```

2. **Integrate with queue sync automation:**
   - Add call to `update_metrics_on_task_completion()` in `queue_sync.py`
   - Ensures metrics update automatically with queue

### Phase 3: Documentation (15 minutes)

1. **Create usage guide at `operations/.docs/metrics-dashboard-guide.md`:**
   - Purpose: Track system health and progress
   - How to read: Metric definitions, targets, trends
   - How to update: Automatic (via queue sync) or manual
   - How to use: Planning decisions, review preparation

2. **Document metric definitions:**
   - System Health: Weighted score of completion rate, queue depth, skill usage, error rate
   - Task Velocity: Tasks completed per hour (avg of last 10)
   - Queue Depth: Current tasks in queue (target: 3-5)
   - Skill Usage: Consideration rate (target: 100%) + invocation rate (target: 10-30%)
   - Feature Delivery: Features completed, in progress, backlog depth

## Files to Modify

- `operations/metrics-dashboard.yaml` (create) - Metrics dashboard
- `operations/.docs/metrics-dashboard-guide.md` (create) - Usage documentation
- `2-engine/.autonomous/lib/metrics_updater.py` (create) - Auto-update logic
- `2-engine/.autonomous/lib/queue_sync.py` (modify) - Integrate metrics update

## Dependencies

- None (can be executed independently)

## Notes

- **Strategic Importance:** This task enables the feature delivery era by providing visibility into feature velocity
- **Integration Point:** Metrics update automatically via queue sync (TASK-1769916001, completed in Run 47)
- **Review Support:** Provides data for Loop 10 review and future reviews
- **Priority:** MEDIUM (enables data-driven planning, supports strategic shift)

## Acceptance Criteria Validation

After completion, verify:

1. **Dashboard exists and is readable:**
   ```bash
   cat operations/metrics-dashboard.yaml
   # Should show 5 metric categories with current values
   ```

2. **Auto-update integration works:**
   - Check `queue_sync.py` for `update_metrics_on_task_completion()` call
   - Verify metrics updater function exists and is callable

3. **Documentation is complete:**
   - Usage guide exists at `operations/.docs/metrics-dashboard-guide.md`
   - Metric definitions documented
   - Update process documented

4. **Historical tracking works:**
   - Dashboard includes historical data (last 10 runs, last 24 hours)
   - Trends are calculated and displayed

## Expected Impact

**Immediate:**
- Centralized metrics visibility
- Reduced manual metrics collection time
- Better planning decisions (data-driven)

**Short-Term:**
- Supports Loop 10 review with data
- Enables feature delivery tracking
- Identifies system health issues early

**Long-Term:**
- Sustainable metrics tracking
- Trend analysis (velocity, health, skill usage)
- Informs strategic decisions (e.g., when to scale, optimize)

## Risk Mitigation

- **Risk:** Metrics calculation complexity may lead to errors
- **Mitigation:** Start simple (4 core metrics), expand later
- **Risk:** Auto-update integration may fail
- **Mitigation:** Test with 1-2 task completions, manual fallback documented
- **Risk:** Metrics may be ignored (not used)
- **Mitigation:** Integrate into planner workflow (check metrics every loop)
