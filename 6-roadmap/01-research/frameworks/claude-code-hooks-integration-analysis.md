# Claude Code Hooks Multi-Agent Observability - BB5 Integration Analysis

**Analysis Date:** 2026-02-10
**Framework:** https://github.com/disler/claude-code-hooks-multi-agent-observability
**Status:** Ready for Implementation

## Executive Summary

This framework provides **real-time multi-agent observability** through Claude Code hooks, a Bun server with SQLite, and a Vue.js dashboard. For BB5, this enables unprecedented visibility into the RALF autonomous execution loop and agent teams.

**Key Integration Value:**
- Real-time monitoring of RALF task execution
- Visual dashboard for autonomous agent operations
- Event tracking for debugging and analytics
- Multi-agent coordination visibility

## Architecture Deep Dive

### 1. Hook System (Client-Side)

**12 Hook Types Implemented:**

| Hook | Purpose | BB5 Value |
|------|---------|-----------|
| `SessionStart` | New session begins | Track RALF iteration start |
| `SessionEnd` | Session terminates | Track task completion |
| `UserPromptSubmit` | User input submitted | Monitor task prompts |
| `PreToolUse` | Before tool execution | Track tool calls |
| `PostToolUse` | After successful tool use | Monitor tool results |
| `PostToolUseFailure` | After failed tool use | Error tracking |
| `PermissionRequest` | Permissions needed | Security monitoring |
| `Notification` | General notifications | Status updates |
| `SubagentStart` | Sub-agent initialized | Track agent teams |
| `SubagentStop` | Sub-agent completed | Agent completion |
| `Stop` | Session stop requested | Emergency stops |
| `PreCompact` | Before context compaction | Memory management |

**Hook Implementation Pattern:**
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["anthropic", "python-dotenv"]
# ///

import json
import sys
from send_event import send_event_to_server

# Read hook data from stdin
input_data = json.load(sys.stdin)

# Send to observability server
send_event_to_server({
    'source_app': 'bb5-ralf',
    'session_id': input_data.get('session_id'),
    'hook_event_type': 'PreToolUse',
    'payload': input_data,
    'timestamp': int(datetime.now().timestamp() * 1000)
})
```

### 2. Server Architecture (Bun + SQLite)

**Components:**
- **HTTP API** (`POST /events`): Receives hook events
- **WebSocket Server**: Broadcasts events to dashboard clients
- **SQLite Database**: WAL mode for high-performance writes
- **Event Processing**: Validation, enrichment, storage

**Database Schema:**
```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_app TEXT NOT NULL,
    session_id TEXT NOT NULL,
    hook_event_type TEXT NOT NULL,
    payload JSON,
    timestamp INTEGER NOT NULL,
    model_name TEXT,
    tool_name TEXT,
    agent_id TEXT,
    -- Additional extracted fields for querying
);

CREATE INDEX idx_session ON events(session_id);
CREATE INDEX idx_timestamp ON events(timestamp);
CREATE INDEX idx_event_type ON events(hook_event_type);
```

### 3. Dashboard (Vue 3 + WebSocket)

**Features:**
- Real-time event stream with color-coded sessions
- Live pulse charts showing agent activity
- Chat transcript viewer with syntax highlighting
- Event filtering by type, session, or agent
- Multi-agent team visualization

**Session Color Coding:**
- Each session gets a unique color
- Visual distinction for parallel agents
- Easy tracking of agent interactions

## BB5 Integration Strategy

### Phase 1: RALF Executor Monitoring (Immediate)

**Goal:** Monitor the autonomous RALF execution loop

**Implementation:**
1. Deploy observability server on VPS (port 4000)
2. Configure hooks in `~/.claude/settings.json`
3. Modify RALF to include session tracking
4. Access dashboard via VPS IP

**Code Changes:**

```python
# ~/.claude/hooks/pre_tool_use.py
#!/usr/bin/env -S uv run --script
import json
import sys
import urllib.request
from datetime import datetime

