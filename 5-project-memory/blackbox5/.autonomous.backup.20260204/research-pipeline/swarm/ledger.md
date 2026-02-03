# Swarm Ledger

**Purpose:** Chronological history of all swarm activity
**Updated:** Automatically by agents and orchestrator
**Format:** Markdown with YAML frontmatter for structured data

---

```yaml
ledger_meta:
  version: "1.0.0"
  created: "2026-02-04T00:00:00Z"
  last_entry: null
  total_entries: 0
```

---

## 2026-02-04

### System Initialization

**Timestamp:** 2026-02-04T00:00:00Z
**Type:** system.initialization

**Details:**
- Swarm memory system initialized
- All 6 agents registered: scout-worker, scout-validator, analyst-worker, analyst-validator, planner-worker, planner-validator
- Pipeline phases configured: scout → analyst → planner
- Resource allocation set based on 10:3:1:0.3 token ratio
- Coordination rules activated

**State:**
- All agents: idle
- All queues: empty
- Pipeline: ready

---

*Ledger will be populated as agents begin operation*

### Entry Template

```markdown
### HH:MM UTC - Event Title

**Timestamp:** ISO-8601 timestamp
**Type:** event_type
**Source:** agent_name
**Run ID:** run-YYYYMMDD-NNN

**Details:**
Description of what happened

**Data:**
```yaml
key: value
```

**Impact:**
- Metric changes
- Queue updates
- State transitions

**Decisions:**
- What was decided
- Why

**Next Steps:**
- What happens next
```

---

## Event Types

| Type | Description | Source |
|------|-------------|--------|
| pattern.extracted | New pattern found | scout-worker |
| analysis.complete | Pattern scored | analyst-worker |
| task.created | BB5 task created | planner-worker |
| validation.feedback | Validator input | *-validator |
| swarm.rebalance | Resource adjustment | orchestrator |
| agent.status_change | Health change | any agent |
| bottleneck.detected | Pipeline blocked | orchestrator |
| system.initialization | Swarm started | system |
