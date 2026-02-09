---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/gateway/sandboxing",
    "fetched_at": "2026-02-07T10:18:50.006475",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 573433
  },
  "metadata": {
    "title": "Sandboxing",
    "section": "sandboxing",
    "tier": 3,
    "type": "reference"
  }
}
---

- Sandboxing - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationSecurity and sandboxingSandboxing[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations- Security and sandboxing[Security](/gateway/security)- [Sandboxing](/gateway/sandboxing)- [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated)- Protocols and APIs- Networking and discoveryRemote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [Sandboxing](#sandboxing)- [What gets sandboxed](#what-gets-sandboxed)- [Modes](#modes)- [Scope](#scope)- [Workspace access](#workspace-access)- [Custom bind mounts](#custom-bind-mounts)- [Images + setup](#images-%2B-setup)- [setupCommand (one-time container setup)](#setupcommand-one-time-container-setup)- [Tool policy + escape hatches](#tool-policy-%2B-escape-hatches)- [Multi-agent overrides](#multi-agent-overrides)- [Minimal enable example](#minimal-enable-example)- [Related docs](#related-docs)Security and sandboxing# Sandboxing# [​](#sandboxing)Sandboxing

OpenClaw can run **tools inside Docker containers** to reduce blast radius.

This is **optional** and controlled by configuration (`agents.defaults.sandbox` or

`agents.list[].sandbox`). If sandboxing is off, tools run on the host.

The Gateway stays on the host; tool execution runs in an isolated sandbox

when enabled.

This is not a perfect security boundary, but it materially limits filesystem

and process access when the model does something dumb.

## [​](#what-gets-sandboxed)What gets sandboxed

- Tool execution (`exec`, `read`, `write`, `edit`, `apply_patch`, `process`, etc.).

- Optional sandboxed browser (`agents.defaults.sandbox.browser`).

By default, the sandbox browser auto-starts (ensures CDP is reachable) when the browser tool needs it.

Configure via `agents.defaults.sandbox.browser.autoStart` and `agents.defaults.sandbox.browser.autoStartTimeoutMs`.

- `agents.defaults.sandbox.browser.allowHostControl` lets sandboxed sessions target the host browser explicitly.

- Optional allowlists gate `target: "custom"`: `allowedControlUrls`, `allowedControlHosts`, `allowedControlPorts`.

Not sandboxed:

- The Gateway process itself.

- Any tool explicitly allowed to run on the host (e.g. `tools.elevated`).

**Elevated exec runs on the host and bypasses sandboxing.**

- If sandboxing is off, `tools.elevated` does not change execution (already on host). See [Elevated Mode](/tools/elevated).

## [​](#modes)Modes

`agents.defaults.sandbox.mode` controls **when** sandboxing is used:

- `"off"`: no sandboxing.

- `"non-main"`: sandbox only **non-main** sessions (default if you want normal chats on host).

- `"all"`: every session runs in a sandbox.

Note: `"non-main"` is based on `session.mainKey` (default `"main"`), not agent id.

Group/channel sessions use their own keys, so they count as non-main and will be sandboxed.

## [​](#scope)Scope

`agents.defaults.sandbox.scope` controls **how many containers** are created:

- `"session"` (default): one container per session.

- `"agent"`: one container per agent.

- `"shared"`: one container shared by all sandboxed sessions.

## [​](#workspace-access)Workspace access

`agents.defaults.sandbox.workspaceAccess` controls **what the sandbox can see**:

- `"none"` (default): tools see a sandbox workspace under `~/.openclaw/sandboxes`.

- `"ro"`: mounts the agent workspace read-only at `/agent` (disables `write`/`edit`/`apply_patch`).

- `"rw"`: mounts the agent workspace read/write at `/workspace`.

Inbound media is copied into the active sandbox workspace (`media/inbound/*`).

Skills note: the `read` tool is sandbox-rooted. With `workspaceAccess: "none"`,

OpenClaw mirrors eligible skills into the sandbox workspace (`.../skills`) so

they can be read. With `"rw"`, workspace skills are readable from

`/workspace/skills`.

## [​](#custom-bind-mounts)Custom bind mounts

`agents.defaults.sandbox.docker.binds` mounts additional host directories into the container.

Format: `host:container:mode` (e.g., `"/home/user/source:/source:rw"`).

Global and per-agent binds are **merged** (not replaced). Under `scope: "shared"`, per-agent binds are ignored.

Example (read-only source + docker socket):

Copy```

{

agents: {

defaults: {

sandbox: {

docker: {

binds: ["/home/user/source:/source:ro", "/var/run/docker.sock:/var/run/docker.sock"],

},

},

},

list: [

{

id: "build",

sandbox: {

docker: {

binds: ["/mnt/cache:/cache:rw"],

},

},

},

],

},

}

```

Security notes:

- Binds bypass the sandbox filesystem: they expose host paths with whatever mode you set (`:ro` or `:rw`).

- Sensitive mounts (e.g., `docker.sock`, secrets, SSH keys) should be `:ro` unless absolutely required.

- Combine with `workspaceAccess: "ro"` if you only need read access to the workspace; bind modes stay independent.

- See [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated) for how binds interact with tool policy and elevated exec.

## [​](#images-+-setup)Images + setup

Default image: `openclaw-sandbox:bookworm-slim`

Build it once:

Copy```

scripts/sandbox-setup.sh

```

Note: the default image does **not** include Node. If a skill needs Node (or

other runtimes), either bake a custom image or install via

`sandbox.docker.setupCommand` (requires network egress + writable root +

root user).

Sandboxed browser image:

Copy```

scripts/sandbox-browser-setup.sh

```

By default, sandbox containers run with **no network**.

Override with `agents.defaults.sandbox.docker.network`.

Docker installs and the containerized gateway live here:

[Docker](/install/docker)

## [​](#setupcommand-one-time-container-setup)setupCommand (one-time container setup)

`setupCommand` runs **once** after the sandbox container is created (not on every run).

It executes inside the container via `sh -lc`.

Paths:

- Global: `agents.defaults.sandbox.docker.setupCommand`

- Per-agent: `agents.list[].sandbox.docker.setupCommand`

Common pitfalls:

- Default `docker.network` is `"none"` (no egress), so package installs will fail.

- `readOnlyRoot: true` prevents writes; set `readOnlyRoot: false` or bake a custom image.

- `user` must be root for package installs (omit `user` or set `user: "0:0"`).

- Sandbox exec does **not** inherit host `process.env`. Use

`agents.defaults.sandbox.docker.env` (or a custom image) for skill API keys.

## [​](#tool-policy-+-escape-hatches)Tool policy + escape hatches

Tool allow/deny policies still apply before sandbox rules. If a tool is denied

globally or per-agent, sandboxing doesn’t bring it back.

`tools.elevated` is an explicit escape hatch that runs `exec` on the host.

`/exec` directives only apply for authorized senders and persist per session; to hard-disable

`exec`, use tool policy deny (see [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated)).

Debugging:

- Use `openclaw sandbox explain` to inspect effective sandbox mode, tool policy, and fix-it config keys.

- See [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated) for the “why is this blocked?” mental model.

Keep it locked down.

## [​](#multi-agent-overrides)Multi-agent overrides

Each agent can override sandbox + tools:

`agents.list[].sandbox` and `agents.list[].tools` (plus `agents.list[].tools.sandbox.tools` for sandbox tool policy).

See [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools) for precedence.

## [​](#minimal-enable-example)Minimal enable example

Copy```

{

agents: {

defaults: {

sandbox: {

mode: "non-main",

scope: "session",

workspaceAccess: "none",

},

},

},

}

```

## [​](#related-docs)Related docs

- [Sandbox Configuration](/gateway/configuration#agentsdefaults-sandbox)

- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)

- [Security](/gateway/security)

[Security](/gateway/security)[Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)