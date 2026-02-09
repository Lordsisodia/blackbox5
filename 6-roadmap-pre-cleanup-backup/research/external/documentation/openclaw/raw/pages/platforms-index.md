---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/index",
    "fetched_at": "2026-02-07T10:19:50.359816",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 476195
  },
  "metadata": {
    "title": "Platforms",
    "section": "index",
    "tier": 3,
    "type": "reference"
  }
}
---

- Platforms - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationPlatforms overviewPlatforms[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Platforms](#platforms)- [Choose your OS](#choose-your-os)- [VPS & hosting](#vps-%26-hosting)- [Common links](#common-links)- [Gateway service install (CLI)](#gateway-service-install-cli)Platforms overview# Platforms# [​](#platforms)Platforms

OpenClaw core is written in TypeScript. **Node is the recommended runtime**.

Bun is not recommended for the Gateway (WhatsApp/Telegram bugs).

Companion apps exist for macOS (menu bar app) and mobile nodes (iOS/Android). Windows and

Linux companion apps are planned, but the Gateway is fully supported today.

Native companion apps for Windows are also planned; the Gateway is recommended via WSL2.

## [​](#choose-your-os)Choose your OS

- macOS: [macOS](/platforms/macos)

- iOS: [iOS](/platforms/ios)

- Android: [Android](/platforms/android)

- Windows: [Windows](/platforms/windows)

- Linux: [Linux](/platforms/linux)

## [​](#vps-&-hosting)VPS & hosting

- VPS hub: [VPS hosting](/vps)

- Fly.io: [Fly.io](/install/fly)

- Hetzner (Docker): [Hetzner](/install/hetzner)

- GCP (Compute Engine): [GCP](/install/gcp)

- exe.dev (VM + HTTPS proxy): [exe.dev](/install/exe-dev)

## [​](#common-links)Common links

- Install guide: [Getting Started](/start/getting-started)

- Gateway runbook: [Gateway](/gateway)

- Gateway configuration: [Configuration](/gateway/configuration)

- Service status: `openclaw gateway status`

## [​](#gateway-service-install-cli)Gateway service install (CLI)

Use one of these (all supported):

- Wizard (recommended): `openclaw onboard --install-daemon`

- Direct: `openclaw gateway install`

- Configure flow: `openclaw configure` → select **Gateway service**

- Repair/migrate: `openclaw doctor` (offers to install or fix the service)

The service target depends on OS:

- macOS: LaunchAgent (`bot.molt.gateway` or `bot.molt.<profile>`; legacy `com.openclaw.*`)

- Linux/WSL2: systemd user service (`openclaw-gateway[-<profile>].service`)

[macOS App](/platforms/macos)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)