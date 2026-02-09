---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/streaming",
    "fetched_at": "2026-02-07T10:16:57.054600",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 523872
  },
  "metadata": {
    "title": "Streaming and Chunking",
    "section": "streaming",
    "tier": 3,
    "type": "reference"
  }
}
---

- Streaming and Chunking - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMessages and deliveryStreaming and Chunking[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Fundamentals- [Gateway Architecture](/concepts/architecture)- [Agent Runtime](/concepts/agent)- [Agent Loop](/concepts/agent-loop)- [System Prompt](/concepts/system-prompt)- [Context](/concepts/context)- [Agent Workspace](/concepts/agent-workspace)- [Bootstrapping](/start/bootstrapping)- [OAuth](/concepts/oauth)Sessions and memory- [Session Management](/concepts/session)- [Sessions](/concepts/sessions)- [Session pruning](/concepts/session-pruning)- [Session Tools](/concepts/session-tool)- [Memory](/concepts/memory)- [Compaction](/concepts/compaction)Multi-agent- [Multi-Agent Routing](/concepts/multi-agent)- [Presence](/concepts/presence)Messages and delivery- [Messages](/concepts/messages)- [Streaming and Chunking](/concepts/streaming)- [Retry Policy](/concepts/retry)- [Command Queue](/concepts/queue)On this page- [Streaming + chunking](#streaming-%2B-chunking)- [Block streaming (channel messages)](#block-streaming-channel-messages)- [Chunking algorithm (low/high bounds)](#chunking-algorithm-low%2Fhigh-bounds)- [Coalescing (merge streamed blocks)](#coalescing-merge-streamed-blocks)- [Human-like pacing between blocks](#human-like-pacing-between-blocks)- [“Stream chunks or everything”](#%E2%80%9Cstream-chunks-or-everything%E2%80%9D)- [Telegram draft streaming (token-ish)](#telegram-draft-streaming-token-ish)Messages and delivery# Streaming and Chunking# [​](#streaming-+-chunking)Streaming + chunking

OpenClaw has two separate “streaming” layers:

- **Block streaming (channels):** emit completed **blocks** as the assistant writes. These are normal channel messages (not token deltas).

- **Token-ish streaming (Telegram only):** update a **draft bubble** with partial text while generating; final message is sent at the end.

There is **no real token streaming** to external channel messages today. Telegram draft streaming is the only partial-stream surface.

## [​](#block-streaming-channel-messages)Block streaming (channel messages)

Block streaming sends assistant output in coarse chunks as it becomes available.

Copy```

Model output

└─ text_delta/events

├─ (blockStreamingBreak=text_end)

│    └─ chunker emits blocks as buffer grows

└─ (blockStreamingBreak=message_end)

└─ chunker flushes at message_end

└─ channel send (block replies)

```

Legend:

- `text_delta/events`: model stream events (may be sparse for non-streaming models).

- `chunker`: `EmbeddedBlockChunker` applying min/max bounds + break preference.

- `channel send`: actual outbound messages (block replies).

**Controls:**

- `agents.defaults.blockStreamingDefault`: `"on"`/`"off"` (default off).

- Channel overrides: `*.blockStreaming` (and per-account variants) to force `"on"`/`"off"` per channel.

- `agents.defaults.blockStreamingBreak`: `"text_end"` or `"message_end"`.

- `agents.defaults.blockStreamingChunk`: `{ minChars, maxChars, breakPreference? }`.

- `agents.defaults.blockStreamingCoalesce`: `{ minChars?, maxChars?, idleMs? }` (merge streamed blocks before send).

- Channel hard cap: `*.textChunkLimit` (e.g., `channels.whatsapp.textChunkLimit`).

- Channel chunk mode: `*.chunkMode` (`length` default, `newline` splits on blank lines (paragraph boundaries) before length chunking).

- Discord soft cap: `channels.discord.maxLinesPerMessage` (default 17) splits tall replies to avoid UI clipping.

**Boundary semantics:**

- `text_end`: stream blocks as soon as chunker emits; flush on each `text_end`.

- `message_end`: wait until assistant message finishes, then flush buffered output.

`message_end` still uses the chunker if the buffered text exceeds `maxChars`, so it can emit multiple chunks at the end.

## [​](#chunking-algorithm-low/high-bounds)Chunking algorithm (low/high bounds)

Block chunking is implemented by `EmbeddedBlockChunker`:

- **Low bound:** don’t emit until buffer >= `minChars` (unless forced).

- **High bound:** prefer splits before `maxChars`; if forced, split at `maxChars`.

- **Break preference:** `paragraph` → `newline` → `sentence` → `whitespace` → hard break.

- **Code fences:** never split inside fences; when forced at `maxChars`, close + reopen the fence to keep Markdown valid.

`maxChars` is clamped to the channel `textChunkLimit`, so you can’t exceed per-channel caps.

## [​](#coalescing-merge-streamed-blocks)Coalescing (merge streamed blocks)

When block streaming is enabled, OpenClaw can **merge consecutive block chunks**

before sending them out. This reduces “single-line spam” while still providing

progressive output.

- Coalescing waits for **idle gaps** (`idleMs`) before flushing.

- Buffers are capped by `maxChars` and will flush if they exceed it.

- `minChars` prevents tiny fragments from sending until enough text accumulates

(final flush always sends remaining text).

- Joiner is derived from `blockStreamingChunk.breakPreference`

(`paragraph` → `\n\n`, `newline` → `\n`, `sentence` → space).

- Channel overrides are available via `*.blockStreamingCoalesce` (including per-account configs).

- Default coalesce `minChars` is bumped to 1500 for Signal/Slack/Discord unless overridden.

## [​](#human-like-pacing-between-blocks)Human-like pacing between blocks

When block streaming is enabled, you can add a **randomized pause** between

block replies (after the first block). This makes multi-bubble responses feel

more natural.

- Config: `agents.defaults.humanDelay` (override per agent via `agents.list[].humanDelay`).

- Modes: `off` (default), `natural` (800–2500ms), `custom` (`minMs`/`maxMs`).

- Applies only to **block replies**, not final replies or tool summaries.

## [​](#“stream-chunks-or-everything”)“Stream chunks or everything”

This maps to:

- **Stream chunks:** `blockStreamingDefault: "on"` + `blockStreamingBreak: "text_end"` (emit as you go). Non-Telegram channels also need `*.blockStreaming: true`.

- **Stream everything at end:** `blockStreamingBreak: "message_end"` (flush once, possibly multiple chunks if very long).

- **No block streaming:** `blockStreamingDefault: "off"` (only final reply).

**Channel note:** For non-Telegram channels, block streaming is **off unless**

`*.blockStreaming` is explicitly set to `true`. Telegram can stream drafts

(`channels.telegram.streamMode`) without block replies.

Config location reminder: the `blockStreaming*` defaults live under

`agents.defaults`, not the root config.

## [​](#telegram-draft-streaming-token-ish)Telegram draft streaming (token-ish)

Telegram is the only channel with draft streaming:

- Uses Bot API `sendMessageDraft` in **private chats with topics**.

- `channels.telegram.streamMode: "partial" | "block" | "off"`.

`partial`: draft updates with the latest stream text.

- `block`: draft updates in chunked blocks (same chunker rules).

- `off`: no draft streaming.

- Draft chunk config (only for `streamMode: "block"`): `channels.telegram.draftChunk` (defaults: `minChars: 200`, `maxChars: 800`).

- Draft streaming is separate from block streaming; block replies are off by default and only enabled by `*.blockStreaming: true` on non-Telegram channels.

- Final reply is still a normal message.

- `/reasoning stream` writes reasoning into the draft bubble (Telegram only).

When draft streaming is active, OpenClaw disables block streaming for that reply to avoid double-streaming.

Copy```

Telegram (private + topics)

└─ sendMessageDraft (draft bubble)

├─ streamMode=partial → update latest text

└─ streamMode=block   → chunker updates draft

└─ final reply → normal message

```

Legend:

- `sendMessageDraft`: Telegram draft bubble (not a real message).

- `final reply`: normal Telegram message send.

[Messages](/concepts/messages)[Retry Policy](/concepts/retry)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)