---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/tools/reactions",
    "fetched_at": "2026-02-07T10:23:49.320879",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 471792
  },
  "metadata": {
    "title": "Reactions",
    "section": "reactions",
    "tier": 3,
    "type": "reference"
  }
}
---

- Reactions - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationBuilt-in toolsReactions[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Reaction tooling](#reaction-tooling)Built-in tools# Reactions# [​](#reaction-tooling)Reaction tooling

Shared reaction semantics across channels:

- `emoji` is required when adding a reaction.

- `emoji=""` removes the bot’s reaction(s) when supported.

- `remove: true` removes the specified emoji when supported (requires `emoji`).

Channel notes:

- **Discord/Slack**: empty `emoji` removes all of the bot’s reactions on the message; `remove: true` removes just that emoji.

- **Google Chat**: empty `emoji` removes the app’s reactions on the message; `remove: true` removes just that emoji.

- **Telegram**: empty `emoji` removes the bot’s reactions; `remove: true` also removes reactions but still requires a non-empty `emoji` for tool validation.

- **WhatsApp**: empty `emoji` removes the bot reaction; `remove: true` maps to empty emoji (still requires `emoji`).

- **Signal**: inbound reaction notifications emit system events when `channels.signal.reactionNotifications` is enabled.

[Thinking Levels](/tools/thinking)[Browser (OpenClaw-managed)](/tools/browser)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)