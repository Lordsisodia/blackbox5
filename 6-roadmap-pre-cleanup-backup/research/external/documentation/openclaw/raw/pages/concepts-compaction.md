---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/compaction",
    "fetched_at": "2026-02-07T10:15:42.068935",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 485299
  },
  "metadata": {
    "title": "Compaction",
    "section": "compaction",
    "tier": 3,
    "type": "reference"
  }
}
---

- Compaction - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationSessions and memoryCompaction[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Fundamentals- [Gateway Architecture](/concepts/architecture)- [Agent Runtime](/concepts/agent)- [Agent Loop](/concepts/agent-loop)- [System Prompt](/concepts/system-prompt)- [Context](/concepts/context)- [Agent Workspace](/concepts/agent-workspace)- [Bootstrapping](/start/bootstrapping)- [OAuth](/concepts/oauth)Sessions and memory- [Session Management](/concepts/session)- [Sessions](/concepts/sessions)- [Session pruning](/concepts/session-pruning)- [Session Tools](/concepts/session-tool)- [Memory](/concepts/memory)- [Compaction](/concepts/compaction)Multi-agent- [Multi-Agent Routing](/concepts/multi-agent)- [Presence](/concepts/presence)Messages and delivery- [Messages](/concepts/messages)- [Streaming and Chunking](/concepts/streaming)- [Retry Policy](/concepts/retry)- [Command Queue](/concepts/queue)On this page- [Context Window & Compaction](#context-window-%26-compaction)- [What compaction is](#what-compaction-is)- [Configuration](#configuration)- [Auto-compaction (default on)](#auto-compaction-default-on)- [Manual compaction](#manual-compaction)- [Context window source](#context-window-source)- [Compaction vs pruning](#compaction-vs-pruning)- [Tips](#tips)Sessions and memory# Compaction# [​](#context-window-&-compaction)Context Window & Compaction

Every model has a **context window** (max tokens it can see). Long-running chats accumulate messages and tool results; once the window is tight, OpenClaw **compacts** older history to stay within limits.

## [​](#what-compaction-is)What compaction is

Compaction **summarizes older conversation** into a compact summary entry and keeps recent messages intact. The summary is stored in the session history, so future requests use:

- The compaction summary

- Recent messages after the compaction point

Compaction **persists** in the session’s JSONL history.

## [​](#configuration)Configuration

See [Compaction config & modes](/concepts/compaction) for the `agents.defaults.compaction` settings.

## [​](#auto-compaction-default-on)Auto-compaction (default on)

When a session nears or exceeds the model’s context window, OpenClaw triggers auto-compaction and may retry the original request using the compacted context.

You’ll see:

- `🧹 Auto-compaction complete` in verbose mode

- `/status` showing `🧹 Compactions: <count>`

Before compaction, OpenClaw can run a **silent memory flush** turn to store

durable notes to disk. See [Memory](/concepts/memory) for details and config.

## [​](#manual-compaction)Manual compaction

Use `/compact` (optionally with instructions) to force a compaction pass:

Copy```

/compact Focus on decisions and open questions

```

## [​](#context-window-source)Context window source

Context window is model-specific. OpenClaw uses the model definition from the configured provider catalog to determine limits.

## [​](#compaction-vs-pruning)Compaction vs pruning

- **Compaction**: summarises and **persists** in JSONL.

- **Session pruning**: trims old **tool results** only, **in-memory**, per request.

See [/concepts/session-pruning](/concepts/session-pruning) for pruning details.

## [​](#tips)Tips

- Use `/compact` when sessions feel stale or context is bloated.

- Large tool outputs are already truncated; pruning can further reduce tool-result buildup.

- If you need a fresh slate, `/new` or `/reset` starts a new session id.

[Memory](/concepts/memory)[Multi-Agent Routing](/concepts/multi-agent)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)