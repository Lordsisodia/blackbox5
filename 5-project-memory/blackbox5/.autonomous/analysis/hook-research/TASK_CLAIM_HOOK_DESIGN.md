# Task Claim Hook - Design Document

**Status:** Design Phase - Pending Review
**Purpose:** Hook that fires when agent selects/claims a task

---

## The Problem

Currently:
- Agent has to manually navigate goals → plans → tasks
- Agent has to create task folder structure manually
- Agent may not know where to document
- No automatic context injection at task selection time

Desired:
- Hook fires when agent claims/selects a task
- Automatically creates task folder with all required files
- Injects full context (goal, plan, task hierarchy)
- Agent knows exactly where to work and document

---

## Proposed Solution: TaskClaim Hook

### When It Fires

Options:
1. **UserPromptSubmit** - Detect "claim task" or "select task" intent
2. **SessionStart** - If agent starts in a task context
3. **Explicit command** - `/claim TASK-001` triggers hook
4. **File watcher** - Detect when `.task-claimed` file is created

**Recommended:** Hybrid approach using UserPromptSubmit + explicit command

### What It Does

```yaml
Phase 1 - Task Selection Detection:
  - Parse user prompt for task selection patterns:
    - "claim TASK-001"
    - "select task TASK-001"
    - "work on TASK-001"
    - "start TASK-001"
  - Or detect explicit /claim command

Phase 2 - Context Loading:
  - Load task.md from tasks/active/TASK-001/
  - Parse task metadata (title, objective, acceptance criteria)
  - Find linked plan from task.md
  - Load plan.md from plans/active/PLAN-XXX/
  - Find linked goal from plan.md
  - Load goal.md from goals/active/IG-XXX/
  - Build full hierarchy: Goal → Plan → Task

Phase 3 - Task Folder Creation:
  - Create run folder: runs/run-YYYYMMDD-HHMMSS-TASK-001/
  - Create THOUGHTS.md with full context:
    - Goal context (what are we trying to achieve)
    - Plan context (how does this task fit)
    - Task context (what specifically to do)
    - Acceptance criteria (how do we know it's done)
  - Create DECISIONS.md
  - Create ASSUMPTIONS.md
  - Create LEARNINGS.md
  - Create RESULTS.md
  - Create timeline.yaml entry
  - Create metadata.yaml with task reference

Phase 4 - Queue Update:
  - Update queue.yaml: mark task as "claimed"
  - Add claimed_by: run_id
  - Add claimed_at: timestamp

Phase 5 - Context Injection:
  - Inject full hierarchy into Claude's context
  - Show: "You are working on TASK-001 as part of PLAN-XXX for IG-XXX"
  - Provide quick links to all relevant files
```

### Input Format

```json
{
  "hook_event": "UserPromptSubmit",
  "prompt": "claim TASK-001",
  "detected_intent": "task_claim",
  "task_id": "TASK-001"
}
```

Or via explicit command:
```bash
bb5 claim TASK-001
# This creates .claim-request file that hook reads
```

### Output Format

```json
{
  "hookSpecificOutput": {
    "hookEventName": "TaskClaim",
    "additionalContext": "Task Claimed: TASK-001 | Goal: IG-008 | Plan: PLAN-003 | Run: run-20260206-143200-TASK-001",
    "task": {
      "id": "TASK-001",
      "title": "Implement Task Claim Hook",
      "goal": "IG-008: Autonomous Hook System",
      "plan": "PLAN-003: Hook Infrastructure",
      "run_dir": "runs/run-20260206-143200-TASK-001/"
    },
    "files_created": [
      "runs/run-20260206-143200-TASK-001/THOUGHTS.md",
      "runs/run-20260206-143200-TASK-001/DECISIONS.md",
      "runs/run-20260206-143200-TASK-001/ASSUMPTIONS.md",
      "runs/run-20260206-143200-TASK-001/LEARNINGS.md",
      "runs/run-20260206-143200-TASK-001/RESULTS.md",
      "runs/run-20260206-143200-TASK-001/timeline.yaml",
      "runs/run-20260206-143200-TASK-001/metadata.yaml"
    ]
  }
}
```

---

## THOUGHTS.md Template (Task Claim Context)

```markdown
# THOUGHTS: TASK-001 - Implement Task Claim Hook

**Claimed:** 2026-02-06T14:32:00Z
**Agent Type:** executor
**Run:** run-20260206-143200-TASK-001

---

## Goal Context (IG-008: Autonomous Hook System)

**Objective:** Build a comprehensive hook system for BB5 that enables autonomous agent execution

**Why This Matters:** Hooks are the backbone of agent coordination and task management

**Success Criteria:**
- [ ] SessionStart hook implemented
- [ ] TaskClaim hook implemented
- [ ] Stop hook implemented

---

## Plan Context (PLAN-003: Hook Infrastructure)

**Plan Objective:** Create the infrastructure for BB5 hooks

**This Task's Role:** Implement the TaskClaim hook that fires when agents select tasks

**Dependencies:**
- SessionStart hook (for context loading)
- Queue system (for task tracking)

**Deliverables:**
- TaskClaim hook implementation
- Documentation templates
- Queue integration

---

## Task Context (TASK-001)

**Objective:** Create a hook that fires when an agent claims/selects a task

**Acceptance Criteria:**
- [ ] Hook detects task selection intent
- [ ] Hook loads full goal/plan/task hierarchy
- [ ] Hook creates task folder with all required files
- [ ] Hook updates queue.yaml
- [ ] Hook injects context into agent

**Approach:**
1. Design hook architecture
2. Implement task detection
3. Implement context loading
4. Implement folder creation
5. Test with real tasks

---

## Assumptions

<!-- Document assumptions as you discover them -->

---

## Progress Log

<!-- Chronological record of work -->

---

*Task claimed: 2026-02-06T14:32:00Z*
```

