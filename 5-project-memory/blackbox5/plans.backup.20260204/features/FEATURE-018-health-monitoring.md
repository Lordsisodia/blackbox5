# Feature F-018: Health Monitoring & Self-Healing System

**Status:** Planned
**Priority:** High
**Estimated Effort:** 200 minutes (human) / ~9 minutes (AI)
**Estimated Lines:** ~3,000 lines
**Type:** Operational Maturity / Reliability

---

## Executive Summary

Implement comprehensive health monitoring for all RALF components with automated self-healing capabilities. The system will detect agent failures, resource exhaustion, stuck tasks, and performance degradation, then automatically execute recovery procedures.

**User Value:** System automatically recovers from failures, reducing manual intervention and improving availability.

**MVP Scope:** Health checks for all components, alert rules, automated recovery actions, dashboard integration.

---

## User Stories

### As a RALF Operator...
1. I want to be alerted when agents fail so I can respond quickly
2. I want the system to automatically restart failed agents so I don't have to
3. I want to see system health at a glance so I can assess status quickly
4. I want to detect stuck tasks so I can unblock progress
5. I want to monitor resource usage so I can prevent exhaustion

### As a RALF System...
6. I want to detect when I'm unhealthy so I can initiate recovery
7. I want to automatically retry failed operations so I can be resilient
8. I want to escalate unresolvable issues to humans so I can get help

---

## Technical Approach

### Architecture

```
health-system/
├── lib/
│   ├── health_checker.py      # Core health check engine
│   ├── resource_monitor.py    # CPU, memory, disk monitoring
│   ├── alert_manager.py       # Alert routing and notification
│   ├── recovery_engine.py     # Automated recovery actions
│   ├── metric_collector.py    # Metrics aggregation
│   └── predictor.py           # Predictive failure analysis
├── config/
│   ├── health-config.yaml     # Health check thresholds
│   └── alert-rules.yaml       # Alert conditions and actions
└── checks/
    ├── agent_health.py        # Agent-specific checks
    ├── task_health.py         # Task health checks
    └── system_health.py       # System resource checks
```

### Health Check Types

**1. Agent Health Checks**
- **Heartbeat:** Agent responded within timeout (120s)
- **Loop Progress:** Agent making progress (loop count increasing)
- **Task Processing:** Executor completing tasks
- **Error Rate:** Recent errors below threshold

**2. Task Health Checks**
- **Stuck Detection:** Task not updated in > 30 minutes
- **Duration Check:** Task running longer than estimate
- **Dependency Check:** Task dependencies satisfied
- **Resource Check:** Task consuming excessive resources

**3. System Health Checks**
- **Disk Space:** > 20% free on all partitions
- **Memory:** > 10% free RAM
- **CPU:** Load average < CPU count * 2
- **Network:** Connectivity to external services

### Recovery Actions

**Level 1: Automatic Recovery (No Human)**
- Restart stuck agent (timeout, crash)
- Retry failed operations (3 attempts)
- Clear stale locks
- Rotate oversized logs

**Level 2: Semi-Automatic (Alert First)**
- Notify operator of resource exhaustion
- Suggest manual intervention for stuck tasks
- Request approval for destructive actions

**Level 3: Escalation (Human Required)**
- Persistent failures (3+ recovery attempts)
- Unknown failure modes
- Data integrity issues
- Security concerns

---

## Success Criteria

### Must-Have (P0)
- [ ] Health checks for planner and executor agents
- [ ] Health checks for system resources (CPU, memory, disk)
- [ ] Health checks for task progress (stuck detection)
- [ ] Automated agent restart on timeout/crash
- [ ] Alert notifications for health issues
- [ ] Integration with F-008 dashboard for health display

### Should-Have (P1)
- [ ] Predictive failure detection (trend analysis)
- [ ] Automated recovery for common failure modes
- [ ] Health history tracking (metrics over time)
- [ ] Configurable alert thresholds
- [ ] Multiple alert channels (dashboard, log, webhook)
- [ ] Health check API endpoints

### Nice-to-Have (P2)
- [ ] Machine learning for anomaly detection
- [ ] Self-optimization (tune parameters based on history)
- [ ] Distributed tracing for cross-agent issues
- [ ] Root cause analysis for failures
- [ ] Health simulation for testing recovery

---

## Integration Points

### Data Sources
- `heartbeat.yaml` - Agent health status
- `events.yaml` - Task events and errors
- Queue state - Task progress
- System metrics - CPU, memory, disk (psutil)

### Actions
- Agent restart (via process control)
- Task state modification (via queue operations)
- Alert notifications (via F-008 dashboard, F-012 webhooks)
- Recovery logging (via F-017 audit system)

---

## Alert Rules

### Critical Alerts (Immediate Action)
```
name: Agent Timeout
condition: heartbeat.last_seen > 120s
action: restart_agent
severity: critical

name: Disk Exhaustion
condition: disk.free_percent < 10%
action: alert_operator, rotate_logs
severity: critical

name: Task Stuck
condition: task.last_updated > 30min AND task.status == "in_progress"
action: notify_operator, mark_stuck
severity: critical
```

### Warning Alerts (Monitor Closely)
```
name: High Error Rate
condition: errors.last_5min > 5
action: notify_operator
severity: warning

name: Memory Pressure
condition: memory.free_percent < 20%
action: notify_operator
severity: warning

name: Queue Starvation
condition: queue.depth < 2
action: notify_planner
severity: warning
```

---

## File Structure

