---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/gateway/openai-http-api",
    "fetched_at": "2026-02-07T10:17:45.272273",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 543524
  },
  "metadata": {
    "title": "OpenAI Chat Completions",
    "section": "openai-http-api",
    "tier": 3,
    "type": "reference"
  }
}
---

- OpenAI Chat Completions - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationProtocols and APIsOpenAI Chat Completions[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations- Security and sandboxing- Protocols and APIs[Gateway Protocol](/gateway/protocol)- [Bridge Protocol](/gateway/bridge-protocol)- [OpenAI Chat Completions](/gateway/openai-http-api)- [Tools Invoke API](/gateway/tools-invoke-http-api)- [CLI Backends](/gateway/cli-backends)- [Local Models](/gateway/local-models)- Networking and discoveryRemote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [OpenAI Chat Completions (HTTP)](#openai-chat-completions-http)- [Authentication](#authentication)- [Choosing an agent](#choosing-an-agent)- [Enabling the endpoint](#enabling-the-endpoint)- [Disabling the endpoint](#disabling-the-endpoint)- [Session behavior](#session-behavior)- [Streaming (SSE)](#streaming-sse)- [Examples](#examples)Protocols and APIs# OpenAI Chat Completions# [​](#openai-chat-completions-http)OpenAI Chat Completions (HTTP)

OpenClaw’s Gateway can serve a small OpenAI-compatible Chat Completions endpoint.

This endpoint is **disabled by default**. Enable it in config first.

- `POST /v1/chat/completions`

- Same port as the Gateway (WS + HTTP multiplex): `http://<gateway-host>:<port>/v1/chat/completions`

Under the hood, requests are executed as a normal Gateway agent run (same codepath as `openclaw agent`), so routing/permissions/config match your Gateway.

## [​](#authentication)Authentication

Uses the Gateway auth configuration. Send a bearer token:

- `Authorization: Bearer <token>`

Notes:

- When `gateway.auth.mode="token"`, use `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`).

- When `gateway.auth.mode="password"`, use `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`).

## [​](#choosing-an-agent)Choosing an agent

No custom headers required: encode the agent id in the OpenAI `model` field:

- `model: "openclaw:<agentId>"` (example: `"openclaw:main"`, `"openclaw:beta"`)

- `model: "agent:<agentId>"` (alias)

Or target a specific OpenClaw agent by header:

- `x-openclaw-agent-id: <agentId>` (default: `main`)

Advanced:

- `x-openclaw-session-key: <sessionKey>` to fully control session routing.

## [​](#enabling-the-endpoint)Enabling the endpoint

Set `gateway.http.endpoints.chatCompletions.enabled` to `true`:

Copy```

{

gateway: {

http: {

endpoints: {

chatCompletions: { enabled: true },

},

},

},

}

```

## [​](#disabling-the-endpoint)Disabling the endpoint

Set `gateway.http.endpoints.chatCompletions.enabled` to `false`:

Copy```

{

gateway: {

http: {

endpoints: {

chatCompletions: { enabled: false },

},

},

},

}

```

## [​](#session-behavior)Session behavior

By default the endpoint is **stateless per request** (a new session key is generated each call).

If the request includes an OpenAI `user` string, the Gateway derives a stable session key from it, so repeated calls can share an agent session.

## [​](#streaming-sse)Streaming (SSE)

Set `stream: true` to receive Server-Sent Events (SSE):

- `Content-Type: text/event-stream`

- Each event line is `data: <json>`

- Stream ends with `data: [DONE]`

## [​](#examples)Examples

Non-streaming:

Copy```

curl -sS http://127.0.0.1:18789/v1/chat/completions \

-H 'Authorization: Bearer YOUR_TOKEN' \

-H 'Content-Type: application/json' \

-H 'x-openclaw-agent-id: main' \

-d '{

"model": "openclaw",

"messages": [{"role":"user","content":"hi"}]

}'

```

Streaming:

Copy```

curl -N http://127.0.0.1:18789/v1/chat/completions \

-H 'Authorization: Bearer YOUR_TOKEN' \

-H 'Content-Type: application/json' \

-H 'x-openclaw-agent-id: main' \

-d '{

"model": "openclaw",

"stream": true,

"messages": [{"role":"user","content":"hi"}]

}'

```[Bridge Protocol](/gateway/bridge-protocol)[Tools Invoke API](/gateway/tools-invoke-http-api)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)