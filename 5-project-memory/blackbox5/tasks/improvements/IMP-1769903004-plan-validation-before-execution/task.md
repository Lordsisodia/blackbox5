# IMP-1769903004: Implement Plan Validation Before Execution

**Type:** implement
**Priority:** medium
**Category:** process
**Source Learning:** L-1769859012-003, L-20260131-060933-L003, L-1769807450-001
**Status:** pending
**Created:** 2026-02-01T13:30:00Z

---

## Objective

Create a plan validation system that checks if referenced files exist and problems are still valid before marking plans as "ready_to_start".

## Problem Statement

Plans frequently reference non-existent code or describe already-resolved issues:
- PLAN-004 referenced outdated codebase structure
- Plans describe problems that don't exist at that scale
- No validation before execution starts
- Wasted effort on invalid plans

## Success Criteria

- [ ] Plan validation script created
- [ ] Checks all files_to_change exist
- [ ] Verifies problem statement against current codebase
- [ ] Integration with plan status workflow
- [ ] Auto-fail plans with invalid references

## Approach

1. Create `lib/plan_validator.py`
2. Implement file existence checks
3. Add problem statement validation
4. Integrate into plan approval workflow
5. Create validation report format

## Files to Modify

- `2-engine/.autonomous/lib/plan_validator.py` (create)
- `2-engine/.autonomous/workflows/plan-approval.yaml`
- `plans/.docs/plan-validation-guide.md` (create)

## Related Learnings

- run-1769859012: "Plans Can Become Stale"
- run-20260131-060933: "Plans Can Reference Non-Existent Code"
- run-1769807450: "Roadmap State Decay"

## Estimated Effort

40 minutes

## Acceptance Criteria

- [ ] Validator checks file existence
- [ ] Validator flags stale problem statements
- [ ] Integrated into plan workflow
- [ ] Validation reports generated
- [ ] Invalid plans marked appropriately
