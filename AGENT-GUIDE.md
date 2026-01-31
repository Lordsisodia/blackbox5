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
| Agent implementations | `2-engine/core/agents/definitions/` |
| Core orchestration | `2-engine/core/orchestration/` |
| CLI/API/Client | `2-engine/core/interface/` |
| Safety systems | `2-engine/core/safety/` |
| Tools (106+) | `2-engine/tools/core/` |
| Memory systems | `2-engine/runtime/memory/` |
| External integrations | `2-engine/tools/integrations/` |
| Hooks | `2-engine/runtime/hooks/` |
| Autonomous system | `2-engine/core/autonomous/` |
| GUI/Vibe Kanban | `3-gui/apps/vibe-kanban/` |
| GUI integrations | `3-gui/integrations/` |
| Project state | `5-project-memory/siso-internal/` |
| Roadmap/plans | `6-roadmap/` |
| Decision records | `1-docs/decisions/` |

### Core Structure Detail

See `2-engine/core/CORE-STRUCTURE.md` for detailed core/ navigation.

| Agent Type | Location |
|------------|----------|
| Core agents (base classes) | `2-engine/core/agents/definitions/core/` |
| Core agents (Analyst, Architect, Developer) | `2-engine/core/agents/definitions/core/` |
| Managerial agents | `2-engine/core/agents/definitions/managerial/` |
| Specialist agents (18 YAMLs) | `2-engine/core/agents/definitions/specialists/` |

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

## Autonomous System

The autonomous multi-agent system is at:

```
2-engine/core/autonomous/
├── README.md              # Architecture overview
├── agents/                # Supervisor, autonomous, interface
├── schemas/               # Task dataclasses
├── stores/                # JSON/SQLite storage
└── redis/                 # Redis coordinator
```

**Key insight:** Uses Redis pub/sub for 1ms agent coordination (10,000x faster than polling).

**Documentation:**
- `1-docs/guides/autonomous/` - Implementation guides
- `1-docs/research/autonomous-system/` - Research findings

---

## Common Tasks

### Pre-execution Verification (Before Starting Work)
```bash
# Run verification to prevent duplicate work and validate paths
./bin/verify-task

# With specific task file
./bin/verify-task --task-file path/to/task.md

# With specific project directory
./bin/verify-task --project-dir 5-project-memory/blackbox5
```

**What it checks:**
1. STATE.yaml freshness (warns if stale)
2. Duplicate task detection (prevents redoing work)
3. Path validation (ensures referenced files exist)
4. Active tasks count

**Exit codes:**
- 0: All checks passed - safe to proceed
- 1: Warnings - proceed with caution
- 2: Errors found - fix recommended
- 3: Critical issues - do not proceed

### Find a specific tool
```bash
grep -r "tool_name" 2-engine/tools/core/
```

### Check current tasks
Read: `5-project-memory/siso-internal/STATE.yaml` → `active_tasks`

### Find decisions about MCP
Look in: `1-docs/decisions/mcp/`

### Understand the memory system
Read: `2-engine/runtime/memory/ProductionMemorySystem.py`

### Run the autonomous system demo
```bash
cd 2-engine/core/autonomous/
python examples/basic_demo.py
```

---

## What Changed Recently

1. **2-Engine Consolidation** → Merged 8 folders into 5:
   - `01-core/` + `02-agents/` + `04-work/` → `2-engine/core/`
   - `03-knowledge/` + `07-operations/` → `2-engine/runtime/`
   - `05-tools/` + `06-integrations/` → `2-engine/tools/`
   - `08-development/` → `1-docs/development/`
2. **Autonomous system** → `2-engine/core/autonomous/`
3. **Auto-claude moved** → `3-gui/integrations/auto-claude/`
4. **Morning routine docs** → `5-project-memory/siso-internal/.docs/`
5. **Decision docs** → `1-docs/decisions/`
6. **SYSTEM-MAP.yaml** → New root file (this guide's machine-readable version)
7. **CORE-STRUCTURE.md** → New guide for navigating core/ directory

---

## Cache Files (Safe to Ignore/Delete)

- `**/__pycache__/` — Python cache
- `**/*.pyc` — Compiled Python
- `**/.pytest_cache/` — Test cache
- `3-gui/apps/vibe-kanban/target/` — Rust build (7GB, rebuildable)
- `**/node_modules/` — JS dependencies

---

## Need Help?

1. Check `SYSTEM-MAP.yaml` for structure
2. Check `CATALOG.md` for features
3. Check `CLAUDE.md` for Claude Code integration
4. Read `README.md` for overview
