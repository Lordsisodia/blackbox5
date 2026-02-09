---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/gateway/discovery",
    "fetched_at": "2026-02-07T10:17:37.813803",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 507732
  },
  "metadata": {
    "title": "Discovery and Transports",
    "section": "discovery",
    "tier": 3,
    "type": "reference"
  }
}
---

- Discovery and Transports - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationNetworking and discoveryDiscovery and Transports[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations- Security and sandboxing- Protocols and APIs- Networking and discovery[Network model](/gateway/network-model)- [Gateway-Owned Pairing](/gateway/pairing)- [Discovery and Transports](/gateway/discovery)- [Bonjour Discovery](/gateway/bonjour)Remote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [Discovery & transports](#discovery-%26-transports)- [Terms](#terms)- [Why we keep both “direct” and SSH](#why-we-keep-both-%E2%80%9Cdirect%E2%80%9D-and-ssh)- [Discovery inputs (how clients learn where the gateway is)](#discovery-inputs-how-clients-learn-where-the-gateway-is)- [1) Bonjour / mDNS (LAN only)](#1-bonjour-%2F-mdns-lan-only)- [Service beacon details](#service-beacon-details)- [2) Tailnet (cross-network)](#2-tailnet-cross-network)- [3) Manual / SSH target](#3-manual-%2F-ssh-target)- [Transport selection (client policy)](#transport-selection-client-policy)- [Pairing + auth (direct transport)](#pairing-%2B-auth-direct-transport)- [Responsibilities by component](#responsibilities-by-component)Networking and discovery# Discovery and Transports# [​](#discovery-&-transports)Discovery & transports

OpenClaw has two distinct problems that look similar on the surface:

- **Operator remote control**: the macOS menu bar app controlling a gateway running elsewhere.

- **Node pairing**: iOS/Android (and future nodes) finding a gateway and pairing securely.

The design goal is to keep all network discovery/advertising in the **Node Gateway** (`openclaw gateway`) and keep clients (mac app, iOS) as consumers.

## [​](#terms)Terms

- **Gateway**: a single long-running gateway process that owns state (sessions, pairing, node registry) and runs channels. Most setups use one per host; isolated multi-gateway setups are possible.

- **Gateway WS (control plane)**: the WebSocket endpoint on `127.0.0.1:18789` by default; can be bound to LAN/tailnet via `gateway.bind`.

- **Direct WS transport**: a LAN/tailnet-facing Gateway WS endpoint (no SSH).

- **SSH transport (fallback)**: remote control by forwarding `127.0.0.1:18789` over SSH.

- **Legacy TCP bridge (deprecated/removed)**: older node transport (see [Bridge protocol](/gateway/bridge-protocol)); no longer advertised for discovery.

Protocol details:

- [Gateway protocol](/gateway/protocol)

- [Bridge protocol (legacy)](/gateway/bridge-protocol)

## [​](#why-we-keep-both-“direct”-and-ssh)Why we keep both “direct” and SSH

- **Direct WS** is the best UX on the same network and within a tailnet:

auto-discovery on LAN via Bonjour

- pairing tokens + ACLs owned by the gateway

- no shell access required; protocol surface can stay tight and auditable

- **SSH** remains the universal fallback:

works anywhere you have SSH access (even across unrelated networks)

- survives multicast/mDNS issues

- requires no new inbound ports besides SSH

## [​](#discovery-inputs-how-clients-learn-where-the-gateway-is)Discovery inputs (how clients learn where the gateway is)

### [​](#1-bonjour-/-mdns-lan-only)1) Bonjour / mDNS (LAN only)

Bonjour is best-effort and does not cross networks. It is only used for “same LAN” convenience.

Target direction:

- The **gateway** advertises its WS endpoint via Bonjour.

- Clients browse and show a “pick a gateway” list, then store the chosen endpoint.

Troubleshooting and beacon details: [Bonjour](/gateway/bonjour).

#### [​](#service-beacon-details)Service beacon details

- Service types:

`_openclaw-gw._tcp` (gateway transport beacon)

- TXT keys (non-secret):

`role=gateway`

- `lanHost=<hostname>.local`

- `sshPort=22` (or whatever is advertised)

- `gatewayPort=18789` (Gateway WS + HTTP)

- `gatewayTls=1` (only when TLS is enabled)

- `gatewayTlsSha256=<sha256>` (only when TLS is enabled and fingerprint is available)

- `canvasPort=18793` (default canvas host port; serves `/__openclaw__/canvas/`)

- `cliPath=<path>` (optional; absolute path to a runnable `openclaw` entrypoint or binary)

- `tailnetDns=<magicdns>` (optional hint; auto-detected when Tailscale is available)

Disable/override:

- `OPENCLAW_DISABLE_BONJOUR=1` disables advertising.

- `gateway.bind` in `~/.openclaw/openclaw.json` controls the Gateway bind mode.

- `OPENCLAW_SSH_PORT` overrides the SSH port advertised in TXT (defaults to 22).

- `OPENCLAW_TAILNET_DNS` publishes a `tailnetDns` hint (MagicDNS).

- `OPENCLAW_CLI_PATH` overrides the advertised CLI path.

### [​](#2-tailnet-cross-network)2) Tailnet (cross-network)

For London/Vienna style setups, Bonjour won’t help. The recommended “direct” target is:

- Tailscale MagicDNS name (preferred) or a stable tailnet IP.

If the gateway can detect it is running under Tailscale, it publishes `tailnetDns` as an optional hint for clients (including wide-area beacons).

### [​](#3-manual-/-ssh-target)3) Manual / SSH target

When there is no direct route (or direct is disabled), clients can always connect via SSH by forwarding the loopback gateway port.

See [Remote access](/gateway/remote).

## [​](#transport-selection-client-policy)Transport selection (client policy)

Recommended client behavior:

- If a paired direct endpoint is configured and reachable, use it.

- Else, if Bonjour finds a gateway on LAN, offer a one-tap “Use this gateway” choice and save it as the direct endpoint.

- Else, if a tailnet DNS/IP is configured, try direct.

- Else, fall back to SSH.

## [​](#pairing-+-auth-direct-transport)Pairing + auth (direct transport)

The gateway is the source of truth for node/client admission.

- Pairing requests are created/approved/rejected in the gateway (see [Gateway pairing](/gateway/pairing)).

- The gateway enforces:

auth (token / keypair)

- scopes/ACLs (the gateway is not a raw proxy to every method)

- rate limits

## [​](#responsibilities-by-component)Responsibilities by component

- **Gateway**: advertises discovery beacons, owns pairing decisions, and hosts the WS endpoint.

- **macOS app**: helps you pick a gateway, shows pairing prompts, and uses SSH only as a fallback.

- **iOS/Android nodes**: browse Bonjour as a convenience and connect to the paired Gateway WS.

[Gateway-Owned Pairing](/gateway/pairing)[Bonjour Discovery](/gateway/bonjour)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)