# Moltbot File Reference

## Configuration Files

### MCP Configuration

**~/.blackbox5/.mcp-moltbot.json**
```json
{
  "mcpServers": {
    "ralf-vps": {
      "type": "stdio",
      "command": "ssh",
      "args": ["-i", "~/.ssh/ralf_hetzner", "root@77.42.66.40", "python3", "-c", "exec(open('/opt/ralf/mcp-server.py').read())"]
    },
    "moltbot-vps": {
      "type": "stdio",
      "command": "python3",
      "args": ["/Users/shaansisodia/.blackbox5/mcp-server-moltbot.py"]
    }
  }
}
```

### User Context

**~/.blackbox5/moltbot-user-context.json**
- User profile and preferences
- RALF integration file paths
- Telegram ID

### OpenClaw Config

**/opt/moltbot/openclaw.json** (on VPS)
```json
{
  "agent": {
    "model": "anthropic/claude-sonnet-4-5",
    "baseUrl": "https://api.z.ai/api/anthropic"
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_TELEGRAM_BOT_TOKEN"
    }
  },
  "skills": {
    "ralf-status": {
      "enabled": true,
      "path": "/opt/moltbot/skills/ralf-status.js"
    }
  },
  "gateway": {
    "port": 18789,
    "host": "0.0.0.0"
  }
}
```

## Code Files

### MCP Server

**~/.blackbox5/mcp-server-moltbot.py**
- Local MCP server implementation
- SSHs to VPS for command execution
- Handles 5 tool calls

### Skills

**~/.blackbox5/ralf-context-skill.js**
- User context loading skill
- Reads /opt/moltbot/user-context.json

**/opt/moltbot/skills/ralf-status.js** (on VPS)
- RALF status reporting skill
- Reads queue.yaml, events.yaml, verify.yaml
- Formats Telegram messages

### Scripts

**~/.blackbox5/bin/moltbot-mcp-connect.sh**
- Tests MCP connections
- Lists available tools

**~/.blackbox5/2-engine/.autonomous/vps-deployment/moltbot-setup.sh**
- VPS deployment script
- Installs OpenClaw
- Creates systemd service
- Sets up cron jobs

**~/.blackbox5/2-engine/.autonomous/vps-deployment/openclaw-telegram.json**
- Telegram-specific OpenClaw config template

## RALF Communication Files (on VPS)

**/opt/ralf/5-project-memory/blackbox5/.autonomous/agents/communications/**

### queue.yaml
Pending and in-progress tasks

```yaml
queue:
  - task_id: "TASK-001"
    status: "pending"
    priority: "high"
    owner: "planner"
    created: "2026-02-04T03:55:41Z"
```

### events.yaml
Completed task events

```yaml
events:
  - timestamp: "2026-02-04T03:55:41Z"
    task_id: "TASK-001"
    type: "completed"
    agent: "executor"
```

### verify.yaml
Verification decisions

```yaml
verifications:
  - task_id: "TASK-001"
    decision: "AUTO_COMMIT"
    confidence: 0.95
    timestamp: "2026-02-04T03:55:41Z"
```

## System Files (on VPS)

### Systemd Service

**/etc/systemd/system/moltbot.service**
```ini
[Unit]
Description=Moltbot (OpenClaw) AI Assistant
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/moltbot
ExecStart=/usr/bin/openclaw daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Cron Jobs

**RALF Watcher:**
```bash
*/2 * * * * /opt/moltbot/ralf-watcher.sh
```

## Documentation Files

**~/.blackbox5/docs/moltbot-ralf-architecture.md**
- Complete architecture diagram
- Communication patterns
- MCP setup instructions

**~/.blackbox5/1-docs/.docs/moltbot/** (this directory)
- README.md - Overview
- ARCHITECTURE.md - Deep dive
- RESEARCH-LOG.md - Research notes
- OPENCLAW-RESEARCH.md - OpenClaw framework
- MCP-PROTOCOL.md - MCP implementation
- TELEGRAM-BOT.md - Telegram integration
- FILE-REFERENCE.md - This file
