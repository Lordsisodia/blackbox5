---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/channels",
    "fetched_at": "2026-02-07T10:13:39.811783",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 559847
  },
  "metadata": {
    "title": "channels",
    "section": "channels",
    "tier": 3,
    "type": "reference"
  }
}
---

- channels - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandschannels[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw channels](#openclaw-channels)- [Common commands](#common-commands)- [Add / remove accounts](#add-%2F-remove-accounts)- [Login / logout (interactive)](#login-%2F-logout-interactive)- [Troubleshooting](#troubleshooting)- [Capabilities probe](#capabilities-probe)- [Resolve names to IDs](#resolve-names-to-ids)CLI commands# channels# [​](#openclaw-channels)`openclaw channels`

Manage chat channel accounts and their runtime status on the Gateway.

Related docs:

- Channel guides: [Channels](/channels/index)

- Gateway configuration: [Configuration](/gateway/configuration)

## [​](#common-commands)Common commands

Copy```

openclaw channels list

openclaw channels status

openclaw channels capabilities

openclaw channels capabilities --channel discord --target channel:123

openclaw channels resolve --channel slack "#general" "@jane"

openclaw channels logs --channel all

```

## [​](#add-/-remove-accounts)Add / remove accounts

Copy```

openclaw channels add --channel telegram --token <bot-token>

openclaw channels remove --channel telegram --delete

```

Tip: `openclaw channels add --help` shows per-channel flags (token, app token, signal-cli paths, etc).

## [​](#login-/-logout-interactive)Login / logout (interactive)

Copy```

openclaw channels login --channel whatsapp

openclaw channels logout --channel whatsapp

```

## [​](#troubleshooting)Troubleshooting

- Run `openclaw status --deep` for a broad probe.

- Use `openclaw doctor` for guided fixes.

- `openclaw channels list` prints `Claude: HTTP 403 ... user:profile` → usage snapshot needs the `user:profile` scope. Use `--no-usage`, or provide a claude.ai session key (`CLAUDE_WEB_SESSION_KEY` / `CLAUDE_WEB_COOKIE`), or re-auth via Claude Code CLI.

## [​](#capabilities-probe)Capabilities probe

Fetch provider capability hints (intents/scopes where available) plus static feature support:

Copy```

openclaw channels capabilities

openclaw channels capabilities --channel discord --target channel:123

```

Notes:

- `--channel` is optional; omit it to list every channel (including extensions).

- `--target` accepts `channel:<id>` or a raw numeric channel id and only applies to Discord.

- Probes are provider-specific: Discord intents + optional channel permissions; Slack bot + user scopes; Telegram bot flags + webhook; Signal daemon version; MS Teams app token + Graph roles/scopes (annotated where known). Channels without probes report `Probe: unavailable`.

## [​](#resolve-names-to-ids)Resolve names to IDs

Resolve channel/user names to IDs using the provider directory:

Copy```

openclaw channels resolve --channel slack "#general" "@jane"

openclaw channels resolve --channel discord "My Server/#support" "@someone"

openclaw channels resolve --channel matrix "Project Room"

```

Notes:

- Use `--kind user|group|auto` to force the target type.

- Resolution prefers active matches when multiple entries share the same name.

[browser](/cli/browser)[configure](/cli/configure)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)