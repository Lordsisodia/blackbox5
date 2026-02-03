---
repo:
  owner: disler
  name: claude-code-hooks-mastery
  url: https://github.com/disler/claude-code-hooks-mastery
  stars: 2200
  forks: 482
  description: "Master Claude Code Hooks"
  captured_at: 2026-02-03T23:30:00Z

type: educational
category: hooks-reference
priority: critical

classification:
  areas: [claude-code, hooks, education]
  topics: [hooks, lifecycle, uv, tts, validation, status-lines]
---

# claude-code-hooks-mastery

**Stars**: 2.2k | **Forks**: 482

## Description

Complete implementations of all 13 Claude Code hook lifecycle events.

## Core Hook Implementations

Located in `.claude/hooks/`:

- `user_prompt_submit.py` - Prompt validation, logging, context injection
- `pre_tool_use.py` - Security blocking for dangerous commands
- `post_tool_use.py` - Logging and transcript conversion
- `session_start.py`, `session_end.py` - Session lifecycle
- `stop.py`, `subagent_stop.py` - Completion handling with TTS
- Plus 7 more hook types

## Architecture Features

- **UV single-file scripts** - Isolation and portability
- **TTS system** - ElevenLabs > OpenAI > pyttsx3 priority
- **Team-based validation** - Builder/Validator patterns
- **9 status line versions** - Progressive terminal UI

## Contents

- `ai_docs/` - Anthropic documentation
- `logs/` - JSON hook execution logs
- Custom slash commands
- Sub-agent configurations
- Output templates (HTML, YAML, markdown)

## Prerequisites

- Astral UV
- Claude Code
