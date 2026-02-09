---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/presence",
    "fetched_at": "2026-02-07T10:16:21.247103",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 503047
  },
  "metadata": {
    "title": "Presence",
    "section": "presence",
    "tier": 3,
    "type": "reference"
  }
}
---

- Presence - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMulti-agentPresence[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Fundamentals- [Gateway Architecture](/concepts/architecture)- [Agent Runtime](/concepts/agent)- [Agent Loop](/concepts/agent-loop)- [System Prompt](/concepts/system-prompt)- [Context](/concepts/context)- [Agent Workspace](/concepts/agent-workspace)- [Bootstrapping](/start/bootstrapping)- [OAuth](/concepts/oauth)Sessions and memory- [Session Management](/concepts/session)- [Sessions](/concepts/sessions)- [Session pruning](/concepts/session-pruning)- [Session Tools](/concepts/session-tool)- [Memory](/concepts/memory)- [Compaction](/concepts/compaction)Multi-agent- [Multi-Agent Routing](/concepts/multi-agent)- [Presence](/concepts/presence)Messages and delivery- [Messages](/concepts/messages)- [Streaming and Chunking](/concepts/streaming)- [Retry Policy](/concepts/retry)- [Command Queue](/concepts/queue)On this page- [Presence](#presence)- [Presence fields (what shows up)](#presence-fields-what-shows-up)- [Producers (where presence comes from)](#producers-where-presence-comes-from)- [1) Gateway self entry](#1-gateway-self-entry)- [2) WebSocket connect](#2-websocket-connect)- [Why one‑off CLI commands don’t show up](#why-one%E2%80%91off-cli-commands-don%E2%80%99t-show-up)- [3) system-event beacons](#3-system-event-beacons)- [4) Node connects (role: node)](#4-node-connects-role-node)- [Merge + dedupe rules (why instanceId matters)](#merge-%2B-dedupe-rules-why-instanceid-matters)- [TTL and bounded size](#ttl-and-bounded-size)- [Remote/tunnel caveat (loopback IPs)](#remote%2Ftunnel-caveat-loopback-ips)- [Consumers](#consumers)- [macOS Instances tab](#macos-instances-tab)- [Debugging tips](#debugging-tips)Multi-agent# Presence# [​](#presence)Presence

OpenClaw “presence” is a lightweight, best‑effort view of:

- the **Gateway** itself, and

- **clients connected to the Gateway** (mac app, WebChat, CLI, etc.)

Presence is used primarily to render the macOS app’s **Instances** tab and to

provide quick operator visibility.

## [​](#presence-fields-what-shows-up)Presence fields (what shows up)

Presence entries are structured objects with fields like:

- `instanceId` (optional but strongly recommended): stable client identity (usually `connect.client.instanceId`)

- `host`: human‑friendly host name

- `ip`: best‑effort IP address

- `version`: client version string

- `deviceFamily` / `modelIdentifier`: hardware hints

- `mode`: `ui`, `webchat`, `cli`, `backend`, `probe`, `test`, `node`, …

- `lastInputSeconds`: “seconds since last user input” (if known)

- `reason`: `self`, `connect`, `node-connected`, `periodic`, …

- `ts`: last update timestamp (ms since epoch)

## [​](#producers-where-presence-comes-from)Producers (where presence comes from)

Presence entries are produced by multiple sources and **merged**.

### [​](#1-gateway-self-entry)1) Gateway self entry

The Gateway always seeds a “self” entry at startup so UIs show the gateway host

even before any clients connect.

### [​](#2-websocket-connect)2) WebSocket connect

Every WS client begins with a `connect` request. On successful handshake the

Gateway upserts a presence entry for that connection.

#### [​](#why-one‑off-cli-commands-don’t-show-up)Why one‑off CLI commands don’t show up

The CLI often connects for short, one‑off commands. To avoid spamming the

Instances list, `client.mode === "cli"` is **not** turned into a presence entry.

### [​](#3-system-event-beacons)3) `system-event` beacons

Clients can send richer periodic beacons via the `system-event` method. The mac

app uses this to report host name, IP, and `lastInputSeconds`.

### [​](#4-node-connects-role-node)4) Node connects (role: node)

When a node connects over the Gateway WebSocket with `role: node`, the Gateway

upserts a presence entry for that node (same flow as other WS clients).

## [​](#merge-+-dedupe-rules-why-instanceid-matters)Merge + dedupe rules (why `instanceId` matters)

Presence entries are stored in a single in‑memory map:

- Entries are keyed by a **presence key**.

- The best key is a stable `instanceId` (from `connect.client.instanceId`) that survives restarts.

- Keys are case‑insensitive.

If a client reconnects without a stable `instanceId`, it may show up as a

**duplicate** row.

## [​](#ttl-and-bounded-size)TTL and bounded size

Presence is intentionally ephemeral:

- **TTL:** entries older than 5 minutes are pruned

- **Max entries:** 200 (oldest dropped first)

This keeps the list fresh and avoids unbounded memory growth.

## [​](#remote/tunnel-caveat-loopback-ips)Remote/tunnel caveat (loopback IPs)

When a client connects over an SSH tunnel / local port forward, the Gateway may

see the remote address as `127.0.0.1`. To avoid overwriting a good client‑reported

IP, loopback remote addresses are ignored.

## [​](#consumers)Consumers

### [​](#macos-instances-tab)macOS Instances tab

The macOS app renders the output of `system-presence` and applies a small status

indicator (Active/Idle/Stale) based on the age of the last update.

## [​](#debugging-tips)Debugging tips

- To see the raw list, call `system-presence` against the Gateway.

- If you see duplicates:

confirm clients send a stable `client.instanceId` in the handshake

- confirm periodic beacons use the same `instanceId`

- check whether the connection‑derived entry is missing `instanceId` (duplicates are expected)

[Multi-Agent Routing](/concepts/multi-agent)[Messages](/concepts/messages)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)