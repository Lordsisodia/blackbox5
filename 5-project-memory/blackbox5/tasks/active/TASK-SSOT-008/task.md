# TASK-SSOT-008: Fix Goal/Status Mismatches

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #15 - SSOT Goals/Plans Violations

## Objective
Fix status mismatches between goal.yaml files and INDEX.yaml. Establish goal.yaml as canonical source.

## Success Criteria
- [ ] Fix IG-008: Change goal.yaml status from "draft" to "completed" (or actual status)
- [ ] Fix IG-009: Update INDEX.yaml to match goal.yaml "completed" status
- [ ] Update INDEX.yaml progress to match goal.yaml
- [ ] Remove status/progress from INDEX.yaml (make it derived)
- [ ] Create script to auto-generate INDEX.yaml from goal files
- [ ] Add "last_synced" timestamp

## Context
Specific mismatches found:
- IG-008: goal.yaml shows `draft`, INDEX.yaml shows `in_progress`
- IG-009: goal.yaml shows `completed`, INDEX.yaml shows `in_progress`
- Progress percentages also differ

## Approach
1. Audit all goal.yaml vs INDEX.yaml entries
2. Update mismatched entries
3. Create INDEX.yaml generator script
4. Remove duplicate data from INDEX.yaml
5. Add sync verification

## Related Files
- goals/active/IG-008/goal.yaml
- goals/active/IG-009/goal.yaml
- goals/INDEX.yaml
- goals/goals.yaml

## Rollback Strategy
Keep backup of INDEX.yaml before changes.
