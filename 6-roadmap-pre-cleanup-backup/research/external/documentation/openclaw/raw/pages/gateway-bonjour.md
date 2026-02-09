---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/gateway/bonjour",
    "fetched_at": "2026-02-07T10:17:03.811808",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 564029
  },
  "metadata": {
    "title": "Bonjour Discovery",
    "section": "bonjour",
    "tier": 3,
    "type": "reference"
  }
}
---

- Bonjour Discovery - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationNetworking and discoveryBonjour Discovery[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Gateway- [Gateway Runbook](/gateway)- Configuration and operations- Security and sandboxing- Protocols and APIs- Networking and discovery[Network model](/gateway/network-model)- [Gateway-Owned Pairing](/gateway/pairing)- [Discovery and Transports](/gateway/discovery)- [Bonjour Discovery](/gateway/bonjour)Remote access- [Remote Access](/gateway/remote)- [Remote Gateway Setup](/gateway/remote-gateway-readme)- [Tailscale](/gateway/tailscale)Security- [Formal Verification (Security Models)](/security/formal-verification)Web interfaces- [Web](/web)- [Control UI](/web/control-ui)- [Dashboard](/web/dashboard)- [WebChat](/web/webchat)- [TUI](/tui)On this page- [Bonjour / mDNS discovery](#bonjour-%2F-mdns-discovery)- [Wide‑area Bonjour (Unicast DNS‑SD) over Tailscale](#wide%E2%80%91area-bonjour-unicast-dns%E2%80%91sd-over-tailscale)- [Gateway config (recommended)](#gateway-config-recommended)- [One‑time DNS server setup (gateway host)](#one%E2%80%91time-dns-server-setup-gateway-host)- [Tailscale DNS settings](#tailscale-dns-settings)- [Gateway listener security (recommended)](#gateway-listener-security-recommended)- [What advertises](#what-advertises)- [Service types](#service-types)- [TXT keys (non‑secret hints)](#txt-keys-non%E2%80%91secret-hints)- [Debugging on macOS](#debugging-on-macos)- [Debugging in Gateway logs](#debugging-in-gateway-logs)- [Debugging on iOS node](#debugging-on-ios-node)- [Common failure modes](#common-failure-modes)- [Escaped instance names (\032)](#escaped-instance-names-%5C032)- [Disabling / configuration](#disabling-%2F-configuration)- [Related docs](#related-docs)Networking and discovery# Bonjour Discovery# [​](#bonjour-/-mdns-discovery)Bonjour / mDNS discovery

OpenClaw uses Bonjour (mDNS / DNS‑SD) as a **LAN‑only convenience** to discover

an active Gateway (WebSocket endpoint). It is best‑effort and does **not** replace SSH or

Tailnet-based connectivity.

## [​](#wide‑area-bonjour-unicast-dns‑sd-over-tailscale)Wide‑area Bonjour (Unicast DNS‑SD) over Tailscale

If the node and gateway are on different networks, multicast mDNS won’t cross the

boundary. You can keep the same discovery UX by switching to **unicast DNS‑SD**

(“Wide‑Area Bonjour”) over Tailscale.

High‑level steps:

- Run a DNS server on the gateway host (reachable over Tailnet).

- Publish DNS‑SD records for `_openclaw-gw._tcp` under a dedicated zone

(example: `openclaw.internal.`).

- Configure Tailscale **split DNS** so your chosen domain resolves via that

DNS server for clients (including iOS).

OpenClaw supports any discovery domain; `openclaw.internal.` is just an example.

iOS/Android nodes browse both `local.` and your configured wide‑area domain.

### [​](#gateway-config-recommended)Gateway config (recommended)

Copy```

{

gateway: { bind: "tailnet" }, // tailnet-only (recommended)

discovery: { wideArea: { enabled: true } }, // enables wide-area DNS-SD publishing

}

```

### [​](#one‑time-dns-server-setup-gateway-host)One‑time DNS server setup (gateway host)

Copy```

openclaw dns setup --apply

```

This installs CoreDNS and configures it to:

- listen on port 53 only on the gateway’s Tailscale interfaces

- serve your chosen domain (example: `openclaw.internal.`) from `~/.openclaw/dns/<domain>.db`

Validate from a tailnet‑connected machine:

Copy```

dns-sd -B _openclaw-gw._tcp openclaw.internal.

dig @<TAILNET_IPV4> -p 53 _openclaw-gw._tcp.openclaw.internal PTR +short

```

### [​](#tailscale-dns-settings)Tailscale DNS settings

In the Tailscale admin console:

- Add a nameserver pointing at the gateway’s tailnet IP (UDP/TCP 53).

- Add split DNS so your discovery domain uses that nameserver.

Once clients accept tailnet DNS, iOS nodes can browse

`_openclaw-gw._tcp` in your discovery domain without multicast.

### [​](#gateway-listener-security-recommended)Gateway listener security (recommended)

The Gateway WS port (default `18789`) binds to loopback by default. For LAN/tailnet

access, bind explicitly and keep auth enabled.

For tailnet‑only setups:

- Set `gateway.bind: "tailnet"` in `~/.openclaw/openclaw.json`.

- Restart the Gateway (or restart the macOS menubar app).

## [​](#what-advertises)What advertises

Only the Gateway advertises `_openclaw-gw._tcp`.

## [​](#service-types)Service types

- `_openclaw-gw._tcp` — gateway transport beacon (used by macOS/iOS/Android nodes).

## [​](#txt-keys-non‑secret-hints)TXT keys (non‑secret hints)

The Gateway advertises small non‑secret hints to make UI flows convenient:

- `role=gateway`

- `displayName=<friendly name>`

- `lanHost=<hostname>.local`

- `gatewayPort=<port>` (Gateway WS + HTTP)

- `gatewayTls=1` (only when TLS is enabled)

- `gatewayTlsSha256=<sha256>` (only when TLS is enabled and fingerprint is available)

- `canvasPort=<port>` (only when the canvas host is enabled; default `18793`)

- `sshPort=<port>` (defaults to 22 when not overridden)

- `transport=gateway`

- `cliPath=<path>` (optional; absolute path to a runnable `openclaw` entrypoint)

- `tailnetDns=<magicdns>` (optional hint when Tailnet is available)

## [​](#debugging-on-macos)Debugging on macOS

Useful built‑in tools:

-

Browse instances:

Copy```

dns-sd -B _openclaw-gw._tcp local.

```

-

Resolve one instance (replace `<instance>`):

Copy```

dns-sd -L "<instance>" _openclaw-gw._tcp local.

```

If browsing works but resolving fails, you’re usually hitting a LAN policy or

mDNS resolver issue.

## [​](#debugging-in-gateway-logs)Debugging in Gateway logs

The Gateway writes a rolling log file (printed on startup as

`gateway log file: ...`). Look for `bonjour:` lines, especially:

- `bonjour: advertise failed ...`

- `bonjour: ... name conflict resolved` / `hostname conflict resolved`

- `bonjour: watchdog detected non-announced service ...`

## [​](#debugging-on-ios-node)Debugging on iOS node

The iOS node uses `NWBrowser` to discover `_openclaw-gw._tcp`.

To capture logs:

- Settings → Gateway → Advanced → **Discovery Debug Logs**

- Settings → Gateway → Advanced → **Discovery Logs** → reproduce → **Copy**

The log includes browser state transitions and result‑set changes.

## [​](#common-failure-modes)Common failure modes

- **Bonjour doesn’t cross networks**: use Tailnet or SSH.

- **Multicast blocked**: some Wi‑Fi networks disable mDNS.

- **Sleep / interface churn**: macOS may temporarily drop mDNS results; retry.

- **Browse works but resolve fails**: keep machine names simple (avoid emojis or

punctuation), then restart the Gateway. The service instance name derives from

the host name, so overly complex names can confuse some resolvers.

## [​](#escaped-instance-names-\032)Escaped instance names (`\032`)

Bonjour/DNS‑SD often escapes bytes in service instance names as decimal `\DDD`

sequences (e.g. spaces become `\032`).

- This is normal at the protocol level.

- UIs should decode for display (iOS uses `BonjourEscapes.decode`).

## [​](#disabling-/-configuration)Disabling / configuration

- `OPENCLAW_DISABLE_BONJOUR=1` disables advertising (legacy: `OPENCLAW_DISABLE_BONJOUR`).

- `gateway.bind` in `~/.openclaw/openclaw.json` controls the Gateway bind mode.

- `OPENCLAW_SSH_PORT` overrides the SSH port advertised in TXT (legacy: `OPENCLAW_SSH_PORT`).

- `OPENCLAW_TAILNET_DNS` publishes a MagicDNS hint in TXT (legacy: `OPENCLAW_TAILNET_DNS`).

- `OPENCLAW_CLI_PATH` overrides the advertised CLI path (legacy: `OPENCLAW_CLI_PATH`).

## [​](#related-docs)Related docs

- Discovery policy and transport selection: [Discovery](/gateway/discovery)

- Node pairing + approvals: [Gateway pairing](/gateway/pairing)

[Discovery and Transports](/gateway/discovery)[Remote Access](/gateway/remote)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)