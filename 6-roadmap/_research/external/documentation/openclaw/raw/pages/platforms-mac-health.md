---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/health",
    "fetched_at": "2026-02-07T10:20:25.830788",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 471735
  },
  "metadata": {
    "title": "Health Checks",
    "section": "health",
    "tier": 3,
    "type": "reference"
  }
}
---

- Health Checks - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appHealth Checks[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Health Checks on macOS](#health-checks-on-macos)- [Menu bar](#menu-bar)- [Settings](#settings)- [How the probe works](#how-the-probe-works)- [When in doubt](#when-in-doubt)macOS companion app# Health Checks# [​](#health-checks-on-macos)Health Checks on macOS

How to see whether the linked channel is healthy from the menu bar app.

## [​](#menu-bar)Menu bar

- Status dot now reflects Baileys health:

Green: linked + socket opened recently.

- Orange: connecting/retrying.

- Red: logged out or probe failed.

- Secondary line reads “linked · auth 12m” or shows the failure reason.

- “Run Health Check” menu item triggers an on-demand probe.

## [​](#settings)Settings

- General tab gains a Health card showing: linked auth age, session-store path/count, last check time, last error/status code, and buttons for Run Health Check / Reveal Logs.

- Uses a cached snapshot so the UI loads instantly and falls back gracefully when offline.

- **Channels tab** surfaces channel status + controls for WhatsApp/Telegram (login QR, logout, probe, last disconnect/error).

## [​](#how-the-probe-works)How the probe works

- App runs `openclaw health --json` via `ShellExecutor` every ~60s and on demand. The probe loads creds and reports status without sending messages.

- Cache the last good snapshot and the last error separately to avoid flicker; show the timestamp of each.

## [​](#when-in-doubt)When in doubt

- You can still use the CLI flow in [Gateway health](/gateway/health) (`openclaw status`, `openclaw status --deep`, `openclaw health --json`) and tail `/tmp/openclaw/openclaw-*.log` for `web-heartbeat` / `web-reconnect`.

[Gateway Lifecycle](/platforms/mac/child-process)[Menu Bar Icon](/platforms/mac/icon)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)