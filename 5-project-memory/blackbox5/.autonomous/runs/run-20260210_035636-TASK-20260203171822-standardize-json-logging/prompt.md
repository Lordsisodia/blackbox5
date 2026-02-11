You are the BB5 Autonomous Executor. Your mission is to execute tasks and improve the BlackBox5 system.

## Current Task

Task File: /opt/blackbox5/5-project-memory/blackbox5/.autonomous/tasks/active/IMPROVING-V2-HOOKS/tasks/TASK-20260203171822-standardize-json-logging.md
Run Folder: /opt/blackbox5/5-project-memory/blackbox5/.autonomous/runs/run-20260210_035636-TASK-20260203171822-standardize-json-logging

# TASK-20260203171822: Standardize JSON Logging Across All RALF Hooks

**Task ID:** TASK-20260203171822
**Type:** refactor
**Priority:** high
**Status:** partial
**Created:** 2026-02-03T17:18:22Z
**Estimated Lines:** 300

---

## Objective

Standardize all RALF hooks to use consistent JSON logging pattern from claude-code-hooks-mastery.

---

## Context

Current RALF has mixed logging - some hooks use text files, some use JSON, some don't log at all. Hooks mastery uses consistent JSON logging pattern across all 13 hooks.

From analysis: "JSON Logging Pattern - All hooks use the same logging pattern: Read existing or init empty list, Append new data, Write back with formatting"

This enables: analytics, debugging, auditing, log aggregation.

---

## Success Criteria

- [ ] All hooks log to `logs/{hook_name}.json`
- [ ] All hooks use consistent JSON structure
- [ ] All hooks append to existing logs (don't overwrite)
- [ ] Log rotation strategy defined
- [ ] Documentation updated with logging schema
- [ ] Helper function created for reuse
- [ ] All 20+ RALF hooks updated

---

## Implementation Details

### Standard Pattern (from mastery)

```python
def log_hook_data(hook_name, input_data):
    """Standard JSON logging for hooks."""
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f'{hook_name}.json'

    # Read existing or init empty
    if log_file.exists():
        with open(log_file, 'r') as f:
            try:
                log_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                log_data = []
    else:
        log_data = []

    # Add timestamp
    entry = {
        "timestamp": datetime.now().isoformat(),
        "data": input_data
    }

    # Append and write
    log_data.append(entry)
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)
```

### Hooks to Update

1. `inject-session-context.sh` - Convert to JSON logging
2. `checkpoint-auto-save.sh` - Already JSON, verify consistency
3. `ralph-context-injector.sh` - Add logging
4. `learning-gate.sh` - Add logging
5. `rule-verification.sh` - Add logging
6. All other active hooks...

---

## Files to Create/Modify

**New Files:**
- `.claude/hooks/utils/logging.py` - Shared logging helper
- `docs/hooks/LOGGING.md` - Logging documentation

**Modified Files:**
- All hook files in `.claude/hooks/`
- `.claude/settings.json` - May need updates

---

## Rollback Strategy

1. Keep text logs as backup during transition
2. Implement JSON logging alongside text logs
3. Verify JSON logs work correctly
4. Remove text logging after validation

---

## Dependencies

- [ ] Decision: Log retention policy
- [ ] Decision: Log rotation strategy
- [ ] Analysis: Inventory all hooks needing updates

---

## Related

- Analysis: `6-roadmap/.research/external/GitHub/Claude-Code/extracted/repos/RALF-HOOKS-ANALYSIS.md`
- Integration Plan: `5-project-memory/blackbox5/.autonomous/tasks/hooks-integration/HOOKS-INTEGRATION-PLAN.md`

---

## Notes

**Why Standardize:**
Mixed logging formats make debugging and analytics impossible. JSON enables: structured queries, log aggregation, debugging tools, audit trails.

**Log Growth:**
Consider log rotation - JSON logs can grow large. Implement rotation after 10MB or 30 days.

**Helper Function:**
Create shared utility to avoid duplicating logging code across 20+ hooks.

## Instructions

1. Read the task description carefully
2. Analyze the current BB5 state related to this task
3. Implement the improvements described
4. Make SMALL, focused changes (30 minutes max)
5. Test your changes if applicable
6. Update the task file to mark it as complete:
   - Change **Status:** from pending/partial to completed
   - Add a summary of what was done
7. Document your work in the run folder:
   - /opt/blackbox5/5-project-memory/blackbox5/.autonomous/runs/run-20260210_035636-TASK-20260203171822-standardize-json-logging/THOUGHTS.md - Your reasoning
   - /opt/blackbox5/5-project-memory/blackbox5/.autonomous/runs/run-20260210_035636-TASK-20260203171822-standardize-json-logging/DECISIONS.md - What you decided
   - /opt/blackbox5/5-project-memory/blackbox5/.autonomous/runs/run-20260210_035636-TASK-20260203171822-standardize-json-logging/LEARNINGS.md - What you learned
   - /opt/blackbox5/5-project-memory/blackbox5/.autonomous/runs/run-20260210_035636-TASK-20260203171822-standardize-json-logging/RESULTS.md - What was accomplished
8. Commit changes with a descriptive message

## Critical Rules

- ONLY work on THIS specific task
- Do NOT modify other tasks
- Do NOT break existing functionality
- If you cannot complete the task, mark it as partial and explain why
- When done, output: <promise>COMPLETE</promise>
- If partially done, output: <promise>PARTIAL</promise>

## Git Commands

After making changes:
```bash
git add -A
git commit -m "ralf: [TASK-20260203171822-standardize-json-logging] brief description of changes"
```

Begin execution now.
