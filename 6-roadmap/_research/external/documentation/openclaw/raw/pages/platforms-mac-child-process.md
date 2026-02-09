---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/child-process",
    "fetched_at": "2026-02-07T10:20:24.428324",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 492330
  },
  "metadata": {
    "title": "Gateway Lifecycle",
    "section": "child-process",
    "tier": 3,
    "type": "reference"
  }
}
---

- Gateway Lifecycle - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appGateway Lifecycle[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Gateway lifecycle on macOS](#gateway-lifecycle-on-macos)- [Default behavior (launchd)](#default-behavior-launchd)- [Unsigned dev builds](#unsigned-dev-builds)- [Attach-only mode](#attach-only-mode)- [Remote mode](#remote-mode)- [Why we prefer launchd](#why-we-prefer-launchd)macOS companion app# Gateway Lifecycle# [​](#gateway-lifecycle-on-macos)Gateway lifecycle on macOS

The macOS app **manages the Gateway via launchd** by default and does not spawn

the Gateway as a child process. It first tries to attach to an already‑running

Gateway on the configured port; if none is reachable, it enables the launchd

service via the external `openclaw` CLI (no embedded runtime). This gives you

reliable auto‑start at login and restart on crashes.

Child‑process mode (Gateway spawned directly by the app) is **not in use** today.

If you need tighter coupling to the UI, run the Gateway manually in a terminal.

## [​](#default-behavior-launchd)Default behavior (launchd)

- The app installs a per‑user LaunchAgent labeled `bot.molt.gateway`

(or `bot.molt.<profile>` when using `--profile`/`OPENCLAW_PROFILE`; legacy `com.openclaw.*` is supported).

- When Local mode is enabled, the app ensures the LaunchAgent is loaded and

starts the Gateway if needed.

- Logs are written to the launchd gateway log path (visible in Debug Settings).

Common commands:

Copy```

launchctl kickstart -k gui/$UID/bot.molt.gateway

launchctl bootout gui/$UID/bot.molt.gateway

```

Replace the label with `bot.molt.<profile>` when running a named profile.

## [​](#unsigned-dev-builds)Unsigned dev builds

`scripts/restart-mac.sh --no-sign` is for fast local builds when you don’t have

signing keys. To prevent launchd from pointing at an unsigned relay binary, it:

- Writes `~/.openclaw/disable-launchagent`.

Signed runs of `scripts/restart-mac.sh` clear this override if the marker is

present. To reset manually:

Copy```

rm ~/.openclaw/disable-launchagent

```

## [​](#attach-only-mode)Attach-only mode

To force the macOS app to **never install or manage launchd**, launch it with

`--attach-only` (or `--no-launchd`). This sets `~/.openclaw/disable-launchagent`,

so the app only attaches to an already running Gateway. You can toggle the same

behavior in Debug Settings.

## [​](#remote-mode)Remote mode

Remote mode never starts a local Gateway. The app uses an SSH tunnel to the

remote host and connects over that tunnel.

## [​](#why-we-prefer-launchd)Why we prefer launchd

- Auto‑start at login.

- Built‑in restart/KeepAlive semantics.

- Predictable logs and supervision.

If a true child‑process mode is ever needed again, it should be documented as a

separate, explicit dev‑only mode.[Canvas](/platforms/mac/canvas)[Health Checks](/platforms/mac/health)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)