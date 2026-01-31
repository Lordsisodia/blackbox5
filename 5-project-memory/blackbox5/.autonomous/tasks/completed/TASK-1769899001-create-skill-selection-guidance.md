# TASK-1769899001: Create Skill Selection Guidance Framework

**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T10:05:00Z

## Objective
Add skill selection guidance to ~/.claude/CLAUDE.md to help agents systematically identify and invoke relevant skills for tasks. Currently 21 skills are available but not systematically utilized.

## Context
The CLAUDE.md decision framework analysis (TASK-1769897000) identified a gap: while skills exist in 2-engine/.autonomous/skills/, there's no guidance on when to check for or invoke them. This leads to missed opportunities for using specialized skills like git-workflows, n8n-validation-expert, or testing-patterns.

This aligns with goals.yaml IG-004 (Optimize Skill Usage and Efficiency).

## Success Criteria
- [ ] New "When to Use Skills" section added to CLAUDE.md
- [ ] Skill selection process documented (check → match → apply)
- [ ] Domain-to-skill mapping provided (git, n8n, testing, etc.)
- [ ] Confidence threshold defined (>80%)
- [ ] Skill usage documentation requirements specified
- [ ] Examples of skill invocation patterns included

## Approach
1. Read ~/.claude/CLAUDE.md to find appropriate insertion point (after "Sub-Agent Deployment")
2. Read available skills from 2-engine/.autonomous/skills/ to understand categories
3. Create "When to Use Skills" section with:
   - Trigger conditions (task type, domain keywords)
   - Selection process (read → check → apply)
   - Confidence threshold (>80%)
   - Documentation requirements
4. Add domain-to-skill mapping table
5. Insert section in logical location

## Files to Modify
- ~/.claude/CLAUDE.md: Add "When to Use Skills" section

## Files to Reference
- 2-engine/.autonomous/skills/ (list available skills)
- operations/skill-usage.yaml (skill categories)
- operations/skill-metrics.yaml (effectiveness data)

## Notes
- Keep guidance actionable and specific
- Reference existing skill files for accuracy
- Include examples of when skills were/weren't used
- This complements the sub-agent deployment refinements

## Rollback Strategy
- Git history preserves original CLAUDE.md
- Can revert specific section if needed
- Test by checking if new guidance is readable and clear
