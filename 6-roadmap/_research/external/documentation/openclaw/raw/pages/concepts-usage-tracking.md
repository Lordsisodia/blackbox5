---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/concepts/usage-tracking",
    "fetched_at": "2026-02-07T10:17:01.030716",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 488685
  },
  "metadata": {
    "title": "Usage Tracking",
    "section": "usage-tracking",
    "tier": 3,
    "type": "reference"
  }
}
---

- Usage Tracking - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationTechnical referenceUsage Tracking[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [Usage tracking](#usage-tracking)- [What it is](#what-it-is)- [Where it shows up](#where-it-shows-up)- [Providers + credentials](#providers-%2B-credentials)Technical reference# Usage Tracking# [​](#usage-tracking)Usage tracking

## [​](#what-it-is)What it is

- Pulls provider usage/quota directly from their usage endpoints.

- No estimated costs; only the provider-reported windows.

## [​](#where-it-shows-up)Where it shows up

- `/status` in chats: emoji‑rich status card with session tokens + estimated cost (API key only). Provider usage shows for the **current model provider** when available.

- `/usage off|tokens|full` in chats: per-response usage footer (OAuth shows tokens only).

- `/usage cost` in chats: local cost summary aggregated from OpenClaw session logs.

- CLI: `openclaw status --usage` prints a full per-provider breakdown.

- CLI: `openclaw channels list` prints the same usage snapshot alongside provider config (use `--no-usage` to skip).

- macOS menu bar: “Usage” section under Context (only if available).

## [​](#providers-+-credentials)Providers + credentials

- **Anthropic (Claude)**: OAuth tokens in auth profiles.

- **GitHub Copilot**: OAuth tokens in auth profiles.

- **Gemini CLI**: OAuth tokens in auth profiles.

- **Antigravity**: OAuth tokens in auth profiles.

- **OpenAI Codex**: OAuth tokens in auth profiles (accountId used when present).

- **MiniMax**: API key (coding plan key; `MINIMAX_CODE_PLAN_KEY` or `MINIMAX_API_KEY`); uses the 5‑hour coding plan window.

- **z.ai**: API key via env/config/auth store.

Usage is hidden if no matching OAuth/API credentials exist.[Typing Indicators](/concepts/typing-indicators)[Timezones](/concepts/timezone)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)