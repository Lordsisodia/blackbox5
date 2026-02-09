# TASK-SSOT-012: Merge Run Output Files (4→1 per run)

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Parent:** Issue #17 - SSOT Run/Agent Outputs Violations

## Objective
Merge THOUGHTS.md, DECISIONS.md, LEARNINGS.md, RESULTS.md into single run-report.md per run.

## Success Criteria
- [ ] Design unified run-report.md format with sections
- [ ] Create migration script to merge existing runs
- [ ] Update agent scripts to write to single file
- [ ] Migrate all 482+ existing run folders
- [ ] Delete old 4-file structure after verification
- [ ] Update any scripts that read run outputs

## Context
Each run folder has 4 files:
- THOUGHTS.md (~400 lines)
- DECISIONS.md (~300 lines)
- LEARNINGS.md (~200 lines)
- RESULTS.md (~250 lines)

Total: 1,928 files for 482 runs. Can reduce to 482 files.

## Approach
1. Design run-report.md template with sections
2. Create merge script
3. Test on small batch of runs
4. Migrate all runs
5. Update agent scripts
6. Clean up old files

## Related Files
- */runs/*/THOUGHTS.md
- */runs/*/DECISIONS.md
- */runs/*/LEARNINGS.md
- */runs/*/RESULTS.md
- All agent scripts that write these files

## Rollback Strategy
Keep old files until new format verified.