---

## Implementation Options

### Option 1: UserPromptSubmit Hook (Recommended)

```python
#!/usr/bin/env python3
"""TaskClaim hook - detects task selection and sets up context."""

import json
import sys
import re
import os
from datetime import datetime
from pathlib import Path

# Task selection patterns
TASK_CLAIM_PATTERNS = [
    r'claim\s+(TASK-\d+)',
    r'select\s+(TASK-\d+)',
    r'start\s+(TASK-\d+)',
    r'work\s+on\s+(TASK-\d+)',
    r'pick\s+up\s+(TASK-\d+)',
]

def detect_task_claim(prompt):
    """Detect if user is trying to claim a task."""
    for pattern in TASK_CLAIM_PATTERNS:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def load_task_hierarchy(task_id):
    """Load goal → plan → task hierarchy."""
    project_root = os.environ.get('BB5_PROJECT_ROOT', '.')

    # Load task
    task_path = Path(project_root) / 'tasks' / 'active' / task_id / 'task.md'
    task_data = parse_task_md(task_path)

    # Load plan
    plan_id = task_data.get('plan_id')
    plan_path = Path(project_root) / 'plans' / 'active' / plan_id / 'plan.md'
    plan_data = parse_plan_md(plan_path)

    # Load goal
    goal_id = plan_data.get('goal_id')
    goal_path = Path(project_root) / 'goals' / 'active' / goal_id / 'goal.md'
    goal_data = parse_goal_md(goal_path)

    return {
        'goal': goal_data,
        'plan': plan_data,
        'task': task_data
    }

def create_task_folder(task_id, hierarchy):
    """Create run folder with all required files."""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    run_id = f"run-{timestamp}-{task_id}"

    project_root = Path(os.environ.get('BB5_PROJECT_ROOT', '.'))
    run_dir = project_root / 'runs' / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # Create all documentation files
    create_thoughts_md(run_dir, task_id, hierarchy)
    create_decisions_md(run_dir, task_id)
    create_assumptions_md(run_dir, task_id)
    create_learnings_md(run_dir, task_id)
    create_results_md(run_dir, task_id)
    create_timeline_yaml(run_dir, task_id)
    create_metadata_yaml(run_dir, task_id, run_id)

    return run_dir, run_id

def update_queue_yaml(task_id, run_id):
    """Mark task as claimed in queue."""
    # Implementation here
    pass

def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)
    prompt = input_data.get('prompt', '')

    # Detect task claim intent
    task_id = detect_task_claim(prompt)

    if not task_id:
        # Not a task claim - allow normal processing
        sys.exit(0)

    try:
        # Load full hierarchy
        hierarchy = load_task_hierarchy(task_id)

        # Create task folder
        run_dir, run_id = create_task_folder(task_id, hierarchy)

        # Update queue
        update_queue_yaml(task_id, run_id)

        # Output context injection
        output = {
            "hookSpecificOutput": {
                "hookEventName": "TaskClaim",
                "additionalContext": f"Task Claimed: {task_id} | Goal: {hierarchy['goal']['id']} | Plan: {hierarchy['plan']['id']} | Run: {run_id}",
                "task": {
                    "id": task_id,
                    "title": hierarchy['task']['title'],
                    "goal": hierarchy['goal']['id'],
                    "plan": hierarchy['plan']['id'],
                    "run_dir": str(run_dir)
                }
            }
        }

        print(json.dumps(output))
        sys.exit(0)

    except Exception as e:
        print(f"TaskClaim hook error: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block on error

if __name__ == '__main__':
    main()
```

### Option 2: Explicit bb5 claim Command

```bash
# User runs:
bb5 claim TASK-001

# This:
# 1. Creates .claim-request file with task_id
# 2. Triggers SessionStart hook to read it
# 3. SessionStart sets up context
```

### Option 3: File Watcher Pattern

```bash
# Agent creates:
touch tasks/active/TASK-001/.claim-request

# File watcher hook detects this:
# - Reads task_id from path
# - Sets up context
# - Removes .claim-request
```

---

## Integration with Existing Hooks

```
User says: "claim TASK-001"
    |
    v
UserPromptSubmit Hook (TaskClaim)
    - Detects claim intent
    - Loads hierarchy
    - Creates folder
    - Updates queue
    - Injects context
    |
    v
SessionStart Hook (if new session)
    - Detects RALF_RUN_DIR already set
    - Loads task context
    - Verifies folder exists
    |
    v
Agent works with full context
    |
    v
Stop Hook
    - Validates documentation
    - Triggers RETAIN
    - Updates queue (task completed)
```

---

## Benefits

1. **Agent knows exactly what to do** - Full context injected
2. **Proper folder structure** - All files created automatically
3. **No manual navigation** - Goal → Plan → Task loaded automatically
4. **Queue integration** - Task status updated automatically
5. **Documentation guidance** - Templates show what to document

---

## Open Questions

1. Should this block and require confirmation?
2. What if task is already claimed?
3. What if task doesn't exist?
4. Should it work with subtasks?
5. How does it interact with planner vs executor agents?

---

*Design pending review by 3 sub-agents*
