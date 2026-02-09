---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/scripts",
    "fetched_at": "2026-02-07T10:22:33.934685",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 462112
  },
  "metadata": {
    "title": "Scripts",
    "section": "scripts",
    "tier": 3,
    "type": "reference"
  }
}
---

- Scripts - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationEnvironment and debuggingScripts[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Help- [Help](/help)- [Troubleshooting](/help/troubleshooting)- [FAQ](/help/faq)Community- [OpenClaw Lore](/start/lore)Environment and debugging- [Node.js](/install/node)- [Environment Variables](/environment)- [Debugging](/debugging)- [Testing](/testing)- [Scripts](/scripts)- [Session Management Deep Dive](/reference/session-management-compaction)Developer workflows- [Setup](/start/setup)- [Submitting a PR](/help/submitting-a-pr)- [Submitting an Issue](/help/submitting-an-issue)Docs meta- [Docs Hubs](/start/hubs)- [Docs directory](/start/docs-directory)On this page- [Scripts](#scripts)- [Conventions](#conventions)- [Auth monitoring scripts](#auth-monitoring-scripts)- [When adding scripts](#when-adding-scripts)Environment and debugging# Scripts# [​](#scripts)Scripts

The `scripts/` directory contains helper scripts for local workflows and ops tasks.

Use these when a task is clearly tied to a script; otherwise prefer the CLI.

## [​](#conventions)Conventions

- Scripts are **optional** unless referenced in docs or release checklists.

- Prefer CLI surfaces when they exist (example: auth monitoring uses `openclaw models status --check`).

- Assume scripts are host‑specific; read them before running on a new machine.

## [​](#auth-monitoring-scripts)Auth monitoring scripts

Auth monitoring scripts are documented here:

[/automation/auth-monitoring](/automation/auth-monitoring)

## [​](#when-adding-scripts)When adding scripts

- Keep scripts focused and documented.

- Add a short entry in the relevant doc (or create one if missing).

[Testing](/testing)[Session Management Deep Dive](/reference/session-management-compaction)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)