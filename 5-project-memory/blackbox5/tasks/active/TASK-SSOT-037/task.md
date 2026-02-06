# TASK-SSOT-037: Unify Agent Identity and State

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** SSOT Violations - Decision Scattering

## Objective
Create a centralized decision registry to consolidate decisions scattered across run folders, enabling decision discovery, history tracking, and pattern analysis.

## Success Criteria
- [ ] Central decision registry schema defined at `.autonomous/decisions.yaml`
- [ ] Decision structure includes all required fields (id, timestamp, phase, selected_option, rationale)
- [ ] Migration script created to extract decisions from run folders
- [ ] All historical decisions migrated from `runs/**/DECISIONS.yaml` and `runs/**/THOUGHTS.md`
- [ ] Decision recording updated to write to central registry
- [ ] Query interface created for searching decisions by task_id, phase, and reversibility
- [ ] Indexes generated for efficient querying (by_task, by_phase, by_reversibility)

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
