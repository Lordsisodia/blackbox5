# TASK-1769911000: Lower skill confidence threshold from 80% to 70%

**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T10:05:00Z

## Objective
Lower the skill confidence threshold from 80% to 70% to enable actual skill invocations while maintaining quality.

## Context
Analysis from TASK-1769910000 confirmed that the 80% confidence threshold is blocking valid skill invocations. Run-0022 showed 70% confidence for a valid bmad-analyst skill match, but the 80% threshold prevented invocation. Evidence supports lowering to 70% to achieve the target 50% skill invocation rate.

## Success Criteria
- [ ] Update confidence threshold from 80% to 70% in all relevant files
- [ ] Update operations/skill-selection.yaml with new threshold
- [ ] Update 2-engine/.autonomous/prompts/ralf-executor.md if threshold is hardcoded
- [ ] Document the threshold change rationale
- [ ] Verify threshold change in next executor run

## Files to Modify
- operations/skill-selection.yaml: Update threshold value
- 2-engine/.autonomous/prompts/ralf-executor.md: Update threshold if present
- operations/skill-metrics.yaml: Document threshold change

## Approach
1. Read current skill-selection.yaml to understand threshold configuration
2. Update threshold from 80% to 70%
3. Check ralf-executor.md for hardcoded threshold references
4. Update skill-metrics.yaml with threshold change history
5. Document rationale in DECISIONS.md

## Notes
- Threshold change is based on empirical evidence from 4+ executor runs
- Run-0022: 70% confidence for bmad-analyst (analysis task) - VALID match
- Target: Enable 50% skill invocation rate
- Risk: Low - 70% still ensures quality matches
