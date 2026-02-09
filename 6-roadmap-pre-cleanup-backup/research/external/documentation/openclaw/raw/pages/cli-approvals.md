---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/approvals",
    "fetched_at": "2026-02-07T10:13:38.253305",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 537216
  },
  "metadata": {
    "title": "approvals",
    "section": "approvals",
    "tier": 3,
    "type": "reference"
  }
}
---

- approvals - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandsapprovals[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw approvals](#openclaw-approvals)- [Common commands](#common-commands)- [Replace approvals from a file](#replace-approvals-from-a-file)- [Allowlist helpers](#allowlist-helpers)- [Notes](#notes)CLI commands# approvals# [​](#openclaw-approvals)`openclaw approvals`

Manage exec approvals for the **local host**, **gateway host**, or a **node host**.

By default, commands target the local approvals file on disk. Use `--gateway` to target the gateway, or `--node` to target a specific node.

Related:

- Exec approvals: [Exec approvals](/tools/exec-approvals)

- Nodes: [Nodes](/nodes)

## [​](#common-commands)Common commands

Copy```

openclaw approvals get

openclaw approvals get --node <id|name|ip>

openclaw approvals get --gateway

```

## [​](#replace-approvals-from-a-file)Replace approvals from a file

Copy```

openclaw approvals set --file ./exec-approvals.json

openclaw approvals set --node <id|name|ip> --file ./exec-approvals.json

openclaw approvals set --gateway --file ./exec-approvals.json

```

## [​](#allowlist-helpers)Allowlist helpers

Copy```

openclaw approvals allowlist add "~/Projects/**/bin/rg"

openclaw approvals allowlist add --agent main --node <id|name|ip> "/usr/bin/uptime"

openclaw approvals allowlist add --agent "*" "/usr/bin/uname"

openclaw approvals allowlist remove "~/Projects/**/bin/rg"

```

## [​](#notes)Notes

- `--node` uses the same resolver as `openclaw nodes` (id, name, ip, or id prefix).

- `--agent` defaults to `"*"`, which applies to all agents.

- The node host must advertise `system.execApprovals.get/set` (macOS app or headless node host).

- Approvals files are stored per host at `~/.openclaw/exec-approvals.json`.

[agents](/cli/agents)[browser](/cli/browser)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)