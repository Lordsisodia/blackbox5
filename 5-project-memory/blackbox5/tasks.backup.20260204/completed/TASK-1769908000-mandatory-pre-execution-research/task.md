# TASK-1769908000: Make Pre-Execution Research Mandatory

**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T14:30:00Z
**Source:** IMP-1769903002 (Improvement Backlog)

## Objective

Make pre-execution research a mandatory step for all task types to prevent duplicate work and validate assumptions.

## Context

Pre-execution research is currently optional but consistently proves valuable across 8+ learnings. It prevents duplicate work, identifies actual vs documented state, and saves significant time. This task implements mandatory research phase in the RALF executor workflow.

Source learnings:
- L-1769813746-003: "Pre-Execution Research Value"
- L-1769800330-003: "Pre-Execution Research Prevents Duplication"
- L-1769808838-001: "Pre-execution research is valuable"
- L-1769807450-002: "Pre-Execution Research Value"
- L-run-integration-test-L3: "Research Before Execution"

## Success Criteria

- [ ] Pre-execution research required in task execution workflow
- [ ] Research sub-agent spawned automatically before execution
- [ ] Research findings documented in THOUGHTS.md
- [ ] Duplicate detection integrated into research phase
- [ ] Cannot proceed to execution without research completion

## Approach

1. Update RALF executor prompt to require research
2. Add research phase to task lifecycle
3. Create research findings template
4. Integrate duplicate detection into research
5. Add research validation checkpoint

## Files to Modify

- `2-engine/.autonomous/prompts/ralf-executor.md`
- `2-engine/.autonomous/workflows/task-execution.yaml`
- `.templates/tasks/THOUGHTS.md.template` (add research section)

## Notes

This improvement addresses one of the most frequently mentioned issues in learnings: lack of pre-execution research leading to duplicate work and wasted effort.

## Rollback Strategy

If issues arise:
1. Revert changes to executor prompt
2. Remove research validation checkpoint
3. Restore previous THOUGHTS.md.template
