# BB5 Metrics Specification

**Version:** 1.0.0
**Created:** 2026-02-06
**Author:** Metrics Engineer
**Status:** Draft

---

## Overview

This document defines the comprehensive metrics collection specification for BlackBox5 (BB5) system monitoring. These metrics enable observability, performance analysis, and operational intelligence for the autonomous task execution system.

---

## Metric Naming Convention

All metrics follow the Prometheus naming convention:
```
bb5_<category>_<metric_name>_<unit>
```

- **Prefix:** `bb5_` - Identifies BB5 system metrics
- **Category:** `task`, `agent`, `queue`, `system`, `skill`, `git`
- **Metric Name:** Descriptive snake_case name
- **Unit Suffix:** `_total`, `_seconds`, `_bytes`, `_count`, `_ratio`

---

## 1. Task Metrics

### 1.1 Task Lifecycle Counters

#### `bb5_task_created_total`
- **Type:** Counter
- **Description:** Total number of tasks created
- **Labels:**
  - `priority` (critical, high, medium, low)
  - `type` (feature, bugfix, refactor, docs, research)
  - `source` (manual, planner, automated)
- **Collection Frequency:** On task creation
- **Example PromQL:**
  ```promql
  # Tasks created per day by priority
  increase(bb5_task_created_total[1d])

  # High priority task creation rate
  rate(bb5_task_created_total{priority="high"}[5m])
  ```

#### `bb5_task_completed_total`
- **Type:** Counter
- **Description:** Total number of tasks completed
- **Labels:**
  - `status` (success, failure, partial, blocked)
  - `priority` (critical, high, medium, low)
  - `exit_code` (complete, partial, blocked)
- **Collection Frequency:** On task completion
- **Example PromQL:**
  ```promql
  # Task completion rate by status
  rate(bb5_task_completed_total[1h])

  # Success ratio over last 24h
  bb5_task_completed_total{status="success"} / bb5_task_completed_total
  ```

#### `bb5_task_duration_seconds`
- **Type:** Histogram
- **Description:** Task execution duration in seconds
- **Buckets:** [30, 60, 120, 300, 600, 1200, 1800, 3600, 7200, 14400]
- **Labels:**
  - `task_type` (feature, bugfix, refactor, docs)
  - `priority` (critical, high, medium, low)
  - `agent_type` (executor, planner, scout)
- **Collection Frequency:** On task completion
- **Example PromQL:**
  ```promql
  # 95th percentile task duration
  histogram_quantile(0.95, bb5_task_duration_seconds_bucket)

  # Average duration by task type
  rate(bb5_task_duration_seconds_sum[1h]) / rate(bb5_task_duration_seconds_count[1h])
  ```

### 1.2 Task State Gauges

#### `bb5_task_active_count`
- **Type:** Gauge
- **Description:** Current number of active (in_progress) tasks
- **Labels:**
  - `priority` (critical, high, medium, low)
  - `agent_id` (executor-1, executor-2, etc.)
- **Collection Frequency:** Every 60 seconds
- **Example PromQL:**
  ```promql
  # Total active tasks
  bb5_task_active_count

  # Critical tasks in progress
  bb5_task_active_count{priority="critical"}
  ```

#### `bb5_task_pending_count`
- **Type:** Gauge
- **Description:** Current number of pending tasks
- **Labels:**
  - `priority` (critical, high, medium, low)
  - `blocked_by_dependencies` (true, false)
- **Collection Frequency:** Every 60 seconds
- **Example PromQL:**
  ```promql
  # Pending tasks blocked by dependencies
  bb5_task_pending_count{blocked_by_dependencies="true"}
  ```

### 1.3 Task Success Metrics

#### `bb5_task_success_ratio`
- **Type:** Gauge
- **Description:** Rolling success rate over last N tasks
- **Labels:**
  - `window` (10, 50, 100)
  - `task_type` (all, feature, bugfix, etc.)
