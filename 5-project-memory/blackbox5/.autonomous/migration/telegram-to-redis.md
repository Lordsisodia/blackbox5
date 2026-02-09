# Migration Guide: Telegram to Redis Agent Communication

**Status:** Complete
**Migration Date:** 2026-02-07
**From:** Telegram Bot API
**To:** Redis Pub/Sub

## Overview

This guide documents the migration from Telegram-based agent communication to Redis pub/sub. The migration was completed to achieve lower latency, higher reliability, and better scalability.

## Why Migrate?

| Factor | Telegram | Redis |
|--------|----------|-------|
| Latency | 100-500ms | <10ms |
| Reliability | Dependent on Telegram API | Local control |
| Rate Limits | 30 msg/sec | Unlimited |
| Message Size | 4096 chars | 512MB |
| Offline Queue | Limited | Unlimited (with persistence) |
| Multi-Agent | Complex | Native pub/sub |

## Pre-Migration Checklist

Before starting migration:

- [ ] Redis server installed and running
- [ ] Network connectivity verified (all agents → Redis)
- [ ] Backup Telegram bot credentials (for rollback)
- [ ] Document current Telegram channel names
- [ ] Identify all agents using Telegram

## Migration Steps

### Step 1: Deploy Redis Server

**On VPS (77.42.66.40):**

```bash
# Install Redis
sudo apt update
sudo apt install redis-server

# Configure for external access (if needed)
sudo nano /etc/redis/redis.conf
# bind 127.0.0.1 ::1  # Keep localhost only for security
# port 6379

# Start Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Verify
redis-cli ping
# Should return: PONG
```

### Step 2: Deploy MCP Redis Bridge (Claude Code)

**On Mac Local:**

```bash
# Navigate to BlackBox5
cd ~/.blackbox5

# Create bridge file
cat > mcp-redis-bridge.py << 'BRIDGE_EOF'
#!/usr/bin/env python3
"""
Redis MCP Bridge - Bidirectional Claude Code <-> OpenClaw Communication
Uses Redis pub/sub for real-time messaging
"""

import asyncio
import json
import sys
import redis
import threading
import time
from datetime import datetime

# Redis configuration
REDIS_HOST = "77.42.66.40"
REDIS_PORT = 6379
REDIS_DB = 0

# Channel names
CHANNEL_CLAUDE_TO_OPENCLAW = "claude:openclaw:messages"
CHANNEL_OPENCLAW_TO_CLAUDE = "openclaw:claude:messages"
CHANNEL_RESPONSES = "claude:responses"

class RedisBridge:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )
        self.pubsub = self.redis_client.pubsub()
        self.message_queue = []
        self.running = True

    def publish_to_openclaw(self, message, msg_type="text"):
        """Publish message from Claude Code to OpenClaw"""
        payload = {
            "from": "claude-code",
            "type": msg_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "id": f"claude-{int(time.time() * 1000)}"
        }
        self.redis_client.publish(CHANNEL_CLAUDE_TO_OPENCLAW, json.dumps(payload))
        return payload["id"]

    def listen_for_responses(self, callback):
        """Listen for messages from OpenClaw"""
        self.pubsub.subscribe(CHANNEL_OPENCLAW_TO_CLAUDE)
        print(f"[Redis Bridge] Subscribed to {CHANNEL_OPENCLAW_TO_CLAUDE}", file=sys.stderr)

        for message in self.pubsub.listen():
            if not self.running:
                break
            if message['type'] == 'message':
                try:
                    data = json.loads(message['data'])
                    callback(data)
                except json.JSONDecodeError:
                    callback({"raw": message['data']})

    def get_recent_messages(self, count=10):
        """Get recent messages from Redis list"""
        messages = self.redis_client.lrange(CHANNEL_RESPONSES, -count, -1)
        return [json.loads(m) for m in messages] if messages else []

    def close(self):
        self.running = False
        self.pubsub.unsubscribe()
        self.redis_client.close()

# Global bridge instance
bridge = RedisBridge()

async def main():
    print("[Redis Bridge] Starting...", file=sys.stderr)

    # Start listener in background thread
    def on_message(data):
        bridge.message_queue.append(data)
        print(f"[Redis Bridge] Received: {data}", file=sys.stderr)

    listener_thread = threading.Thread(
        target=bridge.listen_for_responses,
        args=(on_message,),
        daemon=True
    )
    listener_thread.start()

    # Process MCP requests
    while True:
        line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not line:
            break

        try:
            request = json.loads(line)
            method = request.get("method", "")
            msg_id = request.get("id")

            if method == "tools/list":
                response = {
                    "tools": [
                        {
                            "name": "redis_send_to_openclaw",
                            "description": "Send message to OpenClaw via Redis",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "message": {"type": "string"},
                                    "type": {"type": "string", "default": "text"}
                                },
                                "required": ["message"]
                            }
                        },
                        {
                            "name": "redis_receive_from_openclaw",
                            "description": "Receive messages from OpenClaw (poll for responses)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "timeout": {"type": "integer", "default": 10},
                                    "clear": {"type": "boolean", "default": true}
                                }
                            }
                        },
                        {
                            "name": "redis_conversation",
                            "description": "Send message and wait for response from OpenClaw",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "message": {"type": "string"},
                                    "wait_seconds": {"type": "integer", "default": 15}
                                },
                                "required": ["message"]
                            }
                        },
                        {
                            "name": "redis_status",
                            "description": "Check Redis connection status",
                            "inputSchema": {"type": "object"}
                        }
                    ]
                }

            elif method == "tools/call":
                tool = request.get("params", {}).get("name", "")
                args = request.get("params", {}).get("arguments", {})

                if tool == "redis_send_to_openclaw":
                    message = args.get("message", "")
                    msg_type = args.get("type", "text")
                    msg_id = bridge.publish_to_openclaw(message, msg_type)
                    response = {
                        "content": [{
                            "type": "text",
                            "text": f"✅ Published to Redis (ID: {msg_id})"
                        }]
                    }

                elif tool == "redis_receive_from_openclaw":
                    timeout = args.get("timeout", 10)
                    clear = args.get("clear", True)
                    await asyncio.sleep(timeout)
                    messages = bridge.message_queue.copy()
                    if clear:
                        bridge.message_queue.clear()
                    text = json.dumps(messages, indent=2) if messages else "No messages received"
                    response = {"content": [{"type": "text", "text": text}]}

                elif tool == "redis_conversation":
                    message = args.get("message", "")
                    wait = args.get("wait_seconds", 15)
                    bridge.message_queue.clear()
                    msg_id = bridge.publish_to_openclaw(message)
                    await asyncio.sleep(wait)
                    responses = bridge.message_queue.copy()
                    bridge.message_queue.clear()
                    result = f"📤 Sent: {message}\n📥 Responses ({len(responses)}):\n"
                    result += json.dumps(responses, indent=2) if responses else "No response yet"
                    response = {"content": [{"type": "text", "text": result}]}

                elif tool == "redis_status":
                    try:
                        bridge.redis_client.ping()
                        status = "✅ Connected"
                    except Exception as e:
                        status = f"❌ Error: {e}"
                    response = {"content": [{"type": "text", "text": f"Redis Status: {status}"}]}

                else:
                    response = {
                        "content": [{"type": "text", "text": f"Unknown tool: {tool}"}],
                        "isError": True
                    }

            else:
                response = {"error": f"Unknown method: {method}"}

            response["jsonrpc"] = "2.0"
            response["id"] = msg_id
            print(json.dumps(response), flush=True)

        except Exception as e:
            error = {"jsonrpc": "2.0", "error": str(e), "id": request.get("id")}
            print(json.dumps(error), flush=True)

    bridge.close()

if __name__ == "__main__":
    asyncio.run(main())
BRIDGE_EOF

chmod +x mcp-redis-bridge.py
```

