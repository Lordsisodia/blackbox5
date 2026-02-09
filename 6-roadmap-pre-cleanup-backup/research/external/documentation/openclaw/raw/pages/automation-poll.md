---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/automation/poll",
    "fetched_at": "2026-02-07T10:12:20.685551",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 530302
  },
  "metadata": {
    "title": "Polls",
    "section": "poll",
    "tier": 3,
    "type": "reference"
  }
}
---

- Polls - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationAutomationPolls[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Polls](#polls)- [Supported channels](#supported-channels)- [CLI](#cli)- [Gateway RPC](#gateway-rpc)- [Channel differences](#channel-differences)- [Agent tool (Message)](#agent-tool-message)Automation# Polls# [​](#polls)Polls

## [​](#supported-channels)Supported channels

- WhatsApp (web channel)

- Discord

- MS Teams (Adaptive Cards)

## [​](#cli)CLI

Copy```

# WhatsApp

openclaw message poll --target +15555550123 \

--poll-question "Lunch today?" --poll-option "Yes" --poll-option "No" --poll-option "Maybe"

openclaw message poll --target [[email protected]](/cdn-cgi/l/email-protection) \

--poll-question "Meeting time?" --poll-option "10am" --poll-option "2pm" --poll-option "4pm" --poll-multi

# Discord

openclaw message poll --channel discord --target channel:123456789 \

--poll-question "Snack?" --poll-option "Pizza" --poll-option "Sushi"

openclaw message poll --channel discord --target channel:123456789 \

--poll-question "Plan?" --poll-option "A" --poll-option "B" --poll-duration-hours 48

# MS Teams

openclaw message poll --channel msteams --target conversation:19:[[email protected]](/cdn-cgi/l/email-protection) \

--poll-question "Lunch?" --poll-option "Pizza" --poll-option "Sushi"

```

Options:

- `--channel`: `whatsapp` (default), `discord`, or `msteams`

- `--poll-multi`: allow selecting multiple options

- `--poll-duration-hours`: Discord-only (defaults to 24 when omitted)

## [​](#gateway-rpc)Gateway RPC

Method: `poll`

Params:

- `to` (string, required)

- `question` (string, required)

- `options` (string[], required)

- `maxSelections` (number, optional)

- `durationHours` (number, optional)

- `channel` (string, optional, default: `whatsapp`)

- `idempotencyKey` (string, required)

## [​](#channel-differences)Channel differences

- WhatsApp: 2-12 options, `maxSelections` must be within option count, ignores `durationHours`.

- Discord: 2-10 options, `durationHours` clamped to 1-768 hours (default 24). `maxSelections > 1` enables multi-select; Discord does not support a strict selection count.

- MS Teams: Adaptive Card polls (OpenClaw-managed). No native poll API; `durationHours` is ignored.

## [​](#agent-tool-message)Agent tool (Message)

Use the `message` tool with `poll` action (`to`, `pollQuestion`, `pollOption`, optional `pollMulti`, `pollDurationHours`, `channel`).

Note: Discord has no “pick exactly N” mode; `pollMulti` maps to multi-select.

Teams polls are rendered as Adaptive Cards and require the gateway to stay online

to record votes in `~/.openclaw/msteams-polls.json`.[Gmail PubSub](/automation/gmail-pubsub)[Auth Monitoring](/automation/auth-monitoring)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)