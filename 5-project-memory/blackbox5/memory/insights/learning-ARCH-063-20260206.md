# Learning: Content Standardization (Project to Engine)

**Task:** TASK-ARCH-063
**Date:** 2026-02-06
**Category:** Architecture

---

## What Worked Well

- Clear categorization of items (ready to move vs needs refactoring)
- 8 items were identified as immediately movable
- Documentation files (.docs/) were straightforward to migrate

## What Was Harder Than Expected

- 11 bin/ scripts needed abstraction before migration
- Deprecated operations files needed cleanup decisions
- 6 agent patterns needed architectural abstraction
- Dependencies on TASK-ARCH-060 (path abstraction) blocked progress

## What Would You Do Differently

- Complete path abstraction first before attempting migration
- Create project wrappers earlier to test engine versions
- Separate the "move now" vs "refactor first" items into different tasks

## Technical Insights

- Generic frameworks (queue management, metrics, skill selection) belong in engine
- Project-specific configuration should remain in project
- Abstraction requirements: path resolution, project name config, operations directory location

## Process Improvements

- Analyze dependencies before creating migration plans
- Create abstraction layers before moving code
- Test with multiple projects to ensure genericity

## Key Takeaway

Always complete foundational abstraction work before attempting large-scale code migration between system boundaries.
