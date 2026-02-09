---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/typing-indicators",
    "fetched_at": "2026-02-07T10:17:00.242743",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 516417
  },
  "metadata": {
    "title": "Typing Indicators",
    "section": "typing-indicators",
    "tier": 3,
    "type": "reference"
  }
}
---

- Typing Indicators - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationTechnical referenceTyping Indicators[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [Typing indicators](#typing-indicators)- [Defaults](#defaults)- [Modes](#modes)- [Configuration](#configuration)- [Notes](#notes)Technical reference# Typing Indicators# [​](#typing-indicators)Typing indicators

Typing indicators are sent to the chat channel while a run is active. Use

`agents.defaults.typingMode` to control **when** typing starts and `typingIntervalSeconds`

to control **how often** it refreshes.

## [​](#defaults)Defaults

When `agents.defaults.typingMode` is **unset**, OpenClaw keeps the legacy behavior:

- **Direct chats**: typing starts immediately once the model loop begins.

- **Group chats with a mention**: typing starts immediately.

- **Group chats without a mention**: typing starts only when message text begins streaming.

- **Heartbeat runs**: typing is disabled.

## [​](#modes)Modes

Set `agents.defaults.typingMode` to one of:

- `never` — no typing indicator, ever.

- `instant` — start typing **as soon as the model loop begins**, even if the run

later returns only the silent reply token.

- `thinking` — start typing on the **first reasoning delta** (requires

`reasoningLevel: "stream"` for the run).

- `message` — start typing on the **first non-silent text delta** (ignores

the `NO_REPLY` silent token).

Order of “how early it fires”:

`never` → `message` → `thinking` → `instant`

## [​](#configuration)Configuration

Copy```

{

agent: {

typingMode: "thinking",

typingIntervalSeconds: 6,

},

}

```

You can override mode or cadence per session:

Copy```

{

session: {

typingMode: "message",

typingIntervalSeconds: 4,

},

}

```

## [​](#notes)Notes

- `message` mode won’t show typing for silent-only replies (e.g. the `NO_REPLY`

token used to suppress output).

- `thinking` only fires if the run streams reasoning (`reasoningLevel: "stream"`).

If the model doesn’t emit reasoning deltas, typing won’t start.

- Heartbeats never show typing, regardless of mode.

- `typingIntervalSeconds` controls the **refresh cadence**, not the start time.

The default is 6 seconds.

[Markdown Formatting](/concepts/markdown-formatting)[Usage Tracking](/concepts/usage-tracking)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)