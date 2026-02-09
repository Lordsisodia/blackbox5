# Decisions - TASK-1769916005

## Decision 1: Dashboard Structure - 5 Metric Categories

**Context:** Task acceptance criteria required "4 core metrics" but didn't specify which ones. Needed to determine most valuable metrics for data-driven planning.

**Options Considered:**
1. **Minimal approach:** Task velocity, queue depth only (2 metrics)
2. **Moderate approach:** Task velocity, queue depth, skill usage (3 metrics)
3. **Comprehensive approach:** Task velocity, queue depth, skill usage, system health, feature delivery (5 metrics)

**Selected:** Option 3 - Comprehensive approach (5 metrics)

**Rationale:**
- **System health** provides single-score overview for quick assessment
- **Task velocity** tracks efficiency and identifies bottlenecks
- **Queue metrics** prevent task starvation (critical for autonomous operation)
- **Skill usage** validates skill system investment (13 runs of work)
- **Feature delivery** supports strategic shift from improvements to features

**Reversibility:** HIGH (can remove unused categories later)

**Impact:** Positive - provides comprehensive visibility with minimal overhead

---

## Decision 2: Anomalous Data Filtering

**Context:** Run 48 metadata shows negative duration (-14531 seconds). Including this would skew velocity calculations and produce misleading metrics.

**Options Considered:**
1. **Include all data:** Use all durations regardless of validity
2. **Manual correction:** Edit Run 48 metadata to fix duration
3. **Automatic filtering:** Exclude invalid durations in calculation

**Selected:** Option 3 - Automatic filtering

**Rationale:**
- Non-blocking: don't fail task completion due to data issues
- Automatic: no manual intervention needed
- Preserves raw data: original metadata unchanged
- Handles future anomalies: filter applies to all runs
- Thresholds: exclude negative durations and extreme values (>24 hours)

**Implementation:**
```python
# In calculate_task_velocity()
if 0 < duration < 86400:  # 0 < duration < 24 hours
    valid_durations.append(duration)
```

**Reversibility:** HIGH (can adjust filter thresholds in one place)

**Impact:** Positive - accurate metrics despite data anomalies

---

## Decision 3: Integration Point - roadmap_sync.py

**Context:** Metrics updater needs to be called on task completion. Multiple integration points available.

**Options Considered:**
1. **Executor loop:** Call directly in executor's task completion flow
2. **queue_sync.py:** Call after queue synchronization
3. **roadmap_sync.py:** Call via `sync_all_on_task_completion()`

**Selected:** Option 3 - roadmap_sync.py integration

**Rationale:**
- **Single sync point:** Already syncs STATE.yaml, improvement-backlog.yaml, queue.yaml
- **Already called:** Executor already calls `sync_all_on_task_completion()`
- **Non-blocking:** roadmap_sync has error handling for partial failures
- **Consistent:** All state updates in one place
- **Tested:** Existing infrastructure for sync operations

**Alternative considered:** Option 2 (queue_sync.py) - rejected because queue_sync is single-purpose (queue only), metrics update is broader concern

**Reversibility:** MEDIUM (would need to update executor call site if moved)

**Impact:** Positive - seamless integration with existing sync infrastructure

---

## Decision 4: Historical Window Size - Last 10 Runs

**Context:** Dashboard needs historical data for trend analysis and baseline establishment. Need to determine optimal window size.

**Options Considered:**
1. **Small window:** Last 5 runs (quick trend detection, less stable)
2. **Medium window:** Last 10 runs (balanced, chosen)
3. **Large window:** Last 25 runs (very stable, slow to adapt)

**Selected:** Option 2 - Last 10 runs

**Rationale:**
- **Baseline requirement:** Skill system needs 10-run baseline for invocation rate assessment (from Run 49 analysis)
- **Trend detection:** 10 runs sufficient to identify patterns (improving, stable, declining)
- **Recency:** Recent runs more relevant than old data
- **Performance:** Small enough for fast calculation
- **Industry standard:** 10-data-point window common in metrics systems

**Implementation:**
```python
# Keep only last 10
if len(data_points) > 10:
    data_points = data_points[-10:]
```

**Reversibility:** HIGH (can adjust window size constant)

**Impact:** Positive - balances stability with recency

---

## Decision 5: 24-Hour Window for Daily Metrics

**Context:** Dashboard needs daily throughput metrics in addition to per-run metrics. Need to determine time window.

**Options Considered:**
1. **Fixed window:** Last 24 hours (chosen)
2. **Calendar day:** Current day only (resets at midnight)
3. **Rolling window:** Last N tasks regardless of time

**Selected:** Option 1 - Last 24 hours

**Rationale:**
- **Consistent:** Always 24-hour window, comparable across days
- **Continuous:** No artificial boundary at midnight
- **Relevant:** Shows recent throughput for capacity planning
- **Simple:** Easy to understand and calculate

**Implementation:**
```python
time_window_start = datetime.utcnow() - timedelta(hours=24)
# Filter runs completed after time_window_start
```

**Reversibility:** HIGH (can adjust window size)

**Impact:** Positive - provides daily throughput visibility

---

## Decision 6: System Health Score Formula

**Context:** Need single-score summary (0-10) for quick health assessment. Need to determine weightings for components.

**Options Considered:**
1. **Equal weighting:** All components equal weight (20% each)
2. **Priority weighting:** Task completion and queue depth weighted higher
3. **Adaptive weighting:** Weights adjust based on system state

**Selected:** Option 2 - Priority weighting

**Rationale:**
- **Task completion rate (30%):** Most important - executor health
- **Queue depth (25%):** Critical for autonomous operation
- **Skill consideration (20%):** Validates system investment
- **Skill invocation (15%):** Lower priority, still establishing baseline
- **Error rate (10%):** Currently 0%, less critical but important

