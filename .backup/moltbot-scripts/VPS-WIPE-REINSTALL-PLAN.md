# VPS Wipe & Reinstall Plan

**Date:** 2026-02-07
**Goal:** Clean slate with fresh OpenClaw, keep Redis infrastructure

---

## Phase 1: Backup (Do This First)

### Scripts to Save (Already backed up to laptop)
```
~/.blackbox5/.backup/moltbot-scripts/
├── mcp-server-moltbot.py          ✅ Backed up
├── mcp-redis-bridge.py            ✅ Backed up
└── VPS-WIPE-REINSTALL-PLAN.md     ✅ This file
```

### Redis Bridge on VPS (Keep Running)
```
/opt/openclaw-redis-bridge.js      ✅ Keep this running
```

### Config Files to Backup from VPS
```bash
# Before wiping, save these:
/etc/systemd/system/openclaw-redis-bridge.service
/etc/redis/redis.conf
/opt/moltbot/user-context.json
~/.ssh/authorized_keys
```

---

## Phase 2: What to Wipe

### Delete These Completely
```
/opt/ralf/                    # Old RALF framework
/opt/moltbot/                 # Old Moltbot helpers (save scripts first)
/opt/ralf/5-project-memory/   # Old project memory
```

### Keep These
```
Redis Server (port 6379)      # Message broker
/opt/openclaw-redis-bridge.js # Our bridge
SSH Keys & Config             # Access
```

---

## Phase 3: Fresh OpenClaw Install

### Step 1: Download Latest OpenClaw
```bash
# On VPS (after wipe)
curl -fsSL https://openclaw.dev/install.sh | sh
# OR manually:
# Download from https://github.com/openclaw/openclaw/releases
```

### Step 2: Configure OpenClaw
```bash
# Minimal config for autonomous mode
openclaw config init
openclaw config set telegram.bot_token YOUR_BOT_TOKEN
openclaw config set telegram.user_id 7643203581
```

### Step 3: Restore Redis Bridge
```bash
# Copy back our bridge
cp /opt/openclaw-redis-bridge.js /opt/openclaw-redis-bridge.js.bak  # Just in case
cp ~/.backup/openclaw-redis-bridge.js /opt/openclaw-redis-bridge.js

# Restart service
systemctl restart openclaw-redis-bridge
```

---

## Phase 4: New Architecture

### Proposed Clean Structure
```
/opt/
├── openclaw/                   # Fresh OpenClaw install
│   ├── bin/openclaw           # Main binary
│   ├── config/                # Clean config
│   └── data/                  # OpenClaw data
│
├── blackbox5/                 # Fresh BlackBox5 (git clone)
│   ├── 1-docs/
│   ├── 2-engine/
│   ├── 5-project-memory/      # Start fresh
│   └── bin/
│
├── redis-bridge/              # Our custom stuff
│   ├── openclaw-redis-bridge.js
│   └── moltbot-helpers/
│       ├── mcp-server-moltbot.py
│       └── bb5-query.py
│
└── shared/                    # Shared resources
    ├── logs/
    └── config/
```

---

## Phase 5: Autonomous Moltbot Setup

### What Moltbot Should Do (Fresh Start)
```yaml
Autonomous Capabilities:
  1. Monitor BlackBox5 queue (queue.yaml)
  2. Check agent health (heartbeat)
  3. Send Telegram alerts on issues
  4. Run VPS commands via MCP
  5. Pattern learning from runs

Integration Points:
  - Redis: Agent communication
  - Telegram: User alerts (@SISOlegacybot)
  - MCP: Claude Code integration
  - Filesystem: Read/write queue, events
```

---

## Execution Commands

### Pre-Wipe Backup
```bash
# On VPS
mkdir -p /root/backup-before-wipe
cp /etc/systemd/system/openclaw-redis-bridge.service /root/backup-before-wipe/
cp /etc/redis/redis.conf /root/backup-before-wipe/
cp /opt/moltbot/user-context.json /root/backup-before-wipe/
cp /opt/openclaw-redis-bridge.js /root/backup-before-wipe/
```

### Wipe Commands
```bash
# Stop services
systemctl stop ralf-executor ralf-planner moltbot

# Delete old code
rm -rf /opt/ralf/
rm -rf /opt/moltbot/
rm -rf /opt/blackbox5/  # If exists

# Keep Redis running!
```

### Fresh Install
```bash
# Install OpenClaw
curl -fsSL https://openclaw.dev/install.sh | sh

# Git clone BlackBox5 fresh
git clone https://github.com/Lordsisodia/blackbox5.git /opt/blackbox5

# Restore Redis bridge
cp /root/backup-before-wipe/openclaw-redis-bridge.js /opt/
npm install redis  # In /opt
systemctl start openclaw-redis-bridge
```

---

## Post-Install Verification

```bash
# Test 1: Redis
redis-cli ping
# Expected: PONG

# Test 2: Redis Bridge
ps aux | grep openclaw-redis-bridge
# Expected: Node process running

# Test 3: OpenClaw
openclaw --version
# Expected: Version output

# Test 4: Communication (from laptop)
# Use MCP tool: redis_conversation
# Expected: Response from VPS
```

---

## Questions Before Wipe

1. **Save any data from /opt/ralf/5-project-memory/?**
   - 236 runs history
   - Task completions
   - Or start completely fresh?

2. **Keep Telegram bot token?**
   - @SISOlegacybot
   - Or reconfigure?

3. **OpenClaw version?**
   - Latest stable?
   - Specific version?

4. **BlackBox5 branch?**
   - main?
   - Specific feature branch?

---

## Ready to Execute?

Once you confirm the questions above, run:
```bash
# 1. Backup
# 2. Wipe
# 3. Fresh install
# 4. Verify
```

All scripts are backed up to your laptop at:
`~/.blackbox5/.backup/moltbot-scripts/`
