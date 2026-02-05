# TASK-SSOT-005: Consolidate security_checks.json to Single Location

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #16 - SSOT Metrics/Monitoring Violations

## Objective
Consolidate all 6 security_checks.json files into a single canonical location.

## Success Criteria
- [ ] Identify all 6 security_checks.json locations
- [ ] Choose canonical location: .logs/security_checks.json (project root)
- [ ] Merge data from all locations (if different)
- [ ] Update all scripts to write to canonical location
- [ ] Delete duplicate files
- [ ] Create symlinks if cross-project sharing needed

## Context
security_checks.json exists in 6 locations:
1. tasks/active/.logs/security_checks.json
2. runs/.logs/security_checks.json
3. .logs/security_checks.json (canonical)
4. 6-roadmap/research/external/YouTube/AI-Improvement-Research/.logs/security_checks.json
5. 2-engine/.logs/security_checks.json
6. .logs/security_checks.json (root)

## Approach
1. Find all security_checks.json files
2. Compare contents, merge if needed
3. Update scripts that write security checks
4. Delete duplicates after verification
5. Document the canonical location

## Related Files
- All scripts that perform security checks
- .logs/ directory structure

## Rollback Strategy
Keep backups of all files until verification complete.
