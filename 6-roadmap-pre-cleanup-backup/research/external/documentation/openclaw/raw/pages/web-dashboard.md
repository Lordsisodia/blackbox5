---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/web/dashboard",
    "fetched_at": "2026-02-07T10:23:53.568637",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 472633
  },
  "metadata": {
    "title": "Dashboard",
    "section": "dashboard",
    "tier": 3,
    "type": "reference"
  }
}
---

- Dashboard - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationWeb interfacesDashboard[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations- Security and sandboxing- Protocols and APIs- Networking and discoveryRemote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [Dashboard (Control UI)](#dashboard-control-ui)- [Fast path (recommended)](#fast-path-recommended)- [Token basics (local vs remote)](#token-basics-local-vs-remote)- [If you see “unauthorized” / 1008](#if-you-see-%E2%80%9Cunauthorized%E2%80%9D-%2F-1008)Web interfaces# Dashboard# [​](#dashboard-control-ui)Dashboard (Control UI)

The Gateway dashboard is the browser Control UI served at `/` by default

(override with `gateway.controlUi.basePath`).

Quick open (local Gateway):

- [http://127.0.0.1:18789/](http://127.0.0.1:18789/) (or [http://localhost:18789/](http://localhost:18789/))

Key references:

- [Control UI](/web/control-ui) for usage and UI capabilities.

- [Tailscale](/gateway/tailscale) for Serve/Funnel automation.

- [Web surfaces](/web) for bind modes and security notes.

Authentication is enforced at the WebSocket handshake via `connect.params.auth`

(token or password). See `gateway.auth` in [Gateway configuration](/gateway/configuration).

Security note: the Control UI is an **admin surface** (chat, config, exec approvals).

Do not expose it publicly. The UI stores the token in `localStorage` after first load.

Prefer localhost, Tailscale Serve, or an SSH tunnel.

## [​](#fast-path-recommended)Fast path (recommended)

- After onboarding, the CLI auto-opens the dashboard and prints a clean (non-tokenized) link.

- Re-open anytime: `openclaw dashboard` (copies link, opens browser if possible, shows SSH hint if headless).

- If the UI prompts for auth, paste the token from `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`) into Control UI settings.

## [​](#token-basics-local-vs-remote)Token basics (local vs remote)

- **Localhost**: open `http://127.0.0.1:18789/`.

- **Token source**: `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`); the UI stores a copy in localStorage after you connect.

- **Not localhost**: use Tailscale Serve (tokenless if `gateway.auth.allowTailscale: true`), tailnet bind with a token, or an SSH tunnel. See [Web surfaces](/web).

## [​](#if-you-see-“unauthorized”-/-1008)If you see “unauthorized” / 1008

- Ensure the gateway is reachable (local: `openclaw status`; remote: SSH tunnel `ssh -N -L 18789:127.0.0.1:18789 user@host` then open `http://127.0.0.1:18789/`).

- Retrieve the token from the gateway host: `openclaw config get gateway.auth.token` (or generate one: `openclaw doctor --generate-gateway-token`).

- In the dashboard settings, paste the token into the auth field, then connect.

[Control UI](/web/control-ui)[WebChat](/web/webchat)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)