# PLAN.md: Evaluate Unused Infrastructure Skills

**Task ID:** TASK-SKIL-050
**Status:** Planning
**Priority:** LOW
**Created:** 2026-02-05
**Estimated Effort:** 30 minutes
**Source:** Scout opportunity skill-010 (Score: 5.0)

---

## 1. First Principles Analysis

### Why Evaluate Unused Skills?

1. **Resource Optimization**: Remove or improve unused skills
2. **Maintenance Burden**: Unused code still needs updates
3. **Clarity**: Focus on skills that provide value
4. **Documentation**: Don't document what isn't used
5. **Decision Making**: Data-driven skill portfolio

### What Happens With Unused Skills?

| Problem | Impact | Severity |
|---------|--------|----------|
| Wasted maintenance | Updating skills never used | Low |
| Documentation clutter | Docs for unused features | Low |
| Confusion | Users don't know what's valuable | Medium |
| Missed opportunities | Good skills not discovered | Medium |
| Technical debt | Orphaned code | Low |

### How Should Skills Be Evaluated?

**Usage-Based Assessment:**
- Check usage_count in skill-metrics.yaml
- Review last_used timestamp
- Assess relevance to current workflows
- Decide: Keep, Improve, or Remove

---

## 2. Current State Assessment

### Infrastructure Skills Inventory

**Location:** `operations/skill-usage.yaml` and `operations/skill-metrics.yaml`

**Need to Identify:**
- Which skills are infrastructure-related
- Which have usage_count: 0
- Which haven't been used recently
- Which are candidates for removal

### Potential Infrastructure Skills

Based on naming conventions, likely candidates:
- `infrastructure-*` skills
- `deployment-*` skills
- `ci-cd-*` skills
- `hosting-*` skills
- `server-*` skills

### Evaluation Criteria

| Criterion | Weight | Assessment |
|-----------|--------|------------|
| Usage count | High | How many times used |
| Last used | High | How recently used |
| Relevance | Medium | Still applicable? |
| Maintenance cost | Medium | Effort to keep updated |
| Replacement available | Low | Is there an alternative? |

---

## 3. Proposed Solution

### Evaluation Framework

**Three Categories:**

1. **Keep**: Skills with recent usage or high potential
   - usage_count > 0 in last 90 days
   - Critical for operations
   - No replacement available

2. **Improve**: Skills with low usage but potential
   - usage_count < 5
   - Poor documentation
   - Hard to discover
   - Action: Improve documentation, add examples

3. **Remove**: Skills with no usage and low value
   - usage_count: 0
   - Not used in 180+ days
   - Replacement available
   - Action: Deprecate and remove

### Evaluation Process

```python
# lib/skill_evaluation.py

def evaluate_infrastructure_skills():
    """Evaluate all infrastructure skills for retention."""

    skills = load_skill_metrics()
    infrastructure_skills = filter_by_category(skills, 'infrastructure')

    evaluation = {
        'keep': [],
        'improve': [],
        'remove': []
    }

    for skill in infrastructure_skills:
        score = calculate_retention_score(skill)

        if score >= 70:
            evaluation['keep'].append(skill)
        elif score >= 40:
            evaluation['improve'].append(skill)
        else:
            evaluation['remove'].append(skill)

    return evaluation

def calculate_retention_score(skill):
    """Calculate retention score (0-100)."""
    score = 0

    # Usage (0-40 points)
    if skill['usage_count'] > 10:
        score += 40
    elif skill['usage_count'] > 0:
        score += skill['usage_count'] * 4

    # Recency (0-30 points)
    if skill['last_used']:
        days_since = (now - skill['last_used']).days
        if days_since < 30:
            score += 30
        elif days_since < 90:
            score += 15

    # Criticality (0-20 points)
    if skill.get('is_critical'):
        score += 20

    # No replacement (0-10 points)
    if not skill.get('replacement_available'):
        score += 10

    return score
```

---

## 4. Implementation Plan

### Phase 1: Inventory Skills (10 min)

1. **List all infrastructure skills**
   - Parse skill-usage.yaml
   - Parse skill-metrics.yaml
   - Identify infrastructure category

2. **Extract usage data**
   - usage_count for each skill
   - last_used timestamp
   - Any effectiveness scores

3. **Document current state**
   - Create inventory spreadsheet
   - Note any missing data

### Phase 2: Evaluate Each Skill (15 min)

1. **Apply evaluation criteria**
   - Calculate retention score
   - Categorize as keep/improve/remove
   - Document rationale

2. **Review edge cases**
   - Skills with zero usage but high potential
   - Skills used recently but only once
   - Critical skills with low usage

3. **Finalize recommendations**
   - List skills to keep
   - List skills to improve
   - List skills to remove

### Phase 3: Create Action Plan (5 min)

1. **Document findings**
   - Create evaluation report
   - Include retention scores
   - Provide recommendations

2. **Plan improvements**
   - For "improve" category: specific actions
   - For "remove" category: deprecation plan

3. **Update skill registry**
   - Mark deprecated skills
   - Update documentation
   - Archive if removing

---

## 5. Success Criteria

- [ ] All infrastructure skills inventoried
- [ ] Usage data extracted for each skill
- [ ] Retention scores calculated
- [ ] Skills categorized (keep/improve/remove)
- [ ] Recommendations documented
- [ ] Action plan created
- [ ] Skill registry updated

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Inventory | 10 min | 10 min |
| Phase 2: Evaluate | 15 min | 25 min |
| Phase 3: Action Plan | 5 min | 30 min |
| **Total** | **30 min** | **~30 min** |

---

## 7. Rollback Strategy

If evaluation needs revision:

1. **Keep backups:** Original skill files unchanged
2. **Soft removal:** Mark deprecated before deleting
3. **Restore:** Can un-deprecate if needed

**Deprecation Process:**
```yaml
# In skill-usage.yaml
skills:
  - name: old-skill
    status: deprecated
    deprecation_date: 2026-02-06
    replacement: new-skill
    removal_date: 2026-03-06
```

---

## 8. Files to Modify/Create

### New Files

| File | Purpose | Lines |
|------|---------|-------|
| `knowledge/analysis/infrastructure-skills-evaluation.md` | Evaluation report | ~100 |

### Modified Files

| File | Changes | Lines |
|------|---------|-------|
| `operations/skill-usage.yaml` | Mark deprecated skills | ~10 |
| `operations/skill-metrics.yaml` | Update status | ~10 |

---

## 9. Evaluation Report Template

```markdown
# Infrastructure Skills Evaluation

**Date:** 2026-02-06
**Evaluator:** [Name]

## Summary

| Category | Count |
|----------|-------|
| Keep | X |
| Improve | Y |
| Remove | Z |

## Skills to Keep

| Skill | Usage | Last Used | Score | Rationale |
|-------|-------|-----------|-------|-----------|
| skill-1 | 15 | 2026-01-30 | 85 | High usage, critical |

## Skills to Improve

| Skill | Usage | Last Used | Score | Action |
|-------|-------|-----------|-------|--------|
| skill-2 | 2 | 2026-01-15 | 50 | Add examples |

## Skills to Remove

| Skill | Usage | Last Used | Score | Deprecation Date |
|-------|-------|-----------|-------|------------------|
| skill-3 | 0 | Never | 10 | 2026-03-06 |

## Recommendations

1. [Specific recommendation]
2. [Specific recommendation]
```

---

*Plan created: 2026-02-06*
*Ready for implementation*
