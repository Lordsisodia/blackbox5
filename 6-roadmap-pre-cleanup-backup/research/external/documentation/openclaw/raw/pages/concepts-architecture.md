---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/architecture",
    "fetched_at": "2026-02-07T10:15:39.712780",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 527682
  },
  "metadata": {
    "title": "Gateway Architecture",
    "section": "architecture",
    "tier": 3,
    "type": "reference"
  }
}
---

- Gateway Architecture - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationFundamentalsGateway Architecture[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Fundamentals- [Gateway Architecture](/concepts/architecture)- [Agent Runtime](/concepts/agent)- [Agent Loop](/concepts/agent-loop)- [System Prompt](/concepts/system-prompt)- [Context](/concepts/context)- [Agent Workspace](/concepts/agent-workspace)- [Bootstrapping](/start/bootstrapping)- [OAuth](/concepts/oauth)Sessions and memory- [Session Management](/concepts/session)- [Sessions](/concepts/sessions)- [Session pruning](/concepts/session-pruning)- [Session Tools](/concepts/session-tool)- [Memory](/concepts/memory)- [Compaction](/concepts/compaction)Multi-agent- [Multi-Agent Routing](/concepts/multi-agent)- [Presence](/concepts/presence)Messages and delivery- [Messages](/concepts/messages)- [Streaming and Chunking](/concepts/streaming)- [Retry Policy](/concepts/retry)- [Command Queue](/concepts/queue)On this page- [Gateway architecture](#gateway-architecture)- [Overview](#overview)- [Components and flows](#components-and-flows)- [Gateway (daemon)](#gateway-daemon)- [Clients (mac app / CLI / web admin)](#clients-mac-app-%2F-cli-%2F-web-admin)- [Nodes (macOS / iOS / Android / headless)](#nodes-macos-%2F-ios-%2F-android-%2F-headless)- [WebChat](#webchat)- [Connection lifecycle (single client)](#connection-lifecycle-single-client)- [Wire protocol (summary)](#wire-protocol-summary)- [Pairing + local trust](#pairing-%2B-local-trust)- [Protocol typing and codegen](#protocol-typing-and-codegen)- [Remote access](#remote-access)- [Operations snapshot](#operations-snapshot)- [Invariants](#invariants)Fundamentals# Gateway Architecture# [​](#gateway-architecture)Gateway architecture

Last updated: 2026-01-22

## [​](#overview)Overview

- A single long‑lived **Gateway** owns all messaging surfaces (WhatsApp via

Baileys, Telegram via grammY, Slack, Discord, Signal, iMessage, WebChat).

- Control-plane clients (macOS app, CLI, web UI, automations) connect to the

Gateway over **WebSocket** on the configured bind host (default

`127.0.0.1:18789`).

- **Nodes** (macOS/iOS/Android/headless) also connect over **WebSocket**, but

declare `role: node` with explicit caps/commands.

- One Gateway per host; it is the only place that opens a WhatsApp session.

- A **canvas host** (default `18793`) serves agent‑editable HTML and A2UI.

## [​](#components-and-flows)Components and flows

### [​](#gateway-daemon)Gateway (daemon)

- Maintains provider connections.

- Exposes a typed WS API (requests, responses, server‑push events).

- Validates inbound frames against JSON Schema.

- Emits events like `agent`, `chat`, `presence`, `health`, `heartbeat`, `cron`.

### [​](#clients-mac-app-/-cli-/-web-admin)Clients (mac app / CLI / web admin)

- One WS connection per client.

- Send requests (`health`, `status`, `send`, `agent`, `system-presence`).

- Subscribe to events (`tick`, `agent`, `presence`, `shutdown`).

### [​](#nodes-macos-/-ios-/-android-/-headless)Nodes (macOS / iOS / Android / headless)

- Connect to the **same WS server** with `role: node`.

- Provide a device identity in `connect`; pairing is **device‑based** (role `node`) and

approval lives in the device pairing store.

- Expose commands like `canvas.*`, `camera.*`, `screen.record`, `location.get`.

Protocol details:

- [Gateway protocol](/gateway/protocol)

### [​](#webchat)WebChat

- Static UI that uses the Gateway WS API for chat history and sends.

- In remote setups, connects through the same SSH/Tailscale tunnel as other

clients.

## [​](#connection-lifecycle-single-client)Connection lifecycle (single client)

Copy```

Client                    Gateway

|                          |

|---- req:connect -------->|

|<------ res (ok) ---------|   (or res error + close)

|   (payload=hello-ok carries snapshot: presence + health)

|                          |

|<------ event:presence ---|

|<------ event:tick -------|

|                          |

|------- req:agent ------->|

|<------ res:agent --------|   (ack: {runId,status:"accepted"})

|<------ event:agent ------|   (streaming)

|<------ res:agent --------|   (final: {runId,status,summary})

|                          |

```

## [​](#wire-protocol-summary)Wire protocol (summary)

- Transport: WebSocket, text frames with JSON payloads.

- First frame **must** be `connect`.

- After handshake:

Requests: `{type:"req", id, method, params}` → `{type:"res", id, ok, payload|error}`

- Events: `{type:"event", event, payload, seq?, stateVersion?}`

- If `OPENCLAW_GATEWAY_TOKEN` (or `--token`) is set, `connect.params.auth.token`

must match or the socket closes.

- Idempotency keys are required for side‑effecting methods (`send`, `agent`) to

safely retry; the server keeps a short‑lived dedupe cache.

- Nodes must include `role: "node"` plus caps/commands/permissions in `connect`.

## [​](#pairing-+-local-trust)Pairing + local trust

- All WS clients (operators + nodes) include a **device identity** on `connect`.

- New device IDs require pairing approval; the Gateway issues a **device token**

for subsequent connects.

- **Local** connects (loopback or the gateway host’s own tailnet address) can be

auto‑approved to keep same‑host UX smooth.

- **Non‑local** connects must sign the `connect.challenge` nonce and require

explicit approval.

- Gateway auth (`gateway.auth.*`) still applies to **all** connections, local or

remote.

Details: [Gateway protocol](/gateway/protocol), [Pairing](/start/pairing),

[Security](/gateway/security).

## [​](#protocol-typing-and-codegen)Protocol typing and codegen

- TypeBox schemas define the protocol.

- JSON Schema is generated from those schemas.

- Swift models are generated from the JSON Schema.

## [​](#remote-access)Remote access

-

Preferred: Tailscale or VPN.

-

Alternative: SSH tunnel

Copy```

ssh -N -L 18789:127.0.0.1:18789 user@host

```

-

The same handshake + auth token apply over the tunnel.

-

TLS + optional pinning can be enabled for WS in remote setups.

## [​](#operations-snapshot)Operations snapshot

- Start: `openclaw gateway` (foreground, logs to stdout).

- Health: `health` over WS (also included in `hello-ok`).

- Supervision: launchd/systemd for auto‑restart.

## [​](#invariants)Invariants

- Exactly one Gateway controls a single Baileys session per host.

- Handshake is mandatory; any non‑JSON or non‑connect first frame is a hard close.

- Events are not replayed; clients must refresh on gaps.

[Agent Runtime](/concepts/agent)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)