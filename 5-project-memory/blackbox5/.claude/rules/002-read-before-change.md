---
name: Read Before Change
trigger:
  - file modification
  - code change
  - edit
alwaysApply: true
priority: 100
---

# Read Before Change

## Rule
NEVER propose changes to code you haven't read. Read ALL target files completely before making any modifications.

## Why
- Prevents breaking changes
- Ensures integration
- Avoids assumptions
- Maintains code quality

## Process
1. Use Read tool to examine files
2. Understand existing code
3. Then propose changes

## Source
- LEGACY.md line 11
- CLAUDE.md core principles
- Executor prompts v4
