# TASK-SSOT-034: Merge Duplicate Documentation

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 60

---

## Objective

Merge fragmented run output files (THOUGHTS.md, DECISIONS.yaml, ASSUMPTIONS.md, RESULTS.md, LEARNINGS.md) into a single unified RUN.yaml file per run.

---

## Success Criteria

- [ ] Migration script created to merge run files into RUN.yaml
- [ ] All existing runs migrated to unified format
- [ ] New run template created using unified format
- [ ] Documentation updated with new run structure
- [ ] Old file formats deprecated

---

## Context

Run outputs are currently split across multiple files:
- `THOUGHTS.md` - Thoughts and reasoning
- `DECISIONS.yaml` - Decisions made
- `ASSUMPTIONS.md` - Assumptions
- `RESULTS.md` - Results
- `LEARNINGS.md` - Learnings

This creates:
1. **Fragmented Context**: Need to read multiple files to understand a run
2. **Inconsistent Formats**: Mix of Markdown and YAML
3. **Query Complexity**: Hard to get complete picture programmatically
4. **Navigation Overhead**: Constant file switching during analysis

---

## Approach

### Phase 1: Create Migration Script (2 hours)
1. Build Python script to parse and merge all run file types
2. Handle Markdown (THOUGHTS, ASSUMPTIONS, RESULTS, LEARNINGS)
3. Handle YAML (DECISIONS)
4. Output unified RUN.yaml with structured sections

### Phase 2: Run Migration (1 hour)
1. Execute migration on all existing runs
2. Verify merged content integrity
3. Handle edge cases (missing files, malformed content)
4. Create backup of original files

### Phase 3: Update Templates (1 hour)
1. Create new run template using unified RUN.yaml format
2. Update run initialization scripts
3. Document new structure for agents

---

## Rollback Strategy

If unified format causes issues:
1. Keep original files until new format is validated
2. Restore individual files if needed
3. Consider hybrid approach (unified + individual)

---

## Notes

**Key Insight:** The unified format should be:
- Machine readable (YAML structure)
- Human readable (clear section organization)
- Extensible (easy to add new sections)

**Schema Design:**
```yaml
run_id: "run-20260205_143022"
timestamp: "2026-02-05T14:30:22Z"
task_id: "TASK-001"
agent: "claude"

thoughts: []
decisions: []
assumptions: []
results: {}
learnings: []
```
