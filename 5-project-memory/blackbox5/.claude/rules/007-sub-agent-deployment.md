---
name: Sub-Agent Deployment Rules
trigger:
  - codebase exploration
  - complex search
  - validation
  - cross-project
alwaysApply: true
priority: 90
---

# Sub-Agent Deployment Rules

## ALWAYS Spawn Sub-Agents When

- Searching across >15 files
- Complex pattern matching needed (regex, multiline searches)
- Cross-project exploration (>2 projects involved)
- Estimated search time >5 minutes
- Open-ended codebase exploration (finding files, patterns)
- Validation of complex work (reviewing your work)

## USE DIRECT READS When

- <15 files needed
- Files at known paths
- Simple pattern matching (single grep)
- Known directory structure
- Implementation work (do it yourself)

## Best Practices

- Use sub-agents to gather context (don't waste your context window)
- Scan projects first, then folders
- Cache context for reuse
- Return only synthesized, high-value insights

## Source
- CLAUDE.md Sub-Agent Rules
- Executor prompts
- RALF documentation
