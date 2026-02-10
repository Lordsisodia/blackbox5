# BB5 Observability Integration Plan

**Status:** Ready for Implementation
**Priority:** High
**Owner:** TBD
**Target:** VPS Deployment + Testing

---

## 1. What We're Building

A workflow tracking system that shows:
- Which BB5 agents are running
- What workflow step they're on
- When tasks start/complete
- Git activity (pushes)

**NOT tracking:** Every tool call, permission request, or internal detail (too noisy)

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  CLAUDE CODE (VPS)                                              │
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │ Your Hooks      │    │ Observability   │                    │
│  │ ─────────────── │    │ Hooks           │                    │
│  │ session-start   │───▶│ ─────────────── │                    │
│  │ agent-teams     │    │ session_start   │──┐                 │
│  │ post-message    │    │ session_end     │  │                 │
│  └─────────────────┘    │ subagent_start  │  │ HTTP POST       │
│                         │ subagent_stop   │  │                 │
│                         │ notification    │──┘                 │
│                         │ pre_compact     │                    │
│                         │ user_prompt     │                    │
│                         │ stop            │                    │
│                         └─────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTP POST to localhost:4000/events
┌─────────────────────────────────────────────────────────────────┐
│  OBSERVABILITY SERVER (Bun + SQLite)                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  • Receive events via HTTP                             │   │
│  │  • Store in SQLite (events.db)                         │   │
│  │  • Broadcast via WebSocket                             │   │
│  │  • Mirror to Redis (optional)                          │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐    ┌─────────────────────────┐
│  SQLITE (Persistence)   │    │  REDIS (Real-time)      │
│  events.db              │    │  bb5:workflow:events    │
└─────────────────────────┘    └─────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  DASHBOARD (Vue.js)                                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  • Real-time workflow cards                             │   │
│  │  • Agent status (working/complete/waiting)             │   │
│  │  • Progress bars for workflows                          │   │
│  │  • Recent activity feed                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. File Locations

### Code Locations

| Component | Location | Notes |
|-----------|----------|-------|
| **Your Hooks** | `.claude/hooks/` | EXISTING - Don't touch |
| **Observability Hooks** | `.claude/hooks/observability/` | NEW - 8 Python scripts |
| **Bun Server** | `engine/infrastructure/observability/server/` | NEW - From framework |
| **SQLite DB** | `5-project-memory/blackbox5/.autonomous/observability/events.db` | Auto-created |
| **Dashboard** | `engine/infrastructure/observability/dashboard/` | Vue app |
| **Start/Stop Scripts** | `bin/observability/` | Helper scripts |
| **Settings** | `.claude/settings.json` | Hook registration |

### Full Paths

```
/Users/shaansisodia/.blackbox5/
├── .claude/
│   ├── hooks/
│   │   ├── session-start-agent-teams.sh     # YOURS - Keep
│   │   ├── post-message-agent-teams.sh      # YOURS - Keep
│   │   └── observability/                   # NEW
│   │       ├── __init__.py
│   │       ├── session_start.py
│   │       ├── session_end.py
│   │       ├── subagent_start.py
│   │       ├── subagent_stop.py
│   │       ├── notification.py
│   │       ├── pre_compact.py
│   │       ├── user_prompt_submit.py
│   │       ├── stop.py
│   │       └── send_event.py              # Shared HTTP sender
│   └── settings.json                        # NEW - Hook registration
│
├── engine/infrastructure/observability/
│   ├── server/                              # Bun server from framework
│   │   ├── src/
│   │   │   ├── index.ts                   # Main server
│   │   │   ├── db.ts                      # SQLite operations
│   │   │   └── types.ts                   # TypeScript types
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── dashboard/                           # Vue dashboard from framework
│       ├── src/
│       ├── dist/                          # Built files
│       └── package.json
│
├── 5-project-memory/blackbox5/.autonomous/observability/
│   └── events.db                            # SQLite database (auto-created)
│
└── bin/observability/
    ├── start-server.sh                      # Start Bun server
    ├── stop-server.sh                       # Stop Bun server
    ├── status.sh                            # Check if running
    └── test-hook.sh                         # Test hook manually
```

---

## 4. Hook Integration Strategy

### Option 1: Chain Hooks (RECOMMENDED)

Your existing hook calls observability at the end:

```bash
# .claude/hooks/session-start-agent-teams.sh (your existing)

# ... your existing code ...

# At the very end, add:
# Send to observability (non-blocking, ignore errors)
echo "{
  \"session_id\": \"$RUN_ID\",
  \"agent_type\": \"${CLAUDE_CODE_AGENT_TYPE:-unknown}\",
  \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"
}" | ~/.claude/hooks/observability/session_start.py 2>/dev/null || true
```

