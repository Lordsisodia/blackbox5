# TASK-1769911099: Fix Duration Tracking in Executor Metadata

**Type:** fix
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T14:50:00Z
**Improvement:** IMP-1769903011

## Objective

Fix the critical bug where executor metadata records wall-clock elapsed time instead of actual work time for task durations.

## Context

**Problem Identified:** Duration tracking in executor runs is fundamentally broken. Analysis of runs 0031, 0032, and 0034 shows ~12 hours recorded for ~30 minute tasks (24-25x error).

**Root Cause:**
```yaml
# Current behavior:
# At task start: timestamp_start written, timestamp_end = null
# At task completion: timestamp_end NOT updated
# At later read: timestamp_end calculated as (current_time - start_time)
# Result: Wall-clock elapsed time recorded instead of work time
```

**Impact:**
- **Velocity tracking:** Cannot measure true throughput
- **Trend analysis:** Duration trends meaningless
- **Estimation accuracy:** Cannot compare estimated vs actual
- **Capacity planning:** Cannot predict completion times

## Success Criteria

- [ ] Executor updates `timestamp_end` at actual task completion (not at read time)
- [ ] Duration calculated as `completion_time - start_time` (not `current_time - start_time`)
- [ ] Duration validation added: flag durations > 4 hours for review
- [ ] Test with 3+ tasks to confirm accurate tracking
- [ ] Document fix in knowledge/analysis/duration-tracking-fix-20260201.md

## Approach

### Phase 1: Analysis and Planning (10 min)
1. Read current executor prompt: `2-engine/.autonomous/prompts/system/executor/variations/v2-legacy-based.md`
2. Find the "Update Loop Metadata" section at end of prompt
3. Identify exact location where `timestamp_end: "$NOW"` is set
4. Understand why `NOW` is current time instead of completion time

### Phase 2: Design Fix (10 min)
1. The issue: Executor writes metadata at END of loop using `$NOW` (current time)
2. Solution: Executor must capture completion timestamp at task completion
3. Implementation options:
   - **Option A:** Add completion timestamp capture in executor workflow before signaling completion
   - **Option B:** Modify metadata update to use stored completion time instead of `$(date -u +%Y-%m-%dT%H:%M:%SZ)`
4. Choose best option and document rationale

### Phase 3: Implementation (15 min)
1. Modify executor prompt to capture completion timestamp
2. Update metadata template to use completion time
3. Add duration validation:
   ```bash
   # Add to metadata update section
   if [[ $duration_seconds -gt 14400 ]]; then
     echo "WARNING: Duration > 4 hours. Possible metadata error."
     # Flag for review in notes section
   fi
   ```
4. Test with dry-run to verify syntax

### Phase 4: Validation (10 min)
1. Create test task or wait for next executor run
2. Verify duration is accurate (should be < 2 hours for typical tasks)
3. Check metadata.yaml shows correct timestamp_end
4. Confirm duration_seconds matches actual work time

## Files to Modify

- `2-engine/.autonomous/prompts/system/executor/variations/v2-legacy-based.md`
  - Section: "Update Loop Metadata (REQUIRED)"
  - Change: Capture completion timestamp at task completion, not at metadata update
  - Add: Duration validation (> 4 hours warning)

- `.templates/runs/executor-metadata.yaml.template` (if exists)
  - Add: `completion_timestamp` field
  - Add: Duration validation notes

## Notes

**Critical Finding from Analysis:**
- Runs 0031, 0032, 0034: ~12 hours recorded for ~30 minute tasks
- Pattern: timestamp_end shows current read time, not completion time
- Root cause: `$NOW` in prompt is `$(date -u +%Y-%m-%dT%H:%M:%SZ)` which evaluates at read time

**Fix Strategy:**
1. Executor must capture completion timestamp IMMEDIATELY after completing THOUGHTS.md, RESULTS.md, DECISIONS.md
2. Store completion time in environment variable or file
3. Use stored completion time for metadata update instead of `$NOW`

**Example Fix:**
```bash
# After writing THOUGHTS.md, RESULTS.md, DECISIONS.md:
COMPLETION_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "$COMPLETION_TIME" > "$RUN_DIR/.completion_timestamp"

# Later in metadata update:
COMPLETION_TIME=$(cat "$RUN_DIR/.completion_timestamp" 2>/dev/null || echo "$NOW")
duration_seconds=$(( $(date -d "$COMPLETION_TIME" +%s) - $(date -d "$START_TIME" +%s) ))
```

**Dependencies:**
- Related to improvement IMP-1769903011
- Blocks accurate velocity tracking
- Blocks estimation accuracy analysis

**Warnings:**
- Test fix thoroughly before deploying
- Monitor first 3 runs after fix to ensure accuracy
- If fix fails, revert to current broken state (better than corrupted data)

**Estimated Time:** 45 minutes
**Context Level:** 2 (requires understanding of executor workflow)
**Risk:** Medium (modifying core executor behavior)
