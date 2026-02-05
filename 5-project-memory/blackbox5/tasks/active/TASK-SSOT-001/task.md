# TASK-SSOT-001: Consolidate Skill Metrics Files

**Status:** pending
**Priority:** CRITICAL
**Created:** 2026-02-06
**Parent:** Issue #12 - SSOT Configuration Violations

## Objective
Merge skill-metrics.yaml, skill-usage.yaml, and .autonomous/operations/skill-usage.yaml into a single canonical skill-registry.yaml file.

## Success Criteria
- [ ] Create unified skill-registry.yaml with all skill data
- [ ] Merge effectiveness scores from skill-metrics.yaml
- [ ] Merge usage tracking from skill-usage.yaml
- [ ] Delete duplicate .autonomous/operations/skill-usage.yaml
- [ ] Update all references to use new registry
- [ ] Document the new schema

## Context
Same skill information exists in 3 files with different schemas:
- skill-metrics.yaml tracks effectiveness_score, roi_calculation
- skill-usage.yaml tracks usage_count, success_count, trigger_accuracy
- .autonomous/operations/skill-usage.yaml has entirely different categories

## Approach
1. Analyze all three files to understand schemas
2. Design unified schema that includes all fields
3. Create skill-registry.yaml with merged data
4. Update scripts that read skill data
5. Delete old files after verification

## Related Files
- operations/skill-metrics.yaml
- operations/skill-usage.yaml
- .autonomous/operations/skill-usage.yaml
- CLAUDE.md (references skill data)

## Rollback Strategy
Keep backup of all three files before merging. Can restore if issues found.
