---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/reference/device-models",
    "fetched_at": "2026-02-07T10:21:50.720136",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 508868
  },
  "metadata": {
    "title": "Device Model Database",
    "section": "device-models",
    "tier": 3,
    "type": "reference"
  }
}
---

- Device Model Database - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationRPC and APIDevice Model Database[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [Device model database (friendly names)](#device-model-database-friendly-names)- [Data source](#data-source)- [Updating the database](#updating-the-database)RPC and API# Device Model Database# [​](#device-model-database-friendly-names)Device model database (friendly names)

The macOS companion app shows friendly Apple device model names in the **Instances** UI by mapping Apple model identifiers (e.g. `iPad16,6`, `Mac16,6`) to human-readable names.

The mapping is vendored as JSON under:

- `apps/macos/Sources/OpenClaw/Resources/DeviceModels/`

## [​](#data-source)Data source

We currently vendor the mapping from the MIT-licensed repository:

- `kyle-seongwoo-jun/apple-device-identifiers`

To keep builds deterministic, the JSON files are pinned to specific upstream commits (recorded in `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md`).

## [​](#updating-the-database)Updating the database

- Pick the upstream commits you want to pin to (one for iOS, one for macOS).

- Update the commit hashes in `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md`.

- Re-download the JSON files, pinned to those commits:

Copy```

IOS_COMMIT="<commit sha for ios-device-identifiers.json>"

MAC_COMMIT="<commit sha for mac-device-identifiers.json>"

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${IOS_COMMIT}/ios-device-identifiers.json" \

-o apps/macos/Sources/OpenClaw/Resources/DeviceModels/ios-device-identifiers.json

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${MAC_COMMIT}/mac-device-identifiers.json" \

-o apps/macos/Sources/OpenClaw/Resources/DeviceModels/mac-device-identifiers.json

```

- Ensure `apps/macos/Sources/OpenClaw/Resources/DeviceModels/LICENSE.apple-device-identifiers.txt` still matches upstream (replace it if the upstream license changes).

- Verify the macOS app builds cleanly (no warnings):

Copy```

swift build --package-path apps/macos

```[RPC Adapters](/reference/rpc)[AGENTS.default](/reference/AGENTS.default)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)