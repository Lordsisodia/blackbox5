# TASK-SSOT-011: Consolidate Hook Scripts to Single Directory

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Parent:** Issue #19 - SSOT Hooks/Triggers Violations

## Objective
Move all hook scripts from scattered locations into single .claude/hooks/ directory.

## Success Criteria
- [ ] Move 2-engine/.claude/hooks/* to .claude/hooks/
- [ ] Move .autonomous/memory/hooks/* to .claude/hooks/
- [ ] Resolve any naming conflicts
- [ ] Update .claude/settings.json hook paths
- [ ] Test all hooks still function
- [ ] Delete old hook directories

## Context
Hook scripts exist in 3+ locations:
- .claude/hooks/ - 15 hooks (main)
- 2-engine/.claude/hooks/ - 10 hooks (engine)
- .autonomous/memory/hooks/ - 3 hooks (wrong location)

## Approach
1. Inventory all hooks in all locations
2. Check for naming conflicts
3. Move engine hooks to main hooks/
4. Move memory hooks to main hooks/
5. Update settings.json
6. Test hook execution

## Related Files
- .claude/hooks/*
- 2-engine/.claude/hooks/*
- .autonomous/memory/hooks/*
- .claude/settings.json

## Rollback Strategy
Keep old directories until hooks verified working.
