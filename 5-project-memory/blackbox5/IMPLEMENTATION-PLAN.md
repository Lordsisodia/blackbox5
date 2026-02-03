# Implementation Plan: Intelligent Navigation & Template System

**Status:** Planning Complete
**Date:** 2026-02-04
**Scope:** Navigation commands, template auto-population, hooks

---

## Executive Summary

Based on research of existing systems, we need to implement:

1. **Navigation Commands** - CLI tools to traverse goals/plans/tasks hierarchy
2. **Template Auto-Population** - Scripts to create properly structured items from templates
3. **Navigation Hooks** - Pre-execution hooks that validate structure and guide agents

**What's Already Built:**
- ✅ Templates exist (`.templates/tasks/`, `goals/templates/`)
- ✅ Basic hooks exist (`ralf-session-start-hook.sh`, `ralf-stop-hook.sh`)
- ✅ Task selection script (`ralf-task-select.sh`)
- ✅ MAP.yaml file catalog
- ✅ Framework implementation plan (from 1-docs)

**What's Missing:**
- ❌ Navigation commands (no `bb5 goal:show`, `bb5 plan:list`, etc.)
- ❌ Template population scripts (manual creation only)
- ❌ Hierarchy-aware hooks (hooks don't know about goals/plans/tasks structure)
- ❌ Intelligent agent guidance (agent doesn't auto-discover context)

---

## Part 1: Navigation Commands

### 1.1 Command Structure

Create `bb5` CLI with these commands:

```bash
# Navigation Commands
bb5 whereami                    # Show current location in hierarchy
bb5 goal:show [GOAL-ID]         # Show goal details and linked plans
bb5 goal:list                   # List all goals
bb5 plan:show [PLAN-ID]         # Show plan details and linked tasks
bb5 plan:list                   # List all plans
bb5 task:show [TASK-ID]         # Show task details and subtasks
bb5 task:list                   # List all tasks
bb5 task:current                # Show current active task

# Hierarchy Navigation
bb5 up                          # Go up one level (task -> plan -> goal)
bb5 down [ID]                   # Go down to specific child
bb5 root                        # Go to project root
bb5 goto [GOAL|PLAN|TASK]-ID    # Jump to specific item

# Creation Commands (with template population)
bb5 goal:create [NAME]          # Create new goal from template
bb5 plan:create [NAME]          # Create new plan from template
bb5 task:create [NAME]          # Create new task from template
bb5 subtask:create [NAME]       # Create subtask under current task

# Linking Commands
bb5 link:goal [GOAL-ID]         # Link current item to goal
bb5 link:plan [PLAN-ID]         # Link current item to plan
bb5 link:task [TASK-ID]         # Link current item to task
```

### 1.2 Implementation

**Files to Create:**
- `bin/bb5` - Main CLI entry point
- `bin/bb5-whereami` - Location detection
- `bin/bb5-goal` - Goal commands
- `bin/bb5-plan` - Plan commands
- `bin/bb5-task` - Task commands
- `bin/bb5-goto` - Navigation commands
- `bin/bb5-create` - Creation commands

**Key Features:**
- Parse MAP.yaml for fast lookups
- Use symlinks to traverse hierarchy
- Color-coded output (green=active, yellow=in_progress, gray=completed)
- Tab completion support

---

## Part 2: Template Auto-Population

### 2.1 Current State

Templates exist but require **manual copying and filling**:
- `.templates/tasks/task-specification.md.template`
- `goals/templates/goal-template.yaml`
- Plans use `epic.md` template

### 2.2 Auto-Population Scripts

**Create these scripts:**

```bash
# Goal Creation
bb5 goal:create "Restructure Architecture"
↓
1. Creates folder: goals/active/IG-007/
2. Copies template: goal-template.yaml → goals/active/IG-007/goal.yaml
3. Auto-populates:
   - goal_id: IG-007 (auto-increment)
   - name: "Restructure Architecture"
   - created: today's date
   - owner: current agent
4. Creates subfolders: journal/, plans/
5. Creates timeline.yaml with today's date

# Plan Creation
bb5 plan:create "Migration Plan"
↓
1. Creates folder: plans/active/migration-plan/
2. Creates files:
   - plan.md (from template with populated name)
   - metadata.yaml (with created date, status: draft)
3. Creates subfolders: research/, tasks/

# Task Creation
bb5 task:create "Update Scripts"
↓
1. Creates folder: tasks/active/TASK-17699XXXX/
2. Creates files:
   - task.md (from template with populated fields)
   - THOUGHTS.md (empty)
   - DECISIONS.md (empty)
   - LEARNINGS.md (empty)
3. Creates subfolders: timeline/, subtasks/, artifacts/
4. Auto-populates task.yaml with:
   - task_id: auto-generated
   - created: today's date
   - status: pending
   - parent: current plan/goal (if in one)
```

### 2.3 Template Variables

**Support these variables in templates:**
- `{{GOAL_ID}}` - Auto-generated goal ID
- `{{PLAN_ID}}` - Auto-generated plan ID
- `{{TASK_ID}}` - Auto-generated task ID
- `{{NAME}}` - User-provided name
- `{{DATE}}` - Today's date
- `{{AGENT}}` - Current agent type
- `{{PARENT_GOAL}}` - Parent goal (if linked)
- `{{PARENT_PLAN}}` - Parent plan (if linked)

---

## Part 3: Navigation Hooks

### 3.1 Hook Types Needed

**SessionStart Hook (Enhanced):**
```bash
# Current: Creates run folder
# Enhanced: Also discovers context

1. Create run folder (existing)
2. Discover where we are:
   - Check if in a goal folder → load goal context
   - Check if in a plan folder → load plan context
   - Check if in a task folder → load task context
3. Load parent context (if in task, load plan + goal)
4. Write context to run folder:
   - CURRENT_CONTEXT.md (what we're working on)
   - PARENT_GOAL.md (if applicable)
   - PARENT_PLAN.md (if applicable)
5. Validate structure (warn if missing required files)
```

**PreToolUse Hook (New):**
```bash
# Before any tool use, validate context

1. Check if we're in a valid workspace
2. If Write tool: validate path is within project
3. If Bash tool: validate command is safe
4. If Task tool: validate subtask creation follows hierarchy
5. Log navigation: track where agent goes
```

**Stop Hook (Enhanced):**
```bash
# Current: Archives run, commits changes
# Enhanced: Also updates hierarchy

1. Complete run folder (existing)
2. Update parent task/plan/goal:
   - Add entry to timeline/
   - Update progress in metadata
3. If task completed:
   - Move from tasks/active/ to tasks/completed/
   - Update symlinks in parent plan
4. Commit with proper message including task ID
```

### 3.2 Context Discovery Script

**Create `bin/bb5-discover-context`:**
```bash
# Discovers current location in hierarchy

1. Check current working directory
2. Walk up tree looking for:
   - goals/active/GOAL-XXX/ → we're in a goal
   - plans/active/PLAN-XXX/ → we're in a plan
   - tasks/active/TASK-XXX/ → we're in a task
3. If in task, also find:
   - Parent plan (via symlink or search)
   - Parent goal (via parent plan)
4. Output structured context:
   {
     "current": "task",
     "task_id": "TASK-17699XXXX",
     "task_path": "...",
     "plan_id": "PLAN-XXX",
     "plan_path": "...",
     "goal_id": "GOAL-XXX",
     "goal_path": "..."
   }
```

---

## Part 4: Intelligent Agent Guidance

### 4.1 Context Injection

**Modify SessionStart hook to inject context into Claude's context:**

```markdown
# CURRENT CONTEXT (Auto-Generated)

You are working in: tasks/active/TASK-17699XXXX/

## Current Task
- ID: TASK-17699XXXX
- Name: "Update Scripts"
- Status: in_progress
- Goal: [from parent goal]

## Parent Plan
- ID: PLAN-XXX
- Name: "Migration Plan"

## Parent Goal
- ID: GOAL-006
- Name: "Restructure BlackBox5"

## Navigation
- To see goal: `bb5 goal:show IG-006`
- To see plan: `bb5 plan:show migration-plan`
- To go up: `bb5 up`

## Quick Commands
- `bb5 whereami` - Show current location
- `bb5 task:current` - Show current task details
- `bb5 goal:list` - List all goals
```

### 4.2 Auto-Detection

**Agent should auto-detect:**
- When entering a goal folder → show goal context
- When entering a plan folder → show plan + goal context
- When entering a task folder → show task + plan + goal context
- When creating new item → suggest template population

---

## Part 5: Implementation Phases

### Phase 1: Navigation Commands (Day 1-2)
- [ ] Create `bb5 whereami`
- [ ] Create `bb5 goal:list` and `bb5 goal:show`
- [ ] Create `bb5 plan:list` and `bb5 plan:show`
- [ ] Create `bb5 task:list` and `bb5 task:show`
- [ ] Create `bb5 goto`
- [ ] Add to PATH

### Phase 2: Template Auto-Population (Day 3-4)
- [ ] Create `bb5 goal:create`
- [ ] Create `bb5 plan:create`
- [ ] Create `bb5 task:create`
- [ ] Add template variable substitution
- [ ] Test all three creation flows

### Phase 3: Enhanced Hooks (Day 5-6)
- [ ] Enhance SessionStart hook with context discovery
- [ ] Create context injection system
- [ ] Enhance Stop hook with hierarchy updates
- [ ] Test hook integration

### Phase 4: Documentation (Day 7)
- [ ] Update CLAUDE.md with navigation commands
- [ ] Create navigation guide
- [ ] Add examples
- [ ] Test complete flow

---

## Part 6: Files to Create/Modify

### New Files
```
bin/
├── bb5                          # Main CLI
├── bb5-whereami                 # Location detection
├── bb5-goal                     # Goal commands
├── bb5-plan                     # Plan commands
├── bb5-task                     # Task commands
├── bb5-goto                     # Navigation
├── bb5-create                   # Creation commands
├── bb5-discover-context         # Context discovery
└── bb5-populate-template        # Template population

.claude/hooks/
├── session-start-navigation.sh  # Enhanced SessionStart
└── pre-tool-validation.sh       # PreToolUse hook
```

### Modified Files
```
.claude/CLAUDE.md                # Add navigation commands
bin/ralf-session-start-hook.sh   # Enhance with context
bin/ralf-stop-hook.sh            # Enhance with hierarchy updates
```

---

## Part 7: Success Criteria

- [ ] Agent can run `bb5 whereami` and see current location
- [ ] Agent can run `bb5 goal:show IG-006` and see goal + linked plans
- [ ] Agent can run `bb5 task:create "New Task"` and get populated template
- [ ] SessionStart hook injects current context into Claude
- [ ] Agent can navigate up/down hierarchy with `bb5 up` / `bb5 down`
- [ ] All templates auto-populate with correct IDs and dates
- [ ] Stop hook updates parent goal/plan/task on completion

---

## Next Steps

1. **Approve this plan**
2. **Prioritize phases** (which is most important?)
3. **Start implementation** (I can begin with Phase 1)

Which phase would you like me to start with?
