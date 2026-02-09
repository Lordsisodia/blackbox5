# Memory

> Project memory and knowledge storage

## Overview

This directory contains the project's accumulated knowledge, insights, and historical context. It serves as the long-term memory for the BlackBox5 system.

## Directory Structure

```
memory/
├── insights/      # Key insights and learnings
├── decisions/     # Decision history
├── context/       # Context snapshots
├── patterns/      # Identified patterns
└── archive/       # Old memory (compressed)
```

## Memory Types

### Insights
Key learnings extracted from completed work:
- What worked well
- What didn't work
- Unexpected discoveries
- Efficiency gains

### Decisions
Record of important decisions:
- Decision context
- Options considered
- Chosen approach
- Rationale

### Context
Preserved context from sessions:
- Session summaries
- Key discussions
- Important state

## Memory Format

```markdown
# Memory Entry

**Type**: insight | decision | context
**Created**: YYYY-MM-DD
**Source**: Task ID or session
**Tags**: tag1, tag2

## Content

Detailed memory content here.

## Related

- Link to related memories
- Link to source tasks
```

## Related Documentation

- [../tasks/README.md](../tasks/README.md) - Tasks that generate memory
- [../../1-docs/01-theory/02-concepts/knowledge-accumulation.md](../../1-docs/01-theory/02-concepts/knowledge-accumulation.md) - Theory

## Usage

Memory is automatically captured during task execution. Review periodically for patterns.
