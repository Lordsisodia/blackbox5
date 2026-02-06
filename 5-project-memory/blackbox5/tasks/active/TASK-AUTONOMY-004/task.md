# TASK-AUTONOMY-004: Build BB5 Health Dashboard System

**Goal:** IG-AUTONOMY-001 - Close the Feedback Loops
**Plan:** PLAN-AUTONOMY-001 - Phase 4: System Health Dashboard
**Status:** in_progress
**Priority:** CRITICAL
**Created:** 2026-02-06
**Started:** 2026-02-06

---

## Objective

Build a comprehensive health dashboard system for BlackBox5 that provides real-time visibility into system status, agent health, task progress, and alerts for issues. Designed for VPS deployment with 24/7 monitoring capabilities.

---

## Success Criteria

- [ ] `bb5-health` command provides accurate system snapshot in table/json/csv formats
- [ ] `bb5-watch` daemon runs continuously on VPS with Telegram alerts
- [ ] `bb5-dashboard` provides live terminal UI with refresh capability
- [ ] Stuck task detection working (>2x estimated time)
- [ ] Heartbeat monitoring with timeout alerts
- [ ] Queue depth tracking and backlog warnings
- [ ] Health score calculation from metrics-dashboard.yaml
- [ ] SQLite time-series storage for historical data
- [ ] Systemd service configuration for auto-start
- [ ] Documentation for VPS deployment

---

## Context

Current BB5 system has rich data but poor visibility:
- 90 tasks in queue (25 completed, 5 in_progress, 60 pending)
- Heartbeat last seen 2 days ago (stale)
- Health score 68/100 but not actively monitored
- No automated alerting when things break

This dashboard solves the "black box" problem - you'll know what's happening without manually checking files.

---

## Data Sources

| File | Purpose | Path |
|------|---------|------|
| queue.yaml | Task states, priorities, estimates | `5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` |
| heartbeat.yaml | Agent status, last seen | `5-project-memory/blackbox5/.autonomous/agents/communications/heartbeat.yaml` |
| events.yaml | Activity log | `5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml` |
| metrics-dashboard.yaml | Health scores, targets | `5-project-memory/blackbox5/.autonomous/agents/metrics/metrics-dashboard.yaml` |
| skill-registry.yaml | Skill effectiveness | `5-project-memory/blackbox5/operations/skill-registry.yaml` |
| runs/*/metrics.json | Individual run data | `5-project-memory/blackbox5/.autonomous/runs/*/metrics.json` |

---

## Architecture

```
bb5-health       CLI snapshot (table/json/csv)
bb5-dashboard    Terminal UI with live refresh
bb5-watch        Daemon with Telegram alerts
        |
        v
HealthMonitor Core (Python)
  - Data collectors (YAML/JSON readers)
  - SQLite storage (time-series)
  - Alert manager (Telegram/webhooks)
  - Health calculators
```

---

## Subtasks

### Phase 1: Foundation (SUBTASK-004A)
**SUBTASK-004A: Create Health Monitor Core Library**
- Build data collectors for all YAML/JSON sources
- Create health score calculator
- Build stuck task detector
- Create SQLite schema for metrics

### Phase 2: CLI Tools (SUBTASK-004B)
**SUBTASK-004B: Build bb5-health Command**
- Table output for terminal
- JSON output for APIs/automation
- CSV output for spreadsheets
- Component flags (--queue, --agents, --system)

### Phase 3: Daemon (SUBTASK-004C)
**SUBTASK-004C: Build bb5-watch Daemon**
- Continuous monitoring loop
- Telegram bot integration
- Configuration file support
- Alert routing (critical/warning/info)

### Phase 4: UI (SUBTASK-004D)
**SUBTASK-004D: Build bb5-dashboard TUI**
- Live terminal interface
- Sparklines for trends
- Color-coded health indicators
- Interactive controls

### Phase 5: Deployment (SUBTASK-004E)
**SUBTASK-004E: VPS Deployment Package**
- Systemd service file
- Logrotate configuration
- Environment setup script
- Deployment documentation

---

## Technical Stack

- **Language:** Python 3.9+
- **Database:** SQLite (WAL mode)
- **CLI Framework:** Click or argparse
- **TUI:** rich library (for dashboard)
- **Alerts:** python-telegram-bot
- **Deployment:** systemd

---

## File Locations

```
~/.blackbox5/
├── bin/
│   ├── bb5-health           # CLI snapshot
│   ├── bb5-dashboard        # TUI dashboard
│   ├── bb5-watch            # Daemon control
│   └── lib/
│       └── health_monitor/  # Python package
│           ├── __init__.py
│           ├── collectors.py
│           ├── calculators.py
│           ├── database.py
│           ├── alerts.py
│           └── daemon.py
├── config/
│   └── watch-config.yaml    # Daemon configuration
└── .autonomous/
    └── health/
        └── metrics.db       # SQLite database
```

---

## Rollback Strategy

- All changes are additive (new files only)
- Stop daemon: `bb5-watch stop`
- Remove: Delete bin files and config
- Database can be deleted without affecting core BB5

---

## Notes

- Start with SUBTASK-004A (core library)
- Each subtask should be testable independently
- Use existing `bb5-skill-dashboard` as reference for CLI patterns
- Keep resource usage low (<100MB RAM, minimal CPU)
