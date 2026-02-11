# BlackBox5 Hooks Framework

**Version:** 1.0.0
**Last Updated:** 2026-02-04
**Status:** Production Ready

---

## Overview

The BB5 hooks system provides automated maintenance, security, and context management for the BlackBox5 autonomous agent system. All hooks are **smart** - they self-discover agent type and context without requiring environment variables.

---

## Hook Inventory (9 Total)

### SessionStart Hooks

| Hook | Purpose | Agent-Aware |
|------|---------|-------------|
| `session-start-blackbox5.sh` | Load agent-specific context (planner/executor/architect) | ✅ Yes |
| `session-start-navigation.sh` | Discover hierarchy context (goal/plan/task) | ✅ Yes |

### PreToolUse Hooks

| Hook | Purpose | Blocking |
|------|---------|----------|
| `pre-tool-security.py` | Agent-aware security (rm -rf, .env, force push) | ✅ Exit code 2 |
| `pre-tool-validation.sh` | Validate structure before writes | ⚠️ Warn only |
| `architecture-consistency.sh` | Enforce naming conventions | ⚠️ Warn only |

### PostToolUse Hooks

| Hook | Purpose |
|------|---------|
| `timeline-maintenance.sh` | Auto-update timeline.yaml on milestones |
| `context-synchronization.sh` | Sync goal progress, task status |

### Subagent Hooks

| Hook | Purpose |
|------|---------|
| `subagent-tracking.sh` | Log agent lifecycle to events.yaml |

### Stop Hooks

| Hook | Purpose |
|------|---------|
| `stop-hierarchy-update.sh` | Update parent timelines on completion |

---

## Smart Hook Pattern

All BB5 hooks use **self-discovery** instead of environment variables:

```bash
detect_agent_type() {
    local cwd="$(pwd)"
    local run_dir="${RALF_RUN_DIR:-$cwd}"

    # Method 1: Run directory path
    if [[ "$run_dir" == *"/planner/"* ]]; then
        echo "planner"
    elif [[ "$run_dir" == *"/executor/"* ]]; then
        echo "executor"
    elif [[ "$run_dir" == *"/architect/"* ]]; then
        echo "architect"
    fi

    # Method 2: File patterns
    if [ -f "queue.yaml" ]; then
        echo "planner"  # Only planner has queue
    elif ls task-*-spec.md 1>/dev/null 2>&1; then
        echo "executor"  # Executor has task specs
    fi
}
```

### Detection Methods

1. **Run directory path** - `runs/planner/`, `runs/executor/`, `runs/architect/`
2. **Current working directory** - Agent-specific folders
3. **File patterns** - `queue.yaml` = planner, `task-*-spec.md` = executor
4. **Parent directories** - `.autonomous/agents/{planner,executor,architect}/`
5. **Git branch name** - Branch contains agent type hint

---

## Event Types

### SessionStart
Fires when Claude Code session begins.

**Input:**
```json
{
  "session_id": "uuid",
  "source": "startup|resume|clear",
  "timestamp": "2026-02-04T07:00:00Z"
}
```

