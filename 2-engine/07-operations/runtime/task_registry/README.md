# Task Registry System

> Single source of truth for hierarchical task execution tracking

## Overview

The Task Registry System provides execution tracking for the 3D planning structure already defined in epic.md and TASK-BREAKDOWN.md. It bridges the gap between planning and execution.

## Architecture

```
task_registry.json (Single Source of Truth)
         │
         ▼
┌─────────────────────────────────────────┐
│           TaskRegistry                  │
│  - load() / save()                      │
│  - get_task() / list_tasks()            │
│  - create_task() / update_task()        │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│          StateMachine                   │
│  - transition(task, new_state)          │
│  - validate_dependencies()              │
│  - propagate_to_parent()                │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         WorkspaceFactory                │
│  - create_workspace(task_id)            │
│  - initialize_structure()               │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│           CLI Commands                  │
│  task list, task take, task complete    │
└─────────────────────────────────────────┘
```

## Data Schema

### Task Registry (task_registry.json)

```json
{
  "version": "1.0",
  "last_updated": "2026-01-21T10:00:00Z",
  "tasks": {
    "TASK-2026-01-18-001": {
      "id": "TASK-2026-01-18-001",
      "objective": "user-profile",
      "phase": "foundation",
      "title": "Validate database schema",
      "description": "Ensure Supabase schema matches PRD requirements",
      "state": "BACKLOG",
      "assignee": null,
      "assigned_at": null,
      "started_at": null,
      "completed_at": null,
      "dependencies": [],
      "blocks": ["TASK-2026-01-18-002"],
      "workspace": "./workspaces/TASK-2026-01-18-001/",
      "github_issue": 201,
      "github_url": "https://github.com/siso-agency-internal/issues/201",
      "tags": ["database", "validation"],
      "priority": "high",
      "created_at": "2026-01-18T09:00:00Z",
      "updated_at": "2026-01-21T10:00:00Z"
    }
  },
  "statistics": {
    "total": 18,
    "by_state": {
      "BACKLOG": 15,
      "ASSIGNED": 0,
      "ACTIVE": 2,
      "DONE": 1
    },
    "by_objective": {
      "user-profile": 18
    }
  }
}
```

### Task States

```
BACKLOG    → ASSIGNED → ACTIVE → DONE
             ↓          ↓         ↓
             └──────────┴────────→ FAILED
```

| State | Description | Entry Criteria |
|-------|-------------|----------------|
| BACKLOG | Task not yet assigned | Default initial state |
| ASSIGNED | Task assigned to agent | Agent claims task, dependencies met |
| ACTIVE | Agent actively working | Agent marks as started |
| DONE | Task completed | Agent marks complete, validates |
| FAILED | Task failed | Agent marks failed with reason |

### Workspace Structure

```
workspaces/TASK-2026-01-18-001/
├── timeline/                    # State transition history
│   ├── 2026-01-21-10-00-created.json
│   ├── 2026-01-21-10-05-assigned.json
│   ├── 2026-01-21-10-10-started.json
│   └── 2026-01-21-11-30-completed.json
├── thoughts/                    # Agent thought dumps
│   ├── initial-analysis.md
│   └── design-decisions.md
├── context/                     # Task context materials
│   ├── prd-requirements.md
│   └── database-schema.sql
├── work/                        # Work in progress
│   ├── schema-validation.sql
│   └── migration-plan.md
└── result.json                  # Final output
```

## CLI Interface

### Query Commands

```bash
# List all tasks
task list

# Filter by state
task list --state BACKLOG
task list --state ACTIVE

# Filter by objective
task list --objective user-profile

# Show assignable tasks (dependencies met, not assigned)
task available

# Show what I can work on
task what-can-i-do

# Get task details
task status TASK-2026-01-18-001

# Show what's blocking a task
task what-is-blocking TASK-2026-01-18-001
```

### Execution Commands

```bash
# Assign task to yourself
task take TASK-2026-01-18-001

# Mark task as started (ACTIVE state)
task start TASK-2026-01-18-001

# Mark task as complete
task complete TASK-2026-01-18-001

# Mark task as failed
task fail TASK-2026-01-18-001 "Database connection failed"

# Navigate to workspace
task workspace TASK-2026-01-18-001
```

### Admin Commands

```bash
# Import tasks from epic.md
task import-from-epic plans/active/user-profile/epic.md

# Sync with GitHub
task sync-github

# Generate statistics
task stats
```

## Integration Points

### Vibe Kanban

Vibe Kanban filters `task_registry.json` for active tasks:

```python
import json
from pathlib import Path

def get_active_tasks():
    registry = json.loads(Path("task_registry.json").read_text())
    return [t for t in registry["tasks"].values() if t["state"] == "ACTIVE"]
```

File watching for auto-refresh:

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class TaskRegistryHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("task_registry.json"):
            refresh_kanban_display()

observer.schedule(TaskRegistryHandler(), path=".", recursive=False)
observer.start()
```

### GitHub Sync

```python
import subprocess

