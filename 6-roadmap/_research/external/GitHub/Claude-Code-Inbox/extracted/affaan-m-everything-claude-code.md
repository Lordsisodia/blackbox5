---
repo:
  owner: affaan-m
  name: everything-claude-code
  url: https://github.com/affaan-m/everything-claude-code
  description: "Production-ready agents, skills, hooks, commands, rules, and MCP configurations"
  captured_at: 2026-02-03T23:30:00Z

type: awesome-list
category: configuration-collection
priority: high

classification:
  areas: [claude-code, configuration, agents, skills]
  topics: [hooks, mcp, slash-commands, rules, continuous-learning]
---

# everything-claude-code

**Author**: Anthropic hackathon winner
**Description**: Comprehensive configuration collection for Claude Code CLI

## What's Inside

| Component | Count | Description |
|-----------|-------|-------------|
| **Agents** | 15+ | Planning, architecture, code review, security, TDD, E2E testing, refactoring, Go dev |
| **Skills** | 30+ | Coding standards, backend/frontend patterns, continuous learning, verification |
| **Commands** | 20+ | `/plan`, `/tdd`, `/code-review`, `/build-fix`, Go tools |
| **Rules** | - | Security, coding style, testing, git workflow |
| **Hooks** | - | Memory persistence, strategic compaction |
| **MCP Configs** | - | GitHub, Supabase, Vercel, Railway |

## Key Features

- **"Continuous Learning v2"**: Instinct-based learning system
- **Cross-platform**: Windows, macOS, Linux via Node.js
- **Package manager detection**: npm, pnpm, yarn, bun
- **Skill Creator**: Generates skills from git history

## Installation

```bash
/plugin marketplace add affaan-m/everything-claude-code
/plugin install everything-claude-code@everything-claude-code
```

## Requirements

- Claude Code CLI v2.1.0+
- Node.js

## Notes

- Rules must be manually copied to `~/.claude/rules/`
- Evolved over 10+ months of intensive daily use
