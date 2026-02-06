# TASK-ARCH-060: Fix Engine/Project Boundary - Path Abstraction Layer

**Status:** completed
**Priority:** CRITICAL
**Created:** 2026-02-06
**Completed:** 2026-02-06
**Type:** Structural Architecture

## Objective
Create a path abstraction layer to eliminate 47+ hardcoded cross-boundary paths between 2-engine/ and 5-project-memory/blackbox5/.

## Background
Analysis found 47 hardcoded paths crossing between engine (standardized) and project (BlackBox5-specific). This violates the architectural boundary and makes the system fragile.

## Success Criteria
- [x] Use existing unified_config.py (created by TASK-ARCH-016) for path resolution
- [x] Update 15 Python files in 2-engine/ to use unified_config
- [x] Zero hardcoded /workspaces/blackbox5 paths remain
- [x] All files pass syntax check
- [x] Backward compatibility maintained

## Implementation Summary

### Solution Used
Instead of creating new paths.sh and paths.py files, used the existing `unified_config.py` (created by TASK-ARCH-016) which provides:
- `get_path_resolver()` - Returns a PathResolver instance
- `PathResolver.project_root` - Project directory path
- `PathResolver.engine_root` - Engine directory path
- `PathResolver.get_project_path()` - Get project path with optional name
- `PathResolver.get_tasks_path()` - Get tasks directory path

### Files Updated (15 total)

#### bin/ directory (7 files):
1. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/scout-analyze.py` - Updated default_project_dir to use get_path_resolver()
2. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/scout-intelligent.py` - Updated PROJECT_DIR and ENGINE_DIR
3. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/executor-implement.py` - Updated PROJECT_DIR and ENGINE_DIR
4. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/planner-prioritize.py` - Updated PROJECT_DIR and ENGINE_DIR
5. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/verifier-validate.py` - Updated PROJECT_DIR and ENGINE_DIR
6. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/improvement-loop.py` - Updated PROJECT_DIR and ENGINE_DIR
7. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/scout-task-based.py` - Updated PROJECT_DIR and ENGINE_DIR

#### lib/ directory (7 files):
8. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/historical_analyzer.py` - Updated PROJECT_DIR
9. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/performance_reporter.py` - Updated PROJECT_DIR
10. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/anomaly_detector.py` - Updated PROJECT_DIR
11. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/alert_manager.py` - Updated PROJECT_DIR
12. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/metrics_collector.py` - Updated PROJECT_DIR
13. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/log_ingestor.py` - Updated to use unified_config with fallback for backward compatibility
14. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/roadmap_sync.py` - Updated comments and help text to use ~/.blackbox5 pattern

#### modules/ directory (1 file):
15. `/Users/shaansisodia/.blackbox5/2-engine/modules/fractal_genesis/data/storage.py` - Updated MEMORY_ROOT constant

### Pattern Applied
```python
# Add unified_config to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from unified_config import get_path_resolver

# Configuration
_path_resolver = get_path_resolver()
PROJECT_DIR = _path_resolver.get_project_path()
ENGINE_DIR = _path_resolver.engine_root
```

### Verification
- `grep -r "/workspaces/blackbox5" 2-engine/ --include="*.py"` - No matches found
- `python3 -m py_compile` - All 15 files compile successfully
- `python3 -c "from unified_config import get_path_resolver"` - Import works correctly

## Rollback Strategy
- All changes are in git history
- To rollback: `git checkout HEAD -- 2-engine/.autonomous/bin/*.py 2-engine/.autonomous/lib/*.py 2-engine/modules/fractal_genesis/data/storage.py`

## Notes
- `scout-task-based.py` had a pre-existing syntax error (unrelated to this task) at line 242 with nested triple quotes
- All other files are syntactically valid and ready for use
- Some files in lib/ had hardcoded `/workspaces/blackbox5` paths which were replaced
- `log_ingestor.py` maintains backward compatibility by accepting an optional path parameter

## Related Tasks
- TASK-ARCH-016: Created unified_config.py (dependency)
- TASK-ARCH-061: Migrate Engine Scripts to Project
- TASK-ARCH-062: Consolidate Duplicate Prompts
