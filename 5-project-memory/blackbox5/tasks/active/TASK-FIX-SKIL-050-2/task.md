# TASK-FIX-SKIL-050-2: Implement Decision - Create or Remove Infrastructure Skills

**Status:** pending
**Priority:** MEDIUM
**Category:** skills
**Estimated Effort:** 30-45 minutes
**Created:** 2026-02-09T12:45:00Z
**Parent Task:** TASK-SKIL-050
**Depends On:** TASK-FIX-SKIL-050-1 (decision must be made first)
**Source:** Root cause analysis - SKILL.md files missing for infrastructure skills

---

## Objective

Execute the decision made in TASK-FIX-SKIL-050-1: either create proper SKILL.md implementation files for the infrastructure skills, or remove/archive them from the registry.

---

## Success Criteria

- [ ] If keeping: Create SKILL.md for ralf-cloud-control
- [ ] If keeping: Create SKILL.md for github-codespaces-control
- [ ] If keeping: Create SKILL.md for legacy-cloud-control
- [ ] If removing: Delete entries from skill-registry.yaml
- [ ] If archiving: Move entries to archived_skills section
- [ ] Update total_skills count in registry metadata
- [ ] Validate registry YAML syntax after changes

---

## Context

**Current State:**
- Three infrastructure skills exist in `skill-registry.yaml` (lines 770-870)
- All have `usage_count: 0`
- No SKILL.md files exist for any of them
- Skills reference cloud/Kubernetes functionality not currently in use

**Files to Modify:**
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml`
- New (if keeping): `/Users/shaansisodia/.blackbox5/.skills/ralf-cloud-control/SKILL.md`
- New (if keeping): `/Users/shaansisodia/.blackbox5/.skills/github-codespaces-control/SKILL.md`
- New (if keeping): `/Users/shaansisodia/.blackbox5/.skills/legacy-cloud-control/SKILL.md`

**SKILL.md Template Structure:**
```markdown
# [Skill Name]

## Purpose
[What this skill does]

## When to Use
[Trigger conditions]

## Implementation
[How to execute]

## Parameters
[Input/output specifications]

## Examples
[Usage examples]
```

---

## Implementation Path

### If Decision = KEEP:

1. Create `.skills/` directory structure if not exists
2. Create SKILL.md for each infrastructure skill:
   - Define clear, realistic triggers based on actual usage patterns
   - Document implementation steps
   - Include examples
3. Update skill-registry.yaml:
   - Add `skill_md_path` field to each skill entry
   - Update `last_updated` timestamp

### If Decision = REMOVE:

1. Remove entries from skill-registry.yaml (lines 770-870)
2. Update metadata:
   - `total_skills: 20` (from 23)
   - `last_updated` timestamp
3. Remove any associated implementation files

### If Decision = ARCHIVE:

1. Create new `archived_skills` section in registry
2. Move three skill entries to archived section
3. Add deprecation metadata:
   - `deprecated: true`
   - `deprecated_date: "2026-02-09"`
   - `replacement: null` (or alternative skill)
4. Update `total_skills` count

---

## Rollback Strategy

If changes cause issues:
1. Restore skill-registry.yaml from git: `git checkout -- operations/skill-registry.yaml`
2. Remove created SKILL.md files if applicable
3. Document what went wrong in parent task

---

## Validation Checklist

- [ ] YAML syntax valid (use `yamllint` or similar)
- [ ] All references updated
- [ ] Counts match actual entries
- [ ] No broken links or paths

---

## Notes

_Implementation notes recorded here during execution_
