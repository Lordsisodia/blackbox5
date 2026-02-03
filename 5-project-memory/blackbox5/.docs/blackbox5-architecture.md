# Blackbox5 Infrastructure Architecture

**Purpose**: How to USE Blackbox5 (not just monitor it)
**Date**: 2026-02-04
**For**: Moltbot Integration

---

## Overview

Blackbox5 is a **dual-agent autonomous system** with:
- **Planner Agent**: Creates tasks, maintains queue, handles strategy
- **Executor Agent**: Executes tasks, reports progress, asks questions
- **Hook System**: Manages run lifecycle
- **Communication Protocol**: File-based message passing
- **236 Run History**: Complete execution archive

---

## 1. RALF System (How to Use)

### What RALF Is
RALF = Recursive Autonomous Learning Framework. A self-running loop where Planner creates work and Executor does work.

### How to Trigger RALF

**Start a RALF Session**:
```bash
cd ~/.blackbox5
claude --mcp-config .mcp-moltbot.json
```

**Manual Task Injection**:
```bash
# Create a task file
cat > ~/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-NEW.md << 'EOF'
# TASK-NEW: Task Title

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-04T12:00:00Z

## Objective
Clear description of what to do.

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Context
Background info.

## Approach
1. Step 1
2. Step 2
EOF

# Add to queue
~/.blackbox5/bin/ralf-planner-queue.sh --fill
```

### How to Check RALF Status

```bash
# Check queue depth
cat ~/.blackbox5/.autonomous/communications/queue.yaml

# Check agent health
cat ~/.blackbox5/.autonomous/communications/heartbeat.yaml

# Check recent events
cat ~/.blackbox5/.autonomous/communications/events.yaml

# Get formatted status
~/.blackbox5/bin/ralf-task-select.sh --status
```

---

## 2. Communication Protocol (File-Based Messaging)

### File Locations
All communication files are in:
```
~/.blackbox5/.autonomous/communications/
├── queue.yaml      # Planner writes, Executor reads
├── events.yaml     # Executor writes, Planner reads
├── heartbeat.yaml  # Both write their own status
└── chat-log.yaml   # Both can write messages
```

### How to Read Queue
```bash
# See pending tasks
grep -A 5 "status: pending" ~/.blackbox5/.autonomous/communications/queue.yaml

# Count pending tasks
grep -c "status: pending" ~/.blackbox5/.autonomous/communications/queue.yaml
```

### How to Read Events
```bash
# See last 10 events
tail -50 ~/.blackbox5/.autonomous/communications/events.yaml

# See executor events only
grep "agent: executor" ~/.blackbox5/.autonomous/communications/events.yaml

# See completed tasks
grep "type: completed" ~/.blackbox5/.autonomous/communications/events.yaml
```

### How to Read Heartbeats
```bash
# Check if agents are alive
python3 -c "
import yaml
from datetime import datetime, timedelta

with open('~/.blackbox5/.autonomous/communications/heartbeat.yaml') as f:
    data = yaml.safe_load(f)

for agent, status in data['heartbeats'].items():
    last_seen = datetime.fromisoformat(status['last_seen'])
    stale = datetime.now() - last_seen > timedelta(minutes=10)
    print(f'{agent}: {status[\"status\"]} (stale: {stale})')
"
```

---

## 3. Hook System (Lifecycle Management)

### How Hooks Work

**SessionStart Hook** (`bin/ralf-session-start-hook.sh`):
- Triggers when Claude Code starts
- Creates run folder with templates
- Sets env vars: RALF_RUN_DIR, RALF_RUN_ID, RALF_PROJECT_ROOT

**Stop Hook** (`bin/ralf-stop-hook.sh`):
- Triggers when session ends
- Validates completion
- Updates metadata
- Commits to git
- Archives run folder

**PostToolUse Hook** (`bin/ralf-post-tool-hook.sh`):
- Runs after every tool use
- Detects file changes via git diff
- Logs to events.yaml automatically

### How to Trigger Hooks Manually

```bash
# Simulate session start
export RALF_PROJECT_ROOT=~/.blackbox5
bash ~/.blackbox5/bin/ralf-session-start-hook.sh

# Simulate session stop
bash ~/.blackbox5/bin/ralf-stop-hook.sh
```

