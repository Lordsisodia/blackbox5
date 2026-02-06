# BB5 Essential Hooks Architecture

**Version:** 1.0
**Date:** 2026-02-06
**Status:** Architecture Specification
**Based On:** BB5 Key Thesis, Stop Hook Lessons Learned, SessionStart Design

---

## Executive Summary

For BlackBox5 to function as an "intelligent agent harness and autonomous execution operating system," it requires a **minimum viable set of 7 hooks** out of Claude Code's 12 available hook types. These hooks form the backbone of BB5's ability to run agents, maintain continuity of self, enable multi-agent coordination, and prevent system drift.

**Critical Finding:** Not all hooks can block. Understanding hook capabilities is essential to placing validation logic correctly.

---

## First Principles Analysis

### What Does BB5 Need to Function?

Based on the BB5 Key Thesis, the system must:

1. **Run Agents** - Initialize context, detect agent type, load relevant state
2. **Remember** - Capture learnings, persist memories across sessions
3. **Learn** - Extract insights from every execution
4. **Improve** - Track metrics, validate quality, enable self-optimization
5. **Coordinate** - Multi-agent queue management, heartbeat, state sync
6. **Navigate** - Self-orient in project hierarchies

### What Prevents Drift?

1. **State Validation** - Ensure queue.yaml, events.yaml consistency
2. **Quality Gates** - Validate work before it propagates
3. **Memory Persistence** - RETAIN operation at task completion
4. **Context Loading** - RECALL operation at session start
5. **Heartbeat Monitoring** - Detect stuck/blocked agents

---

## The 7 Essential Hooks

### Priority Order (Critical → Important → Enhancing)

| Priority | Hook | Can Block | BB5 Critical Function |
|----------|------|-----------|----------------------|
| **P0 - CRITICAL** | SessionStart | No | Agent detection, context loading, memory injection |
| **P0 - CRITICAL** | PreToolUse | Yes | Security gates, dangerous command blocking |
| **P0 - CRITICAL** | Stop | No | Task completion, RETAIN trigger, cleanup, notifications |
| **P1 - HIGH** | SubagentStart | No | Subagent context, agent coordination |
| **P1 - HIGH** | SubagentStop | Yes | Subagent validation, result verification |
| **P1 - HIGH** | PreCompact | No | Context preservation before compaction |
| **P2 - MEDIUM** | UserPromptSubmit | Yes | Intent detection, safety validation |

### 5 Hooks NOT Essential for MVP

| Hook | Why Not Essential | When Needed |
|------|-------------------|-------------|
| PostToolUse | Nice for logging, not critical | Production monitoring |
| PostToolUseFailure | Error handling can be in-tool | Complex retry logic |
| Notification | Can be part of Stop hook | Multi-channel alerts |
| PermissionRequest | Can use defaults | Fine-grained security |
| SessionEnd | Stop hook handles cleanup | Complex archival |

---

## Hook Specifications

### 1. SessionStart Hook (P0 - CRITICAL)

**Purpose:** Initialize BB5 sessions with full context

**Cannot Block** - Only initializes

**BB5-Specific Functions:**

```yaml
Phase 1 - Detection:
  - Detect project from BB5_PROJECT, .bb5-project file, or path
  - Detect agent type from BB5_AGENT_TYPE, RALF_RUN_DIR, or file patterns
  - Detect mode (autonomous vs manual) from RALF_RUN_DIR, BB5_AUTONOMOUS
  - Generate run_id if not present

Phase 2 - Context Loading (Agent-Specific):
  Planner:
    - Load queue.yaml (pending count, completed count)
    - Load events.yaml (last 5 events)
    - Load heartbeat.yaml (executor status)
    - Load loop-metadata-template.yaml

  Executor:
    - Find claimed task in queue.yaml
    - Load task.md (objective, acceptance criteria)
    - Load task context from runs/

  Scout:
    - Load scout parameters from task
    - Load previous scout reports

  Verifier:
    - Load verification target
    - Load verification criteria

  Architect:
    - Load goals/INDEX.yaml
    - Load recent decisions from decisions/

  Developer:
    - Load basic project info
    - Load recent timeline entries

Phase 3 - Memory Injection (Hindsight Integration):
  - Query RECALL for memories related to current task
  - Inject top 5 most relevant memories (confidence > 0.7)
  - Format for Claude's context window

Phase 4 - Environment Setup:
  - Set BB5_PROJECT, BB5_AGENT_TYPE, BB5_MODE
  - Set BB5_CONTEXT_LOADED=true
  - Set BB5_HOOK_VERSION
  - Set RALF_RUN_DIR if autonomous mode

Phase 5 - Validation:
  - Verify queue.yaml schema version
  - Verify events.yaml exists
  - Log any missing context (non-blocking)
```

