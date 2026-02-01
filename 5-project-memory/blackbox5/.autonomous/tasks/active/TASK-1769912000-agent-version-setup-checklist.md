# TASK-1769912000: Create Agent Version Setup Checklist

**Type:** implement
**Priority:** medium
**Status:** pending
**Created:** 2026-02-01T11:15:00Z
**Source:** IMP-1769903007

---

## Objective

Create a comprehensive checklist for setting up new agent versions to prevent missing components.

## Context

Agent versions are created but supporting infrastructure is often missed:
- Agent-2.4 AGENT.md created but metrics.jsonl missing
- Templates not copied from previous versions
- Version references not updated
- Dashboard scripts broken

This task addresses the recurring pattern of incomplete agent setups by creating a standardized checklist and automation script.

## Success Criteria

- [ ] Agent version setup checklist created
- [ ] Checklist covers all components (AGENT.md, templates, scripts, metrics)
- [ ] Checklist integrated into agent creation workflow
- [ ] Version update script created
- [ ] Documentation in `.docs/agent-version-checklist.md`

## Approach

1. Analyze Agent-2.2, 2.3, 2.4 structure
2. Create comprehensive checklist
3. Create version update script
4. Document in .docs/
5. Add to agent creation workflow

## Files to Modify

- `.docs/agent-version-checklist.md` (create)
- `2-engine/.autonomous/scripts/create-agent-version.sh` (create)
- `2-engine/.autonomous/workflows/agent-creation.yaml` (modify)

## Related Learnings

- run-20260131-060616: "Version Synchronization Gap"
- run-1769800330: "Version Headers Matter"

## Estimated Effort

35 minutes

## Acceptance Criteria

- [ ] Checklist covers all agent components
- [ ] Setup script automates checklist
- [ ] Documentation complete
- [ ] Tested by creating checklist for next version

## Notes

This improvement was extracted from learnings analysis (TASK-1769902000).
See IMP-1769903007 for full context.
