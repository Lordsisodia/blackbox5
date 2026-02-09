---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/reference/test",
    "fetched_at": "2026-02-07T10:22:02.205730",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 500484
  },
  "metadata": {
    "title": "Tests",
    "section": "test",
    "tier": 3,
    "type": "reference"
  }
}
---

- Tests - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationRelease notesTests[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [Tests](#tests)- [Model latency bench (local keys)](#model-latency-bench-local-keys)- [Onboarding E2E (Docker)](#onboarding-e2e-docker)- [QR import smoke (Docker)](#qr-import-smoke-docker)Release notes# Tests# [​](#tests)Tests

-

Full testing kit (suites, live, Docker): [Testing](/testing)

-

`pnpm test:force`: Kills any lingering gateway process holding the default control port, then runs the full Vitest suite with an isolated gateway port so server tests don’t collide with a running instance. Use this when a prior gateway run left port 18789 occupied.

-

`pnpm test:coverage`: Runs Vitest with V8 coverage. Global thresholds are 70% lines/branches/functions/statements. Coverage excludes integration-heavy entrypoints (CLI wiring, gateway/telegram bridges, webchat static server) to keep the target focused on unit-testable logic.

-

`pnpm test:e2e`: Runs gateway end-to-end smoke tests (multi-instance WS/HTTP/node pairing).

-

`pnpm test:live`: Runs provider live tests (minimax/zai). Requires API keys and `LIVE=1` (or provider-specific `*_LIVE_TEST=1`) to unskip.

## [​](#model-latency-bench-local-keys)Model latency bench (local keys)

Script: [`scripts/bench-model.ts`](https://github.com/openclaw/openclaw/blob/main/scripts/bench-model.ts)

Usage:

- `source ~/.profile && pnpm tsx scripts/bench-model.ts --runs 10`

- Optional env: `MINIMAX_API_KEY`, `MINIMAX_BASE_URL`, `MINIMAX_MODEL`, `ANTHROPIC_API_KEY`

- Default prompt: “Reply with a single word: ok. No punctuation or extra text.”

Last run (2025-12-31, 20 runs):

- minimax median 1279ms (min 1114, max 2431)

- opus median 2454ms (min 1224, max 3170)

## [​](#onboarding-e2e-docker)Onboarding E2E (Docker)

Docker is optional; this is only needed for containerized onboarding smoke tests.

Full cold-start flow in a clean Linux container:

Copy```

scripts/e2e/onboard-docker.sh

```

This script drives the interactive wizard via a pseudo-tty, verifies config/workspace/session files, then starts the gateway and runs `openclaw health`.

## [​](#qr-import-smoke-docker)QR import smoke (Docker)

Ensures `qrcode-terminal` loads under Node 22+ in Docker:

Copy```

pnpm test:docker:qr

```[RELEASING](/reference/RELEASING)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)