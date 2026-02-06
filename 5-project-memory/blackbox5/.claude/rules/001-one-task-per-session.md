---
name: One Task Per Session
trigger:
  - task execution
  - session start
alwaysApply: true
priority: 100
---

# One Task Per Session

## Rule
Each session completes exactly ONE task. No batching. No multitasking.

## Rationale
- Prevents context overflow
- Ensures quality completion
- Maintains focus
- Simplifies debugging

## Exceptions
Spawning sub-agents for research/context gathering is allowed.

## Source
- LEGACY.md line 10
- RALF executor prompts
- CLAUDE.md workflow rules
