# SUBTASK-004B: Build bb5-health Command

**Parent Task:** TASK-AUTONOMY-004
**Depends On:** SUBTASK-004A (Core Library)
**Status:** pending
**Priority:** CRITICAL
**Estimated Tokens:** 35K

---

## Objective

Create the `bb5-health` CLI command for quick system health snapshots. Supports multiple output formats for human and machine consumption.

---

## Success Criteria

- [ ] `bb5-health` shows table output by default
- [ ] `bb5-health --format json` outputs valid JSON
- [ ] `bb5-health --format csv` outputs valid CSV
- [ ] Component flags work (--queue, --agents, --system)
- [ ] Exit codes: 0=healthy, 1=unhealthy, 2=critical
- [ ] Integrates with existing `bb5` CLI

---

## Implementation Plan

### Step 1: Command Structure (5K tokens)
Create `~/.blackbox5/bin/bb5-health`:

```python
#!/usr/bin/env python3
"""BB5 Health - System health snapshot tool"""
import click
from health_monitor import collect_all, calculate_health_score

@click.command()
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'csv']), default='table')
@click.option('--component', '-c', type=click.Choice(['all', 'queue', 'agents', 'system', 'skills']), default='all')
@click.option('--threshold', '-t', type=int, default=60, help='Health score threshold for exit code')
@click.option('--no-color', is_flag=True, help='Disable colored output')
def main(format, component, threshold, no_color):
    """Show BB5 system health snapshot"""
    pass
```

### Step 2: Table Output (10K tokens)
Create rich table output:

```
╔═══════════════════════════════════════════════════════════════╗
║  BB5 HEALTH SNAPSHOT              2026-02-06 14:32:15 UTC     ║
╚═══════════════════════════════════════════════════════════════╝

OVERALL: 68/100 [WARNING]

┌─ QUEUE ─────────────────────────────────────────────────────┐
│ Pending:      60  ████████████████████████████████░░░░░░░░  │
│ In Progress:   5  ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│ Completed:    25  ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│ Total:        90                                            │
└─────────────────────────────────────────────────────────────┘

┌─ AGENTS ────────────────────────────────────────────────────┐
│ Planner    │ ⚠️  stale  │ 2d ago │ loop 30                  │
│ Executor   │ ⚠️  stale  │ 2d ago │ loop 65                  │
└─────────────────────────────────────────────────────────────┘

┌─ STUCK TASKS ───────────────────────────────────────────────┐
│ TASK-ARCH-015 │ in_progress │ 3d │ >2x estimate             │
│ TASK-SSOT-031 │ in_progress │ 2d │ >2x estimate             │
└─────────────────────────────────────────────────────────────┘
```

Use `rich` library for:
- Tables with borders
- Progress bars for queue visualization
- Color coding (green/yellow/red)
- Automatic terminal width detection

### Step 3: JSON Output (5K tokens)
Structured JSON for APIs:

```json
{
  "timestamp": "2026-02-06T14:32:15Z",
  "health_score": 68,
  "status": "warning",
  "components": {
    "queue": {
      "pending": 60,
      "in_progress": 5,
      "completed": 25,
      "total": 90,
      "status": "healthy"
    },
    "agents": {
      "total": 2,
      "online": 0,
      "stale": 2,
      "status": "critical",
      "agents": [
        {"name": "planner", "status": "stale", "last_seen": "2d ago"}
      ]
    }
  },
  "stuck_tasks": [
    {"id": "TASK-ARCH-015", "status": "in_progress", "stuck_for": "3d"}
  ]
}
```

### Step 4: CSV Output (3K tokens)
Flat CSV for spreadsheets:

```csv
component,metric,value,unit,status
total,health_score,68,percent,warning
queue,pending,60,tasks,healthy
queue,in_progress,5,tasks,healthy
agents,planner_status,stale,,critical
agents,executor_status,stale,,critical
```

### Step 5: Component Filtering (5K tokens)
Support `--component` flag:
- `all` - Everything (default)
- `queue` - Just queue stats
- `agents` - Just agent heartbeats
- `system` - System resources (if available)
- `skills` - Skill registry summary

### Step 6: Exit Codes & Thresholds (3K tokens)
- Exit 0: Health score >= threshold (default 60)
- Exit 1: Health score < threshold
- Exit 2: Critical component failure (all agents stale)

Enable use in scripts:
```bash
# Nagios-style check
bb5-health --threshold 70 || echo "ALERT: System unhealthy"

# CI/CD gate
if [ "$(bb5-health --format json | jq '.health_score')" -lt 60 ]; then
  exit 1
fi
```

### Step 7: Integration with bb5 CLI (4K tokens)
Add to existing `bb5` command:
- `bb5 health` → calls `bb5-health`
- `bb5 health --json` → passes through

---

## Files to Create

1. `~/.blackbox5/bin/bb5-health` (executable Python script)

---

## Usage Examples

```bash
# Quick health check
bb5-health

# JSON for monitoring script
bb5-health --format json

# Just queue status
bb5-health --component queue

# Check if healthy (exit code)
bb5-health --threshold 70
if [ $? -eq 0 ]; then
  echo "System healthy"
else
  echo "System unhealthy"
fi

# Export to file
bb5-health --format json > /var/www/health.json
```

---

## Testing

```bash
# Test each format
./bb5-health
./bb5-health --format json | jq .
./bb5-health --format csv

# Test components
./bb5-health --component queue
./bb5-health --component agents

# Test exit codes
./bb5-health --threshold 70; echo "Exit: $?"
```

---

## Definition of Done

- [ ] `bb5-health` executable works
- [ ] Table output looks good in terminal
- [ ] JSON output is valid and complete
- [ ] CSV output is valid
- [ ] Component filtering works
- [ ] Exit codes work correctly
- [ ] Integrated with `bb5` CLI
- [ ] Help text is clear
