---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/channels/mattermost",
    "fetched_at": "2026-02-07T10:13:01.248909",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 562759
  },
  "metadata": {
    "title": "Mattermost",
    "section": "mattermost",
    "tier": 3,
    "type": "reference"
  }
}
---

- Mattermost - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMessaging platformsMattermost[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Chat Channels](/channels)Messaging platforms- [WhatsApp](/channels/whatsapp)- [Telegram](/channels/telegram)- [grammY](/channels/grammy)- [Discord](/channels/discord)- [Slack](/channels/slack)- [Feishu](/channels/feishu)- [Google Chat](/channels/googlechat)- [Mattermost](/channels/mattermost)- [Signal](/channels/signal)- [iMessage](/channels/imessage)- [Microsoft Teams](/channels/msteams)- [LINE](/channels/line)- [Matrix](/channels/matrix)- [Zalo](/channels/zalo)- [Zalo Personal](/channels/zalouser)Configuration- [Pairing](/start/pairing)- [Group Messages](/concepts/group-messages)- [Groups](/concepts/groups)- [Broadcast Groups](/broadcast-groups)- [Channel Routing](/concepts/channel-routing)- [Channel Location Parsing](/channels/location)- [Channel Troubleshooting](/channels/troubleshooting)On this page- [Mattermost (plugin)](#mattermost-plugin)- [Plugin required](#plugin-required)- [Quick setup](#quick-setup)- [Environment variables (default account)](#environment-variables-default-account)- [Chat modes](#chat-modes)- [Access control (DMs)](#access-control-dms)- [Channels (groups)](#channels-groups)- [Targets for outbound delivery](#targets-for-outbound-delivery)- [Multi-account](#multi-account)- [Troubleshooting](#troubleshooting)Messaging platforms# Mattermost# [​](#mattermost-plugin)Mattermost (plugin)

Status: supported via plugin (bot token + WebSocket events). Channels, groups, and DMs are supported.

Mattermost is a self-hostable team messaging platform; see the official site at

[mattermost.com](https://mattermost.com) for product details and downloads.

## [​](#plugin-required)Plugin required

Mattermost ships as a plugin and is not bundled with the core install.

Install via CLI (npm registry):

Copy```

openclaw plugins install @openclaw/mattermost

```

Local checkout (when running from a git repo):

Copy```

openclaw plugins install ./extensions/mattermost

```

If you choose Mattermost during configure/onboarding and a git checkout is detected,

OpenClaw will offer the local install path automatically.

Details: [Plugins](/plugin)

## [​](#quick-setup)Quick setup

- Install the Mattermost plugin.

- Create a Mattermost bot account and copy the **bot token**.

- Copy the Mattermost **base URL** (e.g., `https://chat.example.com`).

- Configure OpenClaw and start the gateway.

Minimal config:

Copy```

{

channels: {

mattermost: {

enabled: true,

botToken: "mm-token",

baseUrl: "https://chat.example.com",

dmPolicy: "pairing",

},

},

}

```

## [​](#environment-variables-default-account)Environment variables (default account)

Set these on the gateway host if you prefer env vars:

- `MATTERMOST_BOT_TOKEN=...`

- `MATTERMOST_URL=https://chat.example.com`

Env vars apply only to the **default** account (`default`). Other accounts must use config values.

## [​](#chat-modes)Chat modes

Mattermost responds to DMs automatically. Channel behavior is controlled by `chatmode`:

- `oncall` (default): respond only when @mentioned in channels.

- `onmessage`: respond to every channel message.

- `onchar`: respond when a message starts with a trigger prefix.

Config example:

Copy```

{

channels: {

mattermost: {

chatmode: "onchar",

oncharPrefixes: [">", "!"],

},

},

}

```

Notes:

- `onchar` still responds to explicit @mentions.

- `channels.mattermost.requireMention` is honored for legacy configs but `chatmode` is preferred.

## [​](#access-control-dms)Access control (DMs)

- Default: `channels.mattermost.dmPolicy = "pairing"` (unknown senders get a pairing code).

- Approve via:

`openclaw pairing list mattermost`

- `openclaw pairing approve mattermost <CODE>`

- Public DMs: `channels.mattermost.dmPolicy="open"` plus `channels.mattermost.allowFrom=["*"]`.

## [​](#channels-groups)Channels (groups)

- Default: `channels.mattermost.groupPolicy = "allowlist"` (mention-gated).

- Allowlist senders with `channels.mattermost.groupAllowFrom` (user IDs or `@username`).

- Open channels: `channels.mattermost.groupPolicy="open"` (mention-gated).

## [​](#targets-for-outbound-delivery)Targets for outbound delivery

Use these target formats with `openclaw message send` or cron/webhooks:

- `channel:<id>` for a channel

- `user:<id>` for a DM

- `@username` for a DM (resolved via the Mattermost API)

Bare IDs are treated as channels.

## [​](#multi-account)Multi-account

Mattermost supports multiple accounts under `channels.mattermost.accounts`:

Copy```

{

channels: {

mattermost: {

accounts: {

default: { name: "Primary", botToken: "mm-token", baseUrl: "https://chat.example.com" },

alerts: { name: "Alerts", botToken: "mm-token-2", baseUrl: "https://alerts.example.com" },

},

},

},

}

```

## [​](#troubleshooting)Troubleshooting

- No replies in channels: ensure the bot is in the channel and mention it (oncall), use a trigger prefix (onchar), or set `chatmode: "onmessage"`.

- Auth errors: check the bot token, base URL, and whether the account is enabled.

- Multi-account issues: env vars only apply to the `default` account.

[Google Chat](/channels/googlechat)[Signal](/channels/signal)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)