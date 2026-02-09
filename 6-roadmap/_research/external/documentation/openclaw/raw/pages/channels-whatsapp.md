---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/channels/whatsapp",
    "fetched_at": "2026-02-07T10:13:05.016391",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 732218
  },
  "metadata": {
    "title": "WhatsApp",
    "section": "whatsapp",
    "tier": 3,
    "type": "reference"
  }
}
---

- WhatsApp - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMessaging platformsWhatsApp[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Chat Channels](/channels)Messaging platforms- [WhatsApp](/channels/whatsapp)- [Telegram](/channels/telegram)- [grammY](/channels/grammy)- [Discord](/channels/discord)- [Slack](/channels/slack)- [Feishu](/channels/feishu)- [Google Chat](/channels/googlechat)- [Mattermost](/channels/mattermost)- [Signal](/channels/signal)- [iMessage](/channels/imessage)- [Microsoft Teams](/channels/msteams)- [LINE](/channels/line)- [Matrix](/channels/matrix)- [Zalo](/channels/zalo)- [Zalo Personal](/channels/zalouser)Configuration- [Pairing](/start/pairing)- [Group Messages](/concepts/group-messages)- [Groups](/concepts/groups)- [Broadcast Groups](/broadcast-groups)- [Channel Routing](/concepts/channel-routing)- [Channel Location Parsing](/channels/location)- [Channel Troubleshooting](/channels/troubleshooting)On this page- [WhatsApp (web channel)](#whatsapp-web-channel)- [Quick setup (beginner)](#quick-setup-beginner)- [Goals](#goals)- [Config writes](#config-writes)- [Architecture (who owns what)](#architecture-who-owns-what)- [Getting a phone number (two modes)](#getting-a-phone-number-two-modes)- [Dedicated number (recommended)](#dedicated-number-recommended)- [Personal number (fallback)](#personal-number-fallback)- [Number sourcing tips](#number-sourcing-tips)- [Why Not Twilio?](#why-not-twilio)- [Login + credentials](#login-%2B-credentials)- [Inbound flow (DM + group)](#inbound-flow-dm-%2B-group)- [Personal-number mode (fallback)](#personal-number-mode-fallback)- [Read receipts](#read-receipts)- [WhatsApp FAQ: sending messages + pairing](#whatsapp-faq-sending-messages-%2B-pairing)- [Message normalization (what the model sees)](#message-normalization-what-the-model-sees)- [Groups](#groups)- [Reply delivery (threading)](#reply-delivery-threading)- [Acknowledgment reactions (auto-react on receipt)](#acknowledgment-reactions-auto-react-on-receipt)- [Agent tool (reactions)](#agent-tool-reactions)- [Limits](#limits)- [Outbound send (text + media)](#outbound-send-text-%2B-media)- [Voice notes (PTT audio)](#voice-notes-ptt-audio)- [Media limits + optimization](#media-limits-%2B-optimization)- [Heartbeats](#heartbeats)- [Reconnect behavior](#reconnect-behavior)- [Config quick map](#config-quick-map)- [Logs + troubleshooting](#logs-%2B-troubleshooting)- [Troubleshooting (quick)](#troubleshooting-quick)Messaging platforms# WhatsApp# [​](#whatsapp-web-channel)WhatsApp (web channel)

Status: WhatsApp Web via Baileys only. Gateway owns the session(s).

## [​](#quick-setup-beginner)Quick setup (beginner)

- Use a **separate phone number** if possible (recommended).

- Configure WhatsApp in `~/.openclaw/openclaw.json`.

- Run `openclaw channels login` to scan the QR code (Linked Devices).

- Start the gateway.

Minimal config:

Copy```

{

channels: {

whatsapp: {

dmPolicy: "allowlist",

allowFrom: ["+15551234567"],

},

},

}

```

## [​](#goals)Goals

- Multiple WhatsApp accounts (multi-account) in one Gateway process.

- Deterministic routing: replies return to WhatsApp, no model routing.

- Model sees enough context to understand quoted replies.

## [​](#config-writes)Config writes

By default, WhatsApp is allowed to write config updates triggered by `/config set|unset` (requires `commands.config: true`).

Disable with:

Copy```

{

channels: { whatsapp: { configWrites: false } },

}

```

## [​](#architecture-who-owns-what)Architecture (who owns what)

- **Gateway** owns the Baileys socket and inbox loop.

- **CLI / macOS app** talk to the gateway; no direct Baileys use.

- **Active listener** is required for outbound sends; otherwise send fails fast.

## [​](#getting-a-phone-number-two-modes)Getting a phone number (two modes)

WhatsApp requires a real mobile number for verification. VoIP and virtual numbers are usually blocked. There are two supported ways to run OpenClaw on WhatsApp:

### [​](#dedicated-number-recommended)Dedicated number (recommended)

Use a **separate phone number** for OpenClaw. Best UX, clean routing, no self-chat quirks. Ideal setup: **spare/old Android phone + eSIM**. Leave it on Wi‑Fi and power, and link it via QR.

**WhatsApp Business:** You can use WhatsApp Business on the same device with a different number. Great for keeping your personal WhatsApp separate — install WhatsApp Business and register the OpenClaw number there.

**Sample config (dedicated number, single-user allowlist):**

Copy```

{

channels: {

whatsapp: {

dmPolicy: "allowlist",

allowFrom: ["+15551234567"],

},

},

}

```

**Pairing mode (optional):**

If you want pairing instead of allowlist, set `channels.whatsapp.dmPolicy` to `pairing`. Unknown senders get a pairing code; approve with:

`openclaw pairing approve whatsapp <code>`

### [​](#personal-number-fallback)Personal number (fallback)

Quick fallback: run OpenClaw on **your own number**. Message yourself (WhatsApp “Message yourself”) for testing so you don’t spam contacts. Expect to read verification codes on your main phone during setup and experiments. **Must enable self-chat mode.**

When the wizard asks for your personal WhatsApp number, enter the phone you will message from (the owner/sender), not the assistant number.

**Sample config (personal number, self-chat):**

Copy```

{

"whatsapp": {

"selfChatMode": true,

"dmPolicy": "allowlist",

"allowFrom": ["+15551234567"]

}

}

```

Self-chat replies default to `[{identity.name}]` when set (otherwise `[openclaw]`)

if `messages.responsePrefix` is unset. Set it explicitly to customize or disable

the prefix (use `""` to remove it).

### [​](#number-sourcing-tips)Number sourcing tips

- **Local eSIM** from your country’s mobile carrier (most reliable)

Austria: [hot.at](https://www.hot.at)

- UK: [giffgaff](https://www.giffgaff.com) — free SIM, no contract

- **Prepaid SIM** — cheap, just needs to receive one SMS for verification

**Avoid:** TextNow, Google Voice, most “free SMS” services — WhatsApp blocks these aggressively.

**Tip:** The number only needs to receive one verification SMS. After that, WhatsApp Web sessions persist via `creds.json`.

## [​](#why-not-twilio)Why Not Twilio?

- Early OpenClaw builds supported Twilio’s WhatsApp Business integration.

- WhatsApp Business numbers are a poor fit for a personal assistant.

- Meta enforces a 24‑hour reply window; if you haven’t responded in the last 24 hours, the business number can’t initiate new messages.

- High-volume or “chatty” usage triggers aggressive blocking, because business accounts aren’t meant to send dozens of personal assistant messages.

- Result: unreliable delivery and frequent blocks, so support was removed.

## [​](#login-+-credentials)Login + credentials

- Login command: `openclaw channels login` (QR via Linked Devices).

- Multi-account login: `openclaw channels login --account <id>` (`<id>` = `accountId`).

- Default account (when `--account` is omitted): `default` if present, otherwise the first configured account id (sorted).

- Credentials stored in `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`.

- Backup copy at `creds.json.bak` (restored on corruption).

- Legacy compatibility: older installs stored Baileys files directly in `~/.openclaw/credentials/`.

- Logout: `openclaw channels logout` (or `--account <id>`) deletes WhatsApp auth state (but keeps shared `oauth.json`).

- Logged-out socket => error instructs re-link.

## [​](#inbound-flow-dm-+-group)Inbound flow (DM + group)

- WhatsApp events come from `messages.upsert` (Baileys).

- Inbox listeners are detached on shutdown to avoid accumulating event handlers in tests/restarts.

- Status/broadcast chats are ignored.

- Direct chats use E.164; groups use group JID.

- **DM policy**: `channels.whatsapp.dmPolicy` controls direct chat access (default: `pairing`).

Pairing: unknown senders get a pairing code (approve via `openclaw pairing approve whatsapp <code>`; codes expire after 1 hour).

- Open: requires `channels.whatsapp.allowFrom` to include `"*"`.

- Your linked WhatsApp number is implicitly trusted, so self messages skip ⁠`channels.whatsapp.dmPolicy` and `channels.whatsapp.allowFrom` checks.

### [​](#personal-number-mode-fallback)Personal-number mode (fallback)

If you run OpenClaw on your **personal WhatsApp number**, enable `channels.whatsapp.selfChatMode` (see sample above).

Behavior:

- Outbound DMs never trigger pairing replies (prevents spamming contacts).

- Inbound unknown senders still follow `channels.whatsapp.dmPolicy`.

- Self-chat mode (allowFrom includes your number) avoids auto read receipts and ignores mention JIDs.

- Read receipts sent for non-self-chat DMs.

## [​](#read-receipts)Read receipts

By default, the gateway marks inbound WhatsApp messages as read (blue ticks) once they are accepted.

Disable globally:

Copy```

{

channels: { whatsapp: { sendReadReceipts: false } },

}

```

Disable per account:

Copy```

{

channels: {

whatsapp: {

accounts: {

personal: { sendReadReceipts: false },

},

},

},

}

```

Notes:

- Self-chat mode always skips read receipts.

## [​](#whatsapp-faq-sending-messages-+-pairing)WhatsApp FAQ: sending messages + pairing

**Will OpenClaw message random contacts when I link WhatsApp?**

No. Default DM policy is **pairing**, so unknown senders only get a pairing code and their message is **not processed**. OpenClaw only replies to chats it receives, or to sends you explicitly trigger (agent/CLI).

**How does pairing work on WhatsApp?**

Pairing is a DM gate for unknown senders:

- First DM from a new sender returns a short code (message is not processed).

- Approve with: `openclaw pairing approve whatsapp <code>` (list with `openclaw pairing list whatsapp`).

- Codes expire after 1 hour; pending requests are capped at 3 per channel.

**Can multiple people use different OpenClaw instances on one WhatsApp number?**

Yes, by routing each sender to a different agent via `bindings` (peer `kind: "dm"`, sender E.164 like `+15551234567`). Replies still come from the **same WhatsApp account**, and direct chats collapse to each agent’s main session, so use **one agent per person**. DM access control (`dmPolicy`/`allowFrom`) is global per WhatsApp account. See [Multi-Agent Routing](/concepts/multi-agent).

**Why do you ask for my phone number in the wizard?**

The wizard uses it to set your **allowlist/owner** so your own DMs are permitted. It’s not used for auto-sending. If you run on your personal WhatsApp number, use that same number and enable `channels.whatsapp.selfChatMode`.

## [​](#message-normalization-what-the-model-sees)Message normalization (what the model sees)

-

`Body` is the current message body with envelope.

-

Quoted reply context is **always appended**:

Copy```

[Replying to +1555 id:ABC123]

<quoted text or <media:...>>

[/Replying]

```

-

Reply metadata also set:

`ReplyToId` = stanzaId

- `ReplyToBody` = quoted body or media placeholder

- `ReplyToSender` = E.164 when known

-

Media-only inbound messages use placeholders:

`<media:image|video|audio|document|sticker>`

## [​](#groups)Groups

- Groups map to `agent:<agentId>:whatsapp:group:<jid>` sessions.

- Group policy: `channels.whatsapp.groupPolicy = open|disabled|allowlist` (default `allowlist`).

- Activation modes:

`mention` (default): requires @mention or regex match.

- `always`: always triggers.

- `/activation mention|always` is owner-only and must be sent as a standalone message.

- Owner = `channels.whatsapp.allowFrom` (or self E.164 if unset).

- **History injection** (pending-only):

Recent *unprocessed* messages (default 50) inserted under:

`[Chat messages since your last reply - for context]` (messages already in the session are not re-injected)

- Current message under:

`[Current message - respond to this]`

- Sender suffix appended: `[from: Name (+E164)]`

- Group metadata cached 5 min (subject + participants).

## [​](#reply-delivery-threading)Reply delivery (threading)

- WhatsApp Web sends standard messages (no quoted reply threading in the current gateway).

- Reply tags are ignored on this channel.

## [​](#acknowledgment-reactions-auto-react-on-receipt)Acknowledgment reactions (auto-react on receipt)

WhatsApp can automatically send emoji reactions to incoming messages immediately upon receipt, before the bot generates a reply. This provides instant feedback to users that their message was received.

**Configuration:**

Copy```

{

"whatsapp": {

"ackReaction": {

"emoji": "👀",

"direct": true,

"group": "mentions"

}

}

}

```

**Options:**

- `emoji` (string): Emoji to use for acknowledgment (e.g., ”👀”, ”✅”, ”📨”). Empty or omitted = feature disabled.

- `direct` (boolean, default: `true`): Send reactions in direct/DM chats.

- `group` (string, default: `"mentions"`): Group chat behavior:

`"always"`: React to all group messages (even without @mention)

- `"mentions"`: React only when bot is @mentioned

- `"never"`: Never react in groups

**Per-account override:**

Copy```

{

"whatsapp": {

"accounts": {

"work": {

"ackReaction": {

"emoji": "✅",

"direct": false,

"group": "always"

}

}

}

}

}

```

**Behavior notes:**

- Reactions are sent **immediately** upon message receipt, before typing indicators or bot replies.

- In groups with `requireMention: false` (activation: always), `group: "mentions"` will react to all messages (not just @mentions).

- Fire-and-forget: reaction failures are logged but don’t prevent the bot from replying.

- Participant JID is automatically included for group reactions.

- WhatsApp ignores `messages.ackReaction`; use `channels.whatsapp.ackReaction` instead.

## [​](#agent-tool-reactions)Agent tool (reactions)

- Tool: `whatsapp` with `react` action (`chatJid`, `messageId`, `emoji`, optional `remove`).

- Optional: `participant` (group sender), `fromMe` (reacting to your own message), `accountId` (multi-account).

- Reaction removal semantics: see [/tools/reactions](/tools/reactions).

- Tool gating: `channels.whatsapp.actions.reactions` (default: enabled).

## [​](#limits)Limits

- Outbound text is chunked to `channels.whatsapp.textChunkLimit` (default 4000).

- Optional newline chunking: set `channels.whatsapp.chunkMode="newline"` to split on blank lines (paragraph boundaries) before length chunking.

- Inbound media saves are capped by `channels.whatsapp.mediaMaxMb` (default 50 MB).

- Outbound media items are capped by `agents.defaults.mediaMaxMb` (default 5 MB).

## [​](#outbound-send-text-+-media)Outbound send (text + media)

- Uses active web listener; error if gateway not running.

- Text chunking: 4k max per message (configurable via `channels.whatsapp.textChunkLimit`, optional `channels.whatsapp.chunkMode`).

- Media:

Image/video/audio/document supported.

- Audio sent as PTT; `audio/ogg` => `audio/ogg; codecs=opus`.

- Caption only on first media item.

- Media fetch supports HTTP(S) and local paths.

- Animated GIFs: WhatsApp expects MP4 with `gifPlayback: true` for inline looping.

CLI: `openclaw message send --media <mp4> --gif-playback`

- Gateway: `send` params include `gifPlayback: true`

## [​](#voice-notes-ptt-audio)Voice notes (PTT audio)

WhatsApp sends audio as **voice notes** (PTT bubble).

- Best results: OGG/Opus. OpenClaw rewrites `audio/ogg` to `audio/ogg; codecs=opus`.

- `[[audio_as_voice]]` is ignored for WhatsApp (audio already ships as voice note).

## [​](#media-limits-+-optimization)Media limits + optimization

- Default outbound cap: 5 MB (per media item).

- Override: `agents.defaults.mediaMaxMb`.

- Images are auto-optimized to JPEG under cap (resize + quality sweep).

- Oversize media => error; media reply falls back to text warning.

## [​](#heartbeats)Heartbeats

- **Gateway heartbeat** logs connection health (`web.heartbeatSeconds`, default 60s).

- **Agent heartbeat** can be configured per agent (`agents.list[].heartbeat`) or globally

via `agents.defaults.heartbeat` (fallback when no per-agent entries are set).

Uses the configured heartbeat prompt (default: `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`) + `HEARTBEAT_OK` skip behavior.

- Delivery defaults to the last used channel (or configured target).

## [​](#reconnect-behavior)Reconnect behavior

- Backoff policy: `web.reconnect`:

`initialMs`, `maxMs`, `factor`, `jitter`, `maxAttempts`.

- If maxAttempts reached, web monitoring stops (degraded).

- Logged-out => stop and require re-link.

## [​](#config-quick-map)Config quick map

- `channels.whatsapp.dmPolicy` (DM policy: pairing/allowlist/open/disabled).

- `channels.whatsapp.selfChatMode` (same-phone setup; bot uses your personal WhatsApp number).

- `channels.whatsapp.allowFrom` (DM allowlist). WhatsApp uses E.164 phone numbers (no usernames).

- `channels.whatsapp.mediaMaxMb` (inbound media save cap).

- `channels.whatsapp.ackReaction` (auto-reaction on message receipt: `{emoji, direct, group}`).

- `channels.whatsapp.accounts.<accountId>.*` (per-account settings + optional `authDir`).

- `channels.whatsapp.accounts.<accountId>.mediaMaxMb` (per-account inbound media cap).

- `channels.whatsapp.accounts.<accountId>.ackReaction` (per-account ack reaction override).

- `channels.whatsapp.groupAllowFrom` (group sender allowlist).

- `channels.whatsapp.groupPolicy` (group policy).

- `channels.whatsapp.historyLimit` / `channels.whatsapp.accounts.<accountId>.historyLimit` (group history context; `0` disables).

- `channels.whatsapp.dmHistoryLimit` (DM history limit in user turns). Per-user overrides: `channels.whatsapp.dms["<phone>"].historyLimit`.

- `channels.whatsapp.groups` (group allowlist + mention gating defaults; use `"*"` to allow all)

- `channels.whatsapp.actions.reactions` (gate WhatsApp tool reactions).

- `agents.list[].groupChat.mentionPatterns` (or `messages.groupChat.mentionPatterns`)

- `messages.groupChat.historyLimit`

- `channels.whatsapp.messagePrefix` (inbound prefix; per-account: `channels.whatsapp.accounts.<accountId>.messagePrefix`; deprecated: `messages.messagePrefix`)

- `messages.responsePrefix` (outbound prefix)

- `agents.defaults.mediaMaxMb`

- `agents.defaults.heartbeat.every`

- `agents.defaults.heartbeat.model` (optional override)

- `agents.defaults.heartbeat.target`

- `agents.defaults.heartbeat.to`

- `agents.defaults.heartbeat.session`

- `agents.list[].heartbeat.*` (per-agent overrides)

- `session.*` (scope, idle, store, mainKey)

- `web.enabled` (disable channel startup when false)

- `web.heartbeatSeconds`

- `web.reconnect.*`

## [​](#logs-+-troubleshooting)Logs + troubleshooting

- Subsystems: `whatsapp/inbound`, `whatsapp/outbound`, `web-heartbeat`, `web-reconnect`.

- Log file: `/tmp/openclaw/openclaw-YYYY-MM-DD.log` (configurable).

- Troubleshooting guide: [Gateway troubleshooting](/gateway/troubleshooting).

## [​](#troubleshooting-quick)Troubleshooting (quick)

**Not linked / QR login required**

- Symptom: `channels status` shows `linked: false` or warns “Not linked”.

- Fix: run `openclaw channels login` on the gateway host and scan the QR (WhatsApp → Settings → Linked Devices).

**Linked but disconnected / reconnect loop**

- Symptom: `channels status` shows `running, disconnected` or warns “Linked but disconnected”.

- Fix: `openclaw doctor` (or restart the gateway). If it persists, relink via `channels login` and inspect `openclaw logs --follow`.

**Bun runtime**

- Bun is **not recommended**. WhatsApp (Baileys) and Telegram are unreliable on Bun.

Run the gateway with **Node**. (See Getting Started runtime note.)

[Chat Channels](/channels)[Telegram](/channels/telegram)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)