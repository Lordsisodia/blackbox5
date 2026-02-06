# BB5 Operations Hooks - SRE Analysis

**Research Date:** 2026-02-06
**Analyst:** DevOps/Operations Engineer
**Scope:** Reliable operations, monitoring, maintenance, and degradation prevention for BlackBox5

---

## Executive Summary

BB5 is a complex autonomous agent system with multiple interconnected components: task queues, skill registries, run tracking, metrics collection, and state synchronization. Without proper operational hooks, the system is vulnerable to:

- **Silent data corruption** (queue.yaml, skill-registry.yaml drift)
- **Orphaned tasks** (in_progress tasks that never complete)
- **Storage bloat** (unbounded run folder growth)
- **Metrics blindness** (stale or missing operational data)
- **Cascading failures** (one component failure affecting others)

This document identifies critical operational hooks needed to maintain BB5 as a reliable, production-grade system.

---

## 1. Health Check Hooks

### 1.1 Session Start Health Check
**Trigger:** Every new session start
**Purpose:** Validate system state before work begins

**What it checks:**
```yaml
health_checks:
  critical_files:
    - queue.yaml (valid YAML, readable)
    - skill-registry.yaml (valid YAML, readable)
    - timeline.yaml (valid YAML, readable)
    - operations/skill-selection.yaml (valid YAML, readable)

  queue_integrity:
    - Total task count matches metadata
    - No duplicate task IDs
    - All blockedBy references exist
    - No circular dependencies
    - Status counts (pending/in_progress/completed) match actual

  filesystem:
    - runs/ directory writable
    - tasks/active/ directory readable
    - .autonomous/communications/ writable
    - Disk space > 10% available

  git_state:
    - Repository not in conflicted state
    - No uncommitted changes in critical files
    - Remote reachable (if network available)
```

**Failure modes:**
- WARNING: Non-critical file missing - log and continue
- ERROR: Critical file corrupted - block session, alert user
- ERROR: Disk space critical - block session, require cleanup

**Prevents:** Working with corrupted state, making changes that worsen corruption.

---

### 1.2 Pre-Execution Validation Hook
**Trigger:** Before starting any task
**Purpose:** Ensure task is ready for execution

**What it checks:**
```yaml
pre_execution_checks:
  task_file:
    - Task file exists and is readable
    - Task status is "pending" (not already in_progress)
    - All blockedBy tasks are completed
    - Task ID is unique across system

  dependencies:
    - Required skills available in skill-registry.yaml
    - Required tools/binaries available
    - Required environment variables set

  context:
    - Run folder initialized with required files
    - THOUGHTS.md created and writable
    - Previous related runs accessible (if needed)
```

**Failure modes:**
- BLOCK: Task already in_progress - check for orphaned task
- BLOCK: Dependencies not met - update blockedBy or complete deps first
- WARN: Context incomplete - initialize before proceeding

**Prevents:** Duplicate work, working on blocked tasks, missing dependencies.

---

### 1.3 System Health Dashboard Update
**Trigger:** Every 30 minutes during active sessions
**Purpose:** Continuous monitoring of system vitals

**What it tracks:**
```yaml
vitals:
  queue_health:
    - Tasks in_progress > 24 hours (stuck detection)
    - Tasks pending > 7 days (backlog aging)
    - Critical priority tasks count
    - Blocked tasks count

  storage:
    - runs/ directory size
    - .autonomous/logs/ size
    - Number of run folders
    - Largest files in system

  metrics:
    - Last metrics update timestamp
    - skill-registry.yaml age
    - executor-dashboard.yaml age
    - improvement-metrics.yaml age

  performance:
    - Average task completion time (trend)
    - Success rate (last 10 tasks)
    - Skill invocation rate
```

**Output:** Updates to `operations/system-health.yaml`

**Prevents:** Gradual degradation unnoticed, storage exhaustion, stale metrics.

---

## 2. Monitoring & Alerting Hooks

### 2.1 Task State Change Monitor
**Trigger:** On any task status change
**Purpose:** Track task lifecycle and detect anomalies

