# VPS to Mac Mini Migration Status

## Completed ✅

### 1. SSH Access
- ✅ Mac Mini accessible via `ssh mac-mini` (Tailscale)
- ✅ SSH key authentication configured
- ✅ IP: 100.66.34.21

### 2. OpenClaw Configuration
- ✅ All SOUL MDs migrated:
  - `~/.openclaw/agents/general/SOUL.md`
  - `~/.openclaw/agents/content/SOUL.md`
  - `~/.openclaw/agents/engineering/SOUL.md`
  - `~/.openclaw/agents/task-agent/SOUL.md`
- ✅ Telegram configuration migrated:
  - `~/.openclaw/credentials/telegram-allowFrom.json`
  - `~/.openclaw/telegram/` (update offsets)
- ✅ Main OpenClaw config:
  - `~/.openclaw/openclaw.json` (44KB)
  - `~/.openclaw/groups/` (all group configs)
  - `~/.openclaw/skills/` (all skills)
  - `~/.openclaw/workspace/` (workspace files)

### 3. MoltBot Files
- ✅ MoltBot application copied to `~/Projects/moltbot/`
- ✅ Logs preserved in `~/Projects/moltbot/logs/`
- ✅ Agent configs in `~/Projects/moltbot/agents/`

### 4. YouTube Pipeline
- ✅ Repository cloned to `~/Projects/youtube-ai-research/`
- ✅ Python venv created with dependencies
- ✅ Queue database with 7,814 videos
- ✅ Analysis scripts installed

## Pending ⏳

### 1. OpenClaw Installation
**Status:** Needs admin privileges

OpenClaw is a Node.js application that needs to be installed:
```bash
# On Mac Mini, run manually:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install node
npm install -g openclaw
```

### 2. MoltBot Service
**Status:** Needs OpenClaw first

Once OpenClaw is installed, create the LaunchAgent:
```bash
# Create plist file
cat > ~/Library/LaunchAgents/com.siso.moltbot.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.siso.moltbot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/openclaw</string>
        <string>gateway</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/shaansisodia/Projects/moltbot</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>HOME</key>
        <string>/Users/shaansisodia</string>
        <key>OPENCLAW_CONFIG</key>
        <string>/Users/shaansisodia/.openclaw</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/shaansisodia/Projects/moltbot/logs/moltbot.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/shaansisodia/Projects/moltbot/logs/moltbot-error.log</string>
</dict>
</plist>
EOF

# Load it
launchctl load ~/Library/LaunchAgents/com.siso.moltbot.plist
```

### 3. MCP Configuration Update
**Status:** Needs to be updated for Mac Mini paths

Current `~/.blackbox5/.mcp-moltbot.json` points to VPS paths. Update to:
```json
{
  "mcpServers": {
    "moltbot-macmini": {
      "type": "stdio",
      "command": "python3",
      "args": [
        "/Users/shaansisodia/.blackbox5/mcp-server-moltbot.py"
      ]
    }
  }
}
```

## Migration Checklist

- [x] SSH access configured
- [x] OpenClaw config files copied
- [x] SOUL MDs preserved
- [x] Telegram settings migrated
- [x] MoltBot files copied
- [ ] Install Homebrew (needs admin)
- [ ] Install Node.js (needs Homebrew)
- [ ] Install OpenClaw (needs Node.js)
- [ ] Set up MoltBot LaunchAgent
- [ ] Test Telegram bot
- [ ] Update MCP configs
- [ ] Start YouTube worker
- [ ] Verify all services

## Files Migrated

### From VPS /root/.openclaw/
```
~/.openclaw/
├── agents/
│   ├── content/SOUL.md
│   ├── engineering/SOUL.md
│   ├── general/SOUL.md
│   └── task-agent/SOUL.md
├── credentials/
│   └── telegram-allowFrom.json
├── groups/
├── skills/
├── telegram/
├── workspace/
└── openclaw.json
```

### From VPS /opt/moltbot/
```
~/Projects/moltbot/
├── agents/
├── logs/
├── shared/
├── capture-topics.js
└── task-agent-openclaw.json
```

### From VPS /opt/blackbox5/
```
~/.blackbox5/ (already existed, configs merged)
```

## Next Steps

1. **On Mac Mini (manual):**
   ```bash
   # Install Homebrew (requires password)
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Install Node.js
   brew install node

   # Install OpenClaw
   npm install -g openclaw

   # Test OpenClaw
   openclaw --version
   ```

2. **Set up MoltBot service:**
   ```bash
   # Create LaunchAgent plist (see above)
   # Load it
   launchctl load ~/Library/LaunchAgents/com.siso.moltbot.plist
   ```

3. **Start YouTube worker:**
   ```bash
   cd ~/Projects/youtube-ai-research
   ./start-worker.sh
   ```

4. **Test everything:**
   ```bash
   # From your laptop
   ssh mac-mini "tail -f ~/Projects/moltbot/logs/moltbot.log"
   ```

## Rollback Plan

If issues arise:
1. Keep VPS running (already doing this)
2. VPS IP: 77.42.66.40
3. Can switch back by updating Telegram webhook or MCP configs

## Notes

- All critical configuration files are preserved
- The Mac Mini has all the data, just needs OpenClaw installed
- YouTube pipeline is ready to run (just needs worker started)
- Telegram bot will work once OpenClaw is running
