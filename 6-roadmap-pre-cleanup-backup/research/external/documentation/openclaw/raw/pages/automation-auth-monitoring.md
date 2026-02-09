---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/automation/auth-monitoring",
    "fetched_at": "2026-02-07T10:11:47.111482",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 484139
  },
  "metadata": {
    "title": "Auth Monitoring",
    "section": "auth-monitoring",
    "tier": 3,
    "type": "reference"
  }
}
---

- Auth Monitoring - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationAutomationAuth Monitoring[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Auth monitoring](#auth-monitoring)- [Preferred: CLI check (portable)](#preferred-cli-check-portable)- [Optional scripts (ops / phone workflows)](#optional-scripts-ops-%2F-phone-workflows)Automation# Auth Monitoring# [​](#auth-monitoring)Auth monitoring

OpenClaw exposes OAuth expiry health via `openclaw models status`. Use that for

automation and alerting; scripts are optional extras for phone workflows.

## [​](#preferred-cli-check-portable)Preferred: CLI check (portable)

Copy```

openclaw models status --check

```

Exit codes:

- `0`: OK

- `1`: expired or missing credentials

- `2`: expiring soon (within 24h)

This works in cron/systemd and requires no extra scripts.

## [​](#optional-scripts-ops-/-phone-workflows)Optional scripts (ops / phone workflows)

These live under `scripts/` and are **optional**. They assume SSH access to the

gateway host and are tuned for systemd + Termux.

- `scripts/claude-auth-status.sh` now uses `openclaw models status --json` as the

source of truth (falling back to direct file reads if the CLI is unavailable),

so keep `openclaw` on `PATH` for timers.

- `scripts/auth-monitor.sh`: cron/systemd timer target; sends alerts (ntfy or phone).

- `scripts/systemd/openclaw-auth-monitor.{service,timer}`: systemd user timer.

- `scripts/claude-auth-status.sh`: Claude Code + OpenClaw auth checker (full/json/simple).

- `scripts/mobile-reauth.sh`: guided re‑auth flow over SSH.

- `scripts/termux-quick-auth.sh`: one‑tap widget status + open auth URL.

- `scripts/termux-auth-widget.sh`: full guided widget flow.

- `scripts/termux-sync-widget.sh`: sync Claude Code creds → OpenClaw.

If you don’t need phone automation or systemd timers, skip these scripts.[Polls](/automation/poll)[Nodes](/nodes)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)