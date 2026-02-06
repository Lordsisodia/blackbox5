# Claude Code @path Imports Guide for BlackBox5

> Version: 1.0.0
> Created: 2026-02-06
> Purpose: Comprehensive guide for using @path imports in Claude Code memory system

---

## 1. Introduction

Claude Code supports a powerful `@path` import syntax that allows you to dynamically include file contents into the conversation context. This is especially valuable for BlackBox5 projects where state is distributed across many YAML files.

### What Are @path Imports?

`@path` imports are special references that tell Claude Code to:
1. Read the file at the specified path
2. Include its contents in the conversation context
3. Refresh automatically when the file changes

### Why Use @path Imports in BB5?

BlackBox5 projects maintain state across many files:
- `STATE.yaml` - Project structure and current status
- `goals.yaml` - Autonomous agent goals
- `timeline.yaml` - Project milestones and history
- Task files - Individual work items
- Goal files - Detailed goal specifications

Using @path imports:
- **Eliminates manual copy-paste** of file contents
- **Ensures context is always current** (auto-refresh)
- **Reduces context window usage** (only include what you need)
- **Enables modular CLAUDE.md** files that stay synchronized

---

## 2. Import Syntax

### 2.1 Basic File Import

```
@/path/to/file.yaml
```

Imports a file relative to the project root.

**BB5 Example:**
```
@/STATE.yaml
@/goals.yaml
@/timeline.yaml
```

### 2.2 Directory Import (All Files)

```
@/path/to/directory/
```

Imports all files in a directory.

**BB5 Example:**
```
@/goals/active/
@/tasks/active/
@/operations/
```

### 2.3 Home Directory Import

```
@~/path/to/file
```

Imports from the user's home directory.

**BB5 Example:**
```
@~/.claude/CLAUDE.md
@~/.blackbox5/5-project-memory/blackbox5/STATE.yaml
```

### 2.4 Wildcard Patterns

```
@/path/to/*.yaml
@/path/to/TASK-*.md
```

Imports files matching a pattern.

**BB5 Example:**
```
@/goals/active/*/goal.yaml
@/tasks/active/TASK-*/task.md
```

### 2.5 Multiple Specific Files

```
@/file1.yaml @/file2.yaml @/file3.yaml
```

Import multiple files in one line.

---

## 3. BB5 Use Cases

### 3.1 Importing Current Goals

**File:** `@/goals.yaml`

**Purpose:** Keep autonomous agent goals synchronized

**When to Import:**
- At session start to understand current priorities
- When making architectural decisions
- When prioritizing tasks

**Example:**
```markdown
## Current Goals

@/goals.yaml
```

**Result:** Full goals document is included, showing:
- Core goals (CG-001, CG-002, CG-003)
- Improvement goals (IG-001 through IG-006)
- Data collection goals
- Review schedules

---

### 3.2 Importing Specific Goal Details

**File:** `@/goals/active/IG-007/goal.yaml`

**Purpose:** Get detailed information about a specific goal

**When to Import:**
- When working on a specific improvement goal
- To check sub-goal progress
- To find linked tasks

**Example:**
```markdown
## Active Architecture Goal

@/goals/active/IG-007/goal.yaml
```

---

### 3.3 Importing Project State

**File:** `@/STATE.yaml`

**Purpose:** Get complete project structure and status

**When to Import:**
- At session start for full context
- When navigating the project
- To check active tasks and recent activity

**Example:**
```markdown
## Project State

@/STATE.yaml
```

**Result:** Includes:
- Root files map
- Folder structure (6-folder organization)
- Templates catalog
- Active tasks list
- System status
- Improvement metrics

---

### 3.4 Importing Timeline

**File:** `@/timeline.yaml`

**Purpose:** Understand project history and milestones

**When to Import:**
- To check recent activity
- To understand project phases
- To find completed milestones

**Example:**
```markdown
## Project Timeline

@/timeline.yaml
```

---

### 3.5 Importing Specific Task Files

**File:** `@/tasks/active/TASK-*/task.md`

**Purpose:** Get details about a specific task

**When to Import:**
- When assigned a new task
- To check task requirements
- To understand success criteria

**Example:**
```markdown
## Current Task

@/tasks/active/TASK-ARCH-016/task.md
```

---

### 3.6 Importing All Active Tasks

**Pattern:** `@/tasks/active/`

**Purpose:** See all pending work

**When to Import:**
- When prioritizing work
- To check for dependencies
- To understand queue depth

**Example:**
```markdown
## Active Tasks

@/tasks/active/
```

---

### 3.7 Importing Operations Configuration

**File:** `@/operations/skill-selection.yaml`

**Purpose:** Access skill selection rules

**When to Import:**
- Before starting Phase 2 (Execution) of any task
- When deciding whether to use a skill

**Example:**
```markdown
## Skill Selection Rules

@/operations/skill-selection.yaml
```

---

### 3.8 Importing AGENT_CONTEXT

**File:** `@/AGENT_CONTEXT.md`

**Purpose:** Get auto-generated context for current run

**When to Import:**
- At session start
- When agent type detection is needed

