# BB5 Essential Hooks - Master Specification

**Version:** 1.0
**Date:** 2026-02-06
**Status:** Research Complete - Implementation Ready

---

## Executive Summary

After comprehensive 6-agent research (Architecture, External Patterns, Operations, Coordination, Memory, First Principles), we have determined the **essential hooks BB5 needs** to function as an "intelligent agent harness and autonomous execution operating system."

**Key Finding:** Only **3 hooks are truly essential**. The other 4 are high-value but not strictly required for MVP.

---

## Research Inputs

| Research Document | Focus | Key Finding |
|-------------------|-------|-------------|
| ARCHITECTURE_HOOKS.md | BB5 system needs | 7 essential hooks identified |
| FIRST_PRINCIPLES_HOOKS.md | Minimal requirements | Only 3 hooks are truly essential |
| EXTERNAL_HOOK_PATTERNS.md | What works elsewhere | SessionStart + PreToolUse + Stop are universal |
| OPERATIONS_HOOKS.md | Reliability needs | Health checks, corruption detection, cleanup |
| COORDINATION_HOOKS.md | Multi-agent needs | Task handoffs, swarm state, subagent lifecycle |
| MEMORY_HOOKS.md | Hindsight integration | RETAIN/RECALL/REFLECT triggers |

---

## The 3 Essential Hooks (MVP)

From first principles, BB5 needs exactly **3 hooks** to function:

```
┌─────────────────────────────────────────────────────────────┐
│                 BB5 MINIMUM VIABLE HOOKS                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. SessionStart (CANNOT BLOCK)                             │
│     → Initialize workspace, load context, inject memories   │
│                                                             │
│  2. PreToolUse (CAN BLOCK - exit 2)                         │
│     → Safety enforcement, BB5-specific validations          │
│                                                             │
│  3. Stop (CANNOT BLOCK)                                     │
│     → RALF Monitor notifications, async cleanup             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Why These Three?

| Hook | Irreducible Purpose | Why Essential |
|------|---------------------|---------------|
| **SessionStart** | Initialize run folder | Agent needs workspace before it can work |
| **PreToolUse** | Enforce safety | Safety cannot be optional - must be enforced |
| **Stop** | Cleanup on exit | Notifications and cleanup must happen even if agent crashes |

---

## The 7 High-Value Hooks (Full System)

For a complete BB5 system, we recommend **7 hooks**:

| Priority | Hook | Can Block | BB5 Function |
|----------|------|-----------|--------------|
| **P0** | SessionStart | ❌ No | Context loading, agent detection, memory injection |
| **P0** | PreToolUse | ✅ Yes | Security gates, dangerous command blocking |
| **P0** | Stop | ❌ No | RALF Monitor, cleanup, RETAIN trigger |
| **P1** | SubagentStart | ❌ No | Subagent context injection |
| **P1** | SubagentStop | ✅ Yes | Subagent validation, result verification |
| **P1** | PreCompact | ❌ No | Context preservation before compaction |
| **P2** | UserPromptSubmit | ✅ Yes | Intent detection, safety validation |

---

## Detailed Hook Specifications

### 1. SessionStart Hook (P0 - CRITICAL)

**Purpose:** Initialize BB5 sessions with full context

**Cannot Block** - Only initializes

**Input Format:**
```json
{
  "session_id": "uuid",
  "transcript_path": "/path/to/transcript.jsonl"
}
```

**BB5-Specific Functions:**

```yaml
Phase 1 - Detection:
  - Detect project from BB5_PROJECT, .bb5-project file, or path
  - Detect agent type (planner, executor, scout, verifier, architect, developer)
  - Detect mode (autonomous vs manual)
  - Generate run_id

Phase 2 - Context Loading (Agent-Specific):
  Planner:
    - Load queue.yaml (pending/completed counts)
    - Load events.yaml (recent events)
    - Load heartbeat.yaml (executor status)

  Executor:
    - Find claimed task in queue.yaml
    - Load task.md (objective, acceptance criteria)
    - Load task context from previous runs

  Scout/Verifier/Architect/Developer:
    - Load agent-specific context
    - Load relevant memories

Phase 3 - Memory Injection (Hindsight):
  - Query RECALL for memories related to current task
  - Inject top 5 most relevant memories (confidence > 0.7)
  - Format for AGENT_CONTEXT.md

Phase 4 - Environment Setup:
  - Set BB5_PROJECT, BB5_AGENT_TYPE, BB5_MODE
  - Set RALF_RUN_DIR
  - Create run folder with templates

Phase 5 - RALF Monitor:
  - Log session start
  - Send Telegram notification (optional)
```

**Output Format:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "BB5 Session | Project: blackbox5 | Agent: executor",
    "project": "blackbox5",
    "agentType": "executor",
    "mode": "autonomous",
    "runId": "run-20260206-001"
  }
}
```

**Performance Budget:** <100ms

---

### 2. PreToolUse Hook (P0 - CRITICAL)

**Purpose:** Block dangerous commands, enforce BB5 safety rules

**CAN BLOCK** (exit 2 prevents tool execution)

