# TASK-FIX-SKIL-050-1: Decide Fate of Unused Infrastructure Skills

**Status:** pending
**Priority:** MEDIUM
**Category:** skills
**Estimated Effort:** 15 minutes
**Created:** 2026-02-09T12:45:00Z
**Parent Task:** TASK-SKIL-050
**Source:** Root cause analysis - 3 infrastructure skills have 0 usage

---

## Objective

Make a clear decision on whether to keep, archive, or remove the three unused infrastructure skills: `ralf-cloud-control`, `github-codespaces-control`, and `legacy-cloud-control`.

---

## Success Criteria

- [ ] Document decision for each of the 3 skills (keep/archive/remove)
- [ ] Record rationale for the decision
- [ ] Get user confirmation if decision is to remove/archive
- [ ] Update parent task TASK-SKIL-050 with decision

---

## Context

**Problem:** Three infrastructure skills in the skill-registry.yaml have zero usage:

1. **ralf-cloud-control** (lines 770-802)
   - Purpose: Manage RALF agents in Kubernetes
   - Usage count: 0
   - Issue: Current usage is local dev, not cloud infrastructure

2. **github-codespaces-control** (lines 804-836)
   - Purpose: Spawn agents in GitHub Codespaces
   - Usage count: 0
   - Issue: No SKILL.md implementation file exists

3. **legacy-cloud-control** (lines 838-870)
   - Purpose: Control Legacy agents in K8s
   - Usage count: 0
   - Issue: Legacy system may be deprecated

**Current Environment:**
- Primary usage is local development (Mac Mini, local Claude Code)
- No active Kubernetes deployment for agents
- No GitHub Codespaces integration currently in use
- Legacy cloud scripts exist at `/Users/shaansisodia/.blackbox5/bin/legacy/` but may be deprecated

---

## Decision Options

### Option A: Remove Completely
- Delete entries from skill-registry.yaml
- Remove any associated files
- Update total_skills count

### Option B: Archive
- Move entries to "archived_skills" section in registry
- Keep for historical reference
- Mark as deprecated

### Option C: Keep with Implementation
- Create missing SKILL.md files
- Define clear use cases
- Set realistic triggers

---

## Decision to Make

**Primary Question:** Given that BlackBox5 currently operates in local-dev mode only, do these cloud infrastructure skills have future value?

**Considerations:**
- Will we deploy RALF agents to Kubernetes in the next 6 months?
- Is GitHub Codespaces integration on the roadmap?
- Is the legacy system being maintained or phased out?
- Does keeping unused skills create maintenance overhead?

---

## Rollback Strategy

If decision needs reversal:
1. Skill registry is version controlled (git history)
2. Can restore from backup if needed
3. Document decision in DECISIONS.md for future reference

---

## Notes

_Decision recorded here after analysis_
