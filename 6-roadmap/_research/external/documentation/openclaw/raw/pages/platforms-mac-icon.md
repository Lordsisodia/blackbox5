---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/icon",
    "fetched_at": "2026-02-07T10:20:56.538686",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 467382
  },
  "metadata": {
    "title": "Menu Bar Icon",
    "section": "icon",
    "tier": 3,
    "type": "reference"
  }
}
---

- Menu Bar Icon - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appMenu Bar Icon[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Menu Bar Icon States](#menu-bar-icon-states)macOS companion app# Menu Bar Icon# [​](#menu-bar-icon-states)Menu Bar Icon States

Author: steipete · Updated: 2025-12-06 · Scope: macOS app (`apps/macos`)

- **Idle:** Normal icon animation (blink, occasional wiggle).

- **Paused:** Status item uses `appearsDisabled`; no motion.

- **Voice trigger (big ears):** Voice wake detector calls `AppState.triggerVoiceEars(ttl: nil)` when the wake word is heard, keeping `earBoostActive=true` while the utterance is captured. Ears scale up (1.9x), get circular ear holes for readability, then drop via `stopVoiceEars()` after 1s of silence. Only fired from the in-app voice pipeline.

- **Working (agent running):** `AppState.isWorking=true` drives a “tail/leg scurry” micro-motion: faster leg wiggle and slight offset while work is in-flight. Currently toggled around WebChat agent runs; add the same toggle around other long tasks when you wire them.

Wiring points

- Voice wake: runtime/tester call `AppState.triggerVoiceEars(ttl: nil)` on trigger and `stopVoiceEars()` after 1s of silence to match the capture window.

- Agent activity: set `AppStateStore.shared.setWorking(true/false)` around work spans (already done in WebChat agent call). Keep spans short and reset in `defer` blocks to avoid stuck animations.

Shapes & sizes

- Base icon drawn in `CritterIconRenderer.makeIcon(blink:legWiggle:earWiggle:earScale:earHoles:)`.

- Ear scale defaults to `1.0`; voice boost sets `earScale=1.9` and toggles `earHoles=true` without changing overall frame (18×18 pt template image rendered into a 36×36 px Retina backing store).

- Scurry uses leg wiggle up to ~1.0 with a small horizontal jiggle; it’s additive to any existing idle wiggle.

Behavioral notes

- No external CLI/broker toggle for ears/working; keep it internal to the app’s own signals to avoid accidental flapping.

- Keep TTLs short (<10s) so the icon returns to baseline quickly if a job hangs.

[Health Checks](/platforms/mac/health)[macOS Logging](/platforms/mac/logging)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)