**Input Format:**
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /important/path",
    "description": "Clean up files"
  }
}
```

**BB5-Specific Functions:**

```yaml
Security Gates (Always Block):
  - rm -rf /, rm -rf ~, rm -rf /
  - dd if=/dev/zero of=/dev/sda
  - mkfs.ext4 on mounted partitions
  - curl | bash (unless whitelisted)
  - Any command with '&& rm -rf'

Warn List (Require Confirmation):
  - rm -rf on project directories
  - git reset --hard
  - git clean -fd
  - git push --force
  - docker system prune
  - Destructive operations on .blackbox5/

BB5-Specific Validations:
  Git Operations:
    - Block force push to main/master
    - Block reset --hard without backup
    - Validate commit messages follow BB5 format

  File Operations:
    - Block deletion of queue.yaml, events.yaml
    - Block modification of .autonomous/agents/communications/
    - Validate YAML syntax before write

  Agent-Specific Rules:
    Executor:
      - Block git operations outside task scope
      - Block file modifications outside task folder
    Planner:
      - Allow queue.yaml modifications
      - Validate task creation format
```

**Output Behavior:**
- Exit 0: Allow tool execution
- Exit 2: Block tool execution (shows error to user)

---

### 3. Stop Hook (P0 - CRITICAL)

**Purpose:** Session-end notifications, async cleanup, RETAIN trigger

**Cannot Block** - Fires after session ends

**Input Format:**
```json
{
  "session_id": "uuid-string",
  "transcript_path": "/path/to/transcript.jsonl",
  "duration_seconds": 3600
}
```

**BB5-Specific Functions:**

```yaml
Phase 1 - RALF Monitor:
  - Send Telegram notification with:
    - Agent type, project, run ID
    - Session duration
    - Task completed (if any)
    - Token usage (if available)
    - Quick links to run folder

Phase 2 - Task Completion Detection:
  - Parse transcript for completion signals
  - Detect PROMISE_COMPLETE marker
  - Identify completion status (COMPLETE/PARTIAL/BLOCKED)

Phase 3 - RETAIN Trigger:
  - Extract learnings from THOUGHTS.md, DECISIONS.md, RESULTS.md
  - Classify into 4-network memories (World/Experience/Opinion/Observation)
  - Store in vector store with embeddings

Phase 4 - Safe Auto-Actions (with safeguards):
  - Update task status in queue.yaml
  - Move task folder (active → completed) if COMPLETE
  - Log skill usage to skill-metrics.yaml
  - Auto-commit changes (if configured)

  Safeguards:
    - Backup before mutate
    - Transaction wrapper
    - Post-action verification
    - Dead letter queue on failure
```

**Critical Design Notes:**
- Stop hook CANNOT prevent session end
- All actions must be async/non-blocking
- Heavy work must be backgrounded

---

### 4. SubagentStart Hook (P1 - HIGH)

**Purpose:** Inject BB5 context into subagents

**Cannot Block**

**BB5-Specific Functions:**

```yaml
Context Injection:
  - Pass parent agent type and project
  - Pass relevant memories for subtask
  - Pass constraint context (ONE task rule)
  - Pass documentation requirements

Agent Coordination:
  - Log subagent spawn in events.yaml
  - Update agent-state.yaml
  - Track parent-child relationship
```

---

### 5. SubagentStop Hook (P1 - HIGH)

**Purpose:** Validate subagent results

**CAN BLOCK** (exit 2 prevents result acceptance)

**BB5-Specific Functions:**

```yaml
Validation:
  - Verify subagent produced RESULTS.md
  - Check THOUGHTS.md exists
  - Validate output format matches expected

Result Integration:
  - Parse subagent results
  - Update parent run context
  - Log completion in events.yaml

Blocking Conditions:
  - No RESULTS.md produced
  - Critical errors in output
  - Missing required sections
```

---

### 6. PreCompact Hook (P1 - HIGH)

**Purpose:** Preserve critical context before context compaction

**Cannot Block**

**BB5-Specific Functions:**

```yaml
Context Preservation:
  - Save current THOUGHTS.md state
  - Snapshot DECISIONS.md
  - Archive critical reasoning
  - Store as pre-compact-backup.md

State Capture:
  - Current task status
  - Pending decisions
  - Open questions
  - Blockers encountered
```

---

### 7. UserPromptSubmit Hook (P2 - MEDIUM)

**Purpose:** Intent detection, safety validation

**CAN BLOCK** (exit 2 prevents prompt processing)

**BB5-Specific Functions:**

```yaml
Intent Detection:
  - Detect "exit" intent → Warn about unsaved work
  - Detect "complete" intent → Validate task completion
  - Detect "abort" intent → Log abort reason

Safety Validation:
  - Check for destructive intent
  - Validate against current agent constraints
  - Warn on off-task requests
