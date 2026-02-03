---
repo:
  owner: disler
  name: claude-code-hooks-multi-agent-observability
  url: https://github.com/disler/claude-code-hooks-multi-agent-observability
  description: "Real-time monitoring for Claude Code agents through hook event tracking"
  captured_at: 2026-02-03T23:30:00Z

type: observability
category: monitoring-system
priority: high

classification:
  areas: [claude-code, observability, monitoring, hooks]
  topics: [real-time, multi-agent, dashboard, sqlite, websockets]
---

# claude-code-hooks-multi-agent-observability

## Description

Real-time monitoring for Claude Code agents through simple hook event tracking.

## Architecture

```
Claude Agents → Hook Scripts → HTTP POST → Bun Server → SQLite → WebSocket → Vue Client
```

## Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Server** | Bun, TypeScript, SQLite | HTTP/WebSocket, database |
| **Client** | Vue 3, TypeScript, Vite | Real-time dashboard |
| **Hooks** | Python with Astral uv | Event capture |

## Event Types Tracked

- PreToolUse (🔧)
- PostToolUse (✅)
- Notification (🔔)
- Stop (🛑)
- SubagentStop (👥)
- PreCompact (📦)
- UserPromptSubmit (💬)
- SessionStart (🚀)
- SessionEnd (🏁)

## Contents

- `.claude/hooks/` - Python hook scripts
- `apps/server/` - Bun TypeScript server
- `apps/client/` - Vue 3 frontend with live charts
- `scripts/` - start-system.sh, reset-system.sh, test-system.sh
- Docs: AGENTS.md, CLAUDE.md, GEMINI.md

## Requirements

- Claude Code CLI
- Astral uv
- Bun/npm/yarn
- Anthropic API key
