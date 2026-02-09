# PLAN.md: Migrate Engine Scripts to Project

**Task:** TASK-ARCH-061
**Type:** Structural Architecture
**Status:** pending
**Created:** 2026-02-06

## Objective
Move 8 BlackBox5-specific scripts from 2-engine/.autonomous/bin/ to 5-project-memory/blackbox5/bin/

## Scripts to Migrate
1. scout-intelligent.py (19.5KB)
2. scout-analyze.py (18.3KB)
3. scout-task-based.py (12.1KB)
4. planner-prioritize.py (14.7KB)
5. executor-implement.py (14.9KB)
6. verifier-validate.py (12.1KB)
7. improvement-loop.py (11.2KB)
8. intelligent-scout.sh (11.8KB)

## Prompts to Migrate
1. ralf-improvement-loop.md
2. ralf-scout-improve.md

## Key Changes Required
- improvement-loop.py: Update BIN_DIR from ENGINE_DIR/.autonomous/bin to SCRIPT_DIR
- All other scripts: No path changes needed (PROJECT_DIR already correct)

## Migration Steps
1. Copy all 8 scripts to project bin/
2. Update improvement-loop.py BIN_DIR reference
3. Copy 2 prompts to project .autonomous/prompts/
4. Create thin wrapper scripts in engine for backward compatibility
5. Test all scripts

## Timeline
- Pre-Migration Setup: 15 min
- Migrate Scripts: 45 min
- Migrate Prompts: 10 min
- Create Wrappers: 20 min
- Testing: 1 hour
- Total: ~3 hours

## Success Criteria
- [ ] All 8 scripts exist in project bin/
- [ ] All 2 prompts exist in project .autonomous/prompts/
- [ ] improvement-loop.py can find other scripts
- [ ] Wrapper scripts in engine delegate correctly
- [ ] All tests pass
