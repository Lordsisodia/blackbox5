# IMP-1769903002: Make Pre-Execution Research Mandatory

**Type:** implement
**Priority:** high
**Category:** process
**Source Learning:** L-1769813746-003, L-1769800330-003, L-1769808838-001, L-1769807450-002, L-run-integration-test-L3
**Status:** pending
**Created:** 2026-02-01T13:30:00Z

---

## Objective

Make pre-execution research a mandatory step for all task types to prevent duplicate work and validate assumptions.

## Problem Statement

Pre-execution research is optional but consistently proves valuable:
- Prevents duplicate work (8+ learnings)
- Identifies actual vs documented state
- Saves significant time
- Currently not enforced

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

## Related Learnings

- run-1769813746: "Pre-Execution Research Value"
- run-1769800330: "Pre-Execution Research Prevents Duplication"
- run-1769808838: "Pre-execution research is valuable"
- run-1769807450: "Pre-Execution Research Value"
- run-integration-test: "Research Before Execution"

## Estimated Effort

35 minutes

## Acceptance Criteria

- [ ] Research phase added to all task execution paths
- [ ] Template updated with research section
- [ ] Duplicate detection integrated
- [ ] Validation prevents skipping research
- [ ] Tested with 3+ tasks
