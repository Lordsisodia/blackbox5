---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated",
    "fetched_at": "2026-02-07T10:18:49.409581",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 543824
  },
  "metadata": {
    "title": "Sandbox vs Tool Policy vs Elevated",
    "section": "sandbox-vs-tool-policy-vs-elevated",
    "tier": 3,
    "type": "reference"
  }
}
---

- Sandbox vs Tool Policy vs Elevated - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationSecurity and sandboxingSandbox vs Tool Policy vs Elevated[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations- Security and sandboxing[Security](/gateway/security)- [Sandboxing](/gateway/sandboxing)- [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated)- Protocols and APIs- Networking and discoveryRemote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [Sandbox vs Tool Policy vs Elevated](#sandbox-vs-tool-policy-vs-elevated)- [Quick debug](#quick-debug)- [Sandbox: where tools run](#sandbox-where-tools-run)- [Bind mounts (security quick check)](#bind-mounts-security-quick-check)- [Tool policy: which tools exist/are callable](#tool-policy-which-tools-exist%2Fare-callable)- [Tool groups (shorthands)](#tool-groups-shorthands)- [Elevated: exec-only “run on host”](#elevated-exec-only-%E2%80%9Crun-on-host%E2%80%9D)- [Common “sandbox jail” fixes](#common-%E2%80%9Csandbox-jail%E2%80%9D-fixes)- [“Tool X blocked by sandbox tool policy”](#%E2%80%9Ctool-x-blocked-by-sandbox-tool-policy%E2%80%9D)- [“I thought this was main, why is it sandboxed?”](#%E2%80%9Ci-thought-this-was-main-why-is-it-sandboxed%E2%80%9D)Security and sandboxing# Sandbox vs Tool Policy vs Elevated# [​](#sandbox-vs-tool-policy-vs-elevated)Sandbox vs Tool Policy vs Elevated

OpenClaw has three related (but different) controls:

- **Sandbox** (`agents.defaults.sandbox.*` / `agents.list[].sandbox.*`) decides **where tools run** (Docker vs host).

- **Tool policy** (`tools.*`, `tools.sandbox.tools.*`, `agents.list[].tools.*`) decides **which tools are available/allowed**.

- **Elevated** (`tools.elevated.*`, `agents.list[].tools.elevated.*`) is an **exec-only escape hatch** to run on the host when you’re sandboxed.

## [​](#quick-debug)Quick debug

Use the inspector to see what OpenClaw is *actually* doing:

Copy```

openclaw sandbox explain

openclaw sandbox explain --session agent:main:main

openclaw sandbox explain --agent work

openclaw sandbox explain --json

```

It prints:

- effective sandbox mode/scope/workspace access

- whether the session is currently sandboxed (main vs non-main)

- effective sandbox tool allow/deny (and whether it came from agent/global/default)

- elevated gates and fix-it key paths

## [​](#sandbox-where-tools-run)Sandbox: where tools run

Sandboxing is controlled by `agents.defaults.sandbox.mode`:

- `"off"`: everything runs on the host.

- `"non-main"`: only non-main sessions are sandboxed (common “surprise” for groups/channels).

- `"all"`: everything is sandboxed.

See [Sandboxing](/gateway/sandboxing) for the full matrix (scope, workspace mounts, images).

### [​](#bind-mounts-security-quick-check)Bind mounts (security quick check)

- `docker.binds` *pierces* the sandbox filesystem: whatever you mount is visible inside the container with the mode you set (`:ro` or `:rw`).

- Default is read-write if you omit the mode; prefer `:ro` for source/secrets.

- `scope: "shared"` ignores per-agent binds (only global binds apply).

- Binding `/var/run/docker.sock` effectively hands host control to the sandbox; only do this intentionally.

- Workspace access (`workspaceAccess: "ro"`/`"rw"`) is independent of bind modes.

## [​](#tool-policy-which-tools-exist/are-callable)Tool policy: which tools exist/are callable

Two layers matter:

- **Tool profile**: `tools.profile` and `agents.list[].tools.profile` (base allowlist)

- **Provider tool profile**: `tools.byProvider[provider].profile` and `agents.list[].tools.byProvider[provider].profile`

- **Global/per-agent tool policy**: `tools.allow`/`tools.deny` and `agents.list[].tools.allow`/`agents.list[].tools.deny`

- **Provider tool policy**: `tools.byProvider[provider].allow/deny` and `agents.list[].tools.byProvider[provider].allow/deny`

- **Sandbox tool policy** (only applies when sandboxed): `tools.sandbox.tools.allow`/`tools.sandbox.tools.deny` and `agents.list[].tools.sandbox.tools.*`

Rules of thumb:

- `deny` always wins.

- If `allow` is non-empty, everything else is treated as blocked.

- Tool policy is the hard stop: `/exec` cannot override a denied `exec` tool.

- `/exec` only changes session defaults for authorized senders; it does not grant tool access.

Provider tool keys accept either `provider` (e.g. `google-antigravity`) or `provider/model` (e.g. `openai/gpt-5.2`).

### [​](#tool-groups-shorthands)Tool groups (shorthands)

Tool policies (global, agent, sandbox) support `group:*` entries that expand to multiple tools:

Copy```

{

tools: {

sandbox: {

tools: {

allow: ["group:runtime", "group:fs", "group:sessions", "group:memory"],

},

},

},

}

```

Available groups:

- `group:runtime`: `exec`, `bash`, `process`

- `group:fs`: `read`, `write`, `edit`, `apply_patch`

- `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`

- `group:memory`: `memory_search`, `memory_get`

- `group:ui`: `browser`, `canvas`

- `group:automation`: `cron`, `gateway`

- `group:messaging`: `message`

- `group:nodes`: `nodes`

- `group:openclaw`: all built-in OpenClaw tools (excludes provider plugins)

## [​](#elevated-exec-only-“run-on-host”)Elevated: exec-only “run on host”

Elevated does **not** grant extra tools; it only affects `exec`.

- If you’re sandboxed, `/elevated on` (or `exec` with `elevated: true`) runs on the host (approvals may still apply).

- Use `/elevated full` to skip exec approvals for the session.

- If you’re already running direct, elevated is effectively a no-op (still gated).

- Elevated is **not** skill-scoped and does **not** override tool allow/deny.

- `/exec` is separate from elevated. It only adjusts per-session exec defaults for authorized senders.

Gates:

- Enablement: `tools.elevated.enabled` (and optionally `agents.list[].tools.elevated.enabled`)

- Sender allowlists: `tools.elevated.allowFrom.<provider>` (and optionally `agents.list[].tools.elevated.allowFrom.<provider>`)

See [Elevated Mode](/tools/elevated).

## [​](#common-“sandbox-jail”-fixes)Common “sandbox jail” fixes

### [​](#“tool-x-blocked-by-sandbox-tool-policy”)“Tool X blocked by sandbox tool policy”

Fix-it keys (pick one):

- Disable sandbox: `agents.defaults.sandbox.mode=off` (or per-agent `agents.list[].sandbox.mode=off`)

- Allow the tool inside sandbox:

remove it from `tools.sandbox.tools.deny` (or per-agent `agents.list[].tools.sandbox.tools.deny`)

- or add it to `tools.sandbox.tools.allow` (or per-agent allow)

### [​](#“i-thought-this-was-main-why-is-it-sandboxed”)“I thought this was main, why is it sandboxed?”

In `"non-main"` mode, group/channel keys are *not* main. Use the main session key (shown by `sandbox explain`) or switch mode to `"off"`.[Sandboxing](/gateway/sandboxing)[Gateway Protocol](/gateway/protocol)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)