**Output Format:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "BB5 Session | Project: blackbox5 | Agent: executor | Mode: autonomous",
    "project": "blackbox5",
    "agentType": "executor",
    "mode": "autonomous",
    "runId": "run-20260206-001",
    "context": {
      "claimedTask": { "id": "TASK-001", "title": "...", "status": "..." },
      "queueStats": { "pending": 12, "completed": 45 },
      "relevantMemories": [...]
    }
  }
}
```

**Performance Budget:** <100ms total
- Detection: <20ms
- Context Loading: <50ms
- Memory Injection: <20ms
- Env Setup: <10ms

---

### 2. PreToolUse Hook (P0 - CRITICAL)

**Purpose:** Block dangerous commands, enforce BB5 safety rules

**CAN BLOCK** (exit 2 prevents tool execution)

**BB5-Specific Functions:**

```yaml
Security Gates:
  Block List (Always):
    - rm -rf /
    - rm -rf ~
    - rm -rf /
    - Any command with '&& rm -rf'
    - dd if=/dev/zero of=/dev/sda
    - mkfs.ext4 on mounted partitions
    - curl | bash (unless whitelisted)
    - wget -O - | bash (unless whitelisted)

  Warn List (Require Confirmation):
    - rm -rf on project directories
    - git reset --hard
    - git clean -fd
    - git push --force
    - docker system prune
    - Any destructive operation on .blackbox5/

BB5-Specific Validations:
  Git Operations:
    - Block force push to main/master
    - Block reset --hard without backup
    - Warn on uncommitted changes before destructive ops
    - Validate commit messages follow BB5 format

  File Operations:
    - Block deletion of queue.yaml, events.yaml
    - Block modification of .autonomous/agents/communications/
    - Warn on bulk file operations (>10 files)
    - Validate YAML syntax before write

  Database Operations:
    - Block DROP TABLE on BB5 tables
    - Block DELETE without WHERE
    - Warn on UPDATE without WHERE

Agent-Specific Rules:
  Executor:
    - Block git operations outside task scope
    - Block file modifications outside task folder

  Planner:
    - Allow queue.yaml modifications
    - Validate task creation format
```

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

**Output Behavior:**
- Exit 0: Allow tool execution
- Exit 2: Block tool execution (shows error to user)
- Exit 1: Error in hook (logs error, allows execution)

**Error Message Format:**
```
[BB5 Security Gate Blocked]

Command: rm -rf /important/path
Reason: Destructive operation on protected directory

Protected paths:
- ~/.blackbox5/2-engine/.autonomous/agents/communications/
- ~/.blackbox5/5-project-memory/*/tasks/active/*/task.md

Use --force flag or modify command to proceed.
```

---

### 3. Stop Hook (P0 - CRITICAL)

**Purpose:** Session-end cleanup, notifications, RETAIN trigger

**Cannot Block** - Fires after session ends

**BB5-Specific Functions:**

```yaml
Phase 1 - RALF Monitor (v1.0):
  - Send Telegram notification
  - Include: agent type, project, duration, task completed
  - Include quick links to run folder
  - Track session metrics

Phase 2 - Task Completion Detection:
  - Parse transcript for completion signals
  - Detect PROMISE_COMPLETE, exit status
  - Identify task_id from context
  - Determine completion status (COMPLETE/PARTIAL/BLOCKED)