**Pros:** Simple, keeps your logic separate
**Cons:** Your hook modified (but minimally)

### Option 2: Wrapper Hook

Create a master hook that calls both:

```bash
# .claude/hooks/session-start-master.sh
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run your hook first
"$SCRIPT_DIR/session-start-agent-teams.sh"

# Run observability
cat | "$SCRIPT_DIR/observability/session_start.py"
```

**Pros:** Your hooks untouched
**Cons:** More complex, Claude only calls one hook per event

### Option 3: Merge Into Your Hooks

Add observability code directly to your existing hooks.

**Pros:** Single hook per event
**Cons:** Tight coupling

---

## 5. Settings.json Configuration

Create `.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "18849801bb674d08b2df2d27822a5037.aW3s8UbOhKjMRxan",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "OBSERVABILITY_SERVER_URL": "http://localhost:4000/events"
  },
  "hooks": {
    "SessionStart": "session-start-agent-teams.sh",
    "PostMessage": "post-message-agent-teams.sh",
    "SessionEnd": "observability/session_end.py",
    "SubagentStart": "observability/subagent_start.py",
    "SubagentStop": "observability/subagent_stop.py",
    "Notification": "observability/notification.py",
    "PreCompact": "observability/pre_compact.py",
    "UserPromptSubmit": "observability/user_prompt_submit.py",
    "Stop": "observability/stop.py"
  }
}
```

---

## 6. Implementation Checklist

### Phase 1: Copy Framework (30 min)
- [ ] Clone framework to `/tmp`
- [ ] Copy to `engine/infrastructure/observability/`
- [ ] Remove unnecessary hooks (keep only 8)
- [ ] Verify directory structure

### Phase 2: Configure Hooks (30 min)
- [ ] Create `.claude/hooks/observability/` directory
- [ ] Copy 8 hook scripts
- [ ] Modify `send_event.py` for BB5 context
- [ ] Test one hook manually

### Phase 3: Integrate with Your Hooks (30 min)
- [ ] Modify `session-start-agent-teams.sh` to call observability
- [ ] Modify `post-message-agent-teams.sh` to call observability
- [ ] Create `.claude/settings.json`
- [ ] Test hook chain

### Phase 4: Deploy Server (30 min)
- [ ] Install Bun on VPS
- [ ] Install dependencies
- [ ] Create systemd service
- [ ] Start server
- [ ] Verify server running

### Phase 5: Test (30 min)
- [ ] Run manual hook test
- [ ] Start RALF and watch events
- [ ] Check SQLite has data
- [ ] Access dashboard
- [ ] Verify real-time updates

---

## 7. Testing Strategy

### Test 1: Manual Hook Test

```bash
# On VPS, test a hook manually
cat << 'EOF' | python3 ~/.claude/hooks/observability/session_start.py
{
  "session_id": "test-session-001",
  "agent_type": "test-agent",
  "source": "test"
}
EOF

# Check if server received it
curl http://localhost:4000/events/recent
```

**Expected:** Server returns the test event

### Test 2: Server Health Check

```bash
# Check server is running
curl http://localhost:4000/health

# Expected: {"status": "ok", "events_count": N}
```

### Test 3: Hook Chain Test

```bash
# Test your hook still works and calls observability
~/.claude/hooks/session-start-agent-teams.sh

# Check:
# 1. Your run directory created
# 2. Event in SQLite
# 3. No errors in logs
```

### Test 4: RALF Integration Test

```bash
# Start RALF
sudo systemctl start bb5-ralf-executor

# Watch for events
watch -n 2 'curl -s http://localhost:4000/events/recent | head -20'

# Expected: See RALF session events flowing
```

### Test 5: Dashboard Test

```bash
# Open dashboard
open http://77.42.66.40:4000

# Or via SSH tunnel
ssh -L 4000:localhost:4000 root@77.42.66.40
open http://localhost:4000
```

**Expected:** See workflow cards, agent status, recent events

### Test 6: Redis Bridge Test (if enabled)

```bash
# Check Redis has events
redis-cli XREAD STREAMS bb5:workflow:events 0

# Expected: List of events
```

---

## 8. Deployment Commands

### One-Time Setup

