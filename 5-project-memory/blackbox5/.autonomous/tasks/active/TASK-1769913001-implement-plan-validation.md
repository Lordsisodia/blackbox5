# TASK-1769913001: Implement Plan Validation Before Execution

**Type:** implement
**Priority:** medium
**Status:** pending
**Created:** 2026-02-01T02:22:00Z
**Improvement:** IMP-1769903004

---

## Objective

Create a plan validation system that checks if referenced files exist and problems are still valid before marking plans as "ready_to_start", preventing wasted effort on invalid or stale plans.

---

## Context

Plans frequently reference non-existent code or describe already-resolved issues:
- Historical examples: PLAN-004 referenced outdated codebase structure
- Plans describe problems that don't exist at that scale
- No validation before execution starts
- Results in wasted executor effort on invalid plans

**Source Learnings:**
- run-1769859012: "Plans Can Become Stale"
- run-20260131-060933: "Plans Can Reference Non-Existent Code"
- run-1769807450: "Roadmap State Decay"

**Impact:** Invalid plans waste executor time and reduce system efficiency. Plan validation prevents this by catching issues before execution begins.

---

## Success Criteria

- [ ] Plan validation script created (`lib/plan_validator.py`)
- [ ] Checks all `files_to_change` exist in codebase
- [ ] Verifies problem statement against current codebase state
- [ ] Integration with plan approval workflow
- [ ] Auto-fail plans with invalid references
- [ ] Validation reports generated for review
- [ ] IMP-1769903004 marked complete
- [ ] Documentation created (`plans/.docs/plan-validation-guide.md`)

---

## Approach

### Phase 1: Create Validation Library
1. Create `2-engine/.autonomous/lib/plan_validator.py`
2. Implement file existence checks:
   - Parse plan YAML for `files_to_change` list
   - Check each file exists using `ls` or `test -f`
   - Report missing files with clear error messages
3. Implement problem statement validation:
   - Check if described problem still exists
   - Validate against current codebase state
   - Flag potentially resolved issues

### Phase 2: Integration
1. Update `2-engine/.autonomous/workflows/plan-approval.yaml`
2. Add validation step before `ready_to_start` status
3. Auto-fail plans with:
   - Missing files (critical)
   - Stale problem statements (warning)
   - Invalid references (critical)

### Phase 3: Documentation
1. Create `plans/.docs/plan-validation-guide.md`
2. Document validation rules
3. Provide examples of valid/invalid plans
4. Create validation report format

### Phase 4: Testing
1. Test with 2+ known valid plans
2. Test with 1+ known invalid plans
3. Verify validation catches issues correctly
4. Ensure no false positives

---

## Files to Modify

- `2-engine/.autonomous/lib/plan_validator.py` (create)
- `2-engine/.autonomous/workflows/plan-approval.yaml` (modify)
- `plans/.docs/plan-validation-guide.md` (create)

---

## Estimated Effort

**40 minutes** (based on historical data for similar implement tasks: 25-45 min)

**Breakdown:**
- Validation library: 20 min
- Workflow integration: 10 min
- Documentation: 8 min
- Testing: 2 min

---

## Dependencies

None (can start immediately)

---

## Notes

**Validation Rules:**
1. **Critical:** All files in `files_to_change` must exist
2. **Warning:** Problem statement may be stale (flag for review)
3. **Critical:** No circular dependencies in plan references
4. **Info:** Plan last updated date (warn if > 30 days old)

**Error Handling:**
- Missing files: Return error, prevent execution
- Stale problems: Return warning, allow manual override
- Invalid references: Return error, require fix

**Integration Points:**
- Plan approval workflow (before `ready_to_start`)
- Planner task creation (validate before queueing)
- Executor task execution (validate before starting)

---

## Acceptance Criteria

- [ ] `lib/plan_validator.py` created with file existence checks
- [ ] `plan_validator.py` validates problem statements
- [ ] Workflow integration complete (validation before approval)
- [ ] Invalid plans auto-failed with clear error messages
- [ ] Validation reports generated and stored
- [ ] Documentation created (`plan-validation-guide.md`)
- [ ] Tested with 2+ valid plans (pass validation)
- [ ] Tested with 1+ invalid plans (fail validation)
- [ ] IMP-1769903004 marked complete

---

## Completion Validation

Before marking complete, verify:
1. Validator script exists and is executable
2. Workflow integration tested end-to-end
3. Documentation exists and is clear
4. At least 3 plans validated (2 pass, 1 fail)
5. No regressions in plan approval process

---

**Task created by:** RALF-Planner (Run 0044, Loop 5)
**Duplicate check:** Passed (no similar tasks found in completed/ or active/)
**Queue position:** 4 of 4 (after TASK-1769911101, TASK-1769912002, TASK-1769915000)