Phase 3 - Auto-Actions (v1.1) - WITH SAFEGUARDS:
  Preconditions:
    - Check run folder exists
    - Verify THOUGHTS.md exists (if executor)
    - Validate no concurrent modifications

  Actions:
    - Update task status in queue.yaml
    - Move task folder (active → completed) if COMPLETE
    - Run RETAIN operation on run documents
    - Log skill usage to skill-metrics.yaml
    - Auto-commit changes (if configured)

  Safeguards:
    - Backup before mutate
    - Transaction wrapper (all-or-nothing)
    - Post-action verification
    - Dead letter queue on failure
    - Idempotency checks

Phase 4 - Memory Extraction:
  - Extract from THOUGHTS.md → EXPERIENCES.md
  - Extract from DECISIONS.md → FACTS.md + OPINIONS.md
  - Extract from RESULTS.md → OBSERVATIONS.md
  - Store in PostgreSQL + Neo4j

Phase 5 - Metrics Collection:
  - Session duration
  - Token usage (if available)
  - Files modified
  - Success/failure status
  - Log to metrics system
```

**Input Format:**
```json
{
  "session_id": "uuid-string",
  "transcript_path": "/path/to/transcript.jsonl",
  "duration_seconds": 3600
}
```

**Critical Design Notes:**
- Stop hook CANNOT prevent session end
- All actions must be async/non-blocking
- Heavy work must be backgrounded
- Exit codes don't matter (session already ended)

---

### 4. SubagentStart Hook (P1 - HIGH)

**Purpose:** Inject BB5 context into subagents

**Cannot Block** - Only injects context

**BB5-Specific Functions:**

```yaml
Context Injection:
  - Pass parent agent type
  - Pass current project
  - Pass relevant memories for subtask
  - Pass constraint context (ONE task rule)
  - Pass documentation requirements

Agent Coordination:
  - Log subagent spawn in events.yaml
  - Update agent-state.yaml
  - Track parent-child relationship
  - Inherit parent's mode (autonomous/manual)

Validation:
  - Verify subagent task is defined
  - Check subagent count limits
  - Warn on deep nesting (>3 levels)
```

**Output Format:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "BB5 Subagent | Parent: executor | Project: blackbox5 | Task: research-component",
    "parentAgent": "executor",
    "project": "blackbox5",
    "constraints": ["ONE task per run", "Document in THOUGHTS.md"]
  }
}
```

---

### 5. SubagentStop Hook (P1 - HIGH)

**Purpose:** Validate subagent results, ensure quality

**CAN BLOCK** (exit 2 prevents result acceptance)

**BB5-Specific Functions:**

```yaml
Validation:
  - Verify subagent produced RESULTS.md
  - Check THOUGHTS.md exists
  - Validate output format matches expected
  - Check for error patterns in output

Result Integration:
  - Parse subagent results
  - Update parent run context
  - Log completion in events.yaml
  - Trigger parent notification

Blocking Conditions:
  - No RESULTS.md produced (unless exploration)
  - Critical errors in output
  - Missing required sections
  - Format validation failures
```

**Input Format:**
```json
{
  "agent_type": "researcher",
  "result": "subagent output text"
}
```

---

### 6. PreCompact Hook (P1 - HIGH)

**Purpose:** Preserve critical context before Claude compacts context window

**Cannot Block** - Only preserves data

**BB5-Specific Functions:**

```yaml
Context Preservation:
  - Save current THOUGHTS.md state
  - Snapshot DECISIONS.md
  - Archive critical reasoning
  - Store in run folder as pre-compact-backup.md

State Capture:
  - Current task status
  - Pending decisions
  - Open questions
  - Blockers encountered

Notification:
  - Log compaction event
  - Include compaction reason (token limit, manual)
  - Track compaction frequency per run
```

**Why This Matters:**
When Claude's context window fills, it "compacts" (summarizes) the conversation. BB5 runs can span long sessions. PreCompact ensures critical reasoning isn't lost during compaction.

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
  - Detect "skip" intent → Track bypass usage

Safety Validation:
  - Check for destructive intent
  - Validate against current agent constraints
  - Warn on off-task requests

BB5-Specific Patterns:
  - "just do it" → Bypass validation flag
  - "skip docs" → Document bypass
  - "force" → Override blocking
  - "exit anyway" → Confirm data loss
