---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/gateway/bridge-protocol",
    "fetched_at": "2026-02-07T10:17:05.818027",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 491978
  },
  "metadata": {
    "title": "Bridge Protocol",
    "section": "bridge-protocol",
    "tier": 3,
    "type": "reference"
  }
}
---

- Bridge Protocol - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationProtocols and APIsBridge Protocol[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations- Security and sandboxing- Protocols and APIs[Gateway Protocol](/gateway/protocol)- [Bridge Protocol](/gateway/bridge-protocol)- [OpenAI Chat Completions](/gateway/openai-http-api)- [Tools Invoke API](/gateway/tools-invoke-http-api)- [CLI Backends](/gateway/cli-backends)- [Local Models](/gateway/local-models)- Networking and discoveryRemote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [Bridge protocol (legacy node transport)](#bridge-protocol-legacy-node-transport)- [Why we have both](#why-we-have-both)- [Transport](#transport)- [Handshake + pairing](#handshake-%2B-pairing)- [Frames](#frames)- [Exec lifecycle events](#exec-lifecycle-events)- [Tailnet usage](#tailnet-usage)- [Versioning](#versioning)Protocols and APIs# Bridge Protocol# [​](#bridge-protocol-legacy-node-transport)Bridge protocol (legacy node transport)

The Bridge protocol is a **legacy** node transport (TCP JSONL). New node clients

should use the unified Gateway WebSocket protocol instead.

If you are building an operator or node client, use the

[Gateway protocol](/gateway/protocol).

**Note:** Current OpenClaw builds no longer ship the TCP bridge listener; this document is kept for historical reference.

Legacy `bridge.*` config keys are no longer part of the config schema.

## [​](#why-we-have-both)Why we have both

- **Security boundary**: the bridge exposes a small allowlist instead of the

full gateway API surface.

- **Pairing + node identity**: node admission is owned by the gateway and tied

to a per-node token.

- **Discovery UX**: nodes can discover gateways via Bonjour on LAN, or connect

directly over a tailnet.

- **Loopback WS**: the full WS control plane stays local unless tunneled via SSH.

## [​](#transport)Transport

- TCP, one JSON object per line (JSONL).

- Optional TLS (when `bridge.tls.enabled` is true).

- Legacy default listener port was `18790` (current builds do not start a TCP bridge).

When TLS is enabled, discovery TXT records include `bridgeTls=1` plus

`bridgeTlsSha256` so nodes can pin the certificate.

## [​](#handshake-+-pairing)Handshake + pairing

- Client sends `hello` with node metadata + token (if already paired).

- If not paired, gateway replies `error` (`NOT_PAIRED`/`UNAUTHORIZED`).

- Client sends `pair-request`.

- Gateway waits for approval, then sends `pair-ok` and `hello-ok`.

`hello-ok` returns `serverName` and may include `canvasHostUrl`.

## [​](#frames)Frames

Client → Gateway:

- `req` / `res`: scoped gateway RPC (chat, sessions, config, health, voicewake, skills.bins)

- `event`: node signals (voice transcript, agent request, chat subscribe, exec lifecycle)

Gateway → Client:

- `invoke` / `invoke-res`: node commands (`canvas.*`, `camera.*`, `screen.record`,

`location.get`, `sms.send`)

- `event`: chat updates for subscribed sessions

- `ping` / `pong`: keepalive

Legacy allowlist enforcement lived in `src/gateway/server-bridge.ts` (removed).

## [​](#exec-lifecycle-events)Exec lifecycle events

Nodes can emit `exec.finished` or `exec.denied` events to surface system.run activity.

These are mapped to system events in the gateway. (Legacy nodes may still emit `exec.started`.)

Payload fields (all optional unless noted):

- `sessionKey` (required): agent session to receive the system event.

- `runId`: unique exec id for grouping.

- `command`: raw or formatted command string.

- `exitCode`, `timedOut`, `success`, `output`: completion details (finished only).

- `reason`: denial reason (denied only).

## [​](#tailnet-usage)Tailnet usage

- Bind the bridge to a tailnet IP: `bridge.bind: "tailnet"` in

`~/.openclaw/openclaw.json`.

- Clients connect via MagicDNS name or tailnet IP.

- Bonjour does **not** cross networks; use manual host/port or wide-area DNS‑SD

when needed.

## [​](#versioning)Versioning

Bridge is currently **implicit v1** (no min/max negotiation). Backward‑compat

is expected; add a bridge protocol version field before any breaking changes.[Gateway Protocol](/gateway/protocol)[OpenAI Chat Completions](/gateway/openai-http-api)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)