---
name: openclaw-cli-reference
description: Quick reference for OpenClaw CLI commands - sessions, agents, process control
category: documentation
version: 1.0
auto-invoke: false
confidence-threshold: 0.8
---

# OpenClaw CLI Quick Reference

## Session Management Commands

### List Sessions
```bash
# List all sessions
openclaw sessions list

# List only subagent sessions
openclaw sessions list --kinds subagent

# Get specific session info
openclaw session info <sessionKey>
```

### Kill Sessions
```bash
# Kill a specific session by session key
openclaw session kill <sessionKey>

# Kill all subagent sessions
openclaw session kill --kinds subagent
```

### Session Tools
```bash
# Send message to another session
openclaw sessions send <sessionKey> "Your message"

# Get session history
openclaw session history <sessionKey> --limit 50

# Spawn new session (creates subagent)
openclaw sessions spawn --task "Task description" --label "task-name"
```

## Process Management

### List Processes
```bash
# List all processes
openclaw process list

# Get process details
openclaw process info <processId>
```

### Kill Processes
```bash
# Kill a process by ID
openclaw process kill <processId>

# Kill all processes
openclaw process kill --all
```

## Common Session Keys

**Main Sessions:**
- `agent:main:main` - Main orchestrator
- `agent:content:main` - Content agent
- `agent:engineering:main` - Engineering agent
- `agent:general:main` - General assistant
- `agent:task-agent:main` - Task manager

**Sub-Agent Sessions:**
- `agent:main:subagent:<uuid>` - Sub-agent session

**Channel Sessions:**
- `agent:main:telegram:group:<id>:topic:<id>` - Telegram group with topic
- `agent:main:discord:guild:<id>:channel:<id>` - Discord server

**Key Patterns:**
- Sub-agent keys always contain `:subagent:` followed by a UUID
- Main sessions have simple format `agent:<agent-id>:main`
- Channel sessions include full path with group ID and topic ID
- Session keys match exactly what `sessions_list` returns

## Examples

### Example 1: Kill all sub-agent sessions
```bash
# Get all subagent sessions
openclaw sessions list --kinds subagent

# Kill each one
for sessionKey in $(openclaw sessions list --kinds subagent | grep -o "key=" | cut -d'"' -f1); do
    openclaw session kill "$sessionKey"
done
```

### Example 2: Spawn a sub-agent
```bash
# Create a sub-agent session
openclaw sessions spawn \
    --task "Analyze these YouTube transcripts" \
    --label "youtube-analysis" \
    --agent content
```

### Example 3: Send message to sub-agent
```bash
# Get the session key first
sessionKey=$(openclaw sessions list --kinds subagent | grep "youtube-scraper" | cut -d'"' -f1)

# Send message
openclaw sessions send "$sessionKey" "Here's your task data"
```

### Example 4: Monitor sub-agent status
```bash
# Check if session is active
openclaw session list --kinds subagent --messageLimit 0 | grep "youtube-scraper"

# View recent activity
openclaw session history <sessionKey> --limit 10
```

### Example 5: Kill zombie sessions
```bash
# Find sessions that haven't been updated in 1 hour
openclaw sessions list --activeMinutes 60 | \
    while read sessionKey; do
        # Check last update time
        openclaw session kill "$sessionKey"
    done
```

---

**Created:** 2026-02-10
**Usage:** Use this reference to quickly find OpenClaw commands for session and process management.
