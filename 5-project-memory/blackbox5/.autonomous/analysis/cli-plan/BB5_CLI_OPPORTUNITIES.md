# BB5 CLI vs Hook Audit Report

**Date:** 2026-02-06
**Author:** Systems Architect
**Status:** Analysis Complete

---

## Executive Summary

This audit identifies opportunities to convert manual BB5 operations into CLI commands vs hooks. The analysis covers existing CLIs, hooks, operations, workflows, and the queue system to determine the optimal automation strategy.

**Key Finding:** BB5 has 12 existing CLI commands and 12 planned hooks, but significant gaps exist in queue management, task lifecycle, and operational automation that should be CLI commands rather than manual processes or hooks.

---

## Current State Analysis

### Existing CLI Commands (12)

| Command | Purpose | Type |
|---------|---------|------|
| `bb5-goal` | Goal listing and display | Read |
| `bb5-plan` | Plan listing and display | Read |
| `bb5-task` | Task listing and display | Read |
| `bb5-create` | Create goals/plans/tasks/subtasks | Write |
| `bb5-link` | Link hierarchy items | Write |
| `bb5-goto` | Navigation (up/down/root/goto) | Navigation |
| `bb5-whereami` | Context discovery | Read |
| `bb5-discover-context` | Core context library | Library |
| `bb5-timeline` | Timeline management | Read/Write |
| `bb5-populate-template` | Template engine | Library |
| `bb5-scout-improve` | Self-improvement runner | Execution |
| `bb5-skill-dashboard` | Skill metrics display | Read |

### Planned Hooks (12 Lifecycle Events)

| Hook | Purpose | Status |
|------|---------|--------|
| SessionStart | Initialize session, load context | In Development |
| UserPromptSubmit | Validate/filter prompts | Planned |
| PreToolUse | Security gates, block dangerous commands | Planned |
| PostToolUse | Auto-formatting, logging | Planned |
| PostToolUseFailure | Error handling | Planned |
| Notification | Desktop alerts, TTS, Slack | Planned |
| SubagentStart | Subagent context setup | Planned |
| SubagentStop | Subagent validation | Planned |
| Stop | Session-end cleanup (NON-BLOCKING) | Planned |
| PreCompact | Context preservation | Planned |
| SessionEnd | Cleanup, archiving | Planned |
| PermissionRequest | Auto-allow rules | Planned |

### Operations Binaries (22 Python/Shell Scripts)

Located in `5-project-memory/blackbox5/bin/`:

**Queue & Task Management:**
- `bb5-queue-manager.py` - Task queue management and prioritization
- `bb5-reanalysis-engine.py` - Task reanalysis and priority management
- `bb5-parallel-dispatch.sh` - Parallel task dispatch

**Validation & Quality:**
- `validate-run-documentation.py` - Run folder documentation validation
- `validate-skill-usage.py` - Skill usage validation
- `validate-ssot.py` - STATE.yaml consistency validation

**Metrics & Dashboards:**
- `bb5-health-dashboard.py` - Real-time system health monitoring
- `bb5-metrics-collector.py` - Metrics collection
- `calculate-skill-metrics.py` - Skill metrics calculation
- `collect-skill-metrics.py` - Skill metrics collection
- `generate-skill-metrics-data.py` - Generate skill metrics data
- `generate-skill-report.py` - Generate skill reports
- `log-skill-usage.py` - Log skill usage

**State Management:**
- `sync-state.py` - STATE.yaml synchronization
- `standardize-run-names.py` - Run naming standardization
- `update-dashboard.py` - Dashboard updates
- `atomic_io.py` - Atomic file I/O library
- `skill_registry.py` - Skill registry library

---

## Pain Points Identified

### 1. Task Lifecycle Management (HIGH PRIORITY)

**Current State:** Manual file manipulation

**Problems:**
- Agents manually edit queue.yaml to claim tasks
- Task status updates require precise YAML editing
- Moving tasks (active → completed) is manual
- No unified task claim/release mechanism
- Task blocking/unblocking requires dependency analysis

**Evidence from queue.yaml:**
- 90 tasks tracked with complex dependencies
- 52 tasks are blocked waiting for dependencies
- 17 tasks ready to execute but no claim system
- Manual priority_score calculations

### 2. Queue Operations (HIGH PRIORITY)

**Current State:** Python scripts exist but no CLI wrapper

**Problems:**
- `bb5-queue-manager.py` exists but requires direct Python invocation
- No simple command to view prioritized queue
- No command to find next executable task
- No command to check task dependencies

