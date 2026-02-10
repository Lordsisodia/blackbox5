# RALF CLI Documentation

Version: 1.0.0

## Overview

RALF CLI is a command-line interface for the RALF (Recursive Autonomous Learning Framework) autonomous system. It provides operators with intuitive commands to manage tasks, queues, agents, and system health without directly editing YAML files.

## Installation

The CLI is installed as `/usr/local/bin/ralf` and should be available from any directory.

### Dependencies

- Python 3.9+
- Click 8.1.6+
- PyYAML
- colorama

## Quick Start

```bash
# List all active tasks
ralf task list

# Show queue with priority scores
ralf queue show

# Check agent status
ralf agent status

# View system health
ralf system health

# Get help
ralf --help
ralf task --help
```

## Commands

### Task Management

#### `ralf task list`
Display current active tasks (pending and in_progress).

```bash
ralf task list
ralf task list --output json
```

**Output Fields:**
- Task ID
- Status (pending/in_progress)
- Priority (CRITICAL/HIGH/MEDIUM/LOW)
- Title

**Color Coding:**
- Green: In Progress
- Yellow: Pending
- Red: Error

---

#### `ralf task show <task-id>`
Display full details for a specific task.

```bash
ralf task show TASK-010-001
ralf task show TASK-010-001 --output json
```

**Output Fields:**
- Title
- Status
- Priority
- Type
- Estimated Effort
- Impact Score
- Blocked By
- Blocks

---

### Queue Management

#### `ralf queue show`
Display queue with priority scores.

```bash
ralf queue show
ralf queue show --all
ralf queue show --output json
```

**Output Fields:**
- Rank (sorted by priority_score)
- Task ID
- Status
- Priority
- Priority Score
- Title

**Options:**
- `--all`: Show all tasks including completed
- `--output json`: JSON format for automation

---

### Agent Status

#### `ralf agent status`
Show planner/executor health.

```bash
ralf agent status
ralf agent status --output json
```

**Output Fields:**
- Agent ID
- Status (online/stale/never seen)
- Last Seen timestamp
- Status Type (running/stopped/unknown)

**Status Meaning:**
- Online (green): Active within last 5 minutes
- Stale (yellow): Not seen in 5 minutes to 2 hours
- Stale (red): Not seen in over 2 hours
- Never seen (red): No heartbeat recorded

---

### System Health

#### `ralf system health`
Display overall system status.

```bash
ralf system health
ralf system health --output json
```

**Output Sections:**

**Tasks:**
- Total tasks in queue
- Pending count
- In Progress count
- Completed count

**Agents:**
- Total agents
- Online agents (active in last 5 minutes)
- Stale agents (inactive for >5 minutes)

**Health Score:**
- Weighted score: Agents 40%, Tasks 60%
- Range: 0-100
- Color coded:
  - Green: 80-100 (Healthy)
  - Yellow: 50-79 (Warning)
  - Red: 0-49 (Critical)

---

## Output Formats

### Table (Default)
Human-readable ASCII tables with color coding.

### JSON
Machine-readable JSON for automation and scripting.

```bash
ralf task list --output json | jq '.[] | select(.priority == "CRITICAL")'
```

---

## Color Scheme

| Severity | Color |
|----------|--------|
| Error | Red |
| Warning | Yellow |
| Success/Healthy | Green |
| Info | Cyan |

---

## Integration

### File Locations

The CLI automatically detects the BlackBox5 project location:

1. **Auto-detection:** Searches upward from current directory for `blackbox5` folder
2. **Fallback:** Uses `~/.blackbox5/5-project-memory/blackbox5`

### Data Files

The CLI reads from these files:

- **Queue:** `.autonomous/agents/communications/queue.yaml`
- **Heartbeat:** `.autonomous/agents/communications/heartbeat.yaml`
- **Events:** `.autonomous/agents/communications/events.yaml`

---

## Use Cases

### Operator Dashboard
```bash
watch -n 60 "ralf system health"
```

### Task Prioritization
```bash
ralf queue show | head -10
```

### Task Assignment
```bash
ralf task list
ralf task show TASK-XXX
# Read task details, then start working
```

### Health Monitoring
```bash
# Check agents
ralf agent status

# Check queue
ralf queue show

# Check overall
ralf system health
```

---

## Troubleshooting

### "Queue file not found"
**Problem:** CLI can't find queue.yaml
**Solution:**
1. Ensure you're in or under a `blackbox5` directory
2. Check that `.autonomous/agents/communications/queue.yaml` exists

### "No heartbeat data available"
**Problem:** heartbeat.yaml doesn't exist or is empty
**Solution:**
1. Start agents to generate heartbeats
2. Check `.autonomous/agents/communications/heartbeat.yaml` exists

### Colors not showing
**Problem:** Terminal doesn't support ANSI colors
**Solution:**
- Use `--output json` for machine-readable output
- Ensure you're using a color-capable terminal

---

## Roadmap

### Planned Features (P1 - Should Have)

- `ralf task claim <task-id>` - Claim a task manually
- `ralf task complete <task-id>` - Mark task complete
- `ralf config get <key>` - Retrieve configuration
- `ralf config set <key> <value>` - Update configuration
- Bash/zsh auto-completion

### Future Features (P2 - Nice to Have)

- `ralf agent start/stop/restart` - Agent lifecycle control
- `ralf logs tail` - Display recent logs
- `ralf metrics show` - Performance metrics
- Interactive mode with menu system

---

## Support

For issues or feature requests:
1. Check this documentation
2. Run with `--help` for command details
3. Check BlackBox5 project docs
4. Review task queue for related tasks

---

*Generated by TASK-1738375000 - Feature F-016 Implementation*
