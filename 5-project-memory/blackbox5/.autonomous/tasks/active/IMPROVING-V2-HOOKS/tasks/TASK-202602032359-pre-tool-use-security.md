# TASK-202602032359: Implement Pre-Tool-Use Security Hook

**Task ID:** TASK-202602032359
**Type:** implement
**Priority:** critical
**Status:** completed
**Created:** 2026-02-03T23:59:00Z
**Estimated Lines:** 150
**Completed:** 2026-02-10T03:49:00Z

---

## Summary

Implemented pre_tool_use security hook for BlackBox5 with:

1. **pre_tool_use.py** - Main hook blocking dangerous rm -rf commands and .env file access
   - Comprehensive rm -rf pattern matching (7+ variations)
   - Dangerous path detection (/, ~, $HOME, wildcards)
   - .env file blocking (except .env.sample)
   - JSON logging to logs/pre_tool_use.json
   - Exit code 2 blocking behavior

2. **security_patterns.py** - Shared utility module with reusable patterns
   - is_dangerous_rm_command() function
   - is_env_file_access() function
   - Pattern constants for future hook integration

3. **settings.json** - Hook registration
   - Pre_tool_use hook enabled by default

4. **SECURITY.md** - Complete documentation
   - Usage guide
   - Testing procedures
   - Rollback instructions

---

## Testing Results

**Dangerous Commands (Blocked):**
- rm -rf / → Exit 2
- rm -fr folder → Exit 2
- cat .env → Exit 2

**Safe Commands (Allowed):**
- rm -r mydir → Exit 0
- rm file.txt → Exit 0
- cat .env.sample → Exit 0

**Success Criteria Met:**
- [x] Hook blocks rm -rf commands with comprehensive pattern matching
- [x] Hook blocks .env file access (but allows .env.sample)
- [x] Hook logs all tool calls to JSON (logs/pre_tool_use.json)
- [x] Hook returns proper exit code 2 with error message to stderr
- [x] Hook tested with dangerous commands (should block)
- [x] Hook tested with safe commands (should allow)
- [x] Hook integrated with BB5 settings.json
- [x] Documentation updated

---

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

### Exit Code Semantics for Autonomous Systems

- `exit 0` = Allow tool execution
- `exit 2` = Block tool with error message to stderr

### File Location

`.claude/hooks/pre_tool_use.py`

---

## Files to Create/Modify

**New Files:**
- `.claude/hooks/pre_tool_use.py` - Security hook implementation
- `.claude/hooks/utils/security_patterns.py` - Shared security patterns

**Modified Files:**
- `.claude/settings.json` - Register hook
- `docs/hooks/SECURITY.md` - Documentation

---

## Rollback Strategy

1. Rename hook file to `.claude/hooks/pre_tool_use.py.disabled` to disable
2. Test without hook
3. Fix issues
4. Re-enable by removing `.disabled` suffix

---

## Dependencies

- [ ] Analysis: Review claude-code-hooks-mastery pre_tool_use.py
- [ ] Decision: Confirm exit code 2 blocking behavior

---

## Related

- Source: `6-roadmap/.research/external/GitHub/Claude-Code/data/repos/claude-code-hooks-mastery/.claude/hooks/pre_tool_use.py`
- Analysis: `6-roadmap/.research/external/GitHub/Claude-Code/extracted/repos/RALF-HOOKS-ANALYSIS.md`
- Integration Plan: `5-project-memory/blackbox5/.autonomous/tasks/hooks-integration/HOOKS-INTEGRATION-PLAN.md`

---

## Notes

**Why This is Critical:**
RALF is an autonomous system. Without security hooks, agents could accidentally execute dangerous commands. The mastery repo shows this pattern working in production.

**Exit Code 2 Pattern:**
```python
print("BLOCKED: Dangerous command detected", file=sys.stderr)
sys.exit(2)  # Blocks tool and shows error to Claude
```
