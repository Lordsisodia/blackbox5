# OpenClaw Framework Research

## Overview

OpenClaw is an npm package that provides an AI agent gateway with multi-channel support (Telegram, Discord) and a skill system for extending functionality.

## Installation

```bash
npm install -g openclaw
```

## Core Concepts

### Gateway

The gateway provides an HTTP API for MCP (Model Context Protocol) connections:

- **Port:** Configurable (default 18789)
- **Endpoints:**
  - `/sse` - SSE endpoint for MCP
  - `/health` - Health check
  - `/notify` - Notification endpoint

### Channels

Communication interfaces for different platforms:

#### Telegram
- Bot token authentication
- Command handling (!ralf status)
- Direct message support
- User ID whitelist for security

#### Discord
- Bot token authentication
- Slash commands
- Channel-based messaging

### Skills

JavaScript modules that extend OpenClaw functionality:

```javascript
class MySkill {
  constructor() {
    this.name = 'my-skill';
    this.description = 'What this skill does';
  }

  async someFunction() {
    // Skill logic here
  }
}

module.exports = MySkill;
```

### Agent Configuration

```json
{
  "agent": {
    "model": "anthropic/claude-sonnet-4-5",
    "baseUrl": "https://api.z.ai/api/anthropic"
  }
}
```

## Configuration File (openclaw.json)

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
    },
    "discord": {
      "enabled": true,
      "token": "YOUR_DISCORD_TOKEN"
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
    "host": "0.0.0.0"
  }
}
```

## Commands

```bash
# Start the daemon
openclaw daemon

# Check version
openclaw --version

# Initialize config
openclaw init
```

## Research Questions

1. Is OpenClaw a custom/internal package or public?
2. What is the full MCP implementation?
3. How does the skill system load and execute?
4. What other channels are supported?
5. How does message routing work?

## To Research

- [ ] npm package details (if public)
- [ ] GitHub repository (if exists)
- [ ] Full API documentation
- [ ] Skill development guide
- [ ] MCP protocol implementation
