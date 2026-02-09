---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/model-failover",
    "fetched_at": "2026-02-07T10:16:18.060653",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 532219
  },
  "metadata": {
    "title": "Model Failover",
    "section": "model-failover",
    "tier": 3,
    "type": "reference"
  }
}
---

- Model Failover - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationConfigurationModel Failover[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Model Providers](/providers)- [Model Provider Quickstart](/providers/models)- [Models CLI](/concepts/models)Configuration- [Model Providers](/concepts/model-providers)- [Model Failover](/concepts/model-failover)Providers- [Anthropic](/providers/anthropic)- [OpenAI](/providers/openai)- [OpenRouter](/providers/openrouter)- [Amazon Bedrock](/bedrock)- [Vercel AI Gateway](/providers/vercel-ai-gateway)- [Moonshot AI](/providers/moonshot)- [MiniMax](/providers/minimax)- [OpenCode Zen](/providers/opencode)- [GLM Models](/providers/glm)- [Z.AI](/providers/zai)- [Synthetic](/providers/synthetic)On this page- [Model failover](#model-failover)- [Auth storage (keys + OAuth)](#auth-storage-keys-%2B-oauth)- [Profile IDs](#profile-ids)- [Rotation order](#rotation-order)- [Session stickiness (cache-friendly)](#session-stickiness-cache-friendly)- [Why OAuth can “look lost”](#why-oauth-can-%E2%80%9Clook-lost%E2%80%9D)- [Cooldowns](#cooldowns)- [Billing disables](#billing-disables)- [Model fallback](#model-fallback)- [Related config](#related-config)Configuration# Model Failover# [​](#model-failover)Model failover

OpenClaw handles failures in two stages:

- **Auth profile rotation** within the current provider.

- **Model fallback** to the next model in `agents.defaults.model.fallbacks`.

This doc explains the runtime rules and the data that backs them.

## [​](#auth-storage-keys-+-oauth)Auth storage (keys + OAuth)

OpenClaw uses **auth profiles** for both API keys and OAuth tokens.

- Secrets live in `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` (legacy: `~/.openclaw/agent/auth-profiles.json`).

- Config `auth.profiles` / `auth.order` are **metadata + routing only** (no secrets).

- Legacy import-only OAuth file: `~/.openclaw/credentials/oauth.json` (imported into `auth-profiles.json` on first use).

More detail: [/concepts/oauth](/concepts/oauth)

Credential types:

- `type: "api_key"` → `{ provider, key }`

- `type: "oauth"` → `{ provider, access, refresh, expires, email? }` (+ `projectId`/`enterpriseUrl` for some providers)

## [​](#profile-ids)Profile IDs

OAuth logins create distinct profiles so multiple accounts can coexist.

- Default: `provider:default` when no email is available.

- OAuth with email: `provider:<email>` (for example `google-antigravity:[[email protected]](/cdn-cgi/l/email-protection)`).

Profiles live in `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` under `profiles`.

## [​](#rotation-order)Rotation order

When a provider has multiple profiles, OpenClaw chooses an order like this:

- **Explicit config**: `auth.order[provider]` (if set).

- **Configured profiles**: `auth.profiles` filtered by provider.

- **Stored profiles**: entries in `auth-profiles.json` for the provider.

If no explicit order is configured, OpenClaw uses a round‑robin order:

- **Primary key:** profile type (**OAuth before API keys**).

- **Secondary key:** `usageStats.lastUsed` (oldest first, within each type).

- **Cooldown/disabled profiles** are moved to the end, ordered by soonest expiry.

### [​](#session-stickiness-cache-friendly)Session stickiness (cache-friendly)

OpenClaw **pins the chosen auth profile per session** to keep provider caches warm.

It does **not** rotate on every request. The pinned profile is reused until:

- the session is reset (`/new` / `/reset`)

- a compaction completes (compaction count increments)

- the profile is in cooldown/disabled

Manual selection via `/model …@<profileId>` sets a **user override** for that session

and is not auto‑rotated until a new session starts.

Auto‑pinned profiles (selected by the session router) are treated as a **preference**:

they are tried first, but OpenClaw may rotate to another profile on rate limits/timeouts.

User‑pinned profiles stay locked to that profile; if it fails and model fallbacks

are configured, OpenClaw moves to the next model instead of switching profiles.

### [​](#why-oauth-can-“look-lost”)Why OAuth can “look lost”

If you have both an OAuth profile and an API key profile for the same provider, round‑robin can switch between them across messages unless pinned. To force a single profile:

- Pin with `auth.order[provider] = ["provider:profileId"]`, or

- Use a per-session override via `/model …` with a profile override (when supported by your UI/chat surface).

## [​](#cooldowns)Cooldowns

When a profile fails due to auth/rate‑limit errors (or a timeout that looks

like rate limiting), OpenClaw marks it in cooldown and moves to the next profile.

Format/invalid‑request errors (for example Cloud Code Assist tool call ID

validation failures) are treated as failover‑worthy and use the same cooldowns.

Cooldowns use exponential backoff:

- 1 minute

- 5 minutes

- 25 minutes

- 1 hour (cap)

State is stored in `auth-profiles.json` under `usageStats`:

Copy```

{

"usageStats": {

"provider:profile": {

"lastUsed": 1736160000000,

"cooldownUntil": 1736160600000,

"errorCount": 2

}

}

}

```

## [​](#billing-disables)Billing disables

Billing/credit failures (for example “insufficient credits” / “credit balance too low”) are treated as failover‑worthy, but they’re usually not transient. Instead of a short cooldown, OpenClaw marks the profile as **disabled** (with a longer backoff) and rotates to the next profile/provider.

State is stored in `auth-profiles.json`:

Copy```

{

"usageStats": {

"provider:profile": {

"disabledUntil": 1736178000000,

"disabledReason": "billing"

}

}

}

```

Defaults:

- Billing backoff starts at **5 hours**, doubles per billing failure, and caps at **24 hours**.

- Backoff counters reset if the profile hasn’t failed for **24 hours** (configurable).

## [​](#model-fallback)Model fallback

If all profiles for a provider fail, OpenClaw moves to the next model in

`agents.defaults.model.fallbacks`. This applies to auth failures, rate limits, and

timeouts that exhausted profile rotation (other errors do not advance fallback).

When a run starts with a model override (hooks or CLI), fallbacks still end at

`agents.defaults.model.primary` after trying any configured fallbacks.

## [​](#related-config)Related config

See [Gateway configuration](/gateway/configuration) for:

- `auth.profiles` / `auth.order`

- `auth.cooldowns.billingBackoffHours` / `auth.cooldowns.billingBackoffHoursByProvider`

- `auth.cooldowns.billingMaxHours` / `auth.cooldowns.failureWindowHours`

- `agents.defaults.model.primary` / `agents.defaults.model.fallbacks`

- `agents.defaults.imageModel` routing

See [Models](/concepts/models) for the broader model selection and fallback overview.[Model Providers](/concepts/model-providers)[Anthropic](/providers/anthropic)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)