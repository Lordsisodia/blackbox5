# Dual-RALF Research Pipeline

**Version:** 1.0.0
**Status:** Active Development
**Last Updated:** 2026-02-04

---

## Overview

The Dual-RALF Research Pipeline is a 6-agent parallel architecture that discovers, analyzes, and plans implementation of patterns from external sources (GitHub, YouTube, documentation).

**Architecture:** Worker-Validator pairs running simultaneously
- Scout Pair: Discovers and extracts patterns
- Analyst Pair: Ranks patterns by value/complexity
- Planner Pair: Creates BB5 tasks from recommendations

---

## Quick Start

### Starting the Pipeline

```bash
# Terminal 1 - Scout Worker
./ralf-loop.sh --role scout-worker --project research-pipeline

# Terminal 2 - Scout Validator
./ralf-loop.sh --role scout-validator --project research-pipeline

# Terminal 3 - Analyst Worker
./ralf-loop.sh --role analyst-worker --project research-pipeline

# Terminal 4 - Analyst Validator
./ralf-loop.sh --role analyst-validator --project research-pipeline

# Terminal 5 - Planner Worker
./ralf-loop.sh --role planner-worker --project research-pipeline

# Terminal 6 - Planner Validator
./ralf-loop.sh --role planner-validator --project research-pipeline
```

---

## Directory Structure

```
research-pipeline/
├── README.md                          # This file
├── DUAL-RALF-RESEARCH-ARCHITECTURE.md # Full architecture spec
├── INDEX.md                           # Quick reference index
├── XREF.md                           # Cross-references
├── STATE.yaml                        # Current pipeline state
├── agents/
│   ├── scout-worker/                 # Pattern extraction
│   ├── scout-validator/              # Extraction validation
│   ├── analyst-worker/               # Pattern analysis
│   ├── analyst-validator/            # Analysis validation
│   ├── planner-worker/               # Task planning
│   └── planner-validator/            # Planning validation
├── communications/                   # Shared coordination
├── context/                          # Shared context
├── data/                            # Shared data
├── logs/                            # Centralized logs
├── operations/                      # Operational data
├── reviews/                         # Review documents
└── .templates/                      # Document templates
```

---

## Key Documents

| Document | Purpose |
|----------|---------|
| `DUAL-RALF-RESEARCH-ARCHITECTURE.md` | Complete architecture specification |
| `INDEX.md` | Quick reference for all components |
| `XREF.md` | Cross-references between patterns, tasks, etc. |
| `STATE.yaml` | Current pipeline state |
| `communications/protocol.yaml` | Rules of engagement |

---

## Communication

All agents communicate via files in `communications/`:

- `queue.yaml` - Task queue for BB5
- `events.yaml` - Pipeline events
- `chat-log.yaml` - Bidirectional chat
- `heartbeat.yaml` - Health checks
- `*-state.yaml` - Phase-specific state

---

## Token Budgets

| Agent | Target/Run | Context Limit | Frequency |
|-------|-----------|---------------|-----------|
| Scout Worker | 3,000 | 7,500 (40%) | Every 10 min |
| Scout Validator | 1,000 | 2,500 (40%) | Every 10 min |
| Analyst Worker | 4,800 | 12,000 (40%) | Every 15 min |
| Analyst Validator | 1,200 | 3,000 (40%) | Every 15 min |
| Planner Worker | 3,600 | 9,000 (40%) | On demand |
| Planner Validator | 600 | 1,500 (40%) | On demand |

---

## Status

Check current status:

```bash
# View pipeline state
cat communications/pipeline-state.yaml

# View heartbeats
cat communications/heartbeat.yaml

# View recent events
tail -50 communications/events.yaml
```

---

## Documentation

- Full architecture: `DUAL-RALF-RESEARCH-ARCHITECTURE.md`
- Templates: `.templates/`
- Master task: See BlackBox5 task system

---

*Part of the BlackBox5 Agentic System*
