# BB5 Multi-Agent Coordination Hooks Research

**Version:** 1.0.0
**Date:** 2026-02-06
**Author:** Multi-Agent Systems Specialist

---

## Executive Summary

This document analyzes BlackBox5's multi-agent architecture and identifies the hooks required for effective agent coordination, task handoffs, and swarm intelligence. BB5 currently operates with a hybrid architecture combining **Dual-RALF** (Planner + Executor) and a **6-Agent Pipeline** (Scout, Analyzer, Planner workers with validators).

---

## 1. Current Multi-Agent Architecture

### 1.1 Agent Types

| Agent | Role | Primary Function | Writes To | Reads From |
|-------|------|------------------|-----------|------------|
| **RALF-Planner** | Strategist | Analyze codebase, plan tasks, answer questions | queue.yaml, chat-log.yaml | events.yaml, chat-log.yaml |
| **RALF-Executor** | Tactician | Execute tasks, write code, commit changes | events.yaml, chat-log.yaml | queue.yaml, chat-log.yaml |
| **Deep Repo Scout** | Researcher | 3-loop repo analysis | knowledge/REPO-knowledge.md | repo-list.yaml |
| **Scout Validator** | Quality Gate | Approve/reject scout output | scout-queue.yaml | knowledge/ docs |
| **Integration Analyzer** | Assessor | Assess integration value | assessments/integration-assessments.md | approved knowledge docs |
| **Analyzer Validator** | Quality Gate | Verify scoring | analyzer-queue.yaml | assessments/ |
| **Implementation Planner** | Task Creator | Create executable tasks | plans/, tasks/ | validated assessments |
| **Planner Validator** | Quality Gate | Verify plans | planner-queue.yaml | plans/ |

### 1.2 Communication Patterns

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BB5 COMMUNICATION TOPOLOGY                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐      queue.yaml      ┌──────────────┐                     │
│  │   PLANNER    │ ───────────────────► │   EXECUTOR   │                     │
│  │              │ ◄─────────────────── │              │                     │
│  └──────────────┘      events.yaml     └──────────────┘                     │
│         │                                    │                              │
│         │         ┌──────────────┐           │                              │
│         └────────►│  chat-log    │◄──────────┘                              │
│                   │  (bidirect.) │                                          │
│                   └──────────────┘                                          │
│                          │                                                  │
│  ┌──────────────┐        │         ┌──────────────┐                        │
│  │ SCOUT WORKER │───────┘         │SCOUT VALIDATOR│                        │
│  └──────────────┘                 └──────────────┘                        │
│         │                                │                                 │
│         ▼                                ▼                                 │
│  ┌──────────────┐                 ┌──────────────┐                        │
│  │   ANALYZER   │◄───────────────►│ANALYZER VAL. │                        │
│  └──────────────┘                 └──────────────┘                        │
│         │                                │                                 │
│         ▼                                ▼                                 │
│  ┌──────────────┐                 ┌──────────────┐                        │
│  │   PLANNER    │◄───────────────►│PLANNER VAL.  │                        │
│  │   WORKER     │                 └──────────────┘                        │
│  └──────────────┘                                                          │
│         │                                                                  │
│         └────────────────────────────────────────────────────────────►     │
│                                    queue.yaml (for Executor)               │
│                                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Coordination Questions Answered

### 2.1 How Does a Planner Tell an Executor About a Task?

**Mechanism:** `queue.yaml` file-based communication

```yaml
# queue.yaml - Written by Planner, read by Executor
tasks:
  - id: "TASK-ARCH-016"
    type: "architecture"
    status: "pending"  # pending | in_progress | completed
    priority: "CRITICAL"
    priority_score: 15.0
    title: "Design Agent Execution Flow"
    estimated_minutes: 120
    roi:
      impact: 15.0
      effort: 120
      confidence: 1.2
    blockedBy: ["TASK-ARCH-011"]
    blocks: ["TASK-ARCH-039", "TASK-PROC-008"]
    resource_type: "cpu_bound"
    parallel_group: "sequential"
    goal: "IG-007"
```

