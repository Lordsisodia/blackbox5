---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/voicewake",
    "fetched_at": "2026-02-07T10:21:05.067224",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 493627
  },
  "metadata": {
    "title": "Voice Wake",
    "section": "voicewake",
    "tier": 3,
    "type": "reference"
  }
}
---

- Voice Wake - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appVoice Wake[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Voice Wake & Push-to-Talk](#voice-wake-%26-push-to-talk)- [Modes](#modes)- [Runtime behavior (wake-word)](#runtime-behavior-wake-word)- [Lifecycle invariants](#lifecycle-invariants)- [Sticky overlay failure mode (previous)](#sticky-overlay-failure-mode-previous)- [Push-to-talk specifics](#push-to-talk-specifics)- [User-facing settings](#user-facing-settings)- [Forwarding behavior](#forwarding-behavior)- [Forwarding payload](#forwarding-payload)- [Quick verification](#quick-verification)macOS companion app# Voice Wake# [​](#voice-wake-&-push-to-talk)Voice Wake & Push-to-Talk

## [​](#modes)Modes

- **Wake-word mode** (default): always-on Speech recognizer waits for trigger tokens (`swabbleTriggerWords`). On match it starts capture, shows the overlay with partial text, and auto-sends after silence.

- **Push-to-talk (Right Option hold)**: hold the right Option key to capture immediately—no trigger needed. The overlay appears while held; releasing finalizes and forwards after a short delay so you can tweak text.

## [​](#runtime-behavior-wake-word)Runtime behavior (wake-word)

- Speech recognizer lives in `VoiceWakeRuntime`.

- Trigger only fires when there’s a **meaningful pause** between the wake word and the next word (~0.55s gap). The overlay/chime can start on the pause even before the command begins.

- Silence windows: 2.0s when speech is flowing, 5.0s if only the trigger was heard.

- Hard stop: 120s to prevent runaway sessions.

- Debounce between sessions: 350ms.

- Overlay is driven via `VoiceWakeOverlayController` with committed/volatile coloring.

- After send, recognizer restarts cleanly to listen for the next trigger.

## [​](#lifecycle-invariants)Lifecycle invariants

- If Voice Wake is enabled and permissions are granted, the wake-word recognizer should be listening (except during an explicit push-to-talk capture).

- Overlay visibility (including manual dismiss via the X button) must never prevent the recognizer from resuming.

## [​](#sticky-overlay-failure-mode-previous)Sticky overlay failure mode (previous)

Previously, if the overlay got stuck visible and you manually closed it, Voice Wake could appear “dead” because the runtime’s restart attempt could be blocked by overlay visibility and no subsequent restart was scheduled.

Hardening:

- Wake runtime restart is no longer blocked by overlay visibility.

- Overlay dismiss completion triggers a `VoiceWakeRuntime.refresh(...)` via `VoiceSessionCoordinator`, so manual X-dismiss always resumes listening.

## [​](#push-to-talk-specifics)Push-to-talk specifics

- Hotkey detection uses a global `.flagsChanged` monitor for **right Option** (`keyCode 61` + `.option`). We only observe events (no swallowing).

- Capture pipeline lives in `VoicePushToTalk`: starts Speech immediately, streams partials to the overlay, and calls `VoiceWakeForwarder` on release.

- When push-to-talk starts we pause the wake-word runtime to avoid dueling audio taps; it restarts automatically after release.

- Permissions: requires Microphone + Speech; seeing events needs Accessibility/Input Monitoring approval.

- External keyboards: some may not expose right Option as expected—offer a fallback shortcut if users report misses.

## [​](#user-facing-settings)User-facing settings

- **Voice Wake** toggle: enables wake-word runtime.

- **Hold Cmd+Fn to talk**: enables the push-to-talk monitor. Disabled on macOS < 26.

- Language & mic pickers, live level meter, trigger-word table, tester (local-only; does not forward).

- Mic picker preserves the last selection if a device disconnects, shows a disconnected hint, and temporarily falls back to the system default until it returns.

- **Sounds**: chimes on trigger detect and on send; defaults to the macOS “Glass” system sound. You can pick any `NSSound`-loadable file (e.g. MP3/WAV/AIFF) for each event or choose **No Sound**.

## [​](#forwarding-behavior)Forwarding behavior

- When Voice Wake is enabled, transcripts are forwarded to the active gateway/agent (the same local vs remote mode used by the rest of the mac app).

- Replies are delivered to the **last-used main provider** (WhatsApp/Telegram/Discord/WebChat). If delivery fails, the error is logged and the run is still visible via WebChat/session logs.

## [​](#forwarding-payload)Forwarding payload

- `VoiceWakeForwarder.prefixedTranscript(_:)` prepends the machine hint before sending. Shared between wake-word and push-to-talk paths.

## [​](#quick-verification)Quick verification

- Toggle push-to-talk on, hold Cmd+Fn, speak, release: overlay should show partials then send.

- While holding, menu-bar ears should stay enlarged (uses `triggerVoiceEars(ttl:nil)`); they drop after release.

[Menu Bar](/platforms/mac/menu-bar)[Voice Overlay](/platforms/mac/voice-overlay)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)