# TASK-SSOT-039: Consolidate Validation Rules

**Status:** pending
**Priority:** LOW
**Created:** 2026-02-06
**Parent:** SSOT Violations - CLAUDE.md Scope Mixing

## Objective
Split CLAUDE.md into hierarchical levels (Global, Project, Task) to separate universal instructions from project-specific and task-specific content.

## Success Criteria
- [ ] Global CLAUDE.md audited for project-specific content
- [ ] Project CLAUDE.md created at `5-project-memory/blackbox5/.claude/CLAUDE.md`
- [ ] Project file includes BlackBox5-specific commands and workflows
- [ ] Global CLAUDE.md cleaned to contain only universal standards
- [ ] Hierarchical loading order documented (Global → Project → Task)
- [ ] Task-level CLAUDE.md capability implemented
- [ ] All project-specific references removed from global file

## Context
CLAUDE.md currently mixes global instructions with project-specific content, creating scope confusion, maintenance issues when project changes require global edits, portability problems, and uncontrolled growth of the global file. The solution requires a hierarchical structure with clear separation between universal and specific instructions.

## Approach
1. Audit global CLAUDE.md to identify project-specific content (BlackBox5 commands, directory references, task workflows)
2. Create `.claude/` directory in project root
3. Create project CLAUDE.md with BlackBox5-specific instructions
4. Clean global CLAUDE.md to retain only universal coding standards and best practices
5. Document the three-level hierarchy and loading order

## Estimated Effort
2-3 hours

## Rollback Strategy
If hierarchical structure causes confusion, merge files back together while maintaining clear section separation with explicit headers indicating scope.
