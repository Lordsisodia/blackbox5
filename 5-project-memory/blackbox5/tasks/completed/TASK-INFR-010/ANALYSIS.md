# TASK-INFR-010 Analysis: Learning Index Shows Zero Learnings

## Task Summary

The learning index at `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/memory/insights/learning-index.yaml` shows `total_learnings: 0` despite 80+ claimed learnings. The file header states it is "auto-populated by the learning_extractor.py library" but this library does not exist in the codebase.

## Key Files Involved

- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/memory/insights/learning-index.yaml` - Empty learning index
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/memory/insights/LEARNINGS.md` - May contain raw learnings
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/executor/runs/` - Task run folders with THOUGHTS.md/DECISIONS.md
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/hooks/` - Hook scripts directory

## Estimated Complexity

**Medium** - Requires:
1. Creating the missing `learning_extractor.py` library
2. Implementing parsing logic for THOUGHTS.md and DECISIONS.md files
3. Integrating with task completion hooks
4. Backfilling from existing run folders

## Dependencies

- TASK-INFR-002 (Skill Metrics) - Shares similar hook/extraction infrastructure needs
- Task completion workflow must trigger extraction

## Recommended Approach

1. **Create learning_extractor.py** - Implement the library referenced in learning-index.yaml header
2. **Parse run artifacts** - Extract learnings from THOUGHTS.md, DECISIONS.md, LEARNINGS.md in run folders
3. **Structure extraction** - Map to the learning schema (learning_id, task_id, type, category, etc.)
4. **Hook integration** - Call extractor on task completion
5. **Backfill** - Process existing 80+ runs to populate index

## Root Cause

The learning-index.yaml file (line 6) states: "This file is auto-populated by the learning_extractor.py library" but:
- No `learning_extractor.py` exists in the codebase
- No extraction logic is running to populate the `learnings: []` array
- Raw learning data exists in run folders but is never processed

## Reference

The learning-index.yaml schema is well-defined (lines 19-40) with fields for:
- learning_type: pattern, decision, challenge, optimization, bugfix, insight
- category: technical, process, architectural, operational
- severity, effectiveness, frequency tracking
