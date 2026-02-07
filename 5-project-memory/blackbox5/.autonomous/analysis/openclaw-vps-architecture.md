# OpenClaw VPS Architecture Analysis

## Executive Summary

OpenClaw is a multi-agent AI gateway system designed to run as a central manager on a VPS. It provides a WebSocket-based control plane for managing multiple isolated agents across various messaging channels (Telegram, WhatsApp, Discord, Slack, etc.). This document analyzes its architecture and deployment patterns for VPS-based managerial agent scenarios.

---

## 1. OpenClaw Gateway Architecture Overview

### 1.1 Core Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           OPENCLAW GATEWAY ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
│  │   Gateway    │◄──►│   Agent      │◄──►│   Channel    │                   │
│  │   (WebSocket)│    │   Runtime    │    │   Adapters   │                   │
│  │   Port 18789 │    │              │    │              │                   │
│  └──────┬───────┘    └──────────────┘    └──────┬───────┘                   │
│         │                                        │                           │
│         │    ┌──────────────┐                   │                           │
│         └───►│   Session    │◄──────────────────┘                           │
│              │   Store      │                                               │
│              └──────────────┘                                               │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
│  │   Control    │    │   Nodes      │    │   Sandbox    │                   │
│  │   UI (Web)   │    │   (iOS/Mac/  │    │   (Docker)   │                   │
│  │              │    │   Android)   │    │              │                   │
│  └──────────────┘    └──────────────┘    └──────────────┘                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Key Architectural Principles

| Principle | Description |
|-----------|-------------|
| **Single Gateway** | One Gateway per host owns all messaging surfaces and state |
| **WebSocket Control Plane** | All clients connect via WebSocket on port 18789 (default) |
| **Agent Isolation** | Each agent has isolated workspace, auth, and session store |
| **Channel Abstraction** | Normalized message envelope across all channel types |
| **Node Capability Model** | Nodes declare caps/commands/permissions at connect time |

### 1.3 Gateway Responsibilities

- **Message Routing**: Routes inbound messages to appropriate agents via bindings
- **Session Management**: Maintains chat history and routing state per agent
- **Channel Connections**: Manages WhatsApp (Baileys), Telegram (grammY), Slack, Discord, etc.
- **Authentication**: Device-based pairing with token issuance
- **Tool Execution**: Orchestrates tool calls with sandboxing support
- **Presence Tracking**: Tracks connected operators and nodes

---

## 2. VPS Deployment Options

### 2.1 Docker Deployment (Recommended)

The Docker deployment is the preferred method for VPS installations due to isolation and reproducibility.

#### Quick Setup Script
```bash
# From repository root
./docker-setup.sh
```

This script:
1. Builds the gateway image
2. Runs the onboarding wizard
3. Generates a gateway token and writes it to `.env`
4. Starts the gateway via Docker Compose

#### Docker Compose Configuration
```yaml
services:
  openclaw-gateway:
    image: openclaw:local
    build: .
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - HOME=/home/node
      - NODE_ENV=production
      - OPENCLAW_GATEWAY_BIND=${OPENCLAW_GATEWAY_BIND:-lan}
      - OPENCLAW_GATEWAY_PORT=${OPENCLAW_GATEWAY_PORT:-18789}
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}
    volumes:
      - ${OPENCLAW_CONFIG_DIR:-~/.openclaw}:/home/node/.openclaw
      - ${OPENCLAW_WORKSPACE_DIR:-~/.openclaw/workspace}:/home/node/.openclaw/workspace
    ports:
      # Loopback-only for security (access via SSH tunnel)
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"
    command: ["node", "dist/index.js", "gateway", "--bind", "lan"]
```

#### Production VPS (Hetzner Example)

**Environment Variables (.env)**:
```bash
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=<secure-random-token>
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789
OPENCLAW_CONFIG_DIR=/root/.openclaw
OPENCLAW_WORKSPACE_DIR=/root/.openclaw/workspace
GOG_KEYRING_PASSWORD=<keyring-password>
```

