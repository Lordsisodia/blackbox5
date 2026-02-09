---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/agents",
    "fetched_at": "2026-02-07T10:13:37.661700",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 544015
  },
  "metadata": {
    "title": "agents",
    "section": "agents",
    "tier": 3,
    "type": "reference"
  }
}
---

- agents - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandsagents[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw agents](#openclaw-agents)- [Examples](#examples)- [Identity files](#identity-files)- [Set identity](#set-identity)CLI commands# agents# [​](#openclaw-agents)`openclaw agents`

Manage isolated agents (workspaces + auth + routing).

Related:

- Multi-agent routing: [Multi-Agent Routing](/concepts/multi-agent)

- Agent workspace: [Agent workspace](/concepts/agent-workspace)

## [​](#examples)Examples

Copy```

openclaw agents list

openclaw agents add work --workspace ~/.openclaw/workspace-work

openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity

openclaw agents set-identity --agent main --avatar avatars/openclaw.png

openclaw agents delete work

```

## [​](#identity-files)Identity files

Each agent workspace can include an `IDENTITY.md` at the workspace root:

- Example path: `~/.openclaw/workspace/IDENTITY.md`

- `set-identity --from-identity` reads from the workspace root (or an explicit `--identity-file`)

Avatar paths resolve relative to the workspace root.

## [​](#set-identity)Set identity

`set-identity` writes fields into `agents.list[].identity`:

- `name`

- `theme`

- `emoji`

- `avatar` (workspace-relative path, http(s) URL, or data URI)

Load from `IDENTITY.md`:

Copy```

openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity

```

Override fields explicitly:

Copy```

openclaw agents set-identity --agent main --name "OpenClaw" --emoji "🦞" --avatar avatars/openclaw.png

```

Config sample:

Copy```

{

agents: {

list: [

{

id: "main",

identity: {

name: "OpenClaw",

theme: "space lobster",

emoji: "🦞",

avatar: "avatars/openclaw.png",

},

},

],

},

}

```[agent](/cli/agent)[approvals](/cli/approvals)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)