---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/start/bootstrapping",
    "fetched_at": "2026-02-07T10:22:34.541166",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 469475
  },
  "metadata": {
    "title": "Agent Bootstrapping",
    "section": "bootstrapping",
    "tier": 3,
    "type": "reference"
  }
}
---

- Agent Bootstrapping - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationFundamentalsAgent Bootstrapping[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Fundamentals- [Gateway Architecture](/concepts/architecture)- [Agent Runtime](/concepts/agent)- [Agent Loop](/concepts/agent-loop)- [System Prompt](/concepts/system-prompt)- [Context](/concepts/context)- [Agent Workspace](/concepts/agent-workspace)- [Bootstrapping](/start/bootstrapping)- [OAuth](/concepts/oauth)Sessions and memory- [Session Management](/concepts/session)- [Sessions](/concepts/sessions)- [Session pruning](/concepts/session-pruning)- [Session Tools](/concepts/session-tool)- [Memory](/concepts/memory)- [Compaction](/concepts/compaction)Multi-agent- [Multi-Agent Routing](/concepts/multi-agent)- [Presence](/concepts/presence)Messages and delivery- [Messages](/concepts/messages)- [Streaming and Chunking](/concepts/streaming)- [Retry Policy](/concepts/retry)- [Command Queue](/concepts/queue)On this page- [Agent Bootstrapping](#agent-bootstrapping)- [What bootstrapping does](#what-bootstrapping-does)- [Where it runs](#where-it-runs)- [Related docs](#related-docs)Fundamentals# Agent Bootstrapping# [​](#agent-bootstrapping)Agent Bootstrapping

Bootstrapping is the **first‑run** ritual that prepares an agent workspace and

collects identity details. It happens after onboarding, when the agent starts

for the first time.

## [​](#what-bootstrapping-does)What bootstrapping does

On the first agent run, OpenClaw bootstraps the workspace (default

`~/.openclaw/workspace`):

- Seeds `AGENTS.md`, `BOOTSTRAP.md`, `IDENTITY.md`, `USER.md`.

- Runs a short Q&A ritual (one question at a time).

- Writes identity + preferences to `IDENTITY.md`, `USER.md`, `SOUL.md`.

- Removes `BOOTSTRAP.md` when finished so it only runs once.

## [​](#where-it-runs)Where it runs

Bootstrapping always runs on the **gateway host**. If the macOS app connects to

a remote Gateway, the workspace and bootstrapping files live on that remote

machine.

When the Gateway runs on another machine, edit workspace files on the gateway

host (for example, `user@gateway-host:~/.openclaw/workspace`).

## [​](#related-docs)Related docs

- macOS app onboarding: [Onboarding](/start/onboarding)

- Workspace layout: [Agent workspace](/concepts/agent-workspace)

[Agent Workspace](/concepts/agent-workspace)[OAuth](/concepts/oauth)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)