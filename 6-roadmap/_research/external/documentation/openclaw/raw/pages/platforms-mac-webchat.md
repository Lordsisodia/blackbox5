---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/webchat",
    "fetched_at": "2026-02-07T10:21:05.645797",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 478308
  },
  "metadata": {
    "title": "WebChat",
    "section": "webchat",
    "tier": 3,
    "type": "reference"
  }
}
---

- WebChat - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appWebChat[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [WebChat (macOS app)](#webchat-macos-app)- [Launch & debugging](#launch-%26-debugging)- [How it’s wired](#how-it%E2%80%99s-wired)- [Security surface](#security-surface)- [Known limitations](#known-limitations)macOS companion app# WebChat# [​](#webchat-macos-app)WebChat (macOS app)

The macOS menu bar app embeds the WebChat UI as a native SwiftUI view. It

connects to the Gateway and defaults to the **main session** for the selected

agent (with a session switcher for other sessions).

- **Local mode**: connects directly to the local Gateway WebSocket.

- **Remote mode**: forwards the Gateway control port over SSH and uses that

tunnel as the data plane.

## [​](#launch-&-debugging)Launch & debugging

-

Manual: Lobster menu → “Open Chat”.

-

Auto‑open for testing:

Copy```

dist/OpenClaw.app/Contents/MacOS/OpenClaw --webchat

```

-

Logs: `./scripts/clawlog.sh` (subsystem `bot.molt`, category `WebChatSwiftUI`).

## [​](#how-it’s-wired)How it’s wired

- Data plane: Gateway WS methods `chat.history`, `chat.send`, `chat.abort`,

`chat.inject` and events `chat`, `agent`, `presence`, `tick`, `health`.

- Session: defaults to the primary session (`main`, or `global` when scope is

global). The UI can switch between sessions.

- Onboarding uses a dedicated session to keep first‑run setup separate.

## [​](#security-surface)Security surface

- Remote mode forwards only the Gateway WebSocket control port over SSH.

## [​](#known-limitations)Known limitations

- The UI is optimized for chat sessions (not a full browser sandbox).

[Voice Overlay](/platforms/mac/voice-overlay)[Canvas](/platforms/mac/canvas)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)