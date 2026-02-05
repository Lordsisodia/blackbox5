# PLAN.md: Remove Duplicate Queue Entries

**Task:** TASK-SSOT-010 - Duplicate queue entries in queue.yaml
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 1-2 hours
**Importance:** 55 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
The queue.yaml file contains duplicate entries for the same tasks/events. This creates:
1. **Processing Duplicates**: Same task processed multiple times
2. **Incorrect Metrics**: Queue stats are inflated
3. **Confusion**: Unclear which entry is current
4. **Wasted Space**: Unnecessary file bloat

### First Principles Solution
- **Unique Entries**: Each task/event appears exactly once
- **Deduplication**: Clean up existing duplicates
- **Prevention**: Validation to prevent future duplicates
- **Clear State**: Single source of truth for queue state

---

## 2. Current State Analysis

### File Location

`5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml`

### Example Duplicates

```yaml
queue:
  - id: "task-001"
    timestamp: "2026-02-05T10:00:00Z"
    status: pending
  - id: "task-001"  # DUPLICATE!
    timestamp: "2026-02-05T10:05:00Z"
    status: pending
  - id: "task-002"
    timestamp: "2026-02-05T10:10:00Z"
    status: in_progress
```

### Causes

1. Race conditions in queue updates
2. Missing deduplication logic
3. Concurrent writes without locking

---

## 3. Proposed Solution

### Step 1: Deduplicate Current Queue (30 min)

**Script:** `2-engine/.autonomous/bin/dedup-queue.py`

```python
#!/usr/bin/env python3
"""Remove duplicate entries from queue.yaml."""

import yaml
from pathlib import Path

def deduplicate_queue(queue_path: Path):
    """Remove duplicate queue entries, keeping most recent."""
    with open(queue_path) as f:
        data = yaml.safe_load(f)

    seen = {}
    unique_queue = []

    for entry in data.get('queue', []):
        entry_id = entry.get('id')
        if entry_id not in seen:
            seen[entry_id] = entry
            unique_queue.append(entry)
        else:
            # Keep the more recent entry
            existing = seen[entry_id]
            if entry.get('timestamp', '') > existing.get('timestamp', ''):
                # Replace with newer entry
                idx = unique_queue.index(existing)
                unique_queue[idx] = entry
                seen[entry_id] = entry

    data['queue'] = unique_queue

    with open(queue_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

    print(f"Removed {len(data['queue']) - len(unique_queue)} duplicates")
```

### Step 2: Add Validation (30 min)

**Update:** Queue update logic

```python
def add_to_queue(entry: dict):
    """Add entry to queue with deduplication."""
    queue = load_queue()

    # Check for existing entry
    existing = find_entry(queue, entry['id'])
    if existing:
        # Update existing instead of adding new
        update_entry(existing, entry)
    else:
        queue.append(entry)

    save_queue(queue)
```

### Step 3: Add File Locking (30 min)

**Update:** Queue operations with locking

```python
import fcntl

def update_queue_atomic(update_fn):
    """Update queue with file locking to prevent race conditions."""
    with open(QUEUE_PATH, 'r+') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            queue = yaml.safe_load(f)
            updated = update_fn(queue)
            f.seek(0)
            f.truncate()
            yaml.dump(updated, f)
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
```

---

## 4. Files to Modify

### Modified Files
1. `5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` - Deduplicate
2. Queue update scripts - Add validation and locking

### New Files
1. `2-engine/.autonomous/bin/dedup-queue.py` - Deduplication script

---

## 5. Success Criteria

- [ ] All duplicates removed from queue.yaml
- [ ] Deduplication script created
- [ ] Queue update logic has validation
- [ ] File locking implemented for concurrent access
- [ ] No new duplicates can be added

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore queue.yaml from backup
2. **Fix**: Debug deduplication logic
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Step | Duration | Cumulative |
|------|----------|------------|
| Step 1: Deduplicate | 30 min | 30 min |
| Step 2: Validation | 30 min | 1 hour |
| Step 3: File Locking | 30 min | 1.5 hours |
| **Total** | | **1-2 hours** |

---

*Plan created based on SSOT violation analysis - Duplicate queue entries*
