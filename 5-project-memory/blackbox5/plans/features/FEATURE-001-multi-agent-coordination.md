# FEATURE-001: Multi-Agent Coordination System

**Status:** active
**Priority:** HIGH (Score: 3.0)
**Type:** feature
**Estimated:** 180 minutes (~3 hours)
**Created:** 2026-02-01
**Feature ID:** F-001

---

## User Value

**Who benefits:** RALF agents (planner, executor, analyst) and BlackBox5 operators

**What problem does it solve:**
Currently, RALF agents operate in isolation. Each agent claims and executes tasks independently without awareness of other running agents. This prevents parallel task execution and collaboration on complex, multi-step work. When a large task could be split among multiple agents, the system cannot distribute work, limiting throughput to serial execution.

**What value does it create:**
- **Immediate:** Enables 2-3 agents to work in parallel on different sub-tasks
- **Short-term:** 2-3x throughput improvement for complex, multi-stage work
- **Long-term:** Scalable to N agents, enabling massive parallelization of large tasks
- **Strategic:** Foundation for advanced multi-agent patterns (specialization, consensus, voting)

**Example Use Case:**
A task like "Implement complete authentication system" can be split:
- Agent 1: Backend API design and implementation
- Agent 2: Database schema and migrations
- Agent 3: Frontend login form and UI

Without coordination: 9 hours serial execution
With coordination: 3 hours parallel execution (3x throughput)

---

## Feature Scope

**MVP (Minimum Viable Product):**
- [ ] Agent discovery mechanism (find other running agents via heartbeat.yaml)
- [ ] Task distribution protocol (split tasks into sub-tasks, assign to agents)
- [ ] State synchronization (shared state file for agent status updates)
- [ ] Conflict resolution (file locking for concurrent writes)
- [ ] Basic integration with RALF-Executor and RALF-Planner
- [ ] Documentation (multi-agent guide)

**Future Enhancements (out of scope for this feature):**
- [ ] Agent specialization (agents declare capabilities, tasks routed by skill)
- [ ] Consensus protocols (multi-agent voting for decisions)
- [ ] Dynamic agent spawning (create/destroy agents on-demand)
- [ ] Task dependency graphs (complex workflows with dependencies)
- [ ] Result aggregation (combine results from multiple sub-tasks)

**Scope Boundaries:**
- **IN SCOPE:**
  - Basic discovery (find agents in heartbeat.yaml)
  - Simple task distribution (1 task → 2-3 sub-tasks)
  - Shared state file for coordination
  - File locking to prevent corruption
  - Integration points for planner/executor

- **OUT OF SCOPE:**
  - Complex task decomposition algorithms
  - Agent specialization or skill matching
  - Task dependencies or DAGs
  - Real-time messaging (we use polling-based state sync)
  - Load balancing or optimization

---

## Context & Background

**Why this feature matters:**
- **Strategic milestone:** First feature delivery under new framework (validates feature delivery system)
- **Throughput bottleneck:** Current single-agent execution limits system velocity
- **Scalability foundation:** Required for future multi-agent patterns
- **Shift completion:** Completes transition from "improvement era" to "feature delivery era"

**Related Features:**
- **Preceding:** TASK-1769916004 (Feature Framework) - created this feature system
- **Preceding:** TASK-1769916006 (Feature Backlog) - populated feature pipeline
- **Following:** F-002 (Advanced Skills) - benefits from agent specialization
- **Following:** F-008 (Agent Analytics) - can track multi-agent performance

**Current State:**
- RALF agents run independently (planner, executor loops)
- Each agent updates heartbeat.yaml with status
- No agent-to-agent communication or coordination
- Tasks executed serially, one at a time

**Desired State:**
- RALF agents discover each other via heartbeat.yaml
- Planner can split large tasks into sub-tasks
- Executor can collaborate on sub-tasks in parallel
- Shared state file tracks agent progress
- 2-3x throughput improvement for parallelizable work

---

## Success Criteria

