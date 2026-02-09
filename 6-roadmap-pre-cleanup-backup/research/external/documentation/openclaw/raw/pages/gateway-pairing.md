---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/gateway/pairing",
    "fetched_at": "2026-02-07T10:17:45.919446",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 510812
  },
  "metadata": {
    "title": "Gateway-Owned Pairing",
    "section": "pairing",
    "tier": 3,
    "type": "reference"
  }
}
---

- Gateway-Owned Pairing - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationNetworking and discoveryGateway-Owned Pairing[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations- Security and sandboxing- Protocols and APIs- Networking and discovery[Network model](/gateway/network-model)- [Gateway-Owned Pairing](/gateway/pairing)- [Discovery and Transports](/gateway/discovery)- [Bonjour Discovery](/gateway/bonjour)Remote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [Gateway-owned pairing (Option B)](#gateway-owned-pairing-option-b)- [Concepts](#concepts)- [How pairing works](#how-pairing-works)- [CLI workflow (headless friendly)](#cli-workflow-headless-friendly)- [API surface (gateway protocol)](#api-surface-gateway-protocol)- [Auto-approval (macOS app)](#auto-approval-macos-app)- [Storage (local, private)](#storage-local-private)- [Transport behavior](#transport-behavior)Networking and discovery# Gateway-Owned Pairing# [​](#gateway-owned-pairing-option-b)Gateway-owned pairing (Option B)

In Gateway-owned pairing, the **Gateway** is the source of truth for which nodes

are allowed to join. UIs (macOS app, future clients) are just frontends that

approve or reject pending requests.

**Important:** WS nodes use **device pairing** (role `node`) during `connect`.

`node.pair.*` is a separate pairing store and does **not** gate the WS handshake.

Only clients that explicitly call `node.pair.*` use this flow.

## [​](#concepts)Concepts

- **Pending request**: a node asked to join; requires approval.

- **Paired node**: approved node with an issued auth token.

- **Transport**: the Gateway WS endpoint forwards requests but does not decide

membership. (Legacy TCP bridge support is deprecated/removed.)

## [​](#how-pairing-works)How pairing works

- A node connects to the Gateway WS and requests pairing.

- The Gateway stores a **pending request** and emits `node.pair.requested`.

- You approve or reject the request (CLI or UI).

- On approval, the Gateway issues a **new token** (tokens are rotated on re‑pair).

- The node reconnects using the token and is now “paired”.

Pending requests expire automatically after **5 minutes**.

## [​](#cli-workflow-headless-friendly)CLI workflow (headless friendly)

Copy```

openclaw nodes pending

openclaw nodes approve <requestId>

openclaw nodes reject <requestId>

openclaw nodes status

openclaw nodes rename --node <id|name|ip> --name "Living Room iPad"

```

`nodes status` shows paired/connected nodes and their capabilities.

## [​](#api-surface-gateway-protocol)API surface (gateway protocol)

Events:

- `node.pair.requested` — emitted when a new pending request is created.

- `node.pair.resolved` — emitted when a request is approved/rejected/expired.

Methods:

- `node.pair.request` — create or reuse a pending request.

- `node.pair.list` — list pending + paired nodes.

- `node.pair.approve` — approve a pending request (issues token).

- `node.pair.reject` — reject a pending request.

- `node.pair.verify` — verify `{ nodeId, token }`.

Notes:

- `node.pair.request` is idempotent per node: repeated calls return the same

pending request.

- Approval **always** generates a fresh token; no token is ever returned from

`node.pair.request`.

- Requests may include `silent: true` as a hint for auto-approval flows.

## [​](#auto-approval-macos-app)Auto-approval (macOS app)

The macOS app can optionally attempt a **silent approval** when:

- the request is marked `silent`, and

- the app can verify an SSH connection to the gateway host using the same user.

If silent approval fails, it falls back to the normal “Approve/Reject” prompt.

## [​](#storage-local-private)Storage (local, private)

Pairing state is stored under the Gateway state directory (default `~/.openclaw`):

- `~/.openclaw/nodes/paired.json`

- `~/.openclaw/nodes/pending.json`

If you override `OPENCLAW_STATE_DIR`, the `nodes/` folder moves with it.

Security notes:

- Tokens are secrets; treat `paired.json` as sensitive.

- Rotating a token requires re-approval (or deleting the node entry).

## [​](#transport-behavior)Transport behavior

- The transport is **stateless**; it does not store membership.

- If the Gateway is offline or pairing is disabled, nodes cannot pair.

- If the Gateway is in remote mode, pairing still happens against the remote Gateway’s store.

[Network model](/gateway/network-model)[Discovery and Transports](/gateway/discovery)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)