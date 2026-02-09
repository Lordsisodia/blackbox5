---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/gateway/remote",
    "fetched_at": "2026-02-07T10:18:17.171093",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 528708
  },
  "metadata": {
    "title": "Remote Access",
    "section": "remote",
    "tier": 3,
    "type": "reference"
  }
}
---

- Remote Access - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationRemote accessRemote Access[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations- Security and sandboxing- Protocols and APIs- Networking and discoveryRemote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [Remote access (SSH, tunnels, and tailnets)](#remote-access-ssh-tunnels-and-tailnets)- [The core idea](#the-core-idea)- [Common VPN/tailnet setups (where the agent lives)](#common-vpn%2Ftailnet-setups-where-the-agent-lives)- [1) Always-on Gateway in your tailnet (VPS or home server)](#1-always-on-gateway-in-your-tailnet-vps-or-home-server)- [2) Home desktop runs the Gateway, laptop is remote control](#2-home-desktop-runs-the-gateway-laptop-is-remote-control)- [3) Laptop runs the Gateway, remote access from other machines](#3-laptop-runs-the-gateway-remote-access-from-other-machines)- [Command flow (what runs where)](#command-flow-what-runs-where)- [SSH tunnel (CLI + tools)](#ssh-tunnel-cli-%2B-tools)- [CLI remote defaults](#cli-remote-defaults)- [Chat UI over SSH](#chat-ui-over-ssh)- [macOS app “Remote over SSH”](#macos-app-%E2%80%9Cremote-over-ssh%E2%80%9D)- [Security rules (remote/VPN)](#security-rules-remote%2Fvpn)Remote access# Remote Access# [​](#remote-access-ssh-tunnels-and-tailnets)Remote access (SSH, tunnels, and tailnets)

This repo supports “remote over SSH” by keeping a single Gateway (the master) running on a dedicated host (desktop/server) and connecting clients to it.

- For **operators (you / the macOS app)**: SSH tunneling is the universal fallback.

- For **nodes (iOS/Android and future devices)**: connect to the Gateway **WebSocket** (LAN/tailnet or SSH tunnel as needed).

## [​](#the-core-idea)The core idea

- The Gateway WebSocket binds to **loopback** on your configured port (defaults to 18789).

- For remote use, you forward that loopback port over SSH (or use a tailnet/VPN and tunnel less).

## [​](#common-vpn/tailnet-setups-where-the-agent-lives)Common VPN/tailnet setups (where the agent lives)

Think of the **Gateway host** as “where the agent lives.” It owns sessions, auth profiles, channels, and state.

Your laptop/desktop (and nodes) connect to that host.

### [​](#1-always-on-gateway-in-your-tailnet-vps-or-home-server)1) Always-on Gateway in your tailnet (VPS or home server)

Run the Gateway on a persistent host and reach it via **Tailscale** or SSH.

- **Best UX:** keep `gateway.bind: "loopback"` and use **Tailscale Serve** for the Control UI.

- **Fallback:** keep loopback + SSH tunnel from any machine that needs access.

- **Examples:** [exe.dev](/install/exe-dev) (easy VM) or [Hetzner](/install/hetzner) (production VPS).

This is ideal when your laptop sleeps often but you want the agent always-on.

### [​](#2-home-desktop-runs-the-gateway-laptop-is-remote-control)2) Home desktop runs the Gateway, laptop is remote control

The laptop does **not** run the agent. It connects remotely:

- Use the macOS app’s **Remote over SSH** mode (Settings → General → “OpenClaw runs”).

- The app opens and manages the tunnel, so WebChat + health checks “just work.”

Runbook: [macOS remote access](/platforms/mac/remote).

### [​](#3-laptop-runs-the-gateway-remote-access-from-other-machines)3) Laptop runs the Gateway, remote access from other machines

Keep the Gateway local but expose it safely:

- SSH tunnel to the laptop from other machines, or

- Tailscale Serve the Control UI and keep the Gateway loopback-only.

Guide: [Tailscale](/gateway/tailscale) and [Web overview](/web).

## [​](#command-flow-what-runs-where)Command flow (what runs where)

One gateway service owns state + channels. Nodes are peripherals.

Flow example (Telegram → node):

- Telegram message arrives at the **Gateway**.

- Gateway runs the **agent** and decides whether to call a node tool.

- Gateway calls the **node** over the Gateway WebSocket (`node.*` RPC).

- Node returns the result; Gateway replies back out to Telegram.

Notes:

- **Nodes do not run the gateway service.** Only one gateway should run per host unless you intentionally run isolated profiles (see [Multiple gateways](/gateway/multiple-gateways)).

- macOS app “node mode” is just a node client over the Gateway WebSocket.

## [​](#ssh-tunnel-cli-+-tools)SSH tunnel (CLI + tools)

Create a local tunnel to the remote Gateway WS:

Copy```

ssh -N -L 18789:127.0.0.1:18789 user@host

```

With the tunnel up:

- `openclaw health` and `openclaw status --deep` now reach the remote gateway via `ws://127.0.0.1:18789`.

- `openclaw gateway {status,health,send,agent,call}` can also target the forwarded URL via `--url` when needed.

Note: replace `18789` with your configured `gateway.port` (or `--port`/`OPENCLAW_GATEWAY_PORT`).

Note: when you pass `--url`, the CLI does not fall back to config or environment credentials.

Include `--token` or `--password` explicitly. Missing explicit credentials is an error.

## [​](#cli-remote-defaults)CLI remote defaults

You can persist a remote target so CLI commands use it by default:

Copy```

{

gateway: {

mode: "remote",

remote: {

url: "ws://127.0.0.1:18789",

token: "your-token",

},

},

}

```

When the gateway is loopback-only, keep the URL at `ws://127.0.0.1:18789` and open the SSH tunnel first.

## [​](#chat-ui-over-ssh)Chat UI over SSH

WebChat no longer uses a separate HTTP port. The SwiftUI chat UI connects directly to the Gateway WebSocket.

- Forward `18789` over SSH (see above), then connect clients to `ws://127.0.0.1:18789`.

- On macOS, prefer the app’s “Remote over SSH” mode, which manages the tunnel automatically.

## [​](#macos-app-“remote-over-ssh”)macOS app “Remote over SSH”

The macOS menu bar app can drive the same setup end-to-end (remote status checks, WebChat, and Voice Wake forwarding).

Runbook: [macOS remote access](/platforms/mac/remote).

## [​](#security-rules-remote/vpn)Security rules (remote/VPN)

Short version: **keep the Gateway loopback-only** unless you’re sure you need a bind.

- **Loopback + SSH/Tailscale Serve** is the safest default (no public exposure).

- **Non-loopback binds** (`lan`/`tailnet`/`custom`, or `auto` when loopback is unavailable) must use auth tokens/passwords.

- `gateway.remote.token` is **only** for remote CLI calls — it does **not** enable local auth.

- `gateway.remote.tlsFingerprint` pins the remote TLS cert when using `wss://`.

- **Tailscale Serve** can authenticate via identity headers when `gateway.auth.allowTailscale: true`.

Set it to `false` if you want tokens/passwords instead.

- Treat browser control like operator access: tailnet-only + deliberate node pairing.

Deep dive: [Security](/gateway/security).[Bonjour Discovery](/gateway/bonjour)[Remote Gateway Setup](/gateway/remote-gateway-readme)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)