---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/gateway/gateway-lock",
    "fetched_at": "2026-02-07T10:17:39.244649",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 473951
  },
  "metadata": {
    "title": "Gateway Lock",
    "section": "gateway-lock",
    "tier": 3,
    "type": "reference"
  }
}
---

- Gateway Lock - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationConfiguration and operationsGateway Lock[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations[Configuration](/gateway/configuration)- [Configuration Examples](/gateway/configuration-examples)- [Authentication](/gateway/authentication)- [Health Checks](/gateway/health)- [Heartbeat](/gateway/heartbeat)- [Doctor](/gateway/doctor)- [Logging](/gateway/logging)- [Gateway Lock](/gateway/gateway-lock)- [Background Exec and Process Tool](/gateway/background-process)- [Multiple Gateways](/gateway/multiple-gateways)- [Troubleshooting](/gateway/troubleshooting)- Security and sandboxing- Protocols and APIs- Networking and discoveryRemote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [Gateway lock](#gateway-lock)- [Why](#why)- [Mechanism](#mechanism)- [Error surface](#error-surface)- [Operational notes](#operational-notes)Configuration and operations# Gateway Lock# [​](#gateway-lock)Gateway lock

Last updated: 2025-12-11

## [​](#why)Why

- Ensure only one gateway instance runs per base port on the same host; additional gateways must use isolated profiles and unique ports.

- Survive crashes/SIGKILL without leaving stale lock files.

- Fail fast with a clear error when the control port is already occupied.

## [​](#mechanism)Mechanism

- The gateway binds the WebSocket listener (default `ws://127.0.0.1:18789`) immediately on startup using an exclusive TCP listener.

- If the bind fails with `EADDRINUSE`, startup throws `GatewayLockError("another gateway instance is already listening on ws://127.0.0.1:<port>")`.

- The OS releases the listener automatically on any process exit, including crashes and SIGKILL—no separate lock file or cleanup step is needed.

- On shutdown the gateway closes the WebSocket server and underlying HTTP server to free the port promptly.

## [​](#error-surface)Error surface

- If another process holds the port, startup throws `GatewayLockError("another gateway instance is already listening on ws://127.0.0.1:<port>")`.

- Other bind failures surface as `GatewayLockError("failed to bind gateway socket on ws://127.0.0.1:<port>: …")`.

## [​](#operational-notes)Operational notes

- If the port is occupied by *another* process, the error is the same; free the port or choose another with `openclaw gateway --port <port>`.

- The macOS app still maintains its own lightweight PID guard before spawning the gateway; the runtime lock is enforced by the WebSocket bind.

[Logging](/gateway/logging)[Background Exec and Process Tool](/gateway/background-process)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)