# PLAN.md: Create Path Resolution Library

**Task:** TASK-ARCH-065
**Status:** pending
**Created:** 2026-02-06

## Objective
Create paths.sh (bash) and paths.py (Python) libraries to eliminate 47+ hardcoded cross-boundary paths.

## Library API

### paths.sh (Bash Functions)
```bash
get_blackbox5_root()      # ~/.blackbox5
get_engine_path()         # 2-engine
get_project_path()        # 5-project-memory/blackbox5
get_routes_path()         # routes.yaml
get_runs_path()           # .autonomous/runs
get_tasks_path()          # tasks/
get_memory_path()         # .autonomous/memory
get_analysis_path()       # .autonomous/analysis
```

### paths.py (Python Class)
```python
class PathResolver:
    @property
    def engine_path(self) -> Path
    @property
    def project_path(self) -> Path
    @property
    def routes_path(self) -> Path
    def get_path(self, *parts) -> Path
```

## Implementation Steps
1. Create paths.sh with all bash functions (2 hours)
2. Create paths.py with PathResolver class (2 hours)
3. Write unit tests (1 hour)
4. Update 6 agent scripts to use library (4 hours)
5. Update shell scripts (1 hour)
6. Verify zero hardcoded paths remain (1 hour)

## Files to Create
- `2-engine/.autonomous/lib/paths.sh`
- `2-engine/.autonomous/lib/paths.py`
- `2-engine/.autonomous/lib/test_paths.py`

## Timeline
- Total: 4-6 hours

## Success Criteria
- [ ] paths.sh created with all required functions
- [ ] paths.py created with PathResolver class
- [ ] All 6 agent scripts updated
- [ ] Zero hardcoded paths remain (verified by grep)
- [ ] All tests pass
