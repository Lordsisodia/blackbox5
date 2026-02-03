# Moltbot Research Log

## 2026-02-04 - Initial Research (Codebase)

### Sources Reviewed

1. **mcp-server-moltbot.py** - MCP server implementation
   - Uses SSH to connect to VPS (77.42.66.40)
   - Provides 5 tools: get_status, send_message, get_ralf_status, get_user_context, run_command
   - Runs locally on MacBook, executes commands remotely

2. **moltbot-ralf-architecture.md** - Architecture documentation
   - Comprehensive system diagram
   - Communication patterns explained
   - MCP setup instructions
   - Security notes

3. **moltbot-setup.sh** - VPS deployment script
   - Installs OpenClaw (npm package)
   - Creates RALF status skill
   - Sets up systemd service
   - Configures cron jobs for monitoring

## 2026-02-04 - Internet Research (What is Moltbot/OpenClaw)

### Name Evolution

- **Clawdbot** (original name, January 2026) → trademark concerns with Anthropic's Claude
- **Moltbot** (interim name, January 27, 2026) → symbolized transformation/growth
- **OpenClaw** (current name, January 30, 2026) → final stable branding

### What is OpenClaw?

**OpenClaw** is an **open-source, self-hosted AI assistant framework** that functions as a 24/7 "Jarvis-style" personal AI agent. Unlike traditional chatbots, it uses autonomous agents that can take actions on your behalf.

**npm package:** `openclaw` (MIT license, Node.js ≥ 22 required)

**GitHub:** https://github.com/openclaw/openclaw

**Website:** https://openclaw.ai / https://openclaw.my

### Core Architecture

| Layer | Function |
|-------|----------|
| **Reasoning Layer** | Powered by LLMs (Claude, GPT-4, local LLMs via Ollama) |
| **Memory Layer** | Vector-based long-term memory for context and preferences |
| **Execution Layer** | Shell commands, browser automation, file manipulation |
| **Integration Layer** | WhatsApp, Telegram, Discord, Slack, iMessage, Signal |

### Gateway (Port 18789)

The Gateway is the central nervous system:

- **Multiplexed port** - Handles both WebSocket and HTTP on port 18789
- **WebSocket** - Primary control plane, real-time bidirectional RPC
- **HTTP** - Control UI, webhooks, MCP servers, OpenAI-compatible endpoints
- **MCP Integration** - Via plugin architecture (stdio/HTTP bridge)

### How 24/7 Autonomous Mode Works

1. **Persistent Daemon Process**
   - Runs as `gateway daemon` on local machine or VPS
   - Automatically restarts on system boot
   - Maintains long-term memory in `~/.openclaw/workspace`

2. **Heartbeat Engine**
   - Periodic judgment rather than rigid cron schedules
   - Checks conditions at intervals, acts when thresholds are met

3. **Multi-Channel Connectivity**
   - Maintains persistent connections to messaging platforms
   - You can text your agent from your phone
   - It executes tasks on your server while retaining weeks of context

### Skills System

Skills are reusable JavaScript/TypeScript modules:

```javascript
export default {
  name: "my-custom-skill",
  description: "What this skill does",
  triggers: [
    { pattern: /remind me to (.+)/i, handler: "setReminder" }
  ],
  async setReminder(context, match) {
    const reminder = match[1];
    return `I'll remind you to ${reminder}`;
  }
}
```

**Installing Skills:**
```bash
clawd install [skill-name]           # From ClawdHub
clawd install github:username/repo   # From GitHub
clawd install ./path/to/skill        # Local
```

**Community Skills Registry:**
- ClawdHub (clawd-hub.org)
- awesome-openclaw-skills GitHub repo
- 1,700+ community-built skills

### Key Autonomous Capabilities

- **Continuous Monitoring** - Directory watching, server uptime checks
- **Self-Initiated Actions** - Messages you first when conditions are met
- **Tool Execution** - Shell commands, file operations, browser automation
- **Memory Persistence** - Learns preferences across conversations
- **Proactive Agent** - Can reach out to users autonomously

### Real-World Use Cases

1. **Daily Ops Sweep** - Collect status, summarize, ping people
2. **Morning Intelligence Briefs** - Scheduled daily briefings with news, weather, stocks
3. **Vibe Coding** - Implements features, creates PRs, fixes bugs
4. **Email Management** - Sorts inbox, drafts replies
5. **Browser Automation** - Researches topics, fills forms, monitors prices

### Security Considerations

⚠️ **High-risk if not properly sandboxed** - Deep system access (terminal, file deletion)

**Best Practices:**
- Don't run on production hardware
- Use dedicated user accounts with limited sudo
- Never expose Gateway to public internet without auth
- Use SSH tunnels or Tailscale for remote access
- Default pairing mode requires approval for unknown contacts

**Cloudflare Moltworker** - Sandboxed deployment option using Cloudflare Workers

### Cost Comparison

| Model Provider | Estimated Monthly Cost |
|---------------|----------------------|
| Claude Opus 4.5 | ~$200 |
| GPT-4o | ~$100 |
| Minimax (budget) | ~$10 |
| Local models (Ollama) | Free |

### Commands

```bash
# Install
npm install -g openclaw@latest

