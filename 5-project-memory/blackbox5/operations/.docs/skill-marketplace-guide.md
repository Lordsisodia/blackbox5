# Skill Marketplace & Discovery System - User Guide

**Feature:** F-009 Skill Marketplace & Discovery System
**Version:** 1.0.0
**Last Updated:** 2026-02-01

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Skill Registry](#skill-registry)
4. [Skill Versioning](#skill-versioning)
5. [Skill Recommendations](#skill-recommendations)
6. [CLI Reference](#cli-reference)
7. [Python API Reference](#python-api-reference)
8. [Contributing Skills](#contributing-skills)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The Skill Marketplace is a centralized system for discovering, managing, and versioning RALF skills. It provides:

- **Central Registry:** All skills tracked with metadata in one place
- **Search & Discovery:** Find skills by keyword, domain, or tag
- **Version Management:** Semantic versioning prevents breaking changes
- **Automatic Recommendations:** AI-powered skill suggestions based on task context
- **Effectiveness Tracking:** Monitor skill success rates over time

### Components

1. **Skill Registry** (`skill_registry.py`) - Central registry with metadata
2. **Skill Versioning** (`skill_versioning.py`) - Semantic versioning support
3. **Skill Recommender** (`skill_recommender.py`) - AI-powered recommendations
4. **Storage** (`skill-registry.yaml`) - YAML-based persistent storage

---

## Quick Start

### 1. Populate Registry (First Time)

Auto-populate the registry from existing skills:

```bash
cd /workspaces/blackbox5/2-engine/.autonomous
python3 -m lib.skill_registry auto-populate
```

This scans the `skills/` directory and registers all skills with metadata.

### 2. Search for Skills

Find skills by keyword:

```bash
python3 -m lib.skill_registry search "testing"
```

Output:
```
Found 2 skills matching 'testing':
  - bmad-qa v1.0.0 (Quality Assurance)
    Testing strategy and quality assurance
  - test-runner v1.0.0 (Testing)
    Test execution and reporting
```

### 3. Get Recommendations

Get skill recommendations for a task:

```bash
python3 -m lib.skill_recommender recommend "Implement user authentication feature" implement
```

Output:
```
Top 3 Skill Recommendations:

1. bmad-dev v1.0.0
   Confidence: 85%
   Domain: Implementation
   Description: Implementation, coding, and development tasks
   Rationale: Matched keywords: implement, feature. High effectiveness (80%)
```

---

## Skill Registry

### What is the Skill Registry?

The Skill Registry is a centralized database of all RALF skills with metadata:

- **Name:** Unique skill identifier (e.g., "bmad-pm")
- **Version:** Semantic version (e.g., "1.0.0")
- **Domain:** Skill category (e.g., "Product Management")
- **Author:** Skill author
- **Description:** What the skill does
- **Tags:** Searchable keywords
- **Effectiveness Score:** Historical success rate (0.0 to 1.0)
- **Usage Count:** Number of times used

### Registry Storage

Location: `2-engine/.autonomous/config/skill-registry.yaml`

Format:
```yaml
registry_version: "1.0.0"
last_updated: "2026-02-01T14:35:00Z"
skills:
  - name: bmad-pm
    version: "1.0.0"
    domain: "Product Management"
    author: "John"
    description: "Product Manager - PRD creation and requirements"
    tags: ["prd", "requirements", "product"]
    created_at: "2026-01-01T00:00:00Z"
    effectiveness_score: 0.85
    usage_count: 12
    last_used: "2026-02-01T14:00:00Z"
```

### Registry Operations

#### List All Skills

```bash
python3 -m lib.skill_registry list
```

#### Get Skill Details

```bash
python3 -m lib.skill_registry get bmad-pm
```

#### Register a New Skill

```python
from lib.skill_registry import SkillRegistry

registry = SkillRegistry()
registry.register_skill(
    name="my-custom-skill",
    version="1.0.0",
    domain="Implementation",
    author="Your Name",
    description="My custom skill for X",
    tags=["custom", "x"]
)
```

#### Update Effectiveness

After using a skill, update its effectiveness:

```python
registry.update_skill_effectiveness("bmad-pm", success=True)
```

This updates the skill's effectiveness score and usage count automatically.

---

## Skill Versioning

### Semantic Versioning

Skills use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR:** Incompatible API changes
- **MINOR:** New functionality (backwards compatible)
- **PATCH:** Bug fixes (backwards compatible)

Examples:
- `1.0.0` → `1.0.1` (PATCH): Bug fix
- `1.0.0` → `1.1.0` (MINOR): New feature
- `1.0.0` → `2.0.0` (MAJOR): Breaking changes

### Version Operations

#### Compare Versions

```bash
python3 -m lib.skill_versioning compare "1.2.3" "1.2.4"
# Output: 1.2.3 < 1.2.4
```

#### Check Compatibility

Check if a version is compatible with required minimum:

```bash
python3 -m lib.skill_versioning compatible "1.2.0" "1.2.3"
# Output: 1.2.3 is compatible with 1.2.0

python3 -m lib.skill_versioning compatible "1.2.0" "2.0.0"
# Output: 2.0.0 is NOT compatible with 1.2.0 (MAJOR mismatch)
```

#### Increment Version

```bash
python3 -m lib.skill_versioning increment "1.2.3" patch
# Output: Incremented 1.2.3 -> 1.2.4

python3 -m lib.skill_versioning increment "1.2.3" minor
# Output: Incremented 1.2.3 -> 1.3.0

python3 -m lib.skill_versioning increment "1.2.3" major
# Output: Incremented 1.2.3 -> 2.0.0
```

#### Detect Breaking Changes

Check if a version update includes breaking changes:

```python
from lib.skill_versioning import has_breaking_changes

# Check if upgrading from 1.2.3 to 2.0.0 has breaking changes
breaking = has_breaking_changes("1.2.3", "2.0.0")
# Returns: True (MAJOR version change = breaking)
```

---

## Skill Recommendations

### How Recommendations Work

The recommendation engine analyzes task context and suggests relevant skills:

1. **Extract Keywords:** From task type, description, approach, files
2. **Match Patterns:** Against skill names, descriptions, tags, domains
3. **Calculate Confidence:** Based on:
   - Keyword overlap (40% weight)
   - Domain match (30% weight)
   - Historical effectiveness (20% weight)
   - Usage frequency (10% weight)
4. **Return Top-N:** Skills with confidence >= threshold

### Getting Recommendations

#### Using CLI

```bash
python3 -m lib.skill_recommender recommend "Implement REST API" implement
```

#### Using Python API

```python
from lib.skill_recommender import SkillRecommender

recommender = SkillRecommender()
task_context = {
    'type': 'implement',
    'description': 'Implement user authentication feature',
    'files': ['auth.py', 'user.py']
}

recommendations = recommender.recommend_skills(task_context, threshold=0.7)

for rec in recommendations:
    print(f"{rec.skill.name}: {rec.confidence:.1%}")
    print(f"  Rationale: {rec.rationale}")
```

### Recommendation Thresholds

- **70% (0.7):** Default threshold for executor skill invocation
- **> 80%:** High confidence, should invoke skill
- **70-80%:** Medium confidence, consider invoking skill
- **< 70%:** Low confidence, proceed with standard execution

---

## CLI Reference

### Skill Registry CLI

```bash
# Show registry statistics
python3 -m lib.skill_registry

# Search skills by keyword
python3 -m lib.skill_registry search <keyword>

# List all skills
python3 -m lib.skill_registry list

# Get skill details
python3 -m lib.skill_registry get <name>

# Auto-populate from skills/ directory
python3 -m lib.skill_registry auto-populate
```

### Skill Versioning CLI

```bash
# Compare two versions
python3 -m lib.skill_versioning compare <v1> <v2>

# Check compatibility
python3 -m lib.skill_versioning compatible <required> <current>

# Increment version
python3 -m lib.skill_versioning increment <version> <major|minor|patch>

# Validate version string
python3 -m lib.skill_versioning validate <version>

# Suggest next version
python3 -m lib.skill_versioning next <version> <patch|minor|major>
```

### Skill Recommender CLI

```bash
# Analyze task patterns
python3 -m lib.skill_recommender analyze "<description>" [type]

# Get recommendations
python3 -m lib.skill_recommender recommend "<description>" [type]
```

---

## Python API Reference

### SkillRegistry

```python
from lib.skill_registry import SkillRegistry

registry = SkillRegistry()

# Register a skill
skill = registry.register_skill(
    name="skill-name",
    version="1.0.0",
    domain="Domain",
    author="Author",
    description="Description",
    tags=["tag1", "tag2"]
)

# Search skills
skills = registry.search_skills(keyword="testing", domain="Quality Assurance")

# Get skill metadata
skill = registry.get_skill_metadata("skill-name")

# List all skills
skills = registry.list_skills(domain="Implementation", sort_by="usage_count")

# Update effectiveness
registry.update_skill_effectiveness("skill-name", success=True)

# Get statistics
stats = registry.get_stats()
```

### Skill Versioning

```python
from lib.skill_versioning import (
    parse_version,
    compare_versions,
    is_compatible,
    has_breaking_changes,
    suggest_next_version
)

# Parse version
version = parse_version("1.2.3")
# Returns: Version(major=1, minor=2, patch=3)

# Compare versions
result = compare_versions("1.2.3", "1.2.4")
# Returns: -1 (v1 < v2)

# Check compatibility
compatible = is_compatible("1.2.0", "1.2.3")
# Returns: True

# Detect breaking changes
breaking = has_breaking_changes("1.2.3", "2.0.0")
# Returns: True

# Suggest next version
next_version = suggest_next_version("1.2.3", VersionChangeType.MINOR)
# Returns: "1.3.0"
```

### SkillRecommender

```python
from lib.skill_recommender import SkillRecommender

recommender = SkillRecommender()

# Recommend skills
task_context = {
    'type': 'implement',
    'description': 'Implement feature X',
    'approach': 'Create new module',
    'files': ['module.py']
}

recommendations = recommender.recommend_skills(
    task_context,
    threshold=0.7,
    max_results=5
)

for rec in recommendations:
    print(f"{rec.skill.name}: {rec.confidence:.1%}")
    print(f"  Matched: {rec.matched_keywords}")
    print(f"  Rationale: {rec.rationale}")

# Get top-N recommendations
top_3 = recommender.get_top_recommendations(task_context, n=3)

# Analyze task patterns
analysis = recommender.analyze_task_patterns(
    task_description="Implement user authentication",
    task_type="implement"
)
```

---

## Contributing Skills

### Adding a New Skill

1. **Create Skill Directory**

```bash
mkdir -p /workspaces/blackbox5/2-engine/.autonomous/skills/my-skill
```

2. **Create SKILL.md**

```markdown
---
name: my-skill
description: My custom skill for X
category: agent
agent: CustomAgent
role: Specialist
trigger: When X is needed
inputs:
  - name: requirements
    type: document
    description: Task requirements
outputs:
  - name: result
    type: document
    description: Execution result
commands:
  - EXECUTE
---

# My Custom Skill

## Description
This skill does X...

## Usage
...
```

3. **Register in Marketplace**

```python
from lib.skill_registry import SkillRegistry

registry = SkillRegistry()
registry.register_skill(
    name="my-skill",
    version="1.0.0",
    domain="Custom Domain",
    author="Your Name",
    description="My custom skill for X",
    tags=["custom", "x"]
)
```

4. **Test Registration**

```bash
python3 -m lib.skill_registry get my-skill
```

### Skill Contribution Checklist

- [ ] Skill directory created in `2-engine/.autonomous/skills/`
- [ ] SKILL.md with frontmatter metadata
- [ ] Skill logic implemented
- [ ] Registered in skill registry
- [ ] Tested with sample tasks
- [ ] Documentation updated

---

## Troubleshooting

### Registry Not Found

**Problem:** `Registry file not found at skill-registry.yaml`

**Solution:** Run auto-populate to initialize registry:

```bash
python3 -m lib.skill_registry auto-populate
```

### Skill Not Found

**Problem:** `Skill not found: skill-name`

**Solution:**
1. Check skill is registered: `python3 -m lib.skill_registry list`
2. If not registered, run auto-populate
3. Verify skill name is correct

### Low Recommendation Confidence

**Problem:** Recommendations have low confidence (< 70%)

**Solution:**
1. Check skill metadata has good description and tags
2. Update skill effectiveness after successful uses
3. Adjust confidence weights in `skill_recommender.py`

### Version Comparison Errors

**Problem:** `Invalid semantic version: X.Y.Z`

**Solution:** Ensure version follows semantic versioning:
- Format: `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)
- All three parts required
- Must be integers

### Registry Stale

**Problem:** Registry doesn't reflect recent skill changes

**Solution:** Re-run auto-populate to refresh:

```bash
python3 -m lib.skill_registry auto-populate
```

---

## Best Practices

1. **Version Management**
   - Start at `1.0.0` for new skills
   - Increment PATCH for bug fixes
   - Increment MINOR for new features
   - Increment MAJOR for breaking changes

2. **Metadata Quality**
   - Write clear descriptions (what the skill does)
   - Add relevant tags (searchable keywords)
   - Set appropriate domain (category)

3. **Effectiveness Tracking**
   - Always update effectiveness after skill use
   - Use `success=True` for successful outcomes
   - Use `success=False` for failures

4. **Recommendation Accuracy**
   - Provide detailed task descriptions
   - Include task type (implement, fix, analyze)
   - List relevant files in task context

---

## Future Enhancements

**Phase 2 (Planned):**
- Skill dependency management
- Skill deprecation warnings
- Analytics dashboard
- CLI command completion

**Phase 3 (Future):**
- Machine learning for recommendations
- External skill repositories (GitHub integration)
- Community feedback system (ratings, reviews)

---

## Support

For issues or questions:
1. Check this guide's Troubleshooting section
2. Review feature spec: `plans/features/FEATURE-009-skill-marketplace.md`
3. Check library source code in `2-engine/.autonomous/lib/`

---

**End of User Guide**
