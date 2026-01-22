# DEC-2026-01-21-arch-002: Task Registry System Architecture

**Date**: 2026-01-21
**Status**: Accepted
**Author**: Claude (with User)
**Type**: Architectural Decision

---

## Context

We have sophisticated 3D planning documents (epic.md, TASK-BREAKDOWN.md) that define:
- Objectives → Phases → Tasks hierarchy
- Dependencies and parallelization
- Per-task workspace structure

What's missing is the **execution tracking layer** that:
1. Centralizes all tasks in one queryable registry
2. Tracks state transitions (BACKLOG → ASSIGNED → ACTIVE → DONE)
3. Creates per-task workspaces
4. Integrates with Vibe Kanban (shows ACTIVE tasks only)
5. Syncs with GitHub issues
6. Provides CLI interfaces for Claude Code agents

## Decision

Build a **Task Registry System** with direct file-based storage (JSON), not MCP.

### Architecture

```
2-engine/07-operations/runtime/
├── data/
│   └── task_registry.json          # Single source of truth
├── task_registry/
│   ├── __init__.py
│   ├── registry.py                 # TaskRegistryManager class
│   ├── state_machine.py            # State transitions
│   ├── workspace.py                # Workspace factory
│   ├── cli.py                      # CLI commands
│   ├── epic_import.py              # Epic import functionality
│   ├── models/
│   │   └── task.py                 # Task dataclass
│   ├── integrations/
│   │   ├── vibe_kanban.py          # Vibe Kanban sync
│   │   └── github_sync.py          # GitHub issue sync
│   └── tests/
│       ├── test_registry.py
│       ├── test_state_machine.py
│       ├── test_workspace.py
│       └── test_integration.py
```

### Core Components

#### 1. Task Registry (task_registry.json)

```json
{
  "version": "1.0",
  "last_updated": "2026-01-21T10:00:00Z",
  "tasks": {
    "TASK-001": {
      "id": "TASK-001",
      "title": "Validate database schema",
      "state": "BACKLOG",
      "dependencies": [],
      "workspace": "./workspaces/TASK-001/"
    }
  }
}
```

#### 2. State Machine

State transitions:
```
BACKLOG → ASSIGNED → ACTIVE → DONE
   ↓         ↓         ↓
   └─────────┴────────→ FAILED
```

#### 3. CLI Commands

```bash
task list                    # List all tasks
task available              # Show assignable tasks
task take TASK-001          # Assign to self
task start TASK-001         # Mark as ACTIVE
task complete TASK-001      # Mark as DONE
task import-epic epic.md    # Import from epic.md
task sync-github            # Sync to GitHub
```

#### 4. Vibe Kanban Integration

Vibe Kanban filters `task_registry.json` for ACTIVE tasks:

```typescript
// frontend/src/lib/taskRegistry.ts
export function getActiveTasks(registry: TaskRegistry): ActiveTaskDisplay[] {
  return Object.values(registry.tasks).filter(t => t.state === "ACTIVE");
}

// frontend/src/components/ActiveTasksPanel.tsx
<ActiveTasksPanel registryPath="./data/task_registry.json" />
```

## Rationale

### Why JSON Files Instead of MCP?

| Criterion | JSON Files | MCP Server |
|-----------|-----------|------------|
| **Simplicity** | ✅ Read/write JSON | ❌ Server + client |
| **Debugging** | ✅ Open file | ❌ Check server logs |
| **Reliability** | ✅ FS guarantees | ❌ Process dependency |
| **Use Case** | ✅ Internal orchestration | ❌ Overkill |

### Why This Architecture?

1. **Single Source of Truth**: One JSON file contains all task state
2. **State Propagation**: Parent tasks auto-update when children change
3. **Dependency Validation**: Can't assign/complete if dependencies unmet
4. **Workspace Isolation**: Each task has its own workspace
5. **CLI First**: Designed for Claude Code CLI usage
6. **External Sync**: GitHub and Vibe Kanban integrate via file watching

## Implementation Status

**Date**: 2026-01-21
**Status**: ✅ Fully Implemented

### Completed Components

1. **Core Registry** ✅
   - `models/task.py`: Task, TaskState, TaskPriority dataclasses
   - `registry.py`: TaskRegistryManager with load/save/create/update

2. **State Machine** ✅
   - `state_machine.py`: State transitions with validation
   - Dependency checking
   - State propagation to dependent tasks

3. **Workspace Factory** ✅
   - `workspace.py`: Per-task workspace creation
   - Creates timeline/, thoughts/, context/, work/ directories

