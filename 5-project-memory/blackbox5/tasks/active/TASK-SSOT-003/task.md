# TASK-SSOT-003: Consolidate Run Folders to Single Location

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #17 - SSOT Run/Agent Outputs Violations

## Objective
Move all run folders from scattered locations into a single canonical runs/ directory.

## Success Criteria
- [ ] Move .autonomous/agents/planner/runs/* to runs/planner/
- [ ] Move .autonomous/agents/architect/runs/* to runs/architect/
- [ ] Move .autonomous/agents/executor/runs/* to runs/executor/
- [ ] Move .autonomous/agents/analyzer/runs/* to runs/analyzer/
- [ ] Move .autonomous/runs/* to runs/general/
- [ ] Move 5-project-memory/blackbox5/runs/* to runs/ (consolidate)
- [ ] Update all scripts that reference run paths
- [ ] Create migration log

## Context
Run folders exist in 10+ locations:
- .autonomous/agents/*/runs/ (4 agent types, ~117 runs)
- .autonomous/runs/ (~7 runs)
- runs/ (~130 runs)
- tasks/active/TASK-*/runs/ (~20 runs)
- goals/active/IG-*/runs/ (~5 runs)
- 5-project-memory/blackbox5/runs/ (~200 runs - duplicate!)

## Approach
1. Create new runs/{agent-type}/ directory structure
2. Move runs in batches (by agent type)
3. Update scripts to use new paths
4. Verify no broken references
5. Delete old directories after verification

## Related Files
- All agent scripts that write to run folders
- bin/bb5-* commands that read run data
- heartbeat.yaml (references run numbers)

## Rollback Strategy
Keep old directories until verification complete. Can restore if needed.
