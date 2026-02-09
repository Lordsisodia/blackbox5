---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/tools/exec",
    "fetched_at": "2026-02-07T10:23:16.711645",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 644523
  },
  "metadata": {
    "title": "Exec Tool",
    "section": "exec",
    "tier": 3,
    "type": "reference"
  }
}
---

- Exec Tool - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationBuilt-in toolsExec Tool[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Exec tool](#exec-tool)- [Parameters](#parameters)- [Config](#config)- [PATH handling](#path-handling)- [Session overrides (/exec)](#session-overrides-%2Fexec)- [Authorization model](#authorization-model)- [Exec approvals (companion app / node host)](#exec-approvals-companion-app-%2F-node-host)- [Allowlist + safe bins](#allowlist-%2B-safe-bins)- [Examples](#examples)- [apply_patch (experimental)](#apply_patch-experimental)Built-in tools# Exec Tool# [​](#exec-tool)Exec tool

Run shell commands in the workspace. Supports foreground + background execution via `process`.

If `process` is disallowed, `exec` runs synchronously and ignores `yieldMs`/`background`.

Background sessions are scoped per agent; `process` only sees sessions from the same agent.

## [​](#parameters)Parameters

- `command` (required)

- `workdir` (defaults to cwd)

- `env` (key/value overrides)

- `yieldMs` (default 10000): auto-background after delay

- `background` (bool): background immediately

- `timeout` (seconds, default 1800): kill on expiry

- `pty` (bool): run in a pseudo-terminal when available (TTY-only CLIs, coding agents, terminal UIs)

- `host` (`sandbox | gateway | node`): where to execute

- `security` (`deny | allowlist | full`): enforcement mode for `gateway`/`node`

- `ask` (`off | on-miss | always`): approval prompts for `gateway`/`node`

- `node` (string): node id/name for `host=node`

- `elevated` (bool): request elevated mode (gateway host); `security=full` is only forced when elevated resolves to `full`

Notes:

- `host` defaults to `sandbox`.

- `elevated` is ignored when sandboxing is off (exec already runs on the host).

- `gateway`/`node` approvals are controlled by `~/.openclaw/exec-approvals.json`.

- `node` requires a paired node (companion app or headless node host).

- If multiple nodes are available, set `exec.node` or `tools.exec.node` to select one.

- On non-Windows hosts, exec uses `SHELL` when set; if `SHELL` is `fish`, it prefers `bash` (or `sh`)

from `PATH` to avoid fish-incompatible scripts, then falls back to `SHELL` if neither exists.

- Host execution (`gateway`/`node`) rejects `env.PATH` and loader overrides (`LD_*`/`DYLD_*`) to

prevent binary hijacking or injected code.

- Important: sandboxing is **off by default**. If sandboxing is off, `host=sandbox` runs directly on

the gateway host (no container) and **does not require approvals**. To require approvals, run with

`host=gateway` and configure exec approvals (or enable sandboxing).

## [​](#config)Config

- `tools.exec.notifyOnExit` (default: true): when true, backgrounded exec sessions enqueue a system event and request a heartbeat on exit.

- `tools.exec.approvalRunningNoticeMs` (default: 10000): emit a single “running” notice when an approval-gated exec runs longer than this (0 disables).

- `tools.exec.host` (default: `sandbox`)

- `tools.exec.security` (default: `deny` for sandbox, `allowlist` for gateway + node when unset)

- `tools.exec.ask` (default: `on-miss`)

- `tools.exec.node` (default: unset)

- `tools.exec.pathPrepend`: list of directories to prepend to `PATH` for exec runs.

- `tools.exec.safeBins`: stdin-only safe binaries that can run without explicit allowlist entries.

Example:

Copy```

{

tools: {

exec: {

pathPrepend: ["~/bin", "/opt/oss/bin"],

},

},

}

```

### [​](#path-handling)PATH handling

- `host=gateway`: merges your login-shell `PATH` into the exec environment. `env.PATH` overrides are

rejected for host execution. The daemon itself still runs with a minimal `PATH`:

macOS: `/opt/homebrew/bin`, `/usr/local/bin`, `/usr/bin`, `/bin`

- Linux: `/usr/local/bin`, `/usr/bin`, `/bin`

- `host=sandbox`: runs `sh -lc` (login shell) inside the container, so `/etc/profile` may reset `PATH`.

OpenClaw prepends `env.PATH` after profile sourcing via an internal env var (no shell interpolation);

`tools.exec.pathPrepend` applies here too.

- `host=node`: only non-blocked env overrides you pass are sent to the node. `env.PATH` overrides are

rejected for host execution. Headless node hosts accept `PATH` only when it prepends the node host

PATH (no replacement). macOS nodes drop `PATH` overrides entirely.

Per-agent node binding (use the agent list index in config):

Copy```

openclaw config get agents.list

openclaw config set agents.list[0].tools.exec.node "node-id-or-name"

```

Control UI: the Nodes tab includes a small “Exec node binding” panel for the same settings.

## [​](#session-overrides-/exec)Session overrides (`/exec`)

Use `/exec` to set **per-session** defaults for `host`, `security`, `ask`, and `node`.

Send `/exec` with no arguments to show the current values.

Example:

Copy```

/exec host=gateway security=allowlist ask=on-miss node=mac-1

```

## [​](#authorization-model)Authorization model

`/exec` is only honored for **authorized senders** (channel allowlists/pairing plus `commands.useAccessGroups`).

It updates **session state only** and does not write config. To hard-disable exec, deny it via tool

policy (`tools.deny: ["exec"]` or per-agent). Host approvals still apply unless you explicitly set

`security=full` and `ask=off`.

## [​](#exec-approvals-companion-app-/-node-host)Exec approvals (companion app / node host)

Sandboxed agents can require per-request approval before `exec` runs on the gateway or node host.

See [Exec approvals](/tools/exec-approvals) for the policy, allowlist, and UI flow.

When approvals are required, the exec tool returns immediately with

`status: "approval-pending"` and an approval id. Once approved (or denied / timed out),

the Gateway emits system events (`Exec finished` / `Exec denied`). If the command is still

running after `tools.exec.approvalRunningNoticeMs`, a single `Exec running` notice is emitted.

## [​](#allowlist-+-safe-bins)Allowlist + safe bins

Allowlist enforcement matches **resolved binary paths only** (no basename matches). When

`security=allowlist`, shell commands are auto-allowed only if every pipeline segment is

allowlisted or a safe bin. Chaining (`;`, `&&`, `||`) and redirections are rejected in

allowlist mode.

## [​](#examples)Examples

Foreground:

Copy```

{ "tool": "exec", "command": "ls -la" }

```

Background + poll:

Copy```

{"tool":"exec","command":"npm run build","yieldMs":1000}

{"tool":"process","action":"poll","sessionId":"<id>"}

```

Send keys (tmux-style):

Copy```

{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["Enter"]}

{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["C-c"]}

{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["Up","Up","Enter"]}

```

Submit (send CR only):

Copy```

{ "tool": "process", "action": "submit", "sessionId": "<id>" }

```

Paste (bracketed by default):

Copy```

{ "tool": "process", "action": "paste", "sessionId": "<id>", "text": "line1\nline2\n" }

```

## [​](#apply_patch-experimental)apply_patch (experimental)

`apply_patch` is a subtool of `exec` for structured multi-file edits.

Enable it explicitly:

Copy```

{

tools: {

exec: {

applyPatch: { enabled: true, allowModels: ["gpt-5.2"] },

},

},

}

```

Notes:

- Only available for OpenAI/OpenAI Codex models.

- Tool policy still applies; `allow: ["exec"]` implicitly allows `apply_patch`.

- Config lives under `tools.exec.applyPatch`.

[LLM Task](/tools/llm-task)[Web Tools](/tools/web)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)