**Hook Needed:** `on_task_queued`
- Fires when Planner adds task to queue
- Updates events.yaml with `type: task_queued`
- Triggers notification to Executor

### 2.2 How Does an Executor Report Completion?

**Mechanism:** `events.yaml` file-based reporting

```yaml
# events.yaml - Written by Executor, read by Planner
events:
  - timestamp: "2026-02-05T15:21:14+07:00"
    task_id: "TASK-ARCH-016"
    type: completed  # started | in_progress | completed | failed
    agent: executor
    run_id: "run-20260205-152114"
    result: success
    commit_hash: "9a4a85b"
```

**Hook Needed:** `on_task_completed`
- Fires when Executor marks task complete
- Updates queue.yaml status to `completed`
- Moves task from `tasks/active/` to `tasks/completed/`
- Triggers skill usage recording

### 2.3 How Do Agents Discover Context from Previous Agents?

**Mechanism:** Shared filesystem + standardized run folders

```
runs/
├── active/                    # Currently executing
├── completed/                 # Finished runs
│   └── run-20260205-152114/
│       ├── THOUGHTS.md       # Agent reasoning
│       ├── RESULTS.md        # Outcomes
│       ├── DECISIONS.md      # Choices made
│       ├── ASSUMPTIONS.md    # Verified assumptions
│       └── LEARNINGS.md      # Patterns discovered
└── archived/                  # Old runs (90+ days)
```

**Hook Needed:** `on_context_request`
- Agent queries previous agent's run folder
- Loads THOUGHTS.md, DECISIONS.md for context
- Aggregates learnings across related runs

### 2.4 What Prevents Two Agents from Claiming the Same Task?

**Mechanism:** Atomic file writes + status transitions

```python
# From bb5-queue-manager.py
def claim_task(task_id: str, agent_id: str) -> bool:
    """Atomically claim a task."""
    # 1. Read current state
    task = task_map.get(task_id)

    # 2. Check if already claimed
    if task.status != TaskStatus.PENDING:
        return False

    # 3. Atomic update
    task.status = TaskStatus.IN_PROGRESS
    task.claimed_by = agent_id
    task.claimed_at = datetime.now()

    # 4. Write atomically (temp file + rename)
    write_atomic(queue_file, updated_queue)
    return True
```

**Hook Needed:** `on_task_claim`
- Validates task is still pending
- Records claim in events.yaml
- Sets 30-second heartbeat expectation

### 2.5 How Do Subagents Report Back to Parents?

**Mechanism:** Events.yaml with parent_task reference

```yaml
# Subagent reports to parent
- timestamp: "2026-02-05T15:21:14+07:00"
  type: agent_stop
  agent_type: "scout"
  agent_id: "scout-001"
  parent_task: "TASK-ARCH-002"
  source: hook
  data:
    knowledge_doc: "knowledge/ralphex-knowledge.md"
    findings_count: 12
    confidence: 0.85
```

**Hook Needed:** `on_subagent_complete`
- Fires when subagent finishes
- Updates parent task with results
- Triggers validation workflow

### 2.6 What Hooks Fire When Agents Start/Stop?

**Current Implementation:**

| Event | Hook Script | Fires | Action |
|-------|-------------|-------|--------|
| Session Start | `ralf-session-start-hook.sh` | Claude starts | Create run folder, templates |
| Session Stop | `ralf-stop-hook.sh` | Claude stops | Validate, commit, archive |
| Agent Start | (internal) | Agent loop begins | Write agent_start event |
| Agent Stop | (internal) | Agent loop ends | Write agent_stop event |

---

## 3. Required Coordination Hooks

### 3.1 Agent-to-Agent Communication Hooks

#### `on_task_queued`
```yaml
# Fires when: Planner adds task to queue
# Location: queue.yaml
# Action:
trigger:
  file: queue.yaml
  condition: new task added
actions:
  - write_event:
      type: task_queued
      task_id: "{task.id}"
      queued_by: "{agent.id}"
  - notify:
      target: executor
      message: "New task available: {task.title}"
  - update_metrics:
      queue_depth: +1
```