**Key Deployment Steps**:
1. Provision VPS (Ubuntu/Debian)
2. Install Docker and Docker Compose
3. Clone OpenClaw repository
4. Create persistent host directories
5. Configure environment variables
6. Bake required binaries into image (Dockerfile)
7. Build and launch with `docker compose up -d`

### 2.2 systemd Deployment

For non-Docker deployments, OpenClaw can run under systemd:

```bash
# Install service
openclaw gateway install --port 18789 --token <token>

# Manage service
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway status
```

### 2.3 Security Best Practices for VPS

| Practice | Implementation |
|----------|----------------|
| **Loopback Binding** | Keep Gateway on `127.0.0.1:18789`, access via SSH tunnel |
| **Token Auth** | Set strong `OPENCLAW_GATEWAY_TOKEN` (32+ chars) |
| **SSH Tunnel** | `ssh -N -L 18789:127.0.0.1:18789 user@vps` |
| **Tailscale** | Alternative to SSH: `gateway.tailscale: serve` or `funnel` |
| **Firewall** | Block port 18789 externally if binding to LAN |
| **Persistent State** | Mount host volumes for `~/.openclaw` and workspace |

---

## 3. Multi-Agent Management Capabilities

### 3.1 Agent Isolation Model

Each agent is a fully scoped "brain" with:

```
~/.openclaw/
├── agents/
│   ├── <agentId>/
│   │   ├── agent/
│   │   │   └── auth-profiles.json    # Per-agent OAuth + API keys
│   │   └── sessions/                 # Chat history + routing state
│   └── ...
├── workspace-<agentId>/              # Agent workspace (files, docs)
└── skills/                           # Shared skills
```

### 3.2 Agent Configuration

```json5
{
  agents: {
    list: [
      {
        id: "home",
        name: "Home Assistant",
        default: true,
        workspace: "~/.openclaw/workspace-home",
        agentDir: "~/.openclaw/agents/home/agent",
        model: "anthropic/claude-sonnet-4-5",
        identity: {
          name: "HomeBot",
          emoji: "🏠",
          theme: "helpful home assistant"
        },
        groupChat: {
          mentionPatterns: ["@home", "@homebot"]
        },
        sandbox: {
          mode: "all",
          scope: "agent"
        },
        tools: {
          allow: ["exec", "read", "write", "sessions_list"],
          deny: ["browser", "canvas"]
        }
      },
      {
        id: "work",
        name: "Work Agent",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
        model: "anthropic/claude-opus-4-6"
      }
    ]
  }
}
```

### 3.3 Routing Bindings

Bindings determine which agent handles incoming messages:

```json5
{
  bindings: [
    // Route by channel + account
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },

    // Route by specific peer (DM or group)
    { agentId: "work", match: { channel: "whatsapp", peer: { kind: "dm", id: "+15551230001" } } },
    { agentId: "family", match: { channel: "whatsapp", peer: { kind: "group", id: "group-id" } } },

    // Route by channel type
    { agentId: "chat", match: { channel: "telegram" } },
    { agentId: "support", match: { channel: "slack" } }
  ]
}
```

**Routing Priority** (most-specific wins):
1. `peer` match (exact DM/group/channel ID)
2. `guildId` (Discord) / `teamId` (Slack)
3. `accountId` match
4. Channel-level match (`accountId: "*"`)
5. Fallback to default agent

### 3.4 Agent-to-Agent Communication

Optional inter-agent messaging (disabled by default):

```json5
{
  tools: {
    agentToAgent: {
      enabled: true,
      allow: ["home", "work"]  // Which agents can message each other
    }
  }
}
```

---

## 4. Integration Patterns for External Agents

### 4.1 WebSocket Protocol

External agents connect via WebSocket and declare capabilities at handshake:

**Connection Flow**:
```
Client                    Gateway
  |                          |
  |---- req:connect -------->|
  |<------ res (ok) ---------|   (hello-ok with protocol version)
  |   (payload includes presence + health snapshot)
  |<------ event:presence ---|
  |<------ event:tick -------|
  |------- req:agent ------->|
  |<------ event:agent ------|   (streaming responses)
```

