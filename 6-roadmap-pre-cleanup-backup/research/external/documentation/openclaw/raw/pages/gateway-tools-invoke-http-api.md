---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/gateway/tools-invoke-http-api",
    "fetched_at": "2026-02-07T10:18:52.715421",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 511366
  },
  "metadata": {
    "title": "Tools Invoke API",
    "section": "tools-invoke-http-api",
    "tier": 3,
    "type": "reference"
  }
}
---

- Tools Invoke API - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationProtocols and APIsTools Invoke API[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations- Security and sandboxing- Protocols and APIs[Gateway Protocol](/gateway/protocol)- [Bridge Protocol](/gateway/bridge-protocol)- [OpenAI Chat Completions](/gateway/openai-http-api)- [Tools Invoke API](/gateway/tools-invoke-http-api)- [CLI Backends](/gateway/cli-backends)- [Local Models](/gateway/local-models)- Networking and discoveryRemote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [Tools Invoke (HTTP)](#tools-invoke-http)- [Authentication](#authentication)- [Request body](#request-body)- [Policy + routing behavior](#policy-%2B-routing-behavior)- [Responses](#responses)- [Example](#example)Protocols and APIs# Tools Invoke API# [​](#tools-invoke-http)Tools Invoke (HTTP)

OpenClaw’s Gateway exposes a simple HTTP endpoint for invoking a single tool directly. It is always enabled, but gated by Gateway auth and tool policy.

- `POST /tools/invoke`

- Same port as the Gateway (WS + HTTP multiplex): `http://<gateway-host>:<port>/tools/invoke`

Default max payload size is 2 MB.

## [​](#authentication)Authentication

Uses the Gateway auth configuration. Send a bearer token:

- `Authorization: Bearer <token>`

Notes:

- When `gateway.auth.mode="token"`, use `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`).

- When `gateway.auth.mode="password"`, use `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`).

## [​](#request-body)Request body

Copy```

{

"tool": "sessions_list",

"action": "json",

"args": {},

"sessionKey": "main",

"dryRun": false

}

```

Fields:

- `tool` (string, required): tool name to invoke.

- `action` (string, optional): mapped into args if the tool schema supports `action` and the args payload omitted it.

- `args` (object, optional): tool-specific arguments.

- `sessionKey` (string, optional): target session key. If omitted or `"main"`, the Gateway uses the configured main session key (honors `session.mainKey` and default agent, or `global` in global scope).

- `dryRun` (boolean, optional): reserved for future use; currently ignored.

## [​](#policy-+-routing-behavior)Policy + routing behavior

Tool availability is filtered through the same policy chain used by Gateway agents:

- `tools.profile` / `tools.byProvider.profile`

- `tools.allow` / `tools.byProvider.allow`

- `agents.<id>.tools.allow` / `agents.<id>.tools.byProvider.allow`

- group policies (if the session key maps to a group or channel)

- subagent policy (when invoking with a subagent session key)

If a tool is not allowed by policy, the endpoint returns **404**.

To help group policies resolve context, you can optionally set:

- `x-openclaw-message-channel: <channel>` (example: `slack`, `telegram`)

- `x-openclaw-account-id: <accountId>` (when multiple accounts exist)

## [​](#responses)Responses

- `200` → `{ ok: true, result }`

- `400` → `{ ok: false, error: { type, message } }` (invalid request or tool error)

- `401` → unauthorized

- `404` → tool not available (not found or not allowlisted)

- `405` → method not allowed

## [​](#example)Example

Copy```

curl -sS http://127.0.0.1:18789/tools/invoke \

-H 'Authorization: Bearer YOUR_TOKEN' \

-H 'Content-Type: application/json' \

-d '{

"tool": "sessions_list",

"action": "json",

"args": {}

}'

```[OpenAI Chat Completions](/gateway/openai-http-api)[CLI Backends](/gateway/cli-backends)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)