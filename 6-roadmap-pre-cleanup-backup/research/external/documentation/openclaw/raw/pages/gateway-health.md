---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/gateway/health",
    "fetched_at": "2026-02-07T10:17:39.831423",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 478798
  },
  "metadata": {
    "title": "Health Checks",
    "section": "health",
    "tier": 3,
    "type": "reference"
  }
}
---

- Health Checks - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationConfiguration and operationsHealth Checks[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations[Configuration](/gateway/configuration)- [Configuration Examples](/gateway/configuration-examples)- [Authentication](/gateway/authentication)- [Health Checks](/gateway/health)- [Heartbeat](/gateway/heartbeat)- [Doctor](/gateway/doctor)- [Logging](/gateway/logging)- [Gateway Lock](/gateway/gateway-lock)- [Background Exec and Process Tool](/gateway/background-process)- [Multiple Gateways](/gateway/multiple-gateways)- [Troubleshooting](/gateway/troubleshooting)- Security and sandboxing- Protocols and APIs- Networking and discoveryRemote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [Health Checks (CLI)](#health-checks-cli)- [Quick checks](#quick-checks)- [Deep diagnostics](#deep-diagnostics)- [When something fails](#when-something-fails)- [Dedicated “health” command](#dedicated-%E2%80%9Chealth%E2%80%9D-command)Configuration and operations# Health Checks# [​](#health-checks-cli)Health Checks (CLI)

Short guide to verify channel connectivity without guessing.

## [​](#quick-checks)Quick checks

- `openclaw status` — local summary: gateway reachability/mode, update hint, linked channel auth age, sessions + recent activity.

- `openclaw status --all` — full local diagnosis (read-only, color, safe to paste for debugging).

- `openclaw status --deep` — also probes the running Gateway (per-channel probes when supported).

- `openclaw health --json` — asks the running Gateway for a full health snapshot (WS-only; no direct Baileys socket).

- Send `/status` as a standalone message in WhatsApp/WebChat to get a status reply without invoking the agent.

- Logs: tail `/tmp/openclaw/openclaw-*.log` and filter for `web-heartbeat`, `web-reconnect`, `web-auto-reply`, `web-inbound`.

## [​](#deep-diagnostics)Deep diagnostics

- Creds on disk: `ls -l ~/.openclaw/credentials/whatsapp/<accountId>/creds.json` (mtime should be recent).

- Session store: `ls -l ~/.openclaw/agents/<agentId>/sessions/sessions.json` (path can be overridden in config). Count and recent recipients are surfaced via `status`.

- Relink flow: `openclaw channels logout && openclaw channels login --verbose` when status codes 409–515 or `loggedOut` appear in logs. (Note: the QR login flow auto-restarts once for status 515 after pairing.)

## [​](#when-something-fails)When something fails

- `logged out` or status 409–515 → relink with `openclaw channels logout` then `openclaw channels login`.

- Gateway unreachable → start it: `openclaw gateway --port 18789` (use `--force` if the port is busy).

- No inbound messages → confirm linked phone is online and the sender is allowed (`channels.whatsapp.allowFrom`); for group chats, ensure allowlist + mention rules match (`channels.whatsapp.groups`, `agents.list[].groupChat.mentionPatterns`).

## [​](#dedicated-“health”-command)Dedicated “health” command

`openclaw health --json` asks the running Gateway for its health snapshot (no direct channel sockets from the CLI). It reports linked creds/auth age when available, per-channel probe summaries, session-store summary, and a probe duration. It exits non-zero if the Gateway is unreachable or the probe fails/timeouts. Use `--timeout <ms>` to override the 10s default.[Authentication](/gateway/authentication)[Heartbeat](/gateway/heartbeat)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)