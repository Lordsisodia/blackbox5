# TASK-SSOT-032: Unify Task State Management

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 55

---

## Objective

Eliminate cached task counts from multiple YAML files by implementing a derivation function that calculates counts directly from the `tasks/active/` directory source of truth.

---

## Success Criteria

- [ ] Derivation function `get_task_counts()` created in `2-engine/.autonomous/lib/task_utils.py`
- [ ] Cached counts removed from `STATE.yaml`, `timeline.yaml`, and `queue.yaml`
- [ ] All scripts that read task counts updated to use derivation function
- [ ] Counts are accurate and validated against source directory
- [ ] Optional caching with auto-invalidation implemented

---

## Context

Task counts are currently stored/cached in multiple locations:
- `STATE.yaml` - metrics.active_tasks
- `timeline.yaml` - stats.pending_tasks
- `queue.yaml` - queue_stats.total_tasks

This creates:
1. **Staleness**: Counts get out of sync with actual directory contents
2. **Manual Updates**: Must update multiple places when tasks change
3. **Inconsistency**: Different files show different counts

The `tasks/active/` directory is the true source of truth. Counts should be derived on-demand rather than cached.

---

## Approach

### Phase 1: Create Derivation Function (30 min)
1. Implement `get_task_counts()` that scans `tasks/active/` directory
2. Parse each task.md file to determine status (pending, in_progress, completed)
3. Add optional caching with TTL

### Phase 2: Update YAML Files (30 min)
1. Remove cached count fields from STATE.yaml, timeline.yaml, queue.yaml
2. Add comments indicating counts are now derived
3. Document the derivation function location

### Phase 3: Update Scripts (1 hour)
1. Update dashboard to use derivation function
2. Update metrics collector
3. Update health checks
4. Update any other scripts reading task counts

### Phase 4: Add Validation (30 min)
1. Create validation function to verify derived counts
2. Add periodic consistency checks
3. Alert if counts deviate from expected

---

## Rollback Strategy

If derivation causes performance issues:
1. Re-enable caching with shorter TTL
2. Consider incremental updates instead of full derivation
3. Document performance characteristics

---

## Notes

**Key Insight:** This follows the Single Source of Truth principle - the filesystem is the truth, YAML files should not duplicate it.

**Performance Consideration:** For large task directories, consider:
- Lazy evaluation (calculate only when needed)
- Short-term caching (5-60 seconds)
- Incremental updates via file watchers
