# PLAN.md: Consolidate Skill Metrics into Single Registry

**Task:** TASK-SSOT-031 - Skill metrics in multiple files need consolidation
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 70 (High)

---

## 1. First Principles Analysis

### The Core Problem
Skill metrics are fragmented across multiple files:
- `operations/skill-metrics.yaml` - Effectiveness scores
- `operations/skill-usage.yaml` - Usage patterns
- `operations/skill-selection.yaml` - Selection criteria
- `operations/improvement-metrics.yaml` - Improvement tracking

This creates:
1. **Data Fragmentation**: Related data in different files
2. **Update Inconsistency**: Must update multiple files
3. **Query Complexity**: Need to join data manually
4. **Maintenance Overhead**: 4 files to maintain

### First Principles Solution
- **Single Registry**: One file for all skill data
- **Unified Schema**: Consistent structure
- **Query Interface**: Easy access to all metrics
- **Migration**: Move existing data

---

## 2. Current State Analysis

### File Structure

```yaml
# skill-metrics.yaml
skill_metrics:
  git-commit:
    effectiveness_score: 0.92
    success_rate: 0.95

# skill-usage.yaml
skill_usage:
  git-commit:
    last_used: "2026-02-05"
    usage_count: 47

# skill-selection.yaml
selection_criteria:
  git-commit:
    triggers: ["commit", "git"]
    confidence_threshold: 0.70
```

---

## 3. Proposed Solution

### Unified Skill Registry

**File:** `5-project-memory/blackbox5/operations/skill-registry.yaml`

```yaml
version: "2.0"
last_updated: "2026-02-06T00:00:00Z"

skills:
  git-commit:
    # Metadata
    name: "Git Commit"
    description: "Standardized git commit workflow"
    category: "git"
    version: "1.0"
    created_at: "2026-01-15"

    # Selection criteria
    selection:
      triggers: ["commit", "git workflow", "git commit"]
      confidence_threshold: 0.70
      priority: 1
      domain_keywords: ["git", "commit", "PR", "pull request"]

    # Current metrics
    metrics:
      effectiveness_score: 0.92
      success_rate: 0.95
      usage_count: 47
      average_duration_minutes: 5.2
      last_used: "2026-02-05T14:30:00Z"

    # Usage history (last 30 days)
    recent_usage:
      - date: "2026-02-05"
        task_id: "TASK-001"
        outcome: "success"
        duration_minutes: 5

    # Improvement tracking
    improvements:
      - date: "2026-02-01"
        description: "Added co-author handling"
        impact: "positive"
```

### Implementation Plan

#### Phase 1: Create Unified Schema (1 hour)

1. Design comprehensive skill schema
2. Include all current fields
3. Plan for future extensions

#### Phase 2: Create Migration Script (1 hour)

```python
def migrate_skills():
    """Migrate skill data from multiple files to registry."""
    registry = {'version': '2.0', 'skills': {}}

    # Load from all sources
    metrics = load_yaml('skill-metrics.yaml')
    usage = load_yaml('skill-usage.yaml')
    selection = load_yaml('skill-selection.yaml')

    # Merge into registry
    all_skills = set()
    all_skills.update(metrics.get('skill_metrics', {}).keys())
    all_skills.update(usage.get('skill_usage', {}).keys())
    all_skills.update(selection.get('selection_criteria', {}).keys())

    for skill_name in all_skills:
        registry['skills'][skill_name] = {
            'metrics': metrics.get('skill_metrics', {}).get(skill_name, {}),
            'recent_usage': usage.get('skill_usage', {}).get(skill_name, {}),
            'selection': selection.get('selection_criteria', {}).get(skill_name, {})
        }

    save_yaml('skill-registry.yaml', registry)
```

#### Phase 3: Update References (1 hour)

Update all code that reads skill data:
- Skill selection logic
- Metrics collection
- Dashboard queries

#### Phase 4: Deprecate Old Files (1 hour)

1. Add deprecation notices
2. Create symlinks if needed
3. Update documentation

---

## 4. Success Criteria

- [ ] Unified skill-registry.yaml created
- [ ] All data migrated
- [ ] All references updated
- [ ] Old files deprecated
- [ ] Documentation updated

---

## 5. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Schema | 1 hour |
| Migration | 1 hour |
| References | 1 hour |
| Deprecation | 1 hour |
| **Total** | **3-4 hours** |

---

*Plan created based on SSOT violation analysis*
