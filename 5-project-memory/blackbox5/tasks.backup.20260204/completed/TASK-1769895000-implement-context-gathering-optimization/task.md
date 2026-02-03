# TASK-1769895000: Implement Context Gathering Optimization

**Type:** implement
**Priority:** high
**Status:** completed
**Created:** 2026-02-01T08:00:00Z
**Source:** goals.yaml IG-003, project-relationships.md recommendations

---

## Objective

Implement the context gathering optimization recommendations from the project relationship analysis to reduce "missed file" errors and improve cross-project task execution efficiency.

## Context

The project-relationships.md analysis identified specific context gathering heuristics that should be integrated into the run initialization process. Currently, agents may miss critical cross-project files because they don't automatically check the project-map.yaml or follow the documented heuristics.

Key recommendations to implement:
1. Always read routes.yaml first for cross-project tasks
2. Check project-map.yaml for dependency awareness
3. Cache frequently accessed shared files
4. Validate paths before execution

## Success Criteria

- [ ] Update run initialization to reference project-map.yaml
- [ ] Add automatic routes.yaml reading for cross-project tasks
- [ ] Create context gathering helper that follows documented heuristics
- [ ] Add path validation before file operations
- [ ] Document the optimization in operations/.docs/

## Approach

1. Read current run initialization process (operations/workflows/ or similar)
2. Identify where context gathering happens
3. Add project-map.yaml reference step
4. Add routes.yaml auto-read for tasks with cross-project indicators
5. Create shared file caching mechanism
6. Test with a sample cross-project task

## Files to Read

- operations/project-map.yaml (context_gathering section)
- knowledge/analysis/project-relationships.md (recommendations)
- .autonomous/routes.yaml (current routing)
- Any existing run initialization scripts

## Files to Create/Modify

- operations/context-gathering.yaml - Configuration for context gathering optimization
- operations/.docs/context-gathering-guide.md - Usage documentation
- Update run initialization to use new optimization

## Indicators of Cross-Project Tasks

- Task references multiple project paths (e.g., "2-engine", "siso-internal")
- Task involves BMAD skills or workflows
- Task mentions shared configuration files
- Task requires pattern replication across projects

## Notes

This directly addresses goals.yaml IG-003 (Improve System Flow and Code Mapping) success criteria:
- Fewer 'missed file' errors
- Faster context acquisition
- Better cross-project awareness

The implementation should be non-breaking and additive to existing processes.
