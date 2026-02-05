# TASK-SSOT-025: Migrate 35+ Files to Storage Abstraction

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #3 - Missing Storage Abstraction Layer

## Objective
Migrate all 35+ files with raw file I/O to use the new StorageBackend abstraction.

## Success Criteria
- [ ] Phase 1: Migrate high-impact files (bb5-queue-manager, bb5-reanalysis-engine, bb5-metrics-collector)
- [ ] Phase 2: Migrate agent scripts (scout-intelligent, planner-prioritize, executor-implement, verifier-validate)
- [ ] Phase 3: Migrate utility scripts (sync-state, log-skill-usage, validate-ssot)
- [ ] Phase 4: Migrate 2-engine lib files (config_manager, decision_registry, workflow_loader)
- [ ] Verify all migrated files use atomic writes
- [ ] Verify error handling consistency
- [ ] Delete old raw I/O code paths

## Migration Pattern
```python
# Before
with open(filepath, 'r') as f:
    data = yaml.safe_load(f)

# After
from storage.factory import StorageFactory
backend = StorageFactory.get_backend(filepath)
data = backend.load(filepath)
```

## Files to Migrate (Priority Order)
1. bb5-queue-manager.py - 3 I/O operations
2. bb5-reanalysis-engine.py - 7 I/O operations
3. bb5-metrics-collector.py - 7 I/O operations
4. scout-intelligent.py - 2 I/O operations
5. planner-prioritize.py - 2 I/O operations
6. executor-implement.py - 6 I/O operations
7. verifier-validate.py - 5 I/O operations
8. sync-state.py - 3 I/O operations
9. log-skill-usage.py - 3 I/O operations
10. (25 more files...)

## Related Files
- storage-pattern-inventory.md
- All 35+ files listed in inventory

## Rollback Strategy
Keep backups of all modified files until migration verified.
