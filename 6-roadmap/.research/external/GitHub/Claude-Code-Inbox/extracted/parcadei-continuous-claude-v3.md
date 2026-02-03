---
repo:
  owner: parcadei
  name: Continuous-Claude-v3
  url: https://github.com/parcadei/Continuous-Claude-v3
  description: "Context management with ledgers and handoffs - MCP execution without context pollution"
  captured_at: 2026-02-03T23:30:00Z

type: framework
category: context-management
priority: critical

classification:
  areas: [claude-code, context-management, agents, memory]
  topics: [continuity, handoffs, skills, tldr-analysis, multi-agent]
---

# Continuous-Claude-v3

## Philosophy

**"Compound, don't compact."**

Automatically extracts learnings so you can start fresh with full context.

## Key Features

| Feature | Count | Description |
|---------|-------|-------------|
| **Skills** | 109 | Natural language triggered capabilities |
| **Agents** | 32 | Specialized sub-sessions (scout, oracle, debug-agent) |
| **Hooks** | 30 | System reminders, context injection |
| **TLDR Analysis** | 5-layer | AST → CallGraph → CFG → DFG → Slicing (95% token savings) |
| **Memory** | PostgreSQL+pgvector | Daemon auto-extraction |
| **Continuity** | YAML handoffs | Token-efficient session transfer |

## Architecture

```
Skills → Agents → Hooks → TLDR Analysis
                ↓
        Memory / Continuity Ledgers / Coordination
```

## Workflows

| Command | Flow |
|---------|------|
| `/fix` | sleuth → premortem → kraken → test → commit |
| `/build` | discovery → plan → validate → implement → commit |
| `/tdd` | plan → arbiter (tests) → kraken (implement) → arbiter |

## Requirements

- Python 3.11+
- uv package manager
- Docker
- Claude Code CLI

## License

MIT
