# Research Pipeline Index

**Quick reference for all components**

---

## Agents (6 Total)

### Scout Pair
| Component | Type | Purpose | Location |
|-----------|------|---------|----------|
| Scout Worker | Worker | Extract patterns from sources | `agents/scout-worker/` |
| Scout Validator | Validator | Monitor and improve extraction | `agents/scout-validator/` |

### Analyst Pair
| Component | Type | Purpose | Location |
|-----------|------|---------|----------|
| Analyst Worker | Worker | Rank patterns by value/cost | `agents/analyst-worker/` |
| Analyst Validator | Validator | Monitor and improve analysis | `agents/analyst-validator/` |

### Planner Pair
| Component | Type | Purpose | Location |
|-----------|------|---------|----------|
| Planner Worker | Worker | Create BB5 tasks | `agents/planner-worker/` |
| Planner Validator | Validator | Monitor and improve planning | `agents/planner-validator/` |

---

## Communication Files

| File | Purpose | Written By | Read By |
|------|---------|------------|---------|
| `communications/queue.yaml` | Task queue | Planner Worker | BB5 Executor |
| `communications/events.yaml` | Pipeline events | All | All |
| `communications/chat-log.yaml` | Bidirectional chat | All | All |
| `communications/heartbeat.yaml` | Health checks | All | All |
| `communications/protocol.yaml` | Rules | Human | All |
| `communications/scout-state.yaml` | Scout state | Scout Pair | Scout Pair |
| `communications/analyst-state.yaml` | Analyst state | Analyst Pair | Analyst Pair |
| `communications/planner-state.yaml` | Planner state | Planner Pair | Planner Pair |
| `communications/pipeline-state.yaml` | Overall state | All | All |

---

## Run Documentation (Per Agent)

Each run creates:
- `THOUGHTS.md` - Reasoning and analysis
- `RESULTS.md` - Outcomes and metrics
- `DECISIONS.md` - Decisions made
- `ASSUMPTIONS.md` - Assumptions and validation
- `LEARNINGS.md` - Patterns and insights
- `metadata.yaml` - Structured run data
- `timeline/{DATE}.md` - Daily activity log

Templates: `.templates/runs/`

---

## Data Storage

| Location | Purpose |
|----------|---------|
| `data/patterns/` | Extracted patterns |
| `data/analysis/` | Analysis results |
| `data/tasks/` | Planned tasks |

---

## Key Metrics

- **Sources/Patterns/Tasks processed** - Throughput
- **Token usage** - Efficiency
- **Confidence scores** - Quality
- **Time per phase** - Speed

View in: `communications/pipeline-state.yaml`

---

## Quick Commands

```bash
# Check status
cat communications/pipeline-state.yaml

# View heartbeats
cat communications/heartbeat.yaml

# Recent events
tail -50 communications/events.yaml

# Queue depth
cat communications/queue.yaml | grep current_depth

# Agent logs
ls logs/{scout,analyst,planner}/
```

---

## Architecture

Full specification: `DUAL-RALF-RESEARCH-ARCHITECTURE.md`

---

*Last updated: 2026-02-04*