**Example:**
```markdown
## Agent Context

@/AGENT_CONTEXT.md
```

---

## 4. Creating a Unified CLAUDE.md

A unified CLAUDE.md uses @path imports to create a living document that stays synchronized with BB5 state.

### 4.1 Recommended Structure

```markdown
---
name: BlackBox5 Project Configuration
version: 1.0.0
includes:
  - @~/.claude/OUTPUT_STYLE.md
---

# BlackBox5 Project Configuration

## Quick Reference

@/AGENT_CONTEXT.md

## Current State

@/STATE.yaml

## Active Goals

@/goals.yaml

## Recent Timeline

@/timeline.yaml

## Active Tasks

@/tasks/active/

## Skill Selection

@/operations/skill-selection.yaml

## Project Context

@/project/context.yaml
```

### 4.2 Benefits of Unified CLAUDE.md

1. **Always Current:** Files refresh automatically when modified
2. **Single Source of Truth:** No duplication between CLAUDE.md and BB5 files
3. **Reduced Maintenance:** Update BB5 files, CLAUDE.md stays current
4. **Modular:** Include only what you need for each session type

### 4.3 Session-Type Specific CLAUDE.md

Create specialized CLAUDE.md files for different session types:

**For Planning Sessions:**
```markdown
# Planning Session Context

@/goals.yaml
@/plans/active/
@/timeline.yaml
```

**For Task Execution:**
```markdown
# Task Execution Context

@/tasks/active/TASK-*/task.md
@/operations/skill-selection.yaml
@/STATE.yaml
```

**For Architecture Work:**
```markdown
# Architecture Context

@/goals/active/IG-007/goal.yaml
@/decisions/architectural/
@/knowledge/architecture/
```

---

## 5. Dynamic Imports and Auto-Refresh

### 5.1 How Auto-Refresh Works

When you use `@/file.yaml` in a conversation:
1. Claude Code reads the file at conversation start
2. If the file changes during the conversation, it does NOT auto-refresh
3. For new sessions, the latest version is always loaded

### 5.2 Forcing a Refresh

To get the latest version mid-conversation:
```
Please re-read @/STATE.yaml
```

Or use the Read tool explicitly.

### 5.3 Best Practices for Dynamic Content

1. **Reference, don't copy:** Use @path instead of pasting content
2. **Version-sensitive files:** For files that change frequently, note the timestamp
3. **Multiple sessions:** Each new session gets fresh imports

---

## 6. Best Practices

### 6.1 What to Import vs. Keep Inline

| Import | Keep Inline |
|--------|-------------|
| State files (STATE.yaml) | Session-specific decisions |
| Goals (goals.yaml) | Task-specific approach |
| Timeline (timeline.yaml) | Current run THOUGHTS.md |
| Task definitions | Execution progress |
| Skill configurations | Skill selection rationale |
| Project context | Validation results |

### 6.2 Import Order Matters

Place imports in logical order:
1. **Context first** - AGENT_CONTEXT.md, STATE.yaml
2. **Goals second** - goals.yaml, specific goal files
3. **Tasks third** - Active tasks, current task
4. **Reference last** - Skill configs, templates

### 6.3 Avoid Over-Importing

Don't import everything:
- **Bad:** `@/` (entire project)
- **Good:** `@/STATE.yaml` + `@/goals.yaml`

Be selective to preserve context window.

### 6.4 Use Relative Paths

Always use paths relative to project root:
- **Good:** `@/goals.yaml`
- **Bad:** `@~/blackbox5/goals.yaml` (unless cross-project)

### 6.5 Document Your Imports

Add comments explaining why you import each file:
```markdown
## Project State
@/STATE.yaml
<!-- Current structure, active tasks, system status -->

## Goals
@/goals.yaml
<!-- Autonomous agent priorities and improvement targets -->
```

---

## 7. Practical Examples

### Example 1: Session Start Template

```markdown
# BB5 Session Start

## Who Am I?
@/AGENT_CONTEXT.md

## What's the Current State?
@/STATE.yaml

## What Are We Working Toward?
@/goals.yaml

## What's In Progress?
@/tasks/active/
```

**Use Case:** Start every BB5 session with this template for complete context.

---

### Example 2: Task-Specific Context

```markdown
# Task: TASK-ARCH-016

## Task Definition
@/tasks/active/TASK-ARCH-016/task.md

## Related Goal
@/goals/active/IG-007/goal.yaml

## Skill Selection Rules
@/operations/skill-selection.yaml
```

**Use Case:** When assigned a specific task, import its definition and related context.

---

### Example 3: Architecture Decision Context

```markdown
# Architecture Decision Context

## Current Architecture Goal
@/goals/active/IG-007/goal.yaml

## Related Decisions
@/decisions/architectural/

## Architecture Knowledge
@/knowledge/architecture/

## Active Architecture Tasks
@/tasks/active/TASK-ARCH-*/
```

**Use Case:** When making architectural decisions, import relevant context.

---

### Example 4: First Principles Review

```markdown
# First Principles Review (Run 55)

## Improvement Metrics
@/STATE.yaml
<!-- Check improvement_metrics section -->

## Recent Learnings
@/runs/run-*/LEARNINGS.md

## Timeline
@/timeline.yaml
```