### 3. Validation & Quality Gates (MEDIUM PRIORITY)

**Current State:** Validation scripts exist but fragmented

**Problems:**
- `validate-run-documentation.py` - not integrated into CLI
- `validate-skill-usage.py` - standalone script
- `validate-ssot.py` - standalone script
- No unified `bb5 validate` command

### 4. State Synchronization (MEDIUM PRIORITY)

**Current State:** Manual STATE.yaml updates

**Problems:**
- `sync-state.py` exists but not exposed as CLI
- Task completion requires updating multiple files
- No atomic state update command
- Risk of SSOT violations

### 5. Task Reanalysis (MEDIUM PRIORITY)

**Current State:** `bb5-reanalysis-engine.py` exists but no CLI

**Problems:**
- Trigger detection requires Python invocation
- No command to check if tasks need reanalysis
- No integration with git hooks (planned but not CLI)

### 6. Skill Operations (LOW PRIORITY)

**Current State:** Multiple skill scripts

**Problems:**
- `log-skill-usage.py` - manual invocation
- `calculate-skill-metrics.py` - manual invocation
- `bb5-skill-dashboard` exists but skill logging is separate

---

## Decision Framework

### CLI vs Hook Classification

| Criteria | CLI | Hook |
|----------|-----|------|
| **Trigger** | Explicit user action | Automatic lifecycle event |
| **Feedback** | Immediate output to user | Silent/background execution |
| **Transaction** | Yes - atomic operations | No - fire-and-forget |
| **User Control** | User decides when to run | Runs automatically |
| **Blocking** | Can prompt for input | Cannot block (except PreCompact) |
| **Use Case** | Task management, queries, updates | Session lifecycle, cross-cutting concerns |

### Rules for Classification

1. **Use CLI when:**
   - User needs to make a decision (claim task, validate, etc.)
   - Operation needs immediate feedback
   - Data modification requires confirmation
   - Operation is transactional
   - User initiates the action

2. **Use Hook when:**
   - Operation should happen automatically
   - No user decision required
   - Cross-cutting concern (logging, notifications)
   - Session lifecycle event
   - Background processing acceptable

---

## Proposed New CLI Commands

### Priority 1: Task Lifecycle (CRITICAL)

#### `bb5 claim [TASK-ID]`
**Purpose:** Claim a task for execution

**Rationale:**
- Currently manual queue.yaml editing
- Requires atomic update of claimed_by, claimed_at, status
- Must validate task is not already claimed
- Must check dependencies are satisfied

**Implementation:**
```bash
bb5 claim TASK-ARCH-001
# Updates queue.yaml: claimed_by, claimed_at, status: in_progress
# Creates .task-claimed file in run folder
# Validates dependencies are complete
```

**Why CLI not Hook:**
- Explicit user decision
- Requires validation feedback (is task available?)
- Transactional - must succeed or fail atomically
- User needs confirmation of claim

---

#### `bb5 complete [TASK-ID] [STATUS]`
**Purpose:** Mark task as complete with status

**Rationale:**
- Currently manual file moves and YAML edits
- Must update queue.yaml, move folder, update STATE.yaml
- Needs validation that task is actually complete

**Implementation:**
```bash
bb5 complete TASK-ARCH-001 --status complete --results "Outcome..."
# Moves tasks/active/TASK-XXX → tasks/completed/TASK-XXX
# Updates queue.yaml: status, completed_at, completion_notes
# Updates STATE.yaml if linked to plan/goal
# Triggers dependency unblocking
```

**Why CLI not Hook:**
- User decides when task is complete
- Requires validation (acceptance criteria check)
- Transactional across multiple files
- Immediate feedback needed

---

#### `bb5 release [TASK-ID]`
**Purpose:** Release a claimed task (unclaim)

**Rationale:**
- No current mechanism to unclaim
- Needed when task cannot be completed
- Must clear claimed_by, reset status

**Implementation:**
```bash
bb5 release TASK-ARCH-001 --reason "Blocked by external dependency"
# Clears claimed_by, claimed_at
# Resets status to pending
# Logs release reason
```

**Why CLI not Hook:**
- Explicit user decision
- Needs confirmation
- Transactional update

---

### Priority 2: Queue Operations (HIGH)

#### `bb5 queue [COMMAND]`
**Purpose:** Unified queue management

