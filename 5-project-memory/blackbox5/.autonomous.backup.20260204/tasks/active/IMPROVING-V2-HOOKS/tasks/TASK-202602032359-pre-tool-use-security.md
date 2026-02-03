# TASK-202602032359: Implement Pre-Tool-Use Security Hook

**Task ID:** TASK-202602032359
**Type:** implement
**Priority:** critical
**Status:** pending
**Created:** 2026-02-03T23:59:00Z
**Estimated Lines:** 150

---

## Objective

Implement pre_tool_use hook with security blocking for dangerous commands (rm -rf) and sensitive file access (.env), based on patterns from claude-code-hooks-mastery.

---

## Context

From analysis of claude-code-hooks-mastery (92/100 BB5 relevance), the pre_tool_use hook can block dangerous operations by returning exit code 2. This is critical for autonomous systems to prevent accidental data loss.

Current RALF has 20+ hooks but NO security blocking hook. This is a critical gap.

---

## Success Criteria

- [ ] Hook blocks `rm -rf` commands with comprehensive pattern matching
- [ ] Hook blocks `.env` file access (but allows `.env.sample`)
- [ ] Hook logs all tool calls to JSON (`logs/pre_tool_use.json`)
- [ ] Hook returns proper exit code 2 with error message to stderr
- [ ] Hook tested with dangerous commands (should block)
- [ ] Hook tested with safe commands (should allow)
- [ ] Hook integrated with BB5 settings.json
- [ ] Documentation updated

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
