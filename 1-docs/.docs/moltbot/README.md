# Moltbot Research Documentation

**Previously:** Claudebot → Moltbot → **OpenClaw** (current)

## What is Moltbot/OpenClaw?

**OpenClaw** (formerly Moltbot, originally Clawdbot) is an **open-source, self-hosted AI assistant framework** designed to function as a 24/7 "Jarvis-style" personal AI agent. Unlike traditional chatbots that only respond to questions, OpenClaw uses autonomous agents that can take actions on your behalf.

### Name Evolution

| Date | Name | Reason |
|------|------|--------|
| Jan 2026 | **Clawdbot** | Original name |
| Jan 27, 2026 | **Moltbot** | Trademark concerns with Anthropic's Claude; symbolized transformation |
| Jan 30, 2026 | **OpenClaw** | Final stable branding |

### Quick Facts

- **npm package:** `openclaw` (MIT license)
- **Node.js:** ≥ 22 required
- **GitHub:** https://github.com/openclaw/openclaw
- **Website:** https://openclaw.ai
- **Community:** 100,000+ GitHub stars, 1,700+ community skills

## Core Capabilities

### Autonomous Features

- **24/7 Operation** - Runs as persistent daemon, not CLI tool
- **Proactive Execution** - Can initiate actions without user prompts
- **Persistent Memory** - Retains context across sessions in local files
- **Multi-Channel** - WhatsApp, Telegram, Discord, Slack, iMessage, Signal
- **Tool Execution** - Shell commands, browser automation, file manipulation
- **Continuous Monitoring** - Directory watching, server uptime checks

### What Makes It Different from Chatbots

| Feature | Traditional Chatbot | OpenClaw |
|---------|-------------------|----------|
| Session | Ephemeral | Persistent |
| Memory | Per-conversation | Long-term |
| Initiative | Reactive only | Proactive |
| Channels | Single | Multiple |
| Tools | Limited | Extensible via skills |
| Execution | Cloud | Local/VPS |

## Architecture

### Four-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  INTEGRATION LAYER                                          │
│  WhatsApp • Telegram • Discord • Slack • iMessage • Signal  │
├─────────────────────────────────────────────────────────────┤
│  REASONING LAYER                                            │
│  LLMs: Claude • GPT-4 • Gemini • Local (Ollama)             │
├─────────────────────────────────────────────────────────────┤
│  MEMORY LAYER                                               │
│  Vector-based long-term memory • User preferences           │
├─────────────────────────────────────────────────────────────┤
│  EXECUTION LAYER                                            │
│  Shell commands • Browser automation • File operations      │
└─────────────────────────────────────────────────────────────┘
```

### Gateway (Port 18789)

The Gateway is the central nervous system:

- **Multiplexed port** - Handles WebSocket + HTTP on port 18789
- **WebSocket** - Primary control plane, real-time bidirectional RPC
- **HTTP** - Control UI, webhooks, MCP servers, OpenAI-compatible endpoints
- **MCP Integration** - Via plugin architecture

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

## Skills System

Skills are reusable JavaScript/TypeScript modules that extend functionality:

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

### Installing Skills

```bash
clawd install [skill-name]           # From ClawdHub
clawd install github:username/repo   # From GitHub
clawd install ./path/to/skill        # Local
```

### Community Resources

- **ClawdHub** (clawd-hub.org) - Official skill registry
- **awesome-openclaw-skills** - GitHub community collection
- **1,700+** community-built skills available

## Commands

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

## Configuration

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

## Real-World Use Cases

1. **Daily Ops Sweep** - Collect status from multiple sources, summarize, ping people
2. **Morning Intelligence Briefs** - Scheduled daily briefings with news, weather, stocks
3. **Vibe Coding** - Implements features, creates PRs, fixes bugs via GitHub
4. **Email Management** - Sorts inbox, drafts replies, sends emails
5. **Browser Automation** - Researches topics, fills forms, monitors prices
6. **Customer Support Triage** - Ingest tickets, pull docs, draft responses

## Cost Comparison

| Model Provider | Estimated Monthly Cost |
|---------------|----------------------|
| Claude Opus 4.5 | ~$200 |
| GPT-4o | ~$100 |
| Minimax (budget) | ~$10 |
| Local models (Ollama) | Free |

## Security Considerations

⚠️ **High-risk if not properly sandboxed** - Deep system access (terminal, file deletion)

**Best Practices:**
- Don't run on production hardware
- Use dedicated user accounts with limited sudo
- Never expose Gateway to public internet without auth
- Use SSH tunnels or Tailscale for remote access
- Default pairing mode requires approval for unknown contacts

**Sandboxed Options:**
- **Cloudflare Moltworker** - Runs on Cloudflare Workers with sandboxing
- **Docker deployment** - Containerized isolation

## Documentation Structure

| File | Description |
|------|-------------|
| [README.md](README.md) | This file - Overview and introduction |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Deep dive into system components |
| [RESEARCH-LOG.md](RESEARCH-LOG.md) | Research notes and findings |
| [OPENCLAW-RESEARCH.md](OPENCLAW-RESEARCH.md) | OpenClaw framework details |
| [MCP-PROTOCOL.md](MCP-PROTOCOL.md) | MCP protocol implementation |
| [TELEGRAM-BOT.md](TELEGRAM-BOT.md) | Telegram Bot integration |
| [FILE-REFERENCE.md](FILE-REFERENCE.md) | Complete file reference |

### Comparison & Integration Research

| File | Description |
|------|-------------|
| [BLACKBOX5-VS-OPENCLAW.md](BLACKBOX5-VS-OPENCLAW.md) | Deep dive comparison between Blackbox5 and OpenClaw architectures |
| [HYBRID-INTEGRATION.md](HYBRID-INTEGRATION.md) | Guide for integrating Blackbox5 with OpenClaw |
| [SKILL-SYSTEMS-COMPARISON.md](SKILL-SYSTEMS-COMPARISON.md) | Comparison of skill systems: Anthropic vs Blackbox5 vs OpenClaw |

## Sources

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
