---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/help/troubleshooting",
    "fetched_at": "2026-02-07T10:18:58.559143",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 529441
  },
  "metadata": {
    "title": "Troubleshooting",
    "section": "troubleshooting",
    "tier": 3,
    "type": "reference"
  }
}
---

- Troubleshooting - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationHelpTroubleshooting[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Help- [Help](/help)- [Troubleshooting](/help/troubleshooting)- [FAQ](/help/faq)Community- [OpenClaw Lore](/start/lore)Environment and debugging- [Node.js](/install/node)- [Environment Variables](/environment)- [Debugging](/debugging)- [Testing](/testing)- [Scripts](/scripts)- [Session Management Deep Dive](/reference/session-management-compaction)Developer workflows- [Setup](/start/setup)- [Submitting a PR](/help/submitting-a-pr)- [Submitting an Issue](/help/submitting-an-issue)Docs meta- [Docs Hubs](/start/hubs)- [Docs directory](/start/docs-directory)On this page- [Troubleshooting](#troubleshooting)- [First 60 seconds](#first-60-seconds)- [Common “it broke” cases](#common-%E2%80%9Cit-broke%E2%80%9D-cases)- [openclaw: command not found](#openclaw-command-not-found)- [Installer fails (or you need full logs)](#installer-fails-or-you-need-full-logs)- [Gateway “unauthorized”, can’t connect, or keeps reconnecting](#gateway-%E2%80%9Cunauthorized%E2%80%9D-can%E2%80%99t-connect-or-keeps-reconnecting)- [Control UI fails on HTTP (device identity required)](#control-ui-fails-on-http-device-identity-required)- [docs.openclaw.ai shows an SSL error (Comcast/Xfinity)](#docs-openclaw-ai-shows-an-ssl-error-comcast%2Fxfinity)- [Service says running, but RPC probe fails](#service-says-running-but-rpc-probe-fails)- [Model/auth failures (rate limit, billing, “all models failed”)](#model%2Fauth-failures-rate-limit-billing-%E2%80%9Call-models-failed%E2%80%9D)- [/model says model not allowed](#%2Fmodel-says-model-not-allowed)- [When filing an issue](#when-filing-an-issue)Help# Troubleshooting# [​](#troubleshooting)Troubleshooting

## [​](#first-60-seconds)First 60 seconds

Run these in order:

Copy```

openclaw status

openclaw status --all

openclaw gateway probe

openclaw logs --follow

openclaw doctor

```

If the gateway is reachable, deep probes:

Copy```

openclaw status --deep

```

## [​](#common-“it-broke”-cases)Common “it broke” cases

### [​](#openclaw-command-not-found)`openclaw: command not found`

Almost always a Node/npm PATH issue. Start here:

- [Install (Node/npm PATH sanity)](/install#nodejs--npm-path-sanity)

### [​](#installer-fails-or-you-need-full-logs)Installer fails (or you need full logs)

Re-run the installer in verbose mode to see the full trace and npm output:

Copy```

curl -fsSL https://openclaw.ai/install.sh | bash -s -- --verbose

```

For beta installs:

Copy```

curl -fsSL https://openclaw.ai/install.sh | bash -s -- --beta --verbose

```

You can also set `OPENCLAW_VERBOSE=1` instead of the flag.

### [​](#gateway-“unauthorized”-can’t-connect-or-keeps-reconnecting)Gateway “unauthorized”, can’t connect, or keeps reconnecting

- [Gateway troubleshooting](/gateway/troubleshooting)

- [Gateway authentication](/gateway/authentication)

### [​](#control-ui-fails-on-http-device-identity-required)Control UI fails on HTTP (device identity required)

- [Gateway troubleshooting](/gateway/troubleshooting)

- [Control UI](/web/control-ui#insecure-http)

### [​](#docs-openclaw-ai-shows-an-ssl-error-comcast/xfinity)`docs.openclaw.ai` shows an SSL error (Comcast/Xfinity)

Some Comcast/Xfinity connections block `docs.openclaw.ai` via Xfinity Advanced Security.

Disable Advanced Security or add `docs.openclaw.ai` to the allowlist, then retry.

- Xfinity Advanced Security help: [https://www.xfinity.com/support/articles/using-xfinity-xfi-advanced-security](https://www.xfinity.com/support/articles/using-xfinity-xfi-advanced-security)

- Quick sanity checks: try a mobile hotspot or VPN to confirm it’s ISP-level filtering

### [​](#service-says-running-but-rpc-probe-fails)Service says running, but RPC probe fails

- [Gateway troubleshooting](/gateway/troubleshooting)

- [Background process / service](/gateway/background-process)

### [​](#model/auth-failures-rate-limit-billing-“all-models-failed”)Model/auth failures (rate limit, billing, “all models failed”)

- [Models](/cli/models)

- [OAuth / auth concepts](/concepts/oauth)

### [​](#/model-says-model-not-allowed)`/model` says `model not allowed`

This usually means `agents.defaults.models` is configured as an allowlist. When it’s non-empty,

only those provider/model keys can be selected.

- Check the allowlist: `openclaw config get agents.defaults.models`

- Add the model you want (or clear the allowlist) and retry `/model`

- Use `/models` to browse the allowed providers/models

### [​](#when-filing-an-issue)When filing an issue

Paste a safe report:

Copy```

openclaw status --all

```

If you can, include the relevant log tail from `openclaw logs --follow`.[Help](/help)[FAQ](/help/faq)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)