#### `on_task_claimed`
```yaml
# Fires when: Executor claims task
# Location: queue.yaml
# Action:
trigger:
  file: queue.yaml
  condition: status changes to in_progress
actions:
  - validate:
      check: "status was pending"
      on_fail: reject_claim
  - write_event:
      type: task_claimed
      task_id: "{task.id}"
      claimed_by: "{agent.id}"
      claimed_at: "{timestamp}"
  - lock_resources:
      resources: "{task.resources}"
      duration: "{task.estimated_minutes}"
```

#### `on_task_completed`
```yaml
# Fires when: Executor marks task complete
# Location: events.yaml
# Action:
trigger:
  file: events.yaml
  condition: type == completed
actions:
  - update_queue:
      task_id: "{event.task_id}"
      status: completed
      completed_at: "{timestamp}"
  - move_task:
      from: "tasks/active/{task_id}"
      to: "tasks/completed/{task_id}"
  - record_skill_usage:
      task_id: "{task_id}"
      skill: "{task.skill_used}"
      outcome: "{event.result}"
  - unblock_dependents:
      task_id: "{task_id}"
      check_queue: true
```

### 3.2 Task Handoff Hooks

#### `on_handoff_planner_to_executor`
```yaml
# Fires when: Task moves from planning to execution
# Action:
trigger:
  condition: task.status == pending AND task.approach is defined
actions:
  - validate_approach:
      check: approach has acceptance_criteria
      check: files_to_modify exist
  - create_run_folder:
      template: executor-run-template
      populate: task_context
  - write_handoff_doc:
      file: "{run_dir}/HANDOFF.md"
      content:
        planned_by: "{planner.id}"
        planned_at: "{timestamp}"
        approach: "{task.approach}"
        context: "{task.context_level}"
```

#### `on_handoff_worker_to_validator`
```yaml
# Fires when: Worker completes, sends to validator
# Action:
trigger:
  condition: worker writes output file
actions:
  - create_validation_task:
      validator: "{worker.type}-validator"
      input: "{worker.output}"
      criteria: "{worker.validation_criteria}"
  - queue_validation:
      priority: same_as_worker_task
      deadline: "{timestamp + 10m}"
```

#### `on_handoff_validator_to_next_stage`
```yaml
# Fires when: Validator approves/rejects
# Action:
trigger:
  condition: validator updates status
actions:
  - if_approved:
      - move_to_next_stage:
          stage: "{next_stage}"
      - notify_worker:
          message: "Validation passed"
  - if_rejected:
      - return_to_worker:
          feedback: "{validator.feedback}"
      - increment_retry_count:
          max_retries: 3
```

### 3.3 Swarm State Management Hooks

#### `on_swarm_heartbeat`
```yaml
# Fires every: 30 seconds
# Action:
trigger:
  interval: 30s
actions:
  - check_agent_health:
      agent: "{agent.id}"
      last_heartbeat: "{timestamp}"
      timeout: 120s
  - update_swarm_state:
      healthy_agents: "{count}"
      active_tasks: "{count}"
      queue_depth: "{count}"
  - if_agent_timeout:
      - mark_agent_unhealthy
      - reassign_tasks
      - alert_operators
```

#### `on_resource_conflict_detected`
```yaml
# Fires when: Multiple tasks claim same resource
# Action:
trigger:
  condition: resource_lock collision
detection:
  method: detect_resource_conflicts()
  from: bb5-queue-manager.py
actions:
  - log_conflict:
      resource: "{resource.name}"
      tasks: "{task_ids}"
  - resolve_strategy:
      options:
        - priority_wins: "highest priority task gets resource"
        - first_claim: "first claimer gets resource"
        - sequential: "queue tasks sequentially"
  - notify_planner:
      message: "Resource conflict detected, resolution: {strategy}"
```

