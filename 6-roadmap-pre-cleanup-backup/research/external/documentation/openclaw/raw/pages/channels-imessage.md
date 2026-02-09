---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/channels/imessage",
    "fetched_at": "2026-02-07T10:12:56.317743",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 719882
  },
  "metadata": {
    "title": "iMessage",
    "section": "imessage",
    "tier": 3,
    "type": "reference"
  }
}
---

- iMessage - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMessaging platformsiMessage[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Chat Channels](/channels)Messaging platforms- [WhatsApp](/channels/whatsapp)- [Telegram](/channels/telegram)- [grammY](/channels/grammy)- [Discord](/channels/discord)- [Slack](/channels/slack)- [Feishu](/channels/feishu)- [Google Chat](/channels/googlechat)- [Mattermost](/channels/mattermost)- [Signal](/channels/signal)- [iMessage](/channels/imessage)- [Microsoft Teams](/channels/msteams)- [LINE](/channels/line)- [Matrix](/channels/matrix)- [Zalo](/channels/zalo)- [Zalo Personal](/channels/zalouser)Configuration- [Pairing](/start/pairing)- [Group Messages](/concepts/group-messages)- [Groups](/concepts/groups)- [Broadcast Groups](/broadcast-groups)- [Channel Routing](/concepts/channel-routing)- [Channel Location Parsing](/channels/location)- [Channel Troubleshooting](/channels/troubleshooting)On this page- [iMessage (legacy: imsg)](#imessage-legacy-imsg)- [Quick setup (beginner)](#quick-setup-beginner)- [What it is](#what-it-is)- [Config writes](#config-writes)- [Requirements](#requirements)- [Troubleshooting macOS Privacy and Security TCC](#troubleshooting-macos-privacy-and-security-tcc)- [Setup (fast path)](#setup-fast-path)- [Dedicated bot macOS user (for isolated identity)](#dedicated-bot-macos-user-for-isolated-identity)- [Remote/SSH variant (optional)](#remote%2Fssh-variant-optional)- [Remote Mac via Tailscale (example)](#remote-mac-via-tailscale-example)- [Access control (DMs + groups)](#access-control-dms-%2B-groups)- [How it works (behavior)](#how-it-works-behavior)- [Group-ish threads (is_group=false)](#group-ish-threads-is_group%3Dfalse)- [Media + limits](#media-%2B-limits)- [Limits](#limits)- [Addressing / delivery targets](#addressing-%2F-delivery-targets)- [Configuration reference (iMessage)](#configuration-reference-imessage)Messaging platforms# iMessage# [​](#imessage-legacy-imsg)iMessage (legacy: imsg)

**Recommended:** Use [BlueBubbles](/channels/bluebubbles) for new iMessage setups.

The `imsg` channel is a legacy external-CLI integration and may be removed in a future release.

Status: legacy external CLI integration. Gateway spawns `imsg rpc` (JSON-RPC over stdio).

## [​](#quick-setup-beginner)Quick setup (beginner)

- Ensure Messages is signed in on this Mac.

- Install `imsg`:

`brew install steipete/tap/imsg`

- Configure OpenClaw with `channels.imessage.cliPath` and `channels.imessage.dbPath`.

- Start the gateway and approve any macOS prompts (Automation + Full Disk Access).

Minimal config:

Copy```

{

channels: {

imessage: {

enabled: true,

cliPath: "/usr/local/bin/imsg",

dbPath: "/Users/<you>/Library/Messages/chat.db",

},

},

}

```

## [​](#what-it-is)What it is

- iMessage channel backed by `imsg` on macOS.

- Deterministic routing: replies always go back to iMessage.

- DMs share the agent’s main session; groups are isolated (`agent:<agentId>:imessage:group:<chat_id>`).

- If a multi-participant thread arrives with `is_group=false`, you can still isolate it by `chat_id` using `channels.imessage.groups` (see “Group-ish threads” below).

## [​](#config-writes)Config writes

By default, iMessage is allowed to write config updates triggered by `/config set|unset` (requires `commands.config: true`).

Disable with:

Copy```

{

channels: { imessage: { configWrites: false } },

}

```

## [​](#requirements)Requirements

- macOS with Messages signed in.

- Full Disk Access for OpenClaw + `imsg` (Messages DB access).

- Automation permission when sending.

- `channels.imessage.cliPath` can point to any command that proxies stdin/stdout (for example, a wrapper script that SSHes to another Mac and runs `imsg rpc`).

## [​](#troubleshooting-macos-privacy-and-security-tcc)Troubleshooting macOS Privacy and Security TCC

If sending/receiving fails (for example, `imsg rpc` exits non-zero, times out, or the gateway appears to hang), a common cause is a macOS permission prompt that was never approved.

macOS grants TCC permissions per app/process context. Approve prompts in the same context that runs `imsg` (for example, Terminal/iTerm, a LaunchAgent session, or an SSH-launched process).

Checklist:

- **Full Disk Access**: allow access for the process running OpenClaw (and any shell/SSH wrapper that executes `imsg`). This is required to read the Messages database (`chat.db`).

- **Automation → Messages**: allow the process running OpenClaw (and/or your terminal) to control **Messages.app** for outbound sends.

- **`imsg` CLI health**: verify `imsg` is installed and supports RPC (`imsg rpc --help`).

Tip: If OpenClaw is running headless (LaunchAgent/systemd/SSH) the macOS prompt can be easy to miss. Run a one-time interactive command in a GUI terminal to force the prompt, then retry:

Copy```

imsg chats --limit 1

# or

imsg send <handle> "test"

```

Related macOS folder permissions (Desktop/Documents/Downloads): [/platforms/mac/permissions](/platforms/mac/permissions).

## [​](#setup-fast-path)Setup (fast path)

- Ensure Messages is signed in on this Mac.

- Configure iMessage and start the gateway.

### [​](#dedicated-bot-macos-user-for-isolated-identity)Dedicated bot macOS user (for isolated identity)

If you want the bot to send from a **separate iMessage identity** (and keep your personal Messages clean), use a dedicated Apple ID + a dedicated macOS user.

- Create a dedicated Apple ID (example: `[[email protected]](/cdn-cgi/l/email-protection)`).

Apple may require a phone number for verification / 2FA.

- Create a macOS user (example: `openclawhome`) and sign into it.

- Open Messages in that macOS user and sign into iMessage using the bot Apple ID.

- Enable Remote Login (System Settings → General → Sharing → Remote Login).

- Install `imsg`:

`brew install steipete/tap/imsg`

- Set up SSH so `ssh <bot-macos-user>@localhost true` works without a password.

- Point `channels.imessage.accounts.bot.cliPath` at an SSH wrapper that runs `imsg` as the bot user.

First-run note: sending/receiving may require GUI approvals (Automation + Full Disk Access) in the *bot macOS user*. If `imsg rpc` looks stuck or exits, log into that user (Screen Sharing helps), run a one-time `imsg chats --limit 1` / `imsg send ...`, approve prompts, then retry. See [Troubleshooting macOS Privacy and Security TCC](#troubleshooting-macos-privacy-and-security-tcc).

Example wrapper (`chmod +x`). Replace `<bot-macos-user>` with your actual macOS username:

Copy```

#!/usr/bin/env bash

set -euo pipefail

# Run an interactive SSH once first to accept host keys:

#   ssh <bot-macos-user>@localhost true

exec /usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=5 -T <bot-macos-user>@localhost \

"/usr/local/bin/imsg" "$@"

```

Example config:

Copy```

{

channels: {

imessage: {

enabled: true,

accounts: {

bot: {

name: "Bot",

enabled: true,

cliPath: "/path/to/imsg-bot",

dbPath: "/Users/<bot-macos-user>/Library/Messages/chat.db",

},

},

},

},

}

```

For single-account setups, use flat options (`channels.imessage.cliPath`, `channels.imessage.dbPath`) instead of the `accounts` map.

### [​](#remote/ssh-variant-optional)Remote/SSH variant (optional)

If you want iMessage on another Mac, set `channels.imessage.cliPath` to a wrapper that runs `imsg` on the remote macOS host over SSH. OpenClaw only needs stdio.

Example wrapper:

Copy```

#!/usr/bin/env bash

exec ssh -T gateway-host imsg "$@"

```

**Remote attachments:** When `cliPath` points to a remote host via SSH, attachment paths in the Messages database reference files on the remote machine. OpenClaw can automatically fetch these over SCP by setting `channels.imessage.remoteHost`:

Copy```

{

channels: {

imessage: {

cliPath: "~/imsg-ssh", // SSH wrapper to remote Mac

remoteHost: "user@gateway-host", // for SCP file transfer

includeAttachments: true,

},

},

}

```

If `remoteHost` is not set, OpenClaw attempts to auto-detect it by parsing the SSH command in your wrapper script. Explicit configuration is recommended for reliability.

#### [​](#remote-mac-via-tailscale-example)Remote Mac via Tailscale (example)

If the Gateway runs on a Linux host/VM but iMessage must run on a Mac, Tailscale is the simplest bridge: the Gateway talks to the Mac over the tailnet, runs `imsg` via SSH, and SCPs attachments back.

Architecture:

Copy```

┌──────────────────────────────┐          SSH (imsg rpc)          ┌──────────────────────────┐

│ Gateway host (Linux/VM)      │──────────────────────────────────▶│ Mac with Messages + imsg │

│ - openclaw gateway           │          SCP (attachments)        │ - Messages signed in     │

│ - channels.imessage.cliPath  │◀──────────────────────────────────│ - Remote Login enabled   │

└──────────────────────────────┘                                   └──────────────────────────┘

▲

│ Tailscale tailnet (hostname or 100.x.y.z)

▼

user@gateway-host

```

Concrete config example (Tailscale hostname):

Copy```

{

channels: {

imessage: {

enabled: true,

cliPath: "~/.openclaw/scripts/imsg-ssh",

remoteHost: "[[email protected]](/cdn-cgi/l/email-protection)",

includeAttachments: true,

dbPath: "/Users/bot/Library/Messages/chat.db",

},

},

}

```

Example wrapper (`~/.openclaw/scripts/imsg-ssh`):

Copy```

#!/usr/bin/env bash

exec ssh -T [[email protected]](/cdn-cgi/l/email-protection) imsg "$@"

```

Notes:

- Ensure the Mac is signed in to Messages, and Remote Login is enabled.

- Use SSH keys so `ssh [[email protected]](/cdn-cgi/l/email-protection)` works without prompts.

- `remoteHost` should match the SSH target so SCP can fetch attachments.

Multi-account support: use `channels.imessage.accounts` with per-account config and optional `name`. See [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) for the shared pattern. Don’t commit `~/.openclaw/openclaw.json` (it often contains tokens).

## [​](#access-control-dms-+-groups)Access control (DMs + groups)

DMs:

- Default: `channels.imessage.dmPolicy = "pairing"`.

- Unknown senders receive a pairing code; messages are ignored until approved (codes expire after 1 hour).

- Approve via:

`openclaw pairing list imessage`

- `openclaw pairing approve imessage <CODE>`

- Pairing is the default token exchange for iMessage DMs. Details: [Pairing](/start/pairing)

Groups:

- `channels.imessage.groupPolicy = open | allowlist | disabled`.

- `channels.imessage.groupAllowFrom` controls who can trigger in groups when `allowlist` is set.

- Mention gating uses `agents.list[].groupChat.mentionPatterns` (or `messages.groupChat.mentionPatterns`) because iMessage has no native mention metadata.

- Multi-agent override: set per-agent patterns on `agents.list[].groupChat.mentionPatterns`.

## [​](#how-it-works-behavior)How it works (behavior)

- `imsg` streams message events; the gateway normalizes them into the shared channel envelope.

- Replies always route back to the same chat id or handle.

## [​](#group-ish-threads-is_group=false)Group-ish threads (`is_group=false`)

Some iMessage threads can have multiple participants but still arrive with `is_group=false` depending on how Messages stores the chat identifier.

If you explicitly configure a `chat_id` under `channels.imessage.groups`, OpenClaw treats that thread as a “group” for:

- session isolation (separate `agent:<agentId>:imessage:group:<chat_id>` session key)

- group allowlisting / mention gating behavior

Example:

Copy```

{

channels: {

imessage: {

groupPolicy: "allowlist",

groupAllowFrom: ["+15555550123"],

groups: {

"42": { requireMention: false },

},

},

},

}

```

This is useful when you want an isolated personality/model for a specific thread (see [Multi-agent routing](/concepts/multi-agent)). For filesystem isolation, see [Sandboxing](/gateway/sandboxing).

## [​](#media-+-limits)Media + limits

- Optional attachment ingestion via `channels.imessage.includeAttachments`.

- Media cap via `channels.imessage.mediaMaxMb`.

## [​](#limits)Limits

- Outbound text is chunked to `channels.imessage.textChunkLimit` (default 4000).

- Optional newline chunking: set `channels.imessage.chunkMode="newline"` to split on blank lines (paragraph boundaries) before length chunking.

- Media uploads are capped by `channels.imessage.mediaMaxMb` (default 16).

## [​](#addressing-/-delivery-targets)Addressing / delivery targets

Prefer `chat_id` for stable routing:

- `chat_id:123` (preferred)

- `chat_guid:...`

- `chat_identifier:...`

- direct handles: `imessage:+1555` / `sms:+1555` / `[[email protected]](/cdn-cgi/l/email-protection)`

List chats:

Copy```

imsg chats --limit 20

```

## [​](#configuration-reference-imessage)Configuration reference (iMessage)

Full configuration: [Configuration](/gateway/configuration)

Provider options:

- `channels.imessage.enabled`: enable/disable channel startup.

- `channels.imessage.cliPath`: path to `imsg`.

- `channels.imessage.dbPath`: Messages DB path.

- `channels.imessage.remoteHost`: SSH host for SCP attachment transfer when `cliPath` points to a remote Mac (e.g., `user@gateway-host`). Auto-detected from SSH wrapper if not set.

- `channels.imessage.service`: `imessage | sms | auto`.

- `channels.imessage.region`: SMS region.

- `channels.imessage.dmPolicy`: `pairing | allowlist | open | disabled` (default: pairing).

- `channels.imessage.allowFrom`: DM allowlist (handles, emails, E.164 numbers, or `chat_id:*`). `open` requires `"*"`. iMessage has no usernames; use handles or chat targets.

- `channels.imessage.groupPolicy`: `open | allowlist | disabled` (default: allowlist).

- `channels.imessage.groupAllowFrom`: group sender allowlist.

- `channels.imessage.historyLimit` / `channels.imessage.accounts.*.historyLimit`: max group messages to include as context (0 disables).

- `channels.imessage.dmHistoryLimit`: DM history limit in user turns. Per-user overrides: `channels.imessage.dms["<handle>"].historyLimit`.

- `channels.imessage.groups`: per-group defaults + allowlist (use `"*"` for global defaults).

- `channels.imessage.includeAttachments`: ingest attachments into context.

- `channels.imessage.mediaMaxMb`: inbound/outbound media cap (MB).

- `channels.imessage.textChunkLimit`: outbound chunk size (chars).

- `channels.imessage.chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.

Related global options:

- `agents.list[].groupChat.mentionPatterns` (or `messages.groupChat.mentionPatterns`).

- `messages.responsePrefix`.

[Signal](/channels/signal)[Microsoft Teams](/channels/msteams)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)