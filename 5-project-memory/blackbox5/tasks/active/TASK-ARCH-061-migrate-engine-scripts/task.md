# TASK-ARCH-061: Migrate BlackBox5-Specific Scripts from Engine to Project

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Type:** Structural Architecture

## Objective
Move 8 BlackBox5-specific scripts from 2-engine/.autonomous/bin/ to 5-project-memory/blackbox5/.autonomous/bin/

## Background
Engine scripts contain hardcoded BlackBox5 paths. They should live in the project since they're project-specific implementations.

## Scripts to Migrate
1. scout-intelligent.py
2. scout-analyze.py
3. scout-task-based.py
4. planner-prioritize.py
5. executor-implement.py
6. verifier-validate.py
7. improvement-loop.py
8. intelligent-scout.sh

## Success Criteria
- [ ] All 8 scripts moved to project .autonomous/bin/
- [ ] Scripts updated to use path abstraction (from TASK-ARCH-060)
- [ ] Symlinks or wrappers created in engine for backward compatibility
- [ ] All references updated
- [ ] Tests pass

## Context
- Analysis: `.autonomous/analysis/engine-content-analysis.md`
- Duplications: `.autonomous/analysis/engine-project-duplications.md`

## Approach
1. Move scripts to project location
2. Update import paths
3. Create thin wrappers in engine that delegate to project
4. Update documentation
5. Test all 8 scripts still work

## Dependencies
- TASK-ARCH-060 (path abstraction layer)

## Rollback Strategy
- Keep copies in engine until verified working
- One-command restore script

## Estimated Effort
3-4 hours
