# Agent Communication Architecture

**Status:** Active
**Last Updated:** 2026-02-07
**Version:** 1.1

## Overview

BlackBox5 uses a distributed multi-agent architecture where agents communicate via Redis pub/sub. This document describes the communication patterns, message broker configuration, and scaling considerations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Redis Message Broker                             │
│                    (77.42.66.40:6379 - VPS)                              │
│                                                                          │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐ │
│  │ claude:openclaw:   │  │ openclaw:claude:   │  │   agents:general   │ │
│  │     messages       │  │     messages       │  │                    │ │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘ │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐ │
│  │ agents:discovery:  │  │ agents:discovery:  │  │  agent:{id}:       │ │
│  │     announce       │  │     response       │  │    heartbeat       │ │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    ▲
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│  Claude Code  │          │   OpenClaw    │          │   Mac Mini    │
│  (Mac Local)  │◄────────►│   (VPS)       │◄────────►│  (Network)    │
│               │          │               │          │               │
│ MCP Bridge    │          │ Node.js       │          │ Node.js       │
│ Python        │          │ Bridge        │          │ Bridge        │
└───────────────┘          └───────────────┘          └───────────────┘
```

## Communication Patterns

### 1. Direct Messaging (Point-to-Point)

**Use Case:** Targeted commands, responses, private communication

**Channels:**
```
[source]:[target]:messages
```

**Examples:**
- `claude:openclaw:messages` - Claude sends to OpenClaw
- `openclaw:claude:messages` - OpenClaw responds to Claude

**Message Flow:**
1. Sender publishes to target's channel
2. Target receives via pub/sub subscription
3. Target processes and optionally responds

### 2. Broadcast Messaging (One-to-Many)

**Use Case:** Announcements, events, general notifications

**Channels:**
```
agents:general      # All agents receive
agents:events       # System events only
agents:discovery:*  # Discovery protocol
```

**Message Flow:**
1. Agent publishes to `agents:general`
2. All subscribed agents receive
3. Each agent decides whether to act

### 3. Discovery Protocol

**Use Case:** Agent joining, capability discovery, presence

**Channels:**
```
agents:discovery:announce   # "I am here"
agents:discovery:query      # "Who is available?"
agents:discovery:response   # "I am agent X with capabilities Y"
```

**Message Flow:**
```
New Agent                  Existing Agents
    │                            │
    ├───agents:discovery:announce─┤
    │                            │
    │◄─────────subscribe─────────┤
    │                            │
    ├───agents:discovery:query──►│
    │                            │
    │◄──agents:discovery:response┤
    │                            │
```

### 4. Presence/Heartbeat

**Use Case:** Liveness detection, health monitoring

**Implementation:**
```
# Each agent publishes to its own heartbeat channel
agent:{id}:heartbeat

# Redis keys for presence tracking (using EXPIRE)
agent:{id}:last_seen      # Timestamp
agents:active             # Redis Set of active agents
```

**Heartbeat Interval:** 30 seconds
**Timeout Threshold:** 90 seconds (3 missed heartbeats)

## Adding New Agents to the Cluster

### Step 1: Assign Agent ID

Choose a unique identifier:
```
[platform]-[instance]-[nn]
```

Examples:
- `claude-code-mac-01`
- `openclaw-vps-01`
- `macmini-local-01`

### Step 2: Deploy Bridge

Choose implementation:

**Option A: Python MCP Bridge** (for Claude Code integration)
```bash
cp mcp-redis-bridge.py mcp-redis-bridge-[agent].py
# Update AGENT_ID constant
# Update channel subscriptions
```

**Option B: Node.js Bridge** (for standalone agents)
```bash
cp openclaw-redis-bridge.js [agent]-bridge.js
# Update AGENT_ID constant
# Update channel subscriptions
```

### Step 3: Configure Channels

Add to bridge configuration:
```python
CHANNELS = {
    "inbox": f"agent:{AGENT_ID}:messages",
    "broadcast": "agents:general",
    "heartbeat": f"agent:{AGENT_ID}:heartbeat",
    "announce": "agents:discovery:announce"
}
```

### Step 4: Start Service

**Systemd (Linux VPS):**
```bash
sudo systemctl enable [agent]-bridge
sudo systemctl start [agent]-bridge
```

**Launchd (macOS):**
```bash
launchctl load ~/Library/LaunchAgents/com.blackbox5.[agent].plist
```

### Step 5: Verify Connection

```bash
# Check Redis for agent presence
redis-cli SMEMBERS agents:active

