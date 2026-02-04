# Setup Summary: Claude Code Repo Analysis with Task Integration

## What's Been Created

### 1. Main Task Spec
**File:** `tasks/active/TASK-CC-REPO-ANALYSIS-001/task.md`
- Top-level task defining the full 8-phase workflow
- Integration between Claude Code Task system and RALF queue.yaml
- Success criteria and artifact structure

### 2. Implementation Plan
**File:** `tasks/active/TASK-CC-REPO-ANALYSIS-001/IMPLEMENTATION-PLAN.md`
- Architecture diagram showing both systems
- Phase-by-phase breakdown
- Integration points (status sync, queue format)
- File structure
- Commands reference

### 3. Phase A Task (Ready to Start)
**File:** `tasks/active/TASK-CC-REPO-ANALYSIS-001/subtasks/TASK-CC-001A/task.md`
**Queue Entry:** Added to `queue.yaml` as pending
**Claude Task:** #26 created with TaskCreate

## How to Run

### Option 1: Manual Execution (Now)

1. **Start an executor session** - The SessionStart hook will create a run folder
2. **Claim Task A:**
   ```bash
   ralf-task-select.sh --claim
   ```
3. **Execute the task** - Search GitHub, create repo-list.yaml
4. **Complete and archive** - Stop hook handles Phase 7

### Option 2: Use Claude Code Task System

Since Task #26 is created, you can:
1. Start a new Claude Code session
2. The task will be available in the task list
3. Work through the discovery phase
4. Mark Task #26 complete when done

### Option 3: Subagent Pattern (For Parallel Repo Analysis)

When doing Phase B (per-repo analysis), use the Task tool:

```bash
# In Task B-N-1 (Research)
TaskCreate:
  subject: "Research repo N structure"
  description: "Clone and analyze..."
  # This creates a parallel subagent
```

## Integration Points

### Claude Code Task → RALF Queue

When a Claude Task completes:
1. Stop hook fires
2. Updates queue.yaml status to "completed"
3. Moves task from active/ to completed/
4. Archives run folder

### RALF Queue → Claude Code Task

When executor claims a task:
1. Reads queue.yaml for pending tasks
2. Claims task (updates status, claimed_by)
3. Creates task working directory
4. Executes 7-phase flow

## Next Tasks to Create

After TASK-CC-001A completes, the Planner agent should create:

1. **TASK-CC-001B-1-1** (Research repo 1) - No blockers
2. **TASK-CC-001B-1-2** (Plan repo 1) - blockedBy: B-1-1
3. **TASK-CC-001B-1-3** (Execute repo 1) - blockedBy: B-1-2
4. **TASK-CC-001B-2-1** (Research repo 2) - No blockers
5. ... (repeat for each repo)
6. **TASK-CC-001C** (Planner Analysis) - blockedBy: all B-*-3

## Status

| Component | Status |
|-----------|--------|
| SessionStart Hook | ✅ Self-discovering |
| Stop Hook | ✅ Self-discovering |
| Task Select Script | ✅ Ready |
| Task Start Script | ✅ Ready |
| Executor v4 Prompt | ⚠️ Needs queue format update |
| Queue.yaml | ✅ Task A added |
| Claude Task #26 | ✅ Created |
| Main Task Spec | ✅ Created |
| Implementation Plan | ✅ Created |

## Immediate Next Steps

1. **Start Task A execution** - Either manually or via Task #26
2. **Update Executor v4 prompt** to match actual queue.yaml list format
3. **Test one full cycle** - From claim → execute → archive
4. **Verify integration** - Check that Claude Task completion updates queue.yaml

## Commands Reference

```bash
# Check queue
ralf-planner-queue.sh --check

# Claim task
ralf-task-select.sh --claim

# Start task
ralf-task-start.sh --task-id TASK-CC-001A

# View pending
ralf-planner-queue.sh --pending

# List Claude Tasks
TaskList
```
