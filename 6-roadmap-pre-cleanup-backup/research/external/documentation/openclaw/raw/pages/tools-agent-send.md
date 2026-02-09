---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/tools/agent-send",
    "fetched_at": "2026-02-07T10:23:11.828341",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 512810
  },
  "metadata": {
    "title": "Agent Send",
    "section": "agent-send",
    "tier": 3,
    "type": "reference"
  }
}
---

- Agent Send - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationAgent coordinationAgent Send[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [openclaw agent (direct agent runs)](#openclaw-agent-direct-agent-runs)- [Behavior](#behavior)- [Examples](#examples)- [Flags](#flags)Agent coordination# Agent Send# [​](#openclaw-agent-direct-agent-runs)`openclaw agent` (direct agent runs)

`openclaw agent` runs a single agent turn without needing an inbound chat message.

By default it goes **through the Gateway**; add `--local` to force the embedded

runtime on the current machine.

## [​](#behavior)Behavior

- Required: `--message <text>`

- Session selection:

`--to <dest>` derives the session key (group/channel targets preserve isolation; direct chats collapse to `main`), **or**

- `--session-id <id>` reuses an existing session by id, **or**

- `--agent <id>` targets a configured agent directly (uses that agent’s `main` session key)

- Runs the same embedded agent runtime as normal inbound replies.

- Thinking/verbose flags persist into the session store.

- Output:

default: prints reply text (plus `MEDIA:<url>` lines)

- `--json`: prints structured payload + metadata

- Optional delivery back to a channel with `--deliver` + `--channel` (target formats match `openclaw message --target`).

- Use `--reply-channel`/`--reply-to`/`--reply-account` to override delivery without changing the session.

If the Gateway is unreachable, the CLI **falls back** to the embedded local run.

## [​](#examples)Examples

Copy```

openclaw agent --to +15555550123 --message "status update"

openclaw agent --agent ops --message "Summarize logs"

openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium

openclaw agent --to +15555550123 --message "Trace logs" --verbose on --json

openclaw agent --to +15555550123 --message "Summon reply" --deliver

openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"

```

## [​](#flags)Flags

- `--local`: run locally (requires model provider API keys in your shell)

- `--deliver`: send the reply to the chosen channel

- `--channel`: delivery channel (`whatsapp|telegram|discord|googlechat|slack|signal|imessage`, default: `whatsapp`)

- `--reply-to`: delivery target override

- `--reply-channel`: delivery channel override

- `--reply-account`: delivery account id override

- `--thinking <off|minimal|low|medium|high|xhigh>`: persist thinking level (GPT-5.2 + Codex models only)

- `--verbose <on|full|off>`: persist verbose level

- `--timeout <seconds>`: override agent timeout

- `--json`: output structured JSON

[Browser Troubleshooting](/tools/browser-linux-troubleshooting)[Sub-Agents](/tools/subagents)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)