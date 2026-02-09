---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/hooks/soul-evil",
    "fetched_at": "2026-02-07T10:11:11.757171",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 516284
  },
  "metadata": {
    "title": "SOUL Evil Hook",
    "section": "soul-evil",
    "tier": 2,
    "type": "reference"
  }
}
---

- SOUL Evil Hook - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationAutomationSOUL Evil Hook[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [SOUL Evil Hook](#soul-evil-hook)- [How It Works](#how-it-works)- [Enable](#enable)- [Options](#options)- [Notes](#notes)- [See Also](#see-also)Automation# SOUL Evil Hook# [​](#soul-evil-hook)SOUL Evil Hook

The SOUL Evil hook swaps the **injected** `SOUL.md` content with `SOUL_EVIL.md` during

a purge window or by random chance. It does **not** modify files on disk.

## [​](#how-it-works)How It Works

When `agent:bootstrap` runs, the hook can replace the `SOUL.md` content in memory

before the system prompt is assembled. If `SOUL_EVIL.md` is missing or empty,

OpenClaw logs a warning and keeps the normal `SOUL.md`.

Sub-agent runs do **not** include `SOUL.md` in their bootstrap files, so this hook

has no effect on sub-agents.

## [​](#enable)Enable

Copy```

openclaw hooks enable soul-evil

```

Then set the config:

Copy```

{

"hooks": {

"internal": {

"enabled": true,

"entries": {

"soul-evil": {

"enabled": true,

"file": "SOUL_EVIL.md",

"chance": 0.1,

"purge": { "at": "21:00", "duration": "15m" }

}

}

}

}

}

```

Create `SOUL_EVIL.md` in the agent workspace root (next to `SOUL.md`).

## [​](#options)Options

- `file` (string): alternate SOUL filename (default: `SOUL_EVIL.md`)

- `chance` (number 0–1): random chance per run to use `SOUL_EVIL.md`

- `purge.at` (HH:mm): daily purge start (24-hour clock)

- `purge.duration` (duration): window length (e.g. `30s`, `10m`, `1h`)

**Precedence:** purge window wins over chance.

**Timezone:** uses `agents.defaults.userTimezone` when set; otherwise host timezone.

## [​](#notes)Notes

- No files are written or modified on disk.

- If `SOUL.md` is not in the bootstrap list, the hook does nothing.

## [​](#see-also)See Also

- [Hooks](/hooks)

[Hooks](/hooks)[Cron Jobs](/automation/cron-jobs)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)