# TASK-1769915000: Add Shellcheck to CI/CD Pipeline

**Type:** implement
**Priority:** low
**Status:** pending
**Created:** 2026-02-01T12:20:00Z
**Source:** IMP-1769903008

## Objective

Integrate shellcheck into the CI/CD pipeline to catch shell script syntax errors before deployment.

## Context

Shell script errors are currently silent until execution. This improvement addresses the need for automated catching of syntax errors in shell scripts across the BlackBox5 repository.

## Success Criteria

- [ ] Shellcheck integrated into CI/CD (ci.yml)
- [ ] All shell scripts in bin/ pass shellcheck
- [ ] CI fails on shellcheck warnings
- [ ] Shell script standards documented
- [ ] Pre-commit hook option for local checking

## Approach

1. Add shellcheck job to .github/workflows/ci.yml
2. Run shellcheck on all .sh files in bin/ directory
3. Fix any existing shellcheck warnings
4. Create shell script standards documentation
5. Add optional pre-commit hook for local checking
6. Test CI integration

## Files to Modify

- `.github/workflows/ci.yml`: Add shellcheck job
- `bin/*.sh`: Fix any shellcheck warnings
- `operations/.docs/shell-script-standards.md`: Create documentation
- `.pre-commit-config.yaml`: Add shellcheck hook (optional)

## Shell Scripts to Check

- `bin/ralf-loop.sh`
- `bin/ralf-verify-run.sh`
- `bin/start.sh`
- `legacy-codespace-loop.sh`
- `5-project-memory/blackbox5/.autonomous/ralf-daemon.sh`

## Notes

- Shellcheck should be added as a separate job in CI
- Use `continue-on-error: true` initially if there are many warnings
- Focus on bin/ directory first, then expand to other scripts
- Document common patterns and standards for future scripts
