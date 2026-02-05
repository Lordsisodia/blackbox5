# PLAN.md: Consolidate Skill Documentation

**Task:** TASK-SSOT-040 - Skill documentation in multiple places
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 60 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Skill documentation is scattered:
- `2-engine/.autonomous/skills/` - Engine skills
- `5-project-memory/blackbox5/.autonomous/skills/` - Project skills
- `operations/skill-*.yaml` - Skill data
- No unified documentation

This creates:
1. **Discovery Difficulty**: Hard to find skill docs
2. **Inconsistency**: Different formats
3. **Maintenance Overhead**: Multiple places to update
4. **No Index**: Can't see all available skills

### First Principles Solution
- **Unified Location**: Single skill documentation directory
- **Standard Format**: Consistent documentation structure
- **Index**: Searchable index of all skills
- **Cross-Reference**: Link to skill data

---

## 2. Proposed Solution

### Unified Skill Documentation

**Directory:** `5-project-memory/blackbox5/.autonomous/skills/`

**Structure:**
```
skills/
├── index.yaml              # Skill index
├── git-commit/
│   ├── README.md           # Skill documentation
│   ├── USAGE.md            # Usage examples
│   └── SKILL.yaml          # Skill metadata
├── supabase-operations/
│   ├── README.md
│   ├── USAGE.md
│   └── SKILL.yaml
└── ...
```

**Skill Index:**
```yaml
version: "1.0"
description: "Available skills index"

skills:
  git-commit:
    name: "Git Commit"
    description: "Standardized git commit workflow"
    category: "git"
    location: "skills/git-commit/"
    triggers: ["commit", "git workflow"]
    confidence_threshold: 0.70

  supabase-operations:
    name: "Supabase Operations"
    description: "Database operations for Supabase"
    category: "database"
    location: "skills/supabase-operations/"
    triggers: ["supabase", "database", "RLS"]
    confidence_threshold: 0.70

categories:
  git:
    - git-commit
    - git-workflows
  database:
    - supabase-operations
  testing:
    - testing-patterns
    - quality-gates
```

**Skill Documentation Template:**
```markdown
# Skill: [Name]

## Description
[Brief description of what this skill does]

## When to Use
- Trigger keywords: [list]
- Confidence threshold: [0-1]
- Priority: [1-10]

## Usage Examples

### Example 1: [Scenario]
```
User: "[Example input]"
→ Invoke skill
```

### Example 2: [Scenario]
```
User: "[Example input]"
→ Invoke skill
```

## Related Skills
- [Skill 1]
- [Skill 2]

## Metrics
- Effectiveness: [score]
- Usage count: [count]
- Last used: [date]
```

### Implementation Plan

#### Phase 1: Create Skill Directory Structure (30 min)

1. Create `skills/` directory
2. Create index.yaml
3. Define category structure

#### Phase 2: Migrate Existing Documentation (1 hour)

Move and consolidate:
- Engine skill docs
- Project skill docs
- Operations skill data

#### Phase 3: Create Skill Index (30 min)

```python
def generate_skill_index(skills_dir: Path) -> dict:
    """Generate skill index from skill directories."""
    index = {'version': '1.0', 'skills': {}}

    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / 'SKILL.yaml'
            if skill_file.exists():
                skill_data = yaml.safe_load(skill_file.read_text())
                index['skills'][skill_dir.name] = skill_data

    return index
```

#### Phase 4: Update Skill Discovery (1 hour)

Update skill selection to use index:
```python
def find_skill_by_trigger(trigger: str) -> Optional[dict]:
    """Find skill matching trigger."""
    index = load_skill_index()

    for skill_name, skill_data in index['skills'].items():
        if trigger in skill_data.get('triggers', []):
            return skill_data

    return None
```

---

## 3. Success Criteria

- [ ] Skill directory created
- [ ] Index generated
- [ ] All docs migrated
- [ ] Discovery working

---

## 4. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Structure | 30 min |
| Migration | 1 hour |
| Index | 30 min |
| Discovery | 1 hour |
| **Total** | **2-3 hours** |

---

*Plan created based on SSOT violation analysis*