**Subcommands:**
```bash
bb5 queue list                    # Show prioritized queue
bb5 queue next                    # Show next executable task
bb5 queue ready                   # List tasks with no dependencies
bb5 queue blocked                 # List blocked tasks and why
bb5 queue stats                   # Queue statistics
bb5 queue prioritize              # Recalculate all priorities
bb5 queue deps TASK-XXX           # Show dependency tree
```

**Rationale:**
- `bb5-queue-manager.py` exists but not CLI-accessible
- Complex queue.yaml structure needs simple interface
- Dependency resolution is complex (topological sort)

**Why CLI not Hook:**
- Information queries need immediate feedback
- Prioritization is explicit operation
- User decides when to reprioritize

---

#### `bb5 next`
**Purpose:** Quick command to get next task

**Implementation:**
```bash
bb5 next
# Output: TASK-ARCH-017 (30 min, score 8.8) - Fix blackbox.py references
# Or: No ready tasks available
```

**Why CLI not Hook:**
- Information query
- User-initiated
- Immediate feedback needed

---

### Priority 3: Validation (MEDIUM)

#### `bb5 validate [SCOPE]`
**Purpose:** Unified validation command

**Subcommands:**
```bash
bb5 validate run                  # Validate current run documentation
bb5 validate task TASK-XXX        # Validate task completeness
bb5 validate ssot                 # Validate STATE.yaml consistency
bb5 validate skills               # Validate skill usage documentation
bb5 validate all                  # Run all validators
```

**Rationale:**
- Multiple validation scripts exist but fragmented
- Stop hook cannot block (discovered limitation)
- PreCompact hook could block but CLI gives user control

**Why CLI not Hook:**
- User should run validation explicitly before completing
- Validation results need immediate display
- User may want to fix issues before continuing
- PreCompact hook can call this CLI for blocking validation

---

### Priority 4: State Management (MEDIUM)

#### `bb5 sync`
**Purpose:** Synchronize STATE.yaml with actual state

**Implementation:**
```bash
bb5 sync [--dry-run]
# Updates STATE.yaml based on actual file system state
# Detects completed tasks, updates progress percentages
# Reports discrepancies
```

**Rationale:**
- `sync-state.py` exists but not CLI-accessible
- SSOT violations are a known issue (TASK-ARCH-003)
- Need simple way to keep STATE.yaml in sync

**Why CLI not Hook:**
- User should control when sync happens
- Dry-run option needed for safety
- Results need review before applying

---

#### `bb5 status`
**Purpose:** Show comprehensive system status

**Implementation:**
```bash
bb5 status
# Shows: Current context, claimed task, queue stats, health
# Integrates with bb5-health-dashboard.py
```

**Why CLI not Hook:**
- Information query
- User-initiated
- Immediate feedback needed

---

### Priority 5: Reanalysis (MEDIUM)

#### `bb5 reanalyze [COMMAND]`
**Purpose:** Task reanalysis operations

**Subcommands:**
```bash
bb5 reanalyze check               # Check for triggers
bb5 reanalyze apply               # Apply auto-actions
bb5 reanalyze status              # Show reanalysis status
bb5 reanalyze triggers            # List active triggers
```

**Rationale:**
- `bb5-reanalysis-engine.py` exists but complex to invoke
- Reanalysis should be explicit operation

**Why CLI not Hook:**
- User should control when reanalysis runs
- Results need review before applying actions
- Git hook can trigger this CLI automatically

---

### Priority 6: Skill Operations (LOW)

#### `bb5 skill log [SKILL-NAME] [OUTCOME]`
**Purpose:** Log skill usage

**Implementation:**
```bash
bb5 skill log bmad-architect success --task TASK-XXX --effectiveness 4
# Updates skill-metrics.yaml
```

**Why CLI not Hook:**
- Explicit action after task completion
- User provides outcome rating
- Could be called by Stop hook for auto-logging

---

## Hook Candidates (What Should Remain as Hooks)

### Confirmed Hook Operations

| Hook | Operation | Why Hook |
|------|-----------|----------|
| **SessionStart** | Load context, set env vars | Automatic initialization |
| **Stop** | RALF Monitor notification, cleanup | Session-end event, async OK |
| **PreCompact** | Validation before context full | Can block, lifecycle event |
| **Notification** | Telegram alerts | Automatic, no user decision |
| **SubagentStart** | Context setup for subagents | Automatic initialization |
| **SubagentStop** | Subagent validation | Automatic cleanup |
| **SessionEnd** | Final cleanup, archiving | Session lifecycle |

### Hook Integration with CLI

