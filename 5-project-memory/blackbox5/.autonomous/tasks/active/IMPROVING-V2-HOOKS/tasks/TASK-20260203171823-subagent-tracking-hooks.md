# TASK-20260203171823: Create Subagent Tracking Hooks for Executor/Planner/Architect

**Task ID:** TASK-20260203171823
**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-03T17:18:23Z
**Estimated Lines:** 400

---

## Objective

Create subagent_start and subagent_stop hooks for tracking Executor, Planner, and Architect agents in the RALF system.

---

## Context

RALF has 3 autonomous agents (Executor, Planner, Architect). Hooks mastery shows comprehensive subagent lifecycle tracking with logging and task summarization.

From analysis: "SubagentStart/Stop hooks - Critical for Executor/Planner/Architect tracking. subagent_stop includes task summarization via LLM."

Current RALF has no subagent lifecycle hooks. This is needed for: agent coordination, task tracking, observability, debugging multi-agent flows.

---

## Success Criteria

- [ ] subagent_start hook created and registered
- [ ] subagent_stop hook created and registered
- [ ] Hooks log agent spawn/completion to JSON
- [ ] subagent_stop includes task summarization
- [ ] Hooks integrate with RALF agent system
- [ ] Executor agent tracking working
- [ ] Planner agent tracking working
- [ ] Architect agent tracking working (if created)
- [ ] Documentation updated

---

## Implementation Details

### Subagent Start Hook

```python
def main():
    input_data = json.loads(sys.stdin.read())
    agent_id = input_data.get("agent_id", "unknown")
    agent_type = input_data.get("agent_type", "unknown")

    # Add timestamp
    input_data["logged_at"] = datetime.now().isoformat()

    # Log to logs/subagent_start.json
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'subagent_start.json'

    # Read existing or init empty
    if log_file.exists():
        with open(log_file, 'r') as f:
            log_data = json.load(f)
    else:
        log_data = []

    log_data.append(input_data)
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)

    sys.exit(0)
```

### Subagent Stop Hook

```python
def extract_task_context(input_data):
    """Extract task context from subagent input data."""
    # Look for agent transcript path
    # Read initial task/prompt from JSONL transcript
    # Return brief description

def summarize_task(task_description, agent_name):
    """Summarize task completion (can use LLM)."""
    # Use local LLM or simple heuristic
    return f"Task completed by {agent_name}"

def main():
    input_data = json.loads(sys.stdin.read())
    agent_id = input_data.get("agent_id", "unknown")

    # Extract and summarize task
    task_context = extract_task_context(input_data)
    summary = summarize_task(task_context, agent_id)

    # Add to input data
    input_data["summary"] = summary
    input_data["logged_at"] = datetime.now().isoformat()

    # Log to logs/subagent_stop.json
    # ... same pattern as subagent_start

    sys.exit(0)
```

---

## Files to Create/Modify

**New Files:**
- `.claude/hooks/subagent_start.py` - Agent spawn tracking
- `.claude/hooks/subagent_stop.py` - Agent completion tracking
- `.claude/hooks/utils/task_summarizer.py` - Task summarization

**Modified Files:**
- `.claude/settings.json` - Register new hooks
- `docs/agents/AGENT_TRACKING.md` - Documentation

---

## Rollback Strategy

1. Create hooks as new files (don't modify existing)
2. Test with subagent tasks
3. If issues, remove hook registrations from settings.json

---

## Dependencies

- [ ] TASK-20260203171822: Standardize JSON Logging (for logging pattern)
- [ ] Decision: Task summarization approach (LLM vs heuristic)
- [ ] Analysis: Current agent spawn mechanism

---

## Related

- Source: `6-roadmap/.research/external/GitHub/Claude-Code/data/repos/claude-code-hooks-mastery/.claude/hooks/subagent_start.py`
- Source: `6-roadmap/.research/external/GitHub/Claude-Code/data/repos/claude-code-hooks-mastery/.claude/hooks/subagent_stop.py`
- Analysis: `6-roadmap/.research/external/GitHub/Claude-Code/extracted/repos/RALF-HOOKS-ANALYSIS.md`
- Integration Plan: `5-project-memory/blackbox5/.autonomous/tasks/hooks-integration/HOOKS-INTEGRATION-PLAN.md`

---

## Notes

**Why This Matters:**
RALF is a multi-agent system. Without subagent tracking, we can't: debug agent flows, audit agent decisions, optimize agent coordination, understand task handoffs.

**Task Summarization:**
The mastery repo uses LLM for summarization. For BB5, we could: use local LLM (Ollama), use simple heuristics, skip summarization initially.

**Agent Types:**
Track agent_type field to distinguish Executor vs Planner vs Architect.
