# TASK-1769899000: Apply CLAUDE.md Sub-Agent Deployment Refinements

**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T10:05:00Z

## Objective
Apply the sub-agent deployment refinements identified in claude-md-decision-effectiveness.md to ~/.claude/CLAUDE.md, adding file count thresholds and specific guidance for when to use direct reads vs sub-agents.

## Context
The decision framework effectiveness analysis (TASK-1769897000) found that the current "ALWAYS spawn for exploration" guidance is too aggressive. Observed runs show 4-12 file reads work efficiently with direct access. The analysis recommends specific thresholds:
- Spawn sub-agents when: >15 files, complex patterns, cross-project exploration
- Use direct reads when: <15 files, known paths, simple patterns

This aligns with goals.yaml IG-001 (Improve CLAUDE.md Effectiveness).

## Success Criteria
- [ ] Sub-agent deployment section updated with file count thresholds
- [ ] "When to use direct reads" guidance added
- [ ] Examples provided for both approaches
- [ ] Cross-project exploration threshold defined
- [ ] Changes tested by reading updated section

## Approach
1. Read ~/.claude/CLAUDE.md lines 246-292 (decision framework section)
2. Locate "Sub-Agent Deployment" subsection
3. Replace "ALWAYS/NEVER" language with threshold-based guidance
4. Add file count criteria (<15 files = direct, >15 files = sub-agent)
5. Add cross-project criteria (>2 projects = sub-agent)
6. Add time-based criteria (>5 min search = sub-agent)
7. Document changes in DECISIONS.md

## Files to Modify
- ~/.claude/CLAUDE.md: Update sub-agent deployment rules (lines ~280-290)

## Notes
- This is a sensitive file - make minimal, targeted changes
- Preserve existing structure and formatting
- The analysis shows current guidance works but can be optimized
- Consider this a refinement, not a rewrite

## Rollback Strategy
- Original CLAUDE.md is in git
- Can restore with: git checkout ~/.claude/CLAUDE.md
- Document original text in DECISIONS.md before changing
