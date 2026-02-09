---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/environment",
    "fetched_at": "2026-02-07T10:17:02.190466",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 513616
  },
  "metadata": {
    "title": "Environment Variables",
    "section": "environment",
    "tier": 3,
    "type": "reference"
  }
}
---

- Environment Variables - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationEnvironment and debuggingEnvironment Variables[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Help- [Help](/help)- [Troubleshooting](/help/troubleshooting)- [FAQ](/help/faq)Community- [OpenClaw Lore](/start/lore)Environment and debugging- [Node.js](/install/node)- [Environment Variables](/environment)- [Debugging](/debugging)- [Testing](/testing)- [Scripts](/scripts)- [Session Management Deep Dive](/reference/session-management-compaction)Developer workflows- [Setup](/start/setup)- [Submitting a PR](/help/submitting-a-pr)- [Submitting an Issue](/help/submitting-an-issue)Docs meta- [Docs Hubs](/start/hubs)- [Docs directory](/start/docs-directory)On this page- [Environment variables](#environment-variables)- [Precedence (highest → lowest)](#precedence-highest-%E2%86%92-lowest)- [Config env block](#config-env-block)- [Shell env import](#shell-env-import)- [Env var substitution in config](#env-var-substitution-in-config)- [Related](#related)Environment and debugging# Environment Variables# [​](#environment-variables)Environment variables

OpenClaw pulls environment variables from multiple sources. The rule is **never override existing values**.

## [​](#precedence-highest-→-lowest)Precedence (highest → lowest)

- **Process environment** (what the Gateway process already has from the parent shell/daemon).

- **`.env` in the current working directory** (dotenv default; does not override).

- **Global `.env`** at `~/.openclaw/.env` (aka `$OPENCLAW_STATE_DIR/.env`; does not override).

- **Config `env` block** in `~/.openclaw/openclaw.json` (applied only if missing).

- **Optional login-shell import** (`env.shellEnv.enabled` or `OPENCLAW_LOAD_SHELL_ENV=1`), applied only for missing expected keys.

If the config file is missing entirely, step 4 is skipped; shell import still runs if enabled.

## [​](#config-env-block)Config `env` block

Two equivalent ways to set inline env vars (both are non-overriding):

Copy```

{

env: {

OPENROUTER_API_KEY: "sk-or-...",

vars: {

GROQ_API_KEY: "gsk-...",

},

},

}

```

## [​](#shell-env-import)Shell env import

`env.shellEnv` runs your login shell and imports only **missing** expected keys:

Copy```

{

env: {

shellEnv: {

enabled: true,

timeoutMs: 15000,

},

},

}

```

Env var equivalents:

- `OPENCLAW_LOAD_SHELL_ENV=1`

- `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`

## [​](#env-var-substitution-in-config)Env var substitution in config

You can reference env vars directly in config string values using `${VAR_NAME}` syntax:

Copy```

{

models: {

providers: {

"vercel-gateway": {

apiKey: "${VERCEL_GATEWAY_API_KEY}",

},

},

},

}

```

See [Configuration: Env var substitution](/gateway/configuration#env-var-substitution-in-config) for full details.

## [​](#related)Related

- [Gateway configuration](/gateway/configuration)

- [FAQ: env vars and .env loading](/help/faq#env-vars-and-env-loading)

- [Models overview](/concepts/models)

[Node.js](/install/node)[Debugging](/debugging)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)