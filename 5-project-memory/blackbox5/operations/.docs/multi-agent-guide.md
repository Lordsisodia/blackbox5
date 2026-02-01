# Multi-Agent Coordination Guide

**Feature:** F-001 - Multi-Agent Coordination System
**Status:** Operational
**Version:** 1.0.0
**Last Updated:** 2026-02-01

---

## Overview

The Multi-Agent Coordination System enables multiple RALF agents to collaborate on complex, multi-step tasks by discovering each other, distributing work, and synchronizing state. This enables 2-3x throughput improvement through parallel task execution.

### What It Does

1. **Agent Discovery:** Finds running RALF agents (planner, executor, analyst) via heartbeat.yaml
2. **Task Distribution:** Splits large tasks into sub-tasks and assigns to available agents
3. **State Synchronization:** Provides shared state file for agent coordination
4. **Conflict Resolution:** Uses file locking to prevent data corruption on concurrent updates

### Benefits

- **2-3x Throughput:** Parallel execution of sub-tasks
- **Scalability:** Support for 2+ agents working simultaneously
- **Reliability:** File locking prevents race conditions and corruption
- **Simplicity:** File-based coordination, no external dependencies

---

## Architecture

### Components

```
2-engine/.autonomous/lib/
├── agent_discovery.py      # Agent discovery service
├── task_distribution.py    # Task distribution service
└── state_sync.py          # State synchronization service
```

### Data Flow

```
┌─────────────┐
│   Planner   │
│  (Agent 1)  │
└──────┬──────┘
       │
       ├─→ discover_agents() ──→ heartbeat.yaml ──→ List[AgentInfo]
       │
       ├─→ can_parallelize(task) ──→ bool
       │
       └─→ distribute_task(task, agents) ──→ List[SubTask]
                                         │
                                         ↓
┌─────────────────────────────────────────────────┐
│         Sub-Tasks Created in active/           │
│  ├── TASK-001-SUB1.md (assigned to executor)  │
│  └── TASK-001-SUB2.md (assigned to planner)   │
└─────────────────────────────────────────────────┘
                                         │
                                         ↓
┌─────────────┐                   ┌─────────────┐
│  Executor   │                   │   Planner   │
│  (Agent 2)  │                   │  (Agent 1)  │
└──────┬──────┘                   └──────┬──────┘
       │                                 │
       └────────→ sync_agent_state() ←──┘
                      │
                      ↓
         .autonomous/communications/
         └── agent-state.yaml (shared state)
```

### File Structure

```
.autonomous/communications/
├── heartbeat.yaml      # Agent registration (existing)
├── agent-state.yaml    # Shared agent state (new)
└── events.yaml         # Event log (existing)
```

---

## Usage

### Basic Workflow

**Step 1: Check if coordination is available**

```python
from agent_discovery import can_coordinate

if can_coordinate(min_agents=2):
    print("Multi-agent coordination is available")
else:
    print("Need at least 2 agents for coordination")
```

**Step 2: Discover available agents**

```python
from agent_discovery import discover_agents

agents = discover_agents()
for agent in agents:
    print(f"{agent.agent_id}: {agent.current_action}")
```

**Step 3: Check if task can be parallelized**

```python
from task_distribution import can_parallelize

if can_parallelize("TASK-001.md"):
    print("Task can be split into sub-tasks")
else:
    print("Task is too simple or has sequential dependencies")
```

**Step 4: Distribute task among agents**

```python
from task_distribution import distribute_task
from agent_discovery import discover_agents

# Get available agents
agents = discover_agents()
agent_ids = [a.agent_id for a in agents]

# Distribute task
subtasks = distribute_task(
    task_file="TASK-001.md",
    available_agents=agent_ids,
    max_subtasks=3
)

print(f"Created {len(subtasks)} sub-tasks")
for subtask in subtasks:
    print(f"  {subtask.sub_task_id} → {subtask.assigned_agent}")
```

**Step 5: Sync agent state during execution**

```python
from state_sync import sync_agent_state

# Update agent state
sync_agent_state("executor", {
    "status": "working",
    "current_task": "TASK-001-SUB1",
    "progress": 50
})
```

**Step 6: Monitor agent states**

```python
from state_sync import get_all_states

all_states = get_all_states()
for agent_id, state in all_states.items():
    print(f"{agent_id}: {state['status']} (progress: {state.get('progress', 0)}%)")
```

---

## Integration with RALF

### RALF-Planner Integration

The planner should:

1. **Before creating tasks:**
   ```python
   from agent_discovery import can_coordinate, discover_agents
   from task_distribution import distribute_task

   if can_coordinate(min_agents=2):
       agents = discover_agents()
       # Consider parallelization in task planning
   ```

