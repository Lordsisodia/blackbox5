---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/token-use",
    "fetched_at": "2026-02-07T10:23:11.219917",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 534453
  },
  "metadata": {
    "title": "Token Use and Costs",
    "section": "token-use",
    "tier": 3,
    "type": "reference"
  }
}
---

- Token Use and Costs - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationTechnical referenceToken Use and Costs[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [Token use & costs](#token-use-%26-costs)- [How the system prompt is built](#how-the-system-prompt-is-built)- [What counts in the context window](#what-counts-in-the-context-window)- [How to see current token usage](#how-to-see-current-token-usage)- [Cost estimation (when shown)](#cost-estimation-when-shown)- [Cache TTL and pruning impact](#cache-ttl-and-pruning-impact)- [Example: keep 1h cache warm with heartbeat](#example-keep-1h-cache-warm-with-heartbeat)- [Tips for reducing token pressure](#tips-for-reducing-token-pressure)Technical reference# Token Use and Costs# [​](#token-use-&-costs)Token use & costs

OpenClaw tracks **tokens**, not characters. Tokens are model-specific, but most

OpenAI-style models average ~4 characters per token for English text.

## [​](#how-the-system-prompt-is-built)How the system prompt is built

OpenClaw assembles its own system prompt on every run. It includes:

- Tool list + short descriptions

- Skills list (only metadata; instructions are loaded on demand with `read`)

- Self-update instructions

- Workspace + bootstrap files (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md` when new). Large files are truncated by `agents.defaults.bootstrapMaxChars` (default: 20000).

- Time (UTC + user timezone)

- Reply tags + heartbeat behavior

- Runtime metadata (host/OS/model/thinking)

See the full breakdown in [System Prompt](/concepts/system-prompt).

## [​](#what-counts-in-the-context-window)What counts in the context window

Everything the model receives counts toward the context limit:

- System prompt (all sections listed above)

- Conversation history (user + assistant messages)

- Tool calls and tool results

- Attachments/transcripts (images, audio, files)

- Compaction summaries and pruning artifacts

- Provider wrappers or safety headers (not visible, but still counted)

For a practical breakdown (per injected file, tools, skills, and system prompt size), use `/context list` or `/context detail`. See [Context](/concepts/context).

## [​](#how-to-see-current-token-usage)How to see current token usage

Use these in chat:

- `/status` → **emoji‑rich status card** with the session model, context usage,

last response input/output tokens, and **estimated cost** (API key only).

- `/usage off|tokens|full` → appends a **per-response usage footer** to every reply.

Persists per session (stored as `responseUsage`).

- OAuth auth **hides cost** (tokens only).

- `/usage cost` → shows a local cost summary from OpenClaw session logs.

Other surfaces:

- **TUI/Web TUI:** `/status` + `/usage` are supported.

- **CLI:** `openclaw status --usage` and `openclaw channels list` show

provider quota windows (not per-response costs).

## [​](#cost-estimation-when-shown)Cost estimation (when shown)

Costs are estimated from your model pricing config:

Copy```

models.providers.<provider>.models[].cost

```

These are **USD per 1M tokens** for `input`, `output`, `cacheRead`, and

`cacheWrite`. If pricing is missing, OpenClaw shows tokens only. OAuth tokens

never show dollar cost.

## [​](#cache-ttl-and-pruning-impact)Cache TTL and pruning impact

Provider prompt caching only applies within the cache TTL window. OpenClaw can

optionally run **cache-ttl pruning**: it prunes the session once the cache TTL

has expired, then resets the cache window so subsequent requests can re-use the

freshly cached context instead of re-caching the full history. This keeps cache

write costs lower when a session goes idle past the TTL.

Configure it in [Gateway configuration](/gateway/configuration) and see the

behavior details in [Session pruning](/concepts/session-pruning).

Heartbeat can keep the cache **warm** across idle gaps. If your model cache TTL

is `1h`, setting the heartbeat interval just under that (e.g., `55m`) can avoid

re-caching the full prompt, reducing cache write costs.

For Anthropic API pricing, cache reads are significantly cheaper than input

tokens, while cache writes are billed at a higher multiplier. See Anthropic’s

prompt caching pricing for the latest rates and TTL multipliers:

[https://docs.anthropic.com/docs/build-with-claude/prompt-caching](https://docs.anthropic.com/docs/build-with-claude/prompt-caching)

### [​](#example-keep-1h-cache-warm-with-heartbeat)Example: keep 1h cache warm with heartbeat

Copy```

agents:

defaults:

model:

primary: "anthropic/claude-opus-4-6"

models:

"anthropic/claude-opus-4-6":

params:

cacheRetention: "long"

heartbeat:

every: "55m"

```

## [​](#tips-for-reducing-token-pressure)Tips for reducing token pressure

- Use `/compact` to summarize long sessions.

- Trim large tool outputs in your workflows.

- Keep skill descriptions short (skill list is injected into the prompt).

- Prefer smaller models for verbose, exploratory work.

See [Skills](/tools/skills) for the exact skill list overhead formula.[Timezones](/concepts/timezone)[Credits](/reference/credits)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)