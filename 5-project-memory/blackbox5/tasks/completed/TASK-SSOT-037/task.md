# TASK-SSOT-037: Cleanup Per-Run Decision Files

**Status:** completed
**Priority:** HIGH
**Created:** 2026-02-06
**Completed:** 2026-02-07
**Parent:** SSOT Violations - Decision Scattering

## Objective
Cleanup per-run DECISIONS.md files after central decision registry has been populated.

## Success Criteria
- [x] Central decision registry verified at `.autonomous/decisions/decision_registry.yaml`
- [x] All per-run DECISIONS.md files deleted (280 files removed)
- [x] Hook script verified to not create separate DECISIONS.md files

## Results

### Cleanup Summary
- **Central Registry:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/decisions/decision_registry.yaml`
- **Registry Stats:** 864 decisions from 107 source files
- **Files Deleted:** 280 per-run DECISIONS.md files
- **Hook Status:** Already compliant - creates only RUN.yaml with embedded decisions section

### Files Cleaned
Per-run DECISIONS.md files removed from:
- `runs/planner/run-*/DECISIONS.md` (80+ files)
- `runs/executor/run-*/DECISIONS.md` (60+ files)
- `runs/architect/run-*/DECISIONS.md` (20+ files)
- `runs/research/*/DECISIONS.md` (10+ files)
- `runs/unknown/*/DECISIONS.md` (100+ files)
- `runs/archived/*/DECISIONS.md` (10+ files)

### Hook Verification
`ralf-session-start-hook.sh` already creates unified `RUN.yaml` with decisions embedded:
- No separate DECISIONS.md file creation
- Decisions section exists within RUN.yaml template
- No changes required to hook script

## Context
Decisions are currently scattered across run folders in multiple formats, making it difficult to discover all decisions, track decision evolution over time, analyze decision patterns, and maintain consistent formatting. The solution requires a central registry with structured format, searchable indexes, and referential links to runs and tasks.

## Approach
1. Define decision registry schema with comprehensive fields (context, options_considered, assumptions, reversibility, rollback_steps, verification)
2. Create migration script to extract and consolidate decisions from all run folders
3. Update DecisionRegistry class to write to central file
4. Implement query interface with filtering capabilities
5. Generate indexes for efficient searching

## Estimated Effort
4-5 hours

## Rollback Strategy
If central registry fails, maintain backups of original run folder decisions and revert to per-run decision recording while fixing the central registry implementation.
