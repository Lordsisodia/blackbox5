---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/agent",
    "fetched_at": "2026-02-07T10:15:37.815436",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 510073
  },
  "metadata": {
    "title": "Agent Runtime",
    "section": "agent",
    "tier": 3,
    "type": "reference"
  }
}
---

- Agent Runtime - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationFundamentalsAgent Runtime[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Fundamentals- [Gateway Architecture](/concepts/architecture)- [Agent Runtime](/concepts/agent)- [Agent Loop](/concepts/agent-loop)- [System Prompt](/concepts/system-prompt)- [Context](/concepts/context)- [Agent Workspace](/concepts/agent-workspace)- [Bootstrapping](/start/bootstrapping)- [OAuth](/concepts/oauth)Sessions and memory- [Session Management](/concepts/session)- [Sessions](/concepts/sessions)- [Session pruning](/concepts/session-pruning)- [Session Tools](/concepts/session-tool)- [Memory](/concepts/memory)- [Compaction](/concepts/compaction)Multi-agent- [Multi-Agent Routing](/concepts/multi-agent)- [Presence](/concepts/presence)Messages and delivery- [Messages](/concepts/messages)- [Streaming and Chunking](/concepts/streaming)- [Retry Policy](/concepts/retry)- [Command Queue](/concepts/queue)On this page- [Agent Runtime 🤖](#agent-runtime-)- [Workspace (required)](#workspace-required)- [Bootstrap files (injected)](#bootstrap-files-injected)- [Built-in tools](#built-in-tools)- [Skills](#skills)- [pi-mono integration](#pi-mono-integration)- [Sessions](#sessions)- [Steering while streaming](#steering-while-streaming)- [Model refs](#model-refs)- [Configuration (minimal)](#configuration-minimal)Fundamentals# Agent Runtime# [​](#agent-runtime-)Agent Runtime 🤖

OpenClaw runs a single embedded agent runtime derived from **pi-mono**.

## [​](#workspace-required)Workspace (required)

OpenClaw uses a single agent workspace directory (`agents.defaults.workspace`) as the agent’s **only** working directory (`cwd`) for tools and context.

Recommended: use `openclaw setup` to create `~/.openclaw/openclaw.json` if missing and initialize the workspace files.

Full workspace layout + backup guide: [Agent workspace](/concepts/agent-workspace)

If `agents.defaults.sandbox` is enabled, non-main sessions can override this with

per-session workspaces under `agents.defaults.sandbox.workspaceRoot` (see

[Gateway configuration](/gateway/configuration)).

## [​](#bootstrap-files-injected)Bootstrap files (injected)

Inside `agents.defaults.workspace`, OpenClaw expects these user-editable files:

- `AGENTS.md` — operating instructions + “memory”

- `SOUL.md` — persona, boundaries, tone

- `TOOLS.md` — user-maintained tool notes (e.g. `imsg`, `sag`, conventions)

- `BOOTSTRAP.md` — one-time first-run ritual (deleted after completion)

- `IDENTITY.md` — agent name/vibe/emoji

- `USER.md` — user profile + preferred address

On the first turn of a new session, OpenClaw injects the contents of these files directly into the agent context.

Blank files are skipped. Large files are trimmed and truncated with a marker so prompts stay lean (read the file for full content).

If a file is missing, OpenClaw injects a single “missing file” marker line (and `openclaw setup` will create a safe default template).

`BOOTSTRAP.md` is only created for a **brand new workspace** (no other bootstrap files present). If you delete it after completing the ritual, it should not be recreated on later restarts.

To disable bootstrap file creation entirely (for pre-seeded workspaces), set:

Copy```

{ agent: { skipBootstrap: true } }

```

## [​](#built-in-tools)Built-in tools

Core tools (read/exec/edit/write and related system tools) are always available,

subject to tool policy. `apply_patch` is optional and gated by

`tools.exec.applyPatch`. `TOOLS.md` does **not** control which tools exist; it’s

guidance for how *you* want them used.

## [​](#skills)Skills

OpenClaw loads skills from three locations (workspace wins on name conflict):

- Bundled (shipped with the install)

- Managed/local: `~/.openclaw/skills`

- Workspace: `<workspace>/skills`

Skills can be gated by config/env (see `skills` in [Gateway configuration](/gateway/configuration)).

## [​](#pi-mono-integration)pi-mono integration

OpenClaw reuses pieces of the pi-mono codebase (models/tools), but **session management, discovery, and tool wiring are OpenClaw-owned**.

- No pi-coding agent runtime.

- No `~/.pi/agent` or `<workspace>/.pi` settings are consulted.

## [​](#sessions)Sessions

Session transcripts are stored as JSONL at:

- `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`

The session ID is stable and chosen by OpenClaw.

Legacy Pi/Tau session folders are **not** read.

## [​](#steering-while-streaming)Steering while streaming

When queue mode is `steer`, inbound messages are injected into the current run.

The queue is checked **after each tool call**; if a queued message is present,

remaining tool calls from the current assistant message are skipped (error tool

results with “Skipped due to queued user message.”), then the queued user

message is injected before the next assistant response.

When queue mode is `followup` or `collect`, inbound messages are held until the

current turn ends, then a new agent turn starts with the queued payloads. See

[Queue](/concepts/queue) for mode + debounce/cap behavior.

Block streaming sends completed assistant blocks as soon as they finish; it is

**off by default** (`agents.defaults.blockStreamingDefault: "off"`).

Tune the boundary via `agents.defaults.blockStreamingBreak` (`text_end` vs `message_end`; defaults to text_end).

Control soft block chunking with `agents.defaults.blockStreamingChunk` (defaults to

800–1200 chars; prefers paragraph breaks, then newlines; sentences last).

Coalesce streamed chunks with `agents.defaults.blockStreamingCoalesce` to reduce

single-line spam (idle-based merging before send). Non-Telegram channels require

explicit `*.blockStreaming: true` to enable block replies.

Verbose tool summaries are emitted at tool start (no debounce); Control UI

streams tool output via agent events when available.

More details: [Streaming + chunking](/concepts/streaming).

## [​](#model-refs)Model refs

Model refs in config (for example `agents.defaults.model` and `agents.defaults.models`) are parsed by splitting on the **first** `/`.

- Use `provider/model` when configuring models.

- If the model ID itself contains `/` (OpenRouter-style), include the provider prefix (example: `openrouter/moonshotai/kimi-k2`).

- If you omit the provider, OpenClaw treats the input as an alias or a model for the **default provider** (only works when there is no `/` in the model ID).

## [​](#configuration-minimal)Configuration (minimal)

At minimum, set:

- `agents.defaults.workspace`

- `channels.whatsapp.allowFrom` (strongly recommended)

*Next: [Group Chats](/concepts/group-messages)* 🦞[Gateway Architecture](/concepts/architecture)[Agent Loop](/concepts/agent-loop)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)