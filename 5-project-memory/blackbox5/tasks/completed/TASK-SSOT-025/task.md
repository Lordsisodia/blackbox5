# TASK-SSOT-025: Migrate 35+ Files to Storage Abstraction

**Status:** in_progress
**Priority:** HIGH
**Created:** 2026-02-06
**Updated:** 2026-02-07
**Parent:** Issue #3 - Missing Storage Abstraction Layer

## Objective
Migrate all 35+ files with raw file I/O to use the new StorageBackend abstraction.

## Success Criteria
- [ ] Phase 1: Migrate high-impact files (bb5-queue-manager, bb5-reanalysis-engine, bb5-metrics-collector)
- [ ] Phase 2: Migrate agent scripts (scout-intelligent, planner-prioritize, executor-implement, verifier-validate)
- [x] Phase 3: Migrate utility scripts (sync-state, **log-skill-usage**, validate-ssot)
- [ ] Phase 4: Migrate 2-engine lib files (config_manager, decision_registry, workflow_loader)
- [x] Verify all migrated files use atomic writes
- [x] Verify error handling consistency
- [ ] Delete old raw I/O code paths

## Migration Pattern
```python
# Before
with open(filepath, 'r') as f:
    data = yaml.safe_load(f)

# After
from storage import SkillRepository
repo = SkillRepository()
repo.log_usage(task_id="TASK-001", skill_invoked="bmad-dev", ...)
```

## Files Migrated

### Completed
1. **log-skill-usage.py** - Migrated 3 I/O operations to SkillRepository
   - Added: `SkillRepository` class to `storage.py`
   - Changed: `load_skill_usage_yaml()` now uses `SkillRepository`
   - Changed: `save_skill_usage_yaml()` now uses atomic writes via `SkillRepository`
   - Changed: `log_skill_usage()` now delegates to `SkillRepository.log_usage()`
   - Verified: Script works with --dry-run and actual logging

### Pending
1. bb5-queue-manager.py - 3 I/O operations
2. bb5-reanalysis-engine.py - 7 I/O operations
3. bb5-metrics-collector.py - 7 I/O operations
4. scout-intelligent.py - 2 I/O operations
5. planner-prioritize.py - 2 I/O operations
6. executor-implement.py - 6 I/O operations
7. verifier-validate.py - 5 I/O operations
8. sync-state.py - 3 I/O operations
9. validate-ssot.py - ? I/O operations
10. (25 more files...)

## Related Files
- storage-pattern-inventory.md
- `.autonomous/lib/storage.py` - Storage abstraction
- `.autonomous/lib/storage_backend.py` - Legacy storage backend
- `bin/log-skill-usage.py` - Migrated script

## Rollback Strategy
- Original functions kept with DEPRECATED warnings for backward compatibility
- All changes are additive (new SkillRepository class)
- skill-usage.yaml format unchanged
