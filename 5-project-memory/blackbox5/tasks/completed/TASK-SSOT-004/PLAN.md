# PLAN.md: Derive Task Count from tasks/active Directory

**Task:** TASK-SSOT-004 - Task count stored in multiple places
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 60 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Task count is stored/cached in multiple places:
- `5-project-memory/blackbox5/STATE.yaml` - task_count field
- `5-project-memory/blackbox5/timeline.yaml` - task metrics
- `5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` - queue stats
- Potentially other dashboard/status files

This creates:
1. **Update Lag**: Counts get out of sync
2. **Manual Updates**: Must update multiple files
3. **Inconsistency**: Different files show different counts
4. **Maintenance**: Multiple places to fix when logic changes

### First Principles Solution
- **Derived Data**: Task count should be derived from source (directory listing)
- **Single Source**: tasks/active/ directory is the truth
- **On-Demand Calculation**: Count when needed, don't cache
- **Caching Optional**: If performance requires, cache with automatic invalidation

---

## 2. Current State Analysis

### Storage Locations

| Location | Field | Purpose |
|----------|-------|---------|
| STATE.yaml | `metrics.task_count` | Dashboard metric |
| timeline.yaml | `stats.pending_tasks` | Timeline stats |
| queue.yaml | `queue_stats.total_tasks` | Queue stats |

### Update Patterns

1. **Manual**: Human updates multiple files
2. **Script**: Scripts update their specific file
3. **Inconsistent**: Files updated at different times

### Query Patterns

1. Dashboard reads STATE.yaml
2. Timeline reads timeline.yaml
3. Queue manager reads queue.yaml

---

## 3. Proposed Solution

### Step 1: Create Derivation Function (30 min)

**File:** `2-engine/.autonomous/lib/task_utils.py`

```python
def get_task_count(project_path: str) -> Dict[str, int]:
    """
    Derive task counts from tasks/active directory.
    Returns dict with pending, in_progress, completed counts.
    """
    tasks_dir = Path(project_path) / "tasks" / "active"

    pending = 0
    in_progress = 0

    for task_dir in tasks_dir.iterdir():
        if task_dir.is_dir() and task_dir.name.startswith("TASK-"):
            task_file = task_dir / "task.md"
            if task_file.exists():
                content = task_file.read_text()
                if "Status:** pending" in content:
                    pending += 1
                elif "Status:** in_progress" in content:
                    in_progress += 1

    return {
        "pending": pending,
        "in_progress": in_progress,
        "total": pending + in_progress
    }
```

### Step 2: Update STATE.yaml (30 min)

**Change:** Remove `metrics.task_count` field

**Add:** Comment indicating derived nature
```yaml
metrics:
  # Task counts are derived from tasks/active/ directory
  # Use task_utils.get_task_count() for current values
```

### Step 3: Update timeline.yaml (30 min)

**Change:** Remove `stats.pending_tasks` cached value

**Add:** Dynamic calculation note
```yaml
stats:
  # Pending tasks calculated from tasks/active/
  # See: task_utils.get_task_count()
```

### Step 4: Update queue.yaml (30 min)

**Change:** Remove `queue_stats.total_tasks` cached value

**Add:** Reference to source
```yaml
queue_stats:
  # Task counts derived from tasks/active/
  # Use task_utils.get_task_count() for accurate values
```

### Step 5: Update Dashboard/Scripts (1 hour)

**Update:** Any script reading task counts

```python
# Before
import yaml
with open("STATE.yaml") as f:
    state = yaml.safe_load(f)
count = state["metrics"]["task_count"]

# After
from task_utils import get_task_count
counts = get_task_count(project_path)
count = counts["total"]
```

---

## 4. Files to Modify

### Modified Files
1. `5-project-memory/blackbox5/STATE.yaml` - Remove cached count
2. `5-project-memory/blackbox5/timeline.yaml` - Remove cached count
3. `5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` - Remove cached count

### New Files
1. `2-engine/.autonomous/lib/task_utils.py` - Derivation functions

### Scripts to Update
1. `bin/bb5-health-dashboard.py` - Use derivation function
2. `bin/bb5-metrics-collector.py` - Use derivation function
3. Any other dashboard/status scripts

---

## 5. Success Criteria

- [ ] task_utils.py created with get_task_count() function
- [ ] All cached task counts removed from YAML files
- [ ] All scripts updated to use derivation function
- [ ] Task counts are always accurate (no stale data)
- [ ] Performance acceptable (or caching with auto-invalidation implemented)

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore cached counts in YAML files
2. **Fix**: Debug derivation function
3. **Re-apply**: Remove caches once fixed

---

## 7. Estimated Timeline

| Step | Duration | Cumulative |
|------|----------|------------|
| Step 1: Derivation Function | 30 min | 30 min |
| Step 2: Update STATE.yaml | 30 min | 1 hour |
| Step 3: Update timeline.yaml | 30 min | 1.5 hours |
| Step 4: Update queue.yaml | 30 min | 2 hours |
| Step 5: Update Scripts | 1 hour | 3 hours |
| **Total** | | **2-3 hours** |

---

*Plan created based on SSOT violation analysis - Task count stored in multiple places*
