# TASK-1769916001: Automate Queue Management

**Type:** implement
**Priority:** low
**Status:** pending
**Created:** 2026-02-01T12:42:40Z
**Estimated Minutes:** 40
**Context Level:** 2
**Improvement:** None (operational excellence)

---

## Objective

Implement automatic synchronization between `.autonomous/tasks/active/` directory and `.autonomous/communications/queue.yaml` to prevent queue sync issues and reduce manual queue management overhead.

---

## Context

**Why This Matters:**
- Queue sync issue occurred in Planner Run 0049
- TASK-1769915000 completed in Executor Run 40 but not removed from queue.yaml
- Manual queue management in every planner loop
- Risk of future sync errors causing Executor confusion

**The Problem:**
1. Executor completes task → moves to completed/
2. Queue.yaml still shows task as "pending" (manual update required)
3. Planner must manually remove completed tasks every loop
4. Error-prone: Just experienced this sync issue

**The Solution:**
Automate queue synchronization so that:
- Completed tasks automatically removed from queue.yaml
- Queue depth always accurate
- No manual intervention needed
- Single source of truth maintained

---

## Success Criteria

- [ ] Queue auto-syncs when tasks complete
- [ ] Completed tasks automatically removed from queue.yaml
- [ ] Queue depth always matches active/ directory count
- [ ] No manual queue management needed
- [ ] Integration point added to task completion workflow
- [ ] Test with 2+ task completions to verify sync works

---

## Approach

**Phase 1: Design (5 minutes)**
1. Review existing task completion workflow
2. Identify integration point for queue update
3. Determine trigger mechanism (when to update queue)
4. Design simple sync function

**Phase 2: Implementation (20 minutes)**
1. Create `2-engine/.autonomous/lib/queue_sync.py`
   - Function: `remove_completed_tasks_from_queue()`
   - Read active/ directory
   - Parse queue.yaml
   - Remove completed tasks
   - Write updated queue.yaml
2. Integrate into task completion workflow:
   - Option A: Add to `roadmap_sync.py` (already runs on completion)
   - Option B: Add to Executor post-completion checklist
   - Option C: Create standalone script
3. Test manually with mock data

**Phase 3: Validation (10 minutes)**
1. Create test scenario:
   - Add mock completed task to queue.yaml
   - Run sync function
   - Verify task removed
2. Test with real task completion:
   - Complete one task
   - Verify queue auto-updates
3. Verify queue depth accuracy

**Phase 4: Documentation (5 minutes)**
1. Document queue sync mechanism
2. Update workflow diagrams
3. Add to operations/.docs/queue-management-guide.md

---

## Files to Modify

**Create:**
- `2-engine/.autonomous/lib/queue_sync.py` - Queue sync library

**Modify:**
- `2-engine/.autonomous/lib/roadmap_sync.py` - Add queue sync call (Option A preferred)
- OR: `2-engine/.autonomous/prompts/system/executor/variations/v2-legacy-based.md` - Add to workflow
- `.autonomous/communications/queue.yaml` - Test sync functionality

**Documentation:**
- Create: `operations/.docs/queue-management-guide.md`
- Update: `2-engine/.autonomous/workflows/task-completion.yaml` (if exists)

---

## Implementation Details

### Queue Sync Function Design

```python
# 2-engine/.autonomous/lib/queue_sync.py

import yaml
from pathlib import Path

def remove_completed_tasks_from_queue(queue_path, active_dir):
    """
    Sync queue.yaml with active/ directory.

    Removes tasks from queue.yaml that are not in active/ directory.
    This ensures queue only contains pending tasks.

    Args:
        queue_path: Path to queue.yaml
        active_dir: Path to active/ directory

    Returns:
        int: Number of tasks removed
    """
    # Read current queue
    with open(queue_path, 'r') as f:
        queue_data = yaml.safe_load(f)

    # Get active task IDs
    active_tasks = [f.name for f in Path(active_dir).glob('TASK-*.md')]
    active_ids = [t.split('-')[1] for t in active_tasks]  # Extract numeric IDs

    # Filter queue to only active tasks
    original_count = len(queue_data['queue'])
    queue_data['queue'] = [
        task for task in queue_data['queue']
        if task['id'].split('-')[1] in active_ids
    ]

    # Update metadata
    removed_count = original_count - len(queue_data['queue'])
    queue_data['metadata']['current_depth'] = len(queue_data['queue'])
    queue_data['metadata']['last_updated'] = datetime.utcnow().isoformat()

    # Write updated queue
    with open(queue_path, 'w') as f:
        yaml.dump(queue_data, f, default_flow_style=False)

    return removed_count
```

### Integration Point

**Option A: Extend roadmap_sync.py** (PREFERRED)
- Add queue sync to existing `sync_task_completion()` function
- Rationale: Already runs on task completion
- Single integration point

**Option B: Executor Prompt**
- Add queue sync step to post-completion checklist
- Rationale: Explicit in workflow
- Risk: Executor may skip if not mandated

**Option C: Standalone Script**
- Create separate workflow trigger
- Rationale: Decoupled from existing code
- Risk: Another moving part to maintain

**Recommendation:** Option A - integrate into roadmap_sync.py

---

## Testing Plan

**Test 1: Manual Mock Test**
1. Create mock task in queue.yaml (not in active/)
2. Run `remove_completed_tasks_from_queue()`
3. Verify mock task removed
4. Verify queue depth updated

**Test 2: Real Task Completion**
1. Complete one real task
2. Verify task moved from active/ to completed/
3. Verify task automatically removed from queue.yaml
4. Verify queue metadata updated

**Test 3: Multiple Completions**
1. Complete 2+ tasks in sequence
2. Verify all removed from queue after each
3. Verify queue depth accurate throughout

---

## Notes

**Dependencies:** None (standalone operational improvement)

**Related Work:**
- TASK-1769911101: Roadmap sync implementation (Run 38)
- IMP-1769903001: Auto-sync roadmap state (completed)
- This task extends the sync concept to queue management

**Priority Justification:**
- LOW because: Manual sync works, just error-prone
- Not urgent: Executor can function with manual queue updates
- Quality-of-life: Reduces Planner overhead, prevents errors

**Risk Assessment:**
- Risk: Breaking queue.yaml format
- Mitigation: Test with mock data first, preserve YAML structure
- Rollback: Manual queue management always works as fallback

---

## Acceptance Criteria Checklist

- [ ] Queue sync library created (`queue_sync.py`)
- [ ] Integration point added to task completion workflow
- [ ] Function tested with mock data (passes)
- [ ] Function tested with real task completion (passes)
- [ ] Queue depth accuracy verified (2+ completions)
- [ ] Documentation created (queue management guide)
- [ ] No manual queue management needed after implementation