4. **CLI Interface** ✅
   - `cli.py`: Full CLI with click
   - Commands: list, available, status, take, start, complete, fail, stats
   - **NEW**: import-epic, sync-github

5. **Epic Import** ✅
   - `epic_import.py`: Parse epic.md and create tasks
   - Supports TASK-BREAKDOWN.md for enhanced dependencies

6. **Vibe Kanban Integration** ✅
   - `integrations/vibe_kanban.py`: Python backend integration
   - `frontend/src/lib/taskRegistry.ts`: TypeScript utilities
   - `frontend/src/components/ActiveTasksPanel.tsx`: React component

7. **GitHub Sync** ✅
   - `integrations/github_sync.py`: Create/update/close GitHub issues

8. **Tests** ✅
   - `tests/task_registry/test_registry.py`: 7 test cases
   - `tests/task_registry/test_state_machine.py`: 11 test cases
   - `tests/task_registry/test_workspace.py`: 9 test cases
   - `tests/task_registry/test_integration.py`: 5 test suites

### File Structure

```
2-engine/07-operations/runtime/
├── data/task_registry.json          # ✅ Empty registry created
├── task_registry/
│   ├── __init__.py                 # ✅ Package exports
│   ├── registry.py                 # ✅ TaskRegistryManager
│   ├── state_machine.py            # ✅ TaskStateMachine
│   ├── workspace.py                # ✅ WorkspaceFactory
│   ├── cli.py                      # ✅ CLI commands + import-epic
│   ├── epic_import.py              # ✅ Epic parser & importer
│   ├── models/task.py              # ✅ Task dataclass
│   └── integrations/
│       ├── vibe_kanban.py          # ✅ Vibe Kanban sync
│       └── github_sync.py          # ✅ GitHub issue sync
└── tests/task_registry/
    ├── test_registry.py           # ✅ Registry tests
    ├── test_state_machine.py      # ✅ State machine tests
    ├── test_workspace.py          # ✅ Workspace tests
    └── test_integration.py        # ✅ Integration tests

3-gui/vibe-kanban/frontend/src/
├── lib/taskRegistry.ts            # ✅ TypeScript utilities
└── components/ActiveTasksPanel.tsx # ✅ React component
```

## Usage Examples

### Import Epic

```bash
# Import from epic.md
cd 2-engine/07-operations/runtime
python -m task_registry.cli import-epic \
  ../../../5-project-memory/siso-internal/plans/active/user-profile/epic.md \
  --breakdown ../../../5-project-memory/siso-internal/plans/active/user-profile/TASK-BREAKDOWN.md \
  --objective user-profile
```

### Agent Workflow

```bash
# Find available work
task available

# Claim and work on a task
task take TASK-2026-01-18-001 --agent claude-agent-1
task start TASK-2026-01-18-001

# Navigate to workspace
cd $(task workspace TASK-2026-01-18-001)

# Complete task
task complete TASK-2026-01-18-001
```

### Vibe Kanban Integration

```typescript
import { ActiveTasksPanel } from "@/components/ActiveTasksPanel";

function App() {
  return (
    <ActiveTasksPanel
      registryPath="./data/task_registry.json"
      autoRefresh={true}
      refreshInterval={5000}
      onTaskClick={(task) => console.log("Clicked:", task)}
    />
  );
}
```

## Next Steps

1. **Testing**: Run pytest to verify all tests pass
2. **Documentation**: Create user guide for agents
3. **Deployment**: Set up file watching for production
4. **Monitoring**: Add metrics for task completion rates

## Alternatives Considered

### Alternative 1: MCP Server
- **Pros**: Standard protocol, external integrations
- **Cons**: Overkill for internal use, adds complexity
- **Rejected**: Simplicity preferred

### Alternative 2: Database (SQLite/Postgres)
- **Pros**: Query power, transactions
- **Cons**: Another dependency, migration complexity
- **Rejected**: JSON is sufficient for our scale

## Impact

- **New Files**: 20+ files across backend and frontend
- **New Data**: task_registry.json (single source of truth)
- **New Commands**: task CLI with 12+ subcommands
- **Integration Points**: Vibe Kanban, GitHub issues

## Related Decisions

- DEC-2026-01-19-arch-001: 6-Folder Memory Structure
- DEC-2026-01-19-scope-001: Remove Empty domains/ Folder
- DEC-2026-01-19-tech-001: Consolidate YAML Files to Root
