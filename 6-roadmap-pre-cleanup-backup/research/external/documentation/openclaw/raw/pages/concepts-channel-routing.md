---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/channel-routing",
    "fetched_at": "2026-02-07T10:15:40.293359",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 543539
  },
  "metadata": {
    "title": "Channel Routing",
    "section": "channel-routing",
    "tier": 3,
    "type": "reference"
  }
}
---

- Channel Routing - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationConfigurationChannel Routing[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Chat Channels](/channels)Messaging platforms- [WhatsApp](/channels/whatsapp)- [Telegram](/channels/telegram)- [grammY](/channels/grammy)- [Discord](/channels/discord)- [Slack](/channels/slack)- [Feishu](/channels/feishu)- [Google Chat](/channels/googlechat)- [Mattermost](/channels/mattermost)- [Signal](/channels/signal)- [iMessage](/channels/imessage)- [Microsoft Teams](/channels/msteams)- [LINE](/channels/line)- [Matrix](/channels/matrix)- [Zalo](/channels/zalo)- [Zalo Personal](/channels/zalouser)Configuration- [Pairing](/start/pairing)- [Group Messages](/concepts/group-messages)- [Groups](/concepts/groups)- [Broadcast Groups](/broadcast-groups)- [Channel Routing](/concepts/channel-routing)- [Channel Location Parsing](/channels/location)- [Channel Troubleshooting](/channels/troubleshooting)On this page- [Channels & routing](#channels-%26-routing)- [Key terms](#key-terms)- [Session key shapes (examples)](#session-key-shapes-examples)- [Routing rules (how an agent is chosen)](#routing-rules-how-an-agent-is-chosen)- [Broadcast groups (run multiple agents)](#broadcast-groups-run-multiple-agents)- [Config overview](#config-overview)- [Session storage](#session-storage)- [WebChat behavior](#webchat-behavior)- [Reply context](#reply-context)Configuration# Channel Routing# [​](#channels-&-routing)Channels & routing

OpenClaw routes replies **back to the channel where a message came from**. The

model does not choose a channel; routing is deterministic and controlled by the

host configuration.

## [​](#key-terms)Key terms

- **Channel**: `whatsapp`, `telegram`, `discord`, `slack`, `signal`, `imessage`, `webchat`.

- **AccountId**: per‑channel account instance (when supported).

- **AgentId**: an isolated workspace + session store (“brain”).

- **SessionKey**: the bucket key used to store context and control concurrency.

## [​](#session-key-shapes-examples)Session key shapes (examples)

Direct messages collapse to the agent’s **main** session:

- `agent:<agentId>:<mainKey>` (default: `agent:main:main`)

Groups and channels remain isolated per channel:

- Groups: `agent:<agentId>:<channel>:group:<id>`

- Channels/rooms: `agent:<agentId>:<channel>:channel:<id>`

Threads:

- Slack/Discord threads append `:thread:<threadId>` to the base key.

- Telegram forum topics embed `:topic:<topicId>` in the group key.

Examples:

- `agent:main:telegram:group:-1001234567890:topic:42`

- `agent:main:discord:channel:123456:thread:987654`

## [​](#routing-rules-how-an-agent-is-chosen)Routing rules (how an agent is chosen)

Routing picks **one agent** for each inbound message:

- **Exact peer match** (`bindings` with `peer.kind` + `peer.id`).

- **Guild match** (Discord) via `guildId`.

- **Team match** (Slack) via `teamId`.

- **Account match** (`accountId` on the channel).

- **Channel match** (any account on that channel).

- **Default agent** (`agents.list[].default`, else first list entry, fallback to `main`).

The matched agent determines which workspace and session store are used.

## [​](#broadcast-groups-run-multiple-agents)Broadcast groups (run multiple agents)

Broadcast groups let you run **multiple agents** for the same peer **when OpenClaw would normally reply** (for example: in WhatsApp groups, after mention/activation gating).

Config:

Copy```

{

broadcast: {

strategy: "parallel",

"[[email protected]](/cdn-cgi/l/email-protection)": ["alfred", "baerbel"],

"+15555550123": ["support", "logger"],

},

}

```

See: [Broadcast Groups](/broadcast-groups).

## [​](#config-overview)Config overview

- `agents.list`: named agent definitions (workspace, model, etc.).

- `bindings`: map inbound channels/accounts/peers to agents.

Example:

Copy```

{

agents: {

list: [{ id: "support", name: "Support", workspace: "~/.openclaw/workspace-support" }],

},

bindings: [

{ match: { channel: "slack", teamId: "T123" }, agentId: "support" },

{ match: { channel: "telegram", peer: { kind: "group", id: "-100123" } }, agentId: "support" },

],

}

```

## [​](#session-storage)Session storage

Session stores live under the state directory (default `~/.openclaw`):

- `~/.openclaw/agents/<agentId>/sessions/sessions.json`

- JSONL transcripts live alongside the store

You can override the store path via `session.store` and `{agentId}` templating.

## [​](#webchat-behavior)WebChat behavior

WebChat attaches to the **selected agent** and defaults to the agent’s main

session. Because of this, WebChat lets you see cross‑channel context for that

agent in one place.

## [​](#reply-context)Reply context

Inbound replies include:

- `ReplyToId`, `ReplyToBody`, and `ReplyToSender` when available.

- Quoted context is appended to `Body` as a `[Replying to ...]` block.

This is consistent across channels.[Broadcast Groups](/broadcast-groups)[Channel Location Parsing](/channels/location)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)