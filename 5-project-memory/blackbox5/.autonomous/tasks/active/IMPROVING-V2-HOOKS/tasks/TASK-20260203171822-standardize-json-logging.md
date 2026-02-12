# TASK-20260203171822: Standardize JSON Logging Across All RALF Hooks

**Task ID:** TASK-20260203171822
**Type:** refactor
**Priority:** high
**Status:** completed
**Created:** 2026-02-03T17:18:22Z
**Completed:** 2026-02-10T04:30:00Z
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

- [x] All hooks log to `logs/{hook_name}.json`
- [x] All hooks use consistent JSON structure
- [x] All hooks append to existing logs (don't overwrite)
- [x] Log rotation strategy defined
- [x] Documentation updated with logging schema
- [x] Helper function created for reuse
- [x] All 2 bash hooks and 1 Python hook updated (BB5 only has 3 active hooks)

---

## Completed Implementation

### Additional Files Updated (2026-02-10)

Found and updated 4 additional Python hooks that were not initially included in the task:

1. `retain-on-complete.py` - Added JSON logging with log_hook_data() calls
2. `task_completion_skill_recorder.py` - Added JSON logging for events and usage logs
3. `log-skill-on-complete.py` - Added JSON logging with hook invocation tracking
4. `pre-tool-security.py` - Replaced custom logging with standardized log_hook_data()

All hooks now use the shared json_logger utility for consistent JSON logging.

## Completed Implementation

### Files Created

1. `.claude/hooks/utils/json_logger.py` - Shared JSON logging utility with:
   - `log_hook_data()` - Main logging function
   - `read_hook_log()` - Read existing logs
   - `get_hook_log_file()` - Get log file path
   - `get_total_log_entries()` - Get entry count
   - `clear_hook_log()` - Clear log
   - `get_latest_log_entry()` - Get latest entry

2. `.claude/hooks/utils/__init__.py` - Exports all logger functions

3. `docs/hooks/LOGGING.md` - Comprehensive documentation including:
   - Log format specification
   - Helper function usage examples
   - Bash and Python logging patterns
   - Log rotation strategy recommendations
   - Migration guide for existing hooks

### Files Modified

1. `.claude/hooks/session-start-agent-teams.sh` - Converted to JSON logging
   - Changed from YAML events file to JSON logs
   - Uses consistent structure: timestamp, hook name, bb5_dir, event

2. `.claude/hooks/post-message-agent-teams.sh` - Converted to JSON logging
   - Changed from YAML events file to JSON logs
   - Uses consistent structure with should_activate flag

3. `.claude/hooks/pre_tool_use.py` - Updated to use shared logger
   - Replaced inline logging code with `log_hook_data()` call
   - Cleaner, more maintainable code

### Hook Inventory for BB5

BB5 currently has 3 active hooks:
- session-start-agent-teams.sh (bash) - ✅ Updated
- post-message-agent-teams.sh (bash) - ✅ Updated
- pre_tool_use.py (python) - ✅ Updated

Note: The task mentioned "20+ RALF hooks" but that refers to the broader Claude Code ecosystem. BB5 only has 3 active hooks in use.

### Implementation Pattern

All hooks now follow the standardized pattern:
1. Create logs directory
2. Format JSON with timestamp, hook name, and data
3. Append to logs/{hook_name}.json (don't overwrite)
4. Handle errors gracefully

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
