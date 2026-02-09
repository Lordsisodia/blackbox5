# TASK-SSOT-034: Merge Duplicate Documentation

**Status:** completed
**Priority:** MEDIUM
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 60

---

## Objective

Merge fragmented run output files (THOUGHTS.md, DECISIONS.yaml, ASSUMPTIONS.md, RESULTS.md, LEARNINGS.md) into a single unified RUN.yaml file per run.

---

## Success Criteria

- [x] Migration script created to merge run files into RUN.yaml
- [x] All existing runs migrated to unified format
- [x] New run template created using unified format
- [x] Documentation updated with new run structure
- [x] Old file formats deprecated

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

## Implementation Summary

### Completed: 2026-02-07

### Files Created/Modified:

1. **`~/.blackbox5/bin/consolidate-run.sh`** (NEW)
   - Bash script to merge THOUGHTS.md, DECISIONS.md|yaml, ASSUMPTIONS.md, RESULTS.md, LEARNINGS.md
   - Supports --dry-run, --all, --keep flags
   - Parses markdown structure and converts to YAML
   - Processes 300 runs in ~30 seconds

2. **`~/.blackbox5/bin/ralf-tools/ralf-session-start-hook.sh`** (MODIFIED)
   - Now creates unified RUN.yaml instead of separate files
   - Includes all sections: metadata, context, thoughts, decisions, assumptions, results, learnings
   - Maintains backward compatibility with source_files reference

3. **RUN.yaml Schema** (NEW STANDARD)
   ```yaml
   run_id: "run-YYYYMMDD-HHMMSS"
   timestamp: "ISO8601"
   project: "project-name"
   agent: "agent-type"
   status: "initialized|in_progress|completed"
   git_branch: "branch-name"
   git_commit: "commit-hash"

   context:
     active_tasks: []
     queue_depth: 0
     previous_run_status: unknown

   thoughts: |
     [Multi-line reasoning content]

   decisions:
     - id: "DEC-001"
       title: "..."
       context: "..."
       decision: "..."
       rationale: "..."

   assumptions:
     - id: "ASM-001"
       assumption: "..."
       validation_method: "..."
       validation_result: "pending|confirmed|rejected"
       confidence: "LOW|MEDIUM|HIGH"

   results:
     status: "..."
     summary: "..."
     tasks_completed: []
     tasks_created: []
     blockers: []

   learnings:
     - id: "LRN-001"
       title: "..."
       what_worked: "..."
       takeaway: "..."

   source_files:
     - RUN.yaml
   ```

### Migration Results:
- **Total runs processed:** 300
- **Successfully consolidated:** 275
- **Skipped (no source files):** 25
- **Failed:** 0

### Benefits:
1. **Single source of truth** - All run data in one file
2. **Machine readable** - YAML structure enables programmatic access
3. **Human readable** - Clear section organization
4. **Extensible** - Easy to add new sections
5. **Reduced fragmentation** - No more file switching during analysis

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
