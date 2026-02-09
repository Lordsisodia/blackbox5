---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/windows",
    "fetched_at": "2026-02-07T10:21:07.950238",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 610350
  },
  "metadata": {
    "title": "Windows (WSL2)",
    "section": "windows",
    "tier": 3,
    "type": "reference"
  }
}
---

- Windows (WSL2) - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationPlatforms overviewWindows (WSL2)[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Windows (WSL2)](#windows-wsl2)- [Install (WSL2)](#install-wsl2)- [Gateway](#gateway)- [Gateway service install (CLI)](#gateway-service-install-cli)- [Advanced: expose WSL services over LAN (portproxy)](#advanced-expose-wsl-services-over-lan-portproxy)- [Step-by-step WSL2 install](#step-by-step-wsl2-install)- [1) Install WSL2 + Ubuntu](#1-install-wsl2-%2B-ubuntu)- [2) Enable systemd (required for gateway install)](#2-enable-systemd-required-for-gateway-install)- [3) Install OpenClaw (inside WSL)](#3-install-openclaw-inside-wsl)- [Windows companion app](#windows-companion-app)Platforms overview# Windows (WSL2)# [​](#windows-wsl2)Windows (WSL2)

OpenClaw on Windows is recommended **via WSL2** (Ubuntu recommended). The

CLI + Gateway run inside Linux, which keeps the runtime consistent and makes

tooling far more compatible (Node/Bun/pnpm, Linux binaries, skills). Native

Windows might be trickier. WSL2 gives you the full Linux experience — one command

to install: `wsl --install`.

Native Windows companion apps are planned.

## [​](#install-wsl2)Install (WSL2)

- [Getting Started](/start/getting-started) (use inside WSL)

- [Install & updates](/install/updating)

- Official WSL2 guide (Microsoft): [https://learn.microsoft.com/windows/wsl/install](https://learn.microsoft.com/windows/wsl/install)

## [​](#gateway)Gateway

- [Gateway runbook](/gateway)

- [Configuration](/gateway/configuration)

## [​](#gateway-service-install-cli)Gateway service install (CLI)

Inside WSL2:

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

## [​](#advanced-expose-wsl-services-over-lan-portproxy)Advanced: expose WSL services over LAN (portproxy)

WSL has its own virtual network. If another machine needs to reach a service

running **inside WSL** (SSH, a local TTS server, or the Gateway), you must

forward a Windows port to the current WSL IP. The WSL IP changes after restarts,

so you may need to refresh the forwarding rule.

Example (PowerShell **as Administrator**):

Copy```

$Distro = "Ubuntu-24.04"

$ListenPort = 2222

$TargetPort = 22

$WslIp = (wsl -d $Distro -- hostname -I).Trim().Split(" ")[0]

if (-not $WslIp) { throw "WSL IP not found." }

netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=$ListenPort `

connectaddress=$WslIp connectport=$TargetPort

```

Allow the port through Windows Firewall (one-time):

Copy```

New-NetFirewallRule -DisplayName "WSL SSH $ListenPort" -Direction Inbound `

-Protocol TCP -LocalPort $ListenPort -Action Allow

```

Refresh the portproxy after WSL restarts:

Copy```

netsh interface portproxy delete v4tov4 listenport=$ListenPort listenaddress=0.0.0.0 | Out-Null

netsh interface portproxy add v4tov4 listenport=$ListenPort listenaddress=0.0.0.0 `

connectaddress=$WslIp connectport=$TargetPort | Out-Null

```

Notes:

- SSH from another machine targets the **Windows host IP** (example: `ssh user@windows-host -p 2222`).

- Remote nodes must point at a **reachable** Gateway URL (not `127.0.0.1`); use

`openclaw status --all` to confirm.

- Use `listenaddress=0.0.0.0` for LAN access; `127.0.0.1` keeps it local only.

- If you want this automatic, register a Scheduled Task to run the refresh

step at login.

## [​](#step-by-step-wsl2-install)Step-by-step WSL2 install

### [​](#1-install-wsl2-+-ubuntu)1) Install WSL2 + Ubuntu

Open PowerShell (Admin):

Copy```

wsl --install

# Or pick a distro explicitly:

wsl --list --online

wsl --install -d Ubuntu-24.04

```

Reboot if Windows asks.

### [​](#2-enable-systemd-required-for-gateway-install)2) Enable systemd (required for gateway install)

In your WSL terminal:

Copy```

sudo tee /etc/wsl.conf >/dev/null <<'EOF'

[boot]

systemd=true

EOF

```

Then from PowerShell:

Copy```

wsl --shutdown

```

Re-open Ubuntu, then verify:

Copy```

systemctl --user status

```

### [​](#3-install-openclaw-inside-wsl)3) Install OpenClaw (inside WSL)

Follow the Linux Getting Started flow inside WSL:

Copy```

git clone https://github.com/openclaw/openclaw.git

cd openclaw

pnpm install

pnpm ui:build # auto-installs UI deps on first run

pnpm build

openclaw onboard

```

Full guide: [Getting Started](/start/getting-started)

## [​](#windows-companion-app)Windows companion app

We do not have a Windows companion app yet. Contributions are welcome if you want

contributions to make it happen.[Linux App](/platforms/linux)[Android App](/platforms/android)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)