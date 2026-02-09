---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/oauth",
    "fetched_at": "2026-02-07T10:16:20.442338",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 538961
  },
  "metadata": {
    "title": "OAuth",
    "section": "oauth",
    "tier": 3,
    "type": "reference"
  }
}
---

- OAuth - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationFundamentalsOAuth[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Fundamentals- [Gateway Architecture](/concepts/architecture)- [Agent Runtime](/concepts/agent)- [Agent Loop](/concepts/agent-loop)- [System Prompt](/concepts/system-prompt)- [Context](/concepts/context)- [Agent Workspace](/concepts/agent-workspace)- [Bootstrapping](/start/bootstrapping)- [OAuth](/concepts/oauth)Sessions and memory- [Session Management](/concepts/session)- [Sessions](/concepts/sessions)- [Session pruning](/concepts/session-pruning)- [Session Tools](/concepts/session-tool)- [Memory](/concepts/memory)- [Compaction](/concepts/compaction)Multi-agent- [Multi-Agent Routing](/concepts/multi-agent)- [Presence](/concepts/presence)Messages and delivery- [Messages](/concepts/messages)- [Streaming and Chunking](/concepts/streaming)- [Retry Policy](/concepts/retry)- [Command Queue](/concepts/queue)On this page- [OAuth](#oauth)- [The token sink (why it exists)](#the-token-sink-why-it-exists)- [Storage (where tokens live)](#storage-where-tokens-live)- [Anthropic setup-token (subscription auth)](#anthropic-setup-token-subscription-auth)- [OAuth exchange (how login works)](#oauth-exchange-how-login-works)- [Anthropic (Claude Pro/Max) setup-token](#anthropic-claude-pro%2Fmax-setup-token)- [OpenAI Codex (ChatGPT OAuth)](#openai-codex-chatgpt-oauth)- [Refresh + expiry](#refresh-%2B-expiry)- [Multiple accounts (profiles) + routing](#multiple-accounts-profiles-%2B-routing)- [1) Preferred: separate agents](#1-preferred-separate-agents)- [2) Advanced: multiple profiles in one agent](#2-advanced-multiple-profiles-in-one-agent)Fundamentals# OAuth# [​](#oauth)OAuth

OpenClaw supports “subscription auth” via OAuth for providers that offer it (notably **OpenAI Codex (ChatGPT OAuth)**). For Anthropic subscriptions, use the **setup-token** flow. This page explains:

- how the OAuth **token exchange** works (PKCE)

- where tokens are **stored** (and why)

- how to handle **multiple accounts** (profiles + per-session overrides)

OpenClaw also supports **provider plugins** that ship their own OAuth or API‑key

flows. Run them via:

Copy```

openclaw models auth login --provider <id>

```

## [​](#the-token-sink-why-it-exists)The token sink (why it exists)

OAuth providers commonly mint a **new refresh token** during login/refresh flows. Some providers (or OAuth clients) can invalidate older refresh tokens when a new one is issued for the same user/app.

Practical symptom:

- you log in via OpenClaw *and* via Claude Code / Codex CLI → one of them randomly gets “logged out” later

To reduce that, OpenClaw treats `auth-profiles.json` as a **token sink**:

- the runtime reads credentials from **one place**

- we can keep multiple profiles and route them deterministically

## [​](#storage-where-tokens-live)Storage (where tokens live)

Secrets are stored **per-agent**:

- Auth profiles (OAuth + API keys): `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`

- Runtime cache (managed automatically; don’t edit): `~/.openclaw/agents/<agentId>/agent/auth.json`

Legacy import-only file (still supported, but not the main store):

- `~/.openclaw/credentials/oauth.json` (imported into `auth-profiles.json` on first use)

All of the above also respect `$OPENCLAW_STATE_DIR` (state dir override). Full reference: [/gateway/configuration](/gateway/configuration#auth-storage-oauth--api-keys)

## [​](#anthropic-setup-token-subscription-auth)Anthropic setup-token (subscription auth)

Run `claude setup-token` on any machine, then paste it into OpenClaw:

Copy```

openclaw models auth setup-token --provider anthropic

```

If you generated the token elsewhere, paste it manually:

Copy```

openclaw models auth paste-token --provider anthropic

```

Verify:

Copy```

openclaw models status

```

## [​](#oauth-exchange-how-login-works)OAuth exchange (how login works)

OpenClaw’s interactive login flows are implemented in `@mariozechner/pi-ai` and wired into the wizards/commands.

### [​](#anthropic-claude-pro/max-setup-token)Anthropic (Claude Pro/Max) setup-token

Flow shape:

- run `claude setup-token`

- paste the token into OpenClaw

- store as a token auth profile (no refresh)

The wizard path is `openclaw onboard` → auth choice `setup-token` (Anthropic).

### [​](#openai-codex-chatgpt-oauth)OpenAI Codex (ChatGPT OAuth)

Flow shape (PKCE):

- generate PKCE verifier/challenge + random `state`

- open `https://auth.openai.com/oauth/authorize?...`

- try to capture callback on `http://127.0.0.1:1455/auth/callback`

- if callback can’t bind (or you’re remote/headless), paste the redirect URL/code

- exchange at `https://auth.openai.com/oauth/token`

- extract `accountId` from the access token and store `{ access, refresh, expires, accountId }`

Wizard path is `openclaw onboard` → auth choice `openai-codex`.

## [​](#refresh-+-expiry)Refresh + expiry

Profiles store an `expires` timestamp.

At runtime:

- if `expires` is in the future → use the stored access token

- if expired → refresh (under a file lock) and overwrite the stored credentials

The refresh flow is automatic; you generally don’t need to manage tokens manually.

## [​](#multiple-accounts-profiles-+-routing)Multiple accounts (profiles) + routing

Two patterns:

### [​](#1-preferred-separate-agents)1) Preferred: separate agents

If you want “personal” and “work” to never interact, use isolated agents (separate sessions + credentials + workspace):

Copy```

openclaw agents add work

openclaw agents add personal

```

Then configure auth per-agent (wizard) and route chats to the right agent.

### [​](#2-advanced-multiple-profiles-in-one-agent)2) Advanced: multiple profiles in one agent

`auth-profiles.json` supports multiple profile IDs for the same provider.

Pick which profile is used:

- globally via config ordering (`auth.order`)

- per-session via `/model ...@<profileId>`

Example (session override):

- `/model Opus@anthropic:work`

How to see what profile IDs exist:

- `openclaw channels list --json` (shows `auth[]`)

Related docs:

- [/concepts/model-failover](/concepts/model-failover) (rotation + cooldown rules)

- [/tools/slash-commands](/tools/slash-commands) (command surface)

[Bootstrapping](/start/bootstrapping)[Session Management](/concepts/session)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)