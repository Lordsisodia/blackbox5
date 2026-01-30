# BLACKBOX5 24/7 Runtime - Quick Start Guide

**Goal:** Run BLACKBOX5 agents 24/7 utilizing 100-200M tokens/day for autonomous self-improvement.

## Overview

The runtime infrastructure provides:
- **Daemon**: Process management with health monitoring and auto-restart
- **Scheduler**: Periodic task execution with dependency resolution
- **Discovery**: Autonomous skill/framework discovery from GitHub
- **Monitor**: Token usage tracking and resource monitoring

## Installation

```bash
cd /Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5/runtime

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Option 1: Run Directly (For Testing)

```bash
python launcher.py
```

This will start the 24/7 runtime with:
- Health checks every 5 minutes
- BlackBox research every hour
- Skill discovery every 2 hours
- Self-improvement analysis every 6 hours
- Resource monitoring every minute

### Option 2: Run as Background Service

```bash
# Start in background
nohup python launcher.py > blackbox5_output.log 2>&1 &

# Check status
tail -f blackbox5_runtime.log

# Stop
kill $(cat .runtime/daemon.pid)
```

### Option 3: Systemd Service (Production)

```bash
# Install service
sudo cp blackbox5.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable blackbox5
sudo systemctl start blackbox5

# Check status
sudo systemctl status blackbox5
journalctl -u blackbox5 -f
```

## Configuration

Edit `launcher.py` to customize:

```python
config = DaemonConfig(
    target_tokens_per_day=150_000_000,  # Adjust target
    health_check_interval=30,             # Seconds between health checks
    max_concurrent_tasks=10,              # Max parallel tasks
    max_memory_mb=8192,                   # 8GB memory limit
    max_cpu_percent=80.0                  # 80% CPU limit
)
```

## Monitoring

### View Logs

```bash
# Runtime logs
tail -f blackbox5_runtime.log

# Resource metrics
tail -f .runtime/metrics.jsonl

# Daemon state
cat .runtime/daemon_state.json
```

### Status Dashboard

The runtime logs status reports every 5 minutes showing:

```
================================================================================
BLACKBOX5 Resource Monitor Status
================================================================================
Uptime: 2:15:30

Token Usage:
  Today: 12,450,000 / 150,000,000
  Progress: 8.3% (Hour: 10.4%)
  Last Hour: 6,250,000
  Est. Daily: 150,000,000
  On Track: ✓

Costs:
  Total: $45.23
  This Hour: $2.50

Tasks:
  Total: 45 | Completed: 42 | Failed: 3
  Success Rate: 93.3%
  Avg Duration: 245.3s

Resources:
  CPU: 45.2% | Memory: 2048MB
  Peak CPU: 78.5% | Peak Memory: 4096MB
================================================================================
```

## Autonomous Tasks

### Pre-configured Tasks

| Task | Frequency | Tokens | Description |
|------|-----------|--------|-------------|
| System Health Check | 5 min | 500 | Monitor system health |
| BlackBox Research | 1 hour | 50K | Analyze architecture |
| Skill Discovery | 2 hours | 100K | Find new skills |
| Self-Improvement | 6 hours | 100K | Performance analysis |

### Adding Custom Tasks

```python
from runtime.scheduler import TaskScheduler, TaskPriority

async def my_custom_task():
    # Your autonomous task logic
    return {"result": "success"}

# In setup_autonomous_tasks():
await scheduler.schedule_periodic_task(
    name="My Custom Task",
    description="Does something useful",
    task_type="custom",
    execute_func=my_custom_task,
    interval_seconds=3600,  # Every hour
    priority=TaskPriority.HIGH,
    estimated_tokens=10000
)
```

## Troubleshooting

### High Memory Usage

```python
# Reduce max concurrent tasks
config = DaemonConfig(max_concurrent_tasks=5)
```

### Below Token Target

The system automatically adds more tasks when below target. Check:

```bash
# Check hourly breakdown
cat .runtime/metrics.jsonl | jq '.hourly_breakdown'
```

### Tasks Failing

```bash
# Check error logs
grep "ERROR" blackbox5_runtime.log

# Check failed tasks
cat .runtime/daemon_state.json | jq '.tasks_failed'
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   BLACKBOX5 Runtime                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │    Daemon    │  │  Scheduler   │  │  Discovery  │ │
│  │              │  │              │  │             │ │
│  │ - Health     │  │ - Tasks      │  │ - GitHub    │ │
│  │ - Restart    │  │ - Priority   │  │ - Evaluate  │ │
│  │ - State      │  │ - Retry      │  │ - Integrate │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
│         │                  │                  │        │
│         └──────────────────┴──────────────────┘        │
│                            │                           │
│                   ┌────────▼────────┐                  │
│                   │     Monitor     │                  │
│                   │                  │                  │
│                   │ - Tokens        │                  │
│                   │ - Resources     │                  │
│                   │ - Costs         │                  │
│                   │ - Performance   │                  │
│                   └──────────────────┘                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Success Metrics

Target achievements:

- ✅ **24/7 Uptime**: Continuous operation
- ✅ **Token Utilization**: 100-200M tokens/day
- ✅ **Self-Improvement**: New skills integrated daily
- ✅ **Cost Efficiency**: Optimal token usage per improvement

## Next Steps

1. **Test locally**: Run `python launcher.py` and monitor for 1 hour
2. **Check integration**: Verify skills are being discovered and integrated
3. **Scale up**: Increase token targets as needed
4. **Add business tasks**: Integrate client work once tested

## Support

- Logs: `blackbox5_runtime.log`
- State: `.runtime/daemon_state.json`
- Metrics: `.runtime/metrics.jsonl`
- Issues: Check logs first, then report bugs
