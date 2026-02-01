# Improvement Pipeline Guide

**Version:** 1.0.0
**Created:** 2026-02-01
**Related:** `operations/improvement-pipeline.yaml`

---

## Overview

The Improvement Pipeline is a structured system that converts captured learnings into actionable improvements. It addresses the critical bottleneck where 49 learnings resulted in only 1 improvement (2% application rate).

### Core Philosophy

> "Learning without application is just information. Application without validation is just activity."

The pipeline ensures:
1. Every learning has an **action item**
2. Action items become **improvement tasks**
3. Improvements are **validated** for effectiveness

---

## Pipeline Flow

```
┌──────────┐    ┌──────────┐    ┌─────────────┐    ┌──────────┐    ┌─────────────┐    ┌──────────┐
│ Captured │───▶│ Reviewed │───▶│ Prioritized │───▶│ Tasked   │───▶│ Implemented │───▶│ Validated│
└──────────┘    └──────────┘    └─────────────┘    └──────────┘    └─────────────┘    └──────────┘
     │               │                 │                │                │                │
     ▼               ▼                 ▼                ▼                ▼                ▼
  LEARNINGS    First Principles   IMP file created   Task queued    Changes         Metrics
  .md created  Review             in improvements/   in active/     committed       compared
```

---

## State Descriptions

### 1. Captured
- **Trigger:** Run completion with LEARNINGS.md created
- **Owner:** Executor
- **Requirements:**
  - Learning has `observation` field
  - Learning has `action_item` field
  - Category and impact assigned

### 2. Reviewed
- **Trigger:** First principles review (every 5 runs)
- **Owner:** Planner
- **Actions:**
  - Validate action item is concrete
  - Assign category and impact
  - Check for duplicates

### 3. Prioritized
- **Trigger:** Learning converted to improvement task
- **Owner:** Planner
- **Actions:**
  - Calculate priority (base + boosts)
  - Estimate effort
  - Set queue position

### 4. Tasked
- **Trigger:** IMP-*.md file created
- **Owner:** Planner
- **Requirements:**
  - Clear acceptance criteria
  - Validation method defined
  - Source learning linked

### 5. Implemented
- **Trigger:** Executor completes improvement task
- **Owner:** Executor
- **Requirements:**
  - Changes committed
  - Tests pass
  - Integration verified

### 6. Validated
- **Trigger:** Post-implementation metrics collected
- **Owner:** Planner
- **Actions:**
  - Compare before/after metrics
  - Determine success
  - Document outcomes

---

## Learning Format

Every learning MUST include an action item:

```yaml
learning:
  id: "L-{timestamp}-{seq}"
  category: "process|technical|documentation|skills|infrastructure"
  observation: "What was learned"
  impact: "high|medium|low"
  action_item: "Concrete, specific task to create"
  proposed_task:
    title: "Task title"
    type: "implement|fix|refactor|analyze"
    priority: "high|medium|low"
    effort_minutes: 30
  auto_create_task: false  # Set true for high-impact items
```

### Categories

| Category | Description | Example |
|----------|-------------|---------|
| `process` | Workflow improvements | "Pre-execution research prevents duplicates" |
| `technical` | Code patterns | "Import path resolution strategy" |
| `documentation` | Docs improvements | "Template files need .template extension" |
| `skills` | Skill effectiveness | "Skill X triggers too often" |
| `infrastructure` | System/tooling | "CI/CD pipeline needs shellcheck" |

### Impact Levels

| Level | Criteria | Priority Boost |
|-------|----------|----------------|
| `high` | Affects >50% of tasks, saves >10 min | +30 |
| `medium` | Affects 20-50%, saves 5-10 min | +15 |
| `low` | Affects <20%, saves <5 min | +5 |

---

## Improvement Task Format

Improvement tasks are created in `.autonomous/tasks/improvements/`:

```markdown
# IMP-{timestamp}: [Title]

**Source Learning:** L-{timestamp}-{seq}
**Category:** [category]
**Priority:** [priority]
**Status:** pending

## Objective
[Clear statement of what to improve]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Validation Method
[How to measure if this improvement worked]

## Approach
[Implementation steps]
```

---

## Queue Management

### Selection Rules

