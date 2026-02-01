# Performance Monitoring & Analytics - User Guide

**Version:** 1.0.0
**Feature ID:** F-014
**Created:** 2026-02-01

---

## Overview

The Performance Monitoring & Analytics system provides comprehensive visibility into RALF system performance over time. It tracks metrics, detects anomalies, triggers alerts, and generates reports to help operators understand system health and optimize performance.

### Key Benefits

- **Historical Tracking:** Store and analyze performance metrics from 1000+ runs
- **Trend Analysis:** Identify performance patterns (velocity, success rate, duration)
- **Anomaly Detection:** Automatically detect outliers and performance issues
- **Proactive Alerting:** Get notified before issues become critical
- **Actionable Insights:** Make data-driven optimization decisions

---

## Components

### 1. Metrics Collector (`metrics_collector.py`)

**Purpose:** Collect and store performance metrics from planner/executor runs.

**What it tracks:**
- Run duration
- Success/failure status
- Files modified
- Task IDs
- Blockers and errors

**Storage:** `2-engine/.autonomous/data/metrics/metrics.yaml` (YAML format, up to 1000 runs)

**Usage:**
```bash
# Collect metrics from all runs
python3 2-engine/.autonomous/lib/metrics_collector.py --collect

# Show metrics summary
python3 2-engine/.autonomous/lib/metrics_collector.py --summary
```

---

### 2. Historical Analyzer (`historical_analyzer.py`)

**Purpose:** Calculate trends and compare current performance to historical baselines.

**What it analyzes:**
- Velocity trends (runs per hour)
- Success rate trends
- Duration trends
- Throughput (files per run)

**Usage:**
```bash
# Analyze last 100 executor runs
python3 2-engine/.autonomous/lib/historical_analyzer.py --window 100 --agent executor

# Analyze planner runs
python3 2-engine/.autonomous/lib/historical_analyzer.py --agent planner

# Output as JSON
python3 2-engine/.autonomous/lib/historical_analyzer.py --json
```

**Output:**
```json
{
  "velocity": {"average": 5.2, "trend": "improving"},
  "success_rate": {"average": 95.5, "trend": "stable"},
  "duration": {"average": 450.3, "trend": "improving"}
}
```

---

### 3. Anomaly Detector (`anomaly_detector.py`)

**Purpose:** Detect statistical and rule-based anomalies in performance data.

**Detection methods:**
- **Statistical:** Z-score analysis (3σ = critical, 2.5σ = warning)
- **Rule-based:** Duration > 2x baseline average
- **Pattern-based:** Consecutive blocker streaks, success rate drops

**Usage:**
```bash
# Detect anomalies in executor runs
python3 2-engine/.autonomous/lib/anomaly_detector.py --agent executor

# Detect with custom baseline window
python3 2-engine/.autonomous/lib/anomaly_detector.py --window 50

# Show detailed anomalies
python3 2-engine/.autonomous/lib/anomaly_detector.py --verbose
```

**Anomaly severity levels:**
- **Critical:** Immediate attention required (e.g., 2x duration, < 50% success rate)
- **Warning:** Investigate soon (e.g., 1.5x duration, < 80% success rate)
- **Info:** For awareness (e.g., minor deviations)

---

### 4. Alert Manager (`alert_manager.py`)

**Purpose:** Configure alert thresholds and manage alert delivery.

**Alert channels:**
- **Log file:** All alerts logged to system logs
- **Dashboard:** Alerts appear in F-008 dashboard
- **Webhook:** (Future) Slack, Discord, email notifications

**Configuration:** `2-engine/.autonomous/config/alert-config.yaml`

**Usage:**
```bash
# Trigger test alert
python3 2-engine/.autonomous/lib/alert_manager.py --test

# Show alert summary (last 24 hours)
python3 2-engine/.autonomous/lib/alert_manager.py --summary 24

# Show alert history
python3 2-engine/.autonomous/lib/alert_manager.py --history
```

**Configuring thresholds:**

Edit `alert-config.yaml`:
```yaml
thresholds:
  duration:
    critical_seconds: 600  # Alert if run > 10 minutes
    warning_seconds: 300   # Alert if run > 5 minutes

  success_rate:
    critical_percent: 50   # Alert if success rate < 50%
    warning_percent: 80    # Alert if success rate < 80%
```

---

### 5. Performance Reporter (`performance_reporter.py`)

**Purpose:** Generate daily, weekly, and custom performance reports.

**Report formats:**
- **Markdown:** Human-readable reports
- **JSON:** Machine-readable data
- **CSV:** Spreadsheet-compatible export

**Usage:**
```bash
# Generate daily report
python3 2-engine/.autonomous/lib/performance_reporter.py --daily

# Generate weekly report
python3 2-engine/.autonomous/lib/performance_reporter.py --weekly

# Generate custom report (last 48 hours)
python3 2-engine/.autonomous/lib/performance_reporter.py --custom 48

# Generate CSV export
python3 2-engine/.autonomous/lib/performance_reporter.py --custom 24 --format csv
```

**Report location:** `2-engine/.autonomous/data/reports/`

---

## Integration with RALF

### Automatic Metrics Collection

Metrics are collected automatically after each run via the executor loop:

```bash
# In executor loop (after task completion)
python3 2-engine/.autonomous/lib/metrics_collector.py --collect
```

### Anomaly Detection on Each Run

After each run, the system checks for anomalies:

