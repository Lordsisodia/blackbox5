---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/session-pruning",
    "fetched_at": "2026-02-07T10:16:55.088300",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 544583
  },
  "metadata": {
    "title": "null",
    "section": "session-pruning",
    "tier": 3,
    "type": "reference"
  }
}
---

- Session pruning - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...Navigation[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Fundamentals- [Gateway Architecture](/concepts/architecture)- [Agent Runtime](/concepts/agent)- [Agent Loop](/concepts/agent-loop)- [System Prompt](/concepts/system-prompt)- [Context](/concepts/context)- [Agent Workspace](/concepts/agent-workspace)- [Bootstrapping](/start/bootstrapping)- [OAuth](/concepts/oauth)Sessions and memory- [Session Management](/concepts/session)- [Sessions](/concepts/sessions)- [Session pruning](/concepts/session-pruning)- [Session Tools](/concepts/session-tool)- [Memory](/concepts/memory)- [Compaction](/concepts/compaction)Multi-agent- [Multi-Agent Routing](/concepts/multi-agent)- [Presence](/concepts/presence)Messages and delivery- [Messages](/concepts/messages)- [Streaming and Chunking](/concepts/streaming)- [Retry Policy](/concepts/retry)- [Command Queue](/concepts/queue)On this page- [Session Pruning](#session-pruning)- [When it runs](#when-it-runs)- [Smart defaults (Anthropic)](#smart-defaults-anthropic)- [What this improves (cost + cache behavior)](#what-this-improves-cost-%2B-cache-behavior)- [What can be pruned](#what-can-be-pruned)- [Context window estimation](#context-window-estimation)- [Mode](#mode)- [cache-ttl](#cache-ttl)- [Soft vs hard pruning](#soft-vs-hard-pruning)- [Tool selection](#tool-selection)- [Interaction with other limits](#interaction-with-other-limits)- [Defaults (when enabled)](#defaults-when-enabled)- [Examples](#examples)Sessions and memory# Session pruning# [​](#session-pruning)Session Pruning

Session pruning trims **old tool results** from the in-memory context right before each LLM call. It does **not** rewrite the on-disk session history (`*.jsonl`).

## [​](#when-it-runs)When it runs

- When `mode: "cache-ttl"` is enabled and the last Anthropic call for the session is older than `ttl`.

- Only affects the messages sent to the model for that request.

- Only active for Anthropic API calls (and OpenRouter Anthropic models).

- For best results, match `ttl` to your model `cacheControlTtl`.

- After a prune, the TTL window resets so subsequent requests keep cache until `ttl` expires again.

## [​](#smart-defaults-anthropic)Smart defaults (Anthropic)

- **OAuth or setup-token** profiles: enable `cache-ttl` pruning and set heartbeat to `1h`.

- **API key** profiles: enable `cache-ttl` pruning, set heartbeat to `30m`, and default `cacheControlTtl` to `1h` on Anthropic models.

- If you set any of these values explicitly, OpenClaw does **not** override them.

## [​](#what-this-improves-cost-+-cache-behavior)What this improves (cost + cache behavior)

- **Why prune:** Anthropic prompt caching only applies within the TTL. If a session goes idle past the TTL, the next request re-caches the full prompt unless you trim it first.

- **What gets cheaper:** pruning reduces the **cacheWrite** size for that first request after the TTL expires.

- **Why the TTL reset matters:** once pruning runs, the cache window resets, so follow‑up requests can reuse the freshly cached prompt instead of re-caching the full history again.

- **What it does not do:** pruning doesn’t add tokens or “double” costs; it only changes what gets cached on that first post‑TTL request.

## [​](#what-can-be-pruned)What can be pruned

- Only `toolResult` messages.

- User + assistant messages are **never** modified.

- The last `keepLastAssistants` assistant messages are protected; tool results after that cutoff are not pruned.

- If there aren’t enough assistant messages to establish the cutoff, pruning is skipped.

- Tool results containing **image blocks** are skipped (never trimmed/cleared).

## [​](#context-window-estimation)Context window estimation

Pruning uses an estimated context window (chars ≈ tokens × 4). The base window is resolved in this order:

- `models.providers.*.models[].contextWindow` override.

- Model definition `contextWindow` (from the model registry).

- Default `200000` tokens.

If `agents.defaults.contextTokens` is set, it is treated as a cap (min) on the resolved window.

## [​](#mode)Mode

### [​](#cache-ttl)cache-ttl

- Pruning only runs if the last Anthropic call is older than `ttl` (default `5m`).

- When it runs: same soft-trim + hard-clear behavior as before.

## [​](#soft-vs-hard-pruning)Soft vs hard pruning

- **Soft-trim**: only for oversized tool results.

Keeps head + tail, inserts `...`, and appends a note with the original size.

- Skips results with image blocks.

- **Hard-clear**: replaces the entire tool result with `hardClear.placeholder`.

## [​](#tool-selection)Tool selection

- `tools.allow` / `tools.deny` support `*` wildcards.

- Deny wins.

- Matching is case-insensitive.

- Empty allow list => all tools allowed.

## [​](#interaction-with-other-limits)Interaction with other limits

- Built-in tools already truncate their own output; session pruning is an extra layer that prevents long-running chats from accumulating too much tool output in the model context.

- Compaction is separate: compaction summarizes and persists, pruning is transient per request. See [/concepts/compaction](/concepts/compaction).

## [​](#defaults-when-enabled)Defaults (when enabled)

- `ttl`: `"5m"`

- `keepLastAssistants`: `3`

- `softTrimRatio`: `0.3`

- `hardClearRatio`: `0.5`

- `minPrunableToolChars`: `50000`

- `softTrim`: `{ maxChars: 4000, headChars: 1500, tailChars: 1500 }`

- `hardClear`: `{ enabled: true, placeholder: "[Old tool result content cleared]" }`

## [​](#examples)Examples

Default (off):

Copy```

{

agent: {

contextPruning: { mode: "off" },

},

}

```

Enable TTL-aware pruning:

Copy```

{

agent: {

contextPruning: { mode: "cache-ttl", ttl: "5m" },

},

}

```

Restrict pruning to specific tools:

Copy```

{

agent: {

contextPruning: {

mode: "cache-ttl",

tools: { allow: ["exec", "read"], deny: ["*image*"] },

},

},

}

```

See config reference: [Gateway Configuration](/gateway/configuration)[Sessions](/concepts/sessions)[Session Tools](/concepts/session-tool)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)