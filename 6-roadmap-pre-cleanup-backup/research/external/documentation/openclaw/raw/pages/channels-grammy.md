---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/channels/grammy",
    "fetched_at": "2026-02-07T10:12:55.712973",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 474762
  },
  "metadata": {
    "title": "grammY",
    "section": "grammy",
    "tier": 3,
    "type": "reference"
  }
}
---

- grammY - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMessaging platformsgrammY[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Chat Channels](/channels)Messaging platforms- [WhatsApp](/channels/whatsapp)- [Telegram](/channels/telegram)- [grammY](/channels/grammy)- [Discord](/channels/discord)- [Slack](/channels/slack)- [Feishu](/channels/feishu)- [Google Chat](/channels/googlechat)- [Mattermost](/channels/mattermost)- [Signal](/channels/signal)- [iMessage](/channels/imessage)- [Microsoft Teams](/channels/msteams)- [LINE](/channels/line)- [Matrix](/channels/matrix)- [Zalo](/channels/zalo)- [Zalo Personal](/channels/zalouser)Configuration- [Pairing](/start/pairing)- [Group Messages](/concepts/group-messages)- [Groups](/concepts/groups)- [Broadcast Groups](/broadcast-groups)- [Channel Routing](/concepts/channel-routing)- [Channel Location Parsing](/channels/location)- [Channel Troubleshooting](/channels/troubleshooting)On this page- [grammY Integration (Telegram Bot API)](#grammy-integration-telegram-bot-api)- [Why grammY](#why-grammy)- [What we shipped](#what-we-shipped)Messaging platforms# grammY# [​](#grammy-integration-telegram-bot-api)grammY Integration (Telegram Bot API)

# [​](#why-grammy)Why grammY

- TS-first Bot API client with built-in long-poll + webhook helpers, middleware, error handling, rate limiter.

- Cleaner media helpers than hand-rolling fetch + FormData; supports all Bot API methods.

- Extensible: proxy support via custom fetch, session middleware (optional), type-safe context.

# [​](#what-we-shipped)What we shipped

- **Single client path:** fetch-based implementation removed; grammY is now the sole Telegram client (send + gateway) with the grammY throttler enabled by default.

- **Gateway:** `monitorTelegramProvider` builds a grammY `Bot`, wires mention/allowlist gating, media download via `getFile`/`download`, and delivers replies with `sendMessage/sendPhoto/sendVideo/sendAudio/sendDocument`. Supports long-poll or webhook via `webhookCallback`.

- **Proxy:** optional `channels.telegram.proxy` uses `undici.ProxyAgent` through grammY’s `client.baseFetch`.

- **Webhook support:** `webhook-set.ts` wraps `setWebhook/deleteWebhook`; `webhook.ts` hosts the callback with health + graceful shutdown. Gateway enables webhook mode when `channels.telegram.webhookUrl` + `channels.telegram.webhookSecret` are set (otherwise it long-polls).

- **Sessions:** direct chats collapse into the agent main session (`agent:<agentId>:<mainKey>`); groups use `agent:<agentId>:telegram:group:<chatId>`; replies route back to the same channel.

- **Config knobs:** `channels.telegram.botToken`, `channels.telegram.dmPolicy`, `channels.telegram.groups` (allowlist + mention defaults), `channels.telegram.allowFrom`, `channels.telegram.groupAllowFrom`, `channels.telegram.groupPolicy`, `channels.telegram.mediaMaxMb`, `channels.telegram.linkPreview`, `channels.telegram.proxy`, `channels.telegram.webhookSecret`, `channels.telegram.webhookUrl`.

- **Draft streaming:** optional `channels.telegram.streamMode` uses `sendMessageDraft` in private topic chats (Bot API 9.3+). This is separate from channel block streaming.

- **Tests:** grammy mocks cover DM + group mention gating and outbound send; more media/webhook fixtures still welcome.

Open questions

- Optional grammY plugins (throttler) if we hit Bot API 429s.

- Add more structured media tests (stickers, voice notes).

- Make webhook listen port configurable (currently fixed to 8787 unless wired through the gateway).

[Telegram](/channels/telegram)[Discord](/channels/discord)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)