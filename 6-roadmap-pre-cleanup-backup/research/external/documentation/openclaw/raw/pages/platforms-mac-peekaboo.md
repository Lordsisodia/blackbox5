---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/peekaboo",
    "fetched_at": "2026-02-07T10:21:01.230884",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 488149
  },
  "metadata": {
    "title": "Peekaboo Bridge",
    "section": "peekaboo",
    "tier": 3,
    "type": "reference"
  }
}
---

- Peekaboo Bridge - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appPeekaboo Bridge[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Peekaboo Bridge (macOS UI automation)](#peekaboo-bridge-macos-ui-automation)- [What this is (and isn’t)](#what-this-is-and-isn%E2%80%99t)- [Enable the bridge](#enable-the-bridge)- [Client discovery order](#client-discovery-order)- [Security & permissions](#security-%26-permissions)- [Snapshot behavior (automation)](#snapshot-behavior-automation)- [Troubleshooting](#troubleshooting)macOS companion app# Peekaboo Bridge# [​](#peekaboo-bridge-macos-ui-automation)Peekaboo Bridge (macOS UI automation)

OpenClaw can host **PeekabooBridge** as a local, permission‑aware UI automation

broker. This lets the `peekaboo` CLI drive UI automation while reusing the

macOS app’s TCC permissions.

## [​](#what-this-is-and-isn’t)What this is (and isn’t)

- **Host**: OpenClaw.app can act as a PeekabooBridge host.

- **Client**: use the `peekaboo` CLI (no separate `openclaw ui ...` surface).

- **UI**: visual overlays stay in Peekaboo.app; OpenClaw is a thin broker host.

## [​](#enable-the-bridge)Enable the bridge

In the macOS app:

- Settings → **Enable Peekaboo Bridge**

When enabled, OpenClaw starts a local UNIX socket server. If disabled, the host

is stopped and `peekaboo` will fall back to other available hosts.

## [​](#client-discovery-order)Client discovery order

Peekaboo clients typically try hosts in this order:

- Peekaboo.app (full UX)

- Claude.app (if installed)

- OpenClaw.app (thin broker)

Use `peekaboo bridge status --verbose` to see which host is active and which

socket path is in use. You can override with:

Copy```

export PEEKABOO_BRIDGE_SOCKET=/path/to/bridge.sock

```

## [​](#security-&-permissions)Security & permissions

- The bridge validates **caller code signatures**; an allowlist of TeamIDs is

enforced (Peekaboo host TeamID + OpenClaw app TeamID).

- Requests time out after ~10 seconds.

- If required permissions are missing, the bridge returns a clear error message

rather than launching System Settings.

## [​](#snapshot-behavior-automation)Snapshot behavior (automation)

Snapshots are stored in memory and expire automatically after a short window.

If you need longer retention, re‑capture from the client.

## [​](#troubleshooting)Troubleshooting

- If `peekaboo` reports “bridge client is not authorized”, ensure the client is

properly signed or run the host with `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1`

in **debug** mode only.

- If no hosts are found, open one of the host apps (Peekaboo.app or OpenClaw.app)

and confirm permissions are granted.

[Skills](/platforms/mac/skills)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)