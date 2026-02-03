# Research Pipeline Hooks

**Location:** `.claude/hooks/`
**Purpose:** Claude Code hooks for the Dual-RALF Research Pipeline

---

## Available Hooks

### session-start-timeline-memory.sh

**Event:** SessionStart
**Purpose:** Automatically injects agent-specific timeline memory into context

**What it does:**
1. Detects which agent is running (via RALF_AGENT_TYPE or prompt file path)
2. Reads the agent's timeline-memory.md file
3. Injects timeline memory + work assignment instructions into context
4. Provides clear guidance on what work to perform

**Agent Detection:**
- Checks `RALF_AGENT_TYPE` environment variable
- Falls back to parsing `RALF_PROMPT_FILE` path
- Supports: scout-worker, scout-validator, analyst-worker, analyst-validator, planner-worker, planner-validator

**Injected Context:**
```
## Agent Identity
You are the {agent} in the Dual-RALF Research Pipeline

## Your Timeline Memory (Long-Term Context)
[Full timeline-memory.md content]

## Work Assignment Instructions
[Specific instructions for this agent type]
```

**Installation:**
Add to your `.claude/settings.json`:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/research-pipeline/.claude/hooks/session-start-timeline-memory.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Timeline Memory System

**Location:** `agents/{agent}/timeline-memory.md`
**Format:** YAML frontmatter + markdown
**Updated:** Automatically by agents at end of each run

**Purpose:**
- Persistent long-term memory across runs
- Work queue management
- History tracking
- Learning progression
- Coordination context

**Structure:**
```yaml
timeline_memory:
  version: "1.0.0"
  agent: "agent-name"
  total_runs: 0

history: []              # Chronological work history
work_queue:              # What to work on
  priority_items: []
  backlog: []
  in_progress: null
current_context: {}      # Current work context
stats: {}                # Performance statistics
```

---

## Related Task Documents

### Active Tasks

| Task | Description | Location |
|------|-------------|----------|
| TASK-1738375000 | Implement Feature F-016 (CLI Interface) | `tasks/active/TASK-1738375000/task.md` |
| TASK-1769978192 | Research Pipeline Implementation | `tasks/active/TASK-1769978192/task.md` |

### Hook-Related Tasks in Blackbox5

| Task ID | Description | Hook Integration |
|---------|-------------|------------------|
| TASK-1769802000 | Shell Phase Gate Integration | Phase gate hooks |
| TASK-1769800446 | Decision Registry Implementation | Decision tracking hooks |
| TASK-1769799336 | Integrate v23 Unified Loop | Session management hooks |
| TASK-1769800176 | Create Workflow Loader Library | Workflow execution hooks |

---

## Hook Integration Points

### SessionStart (Implemented)
- **Hook:** session-start-timeline-memory.sh
- **Purpose:** Inject timeline memory and work assignment instructions
- **Status:** ✅ Ready to use

### Future Hook Opportunities

**PreToolUse - Pattern Extraction Validation:**
- Validate pattern structure before Write
- Check pattern ID format
- Ensure required fields present

**PostToolUse - Event Publishing:**
- Monitor events.yaml updates
- Trigger downstream agents
- Update shared state

**Stop - Timeline Update:**
- Auto-update timeline-memory.md
- Persist run results
- Update work queue

---

## Configuration

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `RALF_AGENT_TYPE` | Agent identification | `scout-worker` |
| `RALF_PROMPT_FILE` | Prompt file path | `/path/to/scout-worker.md` |
| `RALF_PROJECT_DIR` | Project root | `/path/to/project` |
| `RALF_RUN_DIR` | Current run directory | `/path/to/run-20260204-001` |

### Settings.json Example

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.blackbox5/5-project-memory/blackbox5/.autonomous/research-pipeline/.claude/hooks/session-start-timeline-memory.sh",
            "timeout": 30
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.blackbox5/5-project-memory/blackbox5/.autonomous/research-pipeline/.claude/hooks/validate-pattern-write.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Testing Hooks

### Manual Test
```bash
# Test the hook directly
cd ~/.blackbox5/5-project-memory/blackbox5/.autonomous/research-pipeline
echo '{"source": "startup", "session_id": "test-123"}' | ./.claude/hooks/session-start-timeline-memory.sh
```

### Verify Timeline Memory Injection
1. Start a new Claude Code session
2. Check that timeline memory appears in context
3. Verify work assignment instructions are present
4. Confirm agent identity is correct

---

## Troubleshooting

### Hook Not Running
- Check file permissions: `chmod +x session-start-timeline-memory.sh`
- Verify path in settings.json is absolute
- Check Claude Code debug output: `claude --debug`

### Timeline Memory Not Found
- Ensure timeline-memory.md exists for the agent
- Check RALF_AGENT_TYPE is set correctly
- Verify RALF_PROJECT_DIR points to correct location

### Wrong Agent Detected
- Check RALF_AGENT_TYPE environment variable
- Verify RALF_PROMPT_FILE contains agent name
- Review hook logs for detection logic

---

## References

- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Multi-Agent Ralph Loop Hooks](~/.blackbox5/2-engine/.autonomous/.docs/github/multi-agent-ralph-loop/.claude/hooks/)
- [RALF Loop Implementation](../../../2-engine/.autonomous/shell/ralf-loop.sh)
