---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/start/pairing",
    "fetched_at": "2026-02-07T10:23:08.224962",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 512661
  },
  "metadata": {
    "title": "Pairing",
    "section": "pairing",
    "tier": 3,
    "type": "reference"
  }
}
---

- Pairing - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationConfigurationPairing[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Chat Channels](/channels)Messaging platforms- [WhatsApp](/channels/whatsapp)- [Telegram](/channels/telegram)- [grammY](/channels/grammy)- [Discord](/channels/discord)- [Slack](/channels/slack)- [Feishu](/channels/feishu)- [Google Chat](/channels/googlechat)- [Mattermost](/channels/mattermost)- [Signal](/channels/signal)- [iMessage](/channels/imessage)- [Microsoft Teams](/channels/msteams)- [LINE](/channels/line)- [Matrix](/channels/matrix)- [Zalo](/channels/zalo)- [Zalo Personal](/channels/zalouser)Configuration- [Pairing](/start/pairing)- [Group Messages](/concepts/group-messages)- [Groups](/concepts/groups)- [Broadcast Groups](/broadcast-groups)- [Channel Routing](/concepts/channel-routing)- [Channel Location Parsing](/channels/location)- [Channel Troubleshooting](/channels/troubleshooting)On this page- [Pairing](#pairing)- [1) DM pairing (inbound chat access)](#1-dm-pairing-inbound-chat-access)- [Approve a sender](#approve-a-sender)- [Where the state lives](#where-the-state-lives)- [2) Node device pairing (iOS/Android/macOS/headless nodes)](#2-node-device-pairing-ios%2Fandroid%2Fmacos%2Fheadless-nodes)- [Approve a node device](#approve-a-node-device)- [Node pairing state storage](#node-pairing-state-storage)- [Notes](#notes)- [Related docs](#related-docs)Configuration# Pairing# [​](#pairing)Pairing

“Pairing” is OpenClaw’s explicit **owner approval** step.

It is used in two places:

- **DM pairing** (who is allowed to talk to the bot)

- **Node pairing** (which devices/nodes are allowed to join the gateway network)

Security context: [Security](/gateway/security)

## [​](#1-dm-pairing-inbound-chat-access)1) DM pairing (inbound chat access)

When a channel is configured with DM policy `pairing`, unknown senders get a short code and their message is **not processed** until you approve.

Default DM policies are documented in: [Security](/gateway/security)

Pairing codes:

- 8 characters, uppercase, no ambiguous chars (`0O1I`).

- **Expire after 1 hour**. The bot only sends the pairing message when a new request is created (roughly once per hour per sender).

- Pending DM pairing requests are capped at **3 per channel** by default; additional requests are ignored until one expires or is approved.

### [​](#approve-a-sender)Approve a sender

Copy```

openclaw pairing list telegram

openclaw pairing approve telegram <CODE>

```

Supported channels: `telegram`, `whatsapp`, `signal`, `imessage`, `discord`, `slack`.

### [​](#where-the-state-lives)Where the state lives

Stored under `~/.openclaw/credentials/`:

- Pending requests: `<channel>-pairing.json`

- Approved allowlist store: `<channel>-allowFrom.json`

Treat these as sensitive (they gate access to your assistant).

## [​](#2-node-device-pairing-ios/android/macos/headless-nodes)2) Node device pairing (iOS/Android/macOS/headless nodes)

Nodes connect to the Gateway as **devices** with `role: node`. The Gateway

creates a device pairing request that must be approved.

### [​](#approve-a-node-device)Approve a node device

Copy```

openclaw devices list

openclaw devices approve <requestId>

openclaw devices reject <requestId>

```

### [​](#node-pairing-state-storage)Node pairing state storage

Stored under `~/.openclaw/devices/`:

- `pending.json` (short-lived; pending requests expire)

- `paired.json` (paired devices + tokens)

### [​](#notes)Notes

- The legacy `node.pair.*` API (CLI: `openclaw nodes pending/approve`) is a

separate gateway-owned pairing store. WS nodes still require device pairing.

## [​](#related-docs)Related docs

- Security model + prompt injection: [Security](/gateway/security)

- Updating safely (run doctor): [Updating](/install/updating)

- Channel configs:

Telegram: [Telegram](/channels/telegram)

- WhatsApp: [WhatsApp](/channels/whatsapp)

- Signal: [Signal](/channels/signal)

- BlueBubbles (iMessage): [BlueBubbles](/channels/bluebubbles)

- iMessage (legacy): [iMessage](/channels/imessage)

- Discord: [Discord](/channels/discord)

- Slack: [Slack](/channels/slack)

[Zalo Personal](/channels/zalouser)[Group Messages](/concepts/group-messages)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)