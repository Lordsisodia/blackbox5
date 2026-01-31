# TASK-1769892003: Archive Old Runs and Update Run Lifecycle

**Task ID:** TASK-1769892003
**Type:** organize
**Priority:** medium
**Status:** pending
**Created:** 2026-02-01T04:30:00Z

## Objective
Organize the completed runs by archiving old ones and ensuring proper run lifecycle management.

## Context
STATE.yaml shows 47 total runs with 5 in completed/ and 42 already archived. This task ensures the remaining completed runs that have been analyzed are properly archived, and documents the run lifecycle process.

## Success Criteria
- [ ] Review runs in completed/ directory
- [ ] Move analyzed runs to archived/
- [ ] Update STATE.yaml run counts
- [ ] Document run lifecycle: active → completed → archived

## Approach
1. Check runs/completed/ for runs ready to archive
2. Verify runs have been analyzed (have LEARNINGS.md, DECISIONS.md)
3. Move appropriate runs to runs/archived/
4. Update STATE.yaml with accurate counts
5. Document the lifecycle process

## Files to Modify
- `STATE.yaml`: Update run counts
- `runs/completed/`: Move old runs to archived/

## Dependencies
- None

## Notes
Only archive runs that have been fully analyzed. Ensure all required files exist before moving.
