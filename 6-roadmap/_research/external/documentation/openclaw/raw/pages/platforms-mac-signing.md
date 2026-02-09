---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/signing",
    "fetched_at": "2026-02-07T10:21:03.241454",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 496696
  },
  "metadata": {
    "title": "macOS Signing",
    "section": "signing",
    "tier": 3,
    "type": "reference"
  }
}
---

- macOS Signing - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appmacOS Signing[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [mac signing (debug builds)](#mac-signing-debug-builds)- [Usage](#usage)- [Ad-hoc Signing Note](#ad-hoc-signing-note)- [Build metadata for About](#build-metadata-for-about)- [Why](#why)macOS companion app# macOS Signing# [​](#mac-signing-debug-builds)mac signing (debug builds)

This app is usually built from [`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh), which now:

- sets a stable debug bundle identifier: `ai.openclaw.mac.debug`

- writes the Info.plist with that bundle id (override via `BUNDLE_ID=...`)

- calls [`scripts/codesign-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/codesign-mac-app.sh) to sign the main binary and app bundle so macOS treats each rebuild as the same signed bundle and keeps TCC permissions (notifications, accessibility, screen recording, mic, speech). For stable permissions, use a real signing identity; ad-hoc is opt-in and fragile (see [macOS permissions](/platforms/mac/permissions)).

- uses `CODESIGN_TIMESTAMP=auto` by default; it enables trusted timestamps for Developer ID signatures. Set `CODESIGN_TIMESTAMP=off` to skip timestamping (offline debug builds).

- inject build metadata into Info.plist: `OpenClawBuildTimestamp` (UTC) and `OpenClawGitCommit` (short hash) so the About pane can show build, git, and debug/release channel.

- **Packaging requires Node 22+**: the script runs TS builds and the Control UI build.

- reads `SIGN_IDENTITY` from the environment. Add `export SIGN_IDENTITY="Apple Development: Your Name (TEAMID)"` (or your Developer ID Application cert) to your shell rc to always sign with your cert. Ad-hoc signing requires explicit opt-in via `ALLOW_ADHOC_SIGNING=1` or `SIGN_IDENTITY="-"` (not recommended for permission testing).

- runs a Team ID audit after signing and fails if any Mach-O inside the app bundle is signed by a different Team ID. Set `SKIP_TEAM_ID_CHECK=1` to bypass.

## [​](#usage)Usage

Copy```

# from repo root

scripts/package-mac-app.sh               # auto-selects identity; errors if none found

SIGN_IDENTITY="Developer ID Application: Your Name" scripts/package-mac-app.sh   # real cert

ALLOW_ADHOC_SIGNING=1 scripts/package-mac-app.sh    # ad-hoc (permissions will not stick)

SIGN_IDENTITY="-" scripts/package-mac-app.sh        # explicit ad-hoc (same caveat)

DISABLE_LIBRARY_VALIDATION=1 scripts/package-mac-app.sh   # dev-only Sparkle Team ID mismatch workaround

```

### [​](#ad-hoc-signing-note)Ad-hoc Signing Note

When signing with `SIGN_IDENTITY="-"` (ad-hoc), the script automatically disables the **Hardened Runtime** (`--options runtime`). This is necessary to prevent crashes when the app attempts to load embedded frameworks (like Sparkle) that do not share the same Team ID. Ad-hoc signatures also break TCC permission persistence; see [macOS permissions](/platforms/mac/permissions) for recovery steps.

## [​](#build-metadata-for-about)Build metadata for About

`package-mac-app.sh` stamps the bundle with:

- `OpenClawBuildTimestamp`: ISO8601 UTC at package time

- `OpenClawGitCommit`: short git hash (or `unknown` if unavailable)

The About tab reads these keys to show version, build date, git commit, and whether it’s a debug build (via `#if DEBUG`). Run the packager to refresh these values after code changes.

## [​](#why)Why

TCC permissions are tied to the bundle identifier *and* code signature. Unsigned debug builds with changing UUIDs were causing macOS to forget grants after each rebuild. Signing the binaries (ad‑hoc by default) and keeping a fixed bundle id/path (`dist/OpenClaw.app`) preserves the grants between builds, matching the VibeTunnel approach.[Remote Control](/platforms/mac/remote)[macOS Release](/platforms/mac/release)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)