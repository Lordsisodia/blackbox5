# TASK-20260203171822: Standardize JSON Logging Across All RALF Hooks

**Task ID:** TASK-20260203171822
**Type:** refactor
**Priority:** high
**Status:** pending
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