**Use Case:** Every 5 runs, conduct a first principles review.

---

### Example 5: Skill Usage Decision

```markdown
# Skill Selection for This Task

## Skill Selection Rules
@/operations/skill-selection.yaml

## Domain Mapping
@/operations/skill-selection.yaml
<!-- Check domain_mapping section -->

## Current Task
@/tasks/active/TASK-*/task.md
```

**Use Case:** Before Phase 2 (Execution), check skill selection rules.

---

### Example 6: Goal Progress Check

```markdown
# Goal Progress Review

## All Goals
@/goals.yaml

## Specific Goal Details
@/goals/active/IG-007/goal.yaml

## Timeline Progress
@/timeline.yaml
```

**Use Case:** Monthly goal review or progress check.

---

### Example 7: Queue Depth Analysis

```markdown
# Task Queue Analysis

## Active Tasks
@/tasks/active/

## Timeline Events
@/timeline.yaml
<!-- Check recent activity section -->

## System Status
@/STATE.yaml
<!-- Check activity metrics -->
```

**Use Case:** Analyze workload and queue depth.

---

### Example 8: Cross-Project Context

```markdown
# Cross-Project Work

## BB5 State
@~/.blackbox5/5-project-memory/blackbox5/STATE.yaml

## Siso-Internal State
@~/.blackbox5/5-project-memory/siso-internal/STATE.yaml

## Engine State
@~/.blackbox5/2-engine/STATE.yaml
```

**Use Case:** When working across multiple BB5 projects.

---

### Example 9: Run Documentation

```markdown
# Run Documentation Template

## Run Context
@/AGENT_CONTEXT.md

## Current Task
@/tasks/active/TASK-*/task.md

## Goals Context
@/goals.yaml

## To Document
- THOUGHTS.md - @/runs/run-*/THOUGHTS.md
- DECISIONS.md - @/runs/run-*/DECISIONS.md
- LEARNINGS.md - @/runs/run-*/LEARNINGS.md
```

**Use Case:** Template for documenting a new run.

---

### Example 10: Post-Run Analysis

```markdown
# Post-Run Analysis

## Run Results
@/runs/run-*/RESULTS.md

## Learnings Captured
@/runs/run-*/LEARNINGS.md

## Decisions Made
@/runs/run-*/DECISIONS.md

## Timeline Update
@/timeline.yaml
```

**Use Case:** Analyze completed run and update project state.

---

## 8. Troubleshooting

### 8.1 File Not Found

**Error:** `@/file.yaml` not found

**Solutions:**
1. Check the file exists: `ls /Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/file.yaml`
2. Use correct path from project root
3. For home directory files, use `@~/`

### 8.2 Import Not Refreshing

**Issue:** File changed but import shows old content

**Solutions:**
1. Start a new conversation session
2. Explicitly request: "Please re-read @/file.yaml"
3. Use Read tool directly

### 8.3 Too Much Context

**Issue:** Imports consuming too much context window

**Solutions:**
1. Be more selective - import specific files, not directories
2. Use partial reads for large files
3. Import only what's needed for current task

### 8.4 Circular References

**Issue:** CLAUDE.md includes itself via @path

**Solution:** Never import the CLAUDE.md file itself. Keep CLAUDE.md content inline.

---

## 9. Quick Reference Card

```
COMMON BB5 IMPORTS
==================

Project State:
  @/STATE.yaml
  @/AGENT_CONTEXT.md
  @/MAP.yaml

Goals & Planning:
  @/goals.yaml
  @/goals/active/IG-*/goal.yaml
  @/plans/active/

Tasks:
  @/tasks/active/
  @/tasks/active/TASK-*/task.md

Timeline & History:
  @/timeline.yaml
  @/runs/run-*/

Configuration:
  @/operations/skill-selection.yaml
  @/operations/skill-metrics.yaml
  @/project/context.yaml

Knowledge:
  @/knowledge/architecture/
  @/decisions/architectural/

SYNTAX PATTERNS
===============

Single file:     @/path/to/file.yaml
Directory:       @/path/to/directory/
Home directory:  @~/path/to/file
Multiple files:  @/file1.yaml @/file2.yaml
```

---

## 10. Migration Guide

### Converting Existing CLAUDE.md to Use @path

**Before:**
```markdown
# Project Configuration

## Goals
- CG-001: Continuous Self-Improvement
- CG-002: Ship Features Autonomously
... (manually maintained)
```

**After:**
```markdown
# Project Configuration

## Goals
@/goals.yaml

## State
@/STATE.yaml
```

### Steps:
1. Identify content that exists in BB5 files
2. Replace inline content with @path imports
3. Test imports in new conversation
4. Remove duplicate content
5. Document the imports

---

## Related Documentation

- @/NAVIGATION-GUIDE.md - BB5 navigation guide
- @/.docs/dot-docs-system.md - .docs/ system specification
- @/.docs/template-system-guide.md - Template usage guide
- @/README.md - Project overview

---

*This guide uses @path imports. Reference it with: @/.docs/CLAUDE-IMPORTS-GUIDE.md*
