# TASK-ARCH-062: Consolidate Duplicate Agent Prompts

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Type:** Structural Architecture

## Objective
Merge duplicate agent prompts between engine and project into canonical engine location.

## Background
Both engine and project have agent prompts with overlapping functionality. Need to consolidate to single source of truth.

## Prompts to Consolidate

| Engine Prompt | Project Prompt | Action |
|--------------|----------------|--------|
| prompts/agents/deep-repo-scout.md | prompts/agents/scout-agent-prompt.md | Merge best of both |
| prompts/agents/implementation-planner.md | prompts/agents/planner-agent-prompt.md | Merge best of both |
| prompts/ralf-executor.md | prompts/agents/executor-agent-prompt.md | Merge best of both |

## Success Criteria
- [ ] 3 merged prompts created in engine location
- [ ] Project prompts updated to reference engine location
- [ ] No duplication remaining
- [ ] All agent workflows tested

## Context
- Analysis: `.autonomous/analysis/engine-project-duplications.md`

## Approach
1. Compare content of each prompt pair
2. Create merged version with best elements from both
3. Update project references
4. Archive old project prompts
5. Test agent workflows

## Rollback Strategy
- Archive old prompts before merging
- Can restore individual prompts if needed

## Estimated Effort
2-3 hours
