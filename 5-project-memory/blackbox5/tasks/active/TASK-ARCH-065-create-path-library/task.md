# TASK-ARCH-065: Create Path Resolution Library

**Status:** pending
**Priority:** CRITICAL
**Created:** 2026-02-06
**Type:** Structural Architecture

## Objective
Create a path resolution library that abstracts all hardcoded paths between engine and project, eliminating 47+ hardcoded cross-boundary references.

## Background
Scout analysis found 47+ hardcoded paths crossing between 2-engine/ and 5-project-memory/blackbox5/. This creates tight coupling and makes the engine non-reusable.

## Library Requirements

### Shell Library (paths.sh)
Functions needed:
- `get_engine_path()` - Returns 2-engine/ path
- `get_project_path()` - Returns project path (parameterized)
- `get_routes_path()` - Returns routes.yaml path
- `get_runs_path()` - Returns runs directory
- `get_tasks_path()` - Returns tasks directory
- `get_memory_path()` - Returns memory directory

### Python Library (paths.py)
Class needed:
```python
class PathResolver:
    def __init__(self, project_name: str = None)
    def get_engine_path(self) -> Path
    def get_project_path(self) -> Path
    def get_routes_path(self) -> Path
    def get_runs_path(self) -> Path
    def get_tasks_path(self) -> Path
    def get_memory_path(self) -> Path
```

## Scripts to Update

1. scout-intelligent.py
2. executor-implement.py
3. improvement-loop.py
4. planner-prioritize.py
5. verifier-validate.py
6. scout-task-based.py

## Success Criteria
- [ ] paths.sh created with all required functions
- [ ] paths.py created with PathResolver class
- [ ] All 6 agent scripts updated to use library
- [ ] Zero hardcoded paths remain (verified by grep)
- [ ] Backward compatibility maintained

## Context
- Scout report: `.autonomous/analysis/cross-boundary-paths.md`
- Migration strategy: `.autonomous/analysis/migration-strategy.md`

## Approach
1. Create paths.sh library
2. Create paths.py library
3. Update each agent script one by one
4. Test each script after update
5. Run grep to verify no hardcoded paths remain

## Dependencies
- TASK-ARCH-064 (routes.yaml fix) - should be done first

## Rollback Strategy
- Keep old path code commented during transition
- One-command rollback script

## Estimated Effort
4-6 hours

## Related Tasks
- TASK-ARCH-060: Path abstraction layer (parent)
- TASK-ARCH-061: Migrate engine scripts to project
