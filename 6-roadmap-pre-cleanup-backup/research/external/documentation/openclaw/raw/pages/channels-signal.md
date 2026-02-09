---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/channels/signal",
    "fetched_at": "2026-02-07T10:13:02.653324",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 599397
  },
  "metadata": {
    "title": "Signal",
    "section": "signal",
    "tier": 3,
    "type": "reference"
  }
}
---

- Signal - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMessaging platformsSignal[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Chat Channels](/channels)Messaging platforms- [WhatsApp](/channels/whatsapp)- [Telegram](/channels/telegram)- [grammY](/channels/grammy)- [Discord](/channels/discord)- [Slack](/channels/slack)- [Feishu](/channels/feishu)- [Google Chat](/channels/googlechat)- [Mattermost](/channels/mattermost)- [Signal](/channels/signal)- [iMessage](/channels/imessage)- [Microsoft Teams](/channels/msteams)- [LINE](/channels/line)- [Matrix](/channels/matrix)- [Zalo](/channels/zalo)- [Zalo Personal](/channels/zalouser)Configuration- [Pairing](/start/pairing)- [Group Messages](/concepts/group-messages)- [Groups](/concepts/groups)- [Broadcast Groups](/broadcast-groups)- [Channel Routing](/concepts/channel-routing)- [Channel Location Parsing](/channels/location)- [Channel Troubleshooting](/channels/troubleshooting)On this page- [Signal (signal-cli)](#signal-signal-cli)- [Quick setup (beginner)](#quick-setup-beginner)- [What it is](#what-it-is)- [Config writes](#config-writes)- [The number model (important)](#the-number-model-important)- [Setup (fast path)](#setup-fast-path)- [External daemon mode (httpUrl)](#external-daemon-mode-httpurl)- [Access control (DMs + groups)](#access-control-dms-%2B-groups)- [How it works (behavior)](#how-it-works-behavior)- [Media + limits](#media-%2B-limits)- [Typing + read receipts](#typing-%2B-read-receipts)- [Reactions (message tool)](#reactions-message-tool)- [Delivery targets (CLI/cron)](#delivery-targets-cli%2Fcron)- [Configuration reference (Signal)](#configuration-reference-signal)Messaging platforms# Signal# [​](#signal-signal-cli)Signal (signal-cli)

Status: external CLI integration. Gateway talks to `signal-cli` over HTTP JSON-RPC + SSE.

## [​](#quick-setup-beginner)Quick setup (beginner)

- Use a **separate Signal number** for the bot (recommended).

- Install `signal-cli` (Java required).

- Link the bot device and start the daemon:

`signal-cli link -n "OpenClaw"`

- Configure OpenClaw and start the gateway.

Minimal config:

Copy```

{

channels: {

signal: {

enabled: true,

account: "+15551234567",

cliPath: "signal-cli",

dmPolicy: "pairing",

allowFrom: ["+15557654321"],

},

},

}

```

## [​](#what-it-is)What it is

- Signal channel via `signal-cli` (not embedded libsignal).

- Deterministic routing: replies always go back to Signal.

- DMs share the agent’s main session; groups are isolated (`agent:<agentId>:signal:group:<groupId>`).

## [​](#config-writes)Config writes

By default, Signal is allowed to write config updates triggered by `/config set|unset` (requires `commands.config: true`).

Disable with:

Copy```

{

channels: { signal: { configWrites: false } },

}

```

## [​](#the-number-model-important)The number model (important)

- The gateway connects to a **Signal device** (the `signal-cli` account).

- If you run the bot on **your personal Signal account**, it will ignore your own messages (loop protection).

- For “I text the bot and it replies,” use a **separate bot number**.

## [​](#setup-fast-path)Setup (fast path)

- Install `signal-cli` (Java required).

- Link a bot account:

`signal-cli link -n "OpenClaw"` then scan the QR in Signal.

- Configure Signal and start the gateway.

Example:

Copy```

{

channels: {

signal: {

enabled: true,

account: "+15551234567",

cliPath: "signal-cli",

dmPolicy: "pairing",

allowFrom: ["+15557654321"],

},

},

}

```

Multi-account support: use `channels.signal.accounts` with per-account config and optional `name`. See [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) for the shared pattern.

## [​](#external-daemon-mode-httpurl)External daemon mode (httpUrl)

If you want to manage `signal-cli` yourself (slow JVM cold starts, container init, or shared CPUs), run the daemon separately and point OpenClaw at it:

Copy```

{

channels: {

signal: {

httpUrl: "http://127.0.0.1:8080",

autoStart: false,

},

},

}

```

This skips auto-spawn and the startup wait inside OpenClaw. For slow starts when auto-spawning, set `channels.signal.startupTimeoutMs`.

## [​](#access-control-dms-+-groups)Access control (DMs + groups)

DMs:

- Default: `channels.signal.dmPolicy = "pairing"`.

- Unknown senders receive a pairing code; messages are ignored until approved (codes expire after 1 hour).

- Approve via:

`openclaw pairing list signal`

- `openclaw pairing approve signal <CODE>`

- Pairing is the default token exchange for Signal DMs. Details: [Pairing](/start/pairing)

- UUID-only senders (from `sourceUuid`) are stored as `uuid:<id>` in `channels.signal.allowFrom`.

Groups:

- `channels.signal.groupPolicy = open | allowlist | disabled`.

- `channels.signal.groupAllowFrom` controls who can trigger in groups when `allowlist` is set.

## [​](#how-it-works-behavior)How it works (behavior)

- `signal-cli` runs as a daemon; the gateway reads events via SSE.

- Inbound messages are normalized into the shared channel envelope.

- Replies always route back to the same number or group.

## [​](#media-+-limits)Media + limits

- Outbound text is chunked to `channels.signal.textChunkLimit` (default 4000).

- Optional newline chunking: set `channels.signal.chunkMode="newline"` to split on blank lines (paragraph boundaries) before length chunking.

- Attachments supported (base64 fetched from `signal-cli`).

- Default media cap: `channels.signal.mediaMaxMb` (default 8).

- Use `channels.signal.ignoreAttachments` to skip downloading media.

- Group history context uses `channels.signal.historyLimit` (or `channels.signal.accounts.*.historyLimit`), falling back to `messages.groupChat.historyLimit`. Set `0` to disable (default 50).

## [​](#typing-+-read-receipts)Typing + read receipts

- **Typing indicators**: OpenClaw sends typing signals via `signal-cli sendTyping` and refreshes them while a reply is running.

- **Read receipts**: when `channels.signal.sendReadReceipts` is true, OpenClaw forwards read receipts for allowed DMs.

- Signal-cli does not expose read receipts for groups.

## [​](#reactions-message-tool)Reactions (message tool)

- Use `message action=react` with `channel=signal`.

- Targets: sender E.164 or UUID (use `uuid:<id>` from pairing output; bare UUID works too).

- `messageId` is the Signal timestamp for the message you’re reacting to.

- Group reactions require `targetAuthor` or `targetAuthorUuid`.

Examples:

Copy```

message action=react channel=signal target=uuid:123e4567-e89b-12d3-a456-426614174000 messageId=1737630212345 emoji=🔥

message action=react channel=signal target=+15551234567 messageId=1737630212345 emoji=🔥 remove=true

message action=react channel=signal target=signal:group:<groupId> targetAuthor=uuid:<sender-uuid> messageId=1737630212345 emoji=✅

```

Config:

- `channels.signal.actions.reactions`: enable/disable reaction actions (default true).

- `channels.signal.reactionLevel`: `off | ack | minimal | extensive`.

`off`/`ack` disables agent reactions (message tool `react` will error).

- `minimal`/`extensive` enables agent reactions and sets the guidance level.

- Per-account overrides: `channels.signal.accounts.<id>.actions.reactions`, `channels.signal.accounts.<id>.reactionLevel`.

## [​](#delivery-targets-cli/cron)Delivery targets (CLI/cron)

- DMs: `signal:+15551234567` (or plain E.164).

- UUID DMs: `uuid:<id>` (or bare UUID).

- Groups: `signal:group:<groupId>`.

- Usernames: `username:<name>` (if supported by your Signal account).

## [​](#configuration-reference-signal)Configuration reference (Signal)

Full configuration: [Configuration](/gateway/configuration)

Provider options:

- `channels.signal.enabled`: enable/disable channel startup.

- `channels.signal.account`: E.164 for the bot account.

- `channels.signal.cliPath`: path to `signal-cli`.

- `channels.signal.httpUrl`: full daemon URL (overrides host/port).

- `channels.signal.httpHost`, `channels.signal.httpPort`: daemon bind (default 127.0.0.1:8080).

- `channels.signal.autoStart`: auto-spawn daemon (default true if `httpUrl` unset).

- `channels.signal.startupTimeoutMs`: startup wait timeout in ms (cap 120000).

- `channels.signal.receiveMode`: `on-start | manual`.

- `channels.signal.ignoreAttachments`: skip attachment downloads.

- `channels.signal.ignoreStories`: ignore stories from the daemon.

- `channels.signal.sendReadReceipts`: forward read receipts.

- `channels.signal.dmPolicy`: `pairing | allowlist | open | disabled` (default: pairing).

- `channels.signal.allowFrom`: DM allowlist (E.164 or `uuid:<id>`). `open` requires `"*"`. Signal has no usernames; use phone/UUID ids.

- `channels.signal.groupPolicy`: `open | allowlist | disabled` (default: allowlist).

- `channels.signal.groupAllowFrom`: group sender allowlist.

- `channels.signal.historyLimit`: max group messages to include as context (0 disables).

- `channels.signal.dmHistoryLimit`: DM history limit in user turns. Per-user overrides: `channels.signal.dms["<phone_or_uuid>"].historyLimit`.

- `channels.signal.textChunkLimit`: outbound chunk size (chars).

- `channels.signal.chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.

- `channels.signal.mediaMaxMb`: inbound/outbound media cap (MB).

Related global options:

- `agents.list[].groupChat.mentionPatterns` (Signal does not support native mentions).

- `messages.groupChat.mentionPatterns` (global fallback).

- `messages.responsePrefix`.

[Mattermost](/channels/mattermost)[iMessage](/channels/imessage)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)