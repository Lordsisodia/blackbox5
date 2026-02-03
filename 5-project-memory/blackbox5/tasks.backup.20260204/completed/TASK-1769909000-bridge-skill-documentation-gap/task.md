# TASK-1769909000: Bridge Skill Documentation to Execution Gap

**Type:** implement
**Priority:** CRITICAL
**Status:** pending
**Created:** 2026-02-01T07:50:00Z
**Context Level:** 3

## Objective
Bridge the critical gap between skill documentation and actual skill usage in task execution.

## Context
Critical finding from TASK-1769903001 (Validate Skill Effectiveness): Zero skill usage was detected across 5 analyzed runs despite 31 skills being documented in operations/skill-usage.yaml. This represents a significant documentation-execution gap that undermines the entire skill system.

The skills exist, are well-documented, but are not being invoked during task execution. This suggests:
1. Executor is not checking for applicable skills
2. Skill selection criteria are not clear
3. No validation that skills are being used
4. Missing integration between planning and execution

## Success Criteria
- [ ] Executor prompt updated with explicit skill-checking workflow
- [ ] Skill selection decision tree documented in operations/skill-selection.yaml
- [ ] Skill usage validation added to task completion checklist
- [ ] At least 3 skills invoked in test tasks
- [ ] Skill effectiveness metrics updated with actual usage data

## Approach
1. **Update RALF executor prompt** with mandatory skill-checking workflow:
   - Before starting any task, check operations/skill-usage.yaml
   - Match task keywords against skill trigger_keywords
   - If confidence >80%, invoke the skill
   - Document skill usage in THOUGHTS.md

2. **Create skill-selection.yaml** with decision criteria:
   - Task type to skill mapping
   - Confidence threshold rules
   - Fallback behavior when no skill matches

3. **Update task completion template** with skill validation:
   - Was a skill applicable? (yes/no)
   - Was a skill invoked? (yes/no)
   - Skill effectiveness rating

4. **Test with 3 tasks** requiring different skills

## Files to Modify
- 2-engine/.autonomous/prompts/ralf-executor.md
- operations/skill-selection.yaml (create)
- .templates/tasks/task-completion.md.template
- operations/skill-metrics.yaml

## Dependencies
- TASK-1769903001 (completed - validation data)

## Notes
This is a CRITICAL priority task because the entire skill system is non-functional without execution integration.
