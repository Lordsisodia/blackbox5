# TASK-INFR-002 Analysis: Skill Metrics Completely Unpopulated

## Task Summary

The skill metrics system exists but has zero usage data because `calculate-skill-metrics.py` depends on `task_outcomes` entries in `skill-metrics.yaml` that are never populated. The learning index shows 80+ learnings claimed but none indexed, indicating a disconnect between task execution and metrics collection.

## Key Files Involved

- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/calculate-skill-metrics.py` - Main calculator script
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-metrics.yaml` - Metrics data file (has schema, no outcomes)
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-usage.yaml` - Usage tracking file
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-selection.yaml` - Selection framework
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/hooks/task_completion_skill_recorder.py` - Hook for recording

## Estimated Complexity

**Medium** - The infrastructure exists but needs:
1. A data source integration (task outcomes need to be written during task completion)
2. Hook activation in the task completion workflow
3. Potentially backfilling historical data

## Dependencies

- TASK-INFR-010 (Learning Index) - Both share the root cause: missing extraction/aggregation
- Task completion hook system must be operational

## Recommended Approach

1. **Investigate the hook system** - Check if `task_completion_skill_recorder.py` is being called
2. **Add outcome logging** - Ensure task completion writes to `skill-metrics.yaml` `task_outcomes` array
3. **Run calculator** - Execute `calculate-skill-metrics.py` to populate metrics
4. **Verify** - Check that effectiveness scores are calculated (currently all null)

## Root Cause

The calculator script works correctly (line 513-517 shows it looks for `task_outcomes`), but no outcomes are being recorded. The hook exists at `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/hooks/task_completion_skill_recorder.py` but may not be integrated into the task completion workflow.
