# SSOT Hooks/Triggers Violations Report

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Summary

Hooks and triggers are scattered across **3 directories** with **6 different agent detection implementations**. Event logging has **5+ events.yaml files** with no synchronization.

---

## 1. Hook Script Proliferation (CRITICAL)

**Hook scripts exist in 3+ locations:**

| Location | Count | Purpose |
|----------|-------|---------|
| `.claude/hooks/` | ~15 | Main Claude hooks |
| `2-engine/.claude/hooks/` | ~10 | Engine hooks |
| `.autonomous/memory/hooks/` | ~3 | Memory-related hooks |
| `bin/` | ~5 | Hook-related scripts |

**Total: 33+ hook scripts scattered**

---

## 2. Agent Detection Duplication

**6 different implementations of agent detection:**

| Location | Method | Issue |
|----------|--------|-------|
| `.claude/hooks/ralf-session-start-hook.sh` | Hardcoded AGENT_NAME | Not dynamic |
| `2-engine/.claude/hooks/subagent-tracking.sh` | Reads from file | Different method |
| Agent scripts | Hardcoded in script | Per-script definition |
| `events.yaml` | `agent_type: unknown` | 529 occurrences |
| `agent-state.yaml` | Should be registry | EMPTY |
| `protocol.yaml` | Defines agent IDs | Not enforced |

**Specific Inconsistency:**
```yaml
# events.yaml (from hooks)
agent_type: unknown
agent_id: unknown

# vs agent scripts
AGENT_NAME="planner"  # Hardcoded

# vs protocol.yaml
planner:
  id: "RALF-PLANNER-001"
  # Not used consistently
```

---

## 3. Events Log Duplication

**Events stored in 5+ files:**

| File | Purpose | Entries | Issue |
|------|---------|---------|-------|
| `.autonomous/agents/communications/events.yaml` | Main event log | 530+ | Should be SSOT |
| `events.yaml` (root) | Duplicate? | Unknown | Which is canonical? |
| `2-engine/.autonomous/events.yaml` | Engine events | Unknown | Separate from project |
| `goals/active/*/events.yaml` | Goal events | 8+ files | Per-goal duplication |
| `timeline.yaml` | Event timeline | 1500+ lines | Overlapping content |

**Issue:** Same events logged in multiple places with different formats.

---

## 4. Trigger Rules Duplication

**Trigger rules defined in 3+ places:**

| Location | Rules |
|----------|-------|
| `CLAUDE.md` | Auto-trigger rules table |
| `operations/skill-selection.yaml` | Domain mapping triggers |
| `bin/bb5-*` scripts | Inline trigger logic |
| `.claude/hooks/` | Hook trigger conditions |

**Example Duplication:**
- CLAUDE.md: "Task contains 'implement' + domain keyword → MUST check skill"
- skill-selection.yaml: Same logic in YAML format
- Scripts: Same logic in bash

---

## 5. Hook Configuration Duplication

**Hook configuration in multiple places:**

| File | Config |
|------|--------|
| `.claude/settings.json` | Hook paths |
| `2-engine/.claude/settings.json` | Engine hook paths |
| `.claude/hooks/*.sh` | Inline configuration |
| `CLAUDE.md` | Hook documentation |

**Issue:** Hook paths defined in settings AND hardcoded in scripts.

---

## 6. Session/State Tracking Duplication

**Session state tracked in:**

| File | Data |
|------|------|
| `.claude/ralf-session.json` | Session metadata |
| `heartbeat.yaml` | Last seen timestamps |
| `agent-state.yaml` | Should track state | EMPTY |
| `execution-state.yaml` | Slot status |
| `events.yaml` | Lifecycle events |

**Inconsistency Example:**
```yaml
# heartbeat.yaml
planner:
  status: in_progress_TASK-xxx
  loop_number: 30

# execution-state.yaml
slot_1:
  status: "idle"  # <-- Contradicts heartbeat!

# events.yaml
- type: agent_start
  agent_type: unknown  # <-- Can't identify agent!
```

---

## 7. Stop Hook Validation Duplication

**Stop validation in 2+ places:**

| Location | Validation |
|----------|------------|
| `.claude/hooks/ralf-stop-hook.sh` | Stop validation |
| `2-engine/.claude/hooks/validate-stop.sh` | Similar validation |
| `bin/ralf-verifier.sh` | Verification logic |

**Issue:** Same stop validation logic in multiple hooks.

---

## Specific Examples

### Example 1: Agent Identity Unknown
```yaml
# From events.yaml analysis
- timestamp: '2026-02-04T09:45:04+07:00'
  type: agent_stop
  agent_type: unknown      # <-- Hook doesn't know agent
  agent_id: unknown
  source: hook
```

**Root Cause:** Hooks don't have access to agent context.

### Example 2: Duplicate Event Logging
```yaml
# events.yaml (from hook)
- timestamp: '2026-02-04T09:45:04+07:00'
  type: agent_start
  agent_type: unknown

# timeline.yaml (separate system)
- timestamp: "2026-02-04T09:45:04+07:00"
  type: "Agent Started"
  description: "Planner agent started"

# Same event, two logs, different formats
```

### Example 3: Trigger Rule Inconsistency
```yaml
# CLAUDE.md
Auto-Trigger: "implement" + domain keyword → check skill

# skill-selection.yaml
triggers:
  - pattern: "implement.*(git|n8n|supabase)"
    action: check_skill

# Different patterns for same trigger!
```

---

## Recommendations for SSOT

### 1. Hook Consolidation
**Canonical Location:** `.claude/hooks/`
- Move engine hooks to main hooks directory
- Delete `.autonomous/memory/hooks/` (wrong location)
- Single source for all hooks

### 2. Agent Identity SSOT
**Canonical Source:** `agent-state.yaml` (to be populated)
- Hooks read agent identity from state file
- Agents register on start
- Events reference registered agents

### 3. Events SSOT
**Canonical Source:** `.autonomous/agents/communications/events.yaml`
- Delete duplicate events.yaml files
- timeline.yaml becomes DERIVED view
- Single format for all events

### 4. Trigger Rules SSOT
**Canonical Source:** `operations/trigger-rules.yaml` (to create)
- Define all triggers in ONE file
- CLAUDE.md references, doesn't duplicate
- Scripts load rules from file

### 5. Hook Configuration SSOT
**Canonical Source:** `.claude/hooks/config.yaml` (to create)
- All hook configuration in one place
- Settings.json references config.yaml
- Scripts load config, don't hardcode

---

## Critical Files Requiring Immediate Attention

1. `2-engine/.claude/hooks/` - Merge into main hooks/
2. `.autonomous/memory/hooks/` - Move to hooks/
3. `events.yaml` (root) - Delete or merge
4. `2-engine/.autonomous/events.yaml` - Consolidate
5. `agent-state.yaml` - Populate with agent registry
6. `CLAUDE.md` trigger rules - Move to YAML file

---

## Task Creation Checklist

- [ ] TASK-SSOT-019: Consolidate hook scripts to single directory
- [ ] TASK-SSOT-020: Create agent identity registry
- [ ] TASK-SSOT-021: Merge duplicate events.yaml files
- [ ] TASK-SSOT-022: Create central trigger-rules.yaml
- [ ] TASK-SSOT-023: Create hook configuration file
- [ ] TASK-SSOT-024: Update hooks to use agent registry
- [ ] TASK-SSOT-025: Standardize event format
