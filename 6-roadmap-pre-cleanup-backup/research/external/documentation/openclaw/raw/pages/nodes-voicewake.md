---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/nodes/voicewake",
    "fetched_at": "2026-02-07T10:19:48.033331",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 501934
  },
  "metadata": {
    "title": "Voice Wake",
    "section": "voicewake",
    "tier": 3,
    "type": "reference"
  }
}
---

- Voice Wake - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMedia and devicesVoice Wake[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Voice Wake (Global Wake Words)](#voice-wake-global-wake-words)- [Storage (Gateway host)](#storage-gateway-host)- [Protocol](#protocol)- [Methods](#methods)- [Events](#events)- [Client behavior](#client-behavior)- [macOS app](#macos-app)- [iOS node](#ios-node)- [Android node](#android-node)Media and devices# Voice Wake# [​](#voice-wake-global-wake-words)Voice Wake (Global Wake Words)

OpenClaw treats **wake words as a single global list** owned by the **Gateway**.

- There are **no per-node custom wake words**.

- **Any node/app UI may edit** the list; changes are persisted by the Gateway and broadcast to everyone.

- Each device still keeps its own **Voice Wake enabled/disabled** toggle (local UX + permissions differ).

## [​](#storage-gateway-host)Storage (Gateway host)

Wake words are stored on the gateway machine at:

- `~/.openclaw/settings/voicewake.json`

Shape:

Copy```

{ "triggers": ["openclaw", "claude", "computer"], "updatedAtMs": 1730000000000 }

```

## [​](#protocol)Protocol

### [​](#methods)Methods

- `voicewake.get` → `{ triggers: string[] }`

- `voicewake.set` with params `{ triggers: string[] }` → `{ triggers: string[] }`

Notes:

- Triggers are normalized (trimmed, empties dropped). Empty lists fall back to defaults.

- Limits are enforced for safety (count/length caps).

### [​](#events)Events

- `voicewake.changed` payload `{ triggers: string[] }`

Who receives it:

- All WebSocket clients (macOS app, WebChat, etc.)

- All connected nodes (iOS/Android), and also on node connect as an initial “current state” push.

## [​](#client-behavior)Client behavior

### [​](#macos-app)macOS app

- Uses the global list to gate `VoiceWakeRuntime` triggers.

- Editing “Trigger words” in Voice Wake settings calls `voicewake.set` and then relies on the broadcast to keep other clients in sync.

### [​](#ios-node)iOS node

- Uses the global list for `VoiceWakeManager` trigger detection.

- Editing Wake Words in Settings calls `voicewake.set` (over the Gateway WS) and also keeps local wake-word detection responsive.

### [​](#android-node)Android node

- Exposes a Wake Words editor in Settings.

- Calls `voicewake.set` over the Gateway WS so edits sync everywhere.

[Talk Mode](/nodes/talk)[Location Command](/nodes/location-command)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)