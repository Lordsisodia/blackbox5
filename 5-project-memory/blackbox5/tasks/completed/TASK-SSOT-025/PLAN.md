# PLAN.md: Migrate 35+ File Operations to StorageBackend

**Task:** TASK-SSOT-025 - Migrate 35+ file operations to use StorageBackend
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 6-8 hours
**Importance:** 70 (High)

---

## 1. First Principles Analysis

### The Core Problem
There are 35+ locations in the codebase with direct file operations that need to be migrated to use the StorageBackend abstraction:
- Direct `open()` calls
- Direct `yaml.safe_load()` calls
- Direct `yaml.dump()` calls
- No error handling
- No locking
- No caching

This creates:
1. **Technical Debt**: Multiple patterns for same operation
2. **Maintenance Burden**: Changes needed in many places
3. **Inconsistency**: Different error handling
4. **Bugs**: Race conditions, partial writes
5. **Testing Difficulty**: Hard to mock file system

### First Principles Solution
- **Systematic Migration**: Replace all direct file operations
- **Pattern Matching**: Find and replace systematically
- **Validation**: Verify each migration
- **Gradual Rollout**: Migrate in batches
- **Rollback Plan**: Keep backups

---

## 2. Current State Analysis

### File Operation Patterns

```python
# Pattern 1: Simple read
with open(path) as f:
    data = yaml.safe_load(f)

# Pattern 2: Simple write
with open(path, 'w') as f:
    yaml.dump(data, f)

# Pattern 3: Read-modify-write
with open(path) as f:
    data = yaml.safe_load(f)
data['field'] = value
with open(path, 'w') as f:
    yaml.dump(data, f)

# Pattern 4: Check existence + read
if os.path.exists(path):
    with open(path) as f:
        data = yaml.safe_load(f)
```

### Target Locations

| Location | Count | Priority |
|----------|-------|----------|
| `2-engine/.autonomous/bin/*.py` | 15 | High |
| `5-project-memory/blackbox5/bin/*.py` | 10 | High |
| `2-engine/.autonomous/lib/*.py` | 8 | Medium |
| Other scripts | 5 | Low |

---

## 3. Proposed Solution

### Migration Strategy

#### Phase 1: Inventory (1 hour)

Create a complete inventory of file operations:

```bash
# Find all file operations
grep -r "open(" 2-engine/.autonomous/bin/*.py | grep -v ".pyc"
grep -r "yaml.safe_load" 2-engine/.autonomous/bin/*.py
grep -r "yaml.dump" 2-engine/.autonomous/bin/*.py
```

Document each occurrence:
- File path
- Line number
- Operation type (read/write/modify)
- Context (what data)

#### Phase 2: Create Migration Script (1 hour)

**File:** `2-engine/.autonomous/bin/migrate-file-ops.py`

```python
#!/usr/bin/env python3
"""Migrate file operations to StorageBackend."""

import re
from pathlib import Path

MIGRATIONS = {
    # Pattern -> Replacement template
    'simple_read': {
        'pattern': r"with open\((.+?)\) as f:\s*\n\s*data = yaml.safe_load\(f\)",
        'replacement': "data = storage.read({path})",
    },
    'simple_write': {
        'pattern': r"with open\((.+?), ['\"]w['\"]\) as f:\s*\n\s*yaml.dump\((.+?), f\)",
        'replacement': "storage.write({path}, {data})",
    },
    'check_exists': {
        'pattern': r"if os.path.exists\((.+?)\):",
        'replacement': "if storage.exists({path}):",
    }
}

def migrate_file(file_path: Path) -> str:
    """Migrate a single file."""
    content = file_path.read_text()
    original = content

    for name, migration in MIGRATIONS.items():
        content = re.sub(migration['pattern'], migration['replacement'], content)

    if content != original:
        # Backup original
        backup_path = file_path.with_suffix('.py.backup')
        backup_path.write_text(original)

        # Write migrated
        file_path.write_text(content)
        print(f"Migrated: {file_path}")
        return True

    return False
```

#### Phase 3: Batch Migration (4 hours)

**Batch 1: High Priority (2 hours)**
- `2-engine/.autonomous/bin/scout-intelligent.py`
- `2-engine/.autonomous/bin/executor-implement.py`
- `2-engine/.autonomous/bin/verifier-validate.py`
- `2-engine/.autonomous/bin/improvement-loop.py`

**Batch 2: Medium Priority (1.5 hours)**
- `5-project-memory/blackbox5/bin/bb5-*.py`
- `2-engine/.autonomous/lib/*.py`

**Batch 3: Low Priority (30 min)**
- Other scripts

For each file:
1. Read and understand current file operations
2. Apply migration
3. Test the migrated code
4. Verify functionality

#### Phase 4: Validation (2 hours)

1. Run all migrated scripts
2. Verify file operations work correctly
3. Check for any regressions
4. Performance test (ensure no degradation)

---

## 4. Migration Examples

### Example 1: Simple Read

```python
# Before
with open(f"tasks/active/{task_id}/task.md") as f:
    task = yaml.safe_load(f)

# After
storage = get_storage()
task = storage.read(f"tasks/active/{task_id}/task.md")
```

### Example 2: Simple Write

```python
# Before
with open(f"tasks/active/{task_id}/task.md", 'w') as f:
    yaml.dump(task_data, f)

# After
storage = get_storage()
storage.write(f"tasks/active/{task_id}/task.md", task_data)
```

### Example 3: Read-Modify-Write

```python
# Before
with open('queue.yaml') as f:
    queue = yaml.safe_load(f)
queue['items'].append(new_item)
with open('queue.yaml', 'w') as f:
    yaml.dump(queue, f)

# After
storage = get_storage()
with storage.transaction() as tx:
    queue = storage.read('queue.yaml')
    queue['items'].append(new_item)
    tx['queue.yaml'] = queue
```

---

## 5. Files to Modify

### Batch 1 (High Priority)
1. `2-engine/.autonomous/bin/scout-intelligent.py`
2. `2-engine/.autonomous/bin/executor-implement.py`
3. `2-engine/.autonomous/bin/verifier-validate.py`
4. `2-engine/.autonomous/bin/improvement-loop.py`
5. `2-engine/.autonomous/bin/planner-prioritize.py`

### Batch 2 (Medium Priority)
6. `5-project-memory/blackbox5/bin/bb5-metrics-collector.py`
7. `5-project-memory/blackbox5/bin/bb5-queue-manager.py`
8. `5-project-memory/blackbox5/bin/bb5-health-dashboard.py`
9. `2-engine/.autonomous/lib/decision_registry.py`
10. `2-engine/.autonomous/lib/context_budget.py`

### Batch 3 (Low Priority)
11-35+. Other scripts with file operations

---

## 6. Success Criteria

- [ ] All 35+ file operations migrated
- [ ] No direct `open()` calls for YAML files remain
- [ ] All tests passing
- [ ] No performance degradation
- [ ] Backups created for all modified files
- [ ] Documentation updated

---

## 7. Rollback Strategy

If issues arise:

1. **Immediate**: Restore from .backup files
2. **Identify**: Find which migration caused issue
3. **Fix**: Debug and fix specific file
4. **Re-migrate**: Once fixed

---

## 8. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Inventory | 1 hour | 1 hour |
| Phase 2: Migration Script | 1 hour | 2 hours |
| Phase 3: Batch Migration | 4 hours | 6 hours |
| Phase 4: Validation | 2 hours | 8 hours |
| **Total** | | **6-8 hours** |

---

*Plan created based on SSOT violation analysis - 35+ file operations need migration*
