# Moltbot-RALF Integration Architecture

## Overview
Single VPS (Helsingor) hosts both RALF autonomous agent system and OpenClaw (Moltbot) Telegram interface, connected via file-based bridge and MCP.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         YOUR MACBOOK (Local)                                 │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    CLAUDE CODE (This Session)                        │    │
│  │                                                                      │    │
│  │  ┌─────────────────┐            ┌─────────────────────────────────┐  │    │
│  │  │  MCP Client     │◄──────────►│  MCP Servers (via .mcp.json)    │  │    │
│  │  │  (Built-in)     │            │                                 │  │    │
│  │  └─────────────────┘            │  1. ralf-vps (SSH stdio)        │  │    │
│  │                                 │     - Executes RALF commands    │  │    │
│  │                                 │     - Spawns: ssh root@77.42... │  │    │
│  │                                 │                                 │  │    │
│  │                                 │  2. moltbot-vps (SSE)           │  │    │
│  │                                 │     - Talks to OpenClaw Gateway │  │    │
│  │                                 │     - URL: 77.42.66.40:18789    │  │    │
│  │                                 └─────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ SSH (ralf-vps)  │  HTTP/SSE (moltbot-vps)
                                    │                 │
                                    ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VPS HELSINGOR (77.42.66.40)                               │
