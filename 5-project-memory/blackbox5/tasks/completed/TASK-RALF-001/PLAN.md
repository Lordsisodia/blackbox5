# PLAN.md: Extract Hardcoded Paths from RALF Agent Scripts

**Task ID:** TASK-RALF-001
**Status:** Planning
**Priority:** CRITICAL
**Parent:** Issue #4 - RALF Knows Project Structure
**Estimated Effort:** 3 hours

---

## 1. First Principles Analysis

### Why is Path Extraction Critical?

1. **Project Agnosticism**: RALF should work with any project, not just blackbox5
2. **Portability**: Hardcoded paths break when moving between environments
3. **Maintainability**: One configuration change vs. 6 file edits
4. **Testability**: Different paths for testing without code changes

### What Happens Without This Change?

| Problem | Impact | Severity |
|---------|--------|----------|
| Cannot use RALF with other projects | Limited adoption | High |
| Paths break on different systems | Runtime errors | High |
| Multiple places to update paths | Maintenance burden | Medium |
| Cannot override for testing | Poor testability | Medium |

### How Does Environment Variable Configuration Help?

By using environment variables with fallback defaults, we maintain backward compatibility while enabling customization. Scripts validate paths on startup and provide helpful error messages if paths are invalid.

---

## 2. Current State Assessment

### Files with Hardcoded Paths

| File | Lines | Current Pattern |
|------|-------|-----------------|
| `scout-intelligent.py` | 30-32 | `Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"` |
| `scout-task-based.py` | 23-25 | `Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"` |
| `planner-prioritize.py` | 23-26 | `Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"` |
| `executor-implement.py` | 25-29 | `Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"` |
| `verifier-validate.py` | 24-26 | `Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"` |
| `improvement-loop.py` | 24-27 | `Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"` |

### Current Pattern
```python
PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"
ENGINE_DIR = Path.home() / ".blackbox5" / "2-engine"
```

### Target Pattern
```python
PROJECT_DIR = Path(os.environ.get("RALF_PROJECT_DIR", Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"))
ENGINE_DIR = Path(os.environ.get("RALF_ENGINE_DIR", Path.home() / ".blackbox5" / "2-engine"))
```

---

## 3. Proposed Solution

### Configuration Hierarchy

```
1. Environment Variables (highest priority)
   ↓
2. Hardcoded Defaults (backward compatibility)
   ↓
3. Error if invalid (validation)
```

### Path Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `RALF_PROJECT_DIR` | Project memory directory | `~/.blackbox5/5-project-memory/blackbox5` |
| `RALF_ENGINE_DIR` | Engine directory | `~/.blackbox5/2-engine` |

### Validation Strategy

```python
def validate_paths():
    if not PROJECT_DIR.exists():
        print(f"Error: RALF_PROJECT_DIR does not exist: {PROJECT_DIR}")
        print(f"Set RALF_PROJECT_DIR environment variable or create directory")
        sys.exit(1)

    if not ENGINE_DIR.exists():
        print(f"Error: RALF_ENGINE_DIR does not exist: {ENGINE_DIR}")
        print(f"Set RALF_ENGINE_DIR environment variable or create directory")
        sys.exit(1)
```

---

## 4. Implementation Plan

### Phase 1: Create Shared Path Module (30 min)

**1.1 Create `2-engine/.autonomous/lib/paths.py`**
```python
"""RALF path configuration module."""
import os
from pathlib import Path

def get_project_dir() -> Path:
    """Get project directory from environment or default."""
    default = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"
    return Path(os.environ.get("RALF_PROJECT_DIR", default))

def get_engine_dir() -> Path:
    """Get engine directory from environment or default."""
    default = Path.home() / ".blackbox5" / "2-engine"
    return Path(os.environ.get("RALF_ENGINE_DIR", default))

def validate_paths() -> tuple[Path, Path]:
    """Validate and return paths."""
    project_dir = get_project_dir()
    engine_dir = get_engine_dir()

    if not project_dir.exists():
        raise FileNotFoundError(f"RALF_PROJECT_DIR does not exist: {project_dir}")

    if not engine_dir.exists():
        raise FileNotFoundError(f"RALF_ENGINE_DIR does not exist: {engine_dir}")

    return project_dir, engine_dir
```

### Phase 2: Update Agent Scripts (90 min)

**2.1 Update `scout-intelligent.py`**
- Add import: `from lib.paths import validate_paths`
- Replace hardcoded paths with: `PROJECT_DIR, ENGINE_DIR = validate_paths()`
- Add error handling for validation failures

**2.2 Update `scout-task-based.py`**
- Same pattern as scout-intelligent.py

**2.3 Update `planner-prioritize.py`**
- Same pattern as scout-intelligent.py

**2.4 Update `executor-implement.py`**
- Same pattern as scout-intelligent.py

**2.5 Update `verifier-validate.py`**
- Same pattern as scout-intelligent.py

**2.6 Update `improvement-loop.py`**
- Same pattern as scout-intelligent.py

### Phase 3: Create Environment Template (15 min)

**3.1 Create `.env.example`**
```bash
# RALF Configuration
# Copy to .env and customize for your environment

# Project directory (default: ~/.blackbox5/5-project-memory/blackbox5)
RALF_PROJECT_DIR=/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5

# Engine directory (default: ~/.blackbox5/2-engine)
RALF_ENGINE_DIR=/Users/shaansisodia/.blackbox5/2-engine
```

### Phase 4: Testing (45 min)

**4.1 Default Path Test**
- Run each script without env vars
- Verify uses default paths
- Verify runs successfully

**4.2 Custom Path Test**
- Set RALF_PROJECT_DIR to test directory
- Run each script
- Verify uses custom path

**4.3 Invalid Path Test**
- Set RALF_PROJECT_DIR to non-existent path
- Run each script
- Verify helpful error message
- Verify exit code non-zero

**4.4 Backward Compatibility Test**
- Run existing workflows
- Verify no regression

---

## 5. Success Criteria

| Criterion | Verification Method |
|-----------|---------------------|
| All 6 scripts use environment variables | Code review |
| Scripts fall back to current hardcoded paths | Test without env vars |
| Scripts validate paths exist on startup | Test with invalid path |
| Scripts provide helpful error messages | Check error output |
| `.env.example` created | File exists |
| No regression in existing workflows | Run existing tests |

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Shared Path Module | 30 min | 30 min |
| Phase 2: Update Agent Scripts | 90 min | 120 min |
| Phase 3: Environment Template | 15 min | 135 min |
| Phase 4: Testing | 45 min | 180 min |
| **Total** | **3 hours** | |

---

## 7. Rollback Strategy

If issues arise:
1. Revert to hardcoded paths in each script
2. Remove `lib/paths.py`
3. Remove `.env.example`

Scripts maintain backward compatibility, so rollback is simply reverting the imports.

---

## 8. Future Considerations

This task is a prerequisite for TASK-RALF-002 (RALF Configuration System). The path module created here will be extended to support:
- Full configuration hierarchy (CLI args > env vars > config files > defaults)
- Configuration validation
- Multiple project support

---

*Extracting hardcoded paths is the first step toward a fully configurable RALF system.*