```python
# Example integration in executor loop
from lib.anomaly_detector import check_single_run

run_metrics = {...}  # Current run metrics
anomalies = check_single_run(run_metrics, 'executor')

if anomalies:
    from lib.alert_manager import trigger_alert
    for anomaly in anomalies:
        trigger_alert(
            anomaly['type'],
            anomaly['severity'],
            anomaly['message']
        )
```

### Dashboard Integration (F-008)

Alerts are sent to the dashboard via `events.yaml`:

- Real-time alert notifications
- Historical anomaly highlights
- Performance trend charts

---

## Understanding Metrics and Trends

### Velocity (Runs per Hour)

**What it measures:** How many tasks RALF completes per hour.

**Trend interpretation:**
- **Improving:** RALF is getting faster
- **Stable:** Consistent performance
- **Degrading:** RALF is slowing down (investigate bottlenecks)

**Typical values:**
- Good: > 5 runs/hour
- Average: 3-5 runs/hour
- Poor: < 3 runs/hour

### Success Rate (%)

**What it measures:** Percentage of runs that completed successfully.

**Trend interpretation:**
- **Improving:** Fewer failures/blockers
- **Stable:** Consistent quality
- **Degrading:** More failures (check for system issues)

**Typical values:**
- Excellent: > 95%
- Good: 85-95%
- Poor: < 85%

### Duration (seconds)

**What it measures:** Average time to complete a run.

**Trend interpretation:**
- **Improving:** Runs are completing faster
- **Stable:** Consistent duration
- **Degrading:** Runs are taking longer (check task complexity)

**Typical values:**
- Fast: < 300s (5 minutes)
- Average: 300-600s (5-10 minutes)
- Slow: > 600s (10 minutes)

---

## Troubleshooting

### Issue: No metrics collected

**Symptoms:** `metrics_collector.py --summary` shows 0 runs

**Solutions:**
1. Check if runs exist: `ls runs/executor/` and `ls runs/planner/`
2. Verify `metadata.yaml` files exist in run directories
3. Check file permissions: `ls -la .autonomous/data/metrics/`

### Issue: Anomaly detection not working

**Symptoms:** No anomalies detected despite obvious issues

**Solutions:**
1. Verify baseline window size: `--window 50` (need 50+ runs for baseline)
2. Check if metrics are recent: Metrics should include last 50 runs
3. Adjust thresholds in `alert-config.yaml`

### Issue: Alerts not triggering

**Symptoms:** Expected alerts not appearing

**Solutions:**
1. Verify alert channels enabled in `alert-config.yaml`
2. Check logs: `grep "ALERT" .autonomous/logs/`
3. Test alert system: `python3 lib/alert_manager.py --test`

### Issue: Dashboard not showing historical data

**Symptoms:** Dashboard shows real-time data only

**Solutions:**
1. Verify metrics collection ran: Check `metrics.yaml` exists
2. Restart dashboard server to reload metrics
3. Check browser console for errors

---

## Advanced Usage

### Custom Metrics Tracking

To track custom metrics (e.g., specific task types, error categories):

1. Add metrics extraction logic in `metrics_collector.py`:
```python
# In extract_metrics_from_run()
metrics['custom_metric'] = metadata.get('custom_field')
```

2. Update `historical_analyzer.py` to calculate trends for custom metric

3. Add alert threshold in `alert-config.yaml`

### Export Metrics for External Analysis

```bash
# Generate CSV for spreadsheet analysis
python3 lib/performance_reporter.py --custom 168 --format csv > weekly_export.csv

# Generate JSON for custom analysis
python3 lib/historical_analyzer.py --json > analysis.json
```

### Integration with Monitoring Tools

Metrics can be exported to external tools (Prometheus, Grafana, Datadog):

1. Use `performance_reporter.py` to generate JSON exports
2. Write a simple script to push JSON to external API
3. Configure webhook in `alert-config.yaml`

---

## Best Practices

1. **Review reports weekly:** Check weekly reports for performance trends
2. **Investigate anomalies:** Don't ignore critical alerts
3. **Adjust thresholds:** Tune alert thresholds based on your system's baseline
4. **Monitor trends:** Look for gradual degradation (not just sudden anomalies)
5. **Keep historical data:** Don't delete old metrics - useful for long-term analysis

---

## FAQ

**Q: How much disk space do metrics use?**

A: Approximately 1KB per run. 1000 runs = ~1MB. Very lightweight.

**Q: Can I export metrics to Excel?**

A: Yes! Use `--format csv` to generate spreadsheet-compatible exports.

**Q: How often should I generate reports?**

A: Daily reports are automatic. Weekly reports recommended for review.

**Q: What if I don't have 1000 runs yet?**

A: System works with as few as 10 runs. Accuracy improves with more data.

**Q: Can I customize alert thresholds?**

A: Yes! Edit `alert-config.yaml` to adjust all thresholds.

---

## Support and Documentation

**Configuration:** `2-engine/.autonomous/config/alert-config.yaml`
**Data Storage:** `2-engine/.autonomous/data/metrics/`
**Reports:** `2-engine/.autonomous/data/reports/`
**Alert History:** `2-engine/.autonomous/data/alerts/alert_history.yaml`

**Related Features:**
- F-008: Real-time Collaboration Dashboard
- F-006: User Preferences (configuration system)

---

**End of Performance Monitoring Guide**
