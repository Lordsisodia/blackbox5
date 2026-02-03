# .autonomous Folder

**Location:** `5-project-memory/blackbox5/.autonomous/`
**Purpose:** Agent data, tasks, runs, and communications for BlackBox5
**Restructured:** 2026-02-02

---

## Structure

```
.autonomous/
├── agents/                    # Agent-specific data
│   ├── architect/             # Architect agent
│   │   ├── state/             # Current state
│   │   ├── metrics/           # Performance metrics
│   │   └── runs/              # Run history
│   ├── executor/              # Executor agent
│   │   ├── state/
│   │   ├── metrics/
│   │   └── runs/
│   ├── planner/               # Planner agent
│   │   ├── state/
│   │   ├── metrics/
│   │   └── runs/              # Includes runs from root runs/planner/
│   └── communications/        # Agent coordination
│       ├── agent-state.yaml
│       ├── chat-log.yaml
│       ├── events.yaml
│       ├── heartbeat.yaml
│       ├── protocol.yaml
│       └── queue.yaml
│
├── context/                   # System context
│   └── routes.yaml
│
├── data/                      # Data storage
│   ├── metrics/
│   └── reports/
│
├── goals/                     # Goal tracking
│   ├── completed/
│   └── templates/
│
├── logs/                      # Consolidated logs
│   ├── ralf/                  # RALF session logs
│   └── archive/               # Archived logs
│
├── memory/                    # Insights and decisions
│   ├── decisions/
│   │   └── registry.md        # Decision registry
│   └── patterns/              # Discovered patterns
│
├── operations/                # Operations data
│   └── .docs/
│
├── reviews/                   # Code reviews
│
└── tasks/                     # All tasks
    ├── active/                # Currently active tasks
    ├── completed/             # Completed tasks
    └── improvements/          # Improvement suggestions

```

---

## What Changed (2026-02-02)

### Deleted (Empty Folders)
- `validations/` - Empty
- `workspaces/` - Empty
- `approvals/` - Empty
- `feedback/` - Empty
- `timeline/` - Empty (redundant with root timeline.yaml)
- `planner-tracking/` - Consolidated into agents/planner/
- `LOGS/` - Consolidated into logs/
- `runs/` - Consolidated into agents/{planner,executor,architect}/runs/

### Moved
- `communications/` → `agents/communications/`
- `planner-tracking/` → `agents/planner/`
- `LOGS/` → `logs/ralf/`
- `decision_registry.md` → `memory/decisions/registry.md`
- `routes.yaml` → `context/routes.yaml`
- Root `runs/planner/` → `agents/planner/runs/`
- Root `runs/executor/` → `agents/executor/runs/`
- Root `runs/archived/` → `agents/architect/runs/archived/`
- Root `runs/completed/` → `agents/architect/runs/completed/`

---

## Usage

### For Agents
- Planner: Use `agents/planner/` for state, metrics, and runs
- Executor: Use `agents/executor/` for state, metrics, and runs
- Architect: Use `agents/architect/` for state, metrics, and runs
- Communications: Use `agents/communications/` for coordination

### For Tasks
- Active tasks: `tasks/active/`
- Completed tasks: `tasks/completed/`
- Improvements: `tasks/improvements/`

---

## Migration Notes

This structure organizes by agent type rather than by function. Each agent has:
1. **State** - Current operational state
2. **Metrics** - Performance data
3. **Runs** - Historical run data

This makes it easier to:
- Add new agents (just create a new folder)
- Understand which agent owns what data
- Scale without creating new top-level folders
