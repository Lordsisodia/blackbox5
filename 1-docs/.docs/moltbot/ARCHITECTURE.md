# Moltbot Architecture Deep Dive

## System Components

### 1. OpenClaw Framework

OpenClaw is the underlying framework that powers Moltbot. It provides:

- **Gateway API:** HTTP/SSE endpoint for MCP connections
- **Channel Interface:** Telegram/Discord bot integration
- **Skill System:** Pluggable JavaScript modules for custom functionality
- **Agent Configuration:** Model selection and API endpoint configuration

**Key Files:**
- `/opt/moltbot/openclaw.json` - Main configuration
- `/opt/moltbot/skills/*.js` - Custom skills

### 2. MCP (Model Context Protocol) Server

The MCP server acts as a bridge between Claude Code and the VPS.

**Implementation:** `mcp-server-moltbot.py`

```python
# Key functions:
- run_vps_command()      # SSH to VPS and run commands
- get_gateway_status()   # Check if OpenClaw is running
- send_telegram_message() # Send messages via Telegram
- get_ralf_status()      # Read RALF queue files
- get_user_context()     # Load user profile
```

**MCP Protocol Methods:**
- `initialize` - Handshake and capability exchange
- `tools/list` - List available tools
- `tools/call` - Execute a tool with arguments

### 3. RALF Integration Skills

#### ralf-status.js

Reads RALF state files and formats reports:

```javascript
class RalfStatusSkill {
  async getQueueStatus()     // Parse queue.yaml
  async getRecentEvents()    // Parse events.yaml
  async getVerificationStatus() // Parse verify.yaml
  async getGitStatus()       // Run git commands
  async getSystemHealth()    // Get VPS stats
  formatStatusReport()       // Format for Telegram
}
```

**Telegram Commands:**
- `!ralf status` - Full status report
- `!ralf queue` - Queue summary
- `!ralf task TASK-XXX` - Task details
- `!ralf health` - System health

#### ralf-context.js

Loads and provides user context:

```javascript
class UserContextSkill {
  loadContext()          // Read user-context.json
  getUserName()          // Get preferred name
  getUserContext()       // Get full context object
}
```

### 4. Communication Patterns

#### File-Based Bridge (RALF ↔ Moltbot)

RALF writes task state to YAML files:

```yaml
# queue.yaml
queue:
  - task_id: "TASK-001"
    status: "pending"
    priority: "high"
    owner: "planner"
```

```yaml
# events.yaml
events:
  - timestamp: "2026-02-04T03:55:41Z"
    task_id: "TASK-001"
    type: "completed"
    agent: "executor"
```

```yaml
# verify.yaml
verifications:
  - task_id: "TASK-001"
    decision: "AUTO_COMMIT"
    confidence: 0.95
```

#### MCP Connection (MacBook ↔ VPS)

**ralf-vps (stdio over SSH):**
```json
{
  "type": "stdio",
  "command": "ssh",
  "args": [
    "-i", "~/.ssh/ralf_hetzner",
    "root@77.42.66.40",
    "python3", "-c",
    "exec(open('/opt/ralf/mcp-server.py').read())"
  ]
}
```

**moltbot-vps (stdio local):**
```json
{
  "type": "stdio",
  "command": "python3",
  "args": ["/Users/shaansisodia/.blackbox5/mcp-server-moltbot.py"]
}
```

## Data Flow

### 1. RALF Task Completion Flow

```
RALF Executor completes task
        ↓
Writes to events.yaml
        ↓
RALF Watcher (cron) detects change
        ↓
Sends notification to Moltbot Gateway
        ↓
Telegram Bot sends message to user
```

### 2. User Query Flow

```
User sends !ralf status in Telegram
        ↓
Moltbot receives command
        ↓
RALF Status Skill reads queue.yaml
        ↓
Formats status report
        ↓
Sends reply to Telegram
```

### 3. Claude Code Query Flow

```
User asks about RALF status in Claude Code
        ↓
Claude uses moltbot_get_ralf_status tool
        ↓
MCP server SSHs to VPS
        ↓
Reads queue.yaml
        ↓
Returns formatted status
```

## Security Model

1. **SSH Key Authentication:** `~/.ssh/ralf_hetzner` for VPS access
2. **Gateway Token:** `ralf-local-token-12345` for SSE connections
3. **Telegram Pairing:** User ID whitelist (7643203581 approved)
4. **File Permissions:** RALF files readable by moltbot user

## Deployment

### VPS Setup (moltbot-setup.sh)

1. Install Node.js 22+
2. Install Chrome for browser automation
3. Install OpenClaw globally: `npm install -g openclaw`
4. Create directories: `/opt/moltbot`, `/opt/moltbot/logs`, `/opt/moltbot/skills`
5. Create RALF integration skill
6. Create systemd service
7. Create configuration files
8. Set up cron jobs for RALF watching

### Systemd Service

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

## Configuration Files

### openclaw.json

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

### user-context.json

```json
{
  "user": {
    "name": "Shaan",
    "telegram_id": "7643203581",
    "role": "Founder/Developer",
    "preferences": {
      "communication_style": "direct",
      "detail_level": "high"
    }
  },
  "context": {
    "current_focus": "RALF autonomous agent system",
    "active_project": "blackbox5"
  },
  "ralf_integration": {
    "queue_file": "/opt/ralf/.../queue.yaml",
    "events_file": "/opt/ralf/.../events.yaml",
    "verify_file": "/opt/ralf/.../verify.yaml"
  }
}
```
