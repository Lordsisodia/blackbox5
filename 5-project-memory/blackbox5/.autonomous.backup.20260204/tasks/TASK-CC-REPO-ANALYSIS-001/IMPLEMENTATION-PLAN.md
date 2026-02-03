# Implementation Plan: Claude Code Repo Analysis with Task Integration

## Overview

This document shows how to integrate the Claude Code GitHub repo analysis workflow with both:
1. **Claude Code's native Task system** (orchestration, dependencies, parallel execution)
2. **RALF queue.yaml** (executor work tracking, status lifecycle)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE TASK SYSTEM                       │
│  (Orchestration layer - handles dependencies, parallelism)      │
├─────────────────────────────────────────────────────────────────┤
│  TASK-CC-001A (Discovery)                                       │
│       │                                                         │
│       ▼                                                         │
│  TASK-CC-001B-1-* (Repo 1, 3 cycles) ◄────► TASK-CC-001B-2-*   │
│       │                                    (Repo 2, 3 cycles)   │
│       ▼                                                         │
│  TASK-CC-001C (Planner Analysis)                                │
│       │                                                         │
│       ▼                                                         │
│  TASK-CC-001D-* (Deep Dive)                                     │
│       │                                                         │
│       ▼                                                         │
│  TASK-CC-001E (Data Analysis)                                   │
│       │                                                         │
│       ▼                                                         │
│  TASK-CC-001F (Task Generation) ──► queue.yaml                  │
│       │                              (RALF executor tasks)      │
│       ▼                                                         │
│  TASK-CC-001G (Verification)                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RALF SYSTEM                                 │
│  (Execution layer - 7-phase flow, status tracking)              │
├─────────────────────────────────────────────────────────────────┤
│  queue.yaml                                                     │
│    - TASK-GEN-001 (from Phase F)                                │
│    - TASK-GEN-002 (from Phase F)                                │
│    - TASK-GEN-003 (from Phase F)                                │
│                                                                 │
│  Executor Agent picks up tasks → 7-phase execution             │
│  - Phase 1: Runtime init (hook)                                 │
│  - Phase 2: Read prompt                                         │
│  - Phase 3: Task selection (from queue.yaml)                    │
│  - Phase 4: Task folder creation                                │
│  - Phase 5: Context & execution                                 │
│  - Phase 6: Logging & completion                                │
│  - Phase 7: Archive (hook)                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase-by-Phase Implementation

### Phase A: Discovery (Planner Agent)

**Claude Code Task Creation:**
```bash
# This would be done by the Planner agent
# Task A has no blockers - starts immediately
```

**Task A Work:**
1. Search GitHub for "Claude Code" related repos
2. Filter: >100 stars, active in last 6 months
3. Select top 5 repos
4. Create Task B subtasks with dependencies

**RALF Integration:**
- Update `queue.yaml` with discovery task
- Mark complete when repos identified

---

### Phase B: Per-Repo Analysis (Executor + Subagents)

**Claude Code Task Structure:**
```yaml
# For each repo N, create 3 tasks with dependencies
TASK-CC-001B-N-1:  # Research
  description: "Clone and analyze repo N structure"
  # No blockers

TASK-CC-001B-N-2:  # Plan
  description: "Create implementation plan from research"
  blockedBy: ["TASK-CC-001B-N-1"]

TASK-CC-001B-N-3:  # Execute
  description: "Document findings and create artifacts"
  blockedBy: ["TASK-CC-001B-N-2"]
```

**Subagent Pattern (inside each task):**
```bash
# Task B-N-1 uses subagent for research
type: Task
subagent_type: general-purpose
prompt: |
  Clone repo {owner}/{repo}
  Analyze:
  - Directory structure
  - Key files (README, package.json, etc.)
  - Architecture patterns
  - Dependencies
  Output: structure.yaml, key-files.md
```

**Repeat 3x per repo** = 9 subagent calls per repo

---

### Phase C: Planner Analysis

**Claude Code Task:**
```yaml
TASK-CC-001C:
  description: "Synthesize findings across all repos"
  blockedBy: ["TASK-CC-001B-1-3", "TASK-CC-001B-2-3", ...]
```

