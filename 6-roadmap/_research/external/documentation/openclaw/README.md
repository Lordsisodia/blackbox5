---
source:
  name: "OpenClaw Documentation"
  url: "https://docs.openclaw.ai/"
  type: official-docs
  category: ai-tools
  status: active
  last_synced: "2026-02-07T10:10:18Z"
  version: null

structure:
  sections:
    - name: Getting Started
      path: raw/pages/start/
      key_files:
        - getting-started.md
        - onboarding.md
        - setup.md

    - name: Gateway
      path: raw/pages/gateway/
      key_files:
        - configuration.md
        - configuration-examples.md
        - security.md
        - sandboxing.md

    - name: Channels
      path: raw/pages/channels/
      key_files:
        - slack.md
        - telegram.md
        - discord.md
        - whatsapp.md
        - imessage.md

    - name: CLI Reference
      path: raw/pages/cli/
      key_files:
        - skills.md
        - hooks.md
        - memory.md
        - plugins.md
        - security.md

    - name: Concepts
      path: raw/pages/concepts/
      key_files:
        - memory.md
        - sessions.md
        - multi-agent-routing.md
        - agent-workspace.md

    - name: Platforms
      path: raw/pages/platforms/
      key_files:
        - mac/permissions.md
        - mac/canvas.md
        - mac/voice-wake.md

    - name: Tools
      path: raw/pages/tools/
      key_files:
        - sub-agents.md
        - skills.md
        - browser.md
        - lobster.md

    - name: Web
      path: raw/pages/web/
      key_files:
        - control-ui.md
        - dashboard.md
        - webchat.md

    - name: Providers
      path: raw/pages/providers/
      key_files:
        - anthropic.md
        - openai.md
        - openrouter.md

agent_access:
  quick_ref: raw/pages/start/getting-started.md
  search_index: raw/index.json
  code_examples: raw/pages/tools/
---

# OpenClaw Documentation

Official documentation for OpenClaw, a multi-channel AI gateway for Claude and other LLMs.

## Overview

OpenClaw is a self-hosted gateway that enables AI agents across multiple channels:
- **Messaging**: WhatsApp, Telegram, Discord, iMessage, Slack, Signal
- **Web**: Control UI, WebChat, Dashboard
- **Mobile**: iOS and Android apps with Canvas support
- **Enterprise**: Microsoft Teams, Matrix, Mattermost

## Status

- **Last synced**: 2026-02-07
- **Pages fetched**: 252 of 252 (100%)
- **Completeness**: Complete
- **Total size**: 2.7 MB

## Key Documentation Areas

| Area | Description |
|------|-------------|
| **Gateway** | Self-hosted server configuration, security, sandboxing |
| **Channels** | 15+ messaging platform integrations |
| **CLI** | Command-line tools for skills, hooks, memory, plugins |
| **Multi-Agent** | Routing, isolated sessions, agent workspaces |
| **Tools** | Sub-agents, browser automation, Lobster workflows |
| **Mobile** | iOS/Android apps, voice, camera, location |

## Quick Access

| What | Where |
|------|-------|
| Raw fetched pages | `raw/pages/` |
| Index | `raw/index.json` |
| Getting started | `raw/pages/start/getting-started.md` |
| Gateway config | `raw/pages/gateway/configuration.md` |
| Multi-agent routing | `raw/pages/concepts/multi-agent-routing.md` |

## Relationship to BlackBox5

OpenClaw complements BlackBox5:
- **Claude Code** = Terminal IDE (already documented)
- **OpenClaw** = Multi-channel gateway (this documentation)
- **RALF** = Autonomous execution engine (BlackBox5 core)

Use OpenClaw for:
- Multi-channel agent deployment
- WhatsApp/Telegram bot interfaces
- Voice and mobile interactions
- Gateway-based agent routing

## For Agents

Use `raw/index.json` for programmatic discovery.
Reference specific channel docs for integration patterns.

## References

- **Source**: https://docs.openclaw.ai/
- **llms.txt**: https://docs.openclaw.ai/llms.txt
- **GitHub**: https://github.com/openclaw
