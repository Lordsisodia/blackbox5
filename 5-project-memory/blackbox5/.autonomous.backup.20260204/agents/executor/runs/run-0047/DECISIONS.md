# Decisions - TASK-1769916001

## Decision 1: Integration Approach

**Context:** How to integrate queue sync into existing task completion workflow

**Options:**
- **Option A:** Extend `roadmap_sync.py` with new `sync_all_on_task_completion()` function
- **Option B:** Add queue sync call directly to executor prompt (Step 4)
- **Option C:** Create standalone workflow trigger

**Selected:** Option A - Extend roadmap_sync.py

**Rationale:**
- **Single integration point:** Existing `roadmap_sync.py` already called on task completion
- **Non-breaking:** Doesn't modify existing functions (`sync_roadmap_on_task_completion`, `sync_improvement_backlog`)
- **Follows patterns:** Uses same structure as existing sync functions
- **Testable:** CLI interface for manual testing
- **Backwards compatible:** Existing code continues to work unchanged

**Reversibility:** HIGH (can remove function if needed, existing code unchanged)

**Impact:** LOW risk, HIGH benefit

---

## Decision 2: Queue Sync Failure Handling

**Context:** How to handle queue sync failures during task completion

**Options:**
- **Option A:** Blocking - Fail task completion if queue sync fails
- **Option B:** Non-blocking - Log warning, continue task completion
- **Option C:** Retry - Retry queue sync up to N times before failing

**Selected:** Option B - Non-blocking with warning log

**Rationale:**
- **Priority:** Task completion is critical, queue metadata is important but not critical
- **Error surface:** Queue sync can fail due to file permissions, disk space, YAML corruption
- **Recoverability:** Manual sync possible post-completion (CLI tool available)
- **User experience:** Executor shouldn't be blocked by metadata sync issues
- **Observability:** Warning log ensures failures are visible

**Trade-offs:**
- **Pro:** Task completion always succeeds
- **Con:** Queue may become stale if sync fails silently
- **Mitigation:** Log warning + manual sync tool available

**Reversibility:** MEDIUM (would require executor prompt update to change)

**Impact:** LOW risk, MEDIUM benefit

---

## Decision 3: Queue Metadata Structure

**Context:** How to handle missing metadata in existing queue.yaml files

**Options:**
- **Option A:** Require metadata - Fail sync if metadata missing
- **Option B:** Create metadata - Add metadata section if missing
- **Option C:** Optional metadata - Make metadata optional in all operations

**Selected:** Option B - Create metadata if missing

**Rationale:**
- **Flexibility:** Handles both old (no metadata) and new (with metadata) formats
- **Progressive:** Existing queue.yaml files automatically upgraded on first sync
- **User-friendly:** No manual intervention needed
- **Consistency:** All queue.yaml files have metadata after first sync

**Implementation:**
```python
if "metadata" not in queue_data:
    queue_data["metadata"] = {}

queue_data["metadata"]["current_depth"] = len(filtered_queue)
queue_data["metadata"]["last_updated"] = timestamp
queue_data["metadata"]["updated_by"] = "queue_sync.py"
```

**Reversibility:** LOW (now part of expected behavior, would be breaking change to remove)

**Impact:** NO risk, HIGH benefit

---

## Decision 4: Task ID Extraction Strategy

**Context:** How to match queue tasks with active directory tasks

**Options:**
- **Option A:** Full task ID match (TASK-XXXXXXXX)
- **Option B:** Numeric ID match (XXXXXXXX)
- **Option C:** Both - Try full ID, fall back to numeric ID

**Selected:** Option C - Both methods with fallback

**Rationale:**
- **Robustness:** Handles variations in task ID format
- **Compatibility:** Works with different naming conventions
- **Safety:** Double verification reduces false positives
- **Flexibility:** Future-proof against task ID format changes

**Implementation:**
```python
# Match by either full ID or numeric ID
if task_id in active_task_ids or task_numeric_id in active_numeric_ids:
    # Task is still active, keep in queue
```

**Reversibility:** LOW (core logic, would be breaking to change)

**Impact:** NO risk, HIGH benefit

---

## Decision 5: Documentation Scope

**Context:** How much documentation to create for queue management

**Options:**
- **Option A:** Minimal - Just usage examples
- **Option B:** Comprehensive - Full guide with troubleshooting
- **Option C:** Inline only - Comments in code only

**Selected:** Option B - Comprehensive guide

**Rationale:**
- **Operational excellence:** Queue is critical system component
- **Troubleshooting:** Common issues need documented solutions
- **Knowledge transfer:** Future maintainers need complete understanding
- **Best practices:** Document patterns for planner and executor
- **Monitoring:** Health check commands and metrics

**Sections included:**
1. Overview and structure
2. Automatic synchronization workflow
3. Manual CLI usage
4. Queue depth management
5. Troubleshooting (3 common issues)
6. Best practices (planner, executor, system)
7. Monitoring and health metrics
8. Reference and support

**Reversibility:** LOW (documentation can be extended but not easily reduced)

**Impact:** NO risk, HIGH benefit

---

## Decision 6: CLI Interface Design

**Context:** How to design CLI for queue sync library

**Options:**
- **Option A:** Separate CLI (queue_sync.py)
- **Option B:** Extended CLI (roadmap_sync.py "all" mode)
- **Option C:** Both - Separate and extended

**Selected:** Option C - Both interfaces

**Rationale:**
- **Separate CLI:** Simple, focused, for queue-only operations
- **Extended CLI:** Integrated, for full sync operations
- **Flexibility:** User can choose based on use case
- **Testing:** Both interfaces independently testable
- **Compatibility:** Existing roadmap_sync.py CLI unchanged

**Usage:**
```bash
# Queue-only sync
python3 queue_sync.py queue.yaml active/ --dry-run

# Full sync (roadmap + improvement + queue)
python3 roadmap_sync.py all TASK-ID [...] [task-file]
```

**Reversibility:** LOW (CLI is public interface, removing would be breaking change)

**Impact:** LOW risk, HIGH benefit

---

## Summary

| Decision | Choice | Risk | Benefit | Reversibility |
|----------|--------|------|---------|---------------|
| Integration approach | Extend roadmap_sync.py | LOW | HIGH | HIGH |
| Failure handling | Non-blocking | LOW | MEDIUM | MEDIUM |
| Metadata structure | Create if missing | NONE | HIGH | LOW |
| ID extraction | Both methods | NONE | HIGH | LOW |
| Documentation scope | Comprehensive | NONE | HIGH | LOW |
| CLI design | Both interfaces | LOW | HIGH | LOW |

**Overall Approach:** Conservative, flexible, user-friendly
**Key Principle:** Non-blocking, backwards compatible, well-documented
**Success Criteria:** All acceptance criteria met, tests pass, documentation complete