**Work:**
- Read all repo analysis artifacts
- Identify common patterns
- Generate insights report

---

### Phase D-F: Continue Chain

Same pattern - each phase is a Claude Code Task with:
- Clear description
- blockedBy dependencies on previous phase
- Work that feeds into next phase

---

### Phase G: Verification (QA Agent)

**Claude Code Task:**
```yaml
TASK-CC-001G:
  description: "Verify all artifacts and cross-references"
  blockedBy: ["TASK-GEN-001", "TASK-GEN-002", ...]  # All generated tasks
```

---

## Integration Points

### 1. Task Status Sync

When a Claude Code Task completes, update RALF:

```bash
# In stop hook or task completion script
if [ "$CLAUDE_TASK_STATUS" = "completed" ]; then
    # Update queue.yaml
    awk -v task_id="$TASK_ID" '
        /task_id:.*task_id/ { in_task = 1 }
        in_task && /status:/ { print "    status: completed"; next }
        { print }
    ' queue.yaml
fi
```

### 2. Queue.yaml Format for Generated Tasks

```yaml
queue:
  - task_id: TASK-GEN-001
    title: "Implement pattern X from repo analysis"
    priority: high
    status: pending
    source: "TASK-CC-001F"  # Link to parent Claude Task
    claude_task_id: "TASK-CC-001F"
    artifacts_required:
      - "analysis/synthesis-report.md"
```

### 3. Executor Reads Both Systems

Executor v4 prompt updated to:
1. Check `queue.yaml` for pending tasks
2. Check Claude Code Task system for blocked tasks
3. Claim work from appropriate source

---

## Running the Workflow

### Option 1: Manual (Current)

1. Create main task:
```bash
# User creates top-level task
```

2. Planner agent creates subtasks:
```bash
# Planner reads this plan
# Creates Task A with TaskCreate
# Task A creates Task B-* with blockedBy dependencies
```

3. Executor agents pick up work:
```bash
# Each executor session:
# 1. SessionStart hook creates run folder
# 2. Read executor prompt
# 3. Check queue.yaml for pending task
# 4. Claim and execute
# 5. Stop hook archives
```

### Option 2: Semi-Autonomous (Next)

Create orchestrator script that:
1. Polls queue.yaml depth
2. Spawns executor sessions when work available
3. Monitors Claude Task completion
4. Triggers next phases when dependencies met

### Option 3: Fully Autonomous (Future)

Claude Code plugin with:
- PreToolUse hook monitors task status
- Automatically spawns subagents
- Manages Task dependencies
- Self-healing (retries failed tasks)

---

## File Structure

```
5-project-memory/blackbox5/
├── tasks/active/
│   └── TASK-CC-REPO-ANALYSIS-001/
│       ├── task.md              # This main task spec
│       ├── IMPLEMENTATION-PLAN.md  # This file
│       └── subtasks/            # Generated subtask specs
│           ├── TASK-CC-001A.md
│           ├── TASK-CC-001B-1-1.md
│           └── ...
│
├── .autonomous/agents/communications/
│   ├── queue.yaml               # Executor work queue
│   ├── events.yaml              # Task lifecycle events
│   └── tasks.yaml               # Master task list
│
└── runs/
    ├── executor/                # Executor run folders
    └── planner/                 # Planner run folders

6-roadmap/.research/external/GitHub/
├── repos/                       # Repo analysis artifacts
├── analysis/                    # Synthesis reports
└── verification/                # QA reports
```

---

## Next Steps

1. **Create Task A** (Discovery) - No dependencies, can start now
2. **Update Executor v4 prompt** to handle both queue.yaml and Claude Tasks
3. **Test one repo cycle** - Full B-1-1 → B-1-2 → B-1-3 flow
4. **Verify integration** - Ensure queue.yaml updates when Claude Tasks complete
5. **Scale to 5 repos** - Run full workflow

---

## Commands

```bash
# Check queue status
ralf-planner-queue.sh --check

# Claim next task (executor)
ralf-task-select.sh --claim

# Mark task started
ralf-task-start.sh --task-id TASK-XXX

# View pending tasks
ralf-planner-queue.sh --pending
```
