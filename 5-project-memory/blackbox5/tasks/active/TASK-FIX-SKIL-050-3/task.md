# TASK-FIX-SKIL-050-3: Update Documentation and Registry References

**Status:** pending
**Priority:** LOW
**Category:** skills
**Estimated Effort:** 15 minutes
**Created:** 2026-02-09T12:45:00Z
**Parent Task:** TASK-SKIL-050
**Depends On:** TASK-FIX-SKIL-050-2 (implementation must be complete)
**Source:** Root cause analysis - Registry consistency needed after skill changes

---

## Objective

Update all documentation and references to reflect the final state of the infrastructure skills after the decision in TASK-FIX-SKIL-050-1 and implementation in TASK-FIX-SKIL-050-2.

---

## Success Criteria

- [ ] Update skill-effectiveness-report.md if it references these skills
- [ ] Update any documentation mentioning infrastructure skills
- [ ] Update category_performance counts in registry analysis section
- [ ] Create ADR (Architecture Decision Record) documenting the decision
- [ ] Mark parent task TASK-SKIL-050 as complete

---

## Context

**Files That May Need Updates:**

1. **Skill Registry Analysis Section** (lines 1059-1184)
   - Update `category_performance` for infrastructure category
   - Update `total_skills` count
   - Update `underperforming_skills` list

2. **Documentation Files to Check:**
   - `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.docs/skill-effectiveness-report.md`
   - `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/knowledge/analysis/skill-system-analysis.md`
   - Any CLAUDE.md or rules files referencing these skills

3. **Decision Record:**
   - Create ADR in `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/decisions/`
   - Document why skills were kept/removed/archived

---

## Tasks

### 1. Registry Analysis Updates

Update the following sections in `skill-registry.yaml`:

```yaml
analysis:
  category_performance:
    - category: infrastructure
      avg_effectiveness: null  # Update if changed
      total_tasks: 0           # Confirm still 0
      success_rate: null       # Confirm still null
```

### 2. Documentation Sweep

Search for references to the three skills:
```bash
grep -r "ralf-cloud-control\|github-codespaces-control\|legacy-cloud-control" \
  /Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/ \
  --include="*.md" --include="*.yaml" --include="*.json"
```

Update or remove references as appropriate.

### 3. Create ADR

Create `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/decisions/ADR-XXX-infrastructure-skills.md`:

```markdown
# ADR-XXX: Infrastructure Skills Decision

## Status
Accepted / Deprecated / Removed

## Context
Three infrastructure skills had zero usage...

## Decision
[Keep / Archive / Remove]

## Consequences
[What this means for the system]

## Alternatives Considered
[Other options evaluated]
```

### 4. Complete Parent Task

Update `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-SKIL-050/task.md`:
- Mark as completed
- Add summary of actions taken
- Reference the three fix tasks

---

## Rollback Strategy

If documentation updates cause issues:
1. All documentation is version controlled
2. Can revert specific files with git
3. ADR can be amended if decision changes

---

## Validation Checklist

- [ ] No broken references in documentation
- [ ] Registry counts are consistent
- [ ] ADR created and linked
- [ ] Parent task marked complete
- [ ] No orphaned files or entries

---

## Notes

_Final status and completion notes recorded here_