### Must-Have (Required for completion)
- [ ] Agent discovery working: `discover_agents()` returns list of active agents
- [ ] Task distribution working: `distribute_task()` splits task into sub-tasks
- [ ] State sync working: `sync_agent_state()` updates shared state without corruption
- [ ] Conflict resolution working: 2 agents can update state simultaneously (one waits)
- [ ] Integration complete: Planner/Executor can call coordination functions
- [ ] Documentation complete: `operations/.docs/multi-agent-guide.md` exists
- [ ] Feature framework validated: Feature spec template works end-to-end

### Should-Have (Important but not blocking)
- [ ] Task decomposition heuristic (when should tasks be split?)
- [ ] Sub-task status tracking (track which sub-tasks are done)
- [ ] Error handling (what if agent fails mid-task?)

### Nice-to-Have (If time permits)
- [ ] Load balancing (assign sub-tasks to least busy agent)
- [ ] Task result aggregation (combine outputs from sub-tasks)
- [ ] Multi-agent logging (which agent did what)

### Verification Method
- [ ] Manual testing: Start 2 agents, verify both discovered
- [ ] Integration testing: Split test task, verify sub-tasks created
- [ ] Concurrency testing: 2 agents update state, verify no corruption
- [ ] Documentation review: Guide covers architecture, usage, troubleshooting

---

## Technical Approach

### Implementation Plan

**Phase 1: Feature Specification (20 min)**
- [ ] Read backlog entry for F-001
- [ ] Create feature specification document (this file)
- [ ] Document architecture decisions

**Phase 2: Architecture Design (30 min)**
- [ ] Analyze existing agent system (heartbeat.yaml, events.yaml)
- [ ] Design agent discovery mechanism
- [ ] Design task distribution protocol
- [ ] Design state synchronization approach
- [ ] Document architecture decisions

**Phase 3: Component Implementation (90 min)**
- [ ] Implement agent_discovery.py (discover_agents function)
- [ ] Implement task_distribution.py (distribute_task function)
- [ ] Implement state_sync.py (sync_agent_state function)
- [ ] Implement conflict resolution (file locking)
- [ ] Write unit tests for each component

**Phase 4: Integration (20 min)**
- [ ] Integrate with RALF-Planner prompt
- [ ] Integrate with RALF-Executor prompt
- [ ] Test end-to-end with 2 agents
- [ ] Verify parallel task execution works

**Phase 5: Documentation (20 min)**
- [ ] Create multi-agent guide (operations/.docs/multi-agent-guide.md)
- [ ] Document usage examples
- [ ] Document troubleshooting steps
- [ ] Update feature backlog (mark F-001 as completed)

### Architecture & Design

**Key Components:**

1. **Agent Discovery Service** (`agent_discovery.py`)
   - Reads heartbeat.yaml to find active agents
   - Filters by last_seen timestamp (< 120 seconds)
   - Returns list of agent IDs and metadata
   - Function: `discover_agents() -> List[AgentInfo]`

2. **Task Distribution Service** (`task_distribution.py`)
   - Analyzes task to determine if it can be parallelized
   - Splits task into sub-tasks
   - Assigns sub-tasks to available agents
   - Function: `distribute_task(task, agents) -> List[SubTask]`

3. **State Synchronization Service** (`state_sync.py`)
   - Manages shared state file (.autonomous/communications/agent-state.yaml)
   - Provides atomic read/write operations
   - Implements file locking for concurrency
   - Function: `sync_agent_state(agent_id, state) -> bool`

4. **Conflict Resolution** (built into state_sync.py)
   - Uses fcntl.flock() for file locking
   - Implements retry logic with exponential backoff
   - Ensures no data corruption on concurrent writes

**Data Structures:**