### How to Check Hook Status

```bash
# Check if hooks are configured
cat ~/.blackbox5/.claude/settings.json

# Check recent hook executions
ls -la ~/.blackbox5/5-project-memory/blackbox5/runs/unknown/ | head -10
```

---

## 4. Task Management (How to Create/Claim/Complete)

### How Tasks Flow

1. **Planner creates task** → Writes to `tasks/active/TASK-XXX.md`
2. **Planner adds to queue** → Appends to `queue.yaml`
3. **Executor claims task** → Updates status to "in_progress"
4. **Executor works** → Updates `events.yaml` with progress
5. **Executor completes** → Updates status to "completed"
6. **Stop hook archives** → Moves to `tasks/completed/`

### How to Create a Task

```bash
TASK_ID="TASK-$(date +%s)"
cat > ~/.blackbox5/5-project-memory/blackbox5/tasks/active/${TASK_ID}.md << EOF
# ${TASK_ID}: Brief Description

**Status:** pending
**Priority:** HIGH
**Created:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Feature:** F-XXX

## Objective
What needs to be done.

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Context
Background information.

## Approach
1. First step
2. Second step

## Rollback Strategy
How to undo if needed.
EOF
```

### How to Check Task Status

```bash
# List all active tasks
ls ~/.blackbox5/5-project-memory/blackbox5/tasks/active/

# Check specific task
cat ~/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-XXX.md | grep "Status:"

# List completed tasks
ls ~/.blackbox5/5-project-memory/blackbox5/tasks/completed/ | wc -l
```

### How to Claim a Task (Executor)

```bash
~/.blackbox5/bin/ralf-task-select.sh --claim
```

This will:
1. Find highest priority pending task
2. Update status to "in_progress"
3. Write claim event to events.yaml
4. Return task ID

---

## 5. Run System (How to Track Work)

### Run Folder Structure

Each run creates:
```
runs/{agent}/run-YYYYMMDD-HHMMSS/
├── metadata.yaml          # Machine-readable data
├── THOUGHTS.md           # Agent reasoning
├── DECISIONS.md          # Decisions made
├── RESULTS.md            # Outcomes
└── .ralf-metadata        # Hook metadata
```

### How to Find Runs

```bash
# Count total runs
find ~/.blackbox5/5-project-memory/blackbox5 -type d -name "run-*" | wc -l

# Find planner runs
ls ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/planner/runs/ | wc -l

# Find executor runs
ls ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/executor/runs/ | wc -l

# Find recent runs
ls -lt ~/.blackbox5/5-project-memory/blackbox5/runs/unknown/completed/ | head -10
```

### How to Read Run Results

```bash
# Get run summary
RUN_DIR=~/.blackbox5/5-project-memory/blackbox5/runs/unknown/completed/run-XXX
cat $RUN_DIR/RESULTS.md

# Get decisions
cat $RUN_DIR/DECISIONS.md

# Get metadata (YAML)
cat $RUN_DIR/metadata.yaml
```

### How to Query Across Runs

```bash
# Find high-LPM executor runs
for dir in ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/executor/runs/run-*/; do
  lpm=$(grep "lpm:" "$dir/metadata.yaml" 2>/dev/null | awk '{print $2}')
  [[ -n "$lpm" ]] && echo "$lpm LPM: $(basename $dir)"
done | sort -rn | head -10

# Find longest runs
for dir in ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/planner/runs/run-*/; do
  duration=$(grep "duration_seconds:" "$dir/metadata.yaml" 2>/dev/null | awk '{print $2}')
  [[ -n "$duration" ]] && echo "$duration sec: $(basename $dir)"
done | sort -rn | head -10
```

---

## 6. Skill System (How to Invoke)

### How Skills Work

**Agent Skills** (Markdown-based):
- Location: `~/.claude/skills/`
- Format: SKILL.md with YAML frontmatter
- Invocation: `skill: "skill-name"`

**Engine Skills** (Python-based):
- Location: `~/.blackbox5/2-engine/core/skills/`
- Used by RALF agents internally

### How to List Available Skills

```bash
# List agent skills
ls ~/.claude/skills/

# Read a skill
cat ~/.claude/skills/bmad-dev/SKILL.md
```

