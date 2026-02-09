---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/xpc",
    "fetched_at": "2026-02-07T10:21:06.747044",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 490431
  },
  "metadata": {
    "title": "macOS IPC",
    "section": "xpc",
    "tier": 3,
    "type": "reference"
  }
}
---

- macOS IPC - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appmacOS IPC[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [OpenClaw macOS IPC architecture](#openclaw-macos-ipc-architecture)- [Goals](#goals)- [How it works](#how-it-works)- [Gateway + node transport](#gateway-%2B-node-transport)- [Node service + app IPC](#node-service-%2B-app-ipc)- [PeekabooBridge (UI automation)](#peekaboobridge-ui-automation)- [Operational flows](#operational-flows)- [Hardening notes](#hardening-notes)macOS companion app# macOS IPC# [​](#openclaw-macos-ipc-architecture)OpenClaw macOS IPC architecture

**Current model:** a local Unix socket connects the **node host service** to the **macOS app** for exec approvals + `system.run`. A `openclaw-mac` debug CLI exists for discovery/connect checks; agent actions still flow through the Gateway WebSocket and `node.invoke`. UI automation uses PeekabooBridge.

## [​](#goals)Goals

- Single GUI app instance that owns all TCC-facing work (notifications, screen recording, mic, speech, AppleScript).

- A small surface for automation: Gateway + node commands, plus PeekabooBridge for UI automation.

- Predictable permissions: always the same signed bundle ID, launched by launchd, so TCC grants stick.

## [​](#how-it-works)How it works

### [​](#gateway-+-node-transport)Gateway + node transport

- The app runs the Gateway (local mode) and connects to it as a node.

- Agent actions are performed via `node.invoke` (e.g. `system.run`, `system.notify`, `canvas.*`).

### [​](#node-service-+-app-ipc)Node service + app IPC

- A headless node host service connects to the Gateway WebSocket.

- `system.run` requests are forwarded to the macOS app over a local Unix socket.

- The app performs the exec in UI context, prompts if needed, and returns output.

Diagram (SCI):

Copy```

Agent -> Gateway -> Node Service (WS)

|  IPC (UDS + token + HMAC + TTL)

v

Mac App (UI + TCC + system.run)

```

### [​](#peekaboobridge-ui-automation)PeekabooBridge (UI automation)

- UI automation uses a separate UNIX socket named `bridge.sock` and the PeekabooBridge JSON protocol.

- Host preference order (client-side): Peekaboo.app → Claude.app → OpenClaw.app → local execution.

- Security: bridge hosts require an allowed TeamID; DEBUG-only same-UID escape hatch is guarded by `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` (Peekaboo convention).

- See: [PeekabooBridge usage](/platforms/mac/peekaboo) for details.

## [​](#operational-flows)Operational flows

- Restart/rebuild: `SIGN_IDENTITY="Apple Development: <Developer Name> (<TEAMID>)" scripts/restart-mac.sh`

Kills existing instances

- Swift build + package

- Writes/bootstraps/kickstarts the LaunchAgent

- Single instance: app exits early if another instance with the same bundle ID is running.

## [​](#hardening-notes)Hardening notes

- Prefer requiring a TeamID match for all privileged surfaces.

- PeekabooBridge: `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` (DEBUG-only) may allow same-UID callers for local development.

- All communication remains local-only; no network sockets are exposed.

- TCC prompts originate only from the GUI app bundle; keep the signed bundle ID stable across rebuilds.

- IPC hardening: socket mode `0600`, token, peer-UID checks, HMAC challenge/response, short TTL.

[Gateway on macOS](/platforms/mac/bundled-gateway)[Skills](/platforms/mac/skills)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)