1. **If main queue < 3:** Pull from improvement queue
2. **If improvement priority > 80:** Can preempt main queue
3. **Every 3rd task:** Check improvement queue
4. **First principles review:** Pause main queue, process improvements

### Priority Calculation

```
base_priority = learning.impact_value
+ 5 if mentioned in 3+ learnings
+ 3 if learning from last 5 runs
+ 10 if blocking other improvements
+ 20 because it's an improvement task
```

---

## First Principles Review

### When
Every 5 runs (runs divisible by 5: 50, 55, 60...)

### Process (40 minutes max)

1. **Gather Data** (10 min)
   - Read LEARNINGS.md from last 5 runs
   - Review current improvement backlog
   - Check metrics trends

2. **Pattern Recognition** (15 min)
   - Identify recurring themes (3+ mentions)
   - Categorize learnings
   - Assess past improvement effectiveness

3. **Course Correction** (10 min)
   - Create tasks for top 3 themes
   - Update priorities
   - Archive stale improvements

4. **Set Next Focus** (5 min)
   - Define 3 priorities for next 5 runs
   - Update STATE.yaml
   - Document outcomes

---

## Validation Framework

### Metrics Tracked

| Metric | Before Source | After Source | Threshold |
|--------|---------------|--------------|-----------|
| Task completion time | Avg last 10 tasks | Avg next 10 tasks | 10% reduction |
| Error rate | Failed in last 10 | Failed in next 10 | 20% reduction |
| Context efficiency | Avg context % | Avg context % | 15% reduction |
| Learning quality | Actionable/total | Actionable/total | 25% increase |

### Validation Schedule

- **Immediate:** After 3 tasks
- **Short-term:** After 10 tasks (next review)
- **Long-term:** After 30 tasks (monthly)

### Success Criteria

- At least 1 metric improves
- No metric degrades >10%
- Improvement sustains for 10+ tasks

---

## Usage Examples

### Example 1: Capturing a Learning

```yaml
learning:
  id: "L-1769900001-001"
  category: "process"
  observation: "Pre-execution research prevents duplicate tasks"
  impact: "high"
  action_item: "Make pre-execution research mandatory in LEGACY.md"
  proposed_task:
    title: "Add mandatory pre-execution research step"
    type: "implement"
    priority: "high"
    effort_minutes: 20
  auto_create_task: true
```

### Example 2: Creating an Improvement Task

```markdown
# IMP-1769900001: Add Mandatory Pre-Execution Research

**Source Learning:** L-1769900001-001
**Category:** process
**Priority:** 95
**Status:** pending

## Objective
Add a mandatory pre-execution research step to LEGACY.md to prevent duplicate tasks.

## Success Criteria
- [ ] LEGACY.md updated with research step
- [ ] Check for duplicates before any task execution
- [ ] Document research findings in THOUGHTS.md

## Validation Method
Track duplicate task creation rate before/after change.
```

### Example 3: First Principles Review

```yaml
review:
  run: 50
  learnings_reviewed: 15
  themes_identified:
    - name: "Documentation drift"
      mentions: 5
      action: "Create IMP-1769900002: Auto-flag stale docs"
    - name: "Skill discovery slow"
      mentions: 4
      action: "Create IMP-1769900003: Cache frequently used skills"
  improvements_created: 2
  metrics_updated:
    improvement_application_rate: 15%
```

---

## Troubleshooting

### "No action items in learnings"
- Check LEARNINGS.md template is being used
- Ensure `action_item` field is populated
- Review learning format in pipeline.yaml

### "Improvements not being picked up"
- Check improvement queue not full (max 15)
- Verify priority calculation (should be >60)
- Ensure selection rules allow improvement tasks

### "Validation shows no improvement"
- Check metrics are being tracked correctly
- Verify before/after data sources
- Consider if improvement needs more time

---

## Related Files

- `operations/improvement-pipeline.yaml` - Pipeline definition
- `.templates/tasks/LEARNINGS.md.template` - Learning template
- `.autonomous/tasks/improvements/` - Improvement task queue
- `STATE.yaml` - Metrics and review schedule
- `goals.yaml` - Improvement goals

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-01 | 1.0.0 | Initial pipeline guide |
