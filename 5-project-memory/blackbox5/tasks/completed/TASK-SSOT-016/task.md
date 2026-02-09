# TASK-SSOT-016: Consolidate Events to Single events.yaml

**Status:** completed
**Completed:** 2026-02-07
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #19 - SSOT Hooks/Triggers Violations

## Objective
Merge all 5+ events.yaml files into single canonical location. Make timeline.yaml a derived view.

## Success Criteria
- [ ] Identify all events.yaml files (5+ locations)
- [ ] Choose canonical: .autonomous/agents/communications/events.yaml
- [ ] Merge events from all sources
- [ ] Delete duplicate events.yaml files
- [ ] Update timeline.yaml to be derived from events
- [ ] Standardize event format across all sources

## Context
Events stored in 5+ files:
- .autonomous/agents/communications/events.yaml (530+ events, canonical)
- events.yaml (root) - duplicate?
- 2-engine/.autonomous/events.yaml - separate
- goals/active/*/events.yaml - 8+ files
- timeline.yaml - overlapping content

## Approach
1. Find all events.yaml files
2. Compare and merge contents
3. Choose canonical location
4. Delete duplicates
5. Update timeline generation

## Related Files
- .autonomous/agents/communications/events.yaml
- events.yaml (root)
- 2-engine/.autonomous/events.yaml
- timeline.yaml

## Rollback Strategy
Keep backups until merge verified.