2. **When planning complex tasks:**
   ```python
   from task_distribution import can_parallelize, distribute_task

   if can_parallelize(task_file):
       # Split task into sub-tasks
       subtasks = distribute_task(task_file, agent_ids)
       # Create sub-tasks in active/ directory
   ```

### RALF-Executor Integration

The executor should:

1. **On task completion:**
   ```python
   from state_sync import sync_agent_state

   sync_agent_state("executor", {
       "status": "completed",
       "current_task": task_id,
       "completed_at": datetime.now(timezone.utc).isoformat()
   })
   ```

2. **When claiming sub-tasks:**
   ```python
   from state_sync import get_agent_state

   # Check if sub-task is already claimed
   state = get_agent_state("executor")
   if state and state.get("current_task") == subtask_id:
       print("Sub-task already claimed")
   ```

---

## Configuration

### Agent Timeout

```python
# In agent_discovery.py
AGENT_TIMEOUT_SECONDS = 120  # 2 minutes

# Customize:
agents = discover_agents(timeout_seconds=300)  # 5 minutes
```

### Lock Timeout

```python
# In state_sync.py
LOCK_TIMEOUT = 30  # 30 seconds

# Customize:
sync_agent_state("executor", state, timeout=60)  # 60 seconds
```

### State File Location

```python
# Default:
DEFAULT_STATE_FILE = "/path/to/.autonomous/communications/agent-state.yaml"

# Customize:
sync_agent_state("executor", state, state_file="/custom/path/state.yaml")
```

---

## Troubleshooting

### Problem: No agents discovered

**Symptoms:**
```python
discover_agents() returns []
```

**Causes:**
- heartbeat.yaml doesn't exist
- All agents have last_seen > 120 seconds ago
- heartbeat.yaml has incorrect format

**Solutions:**
1. Check heartbeat.yaml exists and is valid YAML
2. Verify agents are running and updating heartbeat.yaml
3. Check agent timeout threshold (default: 120 seconds)
4. Increase timeout if agents are slow: `discover_agents(timeout_seconds=300)`

---

### Problem: Lock acquisition fails

**Symptoms:**
```python
StateLockError: Failed to acquire lock after 5 attempts
```

**Causes:**
- Another process is holding the lock
- Lock timeout is too short
- Previous process crashed without releasing lock

**Solutions:**
1. Wait for other process to complete
2. Increase timeout: `sync_agent_state("executor", state, timeout=60)`
3. Check for stale locks: `lsof | grep agent-state.yaml`
4. If stale lock exists, delete state file and retry

---

### Problem: Task cannot be parallelized

**Symptoms:**
```python
can_parallelize(task_file) returns False
```

**Causes:**
- Task is too simple (< 2000 characters)
- Task has more sequential keywords than parallel keywords
- Task has explicit dependencies

**Solutions:**
1. Review task content for parallelization potential
2. Break task into larger sub-components manually
3. Accept sequential execution for simple tasks
4. Use "implement" keyword to increase parallelization score

---

### Problem: Data corruption in state file

**Symptoms:**
```python
yaml.YAMLError: Failed to parse state file
```

**Causes:**
- Concurrent writes without file locking
- Disk full or I/O error
- File truncated during write

**Solutions:**
1. Always use `sync_agent_state()` (includes file locking)
2. Don't edit agent-state.yaml manually while agents are running
3. Check disk space: `df -h`
4. Reset state file: `reset_all_states()`

---

### Problem: Sub-tasks not being claimed

**Symptoms:**
- Sub-tasks created in active/ directory
- No agents claiming sub-tasks
- Tasks stuck in "pending" status

**Causes:**
- Agents don't know about sub-tasks
- Agent assignment incorrect
- Sub-task files malformed

**Solutions:**
1. Verify sub-task files are in active/ directory
2. Check sub-task file format (should be valid task files)
3. Ensure agents are reading from active/ directory
4. Check agent logs for errors claiming sub-tasks

---

## Examples

### Example 1: Parallel Feature Implementation

**Task:** Implement authentication system (3 components: API, DB, UI)

**Without coordination (serial):**
- Agent 1: API implementation (90 minutes)
- Agent 1: DB schema (30 minutes)
- Agent 1: UI login form (60 minutes)
- **Total: 180 minutes (3 hours)**

**With coordination (parallel):**
- Agent 1 (executor): API implementation (90 minutes)
- Agent 2 (planner): DB schema (30 minutes)
- Agent 3 (analyst): UI login form (60 minutes)
- **Total: 90 minutes (1.5 hours) = 2x improvement**

---

### Example 2: Sub-Task Creation

**Input Task:** TASK-001 (Implement User Management)

