# PLAN.md: Dry-Run Library Not Used Consistently

**Task ID:** TASK-ARCH-052
**Status:** Planning
**Priority:** LOW
**Created:** 2026-02-05
**Estimated Effort:** 30 minutes
**Source:** Scout opportunity arch-008 (Score: 5.0)

---

## 1. First Principles Analysis

### Why Is Dry-Run Support Important?

1. **Safety**: Preview changes before executing destructive operations
2. **Debugging**: Understand what a script would do without side effects
3. **Testing**: Validate script logic without modifying state
4. **Confidence**: Users can verify actions before committing
5. **Documentation**: Dry-run output serves as implicit documentation

### What Happens Without Consistent Dry-Run Support?

| Problem | Impact | Severity |
|---------|--------|----------|
| Inconsistent UX | Some scripts support --dry-run, others don't | Medium |
| Accidental changes | No way to preview before execution | High |
| Testing difficulty | Must use real environment for testing | Medium |
| User confusion | Uncertain which commands are safe | Medium |
| Maintenance burden | Multiple implementations of same pattern | Low |

### How Should Dry-Run Be Implemented?

**Standardized Library Approach:**
- Single library provides all dry-run utilities
- Consistent command-line interface (--dry-run flag)
- Helper functions for common operations
- Visual feedback showing what would happen

---

## 2. Current State Assessment

### Existing Dry-Run Library

**Location:** `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/dry_run.sh`

**Features:**
- `--dry-run` and `--verbose` flag parsing
- Helper functions: `dry_run_exec`, `dry_run_mkdir`, `dry_run_write`, etc.
- Visual feedback with color coding
- Summary on completion

**Current Usage:**
- Library exists and is well-designed
- Used in some scripts (improvement-loop.py references it)
- Many shell scripts don't use it

### Shell Scripts Inventory

| Script | Has Dry-Run | Uses Library | Priority |
|--------|-------------|--------------|----------|
| `bb5-parallel-dispatch.sh` | No | No | High |
| `init-routes.sh` | No | No | Medium |
| `planner-agent.sh` | No | No | Medium |
| `scout-agent.sh` | No | No | Medium |
| `analyzer-agent.sh` | No | No | Medium |
| `github-analysis-pipeline.sh` | No | No | Low |
| `launch-*.sh` scripts | No | No | Low |
| `ralf-daemon.sh` | No | No | Medium |

### Python Scripts

Python scripts use different patterns:
- Some have `--dry-run` flags
- Others use `DRY_RUN` environment variable
- No standardized library approach

---

## 3. Proposed Solution

### Standardized Implementation

**For Shell Scripts:**
```bash
#!/bin/bash
# Standard header for all BB5 shell scripts

# Source dry-run library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/dry_run.sh" 2>/dev/null || \
source "$SCRIPT_DIR/../../2-engine/.autonomous/lib/dry_run.sh"

# Initialize dry-run mode
ARGS=$(dry_run_init "$@")
set -- $ARGS

# Use dry-run helpers throughout
dry_run_mkdir "$TASK_DIR"
dry_run_write "$CONFIG_FILE" "$content"
dry_run_exec "git commit -m '$message'" "Commit changes"

# Set exit trap for summary
dry_run_set_exit_trap
```

**For Python Scripts:**
```python
# lib/dry_run.py - Python equivalent
import os
import argparse
from typing import Callable, Any

class DryRunContext:
    def __init__(self, enabled: bool = False, verbose: bool = False):
        self.enabled = enabled
        self.verbose = verbose

    def exec(self, func: Callable, *args, description: str = None, **kwargs) -> Any:
        if self.enabled:
            print(f"[DRY-RUN] Would: {description or func.__name__}")
            return None
        return func(*args, **kwargs)

    def write_file(self, path: str, content: str):
        if self.enabled:
            print(f"[DRY-RUN] Would write to {path}")
            if self.verbose:
                print(f"  Content: {content[:100]}...")
            return
        with open(path, 'w') as f:
            f.write(content)
```

---

## 4. Implementation Plan

### Phase 1: Audit Shell Scripts (10 min)

1. **Find all shell scripts**
   - List all .sh files in bin/ and .autonomous/
   - Categorize by importance
   - Identify destructive operations

2. **Assess dry-run needs**
   - Which scripts modify files?
   - Which scripts use git commands?
   - Which scripts create/delete directories?

3. **Prioritize scripts**
   - High: User-facing CLI scripts
   - Medium: Agent scripts
   - Low: Internal pipeline scripts

### Phase 2: Add Dry-Run to High-Priority Scripts (15 min)

1. **Update bb5-parallel-dispatch.sh**
   - Source dry_run.sh
   - Add --dry-run flag handling
   - Wrap subprocess calls

2. **Update agent scripts**
   - planner-agent.sh
   - scout-agent.sh
   - analyzer-agent.sh

3. **Update ralf-daemon.sh**
   - Add dry-run for daemon operations

### Phase 3: Create Python Dry-Run Module (5 min)

1. **Create lib/dry_run.py**
   - Port shell functions to Python
   - Add context manager support
   - Include tests

2. **Document usage**
   - Add to developer guide
   - Include examples

---

## 5. Success Criteria

- [ ] All shell scripts audited for dry-run needs
- [ ] High-priority scripts have --dry-run support
- [ ] Python dry_run.py module created
- [ ] Documentation updated with usage examples
- [ ] Consistent --dry-run flag across all scripts
- [ ] Visual feedback shows what would happen

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Audit | 10 min | 10 min |
| Phase 2: Shell Scripts | 15 min | 25 min |
| Phase 3: Python Module | 5 min | 30 min |
| **Total** | **30 min** | **~30 min** |

---

## 7. Rollback Strategy

If issues occur:

1. **Immediate:** Revert modified scripts to previous version
2. **Short-term:** Disable dry-run flags if causing issues
3. **Long-term:** Fix library and re-apply

---

## 8. Files to Modify/Create

### New Files

| File | Purpose | Lines |
|------|---------|-------|
| `lib/dry_run.py` | Python dry-run utilities | ~150 |

### Modified Files

| File | Changes | Lines |
|------|---------|-------|
| `bb5-parallel-dispatch.sh` | Add dry-run support | +20 |
| `planner-agent.sh` | Add dry-run support | +15 |
| `scout-agent.sh` | Add dry-run support | +15 |
| `analyzer-agent.sh` | Add dry-run support | +15 |
| `ralf-daemon.sh` | Add dry-run support | +15 |

---

*Plan created: 2026-02-06*
*Ready for implementation*
