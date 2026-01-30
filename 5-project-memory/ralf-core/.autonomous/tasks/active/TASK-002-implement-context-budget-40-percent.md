# TASK-002: Implement 40% Context Budget Threshold

**Status:** pending
**Priority:** HIGH
**Created:** 2026-01-30
**Agent:** Agent-2.3
**Project:** RALF-CORE

---

## Objective

Implement and test the 40% context budget threshold that triggers sub-agent delegation.

## Background

Agent-2.3 introduces early delegation at 40% context usage (80,000 tokens) instead of waiting until 85%. This keeps the main agent's context pristine and improves overall quality.

## Success Criteria

- [ ] Update `context_budget.py` to accept `--subagent-threshold 40` parameter
- [ ] Implement sub-agent spawning logic at 40% threshold
- [ ] Create sub-agent context compression (task-only context)
- [ ] Test delegation with a complex task
- [ ] Document the sub-agent pattern

## Technical Details

Current context budget:
- Max: 200,000 tokens
- Warning: 70% (140,000)
- Critical: 85% (170,000)
- Hard limit: 95% (190,000)

New threshold:
- Sub-agent: 40% (80,000) - NEW
- Warning: 70% (140,000)
- Critical: 85% (170,000)
- Hard limit: 95% (190,000)

## Approach

1. Modify `/Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5/2-engine/.autonomous/lib/context_budget.py`
2. Add sub-agent threshold parameter
3. Implement delegation logic
4. Test with a task that consumes context quickly
5. Verify main agent stays under 40%

## Files to Modify

- `/Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5/2-engine/.autonomous/lib/context_budget.py`
- May need new: `/Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5/2-engine/.autonomous/lib/subagent_spawner.py`

## Risk Level

MEDIUM - Modifies core context management

## Rollback Strategy

Revert to original context_budget.py if issues arise
