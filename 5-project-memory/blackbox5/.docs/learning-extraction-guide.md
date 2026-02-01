# Learning Extraction Guide

**Purpose:** Document the methodology for extracting actionable improvement tasks from LEARNINGS.md files

**Created:** 2026-02-01

**Related:** TASK-1769902000

---

## Overview

This guide documents the systematic process for converting captured learnings into actionable improvement tasks. The extraction process addresses the critical bottleneck where 80+ learnings resulted in only 1 applied improvement (2% application rate).

## Extraction Methodology

### Step 1: Gather Learnings

**Action:** Collect all LEARNINGS.md files from archived runs

```bash
find $PROJECT_DIR/runs -name "LEARNINGS.md" -type f
```

**Output:** List of learning files with paths

### Step 2: Categorize Learnings

Read each LEARNINGS.md and categorize insights:

| Category | Description | Example |
|----------|-------------|---------|
| Process Improvements | Workflow enhancements | "Pre-execution research prevents duplicates" |
| Technical Discoveries | Code/technical insights | "Python dataclass syntax gotchas" |
| Documentation Gaps | Missing/outdated docs | "STATE.yaml drifts from reality" |
| Tool/Pattern Learnings | Tool usage patterns | "GitHub CLI requires full repo path" |

### Step 3: Identify Recurring Themes

Count mentions of similar issues across learnings:

```yaml
themes:
  - name: "Roadmap/State Synchronization"
    mentions: 7
    files:
      - run-1769861933/LEARNINGS.md
      - run-1769813746/LEARNINGS.md
      - run-20260131-060933/LEARNINGS.md
```

**Threshold:** Themes with 3+ mentions are candidates for improvement tasks

### Step 4: Extract Action Items

For each recurring theme, identify:

1. **Problem Statement** - What is the issue?
2. **Impact** - Why does it matter?
3. **Proposed Solution** - What should be done?
4. **Effort Estimate** - How long will it take?
5. **Acceptance Criteria** - How do we know it's done?

### Step 5: Create Improvement Tasks

Use the improvement task template:

```markdown
# IMP-{timestamp}: {Title}

**Type:** implement | fix | refactor | analyze
**Priority:** high | medium | low
**Category:** process | guidance | infrastructure | skills
**Source Learning:** L-{run-id}-{seq}
**Status:** pending

## Objective
Clear one-sentence goal.

## Problem Statement
Description of the issue.

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Approach
1. Step 1
2. Step 2

## Related Learnings
- run-{id}: "Learning title"

## Estimated Effort
XX minutes
```

### Step 6: Prioritize

Assign priority based on:

| Factor | Weight | High Priority If |
|--------|--------|------------------|
| Mention Count | 30% | 5+ mentions |
| Impact | 40% | Blocks work or causes rework |
| Effort | 20% | < 45 minutes |
| Risk | 10% | Low risk of breaking changes |

### Step 7: Document and Track

1. Create `operations/improvement-backlog.yaml`
2. Update `STATE.yaml` improvement_metrics
3. Document extraction methodology (this file)

## Quality Criteria

A good improvement task should have:

- [ ] Clear problem statement
- [ ] Specific success criteria (testable)
- [ ] Estimated effort
- [ ] Source learning references
- [ ] Concrete approach
- [ ] Single focus (not multiple problems)

## Templates

### Improvement Task Template

```markdown
# IMP-{timestamp}: {Title}

**Type:** {type}
**Priority:** {priority}
**Category:** {category}
**Source Learning:** {learning-ids}
**Status:** pending
**Created:** {ISO8601 timestamp}

---

## Objective

{One sentence goal}

## Problem Statement

{Description of issue}

## Success Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}

## Approach

1. {Step 1}
2. {Step 2}

## Files to Modify

- {path}: {change description}

## Related Learnings

- {run-id}: "{learning title}"

## Estimated Effort

{XX} minutes

## Acceptance Criteria

- [ ] {Specific check}
- [ ] {Specific check}
```

## Automation Opportunities

Future improvements to extraction:

1. **Pattern Detection** - Automatically identify recurring themes
2. **Action Item Extraction** - NLP to extract action items from text
3. **Duplicate Detection** - Check for similar existing improvements
4. **Effort Estimation** - ML model to estimate effort from description

## Success Metrics

Track extraction effectiveness:

```yaml
metrics:
  learnings_reviewed: 22
  improvements_created: 10
  extraction_rate: 45%  # 10 from 22 files
  high_priority_rate: 30%  # 3 of 10 are high
  avg_effort_minutes: 40
```

## Related Files

- `operations/improvement-backlog.yaml` - All improvement tasks
- `operations/improvement-pipeline.yaml` - Pipeline states
- `.templates/tasks/LEARNINGS.md.template` - Learning format
- `STATE.yaml` - Improvement metrics

---

**Last Updated:** 2026-02-01

**Maintained By:** RALF-Executor
