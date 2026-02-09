---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/system",
    "fetched_at": "2026-02-07T10:15:34.515207",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 505997
  },
  "metadata": {
    "title": "system",
    "section": "system",
    "tier": 3,
    "type": "reference"
  }
}
---

- system - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandssystem[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw system](#openclaw-system)- [Common commands](#common-commands)- [system event](#system-event)- [system heartbeat last|enable|disable](#system-heartbeat-last%7Cenable%7Cdisable)- [system presence](#system-presence)- [Notes](#notes)CLI commands# system# [​](#openclaw-system)`openclaw system`

System-level helpers for the Gateway: enqueue system events, control heartbeats,

and view presence.

## [​](#common-commands)Common commands

Copy```

openclaw system event --text "Check for urgent follow-ups" --mode now

openclaw system heartbeat enable

openclaw system heartbeat last

openclaw system presence

```

## [​](#system-event)`system event`

Enqueue a system event on the **main** session. The next heartbeat will inject

it as a `System:` line in the prompt. Use `--mode now` to trigger the heartbeat

immediately; `next-heartbeat` waits for the next scheduled tick.

Flags:

- `--text <text>`: required system event text.

- `--mode <mode>`: `now` or `next-heartbeat` (default).

- `--json`: machine-readable output.

## [​](#system-heartbeat-last|enable|disable)`system heartbeat last|enable|disable`

Heartbeat controls:

- `last`: show the last heartbeat event.

- `enable`: turn heartbeats back on (use this if they were disabled).

- `disable`: pause heartbeats.

Flags:

- `--json`: machine-readable output.

## [​](#system-presence)`system presence`

List the current system presence entries the Gateway knows about (nodes,

instances, and similar status lines).

Flags:

- `--json`: machine-readable output.

## [​](#notes)Notes

- Requires a running Gateway reachable by your current config (local or remote).

- System events are ephemeral and not persisted across restarts.

[status](/cli/status)[tui](/cli/tui)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)