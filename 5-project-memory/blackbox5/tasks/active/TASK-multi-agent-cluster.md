# TASK-CLUSTER-001: Implement Multi-Agent Cluster Support

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-07
**Agent:** TBD

## Objective

Extend the Redis agent communication bridge to support a multi-agent cluster including Mac Mini as a third agent, with general broadcast capabilities, agent discovery, and presence/heartbeat systems.

## Success Criteria

- [ ] Mac Mini integrated as third agent in cluster
- [ ] General broadcast channel `agents:general` operational
- [ ] Agent discovery protocol designed and implemented
- [ ] Agent presence/heartbeat system active
- [ ] Documentation updated with cluster architecture

## Context

Currently we have 2 agents communicating via Redis:
1. **Claude Code** (Mac Local) - MCP bridge
2. **OpenClaw** (VPS) - Node.js bridge

We need to add:
3. **Mac Mini** (Local Network) - New agent

## Approach

### Phase 1: Mac Mini Integration

1. Install Redis client on Mac Mini
2. Deploy agent bridge (Python or Node.js)
3. Configure unique agent ID: `macmini-01`
4. Test bidirectional communication

### Phase 2: Broadcast Channel

1. Create `agents:general` pub/sub channel
2. Implement broadcast message format
3. Add broadcast tools to all agents
4. Test multi-agent message delivery

### Phase 3: Discovery Protocol

Design protocol for agents to:
- Announce presence on startup
- Query for available agents
- Share capabilities
- Handle agent departure

Proposed channel pattern:
```
agents:discovery:announce  - New agent announcements
agents:discovery:query     - Discovery requests
agents:discovery:response  - Discovery replies
```

### Phase 4: Heartbeat System

Implement presence tracking:
- Heartbeat interval: 30 seconds
- Timeout threshold: 90 seconds
- Redis key: `agent:{id}:heartbeat`
- Presence list: `agents:active` (Redis set)

Message format:
```json
{
  "from": "agent-id",
  "type": "heartbeat",
  "timestamp": "2026-02-07T12:00:00Z",
  "capabilities": ["task_execution", "file_ops", "git"],
  "status": "ready|busy|offline"
}
```

## Technical Design

### Channel Architecture

```
# Direct messaging
agent:{id}:messages        # Per-agent inbox

# Broadcast
agents:general             # All agents receive
agents:events              # System events only

# Discovery
agents:discovery:announce  # New agent joins
agents:discovery:query     # Who is available?
agents:discovery:response  # I am here

# Presence
agent:{id}:heartbeat       # TTL-based presence
agents:active              # Set of active agents
```

### Agent Registry (Redis)

```
HSET agent:claude-code \
  id "claude-code" \
  host "mac-local" \
  type "mcp-bridge" \
  capabilities "[task_execution,file_ops,git]" \
  last_seen "2026-02-07T12:00:00Z"

SADD agents:active "claude-code"
EXPIRE agent:claude-code:heartbeat 90
```

### Mac Mini Bridge

Options:
1. **Python MCP** (same as Claude Code)
2. **Node.js** (same as OpenClaw)
3. **Standalone** (direct Redis client)

Recommended: Node.js for consistency with OpenClaw.

## Implementation Tasks

### Task 1: Mac Mini Setup
- [ ] SSH access configured
- [ ] Node.js installed
- [ ] Redis client installed (`npm install redis`)
- [ ] Bridge script deployed
- [ ] Service configured (launchd)

### Task 2: Broadcast System
- [ ] Update `mcp-redis-bridge.py` with broadcast tool
- [ ] Update `openclaw-redis-bridge.js` with broadcast handler
- [ ] Create Mac Mini bridge with broadcast support
- [ ] Test 3-way broadcast

### Task 3: Discovery Protocol
- [ ] Implement announce on startup
- [ ] Add query/response handlers
- [ ] Create agent registry functions
- [ ] Test discovery flow

### Task 4: Heartbeat System
- [ ] Implement heartbeat publisher
- [ ] Create presence monitor
- [ ] Add agent timeout detection
- [ ] Build status dashboard

## Rollback Strategy

1. Stop new bridges
2. Revert to direct Claude ↔ OpenClaw channels
3. Disable broadcast processing
4. Keep individual agent channels isolated

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `~/.blackbox5/mcp-redis-bridge.py` | Modify | Add broadcast, discovery tools |
| `/opt/openclaw-redis-bridge.js` | Modify | Add broadcast, heartbeat |
| `/opt/macmini-bridge.js` | Create | New agent bridge |
| `~/Library/LaunchAgents/com.blackbox5.macmini-bridge.plist` | Create | Mac Mini service |
| `knowledge/multi-agent-cluster.md` | Create | Documentation |

## Dependencies

- Redis server (existing)
- Node.js on Mac Mini
- SSH access to Mac Mini
- Network connectivity (all agents)

## Estimated Effort

- Phase 1 (Mac Mini): 2 hours
- Phase 2 (Broadcast): 1 hour
- Phase 3 (Discovery): 2 hours
- Phase 4 (Heartbeat): 2 hours
- **Total: 7 hours**

## Next Steps

1. Confirm Mac Mini SSH credentials
2. Choose bridge implementation (Node.js recommended)
3. Begin Phase 1: Mac Mini integration
4. Update architecture docs as phases complete
