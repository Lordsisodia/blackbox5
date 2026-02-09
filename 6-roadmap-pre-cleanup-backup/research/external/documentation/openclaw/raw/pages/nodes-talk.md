---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/nodes/talk",
    "fetched_at": "2026-02-07T10:19:47.301194",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 523602
  },
  "metadata": {
    "title": "Talk Mode",
    "section": "talk",
    "tier": 3,
    "type": "reference"
  }
}
---

- Talk Mode - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMedia and devicesTalk Mode[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Talk Mode](#talk-mode)- [Behavior (macOS)](#behavior-macos)- [Voice directives in replies](#voice-directives-in-replies)- [Config (~/.openclaw/openclaw.json)](#config-%2F-openclaw%2Fopenclaw-json)- [macOS UI](#macos-ui)- [Notes](#notes)Media and devices# Talk Mode# [​](#talk-mode)Talk Mode

Talk mode is a continuous voice conversation loop:

- Listen for speech

- Send transcript to the model (main session, chat.send)

- Wait for the response

- Speak it via ElevenLabs (streaming playback)

## [​](#behavior-macos)Behavior (macOS)

- **Always-on overlay** while Talk mode is enabled.

- **Listening → Thinking → Speaking** phase transitions.

- On a **short pause** (silence window), the current transcript is sent.

- Replies are **written to WebChat** (same as typing).

- **Interrupt on speech** (default on): if the user starts talking while the assistant is speaking, we stop playback and note the interruption timestamp for the next prompt.

## [​](#voice-directives-in-replies)Voice directives in replies

The assistant may prefix its reply with a **single JSON line** to control voice:

Copy```

{ "voice": "<voice-id>", "once": true }

```

Rules:

- First non-empty line only.

- Unknown keys are ignored.

- `once: true` applies to the current reply only.

- Without `once`, the voice becomes the new default for Talk mode.

- The JSON line is stripped before TTS playback.

Supported keys:

- `voice` / `voice_id` / `voiceId`

- `model` / `model_id` / `modelId`

- `speed`, `rate` (WPM), `stability`, `similarity`, `style`, `speakerBoost`

- `seed`, `normalize`, `lang`, `output_format`, `latency_tier`

- `once`

## [​](#config-/-openclaw/openclaw-json)Config (`~/.openclaw/openclaw.json`)

Copy```

{

talk: {

voiceId: "elevenlabs_voice_id",

modelId: "eleven_v3",

outputFormat: "mp3_44100_128",

apiKey: "elevenlabs_api_key",

interruptOnSpeech: true,

},

}

```

Defaults:

- `interruptOnSpeech`: true

- `voiceId`: falls back to `ELEVENLABS_VOICE_ID` / `SAG_VOICE_ID` (or first ElevenLabs voice when API key is available)

- `modelId`: defaults to `eleven_v3` when unset

- `apiKey`: falls back to `ELEVENLABS_API_KEY` (or gateway shell profile if available)

- `outputFormat`: defaults to `pcm_44100` on macOS/iOS and `pcm_24000` on Android (set `mp3_*` to force MP3 streaming)

## [​](#macos-ui)macOS UI

- Menu bar toggle: **Talk**

- Config tab: **Talk Mode** group (voice id + interrupt toggle)

- Overlay:

**Listening**: cloud pulses with mic level

- **Thinking**: sinking animation

- **Speaking**: radiating rings

- Click cloud: stop speaking

- Click X: exit Talk mode

## [​](#notes)Notes

- Requires Speech + Microphone permissions.

- Uses `chat.send` against session key `main`.

- TTS uses ElevenLabs streaming API with `ELEVENLABS_API_KEY` and incremental playback on macOS/iOS/Android for lower latency.

- `stability` for `eleven_v3` is validated to `0.0`, `0.5`, or `1.0`; other models accept `0..1`.

- `latency_tier` is validated to `0..4` when set.

- Android supports `pcm_16000`, `pcm_22050`, `pcm_24000`, and `pcm_44100` output formats for low-latency AudioTrack streaming.

[Camera Capture](/nodes/camera)[Voice Wake](/nodes/voicewake)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)