**What it does:**
```yaml
monitoring:
  on_status_change:
    - Log change to timeline.yaml
    - Update queue.yaml metadata
    - Check for state transition validity
    - Alert on suspicious transitions:
        - pending -> completed (skip in_progress)
        - completed -> pending (reopened without reason)
        - in_progress -> pending (abandoned)

  anomaly_detection:
    - Task in_progress > 4 hours (potential stuck)
    - Task completed < 5 minutes (potential false completion)
    - Multiple tasks marked complete in short window (batch issues)
    - Task status doesn't match run folder state
```

**Alerts go to:** `.autonomous/communications/events.yaml`

**Prevents:** Orphaned tasks, false completions, state drift.

---

### 2.2 File Corruption Detection Hook
**Trigger:** Before/after critical file modifications
**Purpose:** Detect and prevent YAML corruption

**What it checks:**
```yaml
corruption_detection:
  queue.yaml:
    - Valid YAML syntax before write
    - Valid YAML syntax after write
    - Required fields present (schema.version, tasks, metadata)
    - Task count matches actual array length
    - Backup created before modification

  skill-registry.yaml:
    - Valid YAML syntax
    - Required sections present
    - No null values in critical fields
    - Referential integrity (skills referenced in metrics exist)

  timeline.yaml:
    - Valid YAML syntax
    - Chronological event ordering
    - No duplicate event IDs
```

**On corruption detected:**
1. Block the write operation
2. Restore from backup
3. Alert user with details
4. Log incident to `.autonomous/communications/events.yaml`

**Prevents:** Catastrophic data loss from corrupted YAML files.

---

### 2.3 Metrics Freshness Monitor
**Trigger:** Hourly + on demand
**Purpose:** Ensure metrics are current and accurate

**What it checks:**
```yaml
metrics_freshness:
  skill-metrics.yaml:
    - Last updated < 24 hours
    - task_outcomes count matches actual completed tasks
    - No skills with null effectiveness_score

  executor-dashboard.yaml:
    - Last updated < 24 hours
    - Total runs matches actual run folders
    - Success rate calculation accurate

  improvement-metrics.yaml:
    - Last updated < 7 days
    - Pipeline stages consistent
    - No negative conversion rates

  quality-gates.yaml:
    - Version matches codebase
    - All referenced files exist
```

**On stale metrics:**
- Auto-trigger metrics collection
- Flag for manual review if auto-collection fails
- Update timestamp after successful refresh

**Prevents:** Decisions based on stale data, undetected metric drift.

---

### 2.4 Budget & Token Usage Monitor
**Trigger:** Every 15 minutes during active work
**Purpose:** Prevent runaway token usage and budget overruns

**What it tracks:**
```yaml
token_monitoring:
  session_level:
    - Current session token count
    - Tokens per hour rate
    - Estimated cost (if API pricing available)
    - Comparison to similar past tasks

  task_level:
    - Tokens used vs task estimate
    - Alert at 70%, 85%, 95% of estimated tokens
    - Force checkpoint at 95%

  historical:
    - Daily token usage trend
    - Weekly token usage pattern
    - Unusual spikes detection
```

**Alerts:**
- INFO: 70% of estimate reached
- WARN: 85% of estimate reached - prepare to checkpoint
- CRITICAL: 95% reached - force checkpoint, require explicit continue

**Prevents:** Budget overruns, context window exhaustion, runaway sessions.

---

## 3. Maintenance & Cleanup Hooks

### 3.1 Run Folder Cleanup Hook
**Trigger:** Daily + when disk space < 20%
**Purpose:** Prevent storage exhaustion from old run folders

**What it does:**
```yaml
cleanup_policy:
  automatic:
    - Compress runs older than 30 days (gzip)
    - Archive compressed runs to runs/archive/ after 60 days
    - Delete archived runs from active after 90 days
    - Always preserve last 20 runs regardless of age

  protected_runs:
    - Never delete runs marked with .protect file
    - Never delete runs with "critical" or "audit" tags
    - Never delete if referenced by active task

  cleanup_actions:
    - Remove .hook_initialized files older than 7 days
    - Remove empty run folders
    - Remove orphaned metadata files
```

