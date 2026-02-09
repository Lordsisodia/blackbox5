---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/linux",
    "fetched_at": "2026-02-07T10:19:51.523367",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 509142
  },
  "metadata": {
    "title": "Linux App",
    "section": "linux",
    "tier": 3,
    "type": "reference"
  }
}
---

- Linux App - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationPlatforms overviewLinux App[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Linux App](#linux-app)- [Beginner quick path (VPS)](#beginner-quick-path-vps)- [Install](#install)- [Gateway](#gateway)- [Gateway service install (CLI)](#gateway-service-install-cli)- [System control (systemd user unit)](#system-control-systemd-user-unit)Platforms overview# Linux App# [​](#linux-app)Linux App

The Gateway is fully supported on Linux. **Node is the recommended runtime**.

Bun is not recommended for the Gateway (WhatsApp/Telegram bugs).

Native Linux companion apps are planned. Contributions are welcome if you want to help build one.

## [​](#beginner-quick-path-vps)Beginner quick path (VPS)

- Install Node 22+

- `npm i -g openclaw@latest`

- `openclaw onboard --install-daemon`

- From your laptop: `ssh -N -L 18789:127.0.0.1:18789 <user>@<host>`

- Open `http://127.0.0.1:18789/` and paste your token

Step-by-step VPS guide: [exe.dev](/install/exe-dev)

## [​](#install)Install

- [Getting Started](/start/getting-started)

- [Install & updates](/install/updating)

- Optional flows: [Bun (experimental)](/install/bun), [Nix](/install/nix), [Docker](/install/docker)

## [​](#gateway)Gateway

- [Gateway runbook](/gateway)

- [Configuration](/gateway/configuration)

## [​](#gateway-service-install-cli)Gateway service install (CLI)

Use one of these:

Copy```

openclaw onboard --install-daemon

```

Or:

Copy```

openclaw gateway install

```

Or:

Copy```

openclaw configure

```

Select **Gateway service** when prompted.

Repair/migrate:

Copy```

openclaw doctor

```

## [​](#system-control-systemd-user-unit)System control (systemd user unit)

OpenClaw installs a systemd **user** service by default. Use a **system**

service for shared or always-on servers. The full unit example and guidance

live in the [Gateway runbook](/gateway).

Minimal setup:

Create `~/.config/systemd/user/openclaw-gateway[-<profile>].service`:

Copy```

[Unit]

Description=OpenClaw Gateway (profile: <profile>, v<version>)

After=network-online.target

Wants=network-online.target

[Service]

ExecStart=/usr/local/bin/openclaw gateway --port 18789

Restart=always

RestartSec=5

[Install]

WantedBy=default.target

```

Enable it:

Copy```

systemctl --user enable --now openclaw-gateway[-<profile>].service

```[macOS App](/platforms/macos)[Windows (WSL2)](/platforms/windows)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)