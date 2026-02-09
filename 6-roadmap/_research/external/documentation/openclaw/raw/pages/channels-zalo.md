---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/channels/zalo",
    "fetched_at": "2026-02-07T10:13:05.712448",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 564171
  },
  "metadata": {
    "title": "Zalo",
    "section": "zalo",
    "tier": 3,
    "type": "reference"
  }
}
---

- Zalo - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMessaging platformsZalo[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Chat Channels](/channels)Messaging platforms- [WhatsApp](/channels/whatsapp)- [Telegram](/channels/telegram)- [grammY](/channels/grammy)- [Discord](/channels/discord)- [Slack](/channels/slack)- [Feishu](/channels/feishu)- [Google Chat](/channels/googlechat)- [Mattermost](/channels/mattermost)- [Signal](/channels/signal)- [iMessage](/channels/imessage)- [Microsoft Teams](/channels/msteams)- [LINE](/channels/line)- [Matrix](/channels/matrix)- [Zalo](/channels/zalo)- [Zalo Personal](/channels/zalouser)Configuration- [Pairing](/start/pairing)- [Group Messages](/concepts/group-messages)- [Groups](/concepts/groups)- [Broadcast Groups](/broadcast-groups)- [Channel Routing](/concepts/channel-routing)- [Channel Location Parsing](/channels/location)- [Channel Troubleshooting](/channels/troubleshooting)On this page- [Zalo (Bot API)](#zalo-bot-api)- [Plugin required](#plugin-required)- [Quick setup (beginner)](#quick-setup-beginner)- [What it is](#what-it-is)- [Setup (fast path)](#setup-fast-path)- [1) Create a bot token (Zalo Bot Platform)](#1-create-a-bot-token-zalo-bot-platform)- [2) Configure the token (env or config)](#2-configure-the-token-env-or-config)- [How it works (behavior)](#how-it-works-behavior)- [Limits](#limits)- [Access control (DMs)](#access-control-dms)- [DM access](#dm-access)- [Long-polling vs webhook](#long-polling-vs-webhook)- [Supported message types](#supported-message-types)- [Capabilities](#capabilities)- [Delivery targets (CLI/cron)](#delivery-targets-cli%2Fcron)- [Troubleshooting](#troubleshooting)- [Configuration reference (Zalo)](#configuration-reference-zalo)Messaging platforms# Zalo# [​](#zalo-bot-api)Zalo (Bot API)

Status: experimental. Direct messages only; groups coming soon per Zalo docs.

## [​](#plugin-required)Plugin required

Zalo ships as a plugin and is not bundled with the core install.

- Install via CLI: `openclaw plugins install @openclaw/zalo`

- Or select **Zalo** during onboarding and confirm the install prompt

- Details: [Plugins](/plugin)

## [​](#quick-setup-beginner)Quick setup (beginner)

- Install the Zalo plugin:

From a source checkout: `openclaw plugins install ./extensions/zalo`

- From npm (if published): `openclaw plugins install @openclaw/zalo`

- Or pick **Zalo** in onboarding and confirm the install prompt

- Set the token:

Env: `ZALO_BOT_TOKEN=...`

- Or config: `channels.zalo.botToken: "..."`.

- Restart the gateway (or finish onboarding).

- DM access is pairing by default; approve the pairing code on first contact.

Minimal config:

Copy```

{

channels: {

zalo: {

enabled: true,

botToken: "12345689:abc-xyz",

dmPolicy: "pairing",

},

},

}

```

## [​](#what-it-is)What it is

Zalo is a Vietnam-focused messaging app; its Bot API lets the Gateway run a bot for 1:1 conversations.

It is a good fit for support or notifications where you want deterministic routing back to Zalo.

- A Zalo Bot API channel owned by the Gateway.

- Deterministic routing: replies go back to Zalo; the model never chooses channels.

- DMs share the agent’s main session.

- Groups are not yet supported (Zalo docs state “coming soon”).

## [​](#setup-fast-path)Setup (fast path)

### [​](#1-create-a-bot-token-zalo-bot-platform)1) Create a bot token (Zalo Bot Platform)

- Go to [https://bot.zaloplatforms.com](https://bot.zaloplatforms.com) and sign in.

- Create a new bot and configure its settings.

- Copy the bot token (format: `12345689:abc-xyz`).

### [​](#2-configure-the-token-env-or-config)2) Configure the token (env or config)

Example:

Copy```

{

channels: {

zalo: {

enabled: true,

botToken: "12345689:abc-xyz",

dmPolicy: "pairing",

},

},

}

```

Env option: `ZALO_BOT_TOKEN=...` (works for the default account only).

Multi-account support: use `channels.zalo.accounts` with per-account tokens and optional `name`.

- Restart the gateway. Zalo starts when a token is resolved (env or config).

- DM access defaults to pairing. Approve the code when the bot is first contacted.

## [​](#how-it-works-behavior)How it works (behavior)

- Inbound messages are normalized into the shared channel envelope with media placeholders.

- Replies always route back to the same Zalo chat.

- Long-polling by default; webhook mode available with `channels.zalo.webhookUrl`.

## [​](#limits)Limits

- Outbound text is chunked to 2000 characters (Zalo API limit).

- Media downloads/uploads are capped by `channels.zalo.mediaMaxMb` (default 5).

- Streaming is blocked by default due to the 2000 char limit making streaming less useful.

## [​](#access-control-dms)Access control (DMs)

### [​](#dm-access)DM access

- Default: `channels.zalo.dmPolicy = "pairing"`. Unknown senders receive a pairing code; messages are ignored until approved (codes expire after 1 hour).

- Approve via:

`openclaw pairing list zalo`

- `openclaw pairing approve zalo <CODE>`

- Pairing is the default token exchange. Details: [Pairing](/start/pairing)

- `channels.zalo.allowFrom` accepts numeric user IDs (no username lookup available).

## [​](#long-polling-vs-webhook)Long-polling vs webhook

- Default: long-polling (no public URL required).

- Webhook mode: set `channels.zalo.webhookUrl` and `channels.zalo.webhookSecret`.

The webhook secret must be 8-256 characters.

- Webhook URL must use HTTPS.

- Zalo sends events with `X-Bot-Api-Secret-Token` header for verification.

- Gateway HTTP handles webhook requests at `channels.zalo.webhookPath` (defaults to the webhook URL path).

**Note:** getUpdates (polling) and webhook are mutually exclusive per Zalo API docs.

## [​](#supported-message-types)Supported message types

- **Text messages**: Full support with 2000 character chunking.

- **Image messages**: Download and process inbound images; send images via `sendPhoto`.

- **Stickers**: Logged but not fully processed (no agent response).

- **Unsupported types**: Logged (e.g., messages from protected users).

## [​](#capabilities)Capabilities

FeatureStatusDirect messages✅ SupportedGroups❌ Coming soon (per Zalo docs)Media (images)✅ SupportedReactions❌ Not supportedThreads❌ Not supportedPolls❌ Not supportedNative commands❌ Not supportedStreaming⚠️ Blocked (2000 char limit)

## [​](#delivery-targets-cli/cron)Delivery targets (CLI/cron)

- Use a chat id as the target.

- Example: `openclaw message send --channel zalo --target 123456789 --message "hi"`.

## [​](#troubleshooting)Troubleshooting

**Bot doesn’t respond:**

- Check that the token is valid: `openclaw channels status --probe`

- Verify the sender is approved (pairing or allowFrom)

- Check gateway logs: `openclaw logs --follow`

**Webhook not receiving events:**

- Ensure webhook URL uses HTTPS

- Verify secret token is 8-256 characters

- Confirm the gateway HTTP endpoint is reachable on the configured path

- Check that getUpdates polling is not running (they’re mutually exclusive)

## [​](#configuration-reference-zalo)Configuration reference (Zalo)

Full configuration: [Configuration](/gateway/configuration)

Provider options:

- `channels.zalo.enabled`: enable/disable channel startup.

- `channels.zalo.botToken`: bot token from Zalo Bot Platform.

- `channels.zalo.tokenFile`: read token from file path.

- `channels.zalo.dmPolicy`: `pairing | allowlist | open | disabled` (default: pairing).

- `channels.zalo.allowFrom`: DM allowlist (user IDs). `open` requires `"*"`. The wizard will ask for numeric IDs.

- `channels.zalo.mediaMaxMb`: inbound/outbound media cap (MB, default 5).

- `channels.zalo.webhookUrl`: enable webhook mode (HTTPS required).

- `channels.zalo.webhookSecret`: webhook secret (8-256 chars).

- `channels.zalo.webhookPath`: webhook path on the gateway HTTP server.

- `channels.zalo.proxy`: proxy URL for API requests.

Multi-account options:

- `channels.zalo.accounts.<id>.botToken`: per-account token.

- `channels.zalo.accounts.<id>.tokenFile`: per-account token file.

- `channels.zalo.accounts.<id>.name`: display name.

- `channels.zalo.accounts.<id>.enabled`: enable/disable account.

- `channels.zalo.accounts.<id>.dmPolicy`: per-account DM policy.

- `channels.zalo.accounts.<id>.allowFrom`: per-account allowlist.

- `channels.zalo.accounts.<id>.webhookUrl`: per-account webhook URL.

- `channels.zalo.accounts.<id>.webhookSecret`: per-account webhook secret.

- `channels.zalo.accounts.<id>.webhookPath`: per-account webhook path.

- `channels.zalo.accounts.<id>.proxy`: per-account proxy URL.

[Matrix](/channels/matrix)[Zalo Personal](/channels/zalouser)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)