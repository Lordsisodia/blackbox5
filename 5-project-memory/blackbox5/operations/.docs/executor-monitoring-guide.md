# Executor Monitoring Guide

**Version:** 1.0.0
**Last Updated:** 2026-02-01
**Purpose:** Guide for using and interpreting the executor monitoring dashboard

---

## Overview

The executor monitoring dashboard (`operations/executor-dashboard.yaml`) provides centralized visibility into RALF-Executor performance, quality metrics, and trends over time.

## Dashboard Structure

### 1. Overview Metrics

High-level health indicators:

| Metric | Description | Target |
|--------|-------------|--------|
| `success_rate_percent` | Percentage of tasks completed successfully | >90% |
| `total_executions` | Total number of executor runs | N/A |
| `successful_completions` | Count of completed tasks | N/A |

**Usage:** Check this section first for a quick health check.

### 2. Performance Metrics

Task execution timing data:

```yaml
performance:
  average_completion_time:
    overall: 4320  # seconds
    by_type:
      implement: 2850
      analyze: 5200
```

**Key Insights:**
- Analyze tasks take ~87 minutes on average
- Implement tasks take ~47 minutes on average
- Audit tasks can vary significantly (credential audit took ~8 hours)

**Usage:** Use for capacity planning and time estimation.

### 3. Skill Usage Metrics

Tracks skill system effectiveness:

```yaml
skill_usage:
  total_skill_invocations: 0
  invocation_rate_percent: 0.0
  phase_1_5_compliance:
    compliance_rate_percent: 100.0
```

**Key Metrics:**
- `invocation_rate_percent`: Target is 50% for applicable tasks
- `phase_1_5_compliance`: Should be 100% (skill checking mandatory)

**Usage:** Monitor to ensure skill system is operational.

### 4. Quality Metrics

Documentation and process compliance:

```yaml
quality:
  documentation_compliance:
    compliance_rate_percent: 100.0
  commit_compliance:
    compliance_rate_percent: 75.0
```

**Targets:**
- Documentation: 100% (all runs must have THOUGHTS.md, RESULTS.md, DECISIONS.md)
- Commits: 100% (all completed tasks should be committed)
- Task Movement: 100% (all tasks moved to completed/)

### 5. Historical Run Data

Last 20 runs with detailed information:

```yaml
runs:
  - id: 28
    task: "TASK-1769913000"
    type: implement
    status: completed
    duration_seconds: 4382
```

**Usage:** Investigate specific runs, identify patterns.

### 6. Alerts & Recommendations

Active issues and suggested actions:

```yaml
alerts:
  active:
    - level: warning
      message: "Commit compliance at 75%"
      action: "Verify commit workflow"
```

**Usage:** Prioritize work based on active alerts.

---

## How to Update the Dashboard

### Automated Updates

The dashboard is designed to be updated automatically after each run. The update process:

1. Extract metrics from `runs/executor/run-XXXX/metadata.yaml`
2. Calculate aggregate statistics
3. Update historical run data
4. Re-evaluate alerts

### Manual Updates

To manually update the dashboard:

```bash
# 1. Read the current dashboard
cat operations/executor-dashboard.yaml

# 2. Extract latest run data
ls -la runs/executor/ | tail -5

# 3. Update relevant sections
# Edit operations/executor-dashboard.yaml

# 4. Update timestamp
# Change last_updated field
```

---

## Interpreting Metrics

### Success Rate

- **>95%**: Excellent - system is healthy
- **90-95%**: Good - minor issues may exist
- **80-90%**: Warning - investigate failure patterns
- **<80%**: Critical - immediate attention required

### Skill Invocation Rate

- **>40%**: Target achieved - skills being used effectively
- **20-40%**: Improving - monitor for continued growth
- **<20%**: Investigation needed - check Phase 1.5 compliance
- **0%**: Critical - skill system not operational

### Completion Time Variance

- **<20%**: Excellent estimation accuracy
- **20-40%**: Good - minor adjustments needed
- **40-60%**: Warning - review estimation guidelines
- **>60%**: Critical - estimation process broken

---

## Common Queries

### Find Longest Running Tasks

```bash
grep -A2 "duration_seconds" operations/executor-dashboard.yaml | \
  grep -v "^--$" | sort -t: -k2 -n -r | head -10
```

### Check Skill Usage Trend

```bash
# View recent runs skill usage
grep "skill_used" operations/executor-dashboard.yaml | tail -10
```

### Find Tasks by Type

```bash
# Count tasks by type
grep "type:" operations/executor-dashboard.yaml | sort | uniq -c
```

---

## Alert Response Guide

### Info Alerts

- No immediate action required
- Monitor for trends
- Document in next retrospective

### Warning Alerts

- Investigate within 24 hours
- Determine root cause
- Create task if fix needed

### Critical Alerts

- Stop current work if related
- Investigate immediately
- Escalate to team lead
- Document resolution

---

## Integration with Other Systems

### RALF-Context

The dashboard feeds into `RALF-CONTEXT.md` for cross-loop memory:

```yaml
# From RALF-CONTEXT.md
current_system_state:
  success_rate: 82.8%
  skill_invocation_rate: 0%
```

### Improvement Backlog

Dashboard alerts can generate improvement tasks:

```yaml
# In operations/improvement-backlog.yaml
- id: IMP-XXXX
  source: "dashboard_alert"
  description: "Address commit compliance gap"
```

### Task Queue

Dashboard insights inform task prioritization:

- Low skill usage → Create skill adoption tasks
- High failure rate → Create reliability tasks
- Long completion times → Create optimization tasks

---

## Best Practices

1. **Review dashboard weekly** - Identify trends before they become issues
2. **Act on alerts promptly** - Don't let warnings accumulate
3. **Update after each run** - Keep data fresh for accurate metrics
4. **Correlate with learnings** - Connect metrics to qualitative insights
5. **Share with team** - Make metrics visible to all stakeholders

---

## Troubleshooting

### Dashboard Out of Date

**Symptom:** Metrics don't reflect recent runs
**Fix:**
```bash
# Rebuild from run metadata
for run in runs/executor/run-*/metadata.yaml; do
  echo "Processing $run"
done
# Update dashboard with extracted data
```

### Inconsistent Metrics

**Symptom:** Calculated metrics don't match raw data
**Fix:**
1. Verify all run metadata files are valid YAML
2. Check for missing duration_seconds values
3. Recalculate aggregates from raw data

### Missing Historical Data

**Symptom:** Runs missing from historical section
**Fix:**
1. Check if run directory exists
2. Verify metadata.yaml is present
3. Add missing run entry manually

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-01 | Initial dashboard and guide |