- **Collection Frequency:** Every 5 minutes
- **Example PromQL:**
  ```promql
  # Success rate over last 100 tasks
  bb5_task_success_ratio{window="100"}

  # Alert when success rate drops
  bb5_task_success_ratio < 0.8
  ```

#### `bb5_task_blocked_total`
- **Type:** Counter
- **Description:** Total tasks blocked by dependencies or external factors
- **Labels:**
  - `blocker_type` (dependency, external_input, resource_unavailable, permission)
  - `blocking_task_id` (task identifier or "unknown")
- **Collection Frequency:** On task block event
- **Example PromQL:**
  ```promql
  # Block rate by type
  rate(bb5_task_blocked_total[1h])

  # Tasks blocked waiting on external input
  bb5_task_blocked_total{blocker_type="external_input"}
  ```

---

## 2. Agent Metrics

### 2.1 Agent Session Metrics

#### `bb5_agent_sessions_total`
- **Type:** Counter
- **Description:** Total number of agent sessions executed
- **Labels:**
  - `agent_type` (planner, executor, scout, verifier, orchestrator)
  - `result` (success, failure, timeout, error)
- **Collection Frequency:** On session completion
- **Example PromQL:**
  ```promql
  # Sessions per day by agent type
  increase(bb5_agent_sessions_total[1d])

  # Executor failure rate
  rate(bb5_agent_sessions_total{agent_type="executor",result="failure"}[1h])
  ```

#### `bb5_agent_session_duration_seconds`
- **Type:** Histogram
- **Description:** Agent session duration in seconds
- **Buckets:** [10, 30, 60, 120, 300, 600, 1200, 1800, 3600]
- **Labels:**
  - `agent_type` (planner, executor, scout, verifier)
  - `task_complexity` (simple, medium, complex)
- **Collection Frequency:** On session completion
- **Example PromQL:**
  ```promql
  # Average session duration by agent type
  rate(bb5_agent_session_duration_seconds_sum[1h]) / rate(bb5_agent_session_duration_seconds_count[1h])

  # Sessions taking > 30 minutes
  bb5_agent_session_duration_seconds_bucket{le="1800"} - bb5_agent_session_duration_seconds_bucket{le="1200"}
  ```

#### `bb5_agent_active_sessions`
- **Type:** Gauge
- **Description:** Currently active agent sessions
- **Labels:**
  - `agent_type` (planner, executor, scout, verifier)
  - `session_id` (unique identifier)
- **Collection Frequency:** Real-time (on session start/end)
- **Example PromQL:**
  ```promql
  # Total active sessions
  sum(bb5_agent_active_sessions)

  # Active executors
  bb5_agent_active_sessions{agent_type="executor"}
  ```

### 2.2 Agent Type Distribution

#### `bb5_agent_type_distribution_ratio`
- **Type:** Gauge
- **Description:** Percentage distribution of agent types over time window
- **Labels:**
  - `agent_type` (planner, executor, scout, verifier)
  - `window` (1h, 24h, 7d)
- **Collection Frequency:** Every 5 minutes
- **Example PromQL:**
  ```promql
  # Agent type distribution (normalized)
  bb5_agent_sessions_total / sum(bb5_agent_sessions_total)
  ```

### 2.3 Token Usage Metrics

#### `bb5_agent_tokens_total`
- **Type:** Counter
- **Description:** Total tokens consumed by agent sessions
- **Labels:**
  - `agent_type` (planner, executor, scout, verifier)
  - `token_type` (input, output, total)
  - `model` (claude-opus, claude-sonnet, etc.)
- **Collection Frequency:** On session completion
- **Example PromQL:**
  ```promql
  # Token usage per hour
  increase(bb5_agent_tokens_total[1h])

  # Average tokens per session
  bb5_agent_tokens_total / bb5_agent_sessions_total
  ```