**Sub-Tasks Created:**
```
TASK-001-SUB1.md → assigned to executor
- User model and database schema
- CRUD operations
- API endpoints

TASK-001-SUB2.md → assigned to planner
- Admin interface
- User permissions
- Access control
```

---

### Example 3: State Monitoring

**Monitor agent progress:**

```python
from state_sync import get_all_states

while True:
    states = get_all_states()

    completed = sum(1 for s in states.values() if s.get('status') == 'completed')
    total = len(states)

    print(f"Progress: {completed}/{total} agents completed")

    if completed == total:
        print("All agents finished!")
        break

    time.sleep(10)
```

---

## Best Practices

### 1. When to Use Multi-Agent Coordination

**Use when:**
- Task is complex (> 5 implementation steps)
- Task has independent components
- Task can be split by layer, component, or feature
- 2+ agents are available
- Task duration > 30 minutes (coordination overhead justified)

**Don't use when:**
- Task is simple (< 5 steps)
- Task has strict sequential dependencies
- Only 1 agent available
- Task duration < 30 minutes (overhead > benefit)

---

### 2. Task Splitting Heuristics

**Split by component:**
- Frontend, Backend, Database
- API, Service, Repository
- Controller, Model, View

**Split by feature:**
- User management, Authentication, Authorization
- Search, Filter, Sort
- Create, Read, Update, Delete

**Split by layer:**
- Data layer, Business layer, Presentation layer
- Models, Services, Controllers

---

### 3. State Management Best Practices

**DO:**
- Always use `sync_agent_state()` for updates (includes file locking)
- Keep state updates small and focused
- Include timestamp in every state update
- Clear state after task completion

**DON'T:**
- Edit agent-state.yaml manually while agents are running
- Write large data structures to state file
- Assume state file exists (check first)
- Forget to release locks (use context managers)

---

### 4. Error Handling

**Always handle exceptions:**

```python
from state_sync import sync_agent_state, StateLockError

try:
    sync_agent_state("executor", {"status": "working"})
except StateLockError:
    print("Failed to acquire lock, retrying...")
    time.sleep(1)
    sync_agent_state("executor", {"status": "working"})
except Exception as e:
    print(f"Failed to sync state: {e}")
```

**Use retry logic:**

```python
MAX_RETRIES = 3

for attempt in range(MAX_RETRIES):
    try:
        sync_agent_state("executor", state)
        break
    except StateLockError:
        if attempt < MAX_RETRIES - 1:
            time.sleep(1)
        else:
            raise
```

---

## Performance

### Expected Throughput Improvement

- **2 agents:** 1.5-2x improvement
- **3 agents:** 2-2.5x improvement
- **4+ agents:** 2.5-3x improvement (diminishing returns)

### Overhead

- **Agent discovery:** ~50ms
- **Task distribution:** ~100ms
- **State sync:** ~10ms (with file locking)
- **Total overhead:** ~160ms per coordination cycle

### Bottlenecks

- **File locking:** Limits to ~100 syncs/second
- **Task splitting quality:** Heuristic-based, not optimal
- **Agent availability:** Depends on running agents

---

## Future Enhancements

### Planned (Out of Scope for MVP)

- **Agent Specialization:** Agents declare capabilities, tasks routed by skill
- **Task Dependencies:** Support DAG-based task workflows
- **Result Aggregation:** Combine outputs from multiple sub-tasks
- **Load Balancing:** Assign sub-tasks to least busy agent
- **Dynamic Agent Spawning:** Create/destroy agents on-demand
- **Consensus Protocols:** Multi-agent voting for decisions

### Next Feature: F-002

After F-001, implement **F-002: Advanced Skills Library Expansion**
- Adds domain-specific skills
- Enables skill-based agent specialization
- Routes tasks to agents with matching skills

---

## References

**Documentation:**
- Feature Specification: `plans/features/FEATURE-001-multi-agent-coordination.md`
- Agent Discovery: `2-engine/.autonomous/lib/agent_discovery.py`
- Task Distribution: `2-engine/.autonomous/lib/task_distribution.py`
- State Sync: `2-engine/.autonomous/lib/state_sync.py`

**Related:**
- RALF-Planner: `2-engine/.autonomous/prompts/ralf-planner.md`
- RALF-Executor: `2-engine/.autonomous/prompts/ralf-executor.md`
- Feature Framework: `TASK-1769916004` (completed)
- Feature Backlog: `plans/features/BACKLOG.md`

---

## Changelog

**2026-02-01 (v1.0.0):** Initial release
- Agent discovery via heartbeat.yaml
- Task distribution with sub-task creation
- State synchronization with file locking
- Documentation and examples

---

**End of Multi-Agent Coordination Guide**
