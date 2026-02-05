# TASK-SSOT-007: Extract Decisions to Central Registry

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #14 - SSOT Knowledge Violations

## Objective
Extract all decisions from 242+ run folder DECISIONS.md files into the central registry.

## Success Criteria
- [ ] Scan all run folders for DECISIONS.md files
- [ ] Extract decisions with metadata (timestamp, agent, run_id)
- [ ] Add to .autonomous/memory/decisions/registry.md
- [ ] Create decision ID format
- [ ] Update run folders to reference decisions by ID
- [ ] Archive old decision files after extraction

## Context
Current state:
- Central registry shows "Total Decisions: 0"
- 242+ DECISIONS.md files in run folders contain detailed decisions
- Decisions are NOT extracted to central registry

## Approach
1. Find all DECISIONS.md files across run folders
2. Parse decision entries
3. Add to registry.md with unique IDs
4. Create cross-references (run_id -> decision_ids)
5. Archive run folder decisions after verification

## Related Files
- .autonomous/memory/decisions/registry.md
- */runs/*/DECISIONS.md (242+ files)
- .autonomous/agents/planner/runs/*/DECISIONS.md
- .autonomous/agents/architect/runs/*/DECISIONS.md

## Rollback Strategy
Keep all original files until extraction verified.