### Step 3: Configure Claude Code MCP

**Edit `~/.claude/settings.json`:**

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

**Restart Claude Code** to load the new MCP server.

### Step 4: Deploy OpenClaw Redis Bridge (VPS)

**On VPS:**

```bash
# Create bridge file
sudo tee /opt/openclaw-redis-bridge.js > /dev/null << 'BRIDGE_EOF'
#!/usr/bin/env node
/**
 * OpenClaw Redis Bridge - Node.js side
 * Listens for messages from Claude Code via Redis and responds
 */

const redis = require('redis');
const { exec } = require('child_process');

const REDIS_HOST = 'localhost';
const REDIS_PORT = 6379;

const CHANNEL_CLAUDE_TO_OPENCLAW = 'claude:openclaw:messages';
const CHANNEL_OPENCLAW_TO_CLAUDE = 'openclaw:claude:messages';

class OpenClawRedisBridge {
  constructor() {
    this.client = redis.createClient({
      host: REDIS_HOST,
      port: REDIS_PORT
    });
    this.subscriber = this.client.duplicate();
  }

  async start() {
    await this.client.connect();
    await this.subscriber.connect();

    console.log('[OpenClaw Bridge] Connected to Redis');

    await this.subscriber.subscribe(CHANNEL_CLAUDE_TO_OPENCLAW, async (message) => {
      try {
        const data = JSON.parse(message);
        console.log('[OpenClaw Bridge] Received:', data);
        const response = await this.processMessage(data);
        await this.publishToClaude(response);
      } catch (err) {
        console.error('[OpenClaw Bridge] Error:', err);
      }
    });

    console.log(`[OpenClaw Bridge] Subscribed to ${CHANNEL_CLAUDE_TO_OPENCLAW}`);
  }

  async processMessage(data) {
    const { message, type, id } = data;
    let responseText = '';

    if (message.includes('status')) {
      responseText = 'OpenClaw is running via Redis bridge';
    } else if (message.includes('hello') || message.includes('hi')) {
      responseText = 'Hello from OpenClaw! I received your message via Redis.';
    } else if (message.includes('task') || message.includes('plan')) {
      responseText = await this.getTasks();
    } else {
      responseText = `Received: "${message}". I'm OpenClaw responding via Redis!`;
    }

    return {
      from: 'openclaw',
      type: 'response',
      message: responseText,
      inReplyTo: id,
      timestamp: new Date().toISOString()
    };
  }

  async getTasks() {
    return new Promise((resolve) => {
      exec('ls ~/.blackbox5/5-project-memory/blackbox5/tasks/active/ 2>/dev/null | head -5', (err, stdout) => {
        if (err) {
          resolve('Could not fetch tasks');
        } else {
          const tasks = stdout.trim().split('\n').filter(t => t);
          resolve(`Active tasks: ${tasks.length > 0 ? tasks.join(', ') : 'None'}`);
        }
      });
    });
  }

  async publishToClaude(data) {
    await this.client.publish(CHANNEL_OPENCLAW_TO_CLAUDE, JSON.stringify(data));
    console.log('[OpenClaw Bridge] Published response:', data);
  }
}

