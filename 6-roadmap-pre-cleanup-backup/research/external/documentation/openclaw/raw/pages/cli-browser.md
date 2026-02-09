---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/browser",
    "fetched_at": "2026-02-07T10:13:38.919807",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 582495
  },
  "metadata": {
    "title": "browser",
    "section": "browser",
    "tier": 3,
    "type": "reference"
  }
}
---

- browser - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandsbrowser[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw browser](#openclaw-browser)- [Common flags](#common-flags)- [Quick start (local)](#quick-start-local)- [Profiles](#profiles)- [Tabs](#tabs)- [Snapshot / screenshot / actions](#snapshot-%2F-screenshot-%2F-actions)- [Chrome extension relay (attach via toolbar button)](#chrome-extension-relay-attach-via-toolbar-button)- [Remote browser control (node host proxy)](#remote-browser-control-node-host-proxy)CLI commands# browser# [​](#openclaw-browser)`openclaw browser`

Manage OpenClaw’s browser control server and run browser actions (tabs, snapshots, screenshots, navigation, clicks, typing).

Related:

- Browser tool + API: [Browser tool](/tools/browser)

- Chrome extension relay: [Chrome extension](/tools/chrome-extension)

## [​](#common-flags)Common flags

- `--url <gatewayWsUrl>`: Gateway WebSocket URL (defaults to config).

- `--token <token>`: Gateway token (if required).

- `--timeout <ms>`: request timeout (ms).

- `--browser-profile <name>`: choose a browser profile (default from config).

- `--json`: machine-readable output (where supported).

## [​](#quick-start-local)Quick start (local)

Copy```

openclaw browser --browser-profile chrome tabs

openclaw browser --browser-profile openclaw start

openclaw browser --browser-profile openclaw open https://example.com

openclaw browser --browser-profile openclaw snapshot

```

## [​](#profiles)Profiles

Profiles are named browser routing configs. In practice:

- `openclaw`: launches/attaches to a dedicated OpenClaw-managed Chrome instance (isolated user data dir).

- `chrome`: controls your existing Chrome tab(s) via the Chrome extension relay.

Copy```

openclaw browser profiles

openclaw browser create-profile --name work --color "#FF5A36"

openclaw browser delete-profile --name work

```

Use a specific profile:

Copy```

openclaw browser --browser-profile work tabs

```

## [​](#tabs)Tabs

Copy```

openclaw browser tabs

openclaw browser open https://docs.openclaw.ai

openclaw browser focus <targetId>

openclaw browser close <targetId>

```

## [​](#snapshot-/-screenshot-/-actions)Snapshot / screenshot / actions

Snapshot:

Copy```

openclaw browser snapshot

```

Screenshot:

Copy```

openclaw browser screenshot

```

Navigate/click/type (ref-based UI automation):

Copy```

openclaw browser navigate https://example.com

openclaw browser click <ref>

openclaw browser type <ref> "hello"

```

## [​](#chrome-extension-relay-attach-via-toolbar-button)Chrome extension relay (attach via toolbar button)

This mode lets the agent control an existing Chrome tab that you attach manually (it does not auto-attach).

Install the unpacked extension to a stable path:

Copy```

openclaw browser extension install

openclaw browser extension path

```

Then Chrome → `chrome://extensions` → enable “Developer mode” → “Load unpacked” → select the printed folder.

Full guide: [Chrome extension](/tools/chrome-extension)

## [​](#remote-browser-control-node-host-proxy)Remote browser control (node host proxy)

If the Gateway runs on a different machine than the browser, run a **node host** on the machine that has Chrome/Brave/Edge/Chromium. The Gateway will proxy browser actions to that node (no separate browser control server required).

Use `gateway.nodes.browser.mode` to control auto-routing and `gateway.nodes.browser.node` to pin a specific node if multiple are connected.

Security + remote setup: [Browser tool](/tools/browser), [Remote access](/gateway/remote), [Tailscale](/gateway/tailscale), [Security](/gateway/security)[approvals](/cli/approvals)[channels](/cli/channels)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)