**Connect Request**:
```json
{
  "type": "req",
  "id": "conn-001",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {
      "id": "external-agent-1",
      "version": "1.0.0",
      "platform": "linux",
      "mode": "node"
    },
    "role": "node",
    "scopes": [],
    "caps": ["exec", "read", "write"],
    "commands": ["exec.run", "file.read", "file.write"],
    "permissions": { "exec.run": true },
    "auth": { "token": "gateway-token" },
    "device": {
      "id": "device-fingerprint",
      "publicKey": "...",
      "signature": "..."
    }
  }
}
```

### 4.2 Node Roles and Capabilities

| Role | Purpose | Typical Caps |
|------|---------|--------------|
| `operator` | Control plane client | `operator.read`, `operator.write`, `operator.admin` |
| `node` | Capability host | `camera`, `canvas`, `screen`, `location`, `voice` |

**Node Capabilities**:
- `camera` - Photo/video capture
- `canvas` - Remote control/UI automation
- `screen` - Screen recording/streaming
- `location` - GPS/location services
- `voice` - Voice wake/interaction

### 4.3 RPC Methods

Key gateway RPC methods for external integration:

| Method | Description |
|--------|-------------|
| `status` | Gateway status and health |
| `config.get` | Retrieve current configuration |
| `config.apply` | Apply full configuration |
| `config.patch` | Partial configuration update |
| `agent` | Send message to agent |
| `send` | Send outbound message |
| `sessions.list` | List active sessions |
| `sessions.history` | Get session history |
| `system-presence` | Get connected devices |
| `exec.approval.resolve` | Resolve pending exec approvals |

---

## 5. Channel/Webhook Configuration

### 5.1 Supported Channels

| Channel | Protocol | Multi-Account | Auth Type |
|---------|----------|---------------|-----------|
| **Telegram** | Bot API (grammY) | Yes | Bot Token |
| **WhatsApp** | Baileys (Web) | Yes | QR Pairing |
| **Discord** | Bot API | Yes | Bot Token |
| **Slack** | Socket Mode | Yes | Bot + App Token |
| **Signal** | signal-cli | Yes | Phone pairing |
| **iMessage** | imsg CLI | Yes | macOS only |
| **Google Chat** | Chat API | Yes | Service Account |
| **Mattermost** | WebSocket | Yes | Bot Token |
| **Microsoft Teams** | Bot Framework | Yes | App credentials |

### 5.2 Telegram Configuration

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "${TELEGRAM_BOT_TOKEN}",
      dmPolicy: "pairing",  // pairing | allowlist | open | disabled
      groups: {
        "-1001234567890": {
          requireMention: true,
          allow: true
        },
        "*": {  // Default for all groups
          requireMention: true
        }
      },
      accounts: {
        default: {
          name: "Primary Bot",
          botToken: "123:abc"
        },
        alerts: {
          name: "Alerts Bot",
          botToken: "987:xyz"
        }
      }
    }
  }
}
```

### 5.3 WhatsApp Configuration

```json5
{
  channels: {
    whatsapp: {
      enabled: true,
      dmPolicy: "pairing",
      allowFrom: ["+15555550123", "+447700900123"],
      groups: {
        "group-id": {
          allow: true,
          requireMention: true
        }
      },
      accounts: {
        personal: {},
        biz: {}
      }
    }
  }
}
```

### 5.4 Webhook Configuration

For receiving webhooks from external services:

```json5
{
  hooks: {
    enabled: true,
    port: 8787,
    bind: "loopback",
    path: "/hooks",
    secret: "${WEBHOOK_SECRET}",
    handlers: {
      "github": {
        enabled: true,
        events: ["push", "pull_request"]
      },
      "stripe": {
        enabled: true,
        verifySignature: true
      }
    }
  }
}
```

---

## 6. CLI Tools for Agent Orchestration

### 6.1 Gateway Management

```bash
# Run gateway
openclaw gateway
openclaw gateway run  # Foreground alias

# Service management
openclaw gateway install --port 18789 --token <token>
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway status
openclaw gateway health

# Discovery
openclaw gateway discover
openclaw gateway probe
openclaw gateway probe --ssh user@gateway-host
```

### 6.2 Agent Management

```bash
# List agents
openclaw agents list
openclaw agents list --bindings

