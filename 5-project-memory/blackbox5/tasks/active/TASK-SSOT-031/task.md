# TASK-SSOT-031: Consolidate Skill Metrics into Single Registry

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 70

---

## Objective

Consolidate fragmented skill metrics from multiple files into a single unified skill registry to eliminate data fragmentation, reduce update inconsistency, and simplify maintenance.

---

## Success Criteria

- [ ] Unified `skill-registry.yaml` created with comprehensive schema
- [ ] All data migrated from `skill-metrics.yaml`, `skill-usage.yaml`, `skill-selection.yaml`, and `improvement-metrics.yaml`
- [ ] All code references updated to use new registry
- [ ] Old files deprecated with clear migration notices
- [ ] Documentation updated to reflect new single registry pattern

---

## Context

Skill metrics are currently fragmented across 4 separate files:
- `operations/skill-metrics.yaml` - Effectiveness scores
- `operations/skill-usage.yaml` - Usage patterns
- `operations/skill-selection.yaml` - Selection criteria
- `operations/improvement-metrics.yaml` - Improvement tracking

This fragmentation creates:
1. **Data Fragmentation**: Related data scattered across different files
2. **Update Inconsistency**: Must update multiple files for single skill changes
3. **Query Complexity**: Need to manually join data from multiple sources
4. **Maintenance Overhead**: 4 files to maintain instead of 1

---

## Approach

### Phase 1: Create Unified Schema (1 hour)
1. Design comprehensive skill schema including metadata, selection criteria, metrics, usage history, and improvements
2. Ensure all current fields are included
3. Plan for future extensions

### Phase 2: Create Migration Script (1 hour)
1. Build Python script to merge data from all 4 source files
2. Handle missing or inconsistent data gracefully
3. Validate merged data integrity

### Phase 3: Update References (1 hour)
1. Update skill selection logic
2. Update metrics collection code
3. Update dashboard queries

### Phase 4: Deprecate Old Files (1 hour)
1. Add deprecation notices to old files
2. Create symlinks if backward compatibility needed
3. Update all documentation

---

## Rollback Strategy

If issues arise:
1. Keep old files until migration is fully validated
2. Restore old file references if new registry causes failures
3. Document any data loss during rollback

---

## Notes

**Key Insight:** The unified registry should follow first principles:
- Single Source of Truth: One canonical location for all skill data
- Convention over Configuration: Consistent schema for all skills
- Minimal Viable Documentation: Only fields that provide value
- Hierarchy of Information: Clear structure from metadata to metrics
