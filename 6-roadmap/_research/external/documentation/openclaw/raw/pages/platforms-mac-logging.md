---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/logging",
    "fetched_at": "2026-02-07T10:20:58.393020",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 496609
  },
  "metadata": {
    "title": "macOS Logging",
    "section": "logging",
    "tier": 3,
    "type": "reference"
  }
}
---

- macOS Logging - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appmacOS Logging[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Logging (macOS)](#logging-macos)- [Rolling diagnostics file log (Debug pane)](#rolling-diagnostics-file-log-debug-pane)- [Unified logging private data on macOS](#unified-logging-private-data-on-macos)- [Enable for OpenClaw (bot.molt)](#enable-for-openclaw-bot-molt)- [Disable after debugging](#disable-after-debugging)macOS companion app# macOS Logging# [​](#logging-macos)Logging (macOS)

## [​](#rolling-diagnostics-file-log-debug-pane)Rolling diagnostics file log (Debug pane)

OpenClaw routes macOS app logs through swift-log (unified logging by default) and can write a local, rotating file log to disk when you need a durable capture.

- Verbosity: **Debug pane → Logs → App logging → Verbosity**

- Enable: **Debug pane → Logs → App logging → “Write rolling diagnostics log (JSONL)”**

- Location: `~/Library/Logs/OpenClaw/diagnostics.jsonl` (rotates automatically; old files are suffixed with `.1`, `.2`, …)

- Clear: **Debug pane → Logs → App logging → “Clear”**

Notes:

- This is **off by default**. Enable only while actively debugging.

- Treat the file as sensitive; don’t share it without review.

## [​](#unified-logging-private-data-on-macos)Unified logging private data on macOS

Unified logging redacts most payloads unless a subsystem opts into `privacy -off`. Per Peter’s write-up on macOS [logging privacy shenanigans](https://steipete.me/posts/2025/logging-privacy-shenanigans) (2025) this is controlled by a plist in `/Library/Preferences/Logging/Subsystems/` keyed by the subsystem name. Only new log entries pick up the flag, so enable it before reproducing an issue.

## [​](#enable-for-openclaw-bot-molt)Enable for OpenClaw (`bot.molt`)

- Write the plist to a temp file first, then install it atomically as root:

Copy```

cat <<'EOF' >/tmp/bot.molt.plist

<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">

<plist version="1.0">

<dict>

<key>DEFAULT-OPTIONS</key>

<dict>

<key>Enable-Private-Data</key>

<true/>

</dict>

</dict>

</plist>

EOF

sudo install -m 644 -o root -g wheel /tmp/bot.molt.plist /Library/Preferences/Logging/Subsystems/bot.molt.plist

```

- No reboot is required; logd notices the file quickly, but only new log lines will include private payloads.

- View the richer output with the existing helper, e.g. `./scripts/clawlog.sh --category WebChat --last 5m`.

## [​](#disable-after-debugging)Disable after debugging

- Remove the override: `sudo rm /Library/Preferences/Logging/Subsystems/bot.molt.plist`.

- Optionally run `sudo log config --reload` to force logd to drop the override immediately.

- Remember this surface can include phone numbers and message bodies; keep the plist in place only while you actively need the extra detail.

[Menu Bar Icon](/platforms/mac/icon)[macOS Permissions](/platforms/mac/permissions)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)