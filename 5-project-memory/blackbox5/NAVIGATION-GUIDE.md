# BlackBox5 Navigation Guide

**Version:** 1.0.0
**Last Updated:** 2026-02-04

This guide documents the `bb5` CLI navigation system for traversing the goals/plans/tasks hierarchy.

---

## Quick Start

```bash
# See where you are
bb5 whereami

# List all goals
bb5 goal:list

# Show specific goal
bb5 goal:show IG-006

# Create a new task
bb5 task:create "Fix navigation bug"

# Navigate up (task → plan → goal)
bb5 up
```

---

## Command Reference

### Navigation Commands

| Command | Description | Example |
|---------|-------------|---------|
| `bb5 whereami` | Show current location in hierarchy | `bb5 whereami` |
| `bb5 goal:list` | List all active goals | `bb5 goal:list` |
| `bb5 goal:show [ID]` | Show goal details and linked plans | `bb5 goal:show IG-006` |
| `bb5 plan:list` | List all active plans | `bb5 plan:list` |
| `bb5 plan:show [ID]` | Show plan details and linked tasks | `bb5 plan:show my-plan` |
| `bb5 task:list` | List all active tasks | `bb5 task:list` |
| `bb5 task:show [ID]` | Show task details and subtasks | `bb5 task:show TASK-123` |
| `bb5 task:current` | Show current task (from context) | `bb5 task:current` |

### Hierarchy Navigation

| Command | Description | Example |
|---------|-------------|---------|
| `bb5 up` | Go up one level (task → plan → goal) | `bb5 up` |
| `bb5 down [ID]` | Go down to specific child | `bb5 down TASK-123` |
| `bb5 root` | Go to project root | `bb5 root` |
| `bb5 goto [ID]` | Jump to specific item by ID | `bb5 goto IG-006` |

### Creation Commands

| Command | Description | Example |
|---------|-------------|---------|
| `bb5 goal:create [NAME]` | Create new goal from template | `bb5 goal:create "Improve Performance"` |
| `bb5 plan:create [NAME]` | Create new plan from template | `bb5 plan:create "Optimization Plan"` |
| `bb5 task:create [NAME]` | Create new task from template | `bb5 task:create "Refactor caching"` |
| `bb5 subtask:create [NAME]` | Create subtask under current task | `bb5 subtask:create "Update tests"` |

### Linking Commands

| Command | Description | Example |
|---------|-------------|---------|
| `bb5 link:goal [ID]` | Link current plan to goal | `bb5 link:goal IG-006` |
| `bb5 link:plan [ID]` | Link current task to plan | `bb5 link:plan my-plan` |

---

## Typical Workflows

### Starting a New Goal

```bash
# Create the goal
bb5 goal:create "Improve System Performance"

# Navigate to it
bb5 goto IG-007

# Create a plan
bb5 plan:create "Performance Optimization"

# Link plan to goal
bb5 link:goal IG-007

# Create tasks
bb5 task:create "Profile bottlenecks"
bb5 link:plan performance-optimization

bb5 task:create "Implement caching"
bb5 link:plan performance-optimization
```

### Working on an Existing Task

```bash
# Find the task
bb5 task:list

# Navigate to it
bb5 goto TASK-1234567890

# Check context
bb5 whereami

# Show task details
bb5 task:current

# Create subtask
bb5 subtask:create "Write tests"

# Navigate up when done
bb5 up
```

### Daily Standup - What Did I Work On?

```bash
# Go to project root
bb5 root

# List all active tasks
bb5 task:list

# Check specific task status
bb5 task:show TASK-1234567890
```

---

## Auto-Discovered Context

When you start a session in a goal/plan/task directory, the system automatically creates `CURRENT_CONTEXT.md` in your run folder with:

- Current location (type, ID)
- Hierarchy (parent goal, plan, task)
- Quick navigation commands
- Structure validation status

Example:
```markdown
# Current Context (Auto-Generated)

## You Are Here
- **Type:** task
- **ID:** TASK-1234567890

## Hierarchy
- **Goal:** IG-006
- **Plan:** project-memory-reorganization
- **Task:** TASK-1234567890

## Quick Navigation
```bash
bb5 whereami              # Show current location
bb5 up                    # Go up one level
bb5 task:current          # Show current task details
```
```

---

## Template Auto-Population

When you create items with `bb5 create`, templates are automatically populated with:

- `{{ID}}` - Auto-generated ID (IG-XXX, TASK-$(date +%s))
- `{{NAME}}` - Item name you provided
- `{{DATE}}` - Today's date (YYYY-MM-DD)
- `{{DATETIME}}` - ISO timestamp
- `{{AGENT}}` - Current agent type

---

## Directory Structure

The hierarchy follows this pattern:

```
~/.blackbox5/5-project-memory/blackbox5/
├── goals/
│   └── active/
│       └── IG-XXX/              # Goal folder
│           ├── goal.yaml        # Goal definition
│           ├── timeline.yaml    # Progress tracking
│           ├── journal/         # Daily notes
│           └── plans/           # Symlinks to plans
│               └── PLAN-NAME -> ../../../plans/active/PLAN-NAME
├── plans/
│   └── active/
│       └── PLAN-NAME/           # Plan folder
│           ├── plan.md          # Plan documentation
│           ├── metadata.yaml    # Estimates, status
│           ├── research/        # Research findings
│           └── tasks/           # Symlinks to tasks
│               └── TASK-XXX -> ../../../tasks/active/TASK-XXX
└── tasks/
    └── active/
        └── TASK-XXX/            # Task folder
            ├── task.md          # Task specification
            ├── THOUGHTS.md      # Execution thinking
            ├── DECISIONS.md     # Key decisions
            ├── LEARNINGS.md     # Post-completion insights
            ├── timeline/        # Daily progress
            ├── subtasks/        # Nested subtasks
            └── artifacts/       # Generated files
```

---

## Hooks Integration

The system includes three enhanced hooks:

1. **session-start-navigation.sh** - Creates CURRENT_CONTEXT.md on session start
2. **pre-tool-validation.sh** - Warns if writing to directories without proper structure
3. **stop-hierarchy-update.sh** - Updates parent timelines on session completion

---

## Tips

1. **Always use `bb5 whereami`** when you start to confirm your location
2. **Use `bb5 up`** to navigate back to parent items
3. **Link items** with `bb5 link:goal` and `bb5 link:plan` to maintain hierarchy
4. **Check CURRENT_CONTEXT.md** for auto-discovered context
5. **Use tab completion** (if configured) for faster navigation

---

## Troubleshooting

### "Not in goals/plans/tasks hierarchy"
Run `bb5 root` to go to the project root, then navigate from there.

### "Goal/Plan/Task not found"
Use the list commands to see available items:
```bash
bb5 goal:list
bb5 plan:list
bb5 task:list
```

### "Missing task.md"
Create the task properly:
```bash
bb5 task:create "Task Name"
```

---

## Files Location

- CLI scripts: `~/.blackbox5/bin/bb5*`
- Hooks: `~/.blackbox5/.claude/hooks/`
- This guide: `~/.blackbox5/5-project-memory/blackbox5/NAVIGATION-GUIDE.md`
