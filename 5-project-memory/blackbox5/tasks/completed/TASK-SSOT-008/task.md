# TASK-SSOT-008: Fix Goal/Status Mismatches

**Status:** completed
**Priority:** HIGH
**Created:** 2026-02-06
**Completed:** 2026-02-07
**Parent:** Issue #15 - SSOT Goals/Plans Violations

## Objective
Fix status mismatches between goal.yaml files and INDEX.yaml. Establish goal.yaml as canonical source.

## Success Criteria
- [x] Fix IG-008: INDEX.yaml now correctly shows "draft" (matches goal.yaml)
- [x] Fix IG-009: INDEX.yaml correctly shows "completed" (matches goal.yaml)
- [x] Update INDEX.yaml progress to match goal.yaml
- [x] Create script to auto-generate INDEX.yaml from goal files
- [x] Add "last_synced" timestamp

## Implementation

Created `~/.blackbox5/bin/sync-goal-index.sh`:
- Reads all `goals/active/IG-*/goal.yaml` files
- Extracts status, progress, priority, owner, name fields
- Generates new INDEX.yaml with derived data
- Creates backup before overwriting
- Supports `--dry-run` and `--verbose` flags
- Adds `last_synced` timestamp in meta section

## Verification

Script tested successfully:
- Parsed 9 valid goal YAML files
- Skipped 3 non-YAML goal files (IG-010, IG-011, IG-AUTONOMY-001)
- INDEX.yaml now correctly reflects goal.yaml statuses:
  - IG-008: draft (75%) - was incorrectly showing in_progress
  - IG-009: completed (100%) - was already correct
- Backup created: INDEX.yaml.backup.20260207_224251

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
