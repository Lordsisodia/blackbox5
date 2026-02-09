---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/channels/index",
    "fetched_at": "2026-02-07T10:12:57.343321",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 476912
  },
  "metadata": {
    "title": "Chat Channels",
    "section": "index",
    "tier": 3,
    "type": "reference"
  }
}
---

- Chat Channels - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationOverviewChat Channels[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Chat Channels](/channels)Messaging platforms- [WhatsApp](/channels/whatsapp)- [Telegram](/channels/telegram)- [grammY](/channels/grammy)- [Discord](/channels/discord)- [Slack](/channels/slack)- [Feishu](/channels/feishu)- [Google Chat](/channels/googlechat)- [Mattermost](/channels/mattermost)- [Signal](/channels/signal)- [iMessage](/channels/imessage)- [Microsoft Teams](/channels/msteams)- [LINE](/channels/line)- [Matrix](/channels/matrix)- [Zalo](/channels/zalo)- [Zalo Personal](/channels/zalouser)Configuration- [Pairing](/start/pairing)- [Group Messages](/concepts/group-messages)- [Groups](/concepts/groups)- [Broadcast Groups](/broadcast-groups)- [Channel Routing](/concepts/channel-routing)- [Channel Location Parsing](/channels/location)- [Channel Troubleshooting](/channels/troubleshooting)On this page- [Chat Channels](#chat-channels)- [Supported channels](#supported-channels)- [Notes](#notes)Overview# Chat Channels# [​](#chat-channels)Chat Channels

OpenClaw can talk to you on any chat app you already use. Each channel connects via the Gateway.

Text is supported everywhere; media and reactions vary by channel.

## [​](#supported-channels)Supported channels

- [WhatsApp](/channels/whatsapp) — Most popular; uses Baileys and requires QR pairing.

- [Telegram](/channels/telegram) — Bot API via grammY; supports groups.

- [Discord](/channels/discord) — Discord Bot API + Gateway; supports servers, channels, and DMs.

- [Slack](/channels/slack) — Bolt SDK; workspace apps.

- [Feishu](/channels/feishu) — Feishu/Lark bot via WebSocket (plugin, installed separately).

- [Google Chat](/channels/googlechat) — Google Chat API app via HTTP webhook.

- [Mattermost](/channels/mattermost) — Bot API + WebSocket; channels, groups, DMs (plugin, installed separately).

- [Signal](/channels/signal) — signal-cli; privacy-focused.

- [BlueBubbles](/channels/bluebubbles) — **Recommended for iMessage**; uses the BlueBubbles macOS server REST API with full feature support (edit, unsend, effects, reactions, group management — edit currently broken on macOS 26 Tahoe).

- [iMessage (legacy)](/channels/imessage) — Legacy macOS integration via imsg CLI (deprecated, use BlueBubbles for new setups).

- [Microsoft Teams](/channels/msteams) — Bot Framework; enterprise support (plugin, installed separately).

- [LINE](/channels/line) — LINE Messaging API bot (plugin, installed separately).

- [Nextcloud Talk](/channels/nextcloud-talk) — Self-hosted chat via Nextcloud Talk (plugin, installed separately).

- [Matrix](/channels/matrix) — Matrix protocol (plugin, installed separately).

- [Nostr](/channels/nostr) — Decentralized DMs via NIP-04 (plugin, installed separately).

- [Tlon](/channels/tlon) — Urbit-based messenger (plugin, installed separately).

- [Twitch](/channels/twitch) — Twitch chat via IRC connection (plugin, installed separately).

- [Zalo](/channels/zalo) — Zalo Bot API; Vietnam’s popular messenger (plugin, installed separately).

- [Zalo Personal](/channels/zalouser) — Zalo personal account via QR login (plugin, installed separately).

- [WebChat](/web/webchat) — Gateway WebChat UI over WebSocket.

## [​](#notes)Notes

- Channels can run simultaneously; configure multiple and OpenClaw will route per chat.

- Fastest setup is usually **Telegram** (simple bot token). WhatsApp requires QR pairing and

stores more state on disk.

- Group behavior varies by channel; see [Groups](/concepts/groups).

- DM pairing and allowlists are enforced for safety; see [Security](/gateway/security).

- Telegram internals: [grammY notes](/channels/grammy).

- Troubleshooting: [Channel troubleshooting](/channels/troubleshooting).

- Model providers are documented separately; see [Model Providers](/providers/models).

[WhatsApp](/channels/whatsapp)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)