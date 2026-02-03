# TASK-002: Enhance SessionStart Hook

**Status**: pending
**Priority**: HIGH
**Created**: 2026-02-03
**Source**: claude-code-hooks-mastery analysis

## Objective

Enhance existing SessionStart hook with git status, context file loading, and JSON logging.

## Background

Current RALF SessionStart is basic. Hooks mastery shows comprehensive session initialization including git status, context files, and TTS.

## Success Criteria

- [ ] Hook gets git branch and uncommitted changes count
- [ ] Hook loads `.claude/CONTEXT.md` if exists
- [ ] Hook loads `.claude/TODO.md` if exists
- [ ] Hook loads `TODO.md` if exists
- [ ] Hook returns `additionalContext` to Claude
- [ ] Hook logs to JSON
- [ ] Hook tested in fresh session
- [ ] Hook tested in resumed session

## Implementation Details

### Git Status Integration

```python
def get_git_status():
    branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    changes = subprocess.run(['git', 'status', '--porcelain'])
    return branch, len(changes)
```

### Context Files to Load

1. `.claude/CONTEXT.md`
2. `.claude/TODO.md`
3. `TODO.md`

### Return Format

```python
output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context
    }
}
print(json.dumps(output))
```

## Rollback Strategy

1. Keep original hook as backup
2. Test enhanced version
3. Restore original if issues

## Related

- Source: `6-roadmap/.research/external/GitHub/Claude-Code/data/repos/claude-code-hooks-mastery/.claude/hooks/session_start.py`
- Analysis: `6-roadmap/.research/external/GitHub/Claude-Code/extracted/repos/RALF-HOOKS-ANALYSIS.md`
