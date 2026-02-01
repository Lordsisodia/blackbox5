# IMP-1769903008: Add Shellcheck to CI/CD Pipeline

**Type:** implement
**Priority:** low
**Category:** infrastructure
**Source Learning:** L-20260131-060616-004
**Status:** pending
**Created:** 2026-02-01T13:30:00Z

---

## Objective

Integrate shellcheck into the CI/CD pipeline to catch shell script syntax errors before deployment.

## Problem Statement

Shell script errors are silent until execution:
- Dashboard had `echo "$line" jq` instead of `echo "$line" | jq`
- Error prevented recent activity display
- No automated catching of syntax errors

## Success Criteria

- [ ] Shellcheck integrated into CI/CD
- [ ] All shell scripts pass shellcheck
- [ ] CI fails on shellcheck warnings
- [ ] Documentation of shell script standards
- [ ] Pre-commit hook option for local checking

## Approach

1. Add shellcheck to CI configuration
2. Fix existing shellcheck warnings
3. Create shell script standards doc
4. Add optional pre-commit hook
5. Test CI integration

## Files to Modify

- `.github/workflows/ci.yml` or equivalent
- Shell scripts with warnings (fix)
- `.docs/shell-script-standards.md` (create)
- `2-engine/.autonomous/hooks/pre-commit-shellcheck` (create)

## Related Learnings

- run-20260131-060616: "Dashboard Syntax Error Impact"

## Estimated Effort

40 minutes

## Acceptance Criteria

- [ ] CI runs shellcheck on all .sh files
- [ ] All existing scripts pass
- [ ] Standards documented
- [ ] Pre-commit hook available
- [ ] CI fails on shellcheck errors
