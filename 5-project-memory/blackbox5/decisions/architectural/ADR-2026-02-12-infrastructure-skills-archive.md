# ADR-2026-02-12: Archive Unused Infrastructure Skills

**Status:** Accepted
**Date:** 2026-02-12
**Type:** Deprecation
**Impact:** Low - affects only unused skill definitions
**Related Tasks:** TASK-SKIL-050, TASK-FIX-SKIL-050-1, TASK-FIX-SKIL-050-2, TASK-FIX-SKIL-050-3

---

## Context

The BlackBox5 skill registry contains three infrastructure skills with zero usage:
- `ralf-cloud-control`: Manage RALF agents in Kubernetes
- `github-codespaces-control`: Spawn agents in GitHub Codespaces
- `legacy-cloud-control`: Control Legacy agents in Kubernetes

These skills were defined to support cloud-based deployment scenarios, but the actual BlackBox5 deployment environment operates in local development mode only.

---

## Problem

### Issues with Unused Skills

1. **Zero Usage Impact:** All three skills have `usage_count: 0` and no documented usage
2. **No Implementation Files:** None of the skills have SKILL.md files providing implementation guidance
3. **Maintenance Overhead:** Skills appear in counts and require maintenance despite no benefit
4. **Confusion:** Agents may consider these skills when they are not applicable to current environment

### Current Deployment Environment

- **Primary Deployment:** Mac Mini (local development)
- **VPS Instance:** moltbot-vps-ai (standard Linux VPS, not Kubernetes)
- **No Active Kubernetes Cluster:** No K8s deployment for RALF agents
- **No GitHub Codespaces:** No Codespaces integration in current workflows
- **Legacy System Status:** Legacy agents being phased out (IG-006 and IG-007 indicate architecture restructure)

---

## Decision

**Archive all three infrastructure skills with full deprecation metadata**

### Rationale

1. **No Current Need:** Cloud deployment is not in current or near-term roadmap
2. **Architecture Focus:** Current priorities are on local autonomy (IG-AUTONOMY-001) and architecture refactoring (IG-006, IG-007)
3. **Maintain Audit Trail:** Archiving preserves historical context for future reference
4. **Easy Recovery:** Can restore skills if cloud deployment becomes a priority

### Skills Archived

| Skill | Purpose | Archive Reason |
|-------|---------|----------------|
| `ralf-cloud-control` | Manage RALF agents in Kubernetes | No K8s deployment; RALF currently local-only |
| `github-codespaces-control` | Spawn agents in GitHub Codespaces | No Codespaces integration; not on roadmap |
| `legacy-cloud-control` | Control Legacy agents in Kubernetes | Legacy system being phased out; deprecated |

---

## Consequences

### Positive

- **Reduced Maintenance:** Skills no longer counted in active skill totals
- **Clearer Documentation:** Skill counts reflect actual usable skills (23 → 20)
- **Better Agent Guidance:** Agents won't consider irrelevant skills
- **Preserved History:** Archive metadata shows when/why skills were considered

### Negative

- **Potential Re-implementation Cost:** If cloud deployment becomes priority, skills must be re-implemented
- **Git Noise:** Archive adds complexity to skill-registry.yaml structure

### Neutral

- **Historical Reference:** Archive section maintains context for future developers
- **Audit Trail:** Git history shows evolution from 23 to 20 skills

---

## Alternatives Considered

### Option A: Remove Completely
**Decision:** Rejected
**Reason:** Would lose historical context; git history less discoverable than archived section

### Option B: Keep and Implement SKILL.md Files
**Decision:** Rejected
**Reason:** No near-term need; implementation effort would be wasted; skills would remain unused

### Option C: Archive (SELECTED)
**Decision:** Accepted
**Reason:** Preserves historical context while removing maintenance overhead; easy recovery if needed

---

## Implementation

### Changes Made

1. **Created `archived_skills` section** in skill-registry.yaml
2. **Moved three skills** from `skills:` to `archived_skills:`
3. **Added deprecation metadata** to each archived skill:
   - `archived: true`
   - `archived_date: '2026-02-12T06:27:34+00:00'`
   - `archived_reason: 'No usage; system operates in local-dev mode only; no K8s/Codespaces deployment planned'`
   - `replacement: null`
4. **Updated metadata:**
   - `total_skills: 25` (20 active + 3 archived)
   - `last_updated: '2026-02-12T06:27:34.643993+00:00'`
   - Added `archive_metadata` section with archive stats

### Documentation Updates

1. Updated `/opt/blackbox5/5-project-memory/blackbox5/operations/skill-effectiveness-validation.md`
   - Updated skill count from 23 to 20 (with note about 3 archived)
   - Updated infrastructure skills section to reflect archived status
   - Added note about archive date and reason

---

## Rollback Strategy

If cloud deployment becomes a priority:

1. **Restore Skills:** Move entries from `archived_skills:` back to `skills:`
2. **Create SKILL.md Files:** Implement proper skill documentation
3. **Update Counts:** Adjust `total_skills` metadata accordingly
4. **Update Documentation:** Revert or update skill-effectiveness-validation.md

All changes are version controlled in git; restoration is straightforward.

---

## Monitoring

### Metrics to Track

- **Total active skills:** Should remain at 20 unless new skills added
- **Archive count:** Should remain at 3 unless more skills archived
- **Skill invocation rate:** Should improve with reduced noise (currently 0%)

### Review Schedule

- **Quarterly Review:** Check if cloud deployment needs have emerged
- **Annual Archive Review:** Evaluate if other skills should be archived

---

## Related Documentation

- **Parent Task:** TASK-SKIL-050 (Unused Infrastructure Skills)
- **Decision Task:** TASK-FIX-SKIL-050-1 (Decide Fate)
- **Implementation Task:** TASK-FIX-SKIL-050-2 (Implement Archive)
- **Documentation Task:** TASK-FIX-SKIL-050-3 (Update References) [THIS TASK]
- **Registry File:** `/opt/blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml`
- **Archived Skills Section:** Lines 976-1078 (as of 2026-02-12)

---

**Approved By:** Autonomous System (RALF)
**Next Review:** 2026-05-12 (3 months from archive date)
