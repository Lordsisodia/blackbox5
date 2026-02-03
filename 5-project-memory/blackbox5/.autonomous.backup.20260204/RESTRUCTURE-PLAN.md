# .autonomous Restructure Plan

**Date:** 2026-02-02
**Status:** Analysis Complete - Ready for Restructure

---

## Current State Analysis

### What's Actually Being Used

| Folder | Status | Content Count | Notes |
|--------|--------|---------------|-------|
| tasks/ | ACTIVE | 120+ files | 2 active, 118 completed - HEAVILY USED |
| runs/ | ACTIVE | 8 runs | Mix of completed and active runs |
| communications/ | ACTIVE | 9 files | queue.yaml, chat-log.yaml, protocol.yaml, etc. |
| LOGS/ | ACTIVE | 6 files | RALF session logs |
| goals/ | MINIMAL | 0 files | Empty completed/ and templates/ folders |
| planner-tracking/ | MINIMAL | 1 template | loop-metadata-template.yaml |
| reviews/ | MINIMAL | 2 files | review-20260201-loop10.md, review-loop-20.md |
| memory/insights/ | EMPTY | 0 files | Empty folder |
| timeline/ | EMPTY | 0 files | Empty folder |
| workspaces/ | EMPTY | 0 files | Empty folder |
| validations/ | EMPTY | 0 files | Empty folder |
| approvals/ | EMPTY | 0 files | Empty folder |
| feedback/incoming/ | EMPTY | 0 files | Empty folder |
| data/metrics/ | UNKNOWN | ? | Needs check |
| data/reports/ | UNKNOWN | ? | Needs check |
| operations/.docs/ | UNKNOWN | ? | Has skill-tracking-guide.md |

### Root Files in .autonomous/
- `decision_registry.md` - Active decision tracking
- `executor.log` - Executor log
- `planner.log` - Planner log
- `planner-test.log` - Planner test log
- `routes.yaml` - Route definitions

---

## Proposed New Structure

Based on the TARGET_STRUCTURE.md principles but keeping `.autonomous/`:

```
.autonomous/
├── README.md                    # Explain the structure
│
├── tasks/                       # ALL task-related data
│   ├── active/                  # Currently active tasks (2 files)
│   ├── completed/               # Completed tasks (118 files)
│   ├── improvements/            # Improvement suggestions
│   └── TEMPLATE.md              # Task template
│
├── runs/                        # Run/session data
│   ├── planner/                 # Move from runs/planner/
│   ├── executor/                # Move from runs/executor/
│   ├── architect/               # New for architect agent
│   ├── archived/                # Move from runs/archived/
│   ├── current/                 # Currently active runs (was: loose run-* folders)
│   └── completed/               # Completed runs from .autonomous/runs/
│
├── agents/                      # Agent-specific data (NEW)
│   ├── planner/                 # Move from planner-tracking/
│   │   ├── state.yaml           # Current planner state
│   │   ├── loops/               # Loop history
│   │   └── metrics/             # Performance metrics
│   ├── executor/                # Executor state
│   │   ├── state.yaml
│   │   └── metrics/
│   └── communications/          # MOVE from communications/
│       ├── protocol.yaml
│       ├── queue.yaml
│       ├── events.yaml
│       └── chat-log.yaml
│
├── memory/                      # Insights and learnings
│   ├── insights/                # KEEP (currently empty)
│   ├── decisions/               # MOVE decision_registry.md here
│   │   └── registry.md
│   └── patterns/                # Discovered patterns
│
├── logs/                        # Consolidated logging
│   ├── ralf/                    # MOVE from LOGS/
│   ├── planner.log              # MOVE from root
│   ├── executor.log             # MOVE from root
│   └── archive/                 # Old logs
│
├── goals/                       # Goal tracking
│   ├── active.yaml              # Current goals
│   ├── completed/               # KEEP folder
│   └── templates/               # KEEP folder
│
├── reviews/                     # KEEP - Code reviews
│
├── operations/                  # Operations data
│   └── skill-usage.yaml         # MOVE from .autonomous/operations/
│
└── context/                     # System context
    └── routes.yaml              # MOVE from root
```

---

## What to Delete

These folders are empty and can be removed:
1. `validations/` - Empty
2. `workspaces/` - Empty
3. `approvals/` - Empty
4. `feedback/` - Empty (incoming/ is empty)
5. `timeline/` - Empty (redundant with root timeline.yaml)
6. `data/` - Check contents first, likely move or delete

---

## Migration Steps

### Phase 1: Cleanup Empty Folders
```bash
# Delete confirmed empty folders
rmdir .autonomous/validations/
rmdir .autonomous/workspaces/
rmdir .autonomous/approvals/
rmdir .autonomous/feedback/incoming/
rmdir .autonomous/feedback/
rmdir .autonomous/timeline/
```

### Phase 2: Create New Structure
```bash
# Create new folders
mkdir -p .autonomous/agents/planner/loops
mkdir -p .autonomous/agents/planner/metrics
mkdir -p .autonomous/agents/executor/metrics
mkdir -p .autonomous/agents/communications
mkdir -p .autonomous/runs/planner
mkdir -p .autonomous/runs/executor
mkdir -p .autonomous/runs/architect
mkdir -p .autonomous/runs/current
mkdir -p .autonomous/memory/decisions
mkdir -p .autonomous/memory/patterns
mkdir -p .autonomous/logs/ralf
mkdir -p .autonomous/logs/archive
```

### Phase 3: Move Files
```bash
# Move communications
mv .autonomous/communications/* .autonomous/agents/communications/

# Move planner tracking
mv .autonomous/planner-tracking/loops/* .autonomous/agents/planner/loops/
mv .autonomous/planner-tracking/assets/* .autonomous/agents/planner/ 2>/dev/null || true

# Move logs
mv .autonomous/LOGS/* .autonomous/logs/ralf/
mv .autonomous/planner.log .autonomous/logs/
mv .autonomous/executor.log .autonomous/logs/
mv .autonomous/planner-test.log .autonomous/logs/archive/

# Move decision registry
mv .autonomous/decision_registry.md .autonomous/memory/decisions/registry.md

# Move routes
mv .autonomous/routes.yaml .autonomous/context/

# Consolidate runs (from root runs/)
mv runs/planner/* .autonomous/runs/planner/
mv runs/executor/* .autonomous/runs/executor/
mv runs/archived/* .autonomous/runs/archived/
mv runs/completed/* .autonomous/runs/completed/ 2>/dev/null || true

# Move current .autonomous runs
mv .autonomous/runs/run-* .autonomous/runs/current/
```

### Phase 4: Update References
- Update all scripts that reference old paths
- Update documentation
- Update CLAUDE.md if needed

---

## Benefits of New Structure

1. **Clear Separation**: Each agent has its own folder
2. **Consolidated Runs**: All run data in one place, organized by agent type
3. **Centralized Communications**: Single location for agent coordination
4. **Better Logging**: Structured log organization
5. **No Empty Folders**: Only folders that are used exist
6. **Scalable**: Easy to add new agents (analyst/, architect/, etc.)

---

## Questions

1. Should we keep `goals/` or move goals to root level (goals.yaml already exists)?
2. What about `memory/insights/` - should this be populated or removed?
3. Should `operations/` stay or be moved to root level `operations/`?
4. Do we want to keep old planner logs in archive/ or delete them?
