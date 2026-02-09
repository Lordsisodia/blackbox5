---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/plugins",
    "fetched_at": "2026-02-07T10:11:06.597898",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 537404
  },
  "metadata": {
    "title": "plugins",
    "section": "plugins",
    "tier": 2,
    "type": "reference"
  }
}
---

- plugins - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandsplugins[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw plugins](#openclaw-plugins)- [Commands](#commands)- [Install](#install)- [Update](#update)CLI commands# plugins# [​](#openclaw-plugins)`openclaw plugins`

Manage Gateway plugins/extensions (loaded in-process).

Related:

- Plugin system: [Plugins](/plugin)

- Plugin manifest + schema: [Plugin manifest](/plugins/manifest)

- Security hardening: [Security](/gateway/security)

## [​](#commands)Commands

Copy```

openclaw plugins list

openclaw plugins info <id>

openclaw plugins enable <id>

openclaw plugins disable <id>

openclaw plugins doctor

openclaw plugins update <id>

openclaw plugins update --all

```

Bundled plugins ship with OpenClaw but start disabled. Use `plugins enable` to

activate them.

All plugins must ship a `openclaw.plugin.json` file with an inline JSON Schema

(`configSchema`, even if empty). Missing/invalid manifests or schemas prevent

the plugin from loading and fail config validation.

### [​](#install)Install

Copy```

openclaw plugins install <path-or-spec>

```

Security note: treat plugin installs like running code. Prefer pinned versions.

Supported archives: `.zip`, `.tgz`, `.tar.gz`, `.tar`.

Use `--link` to avoid copying a local directory (adds to `plugins.load.paths`):

Copy```

openclaw plugins install -l ./my-plugin

```

### [​](#update)Update

Copy```

openclaw plugins update <id>

openclaw plugins update --all

openclaw plugins update <id> --dry-run

```

Updates only apply to plugins installed from npm (tracked in `plugins.installs`).[pairing](/cli/pairing)[reset](/cli/reset)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)