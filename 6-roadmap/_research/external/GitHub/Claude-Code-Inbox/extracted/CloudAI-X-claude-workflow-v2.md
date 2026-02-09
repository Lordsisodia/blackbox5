---
repo:
  owner: CloudAI-X
  name: claude-workflow-v2
  url: https://github.com/CloudAI-X/claude-workflow-v2
  stars: 1200
  forks: 182
  description: "Universal Claude Code workflow plugin with specialized agents, skills, hooks"
  captured_at: 2026-02-03T23:30:00Z

type: plugin
category: workflow-framework
priority: high

classification:
  areas: [claude-code, workflow, agents, skills]
  topics: [plugin, slash-commands, git-workflow, verification]
---

# claude-workflow-v2 (project-starter)

**Stars**: 1.2k | **Forks**: 182

## Description

Universal Claude Code workflow plugin for any software project.

## Components

| Component | Count | Purpose |
|-----------|-------|---------|
| **Agents** | 7 | Orchestrator, code-reviewer, debugger, docs-writer, security-auditor, refactorer, test-architect |
| **Commands** | 17 | Slash commands for workflows |
| **Skills** | 10 | Knowledge domains |
| **Hooks** | 9 | Automation scripts |

## Key Features

- **Output styles**: `/project-starter:architect`, `:rapid`, `:mentor`, `:review`
- **Git workflows**: Auto-commit, commit-push-pr, quick-fix, lint-fix, sync-branch
- **Verification**: Multi-agent verification, build validation, security scanning
- **Auto-agents**: Spawn based on context
- **MCP servers**: External integrations

## Installation

```bash
# CLI (per-session)
claude --plugin-dir ./claude-workflow

# Permanent
claude plugin install project-starter

# Agent SDK
# Import via @anthropic-ai/claude-agent-sdk
```

## Includes

- `CLAUDE.md` templates
- Permissions settings
- MCP server configuration
- GitHub Action for PR integration

## License

MIT
