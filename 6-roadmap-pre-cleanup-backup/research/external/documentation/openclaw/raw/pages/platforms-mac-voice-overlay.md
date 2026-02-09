---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/voice-overlay",
    "fetched_at": "2026-02-07T10:21:04.115100",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 500181
  },
  "metadata": {
    "title": "Voice Overlay",
    "section": "voice-overlay",
    "tier": 3,
    "type": "reference"
  }
}
---

- Voice Overlay - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appVoice Overlay[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Voice Overlay Lifecycle (macOS)](#voice-overlay-lifecycle-macos)- [Current intent](#current-intent)- [Implemented (Dec 9, 2025)](#implemented-dec-9-2025)- [Next steps](#next-steps)- [Debugging checklist](#debugging-checklist)- [Migration steps (suggested)](#migration-steps-suggested)macOS companion app# Voice Overlay# [​](#voice-overlay-lifecycle-macos)Voice Overlay Lifecycle (macOS)

Audience: macOS app contributors. Goal: keep the voice overlay predictable when wake-word and push-to-talk overlap.

## [​](#current-intent)Current intent

- If the overlay is already visible from wake-word and the user presses the hotkey, the hotkey session *adopts* the existing text instead of resetting it. The overlay stays up while the hotkey is held. When the user releases: send if there is trimmed text, otherwise dismiss.

- Wake-word alone still auto-sends on silence; push-to-talk sends immediately on release.

## [​](#implemented-dec-9-2025)Implemented (Dec 9, 2025)

- Overlay sessions now carry a token per capture (wake-word or push-to-talk). Partial/final/send/dismiss/level updates are dropped when the token doesn’t match, avoiding stale callbacks.

- Push-to-talk adopts any visible overlay text as a prefix (so pressing the hotkey while the wake overlay is up keeps the text and appends new speech). It waits up to 1.5s for a final transcript before falling back to the current text.

- Chime/overlay logging is emitted at `info` in categories `voicewake.overlay`, `voicewake.ptt`, and `voicewake.chime` (session start, partial, final, send, dismiss, chime reason).

## [​](#next-steps)Next steps

- **VoiceSessionCoordinator (actor)**

Owns exactly one `VoiceSession` at a time.

- API (token-based): `beginWakeCapture`, `beginPushToTalk`, `updatePartial`, `endCapture`, `cancel`, `applyCooldown`.

- Drops callbacks that carry stale tokens (prevents old recognizers from reopening the overlay).

- **VoiceSession (model)**

Fields: `token`, `source` (wakeWord|pushToTalk), committed/volatile text, chime flags, timers (auto-send, idle), `overlayMode` (display|editing|sending), cooldown deadline.

- **Overlay binding**

`VoiceSessionPublisher` (`ObservableObject`) mirrors the active session into SwiftUI.

- `VoiceWakeOverlayView` renders only via the publisher; it never mutates global singletons directly.

- Overlay user actions (`sendNow`, `dismiss`, `edit`) call back into the coordinator with the session token.

- **Unified send path**

On `endCapture`: if trimmed text is empty → dismiss; else `performSend(session:)` (plays send chime once, forwards, dismisses).

- Push-to-talk: no delay; wake-word: optional delay for auto-send.

- Apply a short cooldown to the wake runtime after push-to-talk finishes so wake-word doesn’t immediately retrigger.

- **Logging**

Coordinator emits `.info` logs in subsystem `bot.molt`, categories `voicewake.overlay` and `voicewake.chime`.

- Key events: `session_started`, `adopted_by_push_to_talk`, `partial`, `finalized`, `send`, `dismiss`, `cancel`, `cooldown`.

## [​](#debugging-checklist)Debugging checklist

-

Stream logs while reproducing a sticky overlay:

Copy```

sudo log stream --predicate 'subsystem == "bot.molt" AND category CONTAINS "voicewake"' --level info --style compact

```

-

Verify only one active session token; stale callbacks should be dropped by the coordinator.

-

Ensure push-to-talk release always calls `endCapture` with the active token; if text is empty, expect `dismiss` without chime or send.

## [​](#migration-steps-suggested)Migration steps (suggested)

- Add `VoiceSessionCoordinator`, `VoiceSession`, and `VoiceSessionPublisher`.

- Refactor `VoiceWakeRuntime` to create/update/end sessions instead of touching `VoiceWakeOverlayController` directly.

- Refactor `VoicePushToTalk` to adopt existing sessions and call `endCapture` on release; apply runtime cooldown.

- Wire `VoiceWakeOverlayController` to the publisher; remove direct calls from runtime/PTT.

- Add integration tests for session adoption, cooldown, and empty-text dismissal.

[Voice Wake](/platforms/mac/voicewake)[WebChat](/platforms/mac/webchat)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)