---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/models",
    "fetched_at": "2026-02-07T10:15:24.504542",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 532389
  },
  "metadata": {
    "title": "models",
    "section": "models",
    "tier": 3,
    "type": "reference"
  }
}
---

- models - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandsmodels[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw models](#openclaw-models)- [Common commands](#common-commands)- [models status](#models-status)- [Aliases + fallbacks](#aliases-%2B-fallbacks)- [Auth profiles](#auth-profiles)CLI commands# models# [​](#openclaw-models)`openclaw models`

Model discovery, scanning, and configuration (default model, fallbacks, auth profiles).

Related:

- Providers + models: [Models](/providers/models)

- Provider auth setup: [Getting started](/start/getting-started)

## [​](#common-commands)Common commands

Copy```

openclaw models status

openclaw models list

openclaw models set <model-or-alias>

openclaw models scan

```

`openclaw models status` shows the resolved default/fallbacks plus an auth overview.

When provider usage snapshots are available, the OAuth/token status section includes

provider usage headers.

Add `--probe` to run live auth probes against each configured provider profile.

Probes are real requests (may consume tokens and trigger rate limits).

Use `--agent <id>` to inspect a configured agent’s model/auth state. When omitted,

the command uses `OPENCLAW_AGENT_DIR`/`PI_CODING_AGENT_DIR` if set, otherwise the

configured default agent.

Notes:

- `models set <model-or-alias>` accepts `provider/model` or an alias.

- Model refs are parsed by splitting on the **first** `/`. If the model ID includes `/` (OpenRouter-style), include the provider prefix (example: `openrouter/moonshotai/kimi-k2`).

- If you omit the provider, OpenClaw treats the input as an alias or a model for the **default provider** (only works when there is no `/` in the model ID).

### [​](#models-status)`models status`

Options:

- `--json`

- `--plain`

- `--check` (exit 1=expired/missing, 2=expiring)

- `--probe` (live probe of configured auth profiles)

- `--probe-provider <name>` (probe one provider)

- `--probe-profile <id>` (repeat or comma-separated profile ids)

- `--probe-timeout <ms>`

- `--probe-concurrency <n>`

- `--probe-max-tokens <n>`

- `--agent <id>` (configured agent id; overrides `OPENCLAW_AGENT_DIR`/`PI_CODING_AGENT_DIR`)

## [​](#aliases-+-fallbacks)Aliases + fallbacks

Copy```

openclaw models aliases list

openclaw models fallbacks list

```

## [​](#auth-profiles)Auth profiles

Copy```

openclaw models auth add

openclaw models auth login --provider <id>

openclaw models auth setup-token

openclaw models auth paste-token

```

`models auth login` runs a provider plugin’s auth flow (OAuth/API key). Use

`openclaw plugins list` to see which providers are installed.

Notes:

- `setup-token` prompts for a setup-token value (generate it with `claude setup-token` on any machine).

- `paste-token` accepts a token string generated elsewhere or from automation.

[message](/cli/message)[nodes](/cli/nodes)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)