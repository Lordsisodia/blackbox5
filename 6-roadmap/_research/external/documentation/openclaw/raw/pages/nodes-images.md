---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/nodes/images",
    "fetched_at": "2026-02-07T10:19:44.944071",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 501895
  },
  "metadata": {
    "title": "Image and Media Support",
    "section": "images",
    "tier": 3,
    "type": "reference"
  }
}
---

- Image and Media Support - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMedia and devicesImage and Media Support[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Image & Media Support — 2025-12-05](#image-%26-media-support-%E2%80%94-2025-12-05)- [Goals](#goals)- [CLI Surface](#cli-surface)- [WhatsApp Web channel behavior](#whatsapp-web-channel-behavior)- [Auto-Reply Pipeline](#auto-reply-pipeline)- [Inbound Media to Commands (Pi)](#inbound-media-to-commands-pi)- [Limits & Errors](#limits-%26-errors)- [Notes for Tests](#notes-for-tests)Media and devices# Image and Media Support# [​](#image-&-media-support-—-2025-12-05)Image & Media Support — 2025-12-05

The WhatsApp channel runs via **Baileys Web**. This document captures the current media handling rules for send, gateway, and agent replies.

## [​](#goals)Goals

- Send media with optional captions via `openclaw message send --media`.

- Allow auto-replies from the web inbox to include media alongside text.

- Keep per-type limits sane and predictable.

## [​](#cli-surface)CLI Surface

- `openclaw message send --media <path-or-url> [--message <caption>]`

`--media` optional; caption can be empty for media-only sends.

- `--dry-run` prints the resolved payload; `--json` emits `{ channel, to, messageId, mediaUrl, caption }`.

## [​](#whatsapp-web-channel-behavior)WhatsApp Web channel behavior

- Input: local file path **or** HTTP(S) URL.

- Flow: load into a Buffer, detect media kind, and build the correct payload:

**Images:** resize & recompress to JPEG (max side 2048px) targeting `agents.defaults.mediaMaxMb` (default 5 MB), capped at 6 MB.

- **Audio/Voice/Video:** pass-through up to 16 MB; audio is sent as a voice note (`ptt: true`).

- **Documents:** anything else, up to 100 MB, with filename preserved when available.

- WhatsApp GIF-style playback: send an MP4 with `gifPlayback: true` (CLI: `--gif-playback`) so mobile clients loop inline.

- MIME detection prefers magic bytes, then headers, then file extension.

- Caption comes from `--message` or `reply.text`; empty caption is allowed.

- Logging: non-verbose shows `↩️`/`✅`; verbose includes size and source path/URL.

## [​](#auto-reply-pipeline)Auto-Reply Pipeline

- `getReplyFromConfig` returns `{ text?, mediaUrl?, mediaUrls? }`.

- When media is present, the web sender resolves local paths or URLs using the same pipeline as `openclaw message send`.

- Multiple media entries are sent sequentially if provided.

## [​](#inbound-media-to-commands-pi)Inbound Media to Commands (Pi)

- When inbound web messages include media, OpenClaw downloads to a temp file and exposes templating variables:

`{{MediaUrl}}` pseudo-URL for the inbound media.

- `{{MediaPath}}` local temp path written before running the command.

- When a per-session Docker sandbox is enabled, inbound media is copied into the sandbox workspace and `MediaPath`/`MediaUrl` are rewritten to a relative path like `media/inbound/<filename>`.

- Media understanding (if configured via `tools.media.*` or shared `tools.media.models`) runs before templating and can insert `[Image]`, `[Audio]`, and `[Video]` blocks into `Body`.

Audio sets `{{Transcript}}` and uses the transcript for command parsing so slash commands still work.

- Video and image descriptions preserve any caption text for command parsing.

- By default only the first matching image/audio/video attachment is processed; set `tools.media.<cap>.attachments` to process multiple attachments.

## [​](#limits-&-errors)Limits & Errors

**Outbound send caps (WhatsApp web send)**

- Images: ~6 MB cap after recompression.

- Audio/voice/video: 16 MB cap; documents: 100 MB cap.

- Oversize or unreadable media → clear error in logs and the reply is skipped.

**Media understanding caps (transcription/description)**

- Image default: 10 MB (`tools.media.image.maxBytes`).

- Audio default: 20 MB (`tools.media.audio.maxBytes`).

- Video default: 50 MB (`tools.media.video.maxBytes`).

- Oversize media skips understanding, but replies still go through with the original body.

## [​](#notes-for-tests)Notes for Tests

- Cover send + reply flows for image/audio/document cases.

- Validate recompression for images (size bound) and voice-note flag for audio.

- Ensure multi-media replies fan out as sequential sends.

[Nodes](/nodes)[Audio and Voice Notes](/nodes/audio)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)