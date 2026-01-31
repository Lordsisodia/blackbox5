# TASK-1769892001: Create Skill Usage Tracking System

**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T04:30:00Z
**Source:** goals.yaml IG-004

---

## Objective

Create a system to track skill usage across the BlackBox5 autonomous system, enabling data-driven skill optimization.

## Context

Per goals.yaml IG-004 (Optimize Skill Usage), we need to track:
- Which skills are used most/least frequently
- Success rates per skill
- Average execution time per skill
- Last used timestamps

This data will inform decisions about skill consolidation, trigger tuning, and identifying gaps.

## Success Criteria

- [ ] Create operations/skill-usage.yaml with proper schema
- [ ] Track: skill name, usage count, last used, success rate, avg execution time
- [ ] Document how to update the tracking
- [ ] Populate initial data for existing skills
- [ ] Create simple query interface (optional)

## Approach

1. Design YAML schema for skill tracking
2. Create operations/skill-usage.yaml
3. Document update procedures
4. Populate with initial data from ~/.claude/CLAUDE.md skills section
5. Add to run completion checklist

## Files to Create/Modify

- operations/skill-usage.yaml (new)
- .docs/skill-tracking-guide.md (new)
- .templates/tasks/task-completion.md.template (add tracking step)

## Schema Design

```yaml
skills:
  - name: "skill-name"
    category: "development|analysis|testing|documentation"
    usage_count: 0
    last_used: "2026-02-01T00:00:00Z"
    success_count: 0
    failure_count: 0
    avg_execution_time_ms: 0
    triggers:
      - "keyword pattern"
    effectiveness_score: 0.0  # calculated

metadata:
  last_updated: "2026-02-01T00:00:00Z"
  total_invocations: 0
  top_skills: []
  underutilized_skills: []
```

## Notes

- Keep it simple - manual updates initially
- Consider automated tracking in future iteration
- Update after each run that uses skills