```

**Input Format:**
```json
{
  "prompt": "exit",
  "context": { ... }
}
```

---

## Hook Dependencies & Ordering

### Execution Order

```
Session Start:
  1. SessionStart (always fires first)
  2. UserPromptSubmit (when user types)
  3. PreToolUse (before each tool)
  4. PostToolUse (after each tool success)
  5. PostToolUseFailure (after each tool failure)
  6. PreCompact (when context fills)
  7. SubagentStart (when spawning subagent)
  8. SubagentStop (when subagent completes)
  9. Stop (when session ends)
  10. SessionEnd (final cleanup)
```

### Data Dependencies

```
SessionStart → All Other Hooks
  - Sets BB5_PROJECT, BB5_AGENT_TYPE
  - Loads queue.yaml, events.yaml
  - Without this, other hooks lack context

PreToolUse → Stop
  - PreToolUse blocks dangerous operations
  - Stop assumes operations were safe

SubagentStart → SubagentStop
  - Start logs spawn, Stop validates result
  - Parent-child relationship tracked

Stop → SessionEnd
  - Stop performs cleanup
  - SessionEnd finalizes
```

### Critical Path

**Minimum Viable BB5 requires:**
1. SessionStart (context)
2. PreToolUse (safety)
3. Stop (cleanup)

Without these 3 hooks, BB5 cannot function as an autonomous agent OS.

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

## Implementation Priority

### Phase 1: Foundation (Week 1-2)
1. **SessionStart v1.0** - Basic detection, context loading
2. **PreToolUse v1.0** - Basic security gates
3. **Stop v1.0** - RALF Monitor notifications only

### Phase 2: Safety (Week 3-4)
4. **PreToolUse v1.1** - BB5-specific validations
5. **Stop v1.1** - Safe auto-actions with transactions
6. **UserPromptSubmit v1.0** - Intent detection

### Phase 3: Coordination (Week 5-6)
7. **SubagentStart v1.0** - Context injection
8. **SubagentStop v1.0** - Result validation
9. **PreCompact v1.0** - Context preservation

### Phase 4: Memory (Week 7-8)
10. **SessionStart v1.1** - RECALL integration
11. **Stop v1.2** - RETAIN integration
12. All hooks - Performance optimization

---

## Failure Modes & Mitigations

| Hook | Failure Mode | Impact | Mitigation |
|------|--------------|--------|------------|
| SessionStart | Detection fails | Wrong context | Default to blackbox5, log error |
| SessionStart | Context load fails | Missing state | Continue with basic info |
| PreToolUse | False positive | Blocks valid work | Whitelist, override flag |
| PreToolUse | False negative | Dangerous op runs | Audit log, post-hoc review |
| Stop | Notification fails | Silent failure | Retry, dead letter queue |
| Stop | Auto-action fails | Inconsistent state | Transaction rollback, alert |
| SubagentStop | Validation fails | Bad result accepted | Parent review, escalation |

---

## Configuration Schema

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
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/2-engine/.autonomous/hooks/active/ralf-monitor.py",
        "timeout": 30
      }, {
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/2-engine/.autonomous/hooks/active/stop-cleanup.py",
        "timeout": 60
      }]
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

## Summary

**Essential Hooks: 7 out of 12**

**Critical (P0):**
1. SessionStart - Context loading, agent detection
2. PreToolUse - Security gates, BB5 validations
3. Stop - Cleanup, notifications, RETAIN trigger

**High (P1):**
4. SubagentStart - Subagent context injection
5. SubagentStop - Subagent result validation
6. PreCompact - Context preservation

**Medium (P2):**
7. UserPromptSubmit - Intent detection

**Dependencies:**
- SessionStart must fire first (provides context to all others)
- PreToolUse must validate before Stop assumes safety
- SubagentStart/Stop form a pair

**Key Insight:**
Understanding which hooks can block (PreToolUse, UserPromptSubmit, SubagentStop) vs which cannot (SessionStart, Stop, PreCompact, SubagentStart) is critical for placing validation logic correctly. BB5's quality gates must be in blocking hooks; cleanup/async actions go in non-blocking hooks.

---

*Based on BB5 Key Thesis, Stop Hook Design Lessons, and SessionStart Specification*
