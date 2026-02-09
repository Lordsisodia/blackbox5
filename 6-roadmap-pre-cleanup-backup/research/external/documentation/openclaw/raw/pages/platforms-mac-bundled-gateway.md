---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/bundled-gateway",
    "fetched_at": "2026-02-07T10:19:52.110914",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 502297
  },
  "metadata": {
    "title": "Gateway on macOS",
    "section": "bundled-gateway",
    "tier": 3,
    "type": "reference"
  }
}
---

- Gateway on macOS - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appGateway on macOS[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Gateway on macOS (external launchd)](#gateway-on-macos-external-launchd)- [Install the CLI (required for local mode)](#install-the-cli-required-for-local-mode)- [Launchd (Gateway as LaunchAgent)](#launchd-gateway-as-launchagent)- [Version compatibility](#version-compatibility)- [Smoke check](#smoke-check)macOS companion app# Gateway on macOS# [​](#gateway-on-macos-external-launchd)Gateway on macOS (external launchd)

OpenClaw.app no longer bundles Node/Bun or the Gateway runtime. The macOS app

expects an **external** `openclaw` CLI install, does not spawn the Gateway as a

child process, and manages a per‑user launchd service to keep the Gateway

running (or attaches to an existing local Gateway if one is already running).

## [​](#install-the-cli-required-for-local-mode)Install the CLI (required for local mode)

You need Node 22+ on the Mac, then install `openclaw` globally:

Copy```

npm install -g openclaw@<version>

```

The macOS app’s **Install CLI** button runs the same flow via npm/pnpm (bun not recommended for Gateway runtime).

## [​](#launchd-gateway-as-launchagent)Launchd (Gateway as LaunchAgent)

Label:

- `bot.molt.gateway` (or `bot.molt.<profile>`; legacy `com.openclaw.*` may remain)

Plist location (per‑user):

- `~/Library/LaunchAgents/bot.molt.gateway.plist`

(or `~/Library/LaunchAgents/bot.molt.<profile>.plist`)

Manager:

- The macOS app owns LaunchAgent install/update in Local mode.

- The CLI can also install it: `openclaw gateway install`.

Behavior:

- “OpenClaw Active” enables/disables the LaunchAgent.

- App quit does **not** stop the gateway (launchd keeps it alive).

- If a Gateway is already running on the configured port, the app attaches to

it instead of starting a new one.

Logging:

- launchd stdout/err: `/tmp/openclaw/openclaw-gateway.log`

## [​](#version-compatibility)Version compatibility

The macOS app checks the gateway version against its own version. If they’re

incompatible, update the global CLI to match the app version.

## [​](#smoke-check)Smoke check

Copy```

openclaw --version

OPENCLAW_SKIP_CHANNELS=1 \

OPENCLAW_SKIP_CANVAS_HOST=1 \

openclaw gateway --port 18999 --bind loopback

```

Then:

Copy```

openclaw gateway call health --url ws://127.0.0.1:18999 --timeout 3000

```[macOS Release](/platforms/mac/release)[macOS IPC](/platforms/mac/xpc)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)