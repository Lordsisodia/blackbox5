# Skill Tracking Guide

**Purpose:** Document how to update and use the skill usage tracking system.

**Related Files:**
- `operations/skill-usage.yaml` - Main tracking file
- `2-engine/.autonomous/skills/` - Skill definitions

---

## Quick Reference

### After Using a Skill

Update `operations/skill-usage.yaml` with the following:

```yaml
# Example: After using the "plan" skill successfully in 5 minutes

skills:
  - name: "plan"
    usage_count: 1          # Increment by 1
    last_used: "2026-02-01T06:15:00Z"  # ISO 8601 timestamp
    success_count: 1        # Increment if successful
    failure_count: 0        # Increment if failed
    avg_execution_time_ms: 300000  # 5 minutes = 300,000ms
```

### Calculating Average Execution Time

```
new_avg = ((old_avg * (count - 1)) + new_time) / count
```

Example:
- Old average: 300,000ms (5 min)
- Usage count: 5
- New time: 240,000ms (4 min)
- New average: ((300000 * 4) + 240000) / 5 = 288,000ms

---

## Schema Reference

### Skill Entry

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique skill identifier |
| `category` | string | Skill category (development, testing, analysis, etc.) |
| `description` | string | What the skill does |
| `usage_count` | integer | Total times skill has been invoked |
| `last_used` | ISO 8601 timestamp | Most recent usage |
| `success_count` | integer | Successful completions |
| `failure_count` | integer | Failed completions |
| `avg_execution_time_ms` | integer | Average execution time in milliseconds |
| `triggers` | array | Keywords/phrases that activate this skill |
| `effectiveness_score` | float | success_count / usage_count (0.0-1.0) |

### Metadata Section

| Field | Type | Description |
|-------|------|-------------|
| `last_updated` | ISO 8601 timestamp | When file was last modified |
| `total_invocations` | integer | Sum of all skill usage_counts |
| `top_skills` | array | Skills sorted by usage_count (auto-generated) |
| `underutilized_skills` | array | Skills with low usage (auto-generated) |
| `categories` | map | Count of skills per category |

---

## Categories

### Core Categories

| Category | Description | Skills Count |
|----------|-------------|--------------|
| `development` | Code implementation | 3 |
| `testing` | Test creation and execution | 2 |
| `analysis` | Research and investigation | 2 |
| `documentation` | Docs and comments | 1 |
| `bmad` | BMAD agent skills | 10 |
| `n8n` | n8n workflow skills | 6 |
| `git` | Git operations | 1 |
| `product` | Product management | 1 |
| `siso` | SISO-specific tools | 2 |
| `integration` | External integrations | 1 |

---

## Adding a New Skill

1. Copy an existing skill entry as template
2. Update all fields:
   - Choose a unique `name` (kebab-case)
   - Select appropriate `category`
   - Write clear `description`
   - Define `triggers` that activate the skill
3. Initialize counters to 0
4. Update `metadata.categories` count if new category
5. Update `metadata.last_updated`

### Example New Skill

```yaml
  - name: "my-new-skill"
    category: "development"
    description: "What this skill does"
    usage_count: 0
    last_used: null
    success_count: 0
    failure_count: 0
    avg_execution_time_ms: 0
    triggers:
      - "trigger phrase 1"
      - "trigger phrase 2"
    effectiveness_score: 0.0
```

---

## Analysis Queries

### Find Most Used Skills

```bash
# Sort by usage_count descending
yq '.skills | sort_by(.usage_count) | reverse' operations/skill-usage.yaml
```

### Find Most Effective Skills

```bash
# Sort by effectiveness_score descending
yq '.skills | sort_by(.effectiveness_score) | reverse' operations/skill-usage.yaml
```

### Find Stale Skills (Unused > 30 Days)

```bash
# Requires yq and date calculation
# Skills not used in last 30 days
```

### Find Underutilized Skills

```bash
# Skills with < 5 uses that are > 30 days old
yq '.skills | map(select(.usage_count < 5))' operations/skill-usage.yaml
```

---

## Integration with Run Completion

Add to your run completion checklist:

```markdown
## Post-Run Checklist

- [ ] Update skill-usage.yaml if skills were used
- [ ] Update DECISIONS.md with skill effectiveness notes
- [ ] Document any new trigger patterns discovered
```

---

## Maintenance

### Monthly Review

1. Review `top_skills` - Are they the right ones being used?
2. Review `underutilized_skills` - Should any be promoted or deprecated?
3. Check for skills with low effectiveness_score (< 0.7)
4. Update trigger patterns based on actual usage

### Quarterly Review

1. Analyze trends in skill usage
2. Identify gaps (common tasks without skills)
3. Propose new skills or skill consolidations
4. Update this guide with lessons learned

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-01 | Manual tracking initially | Simple, no automation complexity |
| 2026-02-01 | YAML format | Human readable, version control friendly |
| 2026-02-01 | 31 initial skills | Cover all current BMAD + system skills |

---

## Future Improvements

- [ ] Automated tracking via skill invocation wrapper
- [ ] Dashboard for skill usage visualization
- [ ] Effectiveness correlation with task outcomes
- [ ] Trigger pattern effectiveness analysis
