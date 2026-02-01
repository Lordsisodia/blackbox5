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
                    │  (goals/active/*.md)    │        │
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
5-project-memory/ralf-core/.autonomous/goals/
├── active/           # Currently active goals
│   └── GOAL-XXX-*.md
├── completed/        # Completed goals
│   └── GOAL-XXX-*.md
└── templates/        # Goal templates
    └── goal-template.md
```

## Goal Format

Goals use YAML frontmatter + markdown:

```markdown
# GOAL-{ID}: {Title}

**Status:** active
**Priority:** {HIGH|MEDIUM|LOW}
**Created:** {YYYY-MM-DDTHH:MM:SSZ}
**Target Completion:** {YYYY-MM-DD}
**Owner:** {human|autonomous}

---

## Objective

{Clear statement of the high-level goal}

## Success Criteria

- [ ] {Measurable outcome 1}
- [ ] {Measurable outcome 2}
- [ ] {Measurable outcome 3}

## Sub-Goals (Optional)

Break down complex goals into smaller milestones:

- [ ] **Sub-Goal 1:** {Description} → Creates: {TASK-XXXX}
- [ ] **Sub-Goal 2:** {Description} → Creates: {TASK-XXXX}
- [ ] **Sub-Goal 3:** {Description} → Creates: {TASK-XXXX}

## Context

{Background information, motivation, and relevant details}

## Constraints

- {Constraint 1}
- {Constraint 2}

## Notes

{Additional thoughts, references, or considerations}

---

## Progress Log

| Date | Event | Task Created |
|------|-------|--------------|
| {DATE} | Goal created | - |
| {DATE} | Sub-goal 1 started | TASK-XXXX |
| {DATE} | Sub-goal 1 completed | - |

## Completion

**Completed:** {YYYY-MM-DDTHH:MM:SSZ}
**Final Status:** {completed|abandoned|superseded}
**Outcome:** {Summary of results}
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
   ls ~/.blackbox5/5-project-memory/ralf-core/.autonomous/goals/active/*.md
   ```

2. **Read highest priority goal**
   - Sort by priority (HIGH > MEDIUM > LOW)
   - If tie, use creation date (older first)

3. **Find next incomplete sub-goal**
   - Scan `## Sub-Goals` section
   - Find first unchecked `[ ]` item
   - Extract task description

4. **Create derived task**
   - Task type: `GOAL_DERIVED`
   - Priority: 90+ (always HIGH)
   - Link to parent goal in context

## Usage

### Creating a New Goal

1. Copy the template:
   ```bash
   cp ~/.blackbox5/5-project-memory/ralf-core/.autonomous/goals/templates/goal-template.md \
      ~/.blackbox5/5-project-memory/ralf-core/.autonomous/goals/active/GOAL-{ID}-{title}.md
   ```

2. Fill in required fields:
   - ID (incremental: GOAL-001, GOAL-002, etc.)
   - Title (descriptive)
   - Objective (clear statement)
   - Success criteria (measurable outcomes)
   - Sub-goals (breakdown if complex)

3. Save to `goals/active/`

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

As sub-goals complete, update the goal file:

```markdown
## Sub-Goals

- [x] **Sub-Goal 1:** {Description} → Creates: TASK-001 (completed)
- [ ] **Sub-Goal 2:** {Description} → Creates: TASK-002 (in progress)
- [ ] **Sub-Goal 3:** {Description} → Creates: TASK-XXXX
```

Add to Progress Log:
```markdown
| 2026-01-30 | Sub-goal 1 completed | TASK-001 |
```

### Completing a Goal

When all success criteria are met:

1. Mark all sub-goals as complete
2. Update status to `completed`
3. Fill in Completion section:
   ```markdown
   **Completed:** 2026-01-30T15:00:00Z
   **Final Status:** completed
   **Outcome:** Successfully implemented [feature]
   ```
4. Move to `goals/completed/`

## Integration with RALF

### In ralf.md (bin/ralf.md)

The goals system is integrated into Step 2 (Alternate) of RALF's execution loop:

```yaml
## Step 2 (Alternate): Autonomous Task Generation

When `tasks/active/` is empty:

**FIRST: Check for Active Goals**

```bash
# Check goals directory for active goals
ls ~/.blackbox5/5-project-memory/ralf-core/.autonomous/goals/active/*.md 2>/dev/null
```

**If active goals exist:**
- Read the highest priority goal
- Find first incomplete sub-goal or success criterion
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
