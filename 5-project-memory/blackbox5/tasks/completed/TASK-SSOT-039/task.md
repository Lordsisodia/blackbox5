# TASK-SSOT-039: Consolidate Validation Rules

**Status:** completed
**Priority:** LOW
**Created:** 2026-02-06
**Completed:** 2026-02-07
**Parent:** SSOT Violations - CLAUDE.md Scope Mixing

## Objective
Split CLAUDE.md into hierarchical levels (Global, Project, Task) to separate universal instructions from project-specific and task-specific content.

## Success Criteria
- [x] Global CLAUDE.md audited for project-specific content
- [x] Project CLAUDE.md created at `5-project-memory/blackbox5/.claude/CLAUDE.md`
- [x] Project file includes BlackBox5-specific commands and workflows
- [x] Global CLAUDE.md cleaned to contain only universal standards
- [x] Hierarchical loading order documented (Global → Project → Task)
- [x] Task-level CLAUDE.md capability implemented
- [x] All project-specific references removed from global file

## Context
CLAUDE.md currently mixes global instructions with project-specific content, creating scope confusion, maintenance issues when project changes require global edits, portability problems, and uncontrolled growth of the global file. The solution requires a hierarchical structure with clear separation between universal and specific instructions.

## Approach
1. Audit global CLAUDE.md to identify project-specific content (BlackBox5 commands, directory references, task workflows)
2. Create `.claude/` directory in project root
3. Create project CLAUDE.md with BlackBox5-specific instructions
4. Clean global CLAUDE.md to retain only universal coding standards and best practices
5. Document the three-level hierarchy and loading order

## Implementation Summary

### Decision: Rules-Based Approach is Sufficient

The project already has a well-organized rules-based structure at `~/.blackbox5/5-project-memory/blackbox5/.claude/rules/` with 8 rule files covering all behavioral aspects:

1. **001-one-task-per-session.md** - One task per session rule
2. **002-read-before-change.md** - Read before change rule
3. **003-git-safety.md** - Git safety protocol
4. **004-phase-1-5-skill-check.md** - Mandatory skill checking
5. **005-superintelligence-auto-activation.md** - Superintelligence protocol activation
6. **006-stop-conditions.md** - When to pause and exit
7. **007-sub-agent-deployment.md** - Sub-agent deployment rules
8. **008-output-style.md** - Output style guidelines

### What Was Created

1. **Project-Level CLAUDE.md** (`~/.blackbox5/5-project-memory/blackbox5/.claude/CLAUDE.md`)
   - References the rules/ directory
   - Contains BlackBox5-specific workflows (bb5 commands, directory structure)
   - Documents the hierarchical loading order
   - Includes skill selection guidelines specific to BlackBox5

2. **Cleaned Global CLAUDE.md** (`~/.claude/CLAUDE.md`)
   - Removed all BlackBox5-specific content
   - Added hierarchy documentation section
   - Retains universal principles (read before change, git safety, stop conditions)
   - Version bumped to 2.1.0

### Hierarchy Established

```
1. Global (~/.claude/CLAUDE.md) - Universal coding standards
2. Project (.claude/CLAUDE.md) - Project-specific workflows
3. Rules (.claude/rules/*.md) - Behavioral rules
4. Task (CLAUDE.md in task dir) - Task-specific context
```

## Files Modified
- `/Users/shaansisodia/.claude/CLAUDE.md` - Cleaned to universal standards only
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.claude/CLAUDE.md` - Created with BlackBox5-specific content

## Estimated Effort
2-3 hours

## Actual Effort
1 hour

## Rollback Strategy
If hierarchical structure causes confusion, merge files back together while maintaining clear section separation with explicit headers indicating scope.
