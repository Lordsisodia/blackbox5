---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/onboard",
    "fetched_at": "2026-02-07T10:15:25.767197",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 507752
  },
  "metadata": {
    "title": "onboard",
    "section": "onboard",
    "tier": 3,
    "type": "reference"
  }
}
---

- onboard - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandsonboard[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw onboard](#openclaw-onboard)- [Related guides](#related-guides)- [Examples](#examples)- [Common follow-up commands](#common-follow-up-commands)CLI commands# onboard# [​](#openclaw-onboard)`openclaw onboard`

Interactive onboarding wizard (local or remote Gateway setup).

## [​](#related-guides)Related guides

- CLI onboarding hub: [Onboarding Wizard (CLI)](/start/wizard)

- CLI onboarding reference: [CLI Onboarding Reference](/start/wizard-cli-reference)

- CLI automation: [CLI Automation](/start/wizard-cli-automation)

- macOS onboarding: [Onboarding (macOS App)](/start/onboarding)

## [​](#examples)Examples

Copy```

openclaw onboard

openclaw onboard --flow quickstart

openclaw onboard --flow manual

openclaw onboard --mode remote --remote-url ws://gateway-host:18789

```

Flow notes:

- `quickstart`: minimal prompts, auto-generates a gateway token.

- `manual`: full prompts for port/bind/auth (alias of `advanced`).

- Fastest first chat: `openclaw dashboard` (Control UI, no channel setup).

## [​](#common-follow-up-commands)Common follow-up commands

Copy```

openclaw configure

openclaw agents add <name>

```

`--json` does not imply non-interactive mode. Use `--non-interactive` for scripts.[nodes](/cli/nodes)[pairing](/cli/pairing)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)