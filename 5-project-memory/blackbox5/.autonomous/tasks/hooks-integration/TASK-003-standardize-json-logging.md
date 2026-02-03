# TASK-003: Standardize JSON Logging Across All Hooks

**Status**: pending
**Priority**: HIGH
**Created**: 2026-02-03
**Source**: claude-code-hooks-mastery analysis

## Objective

Standardize all RALF hooks to use consistent JSON logging pattern.

## Background

Hooks mastery uses consistent JSON logging pattern across all hooks. RALF has mixed logging (some text, some JSON).

## Success Criteria

- [ ] All hooks log to `logs/{hook_name}.json`
- [ ] All hooks use consistent JSON structure
- [ ] All hooks append to existing logs
- [ ] Log rotation considered
- [ ] Documentation updated

## Implementation Details

### Standard Pattern

```python
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / 'hook_name.json'

# Read existing or init empty
if log_file.exists():
    with open(log_file, 'r') as f:
        log_data = json.load(f)
else:
    log_data = []

# Append and write
log_data.append(input_data)
with open(log_file, 'w') as f:
    json.dump(log_data, f, indent=2)
```

### Hooks to Update

1. `inject-session-context.sh` - Convert to JSON logging
2. `checkpoint-auto-save.sh` - Already JSON, verify consistency
3. Any other active hooks

## Rollback Strategy

1. Keep text logs as backup
2. Implement JSON logging
3. Verify both work during transition

## Related

- Analysis: `6-roadmap/.research/external/GitHub/Claude-Code/extracted/repos/RALF-HOOKS-ANALYSIS.md`