│                                                                              │
│  ┌───────────────────────────────┐    ┌─────────────────────────────────┐   │
│  │      OPENCLAW (Moltbot)       │    │           RALF                  │   │
│  │       Port 18789              │    │                                 │   │
│  │                               │    │  ┌─────────────────────────┐    │   │
│  │  ┌─────────────────────────┐  │    │  │  Planner Agent          │    │   │
│  │  │    Gateway API          │  │    │  │  - Creates task plans   │    │   │
│  │  │  - /sse (MCP endpoint)  │◄─┼────┼──┤  - Reads queue.yaml     │    │   │
│  │  │  - /health              │  │    │  └─────────────────────────┘    │   │
│  │  │  - WebSocket control    │  │    │              │                  │   │
│  │  └─────────────────────────┘  │    │              ▼                  │   │
│  │           │                   │    │  ┌─────────────────────────┐    │   │
│  │  ┌────────▼────────┐          │    │  │  Executor Agent         │    │   │
│  │  │  Telegram Bot   │◄─────────┼────┼──┤  - Executes tasks       │    │   │
│  │  │  @SISOlegacybot │          │    │  │  - Updates events.yaml  │    │   │
│  │  └─────────────────┘          │    │  └─────────────────────────┘    │   │
│  │           │                   │    │                                 │   │
│  │  ┌────────▼────────┐          │    │  Communication Files:           │   │
│  │  │  RALF Skills    │◄─────────┘    │  - queue.yaml (pending)         │   │
│  │  │  - ralf-status  │   File Read   │  - events.yaml (completed)      │   │
│  │  │  - ralf-context │               │  - verify.yaml (verification)   │   │
│  │  └─────────────────┘               │                                 │   │
│  └───────────────────────────────┘    └─────────────────────────────────┘   │
│                                                                              │
│  File Locations:                                                             │
│  - /opt/moltbot/user-context.json        (Shaan's profile)                   │
│  - /opt/moltbot/skills/ralf-status.js    (RALF Telegram commands)            │
│  - /opt/ralf/5-project-memory/blackbox5/.autonomous/agents/communications/  │
│    - queue.yaml                                                                │
│    - events.yaml                                                               │
│    - verify.yaml                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Communication Patterns

### 1. File-Based Bridge (RALF ↔ Moltbot)
RALF writes task state to YAML files. Moltbot reads them via skills.

```yaml
# queue.yaml - RALF writes, Moltbot reads
queue:
  - task_id: "TASK-001"
    status: "pending"
    priority: "high"
```

Telegram commands:
- `!ralf status` - Shows current RALF state
- `!ralf queue` - Lists pending tasks
- `!ralf task <id>` - Shows specific task details

### 2. MCP Connection (MacBook ↔ VPS)

#### ralf-vps (stdio over SSH)
```json
{
  "type": "stdio",
  "command": "ssh",
  "args": [
    "-i", "~/.ssh/ralf_hetzner",
    "root@77.42.66.40",
    "python3", "-c",
    "import json, sys, subprocess; exec(open('/opt/ralf/mcp-server.py').read())"
  ]
}
```
Use: Direct RALF command execution on VPS

#### moltbot-vps (SSE)
```json
{
  "type": "sse",
  "url": "http://77.42.66.40:18789/sse"
}
```
Use: Send messages via Telegram, check gateway status

## MCP Setup on MacBook

### Quick Start (Recommended)

Run the setup script to establish SSH tunnel and verify connections:

```bash
~/.blackbox5/bin/moltbot-mcp-connect.sh
```

This will:
1. Create SSH tunnel from localhost:18789 → VPS:18789
2. Verify ralf-vps MCP server is accessible
3. Verify moltbot-vps SSE endpoint is responding

Then start Claude Code with MCP:

```bash
cd ~/.blackbox5 && claude --mcp-config .mcp-moltbot.json
```

### Manual Setup

If you prefer manual setup:

1. **Create SSH tunnel** (in a separate terminal):
```bash
ssh -i ~/.ssh/ralf_hetzner -L 18789:localhost:18789 root@77.42.66.40 -N
```

2. **Start Claude Code with MCP config**:
```bash
claude --mcp-config ~/.blackbox5/.mcp-moltbot.json
```

### MCP Config Location

The config file is at `~/.blackbox5/.mcp-moltbot.json`:

```json
{
  "mcpServers": {
    "ralf-vps": {
      "type": "stdio",
      "command": "ssh",
      "args": [
        "-i", "~/.ssh/ralf_hetzner",
        "root@77.42.66.40",
        "python3", "-c",
        "import json, sys, subprocess; exec(open('/opt/ralf/mcp-server.py').read())"
      ]
    },
    "moltbot-vps": {
      "type": "sse",
      "url": "http://localhost:18789/sse",
      "headers": {
        "Authorization": "Bearer ralf-local-token-12345"
      }
    }
  }
}
```

**Note**: `moltbot-vps` uses `localhost:18789` because the SSH tunnel forwards to the VPS gateway.

## Testing the Connection

### Test ralf-vps MCP
```bash
# This should list RALF tasks
ssh -i ~/.ssh/ralf_hetzner root@77.42.66.40 "ls -la /opt/ralf/5-project-memory/blackbox5/.autonomous/agents/communications/"
```

### Test moltbot-vps MCP
```bash
# Check gateway health
curl http://77.42.66.40:18789/health

# Test SSE endpoint
curl -N http://77.42.66.40:18789/sse -H "Authorization: Bearer ralf-local-token-12345"
```

### Test Telegram Bot
Send to @SISOlegacybot:
- `!ralf status` - Should show current RALF state
- `!ralf queue` - Should show pending tasks

## Current Status

| Component | Status | Location |
|-----------|--------|----------|
| OpenClaw Gateway | Running | 77.42.66.40:18789 |
| Telegram Bot | Connected | @SISOlegacybot |
| User Context | Loaded | /opt/moltbot/user-context.json |
| RALF Skills | Installed | /opt/moltbot/skills/ |
| RALF System | Ready | /opt/ralf/ |

## Security Notes

1. **Gateway Auth**: Token-based (`ralf-local-token-12345`)
2. **SSH Key**: `~/.ssh/ralf_hetzner` for VPS access
3. **Telegram**: Pairing required for DMs (your ID: 7643203581 already approved)
4. **Network**: Gateway bound to localhost on VPS (access via SSH tunnel or direct if firewall allows)

## Next Steps

1. Start Claude Code with MCP config
2. Test `ralf-vps` connection (list queue, check status)
3. Test `moltbot-vps` connection (send Telegram message)
4. Verify Telegram bot responds to `!ralf status`
