---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/start/getting-started",
    "fetched_at": "2026-02-07T10:11:03.804868",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 541905
  },
  "metadata": {
    "title": "Getting Started",
    "section": "getting-started",
    "tier": 1,
    "type": "reference"
  }
}
---

- Getting Started - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationFirst stepsGetting Started[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [OpenClaw](/)- [Features](/concepts/features)- [Showcase](/start/showcase)First steps- [Getting Started](/start/getting-started)- [Onboarding: CLI](/start/wizard)- [Onboarding: macOS App](/start/onboarding)Guides- [Personal Assistant Setup](/start/openclaw)On this page- [Getting Started](#getting-started)- [Prereqs](#prereqs)- [Quick setup (CLI)](#quick-setup-cli)- [Optional checks and extras](#optional-checks-and-extras)- [Go deeper](#go-deeper)- [What you will have](#what-you-will-have)- [Next steps](#next-steps)First steps# Getting Started# [​](#getting-started)Getting Started

Goal: go from zero to a first working chat with minimal setup.

Fastest chat: open the Control UI (no channel setup needed). Run `openclaw dashboard`

and chat in the browser, or open `http://127.0.0.1:18789/` on the

gateway host.

Docs: [Dashboard](/web/dashboard) and [Control UI](/web/control-ui).

## [​](#prereqs)Prereqs

- Node 22 or newer

Check your Node version with `node --version` if you are unsure.

## [​](#quick-setup-cli)Quick setup (CLI)

1[](#)Install OpenClaw (recommended)-  macOS/Linux-  Windows (PowerShell)Copy```

curl -fsSL https://openclaw.ai/install.sh | bash

```Copy```

iwr -useb https://openclaw.ai/install.ps1 | iex

```Other install methods and requirements: [Install](/install).2[](#)Run the onboarding wizardCopy```

openclaw onboard --install-daemon

```The wizard configures auth, gateway settings, and optional channels.

See [Onboarding Wizard](/start/wizard) for details.3[](#)Check the GatewayIf you installed the service, it should already be running:Copy```

openclaw gateway status

```4[](#)Open the Control UICopy```

openclaw dashboard

```

If the Control UI loads, your Gateway is ready for use.

## [​](#optional-checks-and-extras)Optional checks and extras

Run the Gateway in the foregroundUseful for quick tests or troubleshooting.Copy```

openclaw gateway --port 18789

```Send a test messageRequires a configured channel.Copy```

openclaw message send --target +15555550123 --message "Hello from OpenClaw"

```

## [​](#go-deeper)Go deeper

[## Onboarding Wizard (details)Full CLI wizard reference and advanced options.](/start/wizard)[## macOS app onboardingFirst run flow for the macOS app.](/start/onboarding)

## [​](#what-you-will-have)What you will have

- A running Gateway

- Auth configured

- Control UI access or a connected channel

## [​](#next-steps)Next steps

- DM safety and approvals: [Pairing](/start/pairing)

- Connect more channels: [Channels](/channels)

- Advanced workflows and from source: [Setup](/start/setup)

[Showcase](/start/showcase)[Onboarding: CLI](/start/wizard)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)