def send_to_bb5_monitor(event_data):
    """Send event to BB5 observability server"""
    try:
        req = urllib.request.Request(
            'http://localhost:4000/events',
            data=json.dumps(event_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            timeout=2  # Short timeout to not block RALF
        )
        urllib.request.urlopen(req)
    except:
        pass  # Fail silently to not disrupt RALF

# Read from stdin
input_data = json.load(sys.stdin)

# Send event
send_to_bb5_monitor({
    'source_app': 'bb5-ralf',
    'session_id': input_data.get('session_id', 'unknown'),
    'hook_event_type': 'PreToolUse',
    'payload': input_data,
    'timestamp': int(datetime.now().timestamp() * 1000),
    'tool_name': input_data.get('tool_name'),
    'task_context': 'ralf-autonomous'  # BB5-specific context
})
```

**RALF Integration:**
```bash
# In ralf-core.sh, add session tracking
export BB5_SESSION_ID="ralf-$(date +%s)"
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### Phase 2: Multi-Agent Team Visibility (Week 2)

**Goal:** Visualize BB5 agent teams working in parallel

**Implementation:**
1. Configure agent types in settings.json
2. Use SubagentStart/SubagentStop hooks
3. Dashboard shows agent hierarchy
4. Track agent-to-agent communication

**Agent Configuration:**
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "...",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic"
  },
  "agentTeams": {
    "bb5-research": {
      "builder": {
        "model": "glm-4.7",
        "customInstructions": "Research specialist for BB5"
      },
      "validator": {
        "model": "glm-4.7",
        "customInstructions": "Validation specialist for BB5"
      }
    }
  }
}
```

### Phase 3: Redis Integration (Week 3)

**Goal:** Bridge observability with existing Redis status system

**Implementation:**
1. Server writes to both SQLite and Redis
2. Redis pub/sub for real-time updates
3. Maintain existing `ralf:status` key
4. Add new `ralf:events` stream

**Redis Schema:**
```
# Existing
ralf:status -> JSON status object

# New
ralf:events -> Redis Stream (XADD)
ralf:sessions -> Hash of active sessions
ralf:metrics -> Counters and gauges
```

### Phase 4: Advanced Analytics (Week 4)

**Goal:** Task completion analytics and optimization

**Implementation:**
1. Aggregate event data into metrics
2. Track task completion rates
3. Identify bottlenecks
4. Agent performance comparison

**Metrics to Track:**
- Tasks completed per hour
- Average task duration
- Tool usage frequency
- Error rates by task type
- Agent utilization

## Deployment Plan

### VPS Deployment (Recommended)

**Server Setup:**
```bash
# On VPS (77.42.66.40)
cd /opt/blackbox5

# Clone framework
git clone https://github.com/disler/claude-code-hooks-multi-agent-observability.git observability

# Install Bun
curl -fsSL https://bun.sh/install | bash

# Setup server
cd observability/apps/server
bun install

# Create systemd service
sudo tee /etc/systemd/system/bb5-observability.service << 'EOF'
[Unit]
Description=BB5 Observability Server
After=network.target

[Service]
Type=simple
User=bb5-runner
WorkingDirectory=/opt/blackbox5/observability/apps/server
ExecStart=/home/bb5-runner/.bun/bin/bun run src/index.ts
Environment=PORT=4000
Environment=NODE_ENV=production
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable bb5-observability
sudo systemctl start bb5-observability
```

**Dashboard Access:**
```bash
# Build and serve dashboard
cd /opt/blackbox5/observability/apps/client
bun install
bun run build

# Serve via nginx or simple server
sudo tee /etc/nginx/sites-available/bb5-observability << 'EOF'
server {
    listen 80;
    server_name obs.bb5.local;

    location / {
        root /opt/blackbox5/observability/apps/client/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:4000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
    }
}
EOF
```

### Hook Installation

```bash
# Copy hooks to BB5
sudo -u bb5-runner cp -r /opt/blackbox5/observability/.claude/hooks/* ~/.claude/hooks/

# Configure settings
sudo -u bb5-runner tee ~/.claude/settings.json << 'EOF'
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "18849801bb674d08b2df2d27822a5037.aW3s8UbOhKjMRxan",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "OBSERVABILITY_SERVER_URL": "http://localhost:4000/events"
  }
}
EOF
```

## Security Considerations

1. **Server Access:** Bind to localhost only, use SSH tunnel or VPN
2. **API Keys:** Store in environment, not in code
3. **Data Retention:** Implement SQLite cleanup (keep 30 days)
4. **Sensitive Data:** Filter out API keys from event payloads

## Performance Impact

**Hook Overhead:**
- Each hook: ~5-10ms (async HTTP POST)
- Typical task: 50-100 hook events
- Total overhead: <1 second per task

**Mitigation:**
- Fire-and-forget HTTP requests
- 2-second timeout on hook sends
- Fail silently (don't block RALF)
- Optional: Batch events if needed

## Success Metrics

- [ ] Dashboard accessible on VPS
- [ ] Real-time RALF execution visible
- [ ] Task completion tracked
- [ ] Agent teams visualized
- [ ] Error rates monitored
- [ ] Historical analytics available

## Next Steps

1. **Immediate:** Deploy observability server on VPS
2. **Day 2:** Install hooks and test with RALF
3. **Day 3:** Configure dashboard access
4. **Week 2:** Add Redis integration
5. **Week 3:** Implement analytics

## Resources

- **Framework Repo:** https://github.com/disler/claude-code-hooks-multi-agent-observability
- **Documentation:** /tmp/claude-code-hooks-multi-agent-observability/README.md
- **BB5 Framework Doc:** /Users/shaansisodia/blackbox5/6-roadmap/01-research/frameworks/claude-code-hooks-multi-agent-observability.md