**Dry-run mode:** Show what would be deleted without deleting
**Safety:** Move to trash/ first, permanent delete after 7 days

**Prevents:** Storage exhaustion, losing important historical data.

---

### 3.2 Log Rotation Hook
**Trigger:** Daily
**Purpose:** Prevent log file bloat

**What it does:**
```yaml
log_rotation:
  files_to_rotate:
    - .autonomous/logs/*.log
    - .autonomous/communications/events.yaml
    - operations/logs/*.log

  rotation_policy:
    - Rotate when > 10MB
    - Keep 5 rotated versions
    - Compress rotated files
    - Archive to logs/archive/ after 30 days

  cleanup:
    - Delete archived logs older than 90 days
    - Summarize old events before deletion
```

**Prevents:** Log files consuming all disk space, unreadable massive logs.

---

### 3.3 Orphaned Task Cleanup Hook
**Trigger:** Daily + on session start
**Purpose:** Detect and recover stuck/orphaned tasks

**What it does:**
```yaml
orphan_detection:
  criteria:
    - Task status = in_progress
    - No active run folder for task
    - Last updated > 4 hours ago
    - No recent activity in timeline.yaml

  recovery_actions:
    - Mark as "pending" (not completed - work may be lost)
    - Add note to task file about reset
    - Log incident to events.yaml
    - Alert user of recovered task

  investigation:
    - Check if run folder exists elsewhere
    - Check git history for related commits
    - Look for partial work that can be recovered
```

**Prevents:** Tasks stuck in limbo, lost work, inaccurate queue state.

---

### 3.4 Backup & Snapshot Hook
**Trigger:** Hourly during active work + on significant changes
**Purpose:** Enable recovery from corruption or mistakes

**What it backs up:**
```yaml
backup_policy:
  critical_files:
    - queue.yaml (before every modification)
    - skill-registry.yaml (before every modification)
    - timeline.yaml (before every modification)
    - operations/*.yaml (daily)

  snapshot_schedule:
    - Hourly: Critical files only
    - Daily: Full operations/ directory
    - Weekly: Full .autonomous/ directory (minus runs/)

  retention:
    - Hourly: 24 versions
    - Daily: 7 versions
    - Weekly: 4 versions

  storage:
    - Local: .autonomous/backups/
    - Git: Automatic commits of critical files
```

**Prevents:** Data loss from corruption, enables rollback of bad changes.

---

## 4. Degradation Prevention Hooks

### 4.1 Queue Integrity Validator
**Trigger:** Before/after queue.yaml modifications
**Purpose:** Maintain referential integrity in task queue

**What it validates:**
```yaml
queue_validation:
  structural:
    - Valid YAML
    - Required sections present
    - Task IDs are unique
    - No duplicate entries

  referential:
    - All blockedBy tasks exist
    - All blocks tasks exist
    - No circular dependencies
    - Goal references exist in goals/

  consistency:
    - Status counts match metadata
    - Priority scores calculated correctly
    - Resource types are valid
    - Parallel groups are valid

  performance:
    - File size < 1MB (warn if larger)
    - Load time < 1 second
    - Query performance acceptable
```

**On validation failure:**
- Block the modification
- Report specific errors
- Suggest fixes
- Maintain previous valid state

**Prevents:** Queue corruption, broken dependencies, inconsistent state.

---

### 4.2 Skill Registry Consistency Hook
**Trigger:** After skill-registry.yaml modifications
**Purpose:** Ensure skill data integrity

**What it validates:**
```yaml
skill_registry_validation:
  structure:
    - Valid YAML
    - Required sections (skills, metrics, outcomes)
    - All skills have required fields

  consistency:
    - No duplicate skill names
    - All category values valid
    - Effectiveness scores in range 0-100
    - Dates are valid ISO format

  referential:
    - task_outcomes reference valid task IDs
    - Skills referenced in task_outcomes exist
    - No orphaned outcome entries

  metrics:
    - Calculated effectiveness matches stored value
    - ROI calculations are valid
    - Success rates calculable from outcomes
```

**Prevents:** Skill data corruption, broken metrics, inconsistent registry.

---

