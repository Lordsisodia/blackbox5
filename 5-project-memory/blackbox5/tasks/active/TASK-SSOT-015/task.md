# TASK-SSOT-015: Create Central Trigger Rules Configuration

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Parent:** Issue #19 - SSOT Hooks/Triggers Violations

## Objective
Create single trigger-rules.yaml file. Remove duplicate trigger rules from CLAUDE.md and scripts.

## Success Criteria
- [ ] Create operations/trigger-rules.yaml
- [ ] Extract rules from CLAUDE.md
- [ ] Extract rules from skill-selection.yaml
- [ ] Extract rules from bin/bb5-* scripts
- [ ] Update CLAUDE.md to reference trigger-rules.yaml
- [ ] Update scripts to load rules from file

## Context
Trigger rules defined in 3+ places:
- CLAUDE.md: Auto-trigger rules table
- skill-selection.yaml: Domain mapping triggers
- bin/bb5-* scripts: Inline trigger logic

## Approach
1. Audit all trigger rule locations
2. Design unified trigger-rules.yaml schema
3. Create central file
4. Update CLAUDE.md (reference only)
5. Update scripts to load from file

## Related Files
- CLAUDE.md
- operations/skill-selection.yaml
- bin/bb5-* scripts

## Rollback Strategy
Keep original files until new system verified.
