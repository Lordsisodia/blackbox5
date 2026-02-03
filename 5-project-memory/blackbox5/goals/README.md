# Goals System

**Location:** `goals/`
**Purpose:** The nervous system of BlackBox5 - drives work, tracks progress, connects everything

---

## Philosophy

Goals are not just documents. They are:
- **Drivers** - Tasks get created from goals
- **Trackers** - What's actually happening vs what we planned
- **Connectors** - Tasks, plans, decisions, learnings all link back
- **Learners** - Did we achieve it? Why/why not?

---

## Structure

```
goals/
├── README.md              # This file
├── INDEX.yaml             # Auto-generated: all goals, quick lookup
│
├── core/                  # Perpetual goals (never complete)
│   └── core-goals.yaml    # CG-001, CG-002, CG-003
│
├── active/                # Improvement goals in progress
│   └── IG-XXX/            # Each goal gets a folder
│       ├── goal.yaml      # Definition + sub-goals
│       ├── timeline.yaml  # Structured events
│       └── journal/       # Narrative updates
│           └── YYYY-MM-DD.md
│
├── completed/             # Archived goals
│   └── IG-XXX/
│       ├── goal.yaml
│       ├── timeline.yaml
│       ├── outcome.yaml   # What actually happened
│       └── journal/
│
└── templates/
    └── goal-template.yaml
```

---

## How It Works

### Goal Lifecycle

1. **Created** → Folder created in `active/`, status: `not_started`
2. **Activated** → Status: `in_progress`, tasks created
3. **Progress** → Timeline updated, progress auto-calculated from tasks
4. **Completed** → Moved to `completed/`, outcome documented
5. **Archived** → Learnings extracted, linked to knowledge base

### Progress Tracking

Progress is **auto-calculated** from linked tasks:

```yaml
progress:
  percentage: 35  # Auto: (completed_task_weight / total_weight) * 100
  last_updated: "2026-02-02T10:00:00Z"

  by_sub_goal:
    SG-001: 85%  # Calculated from linked tasks
    SG-002: 0%
```

Agents update **task status**, system updates **goal progress**.

### Sub-Goals

Sub-goals are **inline** in goal.yaml:

```yaml
sub_goals:
  - id: SG-001
    name: "Consolidate folders"
    weight: 40  # Percentage of total goal
    linked_tasks:
      - TASK-001
      - TASK-002
```

If a sub-goal becomes too complex, it should become a separate goal.

### Timeline vs Journal

**timeline.yaml** (structured, for agents):
```yaml
events:
  - timestamp: "2026-02-02T10:00:00Z"
    type: task_completed
    task: TASK-001
    progress_delta: +20%
```

**journal/*.md** (narrative, for humans):
```markdown
# 2026-02-02

Completed task migration today. Found duplicate operations folders
that needed manual resolution. Skill-tracking guide moved successfully.
```

---

## For Agents

### Creating a Goal

1. Copy `templates/goal-template.yaml` to `active/IG-XXX/goal.yaml`
2. Fill in goal definition
3. Define 2-5 sub-goals inline
4. Set weights (must sum to 100)
5. Create empty `timeline.yaml` and `journal/` folder

### Updating Progress

1. Complete task in `tasks/`
2. System auto-updates goal progress
3. If sub-goal completes, add event to timeline
4. If goal completes, move folder to `completed/`

### Querying Goals

Read `INDEX.yaml` for quick lookup:
```yaml
critical_goals:
  - IG-006  # Restructure Architecture

blocked_goals:
  - IG-004  # No progress in 7 days
```

---

## For Humans

### Adding a New Goal

```bash
cd goals/active
cp ../templates/goal-template.yaml IG-007/goal.yaml
# Edit goal.yaml
mkdir -p IG-007/journal
touch IG-007/timeline.yaml
```

### Checking Status

```bash
cat goals/INDEX.yaml              # Quick overview
cat goals/active/IG-006/goal.yaml # Full details
cat goals/active/IG-006/journal/* # Recent updates
```

---

## Integration with Other Systems

### Tasks
- Tasks link back to goals via `linked_goal: IG-XXX`
- Tasks link to sub-goals via `linked_sub_goal: SG-XXX`
- Task completion auto-updates goal progress

### Decisions
- Decisions can reference goals they serve
- Goal timeline links to relevant decisions

### Knowledge
- Completed goals extract learnings to `knowledge/`
- Goal outcomes feed into first-principles reviews

---

## Success Criteria

A good goal system:
- [ ] Drives task creation (goals → tasks)
- [ ] Tracks reality (accurate progress)
- [ ] Enables learning (outcomes documented)
- [ ] Connects everything (links work both ways)
- [ ] Scales simply (flat structure, inline sub-goals)

---

## Questions?

See `templates/goal-template.yaml` for examples.
