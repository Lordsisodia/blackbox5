---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/status",
    "fetched_at": "2026-02-07T10:15:33.643287",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 487782
  },
  "metadata": {
    "title": "status",
    "section": "status",
    "tier": 3,
    "type": "reference"
  }
}
---

- status - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandsstatus[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw status](#openclaw-status)CLI commands# status# [​](#openclaw-status)`openclaw status`

Diagnostics for channels + sessions.

Copy```

openclaw status

openclaw status --all

openclaw status --deep

openclaw status --usage

```

Notes:

- `--deep` runs live probes (WhatsApp Web + Telegram + Discord + Google Chat + Slack + Signal).

- Output includes per-agent session stores when multiple agents are configured.

- Overview includes Gateway + node host service install/runtime status when available.

- Overview includes update channel + git SHA (for source checkouts).

- Update info surfaces in the Overview; if an update is available, status prints a hint to run `openclaw update` (see [Updating](/install/updating)).

[skills](/cli/skills)[system](/cli/system)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)