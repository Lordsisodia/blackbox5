---
repo:
  owner: nizos
  name: tdd-guard
  url: https://github.com/nizos/tdd-guard
  description: "Automated Test-Driven Development enforcement for Claude Code"
  captured_at: 2026-02-03T23:30:00Z

type: tool
category: tdd-enforcement
priority: high

classification:
  areas: [claude-code, testing, tdd]
  topics: [tdd, testing, enforcement, multi-language]
---

# TDD Guard

## Description

Automated Test-Driven Development enforcement for Claude Code.

## Features

- **Test-First Enforcement** - Blocks implementation without failing tests
- **Minimal Implementation** - Prevents code beyond test requirements
- **Lint Integration** - Enforces refactoring via linting
- **Multi-Language** - TypeScript, JavaScript, Python, PHP, Go, Rust, Storybook
- **Customizable Rules** - Adjust to your TDD style
- **Session Control** - Toggle on/off mid-session

## Structure

- `/src` - Source code
- `/test` - Test files
- `/docs` - Documentation
- `/reporters` - Language/framework specific reporters

## Installation

```bash
npm install -g tdd-guard
# or
brew install tdd-guard
```

## Requirements

- Node.js 22+
- Claude Code or Anthropic API key
- Test framework (Jest, Vitest, pytest, etc.)

## License

MIT