```bash
# 1. Copy framework to BB5
cp -r /tmp/claude-code-hooks-multi-agent-observability \
  /Users/shaansisodia/.blackbox5/engine/infrastructure/observability

# 2. Create hook directory
mkdir -p /Users/shaansisodia/.blackbox5/.claude/hooks/observability

# 3. Copy selected hooks
cd /Users/shaansisodia/.blackbox5/engine/infrastructure/observability/.claude/hooks
cp session_start.py session_end.py subagent_start.py subagent_stop.py \
   notification.py pre_compact.py user_prompt_submit.py stop.py send_event.py \
   /Users/shaansisodia/.blackbox5/.claude/hooks/observability/

# 4. Create settings.json
cat > /Users/shaansisodia/.blackbox5/.claude/settings.json << 'JSON'
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "18849801bb674d08b2df2d27822a5037.aW3s8UbOhKjMRxan",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "OBSERVABILITY_SERVER_URL": "http://localhost:4000/events"
  },
  "hooks": {
    "SessionStart": "session-start-agent-teams.sh",
    "PostMessage": "post-message-agent-teams.sh",
    "SessionEnd": "observability/session_end.py",
    "SubagentStart": "observability/subagent_start.py",
    "SubagentStop": "observability/subagent_stop.py",
    "Notification": "observability/notification.py",
    "PreCompact": "observability/pre_compact.py",
    "UserPromptSubmit": "observability/user_prompt_submit.py",
    "Stop": "observability/stop.py"
  }
}
JSON
```

### VPS Deployment

```bash
# On VPS (77.42.66.40)

# 1. Copy from local to VPS
scp -r /Users/shaansisodia/.blackbox5/engine/infrastructure/observability \
  root@77.42.66.40:/opt/blackbox5/engine/infrastructure/

scp -r /Users/shaansisodia/.blackbox5/.claude/hooks/observability \
  root@77.42.66.40:/opt/blackbox5/.claude/hooks/

scp /Users/shaansisodia/.blackbox5/.claude/settings.json \
  root@77.42.66.40:/opt/blackbox5/.claude/

# 2. Install Bun
curl -fsSL https://bun.sh/install | bash

# 3. Install server dependencies
cd /opt/blackbox5/engine/infrastructure/observability/apps/server
~/.bun/bin/bun install

# 4. Create systemd service
cat > /etc/systemd/system/bb5-observability.service << 'EOF'
[Unit]
Description=BB5 Observability Server
After=network.target

[Service]
Type=simple
User=bb5-runner
WorkingDirectory=/opt/blackbox5/engine/infrastructure/observability/apps/server
Environment=PORT=4000
Environment=NODE_ENV=production
Environment=BB5_DIR=/opt/blackbox5
ExecStart=/home/bb5-runner/.bun/bin/bun run src/index.ts
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 5. Start server
systemctl daemon-reload
systemctl enable bb5-observability
systemctl start bb5-observability

# 6. Check status
systemctl status bb5-observability
curl http://localhost:4000/health
```

---

## 9. Troubleshooting

### Server Won't Start

```bash
# Check logs
journalctl -u bb5-observability -f

# Check port in use
lsof -i :4000

# Test manually
cd /opt/blackbox5/engine/infrastructure/observability/apps/server
~/.bun/bin/bun run src/index.ts
```

### Hooks Not Firing

```bash
# Check settings.json syntax
python3 -m json.tool ~/.claude/settings.json

# Test hook manually
echo '{"session_id": "test"}' | python3 ~/.claude/hooks/observability/session_start.py

# Check Claude Code sees hooks
claude config get hooks
```

### No Events in Dashboard

```bash
# Check SQLite directly
sqlite3 /opt/blackbox5/5-project-memory/blackbox5/.autonomous/observability/events.db \
  "SELECT * FROM events ORDER BY timestamp DESC LIMIT 10;"

# Check server received events
curl http://localhost:4000/events/count
```

---

## 10. Next Steps

1. **Review this plan** - Any changes needed?
2. **Decide on Option 1 or 2** for hook integration
3. **Test locally first** - Before VPS deployment
4. **Deploy to VPS** - Using commands above
5. **Run test suite** - All 6 tests passing?
6. **Document learnings** - Update this doc

---

## 11. Questions to Resolve

- [ ] Which hook integration option? (1 or 2)
- [ ] Redis bridge needed or SQLite only?
- [ ] Dashboard port? (4000 or 80/443 via nginx)
- [ ] Data retention? (keep 30 days?)
- [ ] Access control? (VPN only or public?)

---

**Document Version:** 1.0
**Last Updated:** 2026-02-10
**Ready for Review:** Yes