# Add new agent
openclaw agents add work --workspace ~/.openclaw/workspace-work

# Set agent identity
openclaw agents set-identity --agent work --name "WorkBot" --emoji "💼"
openclaw agents set-identity --workspace ~/.openclaw/workspace-work --from-identity

# Delete agent
openclaw agents delete work
```

### 6.3 Channel Management

```bash
# Configure channels
openclaw channels add --channel telegram --token "<bot-token>"
openclaw channels login  # Interactive WhatsApp QR setup

# List configured channels
openclaw channels list
```

### 6.4 Session Management

```bash
# List sessions
openclaw sessions list
openclaw sessions list --agent work

# Send message to session
openclaw sessions send <session-id> "Hello from CLI"

# View session history
openclaw sessions history <session-id>
```

### 6.5 Low-Level RPC

```bash
# Call gateway methods directly
openclaw gateway call status
openclaw gateway call config.get --params '{}'
openclaw gateway call config.patch --params '{"raw": "...", "baseHash": "..."}'
openclaw gateway call system-presence
```

---

## 7. Remote Access Patterns

### 7.1 SSH Tunnel (Recommended)

```bash
# Forward local port to remote gateway
ssh -N -L 18789:127.0.0.1:18789 user@vps-host

# With specific key
ssh -N -L 18789:127.0.0.1:18789 -i ~/.ssh/id_rsa user@vps-host

# Auto-start on macOS (LaunchAgent)
# Create ~/Library/LaunchAgents/bot.molt.ssh-tunnel.plist
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/bot.molt.ssh-tunnel.plist
```

### 7.2 Tailscale Integration

```bash
# Enable Tailscale serve for Control UI
openclaw gateway --tailscale serve

# Or use Tailscale funnel for public access
openclaw gateway --tailscale funnel
```

### 7.3 CLI Remote Configuration

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://127.0.0.1:18789",
      token: "your-gateway-token"
    }
  }
}
```

---

## 8. Summary: OpenClaw as Managerial Agent

### 8.1 Strengths for VPS Deployment

1. **Centralized Control**: Single Gateway manages multiple agents and channels
2. **Agent Isolation**: Each agent has separate workspace, auth, and sessions
3. **Flexible Routing**: Sophisticated binding system for message routing
4. **Multi-Channel**: Native support for Telegram, WhatsApp, Discord, Slack, etc.
5. **Security**: Device-based pairing, token auth, sandboxing support
6. **Remote Access**: SSH tunnel and Tailscale integration
7. **Extensibility**: Plugin system for custom channels and tools

### 8.2 Deployment Checklist

- [ ] Provision VPS (Ubuntu/Debian recommended)
- [ ] Install Docker and Docker Compose
- [ ] Clone OpenClaw repository
- [ ] Create persistent directories (`~/.openclaw`, workspace)
- [ ] Configure `.env` with gateway token and settings
- [ ] Customize Dockerfile with required binaries
- [ ] Build and start with `docker compose up -d`
- [ ] Configure channels (Telegram bot, WhatsApp QR, etc.)
- [ ] Set up agents and bindings
- [ ] Configure SSH tunnel or Tailscale for remote access
- [ ] Set up systemd/LaunchAgent for auto-start (optional)

### 8.3 Key Files Reference

| File | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | Main configuration (JSON5) |
| `~/.openclaw/agents/<id>/agent/auth-profiles.json` | Per-agent OAuth/API keys |
| `~/.openclaw/agents/<id>/sessions/` | Session store |
| `~/.openclaw/workspace-<id>/` | Agent workspaces |
| `~/.openclaw/skills/` | Shared skills directory |

---

## References

- Source documentation: `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/openclaw/raw/pages/`
- Gateway Configuration: `gateway-configuration.md`
- Remote Access: `gateway-remote.md`, `gateway-remote-gateway-readme.md`
- Multi-Agent: `concepts-multi-agent.md`
- Docker Install: `install-docker.md`
- Hetzner VPS: `install-hetzner.md`
- CLI Agents: `cli-agents.md`
- CLI Gateway: `cli-gateway.md`
- Protocol: `gateway-protocol.md`
- Architecture: `concepts-architecture.md`
