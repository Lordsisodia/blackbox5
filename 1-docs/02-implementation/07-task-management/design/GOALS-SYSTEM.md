# Goals System

> **Human-Directed Task Generation for RALF** - Design & Implementation

## Overview

The Goals System enables humans to specify high-level objectives for RALF to achieve. When no tasks are explicitly assigned, RALF checks for active goals before falling back to autonomous task generation.

## First Principles

1. **Direction Override**: Humans must be able to direct RALF toward specific objectives
2. **Cascade Effect**: High-level goals should break down into executable tasks
3. **Priority First**: Goal-derived tasks take precedence over autonomous generation
4. **Visibility**: Goals must be tracked and their progress visible

## Architecture

```
                    ┌─────────────────────────┐
                    │  No Active Tasks?       │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │  Check Active Goals     │◄───────┐
                    │  (goals/active/IG-XXX/) │        │
                    └───────────┬─────────────┘        │
                                │                      │
                      ┌─────────┴─────────┐            │
                      │   Goals Exist?    │            │
                      └─────────┬─────────┘            │
                     Yes       │       No             │
                ┌──────────────┴──────────────┐        │
                │                             │        │
         ┌──────▼──────┐              ┌──────▼──────▼──────┐
         │ Read Goal   │              │ Autonomous         │
         │ Find Next   │              │ Task Generation    │
         │ Sub-Goal    │              │ (4 Analyses)       │
         └──────┬──────┘              └────────────────────┘
                │
         ┌──────▼──────┐
         │ Create Task │
         │ Priority 90+│
         └─────────────┘
```

## Directory Structure

```
5-project-memory/blackbox5/goals/
├── README.md              # Goals system overview
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

## Goal Format

Goals use structured YAML files in subdirectories:

### goal.yaml Structure

```yaml
# Goal: {Goal Title}
# =============================================================================
goal_id: IG-XXX
name: "{Goal Name}"
description: "{Brief description}"

meta:
  created: "YYYY-MM-DD"
  target_completion: "YYYY-MM-DD"
  owner: "{agent-id}"
  priority: critical|high|medium|low
  status: not_started|in_progress|completed
  category: {category}

# =============================================================================
# SUB-GOALS
# =============================================================================

sub_goals:
  - id: SG-XXX-1
    name: "{Sub-goal name}"
    description: "{Sub-goal description}"
    weight: 40  # Percentage of total goal
    status: not_started|in_progress|completed

    acceptance_criteria:
      - "{Measurable outcome 1}"
      - "{Measurable outcome 2}"

    linked_tasks:
      - TASK-XXX
      - TASK-YYY

# =============================================================================
# PROGRESS TRACKING
# =============================================================================

progress:
  percentage: 35  # Auto: (completed_task_weight / total_weight) * 100
  last_updated: "YYYY-MM-DDTHH:MM:SSZ"

  by_sub_goal:
    SG-XXX-1: 85%  # Calculated from linked tasks
    SG-XXX-2: 0%

# =============================================================================
# NOTES & CONTEXT
# =============================================================================

context: |
  {Background information, motivation, and relevant details}

constraints:
  - "{Constraint 1}"
  - "{Constraint 2}"

notes: |
  {Additional thoughts, references, or considerations}
```

### timeline.yaml Structure

```yaml
events:
  - timestamp: "YYYY-MM-DDTHH:MM:SSZ"
    type: goal_created
    description: "Goal created by {agent}"

  - timestamp: "YYYY-MM-DDTHH:MM:SSZ"
    type: sub_goal_started
    sub_goal: SG-XXX-1
    task_created: TASK-XXX

  - timestamp: "YYYY-MM-DDTHH:MM:SSZ"
    type: task_completed
    task: TASK-XXX
    progress_delta: +20%
    agent: "{agent-id}"
```

### journal/ Directory

Narrative updates stored as dated markdown files:
- `journal/YYYY-MM-DD.md` - Daily updates, learnings, observations

### outcome.yaml (for completed goals)

```yaml
outcome:
  completion_date: "YYYY-MM-DDTHH:MM:SSZ"
  final_status: completed|abandoned|superseded
  success_percentage: 100

  lessons_learned:
    - "{Lesson 1}"
    - "{Lesson 2}"

  unexpected_results:
    - "{Result 1}"
    - "{Result 2}"

  next_steps:
    - "{Follow-up task 1}"
    - "{Follow-up task 2}"

  superseded_by:  # If applicable
    goal_id: IG-YYY
    reason: "{Why this goal was superseded}"