#### `bb5_agent_tokens_per_session`
- **Type:** Histogram
- **Description:** Token count distribution per session
- **Buckets:** [1000, 5000, 10000, 25000, 50000, 100000, 200000]
- **Labels:**
  - `agent_type` (planner, executor, scout)
- **Collection Frequency:** On session completion
- **Example PromQL:**
  ```promql
  # 99th percentile token usage
  histogram_quantile(0.99, bb5_agent_tokens_per_session_bucket)
  ```

### 2.4 Agent Performance

#### `bb5_agent_actions_total`
- **Type:** Counter
- **Description:** Total actions taken by agents (file reads, edits, commands)
- **Labels:**
  - `agent_type` (executor, planner)
  - `action_type` (read, write, edit, bash, grep, skill_invoke)
  - `result` (success, failure)
- **Collection Frequency:** On action execution
- **Example PromQL:**
  ```promql
  # Action rate by type
  rate(bb5_agent_actions_total[5m])

  # Failed actions
  bb5_agent_actions_total{result="failure"}
  ```

---

## 3. Queue Metrics

### 3.1 Queue Depth

#### `bb5_queue_depth`
- **Type:** Gauge
- **Description:** Current number of tasks in queue
- **Labels:**
  - `queue_name` (default, priority, scheduled)
  - `status` (pending, claimed, processing)
- **Collection Frequency:** Every 30 seconds
- **Example PromQL:**
  ```promql
  # Total queue depth
  sum(bb5_queue_depth)

  # Pending tasks in priority queue
  bb5_queue_depth{queue_name="priority",status="pending"}

  # Alert when queue too deep
  bb5_queue_depth > 20
  ```

#### `bb5_queue_depth_max`
- **Type:** Gauge
- **Description:** Maximum queue depth over time window
- **Labels:**
  - `window` (1h, 24h)
- **Collection Frequency:** Every 5 minutes
- **Example PromQL:**
  ```promql
  # Max queue depth in last hour
  max_over_time(bb5_queue_depth[1h])
  ```

### 3.2 Task Wait Time

#### `bb5_queue_wait_seconds`
- **Type:** Histogram
- **Description:** Time tasks spend waiting in queue before processing
- **Buckets:** [0, 30, 60, 300, 600, 1800, 3600, 7200, 14400]
- **Labels:**
  - `priority` (critical, high, medium, low)
  - `queue_name` (default, priority)
- **Collection Frequency:** On task claim
- **Example PromQL:**
  ```promql
  # Average wait time by priority
  rate(bb5_queue_wait_seconds_sum[1h]) / rate(bb5_queue_wait_seconds_count[1h])

  # 95th percentile wait time
  histogram_quantile(0.95, bb5_queue_wait_seconds_bucket)
  ```

#### `bb5_queue_wait_time_exceeded_total`
- **Type:** Counter
- **Description:** Tasks that exceeded maximum wait time threshold
- **Labels:**
  - `priority` (critical, high, medium, low)
  - `threshold_seconds` (300, 600, 1800)
- **Collection Frequency:** On task claim (if exceeded)
- **Example PromQL:**
  ```promql
  # Critical tasks waiting > 5 minutes
  rate(bb5_queue_wait_time_exceeded_total{priority="critical",threshold_seconds="300"}[1h])
  ```

### 3.3 Queue Priority Distribution

#### `bb5_queue_priority_distribution`
- **Type:** Gauge
- **Description:** Current distribution of tasks by priority
- **Labels:**
  - `priority` (critical, high, medium, low)
  - `status` (pending, claimed)
- **Collection Frequency:** Every 60 seconds
- **Example PromQL:**
  ```promql
  # Priority distribution percentage
  bb5_queue_priority_distribution / sum(bb5_queue_priority_distribution)

  # Critical task ratio
  bb5_queue_priority_distribution{priority="critical"} / sum(bb5_queue_priority_distribution)
  ```

### 3.4 Claimed vs Unclaimed

