---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/plugins/voice-call",
    "fetched_at": "2026-02-07T10:11:43.199779",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 732374
  },
  "metadata": {
    "title": "Voice Call Plugin",
    "section": "voice-call",
    "tier": 2,
    "type": "reference"
  }
}
---

- Voice Call Plugin - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationSkills and extensionsVoice Call Plugin[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Voice Call (plugin)](#voice-call-plugin)- [Where it runs (local vs remote)](#where-it-runs-local-vs-remote)- [Install](#install)- [Option A: install from npm (recommended)](#option-a-install-from-npm-recommended)- [Option B: install from a local folder (dev, no copying)](#option-b-install-from-a-local-folder-dev-no-copying)- [Config](#config)- [Webhook Security](#webhook-security)- [TTS for calls](#tts-for-calls)- [More examples](#more-examples)- [Inbound calls](#inbound-calls)- [CLI](#cli)- [Agent tool](#agent-tool)- [Gateway RPC](#gateway-rpc)Skills and extensions# Voice Call Plugin# [​](#voice-call-plugin)Voice Call (plugin)

Voice calls for OpenClaw via a plugin. Supports outbound notifications and

multi-turn conversations with inbound policies.

Current providers:

- `twilio` (Programmable Voice + Media Streams)

- `telnyx` (Call Control v2)

- `plivo` (Voice API + XML transfer + GetInput speech)

- `mock` (dev/no network)

Quick mental model:

- Install plugin

- Restart Gateway

- Configure under `plugins.entries.voice-call.config`

- Use `openclaw voicecall ...` or the `voice_call` tool

## [​](#where-it-runs-local-vs-remote)Where it runs (local vs remote)

The Voice Call plugin runs **inside the Gateway process**.

If you use a remote Gateway, install/configure the plugin on the **machine running the Gateway**, then restart the Gateway to load it.

## [​](#install)Install

### [​](#option-a-install-from-npm-recommended)Option A: install from npm (recommended)

Copy```

openclaw plugins install @openclaw/voice-call

```

Restart the Gateway afterwards.

### [​](#option-b-install-from-a-local-folder-dev-no-copying)Option B: install from a local folder (dev, no copying)

Copy```

openclaw plugins install ./extensions/voice-call

cd ./extensions/voice-call && pnpm install

```

Restart the Gateway afterwards.

## [​](#config)Config

Set config under `plugins.entries.voice-call.config`:

Copy```

{

plugins: {

entries: {

"voice-call": {

enabled: true,

config: {

provider: "twilio", // or "telnyx" | "plivo" | "mock"

fromNumber: "+15550001234",

toNumber: "+15550005678",

twilio: {

accountSid: "ACxxxxxxxx",

authToken: "...",

},

plivo: {

authId: "MAxxxxxxxxxxxxxxxxxxxx",

authToken: "...",

},

// Webhook server

serve: {

port: 3334,

path: "/voice/webhook",

},

// Webhook security (recommended for tunnels/proxies)

webhookSecurity: {

allowedHosts: ["voice.example.com"],

trustedProxyIPs: ["100.64.0.1"],

},

// Public exposure (pick one)

// publicUrl: "https://example.ngrok.app/voice/webhook",

// tunnel: { provider: "ngrok" },

// tailscale: { mode: "funnel", path: "/voice/webhook" }

outbound: {

defaultMode: "notify", // notify | conversation

},

streaming: {

enabled: true,

streamPath: "/voice/stream",

},

},

},

},

},

}

```

Notes:

- Twilio/Telnyx require a **publicly reachable** webhook URL.

- Plivo requires a **publicly reachable** webhook URL.

- `mock` is a local dev provider (no network calls).

- `skipSignatureVerification` is for local testing only.

- If you use ngrok free tier, set `publicUrl` to the exact ngrok URL; signature verification is always enforced.

- `tunnel.allowNgrokFreeTierLoopbackBypass: true` allows Twilio webhooks with invalid signatures **only** when `tunnel.provider="ngrok"` and `serve.bind` is loopback (ngrok local agent). Use for local dev only.

- Ngrok free tier URLs can change or add interstitial behavior; if `publicUrl` drifts, Twilio signatures will fail. For production, prefer a stable domain or Tailscale funnel.

## [​](#webhook-security)Webhook Security

When a proxy or tunnel sits in front of the Gateway, the plugin reconstructs the

public URL for signature verification. These options control which forwarded

headers are trusted.

`webhookSecurity.allowedHosts` allowlists hosts from forwarding headers.

`webhookSecurity.trustForwardingHeaders` trusts forwarded headers without an allowlist.

`webhookSecurity.trustedProxyIPs` only trusts forwarded headers when the request

remote IP matches the list.

Example with a stable public host:

Copy```

{

plugins: {

entries: {

"voice-call": {

config: {

publicUrl: "https://voice.example.com/voice/webhook",

webhookSecurity: {

allowedHosts: ["voice.example.com"],

},

},

},

},

},

}

```

## [​](#tts-for-calls)TTS for calls

Voice Call uses the core `messages.tts` configuration (OpenAI or ElevenLabs) for

streaming speech on calls. You can override it under the plugin config with the

**same shape** — it deep‑merges with `messages.tts`.

Copy```

{

tts: {

provider: "elevenlabs",

elevenlabs: {

voiceId: "pMsXgVXv3BLzUgSXRplE",

modelId: "eleven_multilingual_v2",

},

},

}

```

Notes:

- **Edge TTS is ignored for voice calls** (telephony audio needs PCM; Edge output is unreliable).

- Core TTS is used when Twilio media streaming is enabled; otherwise calls fall back to provider native voices.

### [​](#more-examples)More examples

Use core TTS only (no override):

Copy```

{

messages: {

tts: {

provider: "openai",

openai: { voice: "alloy" },

},

},

}

```

Override to ElevenLabs just for calls (keep core default elsewhere):

Copy```

{

plugins: {

entries: {

"voice-call": {

config: {

tts: {

provider: "elevenlabs",

elevenlabs: {

apiKey: "elevenlabs_key",

voiceId: "pMsXgVXv3BLzUgSXRplE",

modelId: "eleven_multilingual_v2",

},

},

},

},

},

},

}

```

Override only the OpenAI model for calls (deep‑merge example):

Copy```

{

plugins: {

entries: {

"voice-call": {

config: {

tts: {

openai: {

model: "gpt-4o-mini-tts",

voice: "marin",

},

},

},

},

},

},

}

```

## [​](#inbound-calls)Inbound calls

Inbound policy defaults to `disabled`. To enable inbound calls, set:

Copy```

{

inboundPolicy: "allowlist",

allowFrom: ["+15550001234"],

inboundGreeting: "Hello! How can I help?",

}

```

Auto-responses use the agent system. Tune with:

- `responseModel`

- `responseSystemPrompt`

- `responseTimeoutMs`

## [​](#cli)CLI

Copy```

openclaw voicecall call --to "+15555550123" --message "Hello from OpenClaw"

openclaw voicecall continue --call-id <id> --message "Any questions?"

openclaw voicecall speak --call-id <id> --message "One moment"

openclaw voicecall end --call-id <id>

openclaw voicecall status --call-id <id>

openclaw voicecall tail

openclaw voicecall expose --mode funnel

```

## [​](#agent-tool)Agent tool

Tool name: `voice_call`

Actions:

- `initiate_call` (message, to?, mode?)

- `continue_call` (callId, message)

- `speak_to_user` (callId, message)

- `end_call` (callId)

- `get_status` (callId)

This repo ships a matching skill doc at `skills/voice-call/SKILL.md`.

## [​](#gateway-rpc)Gateway RPC

- `voicecall.initiate` (`to?`, `message`, `mode?`)

- `voicecall.continue` (`callId`, `message`)

- `voicecall.speak` (`callId`, `message`)

- `voicecall.end` (`callId`)

- `voicecall.status` (`callId`)

[Plugins](/plugin)[Zalo Personal Plugin](/plugins/zalouser)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)