# Send test message
redis-cli PUBLISH agents:general '{"from":"test","type":"ping"}'
```

## Scaling Considerations

### Redis Pub/Sub Limits

| Metric | Limit | Notes |
|--------|-------|-------|
| Connections | 10,000+ | Can increase with `ulimit` |
| Channels | Unlimited | Memory-bound only |
| Message Rate | 100K+/sec | Single Redis instance |
| Latency | < 1ms | Local network |

### Scaling Strategies

#### 1. Single Redis Instance (Current)

**Good for:** 2-10 agents, low message volume

**Configuration:**
- Default Redis settings
- No persistence required for messaging
- Memory: 64MB sufficient

#### 2. Redis Cluster (Future)

**Good for:** 10-100 agents, high availability

**Setup:**
```bash
# 3 master + 3 replica nodes
redis-cli --cluster create \
  77.42.66.40:6379 77.42.66.40:6380 77.42.66.40:6381 \
  77.42.66.41:6379 77.42.66.41:6380 77.42.66.41:6381 \
  --cluster-replicas 1
```

**Considerations:**
- Pub/sub broadcasts to all nodes
- Channel patterns work across cluster
- Higher memory overhead

#### 3. Redis Sentinel (High Availability)

**Good for:** Production deployments, failover required

**Setup:**
```bash
# 1 master + 2 replicas + 3 sentinels
# Automatic failover on master failure
```

### Performance Optimization

#### Message Size

Keep messages under 1MB:
```json
{
  "from": "agent-id",
  "type": "command",
  "message": "string or small object",
  "timestamp": "ISO8601",
  "id": "uuid"
}
```

For large payloads:
1. Store in Redis (SET key value)
2. Publish reference ID
3. Receiver fetches by ID

#### Connection Pooling

Use connection pools for high throughput:
```python
# Python redis-py
pool = redis.ConnectionPool(host='77.42.66.40', port=6379)
client = redis.Redis(connection_pool=pool)
```

```javascript
// Node.js ioredis
const Redis = require('ioredis');
const client = new Redis({ host: '77.42.66.40', port: 6379 });
```

#### Pattern Subscriptions

Use pattern matching for dynamic channels:
```python
# Subscribe to all agent channels
pubsub.psubscribe('agent:*:messages')

# Subscribe to all discovery channels
pubsub.psubscribe('agents:discovery:*')
```

## Security

### Network Security

**Current:**
- Redis bound to localhost on VPS
- No external access
- Agents connect via SSH tunnel or local network

**Production:**
```bash
# Enable AUTH
redis-cli AUTH your-strong-password

# Or use TLS
redis-cli --tls --cert client.crt --key client.key
```

### Message Security

**Option 1: Payload Encryption**
```python
from cryptography.fernet import Fernet
cipher = Fernet(key)
encrypted = cipher.encrypt(message.encode())
```

**Option 2: Channel Isolation**
```
# Separate channels by sensitivity
agent:{id}:public:messages
agent:{id}:private:messages
agent:{id}:secure:messages
```

## Monitoring

### Redis Metrics

```bash
# Connection count
redis-cli INFO clients

# Pub/sub channels
redis-cli PUBSUB CHANNELS

# Memory usage
redis-cli INFO memory
```

### Agent Health

```bash
# Check active agents
redis-cli SMEMBERS agents:active

# Check last heartbeat
redis-cli GET agent:claude-code:last_seen

# Check message backlog
redis-cli LLEN agent:claude-code:messages
```

## Troubleshooting

| Issue | Symptom | Solution |
|-------|---------|----------|
| Connection refused | Cannot connect to Redis | Check Redis running, firewall rules |
| Message loss | Messages not received | Use Redis lists for persistence |
| High latency | Slow message delivery | Check network, Redis slowlog |
| Memory growth | Redis using too much RAM | Set TTL on keys, limit channel history |
| Split brain | Agents disagree on state | Implement consensus protocol |

## Migration from Telegram

See: `../migration/telegram-to-redis.md`

## Related Documentation

- `../../knowledge/redis-agent-bridge.md` - Bridge implementation details
- `../tasks/TASK-multi-agent-cluster.md` - Multi-agent roadmap
- `../../DUAL-RALF-ARCHITECTURE.md` - Overall system architecture

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-07 | Initial Redis architecture |
| 1.1 | 2026-02-07 | Added scaling considerations, security |