### How to Invoke a Skill

From within Claude Code:
```
skill: "bmad-dev"
```

Or with arguments:
```
skill: "git-commit", args: "-m 'message'"
```

---

## 7. MCP Integration (How Moltbot Connects)

### MCP Servers

**ralf-vps** (stdio over SSH):
```json
{
  "mcpServers": {
    "ralf-vps": {
      "command": "ssh",
      "args": ["-i", "~/.ssh/ralf", "ralf@77.42.66.40", "python3", "/opt/ralf/mcp-server.py"]
    }
  }
}
```

**moltbot-vps** (stdio via Python):
```json
{
  "mcpServers": {
    "moltbot-vps": {
      "command": "python3",
      "args": ["~/.blackbox5/mcp-server-moltbot.py"]
    }
  }
}
```

### How to Use MCP Tools

```python
# Get RALF status
moltbot_get_ralf_status()

# Send Telegram message
moltbot_send_message(message="Task completed!")

# Run command on VPS
moltbot_run_command(command="ls -la /opt/moltbot/")

# Get user context
moltbot_get_user_context()
```

---

## 8. Moltbot Integration Points

### What Moltbot Should Monitor

1. **Queue Health**:
   ```bash
   # Check if queue needs refill
   ~/.blackbox5/bin/ralf-planner-queue.sh --check
   ```

2. **Agent Health**:
   ```bash
   # Check heartbeats
   cat ~/.blackbox5/.autonomous/communications/heartbeat.yaml
   ```

3. **Task Completion**:
   ```bash
   # Check recent events
   tail -20 ~/.blackbox5/.autonomous/communications/events.yaml
   ```

### What Moltbot Should Do

1. **Send Notifications**:
   - When queue is empty
   - When agent is blocked
   - When task completes
   - When errors occur

2. **Trigger Actions**:
   - Refill queue when low
   - Restart stale agents
   - Archive old runs

3. **Report Status**:
   - Queue depth
   - Agent status
   - Recent completions
   - Error count

### How Moltbot Should Use Blackbox5

**Option 1: Monitor Only** (Current)
- Read communication files
- Send notifications
- Report status

**Option 2: Task Injector** (Recommended)
- Create tasks in `tasks/active/`
- Trigger queue refill
- Monitor execution

**Option 3: Full Integration** (Advanced)
- Run as an agent in the system
- Write to heartbeat.yaml
- Consume from queue.yaml
- Report via events.yaml

---

## 9. Quick Reference Commands

```bash
# RALF Status
~/.blackbox5/bin/ralf-task-select.sh --status

# Queue Status
~/.blackbox5/bin/ralf-planner-queue.sh --pending

# Agent Health
cat ~/.blackbox5/.autonomous/communications/heartbeat.yaml

# Recent Events
tail -30 ~/.blackbox5/.autonomous/communications/events.yaml

# Run Count
find ~/.blackbox5/5-project-memory/blackbox5 -type d -name "run-*" | wc -l

# Task Count
ls ~/.blackbox5/5-project-memory/blackbox5/tasks/active/ | wc -l

# Completed Tasks
ls ~/.blackbox5/5-project-memory/blackbox5/tasks/completed/ | wc -l
```

---

## 10. File Locations Summary

| Component | Location |
|-----------|----------|
| Queue | `~/.blackbox5/.autonomous/communications/queue.yaml` |
| Events | `~/.blackbox5/.autonomous/communications/events.yaml` |
| Heartbeat | `~/.blackbox5/.autonomous/communications/heartbeat.yaml` |
| Active Tasks | `~/.blackbox5/5-project-memory/blackbox5/tasks/active/` |
| Completed Tasks | `~/.blackbox5/5-project-memory/blackbox5/tasks/completed/` |
| Planner Runs | `~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/planner/runs/` |
| Executor Runs | `~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/executor/runs/` |
| Session Runs | `~/.blackbox5/5-project-memory/blackbox5/runs/unknown/completed/` |
| Hooks | `~/.blackbox5/bin/ralf-*-hook.sh` |
| Skills | `~/.claude/skills/` |
| MCP Config | `~/.blackbox5/.mcp-moltbot.json` |

---

*This document explains how to USE Blackbox5 infrastructure, not just observe it.*
