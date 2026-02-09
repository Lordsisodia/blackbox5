---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/nodes",
    "fetched_at": "2026-02-07T10:15:25.120284",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 548157
  },
  "metadata": {
    "title": "nodes",
    "section": "nodes",
    "tier": 3,
    "type": "reference"
  }
}
---

- nodes - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandsnodes[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw nodes](#openclaw-nodes)- [Common commands](#common-commands)- [Invoke / run](#invoke-%2F-run)- [Exec-style defaults](#exec-style-defaults)CLI commands# nodes# [​](#openclaw-nodes)`openclaw nodes`

Manage paired nodes (devices) and invoke node capabilities.

Related:

- Nodes overview: [Nodes](/nodes)

- Camera: [Camera nodes](/nodes/camera)

- Images: [Image nodes](/nodes/images)

Common options:

- `--url`, `--token`, `--timeout`, `--json`

## [​](#common-commands)Common commands

Copy```

openclaw nodes list

openclaw nodes list --connected

openclaw nodes list --last-connected 24h

openclaw nodes pending

openclaw nodes approve <requestId>

openclaw nodes status

openclaw nodes status --connected

openclaw nodes status --last-connected 24h

```

`nodes list` prints pending/paired tables. Paired rows include the most recent connect age (Last Connect).

Use `--connected` to only show currently-connected nodes. Use `--last-connected <duration>` to

filter to nodes that connected within a duration (e.g. `24h`, `7d`).

## [​](#invoke-/-run)Invoke / run

Copy```

openclaw nodes invoke --node <id|name|ip> --command <command> --params <json>

openclaw nodes run --node <id|name|ip> <command...>

openclaw nodes run --raw "git status"

openclaw nodes run --agent main --node <id|name|ip> --raw "git status"

```

Invoke flags:

- `--params <json>`: JSON object string (default `{}`).

- `--invoke-timeout <ms>`: node invoke timeout (default `15000`).

- `--idempotency-key <key>`: optional idempotency key.

### [​](#exec-style-defaults)Exec-style defaults

`nodes run` mirrors the model’s exec behavior (defaults + approvals):

- Reads `tools.exec.*` (plus `agents.list[].tools.exec.*` overrides).

- Uses exec approvals (`exec.approval.request`) before invoking `system.run`.

- `--node` can be omitted when `tools.exec.node` is set.

- Requires a node that advertises `system.run` (macOS companion app or headless node host).

Flags:

- `--cwd <path>`: working directory.

- `--env <key=val>`: env override (repeatable).

- `--command-timeout <ms>`: command timeout.

- `--invoke-timeout <ms>`: node invoke timeout (default `30000`).

- `--needs-screen-recording`: require screen recording permission.

- `--raw <command>`: run a shell string (`/bin/sh -lc` or `cmd.exe /c`).

- `--agent <id>`: agent-scoped approvals/allowlists (defaults to configured agent).

- `--ask <off|on-miss|always>`, `--security <deny|allowlist|full>`: overrides.

[models](/cli/models)[onboard](/cli/onboard)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)