```python
# Agent Info (from heartbeat.yaml)
AgentInfo:
  agent_id: str  # "planner", "executor", etc.
  last_seen: str  # ISO timestamp
  status: str  # "running", "idle", etc.
  current_action: str  # what agent is doing

# Sub-Task (created by distribution)
SubTask:
  parent_task_id: str
  sub_task_id: str
  assigned_agent: str
  status: str  # "pending", "in_progress", "completed"
  description: str

# Agent State (shared state file)
AgentState:
  agent_id: str
  current_task: Optional[str]
  sub_tasks: List[str]
  status: str
  last_update: str  # ISO timestamp
```

**Architecture Decision: File-Based Coordination**

**Chosen Approach:** File-based coordination using YAML files with file locking

**Alternatives Considered:**
- Option A: Message queue (Redis, RabbitMQ) - Too complex for MVP
- Option B: Database (PostgreSQL, SQLite) - Adds dependency
- Option C: Real-time WebSocket - Over-engineering for current use case

**Rationale:**
- **Simplicity:** YAML files are already used (heartbeat.yaml, events.yaml)
- **Reliability:** File locking is well-understood and reliable
- **No dependencies:** Works with existing infrastructure
- **Scalable enough:** For 2-10 agents, file-based is sufficient
- **Future path:** Can migrate to message queue if needed

**Concurrency Control:**

```python
# File locking pattern
def safe_write(filepath, data):
    with open(filepath, 'w') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock
        f.write(data)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)  # Release
```

**Integration Points:**

1. **RALF-Planner Integration:**
   - Before creating task, call `discover_agents()`
   - If 2+ agents available and task is parallelizable, call `distribute_task()`
   - Create sub-tasks in active/ directory

2. **RALF-Executor Integration:**
   - On task completion, call `sync_agent_state(agent_id, state)`
   - Update shared state with progress
   - Check if all sub-tasks complete (for task aggregation)

**File Structure:**

```
2-engine/.autonomous/lib/
├── agent_discovery.py      # Agent discovery service
├── task_distribution.py    # Task distribution service
└── state_sync.py          # State synchronization service

.autonomous/communications/
├── heartbeat.yaml          # Existing (agent registration)
├── agent-state.yaml       # New (shared agent state)
└── chat-log.yaml          # Existing (agent communication)

operations/.docs/
└── multi-agent-guide.md   # New (usage documentation)
```

### Rollout Plan

**Stage 1: Infrastructure (current task)**
- Implement core components (discovery, distribution, sync)
- Test with manual agent simulation
- Document architecture and usage

**Stage 2: Integration (next task or iteration)**
- Integrate with RALF-Planner prompt
- Integrate with RALF-Executor prompt
- Test with 2 actual agents running

**Stage 3: Validation (follow-up)**
- Run parallel task execution test
- Measure throughput improvement
- Validate 2-3x performance claim

**Stage 4: Iteration (future enhancements)**
- Add agent specialization
- Implement task dependencies
- Optimize task splitting algorithms

### Risk Assessment

**Risk 1: Coordination Overhead > Benefit**
- **Likelihood:** Medium
- **Impact:** High (wasted effort)
- **Mitigation:**
  - Start with simple tasks (clear separation)
  - Measure throughput before/after
  - Only use parallel execution for tasks > 30 minutes
  - Add heuristic: "Split if task complexity > threshold"

**Risk 2: Race Conditions, Data Corruption**
- **Likelihood:** Medium
- **Impact:** High (system instability)
- **Mitigation:**
  - Implement file locking (fcntl.flock)
  - Test concurrent writes with 2+ agents
  - Add retry logic with exponential backoff
  - Validate file integrity after writes

**Risk 3: Task Splitting Quality**
- **Likelihood:** High
- **Impact:** Medium (sub-optimal parallelization)
- **Mitigation:**
  - Start with manual task splitting (human-in-the-loop)
  - Use simple heuristics (by feature, by layer, by component)
  - Iteratively improve splitting algorithm
  - Add feedback: "Was this split effective?"

**Risk 4: Feature Framework Validation**
- **Likelihood:** Low
- **Impact:** High (first feature, sets precedent)
- **Mitigation:**
  - Follow template strictly
  - Document all decisions
  - Validate each phase before proceeding
  - Get feedback from Planner/Analyst

