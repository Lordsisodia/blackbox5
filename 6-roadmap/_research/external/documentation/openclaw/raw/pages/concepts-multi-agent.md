---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/multi-agent",
    "fetched_at": "2026-02-07T10:16:19.852861",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 875680
  },
  "metadata": {
    "title": "Multi-Agent Routing",
    "section": "multi-agent",
    "tier": 3,
    "type": "reference"
  }
}
---

- Multi-Agent Routing - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMulti-agentMulti-Agent Routing[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Fundamentals- [Gateway Architecture](/concepts/architecture)- [Agent Runtime](/concepts/agent)- [Agent Loop](/concepts/agent-loop)- [System Prompt](/concepts/system-prompt)- [Context](/concepts/context)- [Agent Workspace](/concepts/agent-workspace)- [Bootstrapping](/start/bootstrapping)- [OAuth](/concepts/oauth)Sessions and memory- [Session Management](/concepts/session)- [Sessions](/concepts/sessions)- [Session pruning](/concepts/session-pruning)- [Session Tools](/concepts/session-tool)- [Memory](/concepts/memory)- [Compaction](/concepts/compaction)Multi-agent- [Multi-Agent Routing](/concepts/multi-agent)- [Presence](/concepts/presence)Messages and delivery- [Messages](/concepts/messages)- [Streaming and Chunking](/concepts/streaming)- [Retry Policy](/concepts/retry)- [Command Queue](/concepts/queue)On this page- [Multi-Agent Routing](#multi-agent-routing)- [What is “one agent”?](#what-is-%E2%80%9Cone-agent%E2%80%9D)- [Paths (quick map)](#paths-quick-map)- [Single-agent mode (default)](#single-agent-mode-default)- [Agent helper](#agent-helper)- [Multiple agents = multiple people, multiple personalities](#multiple-agents-%3D-multiple-people-multiple-personalities)- [One WhatsApp number, multiple people (DM split)](#one-whatsapp-number-multiple-people-dm-split)- [Routing rules (how messages pick an agent)](#routing-rules-how-messages-pick-an-agent)- [Multiple accounts / phone numbers](#multiple-accounts-%2F-phone-numbers)- [Concepts](#concepts)- [Example: two WhatsApps → two agents](#example-two-whatsapps-%E2%86%92-two-agents)- [Example: WhatsApp daily chat + Telegram deep work](#example-whatsapp-daily-chat-%2B-telegram-deep-work)- [Example: same channel, one peer to Opus](#example-same-channel-one-peer-to-opus)- [Family agent bound to a WhatsApp group](#family-agent-bound-to-a-whatsapp-group)- [Per-Agent Sandbox and Tool Configuration](#per-agent-sandbox-and-tool-configuration)Multi-agent# Multi-Agent Routing# [​](#multi-agent-routing)Multi-Agent Routing

Goal: multiple *isolated* agents (separate workspace + `agentDir` + sessions), plus multiple channel accounts (e.g. two WhatsApps) in one running Gateway. Inbound is routed to an agent via bindings.

## [​](#what-is-“one-agent”)What is “one agent”?

An **agent** is a fully scoped brain with its own:

- **Workspace** (files, AGENTS.md/SOUL.md/USER.md, local notes, persona rules).

- **State directory** (`agentDir`) for auth profiles, model registry, and per-agent config.

- **Session store** (chat history + routing state) under `~/.openclaw/agents/<agentId>/sessions`.

Auth profiles are **per-agent**. Each agent reads from its own:

Copy```

~/.openclaw/agents/<agentId>/agent/auth-profiles.json

```

Main agent credentials are **not** shared automatically. Never reuse `agentDir`

across agents (it causes auth/session collisions). If you want to share creds,

copy `auth-profiles.json` into the other agent’s `agentDir`.

Skills are per-agent via each workspace’s `skills/` folder, with shared skills

available from `~/.openclaw/skills`. See [Skills: per-agent vs shared](/tools/skills#per-agent-vs-shared-skills).

The Gateway can host **one agent** (default) or **many agents** side-by-side.

**Workspace note:** each agent’s workspace is the **default cwd**, not a hard

sandbox. Relative paths resolve inside the workspace, but absolute paths can

reach other host locations unless sandboxing is enabled. See

[Sandboxing](/gateway/sandboxing).

## [​](#paths-quick-map)Paths (quick map)

- Config: `~/.openclaw/openclaw.json` (or `OPENCLAW_CONFIG_PATH`)

- State dir: `~/.openclaw` (or `OPENCLAW_STATE_DIR`)

- Workspace: `~/.openclaw/workspace` (or `~/.openclaw/workspace-<agentId>`)

- Agent dir: `~/.openclaw/agents/<agentId>/agent` (or `agents.list[].agentDir`)

- Sessions: `~/.openclaw/agents/<agentId>/sessions`

### [​](#single-agent-mode-default)Single-agent mode (default)

If you do nothing, OpenClaw runs a single agent:

- `agentId` defaults to **`main`**.

- Sessions are keyed as `agent:main:<mainKey>`.

- Workspace defaults to `~/.openclaw/workspace` (or `~/.openclaw/workspace-<profile>` when `OPENCLAW_PROFILE` is set).

- State defaults to `~/.openclaw/agents/main/agent`.

## [​](#agent-helper)Agent helper

Use the agent wizard to add a new isolated agent:

Copy```

openclaw agents add work

```

Then add `bindings` (or let the wizard do it) to route inbound messages.

Verify with:

Copy```

openclaw agents list --bindings

```

## [​](#multiple-agents-=-multiple-people-multiple-personalities)Multiple agents = multiple people, multiple personalities

With **multiple agents**, each `agentId` becomes a **fully isolated persona**:

- **Different phone numbers/accounts** (per channel `accountId`).

- **Different personalities** (per-agent workspace files like `AGENTS.md` and `SOUL.md`).

- **Separate auth + sessions** (no cross-talk unless explicitly enabled).

This lets **multiple people** share one Gateway server while keeping their AI “brains” and data isolated.

## [​](#one-whatsapp-number-multiple-people-dm-split)One WhatsApp number, multiple people (DM split)

You can route **different WhatsApp DMs** to different agents while staying on **one WhatsApp account**. Match on sender E.164 (like `+15551234567`) with `peer.kind: "dm"`. Replies still come from the same WhatsApp number (no per‑agent sender identity).

Important detail: direct chats collapse to the agent’s **main session key**, so true isolation requires **one agent per person**.

Example:

Copy```

{

agents: {

list: [

{ id: "alex", workspace: "~/.openclaw/workspace-alex" },

{ id: "mia", workspace: "~/.openclaw/workspace-mia" },

],

},

bindings: [

{ agentId: "alex", match: { channel: "whatsapp", peer: { kind: "dm", id: "+15551230001" } } },

{ agentId: "mia", match: { channel: "whatsapp", peer: { kind: "dm", id: "+15551230002" } } },

],

channels: {

whatsapp: {

dmPolicy: "allowlist",

allowFrom: ["+15551230001", "+15551230002"],

},

},

}

```

Notes:

- DM access control is **global per WhatsApp account** (pairing/allowlist), not per agent.

- For shared groups, bind the group to one agent or use [Broadcast groups](/broadcast-groups).

## [​](#routing-rules-how-messages-pick-an-agent)Routing rules (how messages pick an agent)

Bindings are **deterministic** and **most-specific wins**:

- `peer` match (exact DM/group/channel id)

- `guildId` (Discord)

- `teamId` (Slack)

- `accountId` match for a channel

- channel-level match (`accountId: "*"`)

- fallback to default agent (`agents.list[].default`, else first list entry, default: `main`)

## [​](#multiple-accounts-/-phone-numbers)Multiple accounts / phone numbers

Channels that support **multiple accounts** (e.g. WhatsApp) use `accountId` to identify

each login. Each `accountId` can be routed to a different agent, so one server can host

multiple phone numbers without mixing sessions.

## [​](#concepts)Concepts

- `agentId`: one “brain” (workspace, per-agent auth, per-agent session store).

- `accountId`: one channel account instance (e.g. WhatsApp account `"personal"` vs `"biz"`).

- `binding`: routes inbound messages to an `agentId` by `(channel, accountId, peer)` and optionally guild/team ids.

- Direct chats collapse to `agent:<agentId>:<mainKey>` (per-agent “main”; `session.mainKey`).

## [​](#example-two-whatsapps-→-two-agents)Example: two WhatsApps → two agents

`~/.openclaw/openclaw.json` (JSON5):

Copy```

{

agents: {

list: [

{

id: "home",

default: true,

name: "Home",

workspace: "~/.openclaw/workspace-home",

agentDir: "~/.openclaw/agents/home/agent",

},

{

id: "work",

name: "Work",

workspace: "~/.openclaw/workspace-work",

agentDir: "~/.openclaw/agents/work/agent",

},

],

},

// Deterministic routing: first match wins (most-specific first).

bindings: [

{ agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },

{ agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },

// Optional per-peer override (example: send a specific group to work agent).

{

agentId: "work",

match: {

channel: "whatsapp",

accountId: "personal",

peer: { kind: "group", id: "[[email protected]](/cdn-cgi/l/email-protection)" },

},

},

],

// Off by default: agent-to-agent messaging must be explicitly enabled + allowlisted.

tools: {

agentToAgent: {

enabled: false,

allow: ["home", "work"],

},

},

channels: {

whatsapp: {

accounts: {

personal: {

// Optional override. Default: ~/.openclaw/credentials/whatsapp/personal

// authDir: "~/.openclaw/credentials/whatsapp/personal",

},

biz: {

// Optional override. Default: ~/.openclaw/credentials/whatsapp/biz

// authDir: "~/.openclaw/credentials/whatsapp/biz",

},

},

},

},

}

```

## [​](#example-whatsapp-daily-chat-+-telegram-deep-work)Example: WhatsApp daily chat + Telegram deep work

Split by channel: route WhatsApp to a fast everyday agent and Telegram to an Opus agent.

Copy```

{

agents: {

list: [

{

id: "chat",

name: "Everyday",

workspace: "~/.openclaw/workspace-chat",

model: "anthropic/claude-sonnet-4-5",

},

{

id: "opus",

name: "Deep Work",

workspace: "~/.openclaw/workspace-opus",

model: "anthropic/claude-opus-4-6",

},

],

},

bindings: [

{ agentId: "chat", match: { channel: "whatsapp" } },

{ agentId: "opus", match: { channel: "telegram" } },

],

}

```

Notes:

- If you have multiple accounts for a channel, add `accountId` to the binding (for example `{ channel: "whatsapp", accountId: "personal" }`).

- To route a single DM/group to Opus while keeping the rest on chat, add a `match.peer` binding for that peer; peer matches always win over channel-wide rules.

## [​](#example-same-channel-one-peer-to-opus)Example: same channel, one peer to Opus

Keep WhatsApp on the fast agent, but route one DM to Opus:

Copy```

{

agents: {

list: [

{

id: "chat",

name: "Everyday",

workspace: "~/.openclaw/workspace-chat",

model: "anthropic/claude-sonnet-4-5",

},

{

id: "opus",

name: "Deep Work",

workspace: "~/.openclaw/workspace-opus",

model: "anthropic/claude-opus-4-6",

},

],

},

bindings: [

{ agentId: "opus", match: { channel: "whatsapp", peer: { kind: "dm", id: "+15551234567" } } },

{ agentId: "chat", match: { channel: "whatsapp" } },

],

}

```

Peer bindings always win, so keep them above the channel-wide rule.

## [​](#family-agent-bound-to-a-whatsapp-group)Family agent bound to a WhatsApp group

Bind a dedicated family agent to a single WhatsApp group, with mention gating

and a tighter tool policy:

Copy```

{

agents: {

list: [

{

id: "family",

name: "Family",

workspace: "~/.openclaw/workspace-family",

identity: { name: "Family Bot" },

groupChat: {

mentionPatterns: ["@family", "@familybot", "@Family Bot"],

},

sandbox: {

mode: "all",

scope: "agent",

},

tools: {

allow: [

"exec",

"read",

"sessions_list",

"sessions_history",

"sessions_send",

"sessions_spawn",

"session_status",

],

deny: ["write", "edit", "apply_patch", "browser", "canvas", "nodes", "cron"],

},

},

],

},

bindings: [

{

agentId: "family",

match: {

channel: "whatsapp",

peer: { kind: "group", id: "[[email protected]](/cdn-cgi/l/email-protection)" },

},

},

],

}

```

Notes:

- Tool allow/deny lists are **tools**, not skills. If a skill needs to run a

binary, ensure `exec` is allowed and the binary exists in the sandbox.

- For stricter gating, set `agents.list[].groupChat.mentionPatterns` and keep

group allowlists enabled for the channel.

## [​](#per-agent-sandbox-and-tool-configuration)Per-Agent Sandbox and Tool Configuration

Starting with v2026.1.6, each agent can have its own sandbox and tool restrictions:

Copy```

{

agents: {

list: [

{

id: "personal",

workspace: "~/.openclaw/workspace-personal",

sandbox: {

mode: "off",  // No sandbox for personal agent

},

// No tool restrictions - all tools available

},

{

id: "family",

workspace: "~/.openclaw/workspace-family",

sandbox: {

mode: "all",     // Always sandboxed

scope: "agent",  // One container per agent

docker: {

// Optional one-time setup after container creation

setupCommand: "apt-get update && apt-get install -y git curl",

},

},

tools: {

allow: ["read"],                    // Only read tool

deny: ["exec", "write", "edit", "apply_patch"],    // Deny others

},

},

],

},

}

```

Note: `setupCommand` lives under `sandbox.docker` and runs once on container creation.

Per-agent `sandbox.docker.*` overrides are ignored when the resolved scope is `"shared"`.

**Benefits:**

- **Security isolation**: Restrict tools for untrusted agents

- **Resource control**: Sandbox specific agents while keeping others on host

- **Flexible policies**: Different permissions per agent

Note: `tools.elevated` is **global** and sender-based; it is not configurable per agent.

If you need per-agent boundaries, use `agents.list[].tools` to deny `exec`.

For group targeting, use `agents.list[].groupChat.mentionPatterns` so @mentions map cleanly to the intended agent.

See [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools) for detailed examples.[Compaction](/concepts/compaction)[Presence](/concepts/presence)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)