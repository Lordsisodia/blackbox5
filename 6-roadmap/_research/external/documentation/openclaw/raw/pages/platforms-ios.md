---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/ios",
    "fetched_at": "2026-02-07T10:19:50.944274",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 547203
  },
  "metadata": {
    "title": "iOS App",
    "section": "ios",
    "tier": 3,
    "type": "reference"
  }
}
---

- iOS App - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationPlatforms overviewiOS App[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [iOS App (Node)](#ios-app-node)- [What it does](#what-it-does)- [Requirements](#requirements)- [Quick start (pair + connect)](#quick-start-pair-%2B-connect)- [Discovery paths](#discovery-paths)- [Bonjour (LAN)](#bonjour-lan)- [Tailnet (cross-network)](#tailnet-cross-network)- [Manual host/port](#manual-host%2Fport)- [Canvas + A2UI](#canvas-%2B-a2ui)- [Canvas eval / snapshot](#canvas-eval-%2F-snapshot)- [Voice wake + talk mode](#voice-wake-%2B-talk-mode)- [Common errors](#common-errors)- [Related docs](#related-docs)Platforms overview# iOS App# [​](#ios-app-node)iOS App (Node)

Availability: internal preview. The iOS app is not publicly distributed yet.

## [​](#what-it-does)What it does

- Connects to a Gateway over WebSocket (LAN or tailnet).

- Exposes node capabilities: Canvas, Screen snapshot, Camera capture, Location, Talk mode, Voice wake.

- Receives `node.invoke` commands and reports node status events.

## [​](#requirements)Requirements

- Gateway running on another device (macOS, Linux, or Windows via WSL2).

- Network path:

Same LAN via Bonjour, **or**

- Tailnet via unicast DNS-SD (example domain: `openclaw.internal.`), **or**

- Manual host/port (fallback).

## [​](#quick-start-pair-+-connect)Quick start (pair + connect)

- Start the Gateway:

Copy```

openclaw gateway --port 18789

```

-

In the iOS app, open Settings and pick a discovered gateway (or enable Manual Host and enter host/port).

-

Approve the pairing request on the gateway host:

Copy```

openclaw nodes pending

openclaw nodes approve <requestId>

```

- Verify connection:

Copy```

openclaw nodes status

openclaw gateway call node.list --params "{}"

```

## [​](#discovery-paths)Discovery paths

### [​](#bonjour-lan)Bonjour (LAN)

The Gateway advertises `_openclaw-gw._tcp` on `local.`. The iOS app lists these automatically.

### [​](#tailnet-cross-network)Tailnet (cross-network)

If mDNS is blocked, use a unicast DNS-SD zone (choose a domain; example: `openclaw.internal.`) and Tailscale split DNS.

See [Bonjour](/gateway/bonjour) for the CoreDNS example.

### [​](#manual-host/port)Manual host/port

In Settings, enable **Manual Host** and enter the gateway host + port (default `18789`).

## [​](#canvas-+-a2ui)Canvas + A2UI

The iOS node renders a WKWebView canvas. Use `node.invoke` to drive it:

Copy```

openclaw nodes invoke --node "iOS Node" --command canvas.navigate --params '{"url":"http://<gateway-host>:18793/__openclaw__/canvas/"}'

```

Notes:

- The Gateway canvas host serves `/__openclaw__/canvas/` and `/__openclaw__/a2ui/`.

- The iOS node auto-navigates to A2UI on connect when a canvas host URL is advertised.

- Return to the built-in scaffold with `canvas.navigate` and `{"url":""}`.

### [​](#canvas-eval-/-snapshot)Canvas eval / snapshot

Copy```

openclaw nodes invoke --node "iOS Node" --command canvas.eval --params '{"javaScript":"(() => { const {ctx} = window.__openclaw; ctx.clearRect(0,0,innerWidth,innerHeight); ctx.lineWidth=6; ctx.strokeStyle=\"#ff2d55\"; ctx.beginPath(); ctx.moveTo(40,40); ctx.lineTo(innerWidth-40, innerHeight-40); ctx.stroke(); return \"ok\"; })()"}'

```

Copy```

openclaw nodes invoke --node "iOS Node" --command canvas.snapshot --params '{"maxWidth":900,"format":"jpeg"}'

```

## [​](#voice-wake-+-talk-mode)Voice wake + talk mode

- Voice wake and talk mode are available in Settings.

- iOS may suspend background audio; treat voice features as best-effort when the app is not active.

## [​](#common-errors)Common errors

- `NODE_BACKGROUND_UNAVAILABLE`: bring the iOS app to the foreground (canvas/camera/screen commands require it).

- `A2UI_HOST_NOT_CONFIGURED`: the Gateway did not advertise a canvas host URL; check `canvasHost` in [Gateway configuration](/gateway/configuration).

- Pairing prompt never appears: run `openclaw nodes pending` and approve manually.

- Reconnect fails after reinstall: the Keychain pairing token was cleared; re-pair the node.

## [​](#related-docs)Related docs

- [Pairing](/gateway/pairing)

- [Discovery](/gateway/discovery)

- [Bonjour](/gateway/bonjour)

[Android App](/platforms/android)[macOS Dev Setup](/platforms/mac/dev-setup)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)