#### `bb5_queue_claimed_total`
- **Type:** Counter
- **Description:** Total tasks claimed from queue
- **Labels:**
  - `agent_type` (executor, planner)
  - `claim_method` (auto, manual)
- **Collection Frequency:** On task claim
- **Example PromQL:**
  ```promql
  # Claim rate
  rate(bb5_queue_claimed_total[5m])
  ```

#### `bb5_queue_unclaimed_count`
- **Type:** Gauge
- **Description:** Current unclaimed tasks by age
- **Labels:**
  - `age_bucket` (0-1h, 1-4h, 4-24h, 24h+)
  - `priority` (critical, high, medium, low)
- **Collection Frequency:** Every 5 minutes
- **Example PromQL:**
  ```promql
  # Old unclaimed tasks
  sum(bb5_queue_unclaimed_count{age_bucket="24h+"})

  # Critical tasks unclaimed > 1 hour
  bb5_queue_unclaimed_count{priority="critical",age_bucket="1-4h"}
  ```

#### `bb5_queue_claim_ratio`
- **Type:** Gauge
- **Description:** Ratio of claimed to total queueable tasks
- **Labels:**
  - `window` (1h, 24h)
- **Collection Frequency:** Every 5 minutes
- **Example PromQL:**
  ```promql
  # Claim ratio (should be > 0.8 for healthy system)
  bb5_queue_claimed_total / (bb5_queue_claimed_total + bb5_queue_unclaimed_count)
  ```

---

## 4. System Health Metrics

### 4.1 Hook Execution

#### `bb5_hook_executions_total`
- **Type:** Counter
- **Description:** Total hook executions
- **Labels:**
  - `hook_name` (pre-task, post-task, on-complete, on-error)
  - `hook_type` (validation, notification, sync)
  - `result` (success, failure, skipped)
- **Collection Frequency:** On hook execution
- **Example PromQL:**
  ```promql
  # Hook success rate
  bb5_hook_executions_total{result="success"} / bb5_hook_executions_total

  # Failed hooks by name
  rate(bb5_hook_executions_total{result="failure"}[5m])
  ```

#### `bb5_hook_execution_duration_seconds`
- **Type:** Histogram
- **Description:** Hook execution duration
- **Buckets:** [0.1, 0.5, 1, 2, 5, 10, 30]
- **Labels:**
  - `hook_name` (pre-task, post-task, on-complete)
- **Collection Frequency:** On hook completion
- **Example PromQL:**
  ```promql
  # Slow hooks (> 5 seconds)
  bb5_hook_execution_duration_seconds_bucket{le="5"} - bb5_hook_execution_duration_seconds_bucket{le="2"}
  ```

### 4.2 Git Operations

#### `bb5_git_operations_total`
- **Type:** Counter
- **Description:** Total Git operations performed
- **Labels:**
  - `operation` (commit, push, pull, branch, merge)
  - `result` (success, failure, conflict)
- **Collection Frequency:** On Git operation
- **Example PromQL:**
  ```promql
  # Push success rate
  bb5_git_operations_total{operation="push",result="success"} / bb5_git_operations_total{operation="push"}

  # Failed pushes per hour
  increase(bb5_git_operations_total{operation="push",result="failure"}[1h])
  ```

#### `bb5_git_push_success_ratio`
- **Type:** Gauge
- **Description:** Rolling success ratio for Git push operations
- **Labels:**
  - `window` (10, 50, 100)
- **Collection Frequency:** Every 5 minutes
- **Example PromQL:**
  ```promql
  # Alert on push failures
  bb5_git_push_success_ratio < 0.95
  ```

### 4.3 Documentation Health

#### `bb5_docs_completeness_ratio`
- **Type:** Gauge
- **Description:** Documentation completeness percentage
- **Labels:**
  - `doc_type` (api, architecture, operational, runbook)
  - `component` (core, engine, memory, roadmap)