Hooks should CALL CLI commands for operations:

```python
# Stop hook example
subprocess.run(['bb5', 'validate', 'run'], capture_output=True)
subprocess.run(['bb5', 'skill', 'log', skill_name, outcome], capture_output=True)
```

---

## Implementation Priority

### Phase 1: Task Lifecycle (Week 1)
1. `bb5 claim` - Critical for task execution
2. `bb5 complete` - Critical for task completion
3. `bb5 release` - Needed for task management

### Phase 2: Queue Operations (Week 2)
4. `bb5 queue` - Essential for queue management
5. `bb5 next` - Quick access to next task

### Phase 3: Validation (Week 3)
6. `bb5 validate` - Quality gates
7. Integrate with PreCompact hook for blocking

### Phase 4: State Management (Week 4)
8. `bb5 sync` - SSOT maintenance
9. `bb5 status` - System overview

### Phase 5: Advanced Features (Week 5-6)
10. `bb5 reanalyze` - Task reanalysis
11. `bb5 skill log` - Skill tracking

---

## Integration Architecture

### CLI → Hook Relationship

```
User Action          CLI Command              Hook Trigger
─────────────────────────────────────────────────────────────
Start Session        ─                        SessionStart hook
                                                    ↓
                                            Load context, env vars
                                                    ↓
Claim Task           bb5 claim TASK-XXX       ─
                     (updates queue.yaml)
                            ↓
Complete Task        bb5 complete TASK-XXX    ─
                     (move folder, update state)
                            ↓
End Session          ─                        Stop hook
                                                    ↓
                                            bb5 validate run (call CLI)
                                            bb5 skill log (call CLI)
                                            Notification
```

### Hook → CLI Call Pattern

Hooks should delegate to CLI for operations:

```python
# In Stop hook
import subprocess

# Validate run documentation
result = subprocess.run(
    ['bb5', 'validate', 'run', '--json'],
    capture_output=True,
    text=True
)

# Log skill usage
subprocess.run([
    'bb5', 'skill', 'log',
    skill_name, outcome,
    '--task', task_id
])
```

---

## File Locations

### New CLI Scripts
- `/Users/shaansisodia/.blackbox5/bin/bb5-claim`
- `/Users/shaansisodia/.blackbox5/bin/bb5-complete`
- `/Users/shaansisodia/.blackbox5/bin/bb5-release`
- `/Users/shaansisodia/.blackbox5/bin/bb5-queue`
- `/Users/shaansisodia/.blackbox5/bin/bb5-next`
- `/Users/shaansisodia/.blackbox5/bin/bb5-validate`
- `/Users/shaansisodia/.blackbox5/bin/bb5-sync`
- `/Users/shaansisodia/.blackbox5/bin/bb5-status`
- `/Users/shaansisodia/.blackbox5/bin/bb5-reanalyze`

### Integration Points
- `bb5` main dispatcher needs new command mappings
- Hook configurations in `~/.claude/settings.json`
- Python libraries in `bin/` for shared logic

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Overlap with existing scripts | Medium | Refactor existing scripts to use new CLI |
| Hook calling CLI adds latency | Low | Hooks run async, latency acceptable |
| Transaction failures | High | Use atomic_io.py for all file operations |
| User confusion (CLI vs Hook) | Medium | Clear documentation, consistent patterns |
| Breaking existing workflows | High | Gradual rollout, maintain backward compatibility |

---

## Success Metrics

1. **Task Claim Time:** Reduce from manual editing to single command
2. **Task Completion Time:** Reduce from multi-file edits to single command
3. **Queue Query Time:** Enable sub-second queue queries
4. **Validation Coverage:** 100% of runs validated before completion
5. **SSOT Violations:** Reduce to zero through `bb5 sync`

---

## Related Tasks

- TASK-ARCH-016: Design Agent Execution Flow (depends on this analysis)
- TASK-PROC-004: Fix Task-to-Completion Pipeline Stall
- TASK-ARCH-003: Fix Single Source of Truth Violations
- TASK-SKIL-001: Fix Zero Skill Invocation Rate

---

## Conclusion

The BB5 system needs 11 new CLI commands to automate manual operations. The key insight is that **task lifecycle operations (claim, complete, release) must be CLI commands** because they require explicit user decisions and transactional updates. Hooks should remain focused on session lifecycle events and can delegate to CLI commands for operations.

**Immediate Action:** Implement `bb5 claim`, `bb5 complete`, and `bb5 queue` as they unblock the critical path for task execution.