```

## Task Generation Logic

### Priority Score Calculation

```yaml
goal_cascade:
  base_score: 90
  multiplier: goal_priority
  reason: "Directed - human-specified priority"

decision_matrix:
  - if: active goals exist
    then: create GOAL_DERIVED task immediately
    because: human direction takes precedence over autonomous generation
```

### Goal Processing Steps

1. **Check for active goals**
   ```bash
   ls /opt/blackbox5/5-project-memory/blackbox5/goals/active/
   ```

2. **Read highest priority goal**
   - Sort by priority (critical > high > medium > low)
   - If tie, use creation date (older first)
   - Read each `IG-XXX/goal.yaml` file

3. **Find next incomplete sub-goal**
   - Scan `sub_goals` array in goal.yaml
   - Find first sub-goal with `status: not_started` or `in_progress`
   - Get task description from sub-goal

4. **Create derived task**
   - Task type: `GOAL_DERIVED`
   - Priority: 90+ (always HIGH)
   - Link to parent goal in context

## Usage

### Creating a New Goal

1. Create directory:
   ```bash
   mkdir -p /opt/blackbox5/5-project-memory/blackbox5/goals/active/IG-XXX
   ```

2. Copy and edit template:
   ```bash
   cp /opt/blackbox5/5-project-memory/blackbox5/goals/templates/goal-template.yaml \
      /opt/blackbox5/5-project-memory/blackbox5/goals/active/IG-XXX/goal.yaml
   ```

3. Fill in required fields:
   - `goal_id` (incremental: IG-001, IG-002, etc.)
   - `name` (descriptive)
   - `description` (brief summary)
   - `meta.priority` (critical|high|medium|low)
   - `sub_goals` array with acceptance criteria

4. Create initial timeline:
   ```bash
   touch /opt/blackbox5/5-project-memory/blackbox5/goals/active/IG-XXX/timeline.yaml
   ```

### Goal Lifecycle

```
┌─────────┐     ┌──────────┐     ┌─────────────┐
│ Created │────▶│  Active  │────▶│  Completed  │
└─────────┘     └──────────┘     └─────────────┘
                      │
                      │ (optional)
                      ▼
                ┌──────────┐
                │ Abandoned│
                └──────────┘
```

### Updating Goal Progress

As sub-goals complete, update the goal.yaml file:

```yaml
sub_goals:
  - id: SG-XXX-1
    name: "Sub-goal 1"
    status: completed  # Changed from in_progress
    linked_tasks:
      - TASK-001

  - id: SG-XXX-2
    name: "Sub-goal 2"
    status: in_progress  # Still in progress
    linked_tasks:
      - TASK-002
```

Add event to timeline.yaml:
```yaml
events:
  - timestamp: "2026-02-12T15:00:00Z"
    type: sub_goal_completed
    sub_goal: SG-XXX-1
    task: TASK-001
    agent: "{agent-id}"
```

### Completing a Goal

When all sub-goals are complete:

1. Verify all acceptance criteria met
2. Update status in goal.yaml to `completed`
3. Create outcome.yaml:
   ```yaml
   outcome:
     completion_date: "2026-02-12T15:00:00Z"
     final_status: completed
     success_percentage: 100
     lessons_learned:
       - "Lesson 1"
       - "Lesson 2"
   ```
4. Move entire directory to `goals/completed/`
5. Update INDEX.yaml

## Integration with RALF

### In ralf.md (bin/ralf.md)

The goals system is integrated into Step 2 (Alternate) of RALF's execution loop:

```yaml
## Step 2 (Alternate): Autonomous Task Generation

When `tasks/active/` is empty:

**FIRST: Check for Active Goals**

```bash
# Check goals directory for active goals
ls /opt/blackbox5/5-project-memory/blackbox5/goals/active/ 2>/dev/null
```

**If active goals exist:**
- Read the highest priority goal.yaml
- Find first incomplete sub-goal
- Create task to advance that goal
- **Priority Override:** Goal-derived tasks score 90+ priority

