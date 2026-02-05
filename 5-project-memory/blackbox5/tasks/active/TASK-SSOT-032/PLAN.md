# PLAN.md: Unify Task Count Storage

**Task:** TASK-SSOT-032 - Task count stored in multiple locations
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 55 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Task counts are stored/cached in:
- `STATE.yaml` - metrics.active_tasks
- `timeline.yaml` - stats.pending_tasks
- `queue.yaml` - queue_stats.total_tasks

This creates:
1. **Staleness**: Counts get out of sync
2. **Manual Updates**: Must update multiple places
3. **Inconsistency**: Different files show different counts

### First Principles Solution
- **Derived Data**: Count from source (tasks/active/)
- **Single Source**: tasks/active/ directory is truth
- **On-Demand**: Calculate when needed
- **Cache Optional**: With auto-invalidation

---

## 2. Proposed Solution

### Derivation Function

**File:** `2-engine/.autonomous/lib/task_utils.py`

```python
def get_task_counts(project_path: str) -> Dict[str, int]:
    """Derive task counts from tasks/active directory."""
    tasks_dir = Path(project_path) / "tasks" / "active"

    counts = {
        'pending': 0,
        'in_progress': 0,
        'completed': 0,
        'total': 0
    }

    for task_dir in tasks_dir.iterdir():
        if task_dir.is_dir() and task_dir.name.startswith('TASK-'):
            task_file = task_dir / "task.md"
            if task_file.exists():
                content = task_file.read_text()
                counts['total'] += 1

                if 'Status:** pending' in content:
                    counts['pending'] += 1
                elif 'Status:** in_progress' in content:
                    counts['in_progress'] += 1
                elif 'Status:** completed' in content:
                    counts['completed'] += 1

    return counts
```

### Implementation Plan

#### Phase 1: Create Derivation Function (30 min)

1. Implement get_task_counts()
2. Add caching option
3. Add tests

#### Phase 2: Update YAML Files (30 min)

Remove cached counts, add comments:
```yaml
# STATE.yaml
metrics:
  # Task counts derived from tasks/active/
  # Use task_utils.get_task_counts() for current values
```

#### Phase 3: Update Scripts (1 hour)

Update all scripts that read task counts:
- Dashboard
- Metrics collector
- Health checks

#### Phase 4: Add Validation (30 min)

Ensure counts are accurate:
```python
def validate_task_counts(project_path: str) -> bool:
    """Validate that derived counts match expectations."""
    counts = get_task_counts(project_path)
    # Add validation logic
    return True
```

---

## 3. Success Criteria

- [ ] Derivation function created
- [ ] Cached counts removed
- [ ] All scripts updated
- [ ] Counts are accurate

---

## 4. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Function | 30 min |
| YAML Updates | 30 min |
| Script Updates | 1 hour |
| Validation | 30 min |
| **Total** | **2-3 hours** |

---

*Plan created based on SSOT violation analysis*
