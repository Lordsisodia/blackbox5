---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/retry",
    "fetched_at": "2026-02-07T10:16:23.211542",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 506027
  },
  "metadata": {
    "title": "Retry Policy",
    "section": "retry",
    "tier": 3,
    "type": "reference"
  }
}
---

- Retry Policy - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMessages and deliveryRetry Policy[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Fundamentals- [Gateway Architecture](/concepts/architecture)- [Agent Runtime](/concepts/agent)- [Agent Loop](/concepts/agent-loop)- [System Prompt](/concepts/system-prompt)- [Context](/concepts/context)- [Agent Workspace](/concepts/agent-workspace)- [Bootstrapping](/start/bootstrapping)- [OAuth](/concepts/oauth)Sessions and memory- [Session Management](/concepts/session)- [Sessions](/concepts/sessions)- [Session pruning](/concepts/session-pruning)- [Session Tools](/concepts/session-tool)- [Memory](/concepts/memory)- [Compaction](/concepts/compaction)Multi-agent- [Multi-Agent Routing](/concepts/multi-agent)- [Presence](/concepts/presence)Messages and delivery- [Messages](/concepts/messages)- [Streaming and Chunking](/concepts/streaming)- [Retry Policy](/concepts/retry)- [Command Queue](/concepts/queue)On this page- [Retry policy](#retry-policy)- [Goals](#goals)- [Defaults](#defaults)- [Behavior](#behavior)- [Discord](#discord)- [Telegram](#telegram)- [Configuration](#configuration)- [Notes](#notes)Messages and delivery# Retry Policy# [​](#retry-policy)Retry policy

## [​](#goals)Goals

- Retry per HTTP request, not per multi-step flow.

- Preserve ordering by retrying only the current step.

- Avoid duplicating non-idempotent operations.

## [​](#defaults)Defaults

- Attempts: 3

- Max delay cap: 30000 ms

- Jitter: 0.1 (10 percent)

- Provider defaults:

Telegram min delay: 400 ms

- Discord min delay: 500 ms

## [​](#behavior)Behavior

### [​](#discord)Discord

- Retries only on rate-limit errors (HTTP 429).

- Uses Discord `retry_after` when available, otherwise exponential backoff.

### [​](#telegram)Telegram

- Retries on transient errors (429, timeout, connect/reset/closed, temporarily unavailable).

- Uses `retry_after` when available, otherwise exponential backoff.

- Markdown parse errors are not retried; they fall back to plain text.

## [​](#configuration)Configuration

Set retry policy per provider in `~/.openclaw/openclaw.json`:

Copy```

{

channels: {

telegram: {

retry: {

attempts: 3,

minDelayMs: 400,

maxDelayMs: 30000,

jitter: 0.1,

},

},

discord: {

retry: {

attempts: 3,

minDelayMs: 500,

maxDelayMs: 30000,

jitter: 0.1,

},

},

},

}

```

## [​](#notes)Notes

- Retries apply per request (message send, media upload, reaction, poll, sticker).

- Composite flows do not retry completed steps.

[Streaming and Chunking](/concepts/streaming)[Command Queue](/concepts/queue)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)