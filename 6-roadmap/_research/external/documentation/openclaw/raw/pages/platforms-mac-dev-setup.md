---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/dev-setup",
    "fetched_at": "2026-02-07T10:20:25.020088",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 529804
  },
  "metadata": {
    "title": "macOS Dev Setup",
    "section": "dev-setup",
    "tier": 3,
    "type": "reference"
  }
}
---

- macOS Dev Setup - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appmacOS Dev Setup[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [macOS Developer Setup](#macos-developer-setup)- [Prerequisites](#prerequisites)- [1. Install Dependencies](#1-install-dependencies)- [2. Build and Package the App](#2-build-and-package-the-app)- [3. Install the CLI](#3-install-the-cli)- [Troubleshooting](#troubleshooting)- [Build Fails: Toolchain or SDK Mismatch](#build-fails-toolchain-or-sdk-mismatch)- [App Crashes on Permission Grant](#app-crashes-on-permission-grant)- [Gateway “Starting…” indefinitely](#gateway-%E2%80%9Cstarting%E2%80%A6%E2%80%9D-indefinitely)macOS companion app# macOS Dev Setup# [​](#macos-developer-setup)macOS Developer Setup

This guide covers the necessary steps to build and run the OpenClaw macOS application from source.

## [​](#prerequisites)Prerequisites

Before building the app, ensure you have the following installed:

- **Xcode 26.2+**: Required for Swift development.

- **Node.js 22+ & pnpm**: Required for the gateway, CLI, and packaging scripts.

## [​](#1-install-dependencies)1. Install Dependencies

Install the project-wide dependencies:

Copy```

pnpm install

```

## [​](#2-build-and-package-the-app)2. Build and Package the App

To build the macOS app and package it into `dist/OpenClaw.app`, run:

Copy```

./scripts/package-mac-app.sh

```

If you don’t have an Apple Developer ID certificate, the script will automatically use **ad-hoc signing** (`-`).

For dev run modes, signing flags, and Team ID troubleshooting, see the macOS app README:

[https://github.com/openclaw/openclaw/blob/main/apps/macos/README.md](https://github.com/openclaw/openclaw/blob/main/apps/macos/README.md)

**Note**: Ad-hoc signed apps may trigger security prompts. If the app crashes immediately with “Abort trap 6”, see the [Troubleshooting](#troubleshooting) section.

## [​](#3-install-the-cli)3. Install the CLI

The macOS app expects a global `openclaw` CLI install to manage background tasks.

**To install it (recommended):**

- Open the OpenClaw app.

- Go to the **General** settings tab.

- Click **“Install CLI”**.

Alternatively, install it manually:

Copy```

npm install -g openclaw@<version>

```

## [​](#troubleshooting)Troubleshooting

### [​](#build-fails-toolchain-or-sdk-mismatch)Build Fails: Toolchain or SDK Mismatch

The macOS app build expects the latest macOS SDK and Swift 6.2 toolchain.

**System dependencies (required):**

- **Latest macOS version available in Software Update** (required by Xcode 26.2 SDKs)

- **Xcode 26.2** (Swift 6.2 toolchain)

**Checks:**

Copy```

xcodebuild -version

xcrun swift --version

```

If versions don’t match, update macOS/Xcode and re-run the build.

### [​](#app-crashes-on-permission-grant)App Crashes on Permission Grant

If the app crashes when you try to allow **Speech Recognition** or **Microphone** access, it may be due to a corrupted TCC cache or signature mismatch.

**Fix:**

-

Reset the TCC permissions:

Copy```

tccutil reset All bot.molt.mac.debug

```

-

If that fails, change the `BUNDLE_ID` temporarily in [`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh) to force a “clean slate” from macOS.

### [​](#gateway-“starting…”-indefinitely)Gateway “Starting…” indefinitely

If the gateway status stays on “Starting…”, check if a zombie process is holding the port:

Copy```

openclaw gateway status

openclaw gateway stop

# If you’re not using a LaunchAgent (dev mode / manual runs), find the listener:

lsof -nP -iTCP:18789 -sTCP:LISTEN

```

If a manual run is holding the port, stop that process (Ctrl+C). As a last resort, kill the PID you found above.[iOS App](/platforms/ios)[Menu Bar](/platforms/mac/menu-bar)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)