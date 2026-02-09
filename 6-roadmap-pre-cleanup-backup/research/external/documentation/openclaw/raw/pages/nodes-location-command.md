---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/nodes/location-command",
    "fetched_at": "2026-02-07T10:19:46.431297",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 535051
  },
  "metadata": {
    "title": "Location Command",
    "section": "location-command",
    "tier": 3,
    "type": "reference"
  }
}
---

- Location Command - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMedia and devicesLocation Command[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Location command (nodes)](#location-command-nodes)- [TL;DR](#tldr)- [Why a selector (not just a switch)](#why-a-selector-not-just-a-switch)- [Settings model](#settings-model)- [Permissions mapping (node.permissions)](#permissions-mapping-node-permissions)- [Command: location.get](#command-location-get)- [Background behavior (future)](#background-behavior-future)- [Model/tooling integration](#model%2Ftooling-integration)- [UX copy (suggested)](#ux-copy-suggested)Media and devices# Location Command# [​](#location-command-nodes)Location command (nodes)

## [​](#tldr)TL;DR

- `location.get` is a node command (via `node.invoke`).

- Off by default.

- Settings use a selector: Off / While Using / Always.

- Separate toggle: Precise Location.

## [​](#why-a-selector-not-just-a-switch)Why a selector (not just a switch)

OS permissions are multi-level. We can expose a selector in-app, but the OS still decides the actual grant.

- iOS/macOS: user can choose **While Using** or **Always** in system prompts/Settings. App can request upgrade, but OS may require Settings.

- Android: background location is a separate permission; on Android 10+ it often requires a Settings flow.

- Precise location is a separate grant (iOS 14+ “Precise”, Android “fine” vs “coarse”).

Selector in UI drives our requested mode; actual grant lives in OS settings.

## [​](#settings-model)Settings model

Per node device:

- `location.enabledMode`: `off | whileUsing | always`

- `location.preciseEnabled`: bool

UI behavior:

- Selecting `whileUsing` requests foreground permission.

- Selecting `always` first ensures `whileUsing`, then requests background (or sends user to Settings if required).

- If OS denies requested level, revert to the highest granted level and show status.

## [​](#permissions-mapping-node-permissions)Permissions mapping (node.permissions)

Optional. macOS node reports `location` via the permissions map; iOS/Android may omit it.

## [​](#command-location-get)Command: `location.get`

Called via `node.invoke`.

Params (suggested):

Copy```

{

"timeoutMs": 10000,

"maxAgeMs": 15000,

"desiredAccuracy": "coarse|balanced|precise"

}

```

Response payload:

Copy```

{

"lat": 48.20849,

"lon": 16.37208,

"accuracyMeters": 12.5,

"altitudeMeters": 182.0,

"speedMps": 0.0,

"headingDeg": 270.0,

"timestamp": "2026-01-03T12:34:56.000Z",

"isPrecise": true,

"source": "gps|wifi|cell|unknown"

}

```

Errors (stable codes):

- `LOCATION_DISABLED`: selector is off.

- `LOCATION_PERMISSION_REQUIRED`: permission missing for requested mode.

- `LOCATION_BACKGROUND_UNAVAILABLE`: app is backgrounded but only While Using allowed.

- `LOCATION_TIMEOUT`: no fix in time.

- `LOCATION_UNAVAILABLE`: system failure / no providers.

## [​](#background-behavior-future)Background behavior (future)

Goal: model can request location even when node is backgrounded, but only when:

- User selected **Always**.

- OS grants background location.

- App is allowed to run in background for location (iOS background mode / Android foreground service or special allowance).

Push-triggered flow (future):

- Gateway sends a push to the node (silent push or FCM data).

- Node wakes briefly and requests location from the device.

- Node forwards payload to Gateway.

Notes:

- iOS: Always permission + background location mode required. Silent push may be throttled; expect intermittent failures.

- Android: background location may require a foreground service; otherwise, expect denial.

## [​](#model/tooling-integration)Model/tooling integration

- Tool surface: `nodes` tool adds `location_get` action (node required).

- CLI: `openclaw nodes location get --node <id>`.

- Agent guidelines: only call when user enabled location and understands the scope.

## [​](#ux-copy-suggested)UX copy (suggested)

- Off: “Location sharing is disabled.”

- While Using: “Only when OpenClaw is open.”

- Always: “Allow background location. Requires system permission.”

- Precise: “Use precise GPS location. Toggle off to share approximate location.”

[Voice Wake](/nodes/voicewake)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)