# Start gateway
openclaw gateway --port 18789 --verbose

# Onboarding wizard
openclaw onboard --install-daemon

# Send message
openclaw message send --to +1234567890 --message "Hello"

# Talk to agent
openclaw agent --message "Ship checklist" --thinking high

# Install skill
clawd install [skill-name]
```

### Configuration File

**~/.openclaw/openclaw.json:**
```json
{
  "agent": {
    "model": "anthropic/claude-sonnet-4-5",
    "baseUrl": "https://api.z.ai/api/anthropic"
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN"
    }
  },
  "skills": {
    "skill-name": {
      "enabled": true,
      "path": "/path/to/skill.js"
    }
  },
  "gateway": {
    "port": 18789,
    "host": "0.0.0.0",
    "auth": {
      "mode": "token",
      "token": "your-secret-token"
    }
  }
}
```

### Sources

- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw npm package](https://www.npmjs.com/package/openclaw)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Clawdbot Complete Guide](https://www.jitendrazaa.com/blog/ai/clawdbot-complete-guide-open-source-ai-assistant-2026/)
- [OpenClaw Use Cases](https://research.aimultiple.com/moltbot/)
- [Moltbot Wiki](https://moltbotwiki.org/)
- [OpenClaw 24/7 Operation](https://amirteymoori.com/openclaw-clawdbot-moltbot-ai-llm-agent/)
- [OpenClaw Skills](https://moltbotwiki.com/skills.html)
- [Claude Cowork vs Moltbot](https://codeagni.com/blog-details?slug=claude-cowork-vs-moltbot-openclaw-in-2026-ai-tools-that-changed-how-we-work)
- [OpenClaw Security](https://hunto.ai/blog/moltbot-security/)
- [Cloudflare Moltworker](https://github.com/cloudflare/moltworker)

## Key Insights

### What Makes It Autonomous

1. **Daemon Architecture** - Runs as persistent background service, not CLI tool
2. **Memory Persistence** - Retains context across sessions in local files
3. **Proactive Execution** - Can initiate actions without user prompts
4. **Multi-Channel** - Always listening on Telegram/WhatsApp/Discord
5. **Heartbeat Engine** - Makes periodic judgments, not just reactive

### Difference from Regular Chatbots

| Feature | Traditional Chatbot | OpenClaw |
|---------|-------------------|----------|
| Session | Ephemeral | Persistent |
| Memory | Per-conversation | Long-term |
| Initiative | Reactive only | Proactive |
| Channels | Single | Multiple |
| Tools | Limited | Extensible via skills |
| Execution | Cloud | Local/VPS |

### How It Relates to RALF

Based on the architecture, OpenClaw provides:
- **Gateway infrastructure** for MCP connections
- **Telegram interface** for notifications
- **Skill system** for custom RALF integrations
- **Daemon process** for 24/7 operation

RALF appears to use OpenClaw as the underlying infrastructure for:
- Receiving task updates via Telegram
- Exposing MCP endpoints for Claude Code
- Running persistent background processes
- File-based communication bridge

## Research Areas

### Completed
- [x] OpenClaw framework research
- [x] npm package details
- [x] 24/7 autonomous operation
- [x] Skills system
- [x] Gateway architecture

### Still Open
- [ ] Specific MCP SSE vs WebSocket clarification
- [ ] RALF-specific integration details
- [ ] Custom skill development for RALF
- [ ] Memory system implementation details