#### `on_dependency_resolved`
```yaml
# Fires when: Blocking task completes
# Action:
trigger:
  condition: task.status == completed
  and: task.blocks is not empty
actions:
  - find_blocked_tasks:
      dependency: "{task.id}"
  - update_blocked_status:
      from: blocked
      to: pending
  - notify_planner:
      message: "Tasks unblocked: {task_ids}"
  - reprioritize_queue:
      method: topological_sort
```

### 3.4 Subagent Lifecycle Hooks

#### `on_subagent_spawn`
```yaml
# Fires when: Parent spawns subagent
# Action:
trigger:
  action: spawn_subagent
actions:
  - register_subagent:
      parent: "{parent.id}"
      subagent: "{subagent.id}"
      type: "{subagent.type}"
      task: "{task.id}"
  - inherit_context:
      from: parent
      to: subagent
      files: [THOUGHTS.md, DECISIONS.md]
  - set_timeout:
      subagent: "{subagent.id}"
      max_duration: "{task.estimated_minutes * 1.5}"
```

#### `on_subagent_progress`
```yaml
# Fires when: Subagent reports progress
# Action:
trigger:
  file: events.yaml
  condition: type == progress AND agent_type == subagent
actions:
  - update_parent:
      parent: "{event.parent_task}"
      progress: "{event.progress_pct}"
      status: "{event.message}"
  - check_timeout:
      elapsed: "{now - subagent.started_at}"
      max: "{subagent.timeout}"
```

#### `on_subagent_complete`
```yaml
# Fires when: Subagent finishes
# Action:
trigger:
  condition: subagent writes completion event
actions:
  - validate_output:
      format: "{expected_format}"
      completeness: "{check}"
  - integrate_results:
      into: parent_task
      results: "{subagent.output}"
  - cleanup:
      - release_subagent_resources
      - archive_subagent_run
  - notify_parent:
      status: "complete"
      summary: "{subagent.summary}"
```

---

## 4. Implementation Recommendations

### 4.1 Hook Infrastructure

```
.autonomous/hooks/
├── coordination/           # Agent-to-agent hooks
│   ├── on_task_queued.sh
│   ├── on_task_claimed.sh
│   ├── on_task_completed.sh
│   └── on_handoff_*.sh
├── swarm/                # Swarm state hooks
│   ├── on_swarm_heartbeat.sh
│   ├── on_agent_timeout.sh
│   └── on_resource_conflict.sh
├── lifecycle/            # Agent lifecycle hooks
│   ├── on_subagent_spawn.sh
│   ├── on_subagent_progress.sh
│   └── on_subagent_complete.sh
└── registry.yaml         # Hook registration and config
```

### 4.2 Hook Registry Format

```yaml
# registry.yaml
hooks:
  on_task_queued:
    version: "1.0.0"
    trigger:
      type: file_change
      file: "communications/queue.yaml"
      condition: "new task added"
    actions:
      - type: event_write
        target: "communications/events.yaml"
      - type: notification
        target: "executor"
    enabled: true
    priority: high

  on_swarm_heartbeat:
    version: "1.0.0"
    trigger:
      type: interval
      seconds: 30
    actions:
      - type: health_check
      - type: state_update
    enabled: true
```

### 4.3 Conflict Prevention Mechanisms

1. **Atomic File Operations**
   ```bash
   # Pattern: Write to temp, then rename
   echo "$content" > "$file.tmp"
   mv "$file.tmp" "$file"  # Atomic on POSIX
   ```

2. **Resource Locking**
   ```yaml
   resource_locks:
     filesystem:
       locked_paths:
         - path: "src/auth.py"
           locked_by: "TASK-001"
           locked_at: "2026-02-06T10:00:00Z"
           expires_at: "2026-02-06T10:30:00Z"
   ```

3. **Queue Claim Pattern**
   ```python
   # Only claim if status is exactly "pending"
   if task.status == "pending":
       task.status = "in_progress"
       task.claimed_by = agent_id
       atomic_write(queue_file, queue)
   ```