**Output (can return additionalContext):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Context injected into Claude's prompt"
  }
}
```

### PreToolUse
Fires before any tool executes. Can block with exit code 2.

**Input:**
```json
{
  "tool_name": "Bash|Write|Edit|Task",
  "tool_input": { "command": "..." },
  "session_id": "uuid"
}
```

**Exit Codes:**
- `0` = Continue (allow tool)
- `2` = Block with error (shows stderr to Claude)

### PostToolUse
Fires after tool succeeds.

**Input:**
```json
{
  "tool_name": "Bash|Write|Edit",
  "tool_input": { ... },
  "tool_output": { ... },
  "session_id": "uuid"
}
```

### SubagentStart / SubagentStop
Fires when subagents spawn/complete.

**Input:**
```json
{
  "agent_id": "executor-001",
  "agent_type": "executor|planner|architect",
  "parent_task": "TASK-123"
}
```

### Stop
Fires when session ends.

**Input:**
```json
{
  "session_id": "uuid",
  "duration_seconds": 3600
}
```

---

## Agent-Specific Context

### Planner Context
Loaded by `session-start-blackbox5.sh`:
- Queue status (active/completed tasks)
- Recent loop summaries
- Executor health from heartbeat.yaml
- Blocked tasks

### Executor Context
- Claimed task from queue.yaml
- Task requirements
- Acceptance criteria
- Related files

### Architect Context
- System architecture docs
- Active goals count
- Recent decisions
- Pending reviews

---

## Security Rules

### Pre-Tool-Security Hook

| Rule | Planner | Executor | Architect |
|------|---------|----------|-----------|
| `rm -rf` | ❌ Block | ❌ Block | ❌ Block |
| `.env` access | ❌ Block | ✅ Allow | ⚠️ Warn |
| `git push --force` | ❌ Block | ❌ Block | ✅ Allow |
| Destructive DB ops | ❌ Block | ❌ Block | ✅ Allow |

---

## Best Practices

### 1. Always Fail Silent
Hooks should never break the user experience:

```python
try:
    main_logic()
except Exception:
    sys.exit(0)  # Never block on hook errors
```

### 2. Use JSON Logging
Standardized logging pattern:

```python
def log_event(data, filename):
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / filename
    logs = json.load(log_file) if log_file.exists() else []
    logs.append(data)

    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
```

### 3. Self-Discover Context
Never rely on environment variables:

```bash
# ❌ Bad
AGENT_TYPE="$RALF_AGENT_TYPE"

# ✅ Good
AGENT_TYPE=$(detect_agent_type)
```

### 4. Exit Code Semantics
- `0` = Success / Continue
- `2` = Block with error (only PreToolUse/UserPromptSubmit)

### 5. Graceful Degradation
If context file missing, continue without it:

```bash
if [ -f "queue.yaml" ]; then
    # Load queue data
else
    echo "⚠️  Queue not found, continuing without it"
fi
```

---

## Troubleshooting

### Hook Not Firing
1. Check `.claude/settings.json` registration
2. Verify hook file permissions (`chmod +x`)
3. Check hook syntax (run manually)

### Hook Blocking Legitimate Actions
1. Check agent type detection: `bb5 whereami`
2. Review security rules in `pre-tool-security.py`
3. Temporarily disable: rename hook with `.disabled` suffix

### Performance Issues
1. Time hook execution: `time ./hook.sh < test_input.json`
2. Target: <100ms per hook
3. Cache expensive operations

### Context Not Loading
1. Check run directory path contains agent type
2. Verify context files exist
3. Check `AGENT_CONTEXT.md` generated in run folder

---

## Integration with BB5 Autonomous Loop

```
Planner Loop:
  SessionStart → Load queue status → Plan → Spawn Executor
                      ↓
              subagent-tracking.sh (logs spawn)

Executor Run:
  SessionStart → Load claimed task → Execute → Complete
                      ↓                    ↓
              subagent-tracking.sh    stop-hierarchy-update.sh
                  (logs completion)      (updates parent)

Agent Handoff:
  Subagent hooks log all transitions in communications/events.yaml
```

---

## Files

- **Hooks:** `~/.blackbox5/.claude/hooks/`
- **Settings:** `~/.blackbox5/.claude/settings.json`
- **Logs:** `~/.blackbox5/.claude/logs/`
- **Documentation:** `~/.blackbox5/.claude/HOOKS.md` (this file)

---

## Research Sources

- [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) - 13 hooks, TTS, LLM integration
- [claudekit](https://github.com/carlrannaberg/claudekit) - Quality enforcement, security patterns
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - Community hooks catalog
- [everything-claude-code](https://github.com/affaan-m/everything-claude-code) - Memory persistence

---

## Changelog

### v1.0.0 (2026-02-04)
- Initial release
- 9 smart hooks implemented
- Agent-aware context loading
- Self-discovery pattern (no env vars)
- Security rules by agent type

---

*For more information, see IG-009: Improve Hooks for Automated Maintenance*
