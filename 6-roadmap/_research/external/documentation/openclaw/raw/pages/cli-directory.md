---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/directory",
    "fetched_at": "2026-02-07T10:13:44.653395",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 548730
  },
  "metadata": {
    "title": "directory",
    "section": "directory",
    "tier": 3,
    "type": "reference"
  }
}
---

- directory - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandsdirectory[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw directory](#openclaw-directory)- [Common flags](#common-flags)- [Notes](#notes)- [Using results with message send](#using-results-with-message-send)- [ID formats (by channel)](#id-formats-by-channel)- [Self (“me”)](#self-%E2%80%9Cme%E2%80%9D)- [Peers (contacts/users)](#peers-contacts%2Fusers)- [Groups](#groups)CLI commands# directory# [​](#openclaw-directory)`openclaw directory`

Directory lookups for channels that support it (contacts/peers, groups, and “me”).

## [​](#common-flags)Common flags

- `--channel <name>`: channel id/alias (required when multiple channels are configured; auto when only one is configured)

- `--account <id>`: account id (default: channel default)

- `--json`: output JSON

## [​](#notes)Notes

- `directory` is meant to help you find IDs you can paste into other commands (especially `openclaw message send --target ...`).

- For many channels, results are config-backed (allowlists / configured groups) rather than a live provider directory.

- Default output is `id` (and sometimes `name`) separated by a tab; use `--json` for scripting.

## [​](#using-results-with-message-send)Using results with `message send`

Copy```

openclaw directory peers list --channel slack --query "U0"

openclaw message send --channel slack --target user:U012ABCDEF --message "hello"

```

## [​](#id-formats-by-channel)ID formats (by channel)

- WhatsApp: `+15551234567` (DM), `[[email protected]](/cdn-cgi/l/email-protection)` (group)

- Telegram: `@username` or numeric chat id; groups are numeric ids

- Slack: `user:U…` and `channel:C…`

- Discord: `user:<id>` and `channel:<id>`

- Matrix (plugin): `user:@user:server`, `room:!roomId:server`, or `#alias:server`

- Microsoft Teams (plugin): `user:<id>` and `conversation:<id>`

- Zalo (plugin): user id (Bot API)

- Zalo Personal / `zalouser` (plugin): thread id (DM/group) from `zca` (`me`, `friend list`, `group list`)

## [​](#self-“me”)Self (“me”)

Copy```

openclaw directory self --channel zalouser

```

## [​](#peers-contacts/users)Peers (contacts/users)

Copy```

openclaw directory peers list --channel zalouser

openclaw directory peers list --channel zalouser --query "name"

openclaw directory peers list --channel zalouser --limit 50

```

## [​](#groups)Groups

Copy```

openclaw directory groups list --channel zalouser

openclaw directory groups list --channel zalouser --query "work"

openclaw directory groups members --channel zalouser --group-id <id>

```[dashboard](/cli/dashboard)[dns](/cli/dns)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)