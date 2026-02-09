---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/install/nix",
    "fetched_at": "2026-02-07T10:19:08.375184",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 509376
  },
  "metadata": {
    "title": "Nix",
    "section": "nix",
    "tier": 3,
    "type": "reference"
  }
}
---

- Nix - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationOther install methodsNix[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Install overview- [Install](/install)- [Installer Internals](/install/installer)Other install methods- [Docker](/install/docker)- [Nix](/install/nix)- [Ansible](/install/ansible)- [Bun (Experimental)](/install/bun)Maintenance- [Updating](/install/updating)- [Migration Guide](/install/migrating)- [Uninstall](/install/uninstall)Hosting and deployment- [Fly.io](/install/fly)- [Hetzner](/install/hetzner)- [GCP](/install/gcp)- [macOS VMs](/install/macos-vm)- [exe.dev](/install/exe-dev)- [Deploy on Railway](/install/railway)- [Deploy on Render](/install/render)- [Deploy on Northflank](/install/northflank)Advanced- [Development Channels](/install/development-channels)On this page- [Nix Installation](#nix-installation)- [Quick Start](#quick-start)- [What you get](#what-you-get)- [Nix Mode Runtime Behavior](#nix-mode-runtime-behavior)- [Config + state paths](#config-%2B-state-paths)- [Runtime behavior in Nix mode](#runtime-behavior-in-nix-mode)- [Packaging note (macOS)](#packaging-note-macos)- [Related](#related)Other install methods# Nix# [​](#nix-installation)Nix Installation

The recommended way to run OpenClaw with Nix is via **[nix-openclaw](https://github.com/openclaw/nix-openclaw)** — a batteries-included Home Manager module.

## [​](#quick-start)Quick Start

Paste this to your AI agent (Claude, Cursor, etc.):

Copy```

I want to set up nix-openclaw on my Mac.

Repository: github:openclaw/nix-openclaw

What I need you to do:

1. Check if Determinate Nix is installed (if not, install it)

2. Create a local flake at ~/code/openclaw-local using templates/agent-first/flake.nix

3. Help me create a Telegram bot (@BotFather) and get my chat ID (@userinfobot)

4. Set up secrets (bot token, Anthropic key) - plain files at ~/.secrets/ is fine

5. Fill in the template placeholders and run home-manager switch

6. Verify: launchd running, bot responds to messages

Reference the nix-openclaw README for module options.

```

**📦 Full guide: [github.com/openclaw/nix-openclaw](https://github.com/openclaw/nix-openclaw)**

The nix-openclaw repo is the source of truth for Nix installation. This page is just a quick overview.

## [​](#what-you-get)What you get

- Gateway + macOS app + tools (whisper, spotify, cameras) — all pinned

- Launchd service that survives reboots

- Plugin system with declarative config

- Instant rollback: `home-manager switch --rollback`

## [​](#nix-mode-runtime-behavior)Nix Mode Runtime Behavior

When `OPENCLAW_NIX_MODE=1` is set (automatic with nix-openclaw):

OpenClaw supports a **Nix mode** that makes configuration deterministic and disables auto-install flows.

Enable it by exporting:

Copy```

OPENCLAW_NIX_MODE=1

```

On macOS, the GUI app does not automatically inherit shell env vars. You can

also enable Nix mode via defaults:

Copy```

defaults write bot.molt.mac openclaw.nixMode -bool true

```

### [​](#config-+-state-paths)Config + state paths

OpenClaw reads JSON5 config from `OPENCLAW_CONFIG_PATH` and stores mutable data in `OPENCLAW_STATE_DIR`.

- `OPENCLAW_STATE_DIR` (default: `~/.openclaw`)

- `OPENCLAW_CONFIG_PATH` (default: `$OPENCLAW_STATE_DIR/openclaw.json`)

When running under Nix, set these explicitly to Nix-managed locations so runtime state and config

stay out of the immutable store.

### [​](#runtime-behavior-in-nix-mode)Runtime behavior in Nix mode

- Auto-install and self-mutation flows are disabled

- Missing dependencies surface Nix-specific remediation messages

- UI surfaces a read-only Nix mode banner when present

## [​](#packaging-note-macos)Packaging note (macOS)

The macOS packaging flow expects a stable Info.plist template at:

Copy```

apps/macos/Sources/OpenClaw/Resources/Info.plist

```

[`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh) copies this template into the app bundle and patches dynamic fields

(bundle ID, version/build, Git SHA, Sparkle keys). This keeps the plist deterministic for SwiftPM

packaging and Nix builds (which do not rely on a full Xcode toolchain).

## [​](#related)Related

- [nix-openclaw](https://github.com/openclaw/nix-openclaw) — full setup guide

- [Wizard](/start/wizard) — non-Nix CLI setup

- [Docker](/install/docker) — containerized setup

[Docker](/install/docker)[Ansible](/install/ansible)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)