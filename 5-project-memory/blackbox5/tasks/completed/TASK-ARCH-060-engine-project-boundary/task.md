# TASK-ARCH-060: Fix Engine/Project Boundary - Path Abstraction Layer

**Status:** completed
**Priority:** CRITICAL
**Created:** 2026-02-06
**Completed:** 2026-02-07
**Type:** Structural Architecture

## Objective
Create a path abstraction layer to eliminate 47+ hardcoded cross-boundary paths between 2-engine/ and 5-project-memory/blackbox5/.

## Background
Analysis found 47 hardcoded paths crossing between engine (standardized) and project (BlackBox5-specific). This violates the architectural boundary and makes the system fragile.

## Success Criteria
- [ ] Create path resolution library in 2-engine/.autonomous/lib/paths.sh
- [ ] Create Python equivalent in 2-engine/.autonomous/lib/paths.py
- [ ] Update all 6 agent scripts in 2-engine/.autonomous/bin/ to use abstraction
- [ ] Fix routes.yaml incorrect path nesting
- [ ] Zero hardcoded paths remain (verified by grep)

## Context
- Analysis: `.autonomous/analysis/engine-project-split-analysis.md`
- Cross-boundary paths: `.autonomous/analysis/cross-boundary-paths.md`
- Migration strategy: `.autonomous/analysis/migration-strategy.md`

## Approach
1. Create paths.sh with functions: get_engine_path(), get_project_path(), get_routes_path()
2. Create paths.py with PathResolver class
3. Update scout-intelligent.py, executor-implement.py, planner-prioritize.py, verifier-validate.py, improvement-loop.py, scout-task-based.py
4. Fix routes.yaml paths
5. Verify with grep -r "5-project-memory/blackbox5" 2-engine/

## Rollback Strategy
- Keep old path definitions commented out during transition
- One-command rollback script to restore hardcoded paths

## Estimated Effort
4-6 hours

## Related Tasks
- TASK-ARCH-061: Migrate Engine Scripts to Project
- TASK-ARCH-062: Consolidate Duplicate Prompts
