# Agent Guide to Blackbox5

> Quick reference for AI agents working with the Blackbox5 system

---

## Start Here

**First file to read:** `SYSTEM-MAP.yaml` — Machine-readable system structure

**For project status:** `5-project-memory/siso-internal/STATE.yaml`

**For feature lookup:** `CATALOG.md` — 200+ features indexed

---

## Directory Quick Reference

| If you need... | Go to... |
|----------------|----------|
| Agent implementations | `2-engine/02-agents/` |
| Tools (106+) | `2-engine/05-tools/` |
| Memory systems | `2-engine/03-knowledge/storage/` |
| External integrations | `2-engine/06-integrations/` |
| Autonomous system (NEW) | `2-engine/08-autonomous-system/` |
| GUI/Vibe Kanban | `3-gui/vibe-kanban/` |
| GUI integrations | `3-gui/integrations/` |
| Project state | `5-project-memory/siso-internal/` |
| Roadmap/plans | `6-roadmap/` |
| Decision records | `1-docs/decisions/` |

---

## Project Memory Structure

Each project in `5-project-memory/` follows this pattern:

```
project-name/
├── decisions/          # Why we made choices
│   ├── architectural/
│   ├── scope/
│   └── technical/
├── knowledge/          # How things work
│   ├── architecture/
│   ├── patterns/
│   └── learnings/
├── operations/         # System operations
├── plans/              # What we're building
│   ├── prds/
│   └── active/
├── project/            # Project identity
├── tasks/              # What we're working on
│   ├── active/
│   └── completed/
└── STATE.yaml          # Single source of truth
```

---

## Key State Files

These YAML files are the "source of truth":

- `5-project-memory/siso-internal/STATE.yaml` — SISO Internal project state
- `6-roadmap/STATE.yaml` — Roadmap state
- `5-project-memory/siso-internal/feature_backlog.yaml` — Feature queue

**Always update these when making changes.**

---

## Autonomous System (NEW)

The new autonomous multi-agent system is at:

```
2-engine/08-autonomous-system/
├── README.md              # Architecture overview
├── redis-guide.md         # Redis coordination
├── task-tracking.md       # Task management
├── implementation/        # Working code
│   ├── agents/            # Supervisor, autonomous, interface
│   ├── schemas/           # Task dataclasses
│   ├── stores/            # JSON/SQLite storage
│   └── redis/             # Redis coordinator
└── research/              # Research findings
```

**Key insight:** Uses Redis pub/sub for 1ms agent coordination (10,000x faster than polling).

---

## Common Tasks

### Find a specific tool
```bash
grep -r "tool_name" 2-engine/05-tools/
```

### Check current tasks
Read: `5-project-memory/siso-internal/STATE.yaml` → `active_tasks`

### Find decisions about MCP
Look in: `1-docs/decisions/mcp/`

### Understand the memory system
Read: `2-engine/03-knowledge/storage/ProductionMemorySystem.py`

### Run the autonomous system demo
```bash
cd 2-engine/08-autonomous-system/implementation
python examples/basic_demo.py
```

---

## What Changed Recently

1. **Autonomous system moved** → `2-engine/08-autonomous-system/`
2. **Auto-claude moved** → `3-gui/integrations/auto-claude/`
3. **Morning routine docs** → `5-project-memory/siso-internal/.docs/`
4. **Decision docs** → `1-docs/decisions/`
5. **SYSTEM-MAP.yaml** → New root file (this guide's machine-readable version)

---

## Cache Files (Safe to Ignore/Delete)

- `**/__pycache__/` — Python cache
- `**/*.pyc` — Compiled Python
- `**/.pytest_cache/` — Test cache
- `3-gui/vibe-kanban/target/` — Rust build (7GB, rebuildable)
- `**/node_modules/` — JS dependencies

---

## Need Help?

1. Check `SYSTEM-MAP.yaml` for structure
2. Check `CATALOG.md` for features
3. Check `CLAUDE.md` for Claude Code integration
4. Read `README.md` for overview
