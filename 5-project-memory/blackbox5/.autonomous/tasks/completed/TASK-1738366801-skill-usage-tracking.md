# TASK-1738366801: Create Skill Usage Tracking System

**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T05:00:00Z
**Source:** goals.yaml IG-004

---

## Objective

Create a system to track skill usage patterns, effectiveness, and identify optimization opportunities.

## Context

Per goals.yaml IG-004, current issues include:
- Some skills may be redundant
- Skill triggers may need tuning
- Missing skills for common tasks

A tracking system will provide data to optimize skill usage and efficiency.

## Success Criteria

- [ ] Create operations/skill-usage.yaml with tracking schema
- [ ] Track: skill name, usage count, last used, success rate, avg execution time
- [ ] Document how to update the tracking (manual or automated)
- [ ] Populate initial data for existing skills
- [ ] Create simple query/report mechanism

## Approach

1. Design YAML schema for skill tracking
2. Inventory existing skills from ~/.blackbox5/5-project-memory/siso-internal/.Autonomous/.skills/
3. Create initial tracking file with known skills
4. Document update procedures
5. Create simple reporting function

## Files to Modify/Create

- operations/skill-usage.yaml (new)
- operations/.docs/skill-tracking-guide.md (new)

## Schema Proposal

```yaml
skills:
  - name: "skill-name"
    category: "development|analysis|testing"
    usage_count: 0
    first_used: "2026-02-01T00:00:00Z"
    last_used: "2026-02-01T00:00:00Z"
    success_count: 0
    failure_count: 0
    avg_execution_time_ms: 0
    trigger_accuracy: "high|medium|low"  # does it trigger when needed?
    notes: ""

metadata:
  last_updated: "2026-02-01T00:00:00Z"
  total_invocations: 0
```

## Notes

Start with manual tracking. Future iteration could automate via wrapper script.
