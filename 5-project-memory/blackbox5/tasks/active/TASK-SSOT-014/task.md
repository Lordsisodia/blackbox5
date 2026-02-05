# TASK-SSOT-014: Standardize on YAML for Scout Reports

**Status:** pending
**Priority:** LOW
**Created:** 2026-02-06
**Parent:** Issue #14 - SSOT Knowledge Violations

## Objective
Choose YAML as canonical format for scout reports. Delete duplicate JSON files.

## Success Criteria
- [ ] Identify all scout reports with both JSON and YAML
- [ ] Choose YAML as canonical format
- [ ] Delete JSON duplicates
- [ ] Update any scripts that read JSON reports
- [ ] Document YAML as standard format

## Context
Each scout report exists in BOTH formats:
- scout-report-intelligent-20260205-013135.json
- scout-report-intelligent-20260205-013135.yaml

8 reports × 2 formats = 16 files for 8 reports' worth of data.

## Approach
1. Find all duplicate format files
2. Verify YAML files are complete
3. Delete JSON duplicates
4. Update any JSON-reading scripts

## Related Files
- .autonomous/analysis/scout-reports/*.json
- .autonomous/analysis/scout-reports/*.yaml
- Scripts that read these reports

## Rollback Strategy
JSON files can be regenerated if needed.
