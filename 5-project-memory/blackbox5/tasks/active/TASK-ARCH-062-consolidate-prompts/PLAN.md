# PLAN.md: Consolidate Duplicate Prompts

**Task:** TASK-ARCH-062
**Status:** pending
**Created:** 2026-02-06

## Objective
Consolidate 3 pairs of duplicate agent prompts between engine and project.

## Prompt Pairs to Consolidate

### 1. Scout Prompts
- Engine: `agents/deep-repo-scout.md` (200 lines, external repos)
- Project: `agents/scout-agent-prompt.md` (207 lines, internal architecture)
- **Strategy:** Keep both, rename project to `internal-scout.md` for clarity

### 2. Planner Prompts  
- Engine: `agents/implementation-planner.md` (132 lines)
- Project: `agents/planner-agent-prompt.md` (284 lines)
- **Strategy:** Merge into unified `planner.md` in engine

### 3. Executor Prompts
- Engine: `ralf-executor.md` (659 lines)
- Project: `agents/executor-agent-prompt.md` (321 lines)
- **Strategy:** Engine supersedes - archive project version

## Implementation Steps
1. **Phase 1 (30 min):** Archive project executor-agent-prompt.md
2. **Phase 2 (1-2 hrs):** Create merged planner.md
3. **Phase 3 (30 min):** Rename scout-agent-prompt.md to internal-scout.md
4. **Phase 4 (30 min):** Update references, test

## Timeline
- Total: 3-4 hours

## Success Criteria
- [ ] Executor consolidated (project version archived)
- [ ] Planner merged (unified version in engine)
- [ ] Scout clarified (renamed and documented)
- [ ] All references updated
- [ ] Integration tests pass
