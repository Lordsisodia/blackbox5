# TASK-1738366802: Archive Analyzed Runs and Update Lifecycle

**Type:** organize
**Priority:** medium
**Status:** pending
**Created:** 2026-02-01T05:00:00Z
**Source:** STATE.yaml runs section

---

## Objective

Organize the 47 completed runs by moving analyzed runs to archived/ and updating STATE.yaml counts.

## Context

STATE.yaml shows:
- runs/completed/: 47 runs
- runs/archived/: 0 runs

Per the run lifecycle (active → completed → archived), runs that have been analyzed should be moved to archived/.

The analysis in knowledge/analysis/autonomous-runs-analysis.md indicates the 47 runs have already been analyzed.

## Success Criteria

- [ ] Identify which runs in completed/ have been analyzed
- [ ] Move analyzed runs from completed/ to archived/
- [ ] Update STATE.yaml run counts
- [ ] Ensure run lifecycle is properly documented
- [ ] Verify no data loss during move

## Approach

1. List all runs in runs/completed/
2. Cross-reference with analysis document
3. Create runs/archived/ if doesn't exist
4. Move analyzed runs (preserve directory structure)
5. Update STATE.yaml:
   - runs.completed.count
   - runs.archived.count
   - last_updated timestamp

## Files to Modify

- STATE.yaml (update run counts)

## Commands to Run

```bash
# Ensure archived directory exists
mkdir -p /Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/runs/archived

# Move analyzed runs (example)
mv runs/completed/run-1769* runs/archived/  # adjust based on analysis
```

## Notes

- Keep recent completed runs (last 5) in completed/ for quick reference
- Preserve all files within each run directory
- Update both the runs section and any activity metrics