### 4.3 Timeline Consistency Hook
**Trigger:** Before timeline.yaml append operations
**Purpose:** Maintain chronological integrity

**What it validates:**
```yaml
timeline_validation:
  chronological:
    - New events have timestamp >= last event
    - No future dates (allow small tolerance)
    - Dates are valid

  structural:
    - Valid YAML
    - Required event fields present
    - Event types are valid

  referential:
    - related_items reference valid goals/tasks
    - No orphaned references
```

**Prevents:** Timeline corruption, incorrect event ordering.

---

### 4.4 State Synchronization Hook
**Trigger:** After task completion, hourly
**Purpose:** Ensure all state files are synchronized

**What it syncs:**
```yaml
state_sync:
  task_completion_sync:
    - Update queue.yaml status
    - Update timeline.yaml with completion event
    - Update STATE.yaml if exists
    - Update goal progress if applicable

  consistency_checks:
    - Task status matches across all files
    - Completion counts match
    - In-progress tasks have active runs

  drift_detection:
    - Compare queue.yaml vs timeline.yaml counts
    - Compare skill-registry.yaml vs actual outcomes
    - Compare metrics files vs actual data
```

**On drift detected:**
- Identify source of truth
- Generate reconciliation report
- Apply fixes with user confirmation
- Log all changes

**Prevents:** State drift between files, inconsistent views of system.

---

## 5. Failure Recovery Hooks

### 5.1 Task Failure Handler
**Trigger:** When task fails or exits with PARTIAL/BLOCKED
**Purpose:** Proper handling of failed work

**What it does:**
```yaml
failure_handling:
  on_failure:
    - Update task status to "failed" (not left in_progress)
    - Create failure record in events.yaml
    - Preserve run folder for analysis
    - Capture error context

  analysis:
    - Categorize failure type (code, config, external, etc.)
    - Check for known failure patterns
    - Suggest remediation steps

  recovery:
    - Create follow-up task if auto-recoverable
    - Escalate to user if manual intervention needed
    - Update blocked tasks if this was a dependency

  notification:
    - Log to events.yaml
    - Update executor-dashboard.yaml failure metrics
    - Alert if critical priority task failed
```

**Prevents:** Failed tasks left in limbo, lost failure context, blocked dependents.

---

### 5.2 Corruption Recovery Hook
**Trigger:** On file corruption detection
**Purpose:** Automated recovery from corruption

**What it does:**
```yaml
corruption_recovery:
  detection:
    - YAML parse errors
    - Schema validation failures
    - Missing required fields
    - Invalid data types

  recovery_steps:
    1. Stop all writes to corrupted file
    2. Load most recent backup
    3. Validate backup integrity
    4. Apply changes since backup (if recoverable)
    5. Write to new file
    6. Atomically replace corrupted file
    7. Verify new file

  fallback:
    - If no valid backup, reconstruct from other sources
    - Use git history if available
    - Manual recovery mode if automatic fails
```

**Prevents:** Extended downtime from corruption, data loss.

---

## 6. Hook Implementation Priority

### Phase 1: Critical (Implement First)
1. **Session Start Health Check** - Prevents working with corrupted state
2. **File Corruption Detection** - Prevents data loss
3. **Task State Change Monitor** - Prevents orphaned tasks
4. **Backup & Snapshot** - Enables recovery

### Phase 2: High Priority
5. **Pre-Execution Validation** - Prevents duplicate/incorrect work
6. **Queue Integrity Validator** - Maintains task system health
7. **Orphaned Task Cleanup** - Recovers stuck tasks
8. **Run Folder Cleanup** - Prevents storage exhaustion

### Phase 3: Medium Priority
9. **System Health Dashboard** - Visibility into system state
10. **Metrics Freshness Monitor** - Ensures data quality
11. **State Synchronization** - Prevents drift
12. **Log Rotation** - Prevents log bloat

### Phase 4: Nice to Have
13. **Token Usage Monitor** - Budget protection
14. **Skill Registry Consistency** - Data quality
15. **Timeline Consistency** - Event integrity
16. **Failure Recovery** - Automated remediation

---

## 7. Hook Implementation Pattern

Each hook should follow this pattern:

