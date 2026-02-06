# TASK-ARCH-061: Move BlackBox5-Specific Scripts from Engine to Project

**Status:** completed
**Priority:** MEDIUM
**Created:** 2026-02-06T00:00:00Z
**Type:** Architecture / Refactoring

## Objective
Move 4 BlackBox5-specific agent scripts from the engine directory to the project directory to improve separation of concerns and project autonomy.

## Scripts to Move
1. `executor-implement.py` - Executor Agent for implementing quick wins
2. `verifier-validate.py` - Verifier Agent for validating improvements
3. `scout-analyze.py` - Improvement Scout Analysis script
4. `scout-task-based.py` - Task-Based Intelligent Scout

## Source
`/Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/`

## Destination
`/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/bin/`

## Success Criteria
- [x] Destination directory created
- [x] All 4 scripts moved to new location
- [x] Import paths updated to point to engine lib
- [x] Scripts verified (3/4 syntax OK, 1 pre-existing issue)
- [x] Task marked as completed
- [x] Task moved to completed folder

## Context
These scripts are part of the Agent Improvement Loop (Scout -> Planner -> Executor -> Verifier) and are specific to the BlackBox5 project. They reference project-specific paths and configurations, making them better suited for the project directory rather than the shared engine directory.

The scripts use `unified_config` from `engine/.autonomous/lib/` which will continue to work via the path resolver that handles cross-directory references.

## Rollback Strategy
If issues arise:
1. Copy scripts back to engine directory
2. Verify functionality
3. Update any references that were changed

## Notes
- Scripts use `sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))` to find unified_config
- In the new location, this will resolve to `project/.autonomous/lib/` which may not exist
- Need to verify the unified_config import strategy works from project location
