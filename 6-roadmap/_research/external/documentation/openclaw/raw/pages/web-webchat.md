---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/web/webchat",
    "fetched_at": "2026-02-07T10:23:54.823669",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 472580
  },
  "metadata": {
    "title": "WebChat",
    "section": "webchat",
    "tier": 3,
    "type": "reference"
  }
}
---

- WebChat - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationWeb interfacesWebChat[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations- Security and sandboxing- Protocols and APIs- Networking and discoveryRemote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [WebChat (Gateway WebSocket UI)](#webchat-gateway-websocket-ui)- [What it is](#what-it-is)- [Quick start](#quick-start)- [How it works (behavior)](#how-it-works-behavior)- [Remote use](#remote-use)- [Configuration reference (WebChat)](#configuration-reference-webchat)Web interfaces# WebChat# [​](#webchat-gateway-websocket-ui)WebChat (Gateway WebSocket UI)

Status: the macOS/iOS SwiftUI chat UI talks directly to the Gateway WebSocket.

## [​](#what-it-is)What it is

- A native chat UI for the gateway (no embedded browser and no local static server).

- Uses the same sessions and routing rules as other channels.

- Deterministic routing: replies always go back to WebChat.

## [​](#quick-start)Quick start

- Start the gateway.

- Open the WebChat UI (macOS/iOS app) or the Control UI chat tab.

- Ensure gateway auth is configured (required by default, even on loopback).

## [​](#how-it-works-behavior)How it works (behavior)

- The UI connects to the Gateway WebSocket and uses `chat.history`, `chat.send`, and `chat.inject`.

- `chat.inject` appends an assistant note directly to the transcript and broadcasts it to the UI (no agent run).

- History is always fetched from the gateway (no local file watching).

- If the gateway is unreachable, WebChat is read-only.

## [​](#remote-use)Remote use

- Remote mode tunnels the gateway WebSocket over SSH/Tailscale.

- You do not need to run a separate WebChat server.

## [​](#configuration-reference-webchat)Configuration reference (WebChat)

Full configuration: [Configuration](/gateway/configuration)

Channel options:

- No dedicated `webchat.*` block. WebChat uses the gateway endpoint + auth settings below.

Related global options:

- `gateway.port`, `gateway.bind`: WebSocket host/port.

- `gateway.auth.mode`, `gateway.auth.token`, `gateway.auth.password`: WebSocket auth.

- `gateway.remote.url`, `gateway.remote.token`, `gateway.remote.password`: remote gateway target.

- `session.*`: session storage and main key defaults.

[Dashboard](/web/dashboard)[TUI](/tui)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)