```bash
#!/bin/bash
# hook-name.sh

# 1. Configuration
HOOK_NAME="hook-name"
LOG_FILE=".autonomous/logs/${HOOK_NAME}.log"
ALERT_FILE=".autonomous/communications/events.yaml"

# 2. Pre-checks
if [[ -f ".autonomous/hooks/disabled/${HOOK_NAME}" ]]; then
    echo "Hook disabled, skipping"
    exit 0
fi

# 3. Main logic
run_hook() {
    # Implementation here
    # Return 0 for success, 1 for warning, 2 for error
}

# 4. Logging
log_result() {
    local level=$1
    local message=$2
    echo "$(date -Iseconds) [${level}] ${HOOK_NAME}: ${message}" >> "$LOG_FILE"
}

# 5. Alerting
send_alert() {
    local level=$1
    local message=$2
    # Append to events.yaml
}

# 6. Execution
result=$(run_hook)
exit_code=$?

if [[ $exit_code -eq 0 ]]; then
    log_result "INFO" "Hook passed"
elif [[ $exit_code -eq 1 ]]; then
    log_result "WARN" "Hook warning: $result"
    send_alert "warning" "$result"
else
    log_result "ERROR" "Hook failed: $result"
    send_alert "error" "$result"
    exit 1
fi
```

---

## 8. Operational Dashboard

A centralized dashboard should display:

```yaml
dashboard_sections:
  system_health:
    - Last health check result
    - Critical file integrity status
    - Disk space available
    - Queue integrity status

  task_health:
    - Tasks in_progress (with age)
    - Stuck tasks (> 4 hours)
    - Orphaned tasks detected
    - Failed tasks (last 24 hours)

  metrics_health:
    - Last metrics update
    - Stale metrics count
    - Data quality issues

  maintenance_status:
    - Last backup timestamp
    - Last cleanup timestamp
    - Storage usage
    - Log file sizes

  alerts:
    - Active alerts (last 24 hours)
    - Alert history
    - Resolution status
```

---

## 9. Summary: What Prevents System Degradation

| Risk | Prevention Hook | Frequency |
|------|----------------|-----------|
| Data corruption | File Corruption Detection | Every write |
| Orphaned tasks | Task State Monitor + Orphan Cleanup | Continuous + Daily |
| Storage exhaustion | Run Folder Cleanup + Log Rotation | Daily |
| State drift | State Synchronization | Hourly + On change |
| Stale metrics | Metrics Freshness Monitor | Hourly |
| Queue corruption | Queue Integrity Validator | Every modification |
| Data loss | Backup & Snapshot | Hourly |
| Silent failures | Health Check + Alerting | Every session + Continuous |
| Budget overrun | Token Usage Monitor | Every 15 min |
| Failed task limbo | Task Failure Handler | On failure |

---

## 10. Recommendations

### Immediate Actions (This Week)
1. Implement **Session Start Health Check** - Critical for data integrity
2. Implement **File Corruption Detection** for queue.yaml and skill-registry.yaml
3. Set up **Backup & Snapshot** for critical files
4. Create **Task State Monitor** to detect orphaned tasks

### Short Term (Next 2 Weeks)
5. Implement **Queue Integrity Validator**
6. Implement **Orphaned Task Cleanup**
7. Set up **Run Folder Cleanup** with conservative retention
8. Create **System Health Dashboard**

### Medium Term (Next Month)
9. Implement **State Synchronization**
10. Set up **Metrics Freshness Monitor**
11. Implement **Log Rotation**
12. Add **Token Usage Monitor** if budget concerns exist

### Long Term (Ongoing)
13. Refine thresholds based on operational data
14. Automate more recovery procedures
15. Build operational runbooks
16. Implement predictive alerting

---

## Appendix: Files Referenced

- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` - Task queue
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/timeline.yaml` - Event timeline
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-metrics.yaml` - Skill effectiveness data
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/improvement-metrics.yaml` - Improvement pipeline
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/quality-gates.yaml` - Quality checklists
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/executor-dashboard.yaml` - Run metrics
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/run-validation.yaml` - Validation config
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/workflows/task-completion.yaml` - Completion workflow
