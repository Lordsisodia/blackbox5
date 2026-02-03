# TASK-20260203171821: Enhance SessionStart Hook with Git Status and Context Loading

**Task ID:** TASK-20260203171821
**Type:** enhance
**Priority:** high
**Status:** pending
**Created:** 2026-02-03T17:18:21Z
**Estimated Lines:** 200

---

## Objective

Enhance existing SessionStart hook with git status, context file loading, and JSON logging based on patterns from claude-code-hooks-mastery.

---

## Context

Current RALF SessionStart is basic. Hooks mastery shows comprehensive session initialization including git status, context files loading (.claude/CONTEXT.md, TODO.md), and returning additionalContext to Claude.

From analysis: "session_start.py - Much more sophisticated than our current hook: Logs to JSON, Gets git status (branch, uncommitted changes), Fetches recent GitHub issues via gh CLI, Loads context files, TTS announcement option, Returns additionalContext to Claude"

---

## Success Criteria

- [ ] Hook gets git branch and uncommitted changes count
- [ ] Hook loads `.claude/CONTEXT.md` if exists
- [ ] Hook loads `.claude/TODO.md` if exists
- [ ] Hook loads `TODO.md` if exists
- [ ] Hook returns `additionalContext` to Claude via JSON output
- [ ] Hook logs to JSON (`logs/session_start.json`)
- [ ] Hook tested in fresh session (source: startup)
- [ ] Hook tested in resumed session (source: resume)
- [ ] Hook tested after clear (source: clear)
- [ ] Documentation updated

---

## Implementation Details

### Git Status Integration

```python
def get_git_status():
    """Get current git status information."""
    branch_result = subprocess.run(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        capture_output=True, text=True, timeout=5
    )
    current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"

    status_result = subprocess.run(
        ['git', 'status', '--porcelain'],
        capture_output=True, text=True, timeout=5
    )
    if status_result.returncode == 0:
        changes = status_result.stdout.strip().split('\n') if status_result.stdout.strip() else []
        uncommitted_count = len(changes)
    else:
        uncommitted_count = 0

    return current_branch, uncommitted_count
```

### Context Files to Load

1. `.claude/CONTEXT.md` - Project context
2. `.claude/TODO.md` - Project todos
3. `TODO.md` - Root todos

### Return Format

```python
output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context
    }
}
print(json.dumps(output))
sys.exit(0)
```

---

## Files to Create/Modify

**New Files:**
- `.claude/hooks/session_start_enhanced.py` - Enhanced session start

**Modified Files:**
- `.claude/hooks/session_start.sh` - Keep as backup
- `.claude/settings.json` - Update hook registration
- `docs/hooks/SESSION_START.md` - Documentation

---

## Rollback Strategy

1. Keep original hook as `session_start.sh.backup`
2. Test enhanced version
3. If issues, restore original: `mv session_start.sh.backup session_start.sh`
4. Update settings.json to point to original

---

## Dependencies

- [ ] TASK-202602032359: Pre-Tool-Use Security Hook (for JSON logging pattern)
- [ ] Analysis: Review current session_start implementation
- [ ] Decision: Which context files to load

---

## Related

- Source: `6-roadmap/.research/external/GitHub/Claude-Code/data/repos/claude-code-hooks-mastery/.claude/hooks/session_start.py`
- Analysis: `6-roadmap/.research/external/GitHub/Claude-Code/extracted/repos/RALF-HOOKS-ANALYSIS.md`
- Integration Plan: `5-project-memory/blackbox5/.autonomous/tasks/hooks-integration/HOOKS-INTEGRATION-PLAN.md`

---

## Notes

**Why This Matters:**
Better context at session start = better autonomous decisions. The mastery repo shows this provides: git branch awareness, uncommitted changes count, project context from files, recent GitHub issues.

**additionalContext Feature:**
This is powerful - it injects context directly into Claude's prompt without user seeing it.

**Source Handling:**
SessionStart receives `source` field: "startup", "resume", or "clear". Handle each appropriately.
