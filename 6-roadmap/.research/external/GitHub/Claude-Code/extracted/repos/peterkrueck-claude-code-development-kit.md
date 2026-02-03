---
repo:
  owner: peterkrueck
  name: Claude-Code-Development-Kit
  url: https://github.com/peterkrueck/Claude-Code-Development-Kit
  description: "Handle context at scale - custom Claude Code workflow including hooks, mcp and sub agents"
  captured_at: 2026-02-03T23:30:00Z

type: toolkit
category: development-kit
priority: medium

classification:
  areas: [claude-code, context-management, mcp, agents]
  topics: [documentation, multi-tier-context, gemini, context7]
---

# Claude-Code-Development-Kit

## Description

Handle context at scale - custom Claude Code workflow including hooks, MCP and sub agents.

## Key Components

| Component | Purpose |
|-----------|---------|
| **3-tier documentation** | Auto-loads context at foundation, component, feature levels |
| **Custom commands** | Orchestrates specialized sub-agents |
| **MCP servers** | Context7 (library docs), Gemini (architecture consultation) |
| **Hooks** | Security scanning, context injection, notifications |

## Structure

- `commands/` - AI orchestration templates
- `docs/` - Documentation templates and examples
- `hooks/` - Automation scripts
- `install.sh` / `setup.sh` - Installation

## Key Commands

- `/full-context`
- `/code-review`
- `/update-docs`
- `/create-docs`

## Requirements

- Claude Code (required)
- Context7 and Gemini Assistant MCP servers (recommended)
- Windows not supported
