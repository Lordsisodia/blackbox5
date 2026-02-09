# TASK-SSOT-020: Create Single Timeline Source

**Status:** completed
**Priority:** MEDIUM
**Created:** 2026-02-06
**Completed:** 2026-02-07
**Parent:** Issue #15 - SSOT Goals/Plans Violations

## Objective
Consolidate timeline data. Either root timeline.yaml is canonical OR goal-specific timelines are views.

## Success Criteria:
- [x] Decide canonical timeline source (recommend: root timeline.yaml)
- [x] Merge goal-specific timeline events to root
- [x] Make goal timelines as filtered views
- [x] Delete duplicate events from goal timelines
- [x] Create timeline query/filter system
- [x] Document timeline architecture

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

## Implementation Summary

### Approach Taken: Option C - Canonical Root with View Definitions

**Root timeline.yaml** is now the single source of truth.

### Changes Made:

1. **Merged 16 unique goal events** into root timeline.yaml:
   - IG-001 through IG-005: Goal creation events
   - IG-006: 4 events (creation, consolidation start, task migration, goals setup)
   - IG-008: 3 events (creation, research, plan created)
   - IG-009: 5 events (creation, 4 sub-goal completions)

2. **Converted 8 goal timelines** to view definitions:
   - `goals/active/IG-001/timeline.yaml` - View definition
   - `goals/active/IG-002/timeline.yaml` - View definition
   - `goals/active/IG-003/timeline.yaml` - View definition
   - `goals/active/IG-004/timeline.yaml` - View definition
   - `goals/active/IG-005/timeline.yaml` - View definition
   - `goals/active/IG-006/timeline.yaml` - View definition
   - `goals/active/IG-008/timeline.yaml` - View definition
   - `goals/active/IG-009/timeline.yaml` - View definition

3. **Created documentation**:
   - `.docs/timeline-architecture.md` - Complete architecture guide

### Query/Filter System:

```bash
# View events for a specific goal
grep -B 5 -A 10 "IG-001" ~/blackbox5/timeline.yaml

# View high-impact events
grep -B 2 -A 8 'impact: "high"' ~/blackbox5/timeline.yaml
```

### Files Modified:
- `~/blackbox5/timeline.yaml` - Added 16 goal events
- `~/blackbox5/goals/active/IG-*/timeline.yaml` - Converted to views (8 files)
- `~/blackbox5/.docs/timeline-architecture.md` - Created

## Related Files:
- timeline.yaml
- goals/active/IG-*/timeline.yaml
- .docs/timeline-architecture.md

## Rollback Strategy:
Goal timeline backups are in git history if needed. Root timeline additions are additive only.