- **Collection Frequency:** Daily (via automated scan)
- **Example PromQL:**
  ```promql
  # Overall documentation health
  avg(bb5_docs_completeness_ratio)

  # API documentation status
  bb5_docs_completeness_ratio{doc_type="api"}
  ```

#### `bb5_docs_outdated_count`
- **Type:** Gauge
- **Description:** Count of outdated documentation pages
- **Labels:**
  - `age_bucket` (7d, 30d, 90d+)
  - `doc_type` (api, architecture, operational)
- **Collection Frequency:** Daily
- **Example PromQL:**
  ```promql
  # Docs not updated in 30+ days
  sum(bb5_docs_outdated_count{age_bucket="30d"})
  ```

### 4.4 Error Rates

#### `bb5_errors_total`
- **Type:** Counter
- **Description:** Total system errors
- **Labels:**
  - `error_type` (validation, execution, system, network)
  - `component` (agent, queue, hook, git, storage)
  - `severity` (warning, error, critical)
- **Collection Frequency:** On error occurrence
- **Example PromQL:**
  ```promql
  # Error rate by component
  rate(bb5_errors_total[5m])

  # Critical errors
  rate(bb5_errors_total{severity="critical"}[1m])

  # Validation errors per hour
  increase(bb5_errors_total{error_type="validation"}[1h])
  ```

#### `bb5_error_rate`
- **Type:** Gauge
- **Description:** Error rate per operation
- **Labels:**
  - `component` (agent, queue, hook)
  - `window` (1m, 5m, 1h)
- **Collection Frequency:** Every minute
- **Example PromQL:**
  ```promql
  # Error rate alert
  bb5_error_rate > 0.05
  ```

### 4.5 System Availability

#### `bb5_system_uptime_seconds`
- **Type:** Counter
- **Description:** Total system uptime in seconds
- **Labels:**
  - `component` (core, queue, agents)
- **Collection Frequency:** Every 60 seconds
- **Example PromQL:**
  ```promql
  # Uptime percentage
  bb5_system_uptime_seconds / (bb5_system_uptime_seconds + bb5_system_downtime_seconds) * 100
  ```

#### `bb5_system_health_score`
- **Type:** Gauge
- **Description:** Composite health score (0-100)
- **Labels:**
  - `component` (overall, task, agent, queue, system)
- **Collection Frequency:** Every 5 minutes
- **Example PromQL:**
  ```promql
  # Overall health score
  bb5_system_health_score{component="overall"}

  # Alert on degraded health
  bb5_system_health_score < 75
  ```

---

## 5. Skill System Metrics

### 5.1 Skill Usage

#### `bb5_skill_invocations_total`
- **Type:** Counter
- **Description:** Total skill invocations
- **Labels:**
  - `skill_name` (bmad-dev, bmad-architect, etc.)
  - `trigger_type` (auto, manual, keyword)
  - `result` (success, failure, skipped)
- **Collection Frequency:** On skill invocation
- **Example PromQL:**
  ```promql
  # Skill usage distribution
  bb5_skill_invocations_total / sum(bb5_skill_invocations_total)

  # Top used skills
  topk(5, bb5_skill_invocations_total)
  ```

#### `bb5_skill_considerations_total`
- **Type:** Counter
- **Description:** Total skill considerations (checked but not invoked)
- **Labels:**
  - `skill_name` (bmad-dev, bmad-architect, etc.)
  - `reason` (confidence_low, not_applicable, user_override)
- **Collection Frequency:** On skill check
- **Example PromQL:**
  ```promql
  # Consideration to invocation ratio
  bb5_skill_considerations_total / bb5_skill_invocations_total
  ```

### 5.2 Skill Effectiveness

#### `bb5_skill_success_ratio`
- **Type:** Gauge
- **Description:** Success rate by skill
- **Labels:**
  - `skill_name` (bmad-dev, bmad-architect, etc.)
  - `window` (10, 50, 100)