def sync_task_to_github(task):
    """Create or update GitHub issue for task"""
    if not task["github_issue"]:
        # Create new issue
        result = subprocess.run([
            "gh", "issue", "create",
            "--title", f"[Task] {task['title']}",
            "--body", task["description"],
            "--label", "task", task["objective"]
        ], capture_output=True, text=True)
        task["github_issue"] = parse_issue_url(result.stdout)
    else:
        # Update existing issue
        subprocess.run([
            "gh", "issue", "edit", str(task["github_issue"]),
            "--state", "open" if task["state"] in ["BACKLOG", "ASSIGNED", "ACTIVE"] else "closed"
        ])

def close_github_issue(task):
    """Close GitHub issue when task is done"""
    if task["github_issue"]:
        subprocess.run(["gh", "issue", "close", str(task["github_issue"])])
```

## State Machine Logic

### Dependency Validation

```python
def can_assign(task):
    """Check if task can be assigned"""
    for dep_id in task["dependencies"]:
        dep_task = registry["tasks"][dep_id]
        if dep_task["state"] != "DONE":
            return False, f"Blocked by {dep_id}"
    return True, None

def can_complete(task):
    """Check if task can be completed"""
    # Check for incomplete subtasks
    for other_id, other_task in registry["tasks"].items():
        if task["id"] in other_task.get("dependencies", []):
            if other_task["state"] != "DONE":
                return False, f"Subtask {other_id} not complete"
    return True, None
```

### State Propagation

```python
def propagate_state_upwards(task):
    """Update parent state based on children"""
    # Find all tasks that depend on this one
    children = [t for t in registry["tasks"].values() 
                if task["id"] in t.get("dependencies", [])]
    
    for child in children:
        # If all dependencies are DONE, child becomes assignable
        if all(d["state"] == "DONE" for d in get_dependencies(child)):
            if child["state"] == "BACKLOG":
                child["state"] = "ASSIGNED"
                notify_assignable(child)
```

## Implementation Phases

### Phase 1: Core Registry (Week 1)
- [ ] JSON schema definition
- [ ] TaskRegistry class (load, save, get, list, create, update)
- [ ] Basic tests

### Phase 2: State Machine (Week 1)
- [ ] StateMachine class (transition, validate)
- [ ] Dependency validation
- [ ] State propagation logic

### Phase 3: Workspace Factory (Week 2)
- [ ] WorkspaceFactory class
- [ ] Directory structure creation
- [ ] Timeline tracking

### Phase 4: CLI Interface (Week 2)
- [ ] CLI framework setup
- [ ] Query commands
- [ ] Execution commands

### Phase 5: Integrations (Week 3)
- [ ] Vibe Kanban file watching
- [ ] GitHub sync (create, update, close)
- [ ] Epic import command

### Phase 6: Testing & Polish (Week 3)
- [ ] End-to-end tests
- [ ] Documentation
- [ ] Performance optimization

## Files

```
2-engine/07-operations/runtime/
├── data/
│   └── task_registry.json          # Single source of truth
├── task_registry/
│   ├── __init__.py
│   ├── registry.py                 # TaskRegistry class
│   ├── state_machine.py            # StateMachine class
│   ├── workspace.py                # WorkspaceFactory class
│   ├── cli.py                      # CLI commands
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py                 # Task dataclass
│   └── integrations/
│       ├── __init__.py
│       ├── vibe_kanban.py          # Vibe Kanban sync
│       └── github_sync.py          # GitHub issue sync
└── tests/
    └── task_registry/
        ├── test_registry.py
        ├── test_state_machine.py
        └── test_workspace.py
```

## Usage Examples

### Agent Workflow

```bash
# Agent finds available work
$ task what-can-i-do
TASK-2026-01-18-002: Create Supabase migrations
  Dependencies: TASK-2026-01-18-001 (DONE)
  Priority: high

# Agent claims task
$ task take TASK-2026-01-18-002
Assigned TASK-2026-01-18-002 to claude-agent-1

# Agent navigates to workspace
$ task workspace TASK-2026-01-18-002
$ cd ../workspaces/TASK-2026-01-18-002/

# Agent starts work
$ task start TASK-2026-01-18-002
Started TASK-2026-01-18-002

# ... Agent does work ...

# Agent completes task
$ task complete TASK-2026-01-18-002
Completed TASK-2026-01-18-002
Closed GitHub issue #202
```

### Vibe Kanban Display

```
┌─────────────────────────────────────────┐
│           ACTIVE TASKS                  │
├─────────────────────────────────────────┤
│ TASK-003: Set up Clerk auth             │
│  Assigned to: arthur                     │
│  Started: 10 min ago                     │
├─────────────────────────────────────────┤
│ TASK-007: Create profile API            │
│  Assigned to: claude-agent-2            │
│  Started: 45 min ago                     │
└─────────────────────────────────────────┘
```
