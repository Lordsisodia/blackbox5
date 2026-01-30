# TASK-003: Create Automatic Skill Router

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-01-30
**Agent:** Agent-2.3
**Project:** RALF-CORE

---

## Objective

Create an automatic skill routing system that selects the appropriate BMAD skill based on task content.

## Background

Agent-2.3 specifies automatic skill routing, but the implementation doesn't exist yet. We need a system that parses task descriptions and loads the appropriate skill file.

## Success Criteria

- [ ] Create skill router script at `/Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5/2-engine/.autonomous/lib/skill_router.py`
- [ ] Implement keyword matching for each BMAD skill
- [ ] Create skill loading mechanism
- [ ] Test routing with different task types
- [ ] Document the routing logic

## Skill Mapping

| Keywords | Skill | Role |
|----------|-------|------|
| PRD, requirements, product | bmad-pm.md | John (PM) |
| architecture, design, system | bmad-architect.md | Winston |
| research, analyze, investigate | bmad-analyst.md | Mary |
| sprint, story, planning | bmad-sm.md | Bob |
| UX, UI, design, user | bmad-ux.md | Sally |
| implement, code, develop, fix | bmad-dev.md | Amelia |
| test, QA, quality | bmad-qa.md | Quinn |
| test architecture, test plan | bmad-tea.md | TEA |
| small, quick, clear, simple | bmad-quick-flow.md | Barry |

## Approach

1. Create skill_router.py with keyword matching
2. Load skill files from `/Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5/2-engine/.autonomous/skills/`
3. Parse task description for keywords
4. Return recommended skill path
5. Integrate with ralf-loop.sh

## Files to Create

- `/Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5/2-engine/.autonomous/lib/skill_router.py`

## Files to Modify

- `/Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5/2-engine/.autonomous/shell/ralf-loop.sh` (to call skill router)

## Risk Level

LOW - New feature, doesn't break existing functionality

## Rollback Strategy

Remove skill router calls from ralf-loop.sh if issues arise
