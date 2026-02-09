---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/reference/rpc",
    "fetched_at": "2026-02-07T10:21:51.309353",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 489329
  },
  "metadata": {
    "title": "RPC Adapters",
    "section": "rpc",
    "tier": 3,
    "type": "reference"
  }
}
---

- RPC Adapters - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationRPC and APIRPC Adapters[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [RPC adapters](#rpc-adapters)- [Pattern A: HTTP daemon (signal-cli)](#pattern-a-http-daemon-signal-cli)- [Pattern B: stdio child process (legacy: imsg)](#pattern-b-stdio-child-process-legacy-imsg)- [Adapter guidelines](#adapter-guidelines)RPC and API# RPC Adapters# [​](#rpc-adapters)RPC adapters

OpenClaw integrates external CLIs via JSON-RPC. Two patterns are used today.

## [​](#pattern-a-http-daemon-signal-cli)Pattern A: HTTP daemon (signal-cli)

- `signal-cli` runs as a daemon with JSON-RPC over HTTP.

- Event stream is SSE (`/api/v1/events`).

- Health probe: `/api/v1/check`.

- OpenClaw owns lifecycle when `channels.signal.autoStart=true`.

See [Signal](/channels/signal) for setup and endpoints.

## [​](#pattern-b-stdio-child-process-legacy-imsg)Pattern B: stdio child process (legacy: imsg)

**Note:** For new iMessage setups, use [BlueBubbles](/channels/bluebubbles) instead.

- OpenClaw spawns `imsg rpc` as a child process (legacy iMessage integration).

- JSON-RPC is line-delimited over stdin/stdout (one JSON object per line).

- No TCP port, no daemon required.

Core methods used:

- `watch.subscribe` → notifications (`method: "message"`)

- `watch.unsubscribe`

- `send`

- `chats.list` (probe/diagnostics)

See [iMessage](/channels/imessage) for legacy setup and addressing (`chat_id` preferred).

## [​](#adapter-guidelines)Adapter guidelines

- Gateway owns the process (start/stop tied to provider lifecycle).

- Keep RPC clients resilient: timeouts, restart on exit.

- Prefer stable IDs (e.g., `chat_id`) over display strings.

[voicecall](/cli/voicecall)[Device Model Database](/reference/device-models)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)