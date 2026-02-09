# TASK-SSOT-006: Create Agent Identity Registry

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #13 - SSOT Agent State Violations

## Objective
Populate agent-state.yaml as the single registry of active agents. Eliminate 529 "unknown" agent entries in events.yaml.

## Success Criteria
- [ ] Design agent registration protocol
- [ ] Populate agent-state.yaml with agent definitions
- [ ] Update hooks to read agent identity from state file
- [ ] Create agent registration on start
- [ ] Update events.yaml to use registered agent IDs
- [ ] Verify no more "unknown" agent entries

## Context
Current state:
- agent-state.yaml is EMPTY (should be registry)
- events.yaml has 529 `agent_type: unknown` entries
- Agent identity exists in 4+ places with no synchronization

## Approach
1. Define agent schema for agent-state.yaml
2. Add all agent types (planner, executor, scout, analyzer, verifier, architect)
3. Update session start hooks to register agents
4. Update event logging to use registered IDs
5. Backfill historical events if possible

## Related Files
- agent-state.yaml
- events.yaml
- .claude/hooks/ralf-session-start-hook.sh
- .claude/hooks/subagent-tracking.sh

## Rollback Strategy
Can revert to "unknown" if registration system fails.