- **Collection Frequency:** Every 5 minutes
- **Example PromQL:**
  ```promql
  # Skills with < 80% success rate
  bb5_skill_success_ratio < 0.8
  ```

---

## 6. Storage & Performance Metrics

### 6.1 Storage Metrics

#### `bb5_storage_size_bytes`
- **Type:** Gauge
- **Description:** Storage size by component
- **Labels:**
  - `component` (tasks, runs, logs, metrics)
  - `storage_type` (local, cloud)
- **Collection Frequency:** Every hour
- **Example PromQL:**
  ```promql
  # Total storage usage
  sum(bb5_storage_size_bytes)

  # Storage growth rate
  rate(bb5_storage_size_bytes[24h])
  ```

#### `bb5_storage_operations_total`
- **Type:** Counter
- **Description:** Storage read/write operations
- **Labels:**
  - `operation` (read, write, delete)
  - `component` (task, run, log)
- **Collection Frequency:** On operation

### 6.2 Performance Metrics

#### `bb5_io_latency_seconds`
- **Type:** Histogram
- **Description:** I/O operation latency
- **Buckets:** [0.001, 0.01, 0.1, 0.5, 1, 5]
- **Labels:**
  - `operation` (read, write)
  - `storage_type` (local, cloud)

---

## Alerting Rules

### Critical Alerts

```yaml
groups:
  - name: bb5_critical
    rules:
      - alert: BB5HighErrorRate
        expr: rate(bb5_errors_total{severity="critical"}[5m]) > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "BB5 critical errors detected"

      - alert: BB5QueueDepthHigh
        expr: bb5_queue_depth > 20
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "BB5 queue depth exceeded 20 tasks"

      - alert: BB5TaskSuccessRateLow
        expr: bb5_task_success_ratio{window="100"} < 0.8
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "BB5 task success rate below 80%"

      - alert: BB5GitPushFailing
        expr: bb5_git_push_success_ratio < 0.95
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "BB5 Git push success rate degraded"

      - alert: BB5HealthScoreLow
        expr: bb5_system_health_score{component="overall"} < 60
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "BB5 overall health score critically low"

      - alert: BB5CriticalTasksWaiting
        expr: bb5_queue_wait_time_exceeded_total{priority="critical",threshold_seconds="300"} > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Critical tasks waiting > 5 minutes"
```

---

## Collection Implementation

### Metric Collection Points

| Metric | Collection Point | Method |
|--------|-----------------|--------|
| Task metrics | Task lifecycle events | Event hooks |
| Agent metrics | Session start/end | Session wrapper |
| Queue metrics | Queue operations | Queue manager |
| System metrics | Health checks | Background job |
| Git metrics | Git operations | Git wrapper |
| Skill metrics | Skill invocation | Skill framework |

### Storage Backend

Metrics are stored in:
1. **Local files:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/data/metrics/`
2. **Prometheus:** Remote write endpoint (optional)
3. **Dashboard:** YAML-based metrics dashboard

### Retention Policy

| Metric Type | Retention |
|-------------|-----------|
| Counter | 90 days |
| Gauge | 30 days |
| Histogram | 14 days |
| Raw events | 7 days |

---

## Dashboard Queries

### Key Performance Indicators

```promql
# Tasks per day
increase(bb5_task_completed_total[1d])

# Average task duration (last 24h)
avg_over_time(
  rate(bb5_task_duration_seconds_sum[1h]) / rate(bb5_task_duration_seconds_count[1h])
[24h])

# System health trend
delta(bb5_system_health_score[1h])

# Queue health
bb5_queue_depth / bb5_queue_depth_max

# Agent utilization
sum(bb5_agent_active_sessions) / sum(bb5_agent_max_sessions)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-06 | Initial specification |

---

## Related Documents

- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/metrics-dashboard.yaml`
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/data/metrics/metrics.yaml`
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/metrics/metrics-dashboard.yaml`
