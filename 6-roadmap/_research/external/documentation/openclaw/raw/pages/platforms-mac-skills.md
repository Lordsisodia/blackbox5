---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/skills",
    "fetched_at": "2026-02-07T10:11:12.348167",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 469936
  },
  "metadata": {
    "title": "Skills",
    "section": "skills",
    "tier": 2,
    "type": "reference"
  }
}
---

- Skills - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appSkills[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Skills (macOS)](#skills-macos)- [Data source](#data-source)- [Install actions](#install-actions)- [Env/API keys](#env%2Fapi-keys)- [Remote mode](#remote-mode)macOS companion app# Skills# [​](#skills-macos)Skills (macOS)

The macOS app surfaces OpenClaw skills via the gateway; it does not parse skills locally.

## [​](#data-source)Data source

- `skills.status` (gateway) returns all skills plus eligibility and missing requirements

(including allowlist blocks for bundled skills).

- Requirements are derived from `metadata.openclaw.requires` in each `SKILL.md`.

## [​](#install-actions)Install actions

- `metadata.openclaw.install` defines install options (brew/node/go/uv).

- The app calls `skills.install` to run installers on the gateway host.

- The gateway surfaces only one preferred installer when multiple are provided

(brew when available, otherwise node manager from `skills.install`, default npm).

## [​](#env/api-keys)Env/API keys

- The app stores keys in `~/.openclaw/openclaw.json` under `skills.entries.<skillKey>`.

- `skills.update` patches `enabled`, `apiKey`, and `env`.

## [​](#remote-mode)Remote mode

- Install + config updates happen on the gateway host (not the local Mac).

[macOS IPC](/platforms/mac/xpc)[Peekaboo Bridge](/platforms/mac/peekaboo)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)