### 4.4 Swarm Coordination Without Chaos

**Key Principles:**

1. **Single Source of Truth:** `queue.yaml` is the authoritative task state
2. **Event-Driven Updates:** All state changes flow through `events.yaml`
3. **Atomic Operations:** All writes use temp-file + rename pattern
4. **Heartbeat Monitoring:** 30-second health checks detect dead agents
5. **Resource Locking:** Explicit locks prevent file conflicts
6. **Validation Gates:** Each stage has a validator agent

**Coordination Flow:**
```
1. Planner analyzes → Writes to queue.yaml
2. Executor polls → Reads queue.yaml
3. Executor claims → Atomic update queue.yaml
4. Executor works → Writes progress to events.yaml
5. Executor completes → Writes completion to events.yaml
6. Planner sees completion → Updates STATE.yaml
7. Hooks fire → Skill recording, task archival, unblock dependents
```

---

## 5. Existing Hooks Analysis

### 5.1 Current Hook Coverage

| Hook | Exists | Location | Status |
|------|--------|----------|--------|
| Session Start | Yes | `ralf-session-start-hook.sh` | Active |
| Session Stop | Yes | `ralf-stop-hook.sh` | Active |
| Task Completion | Partial | `task_completion_skill_recorder.py` | Active |
| Agent Start | Yes | events.yaml | Logging only |
| Agent Stop | Yes | events.yaml | Logging only |
| Task Queued | No | - | Needed |
| Task Claimed | No | - | Needed |
| Resource Conflict | No | - | Needed |
| Subagent Spawn | No | - | Needed |
| Subagent Complete | No | - | Needed |

### 5.2 Hook Gaps Identified

1. **No automatic task claiming validation** - Could lead to double-claims
2. **No resource conflict detection hook** - Relies on manual queue management
3. **No subagent lifecycle management** - Subagents don't report progress
4. **No swarm health coordination** - Heartbeats logged but not acted upon
5. **No automatic dependency unblocking** - Manual queue updates required

---

## 6. Next Steps

### 6.1 Immediate (Priority: HIGH)

1. Implement `on_task_claimed` hook with atomic validation
2. Implement `on_resource_conflict_detected` hook
3. Add resource locking to queue.yaml schema

### 6.2 Short-term (Priority: MEDIUM)

1. Implement `on_subagent_spawn` and `on_subagent_complete` hooks
2. Create hook registry.yaml for configuration
3. Add automatic dependency resolution

### 6.3 Long-term (Priority: LOW)

1. Implement full swarm health monitoring
2. Add predictive task queuing
3. Create automatic retry with backoff

---

## Appendix A: File Locations

| Component | Path |
|-----------|------|
| Queue | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` |
| Events | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml` |
| Execution State | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/execution/execution-state.yaml` |
| Session Start Hook | `/Users/shaansisodia/.blackbox5/bin/ralf-session-start-hook.sh` |
| Session Stop Hook | `/Users/shaansisodia/.blackbox5/bin/ralf-stop-hook.sh` |
| Skill Recorder | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/hooks/task_completion_skill_recorder.py` |
| Queue Manager | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/bb5-queue-manager.py` |
| Dual-RALF Handover | `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/prompts/system/handover/DUAL-RALF-HANDOVER.md` |
| 6-Agent Pipeline | `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/prompts/agents/six-agent-pipeline.md` |

---

## Appendix B: Event Types Reference

| Event Type | Fired By | Purpose |
|------------|----------|---------|
| `started` | Executor | Agent/session started |
| `in_progress` | Executor | Task execution begun |
| `completed` | Executor | Task finished successfully |
| `failed` | Executor | Task execution failed |
| `queue_refilled` | Planner | New tasks added to queue |
| `docs_modified` | Executor | Documentation updated |
| `agent_start` | Hook | Agent instance started |
| `agent_stop` | Hook | Agent instance stopped |
| `skill_used` | Hook | Skill invoked for task |
| `no_skill_used` | Hook | Task completed without skill |