**If NO active goals exist:**
- Perform **ALL FOUR** analyses below
- Create the most impactful task
```

## Examples

### Example 1: Simple Feature Goal

```markdown
# GOAL-002: Add Dark Mode Support

**Status:** active
**Priority:** MEDIUM
**Created:** 2026-01-30T10:00:00Z
**Target Completion:** 2026-02-15
**Owner:** human

---

## Objective

Add dark mode support to the entire application for better user experience in low-light conditions.

## Success Criteria

- [ ] Dark mode toggle in settings
- [ ] All components support dark theme
- [ ] User preference persisted
- [ ] Documentation updated

## Sub-Goals

- [ ] **Sub-Goal 1:** Create theme context provider → Creates: TASK-101
- [ ] **Sub-Goal 2:** Update all components for theming → Creates: TASK-102
- [ ] **Sub-Goal 3:** Add settings UI → Creates: TASK-103
- [ ] **Sub-Goal 4:** Persist preference to localStorage → Creates: TASK-104
- [ ] **Sub-Goal 5:** Write documentation → Creates: TASK-105

## Context

Users have requested dark mode support. Current app only supports light theme.

## Constraints

- Must not break existing light theme
- Should work across all browsers
- Performance impact < 5%

## Notes

Consider using CSS-in-JS solution for easier theme switching.
```

### Example 2: Infrastructure Goal

```markdown
# GOAL-003: Migrate to Supabase Auth

**Status:** active
**Priority:** HIGH
**Created:** 2026-01-30T11:00:00Z
**Target Completion:** 2026-02-28
**Owner:** autonomous

---

## Objective

Replace custom authentication system with Supabase Auth for better security and reduced maintenance.

## Success Criteria

- [ ] Supabase Auth configured
- [ ] All users migrated
- [ ] All auth endpoints updated
- [ ] Old auth system removed
- [ ] Zero data loss

## Sub-Goals

- [ ] **Sub-Goal 1:** Set up Supabase project → Creates: TASK-201
- [ ] **Sub-Goal 2:** Design migration strategy → Creates: TASK-202
- [ ] **Sub-Goal 3:** Implement Supabase Auth → Creates: TASK-203
- [ ] **Sub-Goal 4:** Migrate existing users → Creates: TASK-204
- [ ] **Sub-Goal 5:** Update all auth flows → Creates: TASK-205
- [ ] **Sub-Goal 6:** Remove old auth system → Creates: TASK-206
- [ ] **Sub-Goal 7:** Test thoroughly → Creates: TASK-207

## Context

Current auth system has maintenance burden. Supabase Auth is more secure and actively maintained.

## Constraints

- Must maintain backward compatibility during migration
- Zero data loss requirement
- Cannot break existing sessions

## Notes

This is a critical migration. Requires careful testing before rollout.
```

## Best Practices

1. **Specific Objectives**: Goals should be clear and specific
2. **Measurable Criteria**: Success must be verifiable
3. **Appropriate Granularity**: Break complex goals into sub-goals
4. **Realistic Timelines**: Set achievable target dates
5. **Clear Ownership**: Specify human or autonomous owner
6. **Context Rich**: Provide enough background for autonomous agents
7. **Constraints Documented**: List limits and requirements
8. **Progress Tracked**: Update progress log regularly

## Anti-Patterns

- ❌ **Vague objectives**: "Make it better" (not actionable)
- ❌ **No success criteria**: Impossible to verify completion
- ❌ **Too large**: Monolithic goals that never complete
- ❌ **Missing context**: Autonomous agents can't understand intent
- ❌ **Unrealistic deadlines**: Sets up for failure
- ❌ **No sub-goals**: Complex goals need breakdown

## Implementation Status

✅ **Complete**
- Goals directory structure created
- Goal template defined
- Task generation logic updated to check goals first
- Documentation created
- First active goal created (GOAL-001: RALF v2.3 Integration Release)

## Related Documentation

- `~/.blackbox5/bin/ralf.md` - RALF execution loop
- `TASK-MANAGEMENT-SYSTEM.md` - Task tracking architecture
- `FRAMEWORK-IMPLEMENTATION-PLAN.md` - RALF framework overview

---

**Created:** 2026-01-30
**Version:** 1.0.0
**Status:** Complete
