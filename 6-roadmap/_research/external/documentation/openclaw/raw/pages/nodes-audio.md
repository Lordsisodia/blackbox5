---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/nodes/audio",
    "fetched_at": "2026-02-07T10:19:43.667989",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 582674
  },
  "metadata": {
    "title": "Audio and Voice Notes",
    "section": "audio",
    "tier": 3,
    "type": "reference"
  }
}
---

- Audio and Voice Notes - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMedia and devicesAudio and Voice Notes[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Audio / Voice Notes — 2026-01-17](#audio-%2F-voice-notes-%E2%80%94-2026-01-17)- [What works](#what-works)- [Auto-detection (default)](#auto-detection-default)- [Config examples](#config-examples)- [Provider + CLI fallback (OpenAI + Whisper CLI)](#provider-%2B-cli-fallback-openai-%2B-whisper-cli)- [Provider-only with scope gating](#provider-only-with-scope-gating)- [Provider-only (Deepgram)](#provider-only-deepgram)- [Notes & limits](#notes-%26-limits)- [Gotchas](#gotchas)Media and devices# Audio and Voice Notes# [​](#audio-/-voice-notes-—-2026-01-17)Audio / Voice Notes — 2026-01-17

## [​](#what-works)What works

- **Media understanding (audio)**: If audio understanding is enabled (or auto‑detected), OpenClaw:

Locates the first audio attachment (local path or URL) and downloads it if needed.

- Enforces `maxBytes` before sending to each model entry.

- Runs the first eligible model entry in order (provider or CLI).

- If it fails or skips (size/timeout), it tries the next entry.

- On success, it replaces `Body` with an `[Audio]` block and sets `{{Transcript}}`.

- **Command parsing**: When transcription succeeds, `CommandBody`/`RawBody` are set to the transcript so slash commands still work.

- **Verbose logging**: In `--verbose`, we log when transcription runs and when it replaces the body.

## [​](#auto-detection-default)Auto-detection (default)

If you **don’t configure models** and `tools.media.audio.enabled` is **not** set to `false`,

OpenClaw auto-detects in this order and stops at the first working option:

- **Local CLIs** (if installed)

`sherpa-onnx-offline` (requires `SHERPA_ONNX_MODEL_DIR` with encoder/decoder/joiner/tokens)

- `whisper-cli` (from `whisper-cpp`; uses `WHISPER_CPP_MODEL` or the bundled tiny model)

- `whisper` (Python CLI; downloads models automatically)

- **Gemini CLI** (`gemini`) using `read_many_files`

- **Provider keys** (OpenAI → Groq → Deepgram → Google)

To disable auto-detection, set `tools.media.audio.enabled: false`.

To customize, set `tools.media.audio.models`.

Note: Binary detection is best-effort across macOS/Linux/Windows; ensure the CLI is on `PATH` (we expand `~`), or set an explicit CLI model with a full command path.

## [​](#config-examples)Config examples

### [​](#provider-+-cli-fallback-openai-+-whisper-cli)Provider + CLI fallback (OpenAI + Whisper CLI)

Copy```

{

tools: {

media: {

audio: {

enabled: true,

maxBytes: 20971520,

models: [

{ provider: "openai", model: "gpt-4o-mini-transcribe" },

{

type: "cli",

command: "whisper",

args: ["--model", "base", "{{MediaPath}}"],

timeoutSeconds: 45,

},

],

},

},

},

}

```

### [​](#provider-only-with-scope-gating)Provider-only with scope gating

Copy```

{

tools: {

media: {

audio: {

enabled: true,

scope: {

default: "allow",

rules: [{ action: "deny", match: { chatType: "group" } }],

},

models: [{ provider: "openai", model: "gpt-4o-mini-transcribe" }],

},

},

},

}

```

### [​](#provider-only-deepgram)Provider-only (Deepgram)

Copy```

{

tools: {

media: {

audio: {

enabled: true,

models: [{ provider: "deepgram", model: "nova-3" }],

},

},

},

}

```

## [​](#notes-&-limits)Notes & limits

- Provider auth follows the standard model auth order (auth profiles, env vars, `models.providers.*.apiKey`).

- Deepgram picks up `DEEPGRAM_API_KEY` when `provider: "deepgram"` is used.

- Deepgram setup details: [Deepgram (audio transcription)](/providers/deepgram).

- Audio providers can override `baseUrl`, `headers`, and `providerOptions` via `tools.media.audio`.

- Default size cap is 20MB (`tools.media.audio.maxBytes`). Oversize audio is skipped for that model and the next entry is tried.

- Default `maxChars` for audio is **unset** (full transcript). Set `tools.media.audio.maxChars` or per-entry `maxChars` to trim output.

- OpenAI auto default is `gpt-4o-mini-transcribe`; set `model: "gpt-4o-transcribe"` for higher accuracy.

- Use `tools.media.audio.attachments` to process multiple voice notes (`mode: "all"` + `maxAttachments`).

- Transcript is available to templates as `{{Transcript}}`.

- CLI stdout is capped (5MB); keep CLI output concise.

## [​](#gotchas)Gotchas

- Scope rules use first-match wins. `chatType` is normalized to `direct`, `group`, or `room`.

- Ensure your CLI exits 0 and prints plain text; JSON needs to be massaged via `jq -r .text`.

- Keep timeouts reasonable (`timeoutSeconds`, default 60s) to avoid blocking the reply queue.

[Image and Media Support](/nodes/images)[Camera Capture](/nodes/camera)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)