**Formula:**
```
health_score = (
    completion_rate * 0.30 +
    queue_score * 0.25 +
    consideration_rate * 0.20 +
    invocation_score * 0.15 +
    (1 - error_rate) * 0.10
) * 10
```

**Reversibility:** HIGH (can adjust weights in metrics_updater.py)

**Impact:** Positive - reflects system priorities accurately

---

## Decision 7: Skill Invocation Rate Target - 10-30%

**Context:** Need target range for skill invocation rate to determine if threshold (70%) is appropriate.

**Options Considered:**
1. **Low target:** 5-15% (skills rarely used)
2. **Medium target:** 10-30% (chosen - balanced)
3. **High target:** 30-50% (skills frequently used)

**Selected:** Option 2 - 10-30% target

**Rationale:**
- **Not too low:** 10% minimum ensures skills are used when valuable
- **Not too high:** 30% maximum avoids over-reliance on skills
- **Empirical:** Based on skill system design (skills for complex tasks, not routine)
- **Observation:** 0% invocation for Runs 46-48 is appropriate (all straightforward tasks)

**Assessment method:** Calculate distance from target range
```
if invocation_rate < 10%:
    score = invocation_rate / 10%  # 0-1 scale
elif invocation_rate > 30%:
    score = max(0, 1 - (invocation_rate - 30%) / 20%)
else:
    score = 1.0  # Perfect, within target
```

**Reversibility:** HIGH (can adjust target range)

**Impact:** Positive - provides clear benchmark for skill system effectiveness

---

## Decision 8: Non-Blocking Error Handling

**Context:** Metrics update failure should not prevent task completion. Need error handling strategy.

**Options Considered:**
1. **Blocking:** Fail task completion if metrics update fails
2. **Non-blocking:** Log error but continue (chosen)
3. **Retry:** Retry metrics update before failing

**Selected:** Option 2 - Non-blocking with logging

**Rationale:**
- **Priority:** Task completion is primary, metrics are secondary
- **Resilience:** System continues operating even if metrics fail
- **Debugging:** Errors are logged for investigation
- **Recovery:** Manual update possible if automatic fails
- **Precedent:** Queue sync uses same pattern (non-blocking)

**Implementation:**
```python
try:
    result["metrics_sync"] = update_metrics_on_task_completion(...)
except Exception as e:
    log_message(f"Metrics sync failed (non-critical): {str(e)}", "WARN")
    result["metrics_sync"] = {"success": False, "error": str(e)}
```

**Reversibility:** LOW (would require significant refactoring to change)

**Impact:** Positive - system resilience prioritized over metrics accuracy

---

## Decision 9: Manual Update Capability

**Context:** Automatic updates are primary, but manual updates may be needed for corrections or testing.

**Options Considered:**
1. **Automatic only:** No manual update capability
2. **CLI tool:** Manual update via command line (chosen)
3. **Web UI:** Dashboard with edit forms

**Selected:** Option 2 - CLI tool

**Rationale:**
- **Simple:** CLI already exists for other sync operations
- **Accessible:** Available from terminal
- **Testable:** Dry-run mode for testing
- **Documented:** Usage examples in guide

**CLI usage:**
```bash
python3 2-engine/.autonomous/lib/metrics_updater.py \
  <project_dir> <task_id> <duration> <result> <run_number>
```

**Reversibility:** LOW (removing would reduce flexibility)

**Impact:** Positive - enables corrections and testing

---

## Decision 10: Documentation Scope

**Context:** Need comprehensive documentation for dashboard usage and maintenance.

**Options Considered:**
1. **Minimal:** Basic README only
2. **Moderate:** README + inline comments (chosen)
3. **Extensive:** Full guide with examples, troubleshooting, FAQ

**Selected:** Option 3 - Extensive documentation

**Rationale:**
- **Multiple users:** Planner and Executor both use dashboard
- **Long-term:** Dashboard will persist for many iterations
- **Complexity:** Metric calculations and formulas need explanation
- **Troubleshooting:** Common issues (anomalies, update failures) need solutions
- **Onboarding:** New users need comprehensive guide

**Documentation sections:**
1. Purpose - What and why
2. How to Read - Understanding metrics
3. How to Update - Automatic and manual
4. How to Use - Planning, reviews, monitoring
5. Metric Definitions - Formulas and targets
6. Troubleshooting - Common issues
7. Advanced Usage - Customization
8. Maintenance - Regular tasks
9. FAQ - Common questions
10. Changelog - Version history

**Reversibility:** LOW (documentation can be added to but not removed)

**Impact:** Positive - reduces support burden, enables self-service

---

## Summary of Decisions

| Decision | Selection | Reversibility | Impact |
|----------|-----------|---------------|--------|
| 1. Dashboard structure | 5 metrics | HIGH | Positive |
| 2. Anomalous data | Auto-filter | HIGH | Positive |
| 3. Integration point | roadmap_sync.py | MEDIUM | Positive |
| 4. Historical window | 10 runs | HIGH | Positive |
| 5. Daily window | 24 hours | HIGH | Positive |
| 6. Health score formula | Priority weights | HIGH | Positive |
| 7. Invocation target | 10-30% | HIGH | Positive |
| 8. Error handling | Non-blocking | LOW | Positive |
| 9. Manual updates | CLI tool | LOW | Positive |
| 10. Documentation | Extensive guide | LOW | Positive |

**Overall Assessment:** All decisions aligned with task objectives and system priorities. High reversibility for key technical decisions enables iteration based on usage.

---

**End of Decisions**