```

---

## Implementation Priority

### Phase 1: Foundation (Week 1-2) - MVP
1. **SessionStart v1.0** - Basic detection, context loading
2. **PreToolUse v1.0** - Basic security gates
3. **Stop v1.0** - RALF Monitor notifications only

### Phase 2: Safety (Week 3-4)
4. **PreToolUse v1.1** - BB5-specific validations
5. **Stop v1.1** - RETAIN trigger
6. **UserPromptSubmit v1.0** - Intent detection

### Phase 3: Coordination (Week 5-6)
7. **SubagentStart v1.0** - Context injection
8. **SubagentStop v1.0** - Result validation
9. **PreCompact v1.0** - Context preservation

### Phase 4: Memory (Week 7-8)
10. **SessionStart v1.1** - RECALL integration
11. **Stop v1.2** - Full RETAIN integration
12. All hooks - Performance optimization

---

## Hook Combinations for BB5 Workflows

### Workflow 1: Task Execution
**Hooks:** SessionStart → PreToolUse → Stop

**Flow:**
1. SessionStart loads task context
2. PreToolUse enforces safety during work
3. Stop sends notification, triggers RETAIN

### Workflow 2: Multi-Agent Coordination
**Hooks:** SubagentStart → SubagentStop + SessionStart

**Flow:**
1. Parent spawns subagent (SubagentStart injects context)
2. Subagent runs with its own SessionStart
3. Subagent completes (SubagentStop validates)

### Workflow 3: Long-Running Task
**Hooks:** SessionStart → PreCompact → Stop

**Flow:**
1. SessionStart loads context
2. PreCompact preserves state before context loss
3. Stop archives completed work

### Workflow 4: Safety-Critical Work
**Hooks:** UserPromptSubmit → PreToolUse → SubagentStop

**Flow:**
1. UserPromptSubmit validates intent
2. PreToolUse blocks dangerous operations
3. SubagentStop validates results

---

## BB5-Specific Validations Matrix

| Hook | Queue.yaml | Events.yaml | Task.md | Run Docs | Git State | Memories |
|------|------------|-------------|---------|----------|-----------|----------|
| SessionStart | Verify schema | Load recent | Load if executor | N/A | Detect branch | RECALL injection |
| PreToolUse | Block modify | Block modify | Block modify | N/A | Validate ops | N/A |
| Stop | Update status | Log completion | Update status | Validate exist | Auto-commit | RETAIN trigger |
| SubagentStart | N/A | Log spawn | N/A | N/A | N/A | N/A |
| SubagentStop | N/A | Log complete | N/A | Validate | N/A | N/A |
| PreCompact | N/A | N/A | N/A | Backup | N/A | N/A |
| UserPromptSubmit | N/A | N/A | N/A | N/A | N/A | N/A |

---

## Configuration

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/2-engine/.autonomous/hooks/active/session-start.py"
      }]
    }],
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/2-engine/.autonomous/hooks/active/pre-tool-use.py"
      }]
    }],
    "Stop": [{
      "hooks": [
        {
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/2-engine/.autonomous/hooks/active/ralf-monitor.py",
          "timeout": 30
        },
        {
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/2-engine/.autonomous/hooks/active/stop-cleanup.py",
          "timeout": 60
        }
      ]
    }],
    "SubagentStart": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/2-engine/.autonomous/hooks/active/subagent-start.py"
      }]
    }],
    "SubagentStop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/2-engine/.autonomous/hooks/active/subagent-stop.py"
      }]
    }],
    "PreCompact": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/2-engine/.autonomous/hooks/active/pre-compact.py"
      }]
    }],
    "UserPromptSubmit": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/2-engine/.autonomous/hooks/active/user-prompt-submit.py"
      }]
    }]
  }
}
```

---

## Key Insights from Research

### From First Principles
- Only 3 hooks are truly essential (SessionStart, PreToolUse, Stop)
- Hooks should only do what agents cannot do themselves
- Stop hooks cannot block - they fire after session ends

### From External Patterns
- SessionStart + PreToolUse + Stop are universal across systems
- Most successful hooks are guardrails, not enforcement
- Hook combinations work better than individual hooks

### From Architecture
- BB5 needs agent-type-specific context loading
- Hindsight memory integration requires RECALL/RETAIN hooks
- Multi-agent coordination needs Subagent hooks

### From Operations
- Health checks prevent system degradation
- Cleanup hooks prevent storage exhaustion
- Validation hooks prevent state corruption

---

## Next Steps

1. **Implement MVP (3 hooks)** - SessionStart, PreToolUse, Stop
2. **Test with real tasks** - Validate the approach
3. **Add P1 hooks** - SubagentStart/Stop, PreCompact
4. **Add P2 hooks** - UserPromptSubmit
5. **Iterate based on usage** - Refine based on real-world needs

---

## References

- [ARCHITECTURE_HOOKS.md](ARCHITECTURE_HOOKS.md)
- [FIRST_PRINCIPLES_HOOKS.md](FIRST_PRINCIPLES_HOOKS.md)
- [EXTERNAL_HOOK_PATTERNS.md](EXTERNAL_HOOK_PATTERNS.md)
- [OPERATIONS_HOOKS.md](OPERATIONS_HOOKS.md)
- [COORDINATION_HOOKS.md](COORDINATION_HOOKS.md)
- [MEMORY_HOOKS.md](MEMORY_HOOKS.md)

---

*Synthesized from comprehensive 6-agent research process*