```
2-engine/.autonomous/
├── lib/
│   ├── health_checker.py      # 380 lines - Core health engine
│   ├── resource_monitor.py    # 320 lines - System monitoring
│   ├── alert_manager.py       # 340 lines - Alert routing
│   ├── recovery_engine.py     # 420 lines - Recovery actions
│   ├── metric_collector.py    # 280 lines - Metrics aggregation
│   └── predictor.py           # 360 lines - Predictive analysis
├── config/
│   ├── health-config.yaml     # 160 lines - Thresholds
│   └── alert-rules.yaml       # 200 lines - Alert definitions
├── checks/
│   ├── agent_health.py        # 240 lines - Agent checks
│   ├── task_health.py         # 220 lines - Task checks
│   └── system_health.py       # 260 lines - System checks
└── health/
    └── metrics.db             # SQLite metrics storage

operations/.docs/
└── health-monitoring-guide.md # 700 lines - User guide

plans/features/
└── FEATURE-018-health-monitoring.md # This file
```

**Total Estimated Lines:** ~3,180 lines

---

## Implementation Plan

### Phase 1: Core Health Checks (P0)
1. Implement health_checker.py framework
2. Create agent health checks (heartbeat, loop progress)
3. Create system health checks (CPU, memory, disk)
4. Implement task health checks (stuck detection)
5. Add health display to F-008 dashboard

### Phase 2: Alerting & Recovery (P1)
6. Implement alert_manager.py with routing
7. Create recovery_engine.py with automated actions
8. Implement agent restart recovery
9. Implement task stuck recovery
10. Add configurable alert rules

### Phase 3: Advanced Features (P2)
11. Implement metric_collector.py for history
12. Implement predictor.py for trend analysis
13. Add machine learning anomaly detection
14. Implement root cause analysis

---

## Health Dashboard Integration

The health monitoring system integrates with F-008 (Real-time Dashboard):

**New Dashboard Cards:**
- **Agent Health:** Planner/Executor status with last seen
- **System Resources:** CPU, memory, disk gauges
- **Active Alerts:** List of current alerts with severity
- **Health History:** Sparkline charts for key metrics

**New WebSocket Events:**
```json
{
  "type": "health_alert",
  "severity": "critical",
  "check": "agent_timeout",
  "message": "Executor agent timeout",
  "timestamp": "2026-02-01T15:30:00Z"
}
```

---

## Recovery Scenarios

### Scenario 1: Agent Timeout
```
Detection: heartbeat.last_seen > 120s
Diagnosis: Agent process crashed or hung
Recovery:
  1. Check if process exists (ps aux | grep agent)
  2. If exists: Send SIGTERM, wait 5s
  3. If still exists: Send SIGKILL
  4. Restart agent with same configuration
  5. Verify heartbeat resumes
  6. Log recovery to audit system
```

### Scenario 2: Task Stuck
```
Detection: task.last_updated > 30min AND task.status == "in_progress"
Diagnosis: Task executor hung or external blocker
Recovery:
  1. Check task run logs for errors
  2. Check for external dependencies (API, network)
  3. If external issue: Notify operator
  4. If internal issue: Restart task
  5. Update task state to "retrying"
  6. Log recovery to audit system
```

### Scenario 3: Disk Exhaustion
```
Detection: disk.free_percent < 10%
Diagnosis: Log files or data accumulated
Recovery:
  1. Identify largest directories (du -sh *)
  2. Rotate oversized logs
  3. Clear temporary files
  4. Notify operator of action taken
  5. Log recovery to audit system
```

---

## Testing Strategy

### Unit Tests
- Test each health check function
- Test alert rule evaluation
- Test recovery action execution

### Integration Tests
- Test with real agent failure (kill process)
- Test with stuck task (pause executor)
- Test with resource exhaustion (fill disk)

### Simulation Tests
- Test recovery scenarios in isolation
- Verify rollback mechanisms
- Test alert delivery

---

## Rollout Plan

### Phase 1 (Loop 33): Monitoring Mode
- Implement health checks
- Display health in dashboard
- Log health issues (no recovery)

### Phase 2 (Loop 34): Active Recovery
- Enable automated agent restart
- Enable task stuck recovery
- Test recovery procedures

### Phase 3 (Loop 35+): Full Automation
- Enable all recovery actions
- Implement predictive failure detection
- Add machine learning features

---

## Risk Assessment

**Risk 1: False Positives (Unnecessary Recoveries)**
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Configurable thresholds, retry logic, human approval for destructive actions

**Risk 2: Recovery Failures (Making Things Worse)**
- **Probability:** Low
- **Impact:** High
- **Mitigation:** Recovery testing, rollback plans, audit logging

**Risk 3: Resource Overhead**
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** Efficient monitoring, configurable check intervals

---

## Effort Estimation

**Component Breakdown:**
- Health checker: 380 lines (~7 min)
- Resource monitor: 320 lines (~6 min)
- Alert manager: 340 lines (~6 min)
- Recovery engine: 420 lines (~8 min)
- Metric collector: 280 lines (~5 min)
- Predictor: 360 lines (~7 min)
- Config files: 360 lines (~6 min)
- Health checks: 720 lines (~10 min)
- Documentation: 700 lines (~13 min)
- Feature spec: 300 lines (~6 min)

**Total:** ~4,180 lines → ~12 minutes at 337 LPM

**Buffer:** Add 20% for testing → ~15 minutes

---

## Success Metrics

- **Detection:** 100% of agent failures detected within 2 minutes
- **Recovery:** 90% of automatic recoveries successful
- **Availability:** > 99.9% uptime (excluding maintenance)
- **MTTR:** Mean time to recovery < 5 minutes for known issues
- **False Positives:** < 5% of alerts are false positives

---

**Feature Spec Complete** ✅
**Ready for Implementation:** Loop 33-35
