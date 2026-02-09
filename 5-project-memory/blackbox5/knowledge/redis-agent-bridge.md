# Redis Agent-to-Agent Communication Bridge

**Status:** Active
**Created:** 2026-02-07
**Version:** 1.0

## Overview

The Redis Agent Bridge enables bidirectional real-time communication between Claude Code (local) and OpenClaw (VPS) using Redis pub/sub. This replaces the previous Telegram-based messaging system with a lower-latency, more reliable message broker.

## Architecture

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────────┐
│   Claude Code   │◄───────►│    Redis     │◄───────►│    OpenClaw     │
│   (Mac Local)   │         │   Server     │         │   (VPS Node)    │
└─────────────────┘         └──────────────┘         └─────────────────┘
        │                          │                          │
        │  mcp-redis-bridge.py     │    Pub/Sub Channels      │  openclaw-
        │  (MCP Server)            │                          │  redis-bridge.js
        │                          │                          │  (Node.js)
        └──────────────────────────┘                          └──────────┘
```

### Message Flow

1. **Claude Code → OpenClaw:**
   - Claude calls MCP tool `redis_send_to_openclaw`
   - `mcp-redis-bridge.py` publishes to `claude:openclaw:messages`
   - `openclaw-redis-bridge.js` receives and processes
   - Response published to `openclaw:claude:messages`

2. **OpenClaw → Claude Code:**
   - OpenClaw publishes to `openclaw:claude:messages`
   - `mcp-redis-bridge.py` receives via pub/sub
   - Messages queued for Claude to retrieve via `redis_receive_from_openclaw`

## Components

### 1. MCP Redis Bridge (Local)

**Location:** `~/.blackbox5/mcp-redis-bridge.py`

Python-based MCP server providing tools for Claude Code:

| Tool | Purpose |
|------|---------|
| `redis_send_to_openclaw` | Send message to OpenClaw |
| `redis_receive_from_openclaw` | Poll for responses |
| `redis_conversation` | Send and wait for response |
| `redis_status` | Check connection health |

**Key Features:**
- Async message handling
- Background listener thread
- Message queue for responses
- JSON-RPC MCP protocol

### 2. OpenClaw Redis Bridge (VPS)

**Location:** `/opt/openclaw-redis-bridge.js`

Node.js service running on VPS:

**Key Features:**
- Subscribes to `claude:openclaw:messages`
- Processes commands (status, tasks, hello)
- Publishes responses to `openclaw:claude:messages`
- Auto-reconnect on disconnect

### 3. Redis Server

**Host:** `77.42.66.40` (VPS)
**Port:** `6379`

Configured for:
- Pub/sub messaging
- Low latency (< 10ms typical)
- Persistence optional (not required for messaging)

## Channel Naming Convention

```
[source]:[target]:[purpose]
```

| Channel | Direction | Purpose |
|---------|-----------|---------|
| `claude:openclaw:messages` | Claude → OpenClaw | Commands, queries |
| `openclaw:claude:messages` | OpenClaw → Claude | Responses, events |
| `agents:general` | Broadcast | Multi-agent messages |
| `agent:[id]:heartbeat` | Per-agent | Presence/liveness |

## Message Format

```json
{
  "from": "claude-code|openclaw|agent-id",
  "type": "text|command|response|event",
  "message": "string content",
  "timestamp": "2026-02-07T12:00:00Z",
  "id": "unique-message-id",
  "inReplyTo": "optional-parent-id"
}
```

## Configuration

### MCP Settings (Claude Code)

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "redis-bridge": {
      "command": "python3",
      "args": ["/Users/shaansisodia/.blackbox5/mcp-redis-bridge.py"]
    }
  }
}
```

### VPS Service (OpenClaw)

Create `/etc/systemd/system/openclaw-redis-bridge.service`:

```ini
[Unit]
Description=OpenClaw Redis Bridge
After=network.target redis-server.service

[Service]
Type=simple
User=openclaw
WorkingDirectory=/opt
ExecStart=/usr/bin/node /opt/openclaw-redis-bridge.js
Restart=always
RestartSec=5
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw-redis-bridge
sudo systemctl start openclaw-redis-bridge
```

## Usage Examples

### Send Message
```
Use tool: redis_send_to_openclaw
  message: "Get active tasks"
```

### Conversation
```
Use tool: redis_conversation
  message: "Status check"
  wait_seconds: 10
```

### Check Status
```
Use tool: redis_status
```

## Monitoring

Check bridge status:
```bash
# Local (Claude Code side)
redis-cli -h 77.42.66.40 ping

# VPS (OpenClaw side)
sudo systemctl status openclaw-redis-bridge
journalctl -u openclaw-redis-bridge -f
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Connection refused | Redis not running | `sudo systemctl start redis-server` |
| Timeout on send | OpenClaw bridge down | Check VPS service status |
| No responses | Channel mismatch | Verify channel names match |
| Message loss | No persistence | Use lists for guaranteed delivery |

## Security Considerations

- Redis bound to localhost on VPS (no external access)
- Use Redis AUTH for additional security
- Consider SSH tunnel for remote Redis access
- No sensitive data in message payloads

## Scaling

Redis pub/sub supports:
- 10,000+ concurrent connections
- Sub-millisecond latency
- Pattern matching for channel subscriptions

Future agents can use:
- `agents:general` for broadcasts
- `agent:[id]:messages` for direct messaging
- `agent:[id]:heartbeat` for presence

## Files Reference

| File | Location | Purpose |
|------|----------|---------|
| MCP Bridge | `~/.blackbox5/mcp-redis-bridge.py` | Claude Code integration |
| OpenClaw Bridge | `/opt/openclaw-redis-bridge.js` | VPS listener |
| Service Config | `/etc/systemd/system/openclaw-redis-bridge.service` | Process management |
| MCP Settings | `~/.claude/settings.json` | Claude configuration |

## Related Documentation

- `migration/telegram-to-redis.md` - Migration guide
- `tasks/TASK-multi-agent-cluster.md` - Multi-agent roadmap
- `architecture/agent-communication.md` - System architecture
