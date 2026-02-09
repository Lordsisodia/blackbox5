---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/timezone",
    "fetched_at": "2026-02-07T10:16:58.699058",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 540144
  },
  "metadata": {
    "title": "Timezones",
    "section": "timezone",
    "tier": 3,
    "type": "reference"
  }
}
---

- Timezones - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationTechnical referenceTimezones[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [Timezones](#timezones)- [Message envelopes (local by default)](#message-envelopes-local-by-default)- [Examples](#examples)- [Tool payloads (raw provider data + normalized fields)](#tool-payloads-raw-provider-data-%2B-normalized-fields)- [User timezone for the system prompt](#user-timezone-for-the-system-prompt)Technical reference# Timezones# [​](#timezones)Timezones

OpenClaw standardizes timestamps so the model sees a **single reference time**.

## [​](#message-envelopes-local-by-default)Message envelopes (local by default)

Inbound messages are wrapped in an envelope like:

Copy```

[Provider ... 2026-01-05 16:26 PST] message text

```

The timestamp in the envelope is **host-local by default**, with minutes precision.

You can override this with:

Copy```

{

agents: {

defaults: {

envelopeTimezone: "local", // "utc" | "local" | "user" | IANA timezone

envelopeTimestamp: "on", // "on" | "off"

envelopeElapsed: "on", // "on" | "off"

},

},

}

```

- `envelopeTimezone: "utc"` uses UTC.

- `envelopeTimezone: "user"` uses `agents.defaults.userTimezone` (falls back to host timezone).

- Use an explicit IANA timezone (e.g., `"Europe/Vienna"`) for a fixed offset.

- `envelopeTimestamp: "off"` removes absolute timestamps from envelope headers.

- `envelopeElapsed: "off"` removes elapsed time suffixes (the `+2m` style).

### [​](#examples)Examples

**Local (default):**

Copy```

[Signal Alice +1555 2026-01-18 00:19 PST] hello

```

**Fixed timezone:**

Copy```

[Signal Alice +1555 2026-01-18 06:19 GMT+1] hello

```

**Elapsed time:**

Copy```

[Signal Alice +1555 +2m 2026-01-18T05:19Z] follow-up

```

## [​](#tool-payloads-raw-provider-data-+-normalized-fields)Tool payloads (raw provider data + normalized fields)

Tool calls (`channels.discord.readMessages`, `channels.slack.readMessages`, etc.) return **raw provider timestamps**.

We also attach normalized fields for consistency:

- `timestampMs` (UTC epoch milliseconds)

- `timestampUtc` (ISO 8601 UTC string)

Raw provider fields are preserved.

## [​](#user-timezone-for-the-system-prompt)User timezone for the system prompt

Set `agents.defaults.userTimezone` to tell the model the user’s local time zone. If it is

unset, OpenClaw resolves the **host timezone at runtime** (no config write).

Copy```

{

agents: { defaults: { userTimezone: "America/Chicago" } },

}

```

The system prompt includes:

- `Current Date & Time` section with local time and timezone

- `Time format: 12-hour` or `24-hour`

You can control the prompt format with `agents.defaults.timeFormat` (`auto` | `12` | `24`).

See [Date & Time](/date-time) for the full behavior and examples.[Usage Tracking](/concepts/usage-tracking)[Token Use and Costs](/token-use)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)