# TASK-SSOT-033: Standardize Configuration Schema

**Status:** completed
**Priority:** MEDIUM
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 60

---

## Objective

Consolidate run folders from multiple locations into a single canonical location to eliminate data fragmentation and simplify run management.

---

## Success Criteria

- [ ] All run folders migrated to `5-project-memory/blackbox5/runs/`
- [ ] `2-engine/runs/` directory removed after migration
- [ ] All scripts updated to use canonical run path
- [ ] No broken references to old run locations
- [ ] Migration script created for future use

---

## Context

Run folders currently exist in multiple locations:
- `2-engine/runs/` - Engine runs
- `5-project-memory/blackbox5/runs/` - Project runs

This creates:
1. **Data Fragmentation**: Run data split across locations
2. **Query Complexity**: Finding runs requires checking both directories
3. **Inconsistent Structure**: Different naming conventions between locations
4. **Backup Issues**: Two places to manage for backups

Runs are project-specific and should live in the project directory.

---

## Approach

### Phase 1: Audit (30 min)
1. List all runs in `2-engine/runs/`
2. List all runs in `5-project-memory/blackbox5/runs/`
3. Identify duplicates and unique runs
4. Document naming convention differences

### Phase 2: Migration (1 hour)
1. Create migration script to copy unique runs
2. Handle naming conflicts (append suffix if needed)
3. Verify data integrity after copy
4. Log all migrations

### Phase 3: Update Scripts (1 hour)
1. Update all scripts that reference `2-engine/runs/`
2. Use `get_project_path() + "/runs/"` pattern instead
3. Test all affected scripts

### Phase 4: Cleanup (30 min)
1. Remove `2-engine/runs/` directory
2. Update `.gitignore` if needed
3. Update documentation with new canonical location

---

## Rollback Strategy

If migration issues occur:
1. Keep backup of `2-engine/runs/` until validated
2. Restore from backup if data loss detected
3. Document any manual fixes needed

---

## Notes

**Key Insight:** This is part of the larger engine/project boundary cleanup. Runs belong to projects, not the engine.

**Naming Convention:** Standardize on `run-YYYYMMDD_HHMMSS` format for all runs.
