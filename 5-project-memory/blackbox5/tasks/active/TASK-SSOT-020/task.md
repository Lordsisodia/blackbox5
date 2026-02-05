# TASK-SSOT-020: Create Single Timeline Source

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Parent:** Issue #15 - SSOT Goals/Plans Violations

## Objective
Consolidate timeline data. Either root timeline.yaml is canonical OR goal-specific timelines are views.

## Success Criteria:
- [ ] Decide canonical timeline source (recommend: root timeline.yaml)
- [ ] Merge goal-specific timeline events to root
- [ ] Make goal timelines as filtered views
- [ ] Delete duplicate events from goal timelines
- [ ] Create timeline query/filter system
- [ ] Document timeline architecture

## Context
Timeline data in multiple places:
- Root timeline.yaml (1500+ lines)
- goals/active/IG-001/timeline.yaml
- goals/active/IG-006/timeline.yaml
- etc. (8+ goal timelines)

Same events logged in both root and goal timelines.

## Approach:
1. Audit all timeline files
2. Choose canonical source (root timeline.yaml)
3. Merge goal events to root
4. Create view/filter system for goal timelines
5. Document architecture

## Related Files:
- timeline.yaml
- goals/active/IG-*/timeline.yaml

## Rollback Strategy:
Keep goal timelines until view system working.
