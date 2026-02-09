# MoltBot Autonomous Agent v2 - Specification

## Overview
An intelligent autonomous agent that runs continuously on the VPS, monitors BB5 activity, and sends detailed, metrics-rich reports via Telegram.

## Core Concept
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Telegram  │◄────│   MoltBot    │◄────│    BB5      │
│   (You)     │     │   Agent v2   │     │  Metrics    │
└─────────────┘     └──────────────┘     └─────────────┘
```

## What MoltBot Reports

### Real Metrics (Not Bullshit)

**Git Activity:**
- Number of commits
- Number of pushes to GitHub
- Authors who contributed
- Files changed
- Lines added/removed

**Task Tracking:**
- Tasks completed
- Tasks started
- Tasks in progress
- Tasks pending

**Agent Activity:**
- Which agents ran
- How many agent runs
- What tasks they worked on

**Token Usage:**
- Total tokens consumed
- Input/output breakdown

**Accomplishments:**
- Key achievements from completed runs
- What actually got done

## Report Types

### 1. Hourly Activity Report
```
📊 BB5 Activity Report
Last 1 hour(s)
━━━━━━━━━━━━━━━━━━━━━━━

🔄 Git Activity
• Commits: 5
• Pushed: 3
• Branches: 12
• Authors: Claude, vps-agent

✅ Tasks
• Completed: 2
• Started: 3
• In Progress: 1
• Pending: 4

🤖 Agents
• Active: 3
• Runs: 5
• Types: executor, planner, scout

📁 Work Output
• Files Changed: 23
• Insertions: +456
• Deletions: -123

🏆 Key Accomplishments
1. Implemented BB5 Core Skills System
2. Fixed autonomous improver branch issues
3. Created agent team coordinator

Reply 'details' for full breakdown
```

### 2. Daily Summary
```
📊 BB5 Daily Summary
2026-02-09
━━━━━━━━━━━━━━━━━━━━━━━

🎯 Key Metrics (24h)
• Commits: 12
• Tasks Completed: 5
• Agent Runs: 15
• Files Changed: 67
• Lines: +1,234/-456

🏆 Top Accomplishments
1. Implemented BB5 Core Skills System...
2. Fixed autonomous improver branch issues...
3. Created agent team coordinator...

📊 Current Status
• Active Tasks: 3
• Pending: 4
• In Progress: 1
```

### 3. Detailed Breakdown (on request)
```
📋 Detailed Activity Breakdown
Last 24 hour(s)

📝 Commits (12)
8b4a61e feat: Add BB5 Simple Autonomous Improver...
b207c5c fix: Update BB5 improver to use allowedTools...
ed582c2 feat: Add BB5 Autonomous Improver...
...

✅ Completed Tasks (5)
• TASK-001: Implement Core Skills System
• TASK-002: Fix branch naming issues
...

🤖 Agent Runs (15)
• executor: TASK-001
• planner: queue_refilled
• scout: codebase_analysis
...

📁 Files Changed (67)
• .claude/agents/bb5-team-coordinator.md
• agents/moltbot-autonomous/moltbot-agent.py
...
```

## Telegram Commands

| Command | Action |
|---------|--------|
| `status` | Current system status |
| `report` | Immediate hourly report |
| `report 6` | Report for last 6 hours |
| `daily` | Daily summary |
| `details` | Full detailed breakdown |
| `git` | Git stats only |
| `tasks` | Task list |
| `pause` | Stop reports |
| `resume` | Resume reports |

## How Metrics Are Collected

### Git Metrics
```python
# Uses git log with --shortstat
git log --since="24 hours ago" --pretty=format:%H|%s|%an|%ci --shortstat
```
- Parses commit SHAs, messages, authors, dates
- Extracts insertions/deletions from shortstat
- Counts branches
- Detects pushed commits via --decorate

### Task Metrics
```python
# Reads from filesystem
.autonomous/tasks/active/TASK-*.md
.autonomous/tasks/completed/TASK-*.md
```
- Parses task status from markdown files
- Extracts descriptions
- Tracks completion state

### Agent Metrics
```python
# Reads from events.yaml
.autonomous/agents/communications/events.yaml
```
- Parses agent_start, agent_complete events
- Tracks which agents ran
- Counts total runs

### Token Metrics
```python
# Reads from chat logs
.autonomous/memory/chat-logs/*.jsonl
```
- Extracts token usage from metadata
- Sums input/output tokens

### Accomplishments
```python
# Reads from RESULTS.md files
.autonomous/runs/run-*/RESULTS.md
```
- Finds completed runs
- Extracts key achievements
- Surfaces what actually got done

## Schedule

- **Hourly reports**: Every hour during business hours (9 AM - 9 PM)
- **Daily summary**: Every day at 9 AM
- **Command responses**: Immediate

## Deployment

```bash
# On VPS (77.42.66.40)
cd /opt/blackbox5/agents/moltbot-autonomous

# Install dependencies
pip3 install pyyaml schedule requests

# Copy the updated agent
cp moltbot-agent.py /opt/blackbox5/agents/moltbot-autonomous/

# Restart the service
sudo systemctl restart moltbot-autonomous

# Check status
sudo systemctl status moltbot-autonomous
sudo journalctl -u moltbot-autonomous -f
```

## Configuration

Edit `moltbot-agent.py` to configure:

```python
# Telegram settings (already set)
TELEGRAM_BOT_TOKEN = "8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo"
TELEGRAM_CHAT_ID = "7643203581"

# To use a specific topic (like your Blackbox topic):
self.topic_id = YOUR_TOPIC_ID  # Set this in __init__
```

## File Structure

```
moltbot-autonomous/
├── moltbot-agent.py          # Main agent (intelligent reporting)
├── MOLTBOT-SPEC.md           # This specification
├── moltbot-autonomous.service # systemd service file
└── state/                     # Runtime state
    └── agent_state.json
```

## Why This Is Better

**Before (v1):**
- Generic "analysis reports"
- Counted "issues" (who cares?)
- No real metrics
- Bullshit summaries

**Now (v2):**
- Real git metrics (commits, pushes, authors)
- Actual task tracking
- Token usage reporting
- File change statistics
- Meaningful accomplishments
- Detailed breakdowns on demand

## Testing

```bash
# Test Telegram connection
python3 -c "
import requests
requests.post(
    'https://api.telegram.org/bot8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo/sendMessage',
    json={'chat_id': '7643203581', 'text': '🤖 MoltBot v2 test'}
)
"

# Test metrics collection
python3 -c "
from pathlib import Path
import sys
sys.path.insert(0, '/opt/blackbox5/agents/moltbot-autonomous')

# Import and test
from moltbot_agent import BB5MetricsCollector
collector = BB5MetricsCollector(Path('/opt/blackbox5'))
print('Git:', collector.collect_git_metrics(24))
print('Tasks:', collector.collect_task_metrics())
print('Agents:', collector.collect_agent_metrics(24))
"
```
