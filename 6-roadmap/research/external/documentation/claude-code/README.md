---
source:
  name: "Claude Code Documentation"
  url: "https://code.claude.com/docs"
  type: official-docs
  category: ai-tools
  status: active
  last_synced: "2026-02-03T23:50:00Z"
  version: null

structure:
  sections:
    - name: Getting Started
      path: extracted/by-section/getting-started/
      key_files:
        - overview.md
        - quickstart.md
        - setup.md

    - name: Core Concepts
      path: extracted/by-section/core-concepts/
      key_files:
        - settings.md
        - permissions.md
        - mcp.md
        - sub-agents.md
        - skills.md

    - name: Workflows
      path: extracted/by-section/workflows/
      key_files:
        - common-workflows.md
        - best-practices.md

    - name: Reference
      path: extracted/by-section/reference/
      key_files:
        - cli-reference.md
        - interactive-mode.md
        - headless.md

agent_access:
  quick_ref: extracted/quick-reference.md
  search_index: extracted/search-index.json
  code_examples: extracted/snippets/
---

# Claude Code Documentation

Official documentation for Claude Code, Anthropic's agentic coding tool.

## Overview

Claude Code is an agentic coding tool that lives in your terminal and helps you turn ideas into code faster than ever before.

## Status

- **Last synced**: 2026-02-03
- **Pages fetched**: 6 of ~44
- **Completeness**: 15%

## Quick Access

| What | Where |
|------|-------|
| Raw fetched pages | `raw/pages/` |
| Processed summaries | `extracted/by-section/` |
| Key facts | `extracted/quick-reference.md` |
| Code snippets | `extracted/snippets/` |
| Sync history | `timeline/` |

## Fetched Pages

1. **overview.md** - Introduction and getting started
2. **cli-reference.md** - Complete CLI reference
3. **settings.md** - Configuration options
4. **permissions.md** - Permission system
5. **mcp.md** - Model Context Protocol
6. **common-workflows.md** - Practical workflows

## Pending Pages (Tier 2 & 3)

- quickstart, setup, troubleshooting
- sub-agents, skills, hooks, plugins
- security, data-usage, sandboxing
- VS Code, JetBrains, Desktop, Chrome extensions
- GitHub Actions, GitLab CI/CD, Slack integration
- Amazon Bedrock, Google Vertex, Azure Foundry

## For Agents

Use `extracted/quick-reference.md` for fast lookups.
Dive into `raw/pages/{topic}.md` for full content.

## Key Documentation Index

The docs mention: https://code.claude.com/docs/llms.txt
