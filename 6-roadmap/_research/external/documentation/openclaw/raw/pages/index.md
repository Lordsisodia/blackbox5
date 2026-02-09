---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/index",
    "fetched_at": "2026-02-07T10:18:59.143810",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 547375
  },
  "metadata": {
    "title": "OpenClaw",
    "section": "index",
    "tier": 3,
    "type": "reference"
  }
}
---

- OpenClaw - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationOverviewOpenClaw[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [OpenClaw](/)- [Features](/concepts/features)- [Showcase](/start/showcase)First steps- [Getting Started](/start/getting-started)- [Onboarding: CLI](/start/wizard)- [Onboarding: macOS App](/start/onboarding)Guides- [Personal Assistant Setup](/start/openclaw)On this page- [OpenClaw 🦞](#openclaw-)- [What is OpenClaw?](#what-is-openclaw)- [How it works](#how-it-works)- [Key capabilities](#key-capabilities)- [Quick start](#quick-start)- [Dashboard](#dashboard)- [Configuration (optional)](#configuration-optional)- [Start here](#start-here)- [Learn more](#learn-more)Overview# OpenClaw# [​](#openclaw-)OpenClaw 🦞

*“EXFOLIATE! EXFOLIATE!”* — A space lobster, probably

**Any OS gateway for AI agents across WhatsApp, Telegram, Discord, iMessage, and more.**

Send a message, get an agent response from your pocket. Plugins add Mattermost and more.

[## Get StartedInstall OpenClaw and bring up the Gateway in minutes.](/start/getting-started)[## Run the WizardGuided setup with `openclaw onboard` and pairing flows.](/start/wizard)[## Open the Control UILaunch the browser dashboard for chat, config, and sessions.](/web/control-ui)

## [​](#what-is-openclaw)What is OpenClaw?

OpenClaw is a **self-hosted gateway** that connects your favorite chat apps — WhatsApp, Telegram, Discord, iMessage, and more — to AI coding agents like Pi. You run a single Gateway process on your own machine (or a server), and it becomes the bridge between your messaging apps and an always-available AI assistant.

**Who is it for?** Developers and power users who want a personal AI assistant they can message from anywhere — without giving up control of their data or relying on a hosted service.

**What makes it different?**

- **Self-hosted**: runs on your hardware, your rules

- **Multi-channel**: one Gateway serves WhatsApp, Telegram, Discord, and more simultaneously

- **Agent-native**: built for coding agents with tool use, sessions, memory, and multi-agent routing

- **Open source**: MIT licensed, community-driven

**What do you need?** Node 22+, an API key (Anthropic recommended), and 5 minutes.

## [​](#how-it-works)How it works

The Gateway is the single source of truth for sessions, routing, and channel connections.

## [​](#key-capabilities)Key capabilities

## Multi-channel gatewayWhatsApp, Telegram, Discord, and iMessage with a single Gateway process.## Plugin channelsAdd Mattermost and more with extension packages.## Multi-agent routingIsolated sessions per agent, workspace, or sender.## Media supportSend and receive images, audio, and documents.## Web Control UIBrowser dashboard for chat, config, sessions, and nodes.## Mobile nodesPair iOS and Android nodes with Canvas support.

## [​](#quick-start)Quick start

1[](#)Install OpenClawCopy```

npm install -g openclaw@latest

```2[](#)Onboard and install the serviceCopy```

openclaw onboard --install-daemon

```3[](#)Pair WhatsApp and start the GatewayCopy```

openclaw channels login

openclaw gateway --port 18789

```

Need the full install and dev setup? See [Quick start](/start/quickstart).

## [​](#dashboard)Dashboard

Open the browser Control UI after the Gateway starts.

- Local default: [http://127.0.0.1:18789/](http://127.0.0.1:18789/)

- Remote access: [Web surfaces](/web) and [Tailscale](/gateway/tailscale)

## [​](#configuration-optional)Configuration (optional)

Config lives at `~/.openclaw/openclaw.json`.

- If you **do nothing**, OpenClaw uses the bundled Pi binary in RPC mode with per-sender sessions.

- If you want to lock it down, start with `channels.whatsapp.allowFrom` and (for groups) mention rules.

Example:

Copy```

{

channels: {

whatsapp: {

allowFrom: ["+15555550123"],

groups: { "*": { requireMention: true } },

},

},

messages: { groupChat: { mentionPatterns: ["@openclaw"] } },

}

```

## [​](#start-here)Start here

[## Docs hubsAll docs and guides, organized by use case.](/start/hubs)[## ConfigurationCore Gateway settings, tokens, and provider config.](/gateway/configuration)[## Remote accessSSH and tailnet access patterns.](/gateway/remote)[## ChannelsChannel-specific setup for WhatsApp, Telegram, Discord, and more.](/channels/telegram)[## NodesiOS and Android nodes with pairing and Canvas.](/nodes)[## HelpCommon fixes and troubleshooting entry point.](/help)

## [​](#learn-more)Learn more

[## Full feature listComplete channel, routing, and media capabilities.](/concepts/features)[## Multi-agent routingWorkspace isolation and per-agent sessions.](/concepts/multi-agent)[## SecurityTokens, allowlists, and safety controls.](/gateway/security)[## TroubleshootingGateway diagnostics and common errors.](/gateway/troubleshooting)[## About and creditsProject origins, contributors, and license.](/reference/credits)[Features](/concepts/features)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)