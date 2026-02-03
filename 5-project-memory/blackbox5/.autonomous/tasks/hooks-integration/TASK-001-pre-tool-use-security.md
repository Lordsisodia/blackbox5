# TASK-001: Implement Pre-Tool-Use Security Hook

**Status**: pending
**Priority**: CRITICAL
**Created**: 2026-02-03
**Source**: claude-code-hooks-mastery analysis

## Objective

Implement pre_tool_use hook with security blocking for dangerous commands (rm -rf) and sensitive file access (.env).

## Background

From claude-code-hooks-mastery analysis, the pre_tool_use hook can block dangerous operations by returning exit code 2. This is critical for autonomous systems to prevent accidental data loss.

## Success Criteria

- [ ] Hook blocks `rm -rf` commands with comprehensive pattern matching
- [ ] Hook blocks `.env` file access (but allows `.env.sample`)
- [ ] Hook logs all tool calls to JSON
- [ ] Hook returns proper exit code 2 with error message
- [ ] Hook tested with dangerous commands
- [ ] Hook tested with safe commands (no blocking)

## Implementation Details

### Pattern to Block (from mastery)

```python
dangerous_patterns = [
    r'\brm\s+.*-[a-z]*r[a-z]*f',  # rm -rf, rm -fr, rm -Rf
    r'\brm\s+--recursive\s+--force',
    r'\brm\s+--force\s+--recursive',
    r'\brm\s+-r\s+.*-f',
    r'\brm\s+-f\s+.*-r',
]
```

### Exit Code Semantics

- `exit 0` = Allow tool execution
- `exit 2` = Block tool with error message to stderr

### File Location

`.claude/hooks/pre_tool_use.py`

## Rollback Strategy

1. Rename hook file to disable
2. Test without hook
3. Fix and re-enable

## Related

- Source: `6-roadmap/.research/external/GitHub/Claude-Code/data/repos/claude-code-hooks-mastery/.claude/hooks/pre_tool_use.py`
- Analysis: `6-roadmap/.research/external/GitHub/Claude-Code/extracted/repos/RALF-HOOKS-ANALYSIS.md`