### Dependencies

**Technical Dependencies:**
- None (standalone feature)

**Task Dependencies:**
- ✅ TASK-1769916004 (Feature Framework) - COMPLETED (provides template)
- ✅ TASK-1769916006 (Feature Backlog) - COMPLETED (provides F-001 definition)

**Blocking:**
- None (this task unblocks future multi-agent features)

### Testing Strategy

**Unit Tests:**
```bash
# Test agent discovery
python3 -c "
from agent_discovery import discover_agents
agents = discover_agents()
assert len(agents) >= 1, 'Should find at least one agent'
print(f'✅ Found {len(agents)} agents')
"

# Test task distribution
python3 -c "
from task_distribution import distribute_task
subtasks = distribute_task(test_task, agents)
assert len(subtasks) >= 2, 'Should create at least 2 sub-tasks'
print(f'✅ Created {len(subtasks)} sub-tasks')
"

# Test state sync (concurrent)
# Terminal 1:
python3 -c "sync_agent_state('agent1', {'status': 'working'})"

# Terminal 2:
python3 -c "sync_agent_state('agent2', {'status': 'working'})"

# Verify no corruption, both updates present
```

**Integration Test:**
1. Start 2 RALF-Executor instances
2. Create task that can be split
3. Verify both executors claim sub-tasks
4. Verify both complete successfully
5. Verify throughput improvement (measure time)

**Concurrency Test:**
1. Start 2 agents
2. Both update shared state simultaneously
3. Verify no file corruption
4. Verify both updates persisted

### Success Metrics

**Quantitative:**
- Agent discovery finds 2+ agents: ✅ Yes/No
- Task distribution creates 2+ sub-tasks: ✅ Yes/No
- State sync handles concurrent writes: ✅ Yes/No
- Feature spec document created: ✅ Yes/No
- Documentation complete: ✅ Yes/No

**Qualitative:**
- Feature framework validated: Can we create F-002 using same process?
- Architecture sound: Can we extend to agent specialization later?
- Integration smooth: Can planner/executor use coordination functions?

**Throughput Measurement:**
- Baseline (single agent): Measure time for 3 sequential tasks
- Parallel (2 agents): Measure time for 3 parallel tasks
- Target: 2-3x improvement

---

## Open Questions

**Q1: When should tasks be split?**
- **Answer:** Use heuristic based on task complexity score:
  - Low complexity (< 5 steps): Don't split (overhead > benefit)
  - Medium complexity (5-10 steps): Split into 2 sub-tasks
  - High complexity (> 10 steps): Split into 3+ sub-tasks

**Q2: How do we handle task dependencies?**
- **Answer:** MVP doesn't support dependencies. Sub-tasks are independent. Future enhancement.

**Q3: What if an agent fails mid-task?**
- **Answer:** MVP: Manual intervention (mark sub-task as failed, reassign). Future: automatic retry with another agent.

**Q4: How do we aggregate results from sub-tasks?**
- **Answer:** MVP: Manual aggregation (task creator reviews sub-task outputs). Future: automatic aggregation based on task type.

---

## References

**Related Documentation:**
- RALF-Planner: `2-engine/.autonomous/prompts/ralf-planner.md` (if exists)
- RALF-Executor: `2-engine/.autonomous/prompts/ralf-executor.md`
- Feature Framework: `TASK-1769916004` (completed task)
- Feature Backlog: `plans/features/BACKLOG.md`

**Architecture Patterns:**
- File-based locking: `man fcntl`
- YAML state management: Existing heartbeat.yaml pattern
- Multi-agent systems: https://en.wikipedia.org/wiki/Multi-agent_system

---

## Changelog

**2026-02-01:** Feature specification created (RALF-Executor Run 53)
- Documented architecture, implementation plan, risks
- Established file-based coordination approach
- Defined success criteria and testing strategy

**Status:** Active (in implementation)

---

**End of Feature Specification**
