# NATS JetStream Configuration for Multi-Agent System

## Server Details
- **Host**: 77.42.66.40 (VPS)
- **Port**: 4222
- **Monitoring**: 8222
- **Version**: v2.10.24
- **Authentication**: admin / blackbox5

## JetStream Streams Created

### 1. agent-messages
- **Purpose**: Direct agent-to-agent messaging
- **Subjects**: `agent.*.inbox`, `agent.*.direct`
- **Retention**: Limits-based
- **Max Messages**: 10,000
- **Max Bytes**: 100MB
- **Max Age**: 7 days
- **Storage**: File (persistent)

### 2. agent-broadcast
- **Purpose**: Broadcast messages to all agents
- **Subjects**: `broadcast.*`, `announce.*`
- **Retention**: Limits-based
- **Max Messages**: 5,000
- **Max Bytes**: 50MB
- **Max Age**: 3 days
- **Storage**: File (persistent)

### 3. agent-tasks
- **Purpose**: Task distribution (work queue pattern)
- **Subjects**: `tasks.*`, `work.*`
- **Retention**: Work Queue (messages removed after acknowledgment)
- **Max Messages**: 50,000
- **Max Bytes**: 200MB
- **Max Age**: 14 days
- **Storage**: File (persistent)

## Key Capabilities

### Guaranteed Delivery
- Messages persist to disk until acknowledged
- Subscribers receive messages even if offline during publish
- Durable consumers track delivery state

### Work Queue Pattern
- Tasks are removed after successful processing
- Prevents duplicate task execution
- Supports multiple workers with load balancing

### Broadcast Pattern
- Multiple consumers receive the same message
- Each consumer has independent delivery tracking
- Useful for announcements and notifications

## Hybrid Bridge Integration

### Files
- **VPS Bridge**: `/opt/mcp-hybrid-bridge.py`
- **Setup Script**: `/opt/setup_nats_streams.py`
- **Test Script**: `/opt/test_nats_delivery.py`

### Redis vs NATS Usage
| Feature | Redis | NATS JetStream |
|---------|-------|----------------|
| State/Cache | Yes | No |
| Presence/Heartbeat | Yes | No |
| Pub/Sub (fire-and-forget) | Yes | No |
| Guaranteed Delivery | No | Yes |
| Task Queue | Limited | Yes |
| Broadcast | Yes | Yes |
| Persistence | No | Yes |

### Connection String
```
nats://admin:blackbox5@77.42.66.40:4222
```

## Testing

Run the delivery test:
```bash
python3 /opt/test_nats_delivery.py
```

Tests verify:
1. Basic publish/subscribe
2. Guaranteed delivery (offline subscriber)
3. Work queue pattern
4. Broadcast to multiple consumers

## Monitoring

Check NATS server status:
```bash
curl http://localhost:8222/jsz
```

View stream info:
```bash
# Via Python
python3 -c "
import asyncio
import nats

async def info():
    nc = await nats.connect('nats://admin:blackbox5@localhost:4222')
    js = nc.jetstream()
    for s in await js.streams_info():
        print(f'{s.config.name}: {s.state.messages} messages')
    await nc.close()

asyncio.run(info())
"
```