const bridge = new OpenClawRedisBridge();
bridge.start().catch(console.error);

process.on('SIGINT', async () => {
  console.log('\n[OpenClaw Bridge] Shutting down...');
  await bridge.client.quit();
  await bridge.subscriber.quit();
  process.exit(0);
});
BRIDGE_EOF

# Install dependencies
cd /opt
npm install redis

# Make executable
chmod +x openclaw-redis-bridge.js
```

### Step 5: Create Systemd Service

**On VPS:**

```bash
sudo tee /etc/systemd/system/openclaw-redis-bridge.service > /dev/null << 'EOF'
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
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable openclaw-redis-bridge
sudo systemctl start openclaw-redis-bridge

# Check status
sudo systemctl status openclaw-redis-bridge
```

### Step 6: Test Communication

**In Claude Code:**

```
Use tool: redis_status
```

Expected: `✅ Connected`

```
Use tool: redis_conversation
  message: "Hello from Claude!"
  wait_seconds: 5
```

Expected: Response from OpenClaw within 5 seconds.

### Step 7: Update Documentation

Update all references from Telegram to Redis:

```bash
# Find Telegram references
grep -r "telegram" ~/.blackbox5/5-project-memory/blackbox5/ --include="*.md" -l

# Update each file
# Replace Telegram instructions with Redis equivalents
```

### Step 8: Disable Telegram (Optional)

If migration successful:

```bash
# Stop Telegram bot (if running as service)
sudo systemctl stop telegram-bot
sudo systemctl disable telegram-bot

# Keep credentials for rollback
cp ~/.telegram-bot-token ~/.telegram-bot-token.backup
```

## Rollback Procedure

If issues arise:

1. **Stop Redis bridges:**
   ```bash
   # VPS
   sudo systemctl stop openclaw-redis-bridge

   # Remove from Claude Code MCP config
   ```

2. **Restart Telegram bot:**
   ```bash
   sudo systemctl start telegram-bot
   ```

3. **Update documentation** to reference Telegram again

## Verification Checklist

- [ ] `redis_status` returns "Connected"
- [ ] Messages sent from Claude received by OpenClaw
- [ ] Responses received by Claude within 10 seconds
- [ ] No errors in bridge logs (`journalctl -u openclaw-redis-bridge`)
- [ ] Redis memory usage stable
- [ ] All agents communicating successfully

## Post-Migration Tasks

- [ ] Document new channel names
- [ ] Update runbooks
- [ ] Train team on new tools
- [ ] Monitor for 48 hours
- [ ] Archive Telegram configuration

## Files Reference

| File | Purpose |
|------|---------|
| `~/.blackbox5/mcp-redis-bridge.py` | Claude Code MCP bridge |
| `/opt/openclaw-redis-bridge.js` | OpenClaw VPS bridge |
| `/etc/systemd/system/openclaw-redis-bridge.service` | VPS service config |
| `~/.claude/settings.json` | MCP configuration |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Check Redis running: `redis-cli ping` |
| Timeout on send | Check OpenClaw bridge: `sudo systemctl status openclaw-redis-bridge` |
| No response | Verify channel names match |
| Import errors | Install redis: `pip3 install redis` / `npm install redis` |

## Migration Complete

Once all checks pass, the migration is complete. The system now uses Redis for all agent-to-agent communication.

**Next Steps:**
- Implement multi-agent cluster (see `../tasks/TASK-multi-agent-cluster.md`)
- Add monitoring and alerting
- Document new capabilities
