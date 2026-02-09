---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/tools/elevated",
    "fetched_at": "2026-02-07T10:23:16.131353",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 499702
  },
  "metadata": {
    "title": "Elevated Mode",
    "section": "elevated",
    "tier": 3,
    "type": "reference"
  }
}
---

- Elevated Mode - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationBuilt-in toolsElevated Mode[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Elevated Mode (/elevated directives)](#elevated-mode-%2Felevated-directives)- [What it does](#what-it-does)- [What it controls (and what it doesn’t)](#what-it-controls-and-what-it-doesn%E2%80%99t)- [Resolution order](#resolution-order)- [Setting a session default](#setting-a-session-default)- [Availability + allowlists](#availability-%2B-allowlists)- [Logging + status](#logging-%2B-status)Built-in tools# Elevated Mode# [​](#elevated-mode-/elevated-directives)Elevated Mode (/elevated directives)

## [​](#what-it-does)What it does

- `/elevated on` runs on the gateway host and keeps exec approvals (same as `/elevated ask`).

- `/elevated full` runs on the gateway host **and** auto-approves exec (skips exec approvals).

- `/elevated ask` runs on the gateway host but keeps exec approvals (same as `/elevated on`).

- `on`/`ask` do **not** force `exec.security=full`; configured security/ask policy still applies.

- Only changes behavior when the agent is **sandboxed** (otherwise exec already runs on the host).

- Directive forms: `/elevated on|off|ask|full`, `/elev on|off|ask|full`.

- Only `on|off|ask|full` are accepted; anything else returns a hint and does not change state.

## [​](#what-it-controls-and-what-it-doesn’t)What it controls (and what it doesn’t)

- **Availability gates**: `tools.elevated` is the global baseline. `agents.list[].tools.elevated` can further restrict elevated per agent (both must allow).

- **Per-session state**: `/elevated on|off|ask|full` sets the elevated level for the current session key.

- **Inline directive**: `/elevated on|ask|full` inside a message applies to that message only.

- **Groups**: In group chats, elevated directives are only honored when the agent is mentioned. Command-only messages that bypass mention requirements are treated as mentioned.

- **Host execution**: elevated forces `exec` onto the gateway host; `full` also sets `security=full`.

- **Approvals**: `full` skips exec approvals; `on`/`ask` honor them when allowlist/ask rules require.

- **Unsandboxed agents**: no-op for location; only affects gating, logging, and status.

- **Tool policy still applies**: if `exec` is denied by tool policy, elevated cannot be used.

- **Separate from `/exec`**: `/exec` adjusts per-session defaults for authorized senders and does not require elevated.

## [​](#resolution-order)Resolution order

- Inline directive on the message (applies only to that message).

- Session override (set by sending a directive-only message).

- Global default (`agents.defaults.elevatedDefault` in config).

## [​](#setting-a-session-default)Setting a session default

- Send a message that is **only** the directive (whitespace allowed), e.g. `/elevated full`.

- Confirmation reply is sent (`Elevated mode set to full...` / `Elevated mode disabled.`).

- If elevated access is disabled or the sender is not on the approved allowlist, the directive replies with an actionable error and does not change session state.

- Send `/elevated` (or `/elevated:`) with no argument to see the current elevated level.

## [​](#availability-+-allowlists)Availability + allowlists

- Feature gate: `tools.elevated.enabled` (default can be off via config even if the code supports it).

- Sender allowlist: `tools.elevated.allowFrom` with per-provider allowlists (e.g. `discord`, `whatsapp`).

- Per-agent gate: `agents.list[].tools.elevated.enabled` (optional; can only further restrict).

- Per-agent allowlist: `agents.list[].tools.elevated.allowFrom` (optional; when set, the sender must match **both** global + per-agent allowlists).

- Discord fallback: if `tools.elevated.allowFrom.discord` is omitted, the `channels.discord.dm.allowFrom` list is used as a fallback. Set `tools.elevated.allowFrom.discord` (even `[]`) to override. Per-agent allowlists do **not** use the fallback.

- All gates must pass; otherwise elevated is treated as unavailable.

## [​](#logging-+-status)Logging + status

- Elevated exec calls are logged at info level.

- Session status includes elevated mode (e.g. `elevated=ask`, `elevated=full`).

[apply_patch Tool](/tools/apply-patch)[Thinking Levels](/tools/thinking)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)