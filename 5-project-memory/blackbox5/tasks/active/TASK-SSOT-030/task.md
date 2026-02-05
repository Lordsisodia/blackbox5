# TASK-SSOT-030: Migrate Extreme Complexity Files

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #3 - Missing Storage Abstraction Layer

## Objective
Migrate the 5 most complex files to storage abstraction layer.

## Success Criteria
- [ ] Phase 1: Migrate bb5-reanalysis-engine.py (EXTREME complexity)
- [ ] Phase 2: Migrate bb5-queue-manager.py (EXTREME complexity)
- [ ] Phase 3: Migrate roadmap_sync.py (HIGH complexity)
- [ ] Phase 4: Migrate bb5-metrics-collector.py (HIGH complexity)
- [ ] Phase 5: Migrate log-skill-usage.py (MEDIUM-HIGH complexity)
- [ ] Create migration tests for each file
- [ ] Verify no regression in functionality

## Context
Migration complexity analysis identified:
1. **bb5-reanalysis-engine.py** - 3-4 days, dual storage formats, complex serialization
2. **bb5-queue-manager.py** - 3-4 days, schema translation, format mismatch
3. **roadmap_sync.py** - 2-3 days, multi-entity sync, custom YAML headers
4. **bb5-metrics-collector.py** - 2-3 days, multi-format, event sourcing
5. **log-skill-usage.py** - 1-2 days, markdown parsing, aggregation

**Total effort: 12-18 days**

## Migration Order
1. Start with log-skill-usage.py (lowest risk)
2. Then bb5-metrics-collector.py
3. Then roadmap_sync.py
4. bb5-queue-manager.py (after schema unification)
5. bb5-reanalysis-engine.py (last, most complex)

## Related Files
- migration-complexity-hotspots.md
- All 5 files listed above

## Rollback Strategy
Keep backups of all files until migration verified.
