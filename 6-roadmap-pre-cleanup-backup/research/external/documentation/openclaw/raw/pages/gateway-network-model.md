---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/gateway/network-model",
    "fetched_at": "2026-02-07T10:17:44.677298",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 461359
  },
  "metadata": {
    "title": "Network model",
    "section": "network-model",
    "tier": 3,
    "type": "reference"
  }
}
---

- Network model - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationNetworking and discoveryNetwork model[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations- Security and sandboxing- Protocols and APIs- Networking and discovery[Network model](/gateway/network-model)- [Gateway-Owned Pairing](/gateway/pairing)- [Discovery and Transports](/gateway/discovery)- [Bonjour Discovery](/gateway/bonjour)Remote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [Core rules](#core-rules)Networking and discovery# Network modelMost operations flow through the Gateway (`openclaw gateway`), a single long-running

process that owns channel connections and the WebSocket control plane.

## [​](#core-rules)Core rules

- One Gateway per host is recommended. It is the only process allowed to own the WhatsApp Web session. For rescue bots or strict isolation, run multiple gateways with isolated profiles and ports. See [Multiple gateways](/gateway/multiple-gateways).

- Loopback first: the Gateway WS defaults to `ws://127.0.0.1:18789`. The wizard generates a gateway token by default, even for loopback. For tailnet access, run `openclaw gateway --bind tailnet --token ...` because tokens are required for non-loopback binds.

- Nodes connect to the Gateway WS over LAN, tailnet, or SSH as needed. The legacy TCP bridge is deprecated.

- Canvas host is an HTTP file server on `canvasHost.port` (default `18793`) serving `/__openclaw__/canvas/` for node WebViews. See [Gateway configuration](/gateway/configuration) (`canvasHost`).

- Remote use is typically SSH tunnel or tailnet VPN. See [Remote access](/gateway/remote) and [Discovery](/gateway/discovery).

[Local Models](/gateway/local-models)[Gateway-Owned Pairing](/gateway/pairing)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)