---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/channels/troubleshooting",
    "fetched_at": "2026-02-07T10:13:04.309926",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 474217
  },
  "metadata": {
    "title": "Channel Troubleshooting",
    "section": "troubleshooting",
    "tier": 3,
    "type": "reference"
  }
}
---

- Channel Troubleshooting - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationConfigurationChannel Troubleshooting[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Chat Channels](/channels)Messaging platforms- [WhatsApp](/channels/whatsapp)- [Telegram](/channels/telegram)- [grammY](/channels/grammy)- [Discord](/channels/discord)- [Slack](/channels/slack)- [Feishu](/channels/feishu)- [Google Chat](/channels/googlechat)- [Mattermost](/channels/mattermost)- [Signal](/channels/signal)- [iMessage](/channels/imessage)- [Microsoft Teams](/channels/msteams)- [LINE](/channels/line)- [Matrix](/channels/matrix)- [Zalo](/channels/zalo)- [Zalo Personal](/channels/zalouser)Configuration- [Pairing](/start/pairing)- [Group Messages](/concepts/group-messages)- [Groups](/concepts/groups)- [Broadcast Groups](/broadcast-groups)- [Channel Routing](/concepts/channel-routing)- [Channel Location Parsing](/channels/location)- [Channel Troubleshooting](/channels/troubleshooting)On this page- [Channel troubleshooting](#channel-troubleshooting)- [Channels](#channels)- [Telegram quick fixes](#telegram-quick-fixes)Configuration# Channel Troubleshooting# [​](#channel-troubleshooting)Channel troubleshooting

Start with:

Copy```

openclaw doctor

openclaw channels status --probe

```

`channels status --probe` prints warnings when it can detect common channel misconfigurations, and includes small live checks (credentials, some permissions/membership).

## [​](#channels)Channels

- Discord: [/channels/discord#troubleshooting](/channels/discord#troubleshooting)

- Telegram: [/channels/telegram#troubleshooting](/channels/telegram#troubleshooting)

- WhatsApp: [/channels/whatsapp#troubleshooting-quick](/channels/whatsapp#troubleshooting-quick)

- iMessage (legacy): [/channels/imessage#troubleshooting-macos-privacy-and-security-tcc](/channels/imessage#troubleshooting-macos-privacy-and-security-tcc)

## [​](#telegram-quick-fixes)Telegram quick fixes

- Logs show `HttpError: Network request for 'sendMessage' failed` or `sendChatAction` → check IPv6 DNS. If `api.telegram.org` resolves to IPv6 first and the host lacks IPv6 egress, force IPv4 or enable IPv6. See [/channels/telegram#troubleshooting](/channels/telegram#troubleshooting).

- Logs show `setMyCommands failed` → check outbound HTTPS and DNS reachability to `api.telegram.org` (common on locked-down VPS or proxies).

[Channel Location Parsing](/channels/location)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)