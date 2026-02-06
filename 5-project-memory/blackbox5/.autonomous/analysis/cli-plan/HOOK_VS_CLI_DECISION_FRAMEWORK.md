# BB5 Hook vs CLI Decision Framework

**Version:** 1.0
**Date:** 2026-02-06
**Status:** Architecture Decision Record
**Based On:** First Principles Analysis, Task Claim Review, Operations Research

---

## Executive Summary

This document establishes clear decision criteria for when to implement functionality as a **Claude Code Hook** versus a **BB5 CLI Command**. The framework is derived from extensive analysis of BB5's operational patterns, the Task Claim hook review, and first principles breakdown of BB5's requirements.

**Key Principle:** Hooks are for infrastructure and enforcement; CLI commands are for explicit workflow actions.

---

## 1. Hook Criteria

### 1.1 When Should Something Be a Hook?

A hook is appropriate when ALL of the following are true:

| Criterion | Explanation |
|-----------|-------------|
| **Lifecycle Event** | The event is outside the agent's direct control (session start/end, tool execution) |
| **Must Be Automatic** | The action must happen without explicit user intent |
| **Enforcement Required** | The action enforces policy or safety that agents cannot self-police |
| **Cleanup After Failure** | The action must run even if the agent crashes or exits unexpectedly |

### 1.2 Valid Hook Use Cases

| Use Case | Hook Type | Why It's a Hook |
|----------|-----------|-----------------|
| **Run folder creation** | SessionStart | Agent needs workspace before it can work |
| **Safety enforcement** | PreToolUse | Agents cannot be trusted to self-police dangerous operations |
| **Context preservation** | PreCompact | Must happen automatically when context window fills |
| **Session cleanup** | SessionEnd/Stop | Must run even if agent crashes |
| **Subagent context injection** | SubagentStart | Must happen automatically when subagent spawns |
| **Intent validation** | UserPromptSubmit | Must intercept before processing destructive commands |

### 1.3 Hook Constraints

**Performance Requirements:**
- SessionStart: <100ms total execution time
- PreToolUse: <50ms (blocks every tool call)
- UserPromptSubmit: <30ms (blocks user input)
- Stop/SessionEnd: <5 seconds (cleanup can be longer)

**Blocking Capabilities:**
| Hook Type | Can Block? | Use for Enforcement? |
|-----------|------------|---------------------|
| SessionStart | No | No - only initialize |
| PreToolUse | **Yes** | **Yes** - primary enforcement point |
| UserPromptSubmit | **Yes** | **Yes** - intent validation |
| SubagentStart | No | No - only inject context |
| SubagentStop | **Yes** | **Yes** - result validation |
| PreCompact | No | No - only preserve data |
| Stop | **No** | **No** - fires after session ends |
| SessionEnd | **No** | **No** - fires after session ends |

**Critical Rule:** Stop and SessionEnd hooks CANNOT block or prevent session termination. They fire AFTER the session has ended. Any validation must happen in PreToolUse or UserPromptSubmit.

---

## 2. CLI Criteria

### 2.1 When Should Something Be a CLI Command?

A CLI command is appropriate when ANY of the following are true:

| Criterion | Explanation |
|-----------|-------------|
| **Explicit User Intent** | The action requires clear user intent ("I want to do X") |
| **Workflow Operation** | The action is part of normal task/goal/plan workflow |
| **Transactional State Change** | The action modifies state that needs atomic updates |
| **Needs Error Feedback** | The action requires clear success/failure feedback to the user |
| **Idempotency Required** | The action should be safely repeatable |
| **Composability Needed** | The action should work in scripts, aliases, or pipes |

### 2.2 Valid CLI Use Cases

| Use Case | CLI Command | Why It's a CLI |
|----------|-------------|----------------|
| **Task claiming** | `bb5 claim TASK-001` | Explicit intent, transactional, needs feedback |
| **Task listing** | `bb5 task:list` | Information lookup, user-initiated |
| **Goal creation** | `bb5 goal:create` | Explicit workflow action |
| **Plan linking** | `bb5 link:plan PLAN-001` | State modification with dependencies |
| **Navigation** | `bb5 goto TASK-001` | User-initiated context switch |
| **Status updates** | `bb5 task:complete TASK-001` | Explicit completion action |
| **Health checks** | `bb5 health` | On-demand diagnostic |
| **Documentation validation** | `bb5 validate-docs` | Explicit quality gate |

### 2.3 CLI Benefits

| Benefit | Explanation |
|---------|-------------|
| **Explicitness** | Clear user intent - no hidden magic |
| **Feedback** | Direct success/failure messages |
| **Testability** | Easy to unit test, script, and automate |
| **Debuggability** | Clear command history, reproducible |
| **Idempotency** | Can check state and prevent double-execution |
| **Composability** | Works in shell scripts, aliases, CI/CD |
| **Error Handling** | Clear error messages and exit codes |
| **Documentation** | Self-documenting through help text |

---

## 3. Decision Matrix for BB5 Operations

### 3.1 Core Workflow Operations

| Operation | Hook or CLI? | Decision | Rationale |
|-----------|--------------|----------|-----------|
| **Task claiming** | **CLI** | `bb5 claim TASK-001` | Explicit intent, transactional, needs feedback |
| **Session initialization** | **Hook** | SessionStart | Must happen before agent can work |
| **Safety enforcement** | **Hook** | PreToolUse | Must block dangerous operations automatically |
| **Run folder creation** | **Hook** | SessionStart | Agent needs workspace before working |
| **Task listing** | **CLI** | `bb5 task:list` | Information lookup, user-initiated |
| **Task completion** | **CLI** | `bb5 task:complete TASK-001` | Explicit action, updates multiple files |
| **Goal creation** | **CLI** | `bb5 goal:create` | Workflow action with template generation |
| **Plan linking** | **CLI** | `bb5 link:plan` | State modification with validation |

### 3.2 Documentation & Validation Operations

| Operation | Hook or CLI? | Decision | Rationale |
|-----------|--------------|----------|-----------|
| **Documentation validation** | **CLI** | `bb5 validate-docs` | Explicit quality gate, not automatic |
| **Template population** | **CLI** | `bb5 populate-template` | Called explicitly when needed |
| **THOUGHTS.md creation** | **Hook** | SessionStart | Part of run folder initialization |
| **Documentation generation** | **CLI** | `bb5 generate-docs` | Explicit action, user-controlled |
| **Pre-exit validation** | **CLI** | Agent responsibility | Stop hooks cannot block; agent must validate before exit |

### 3.3 State Management Operations

| Operation | Hook or CLI? | Decision | Rationale |
|-----------|--------------|----------|-----------|
| **Queue updates** | **CLI** | `bb5 queue:update` | State modification, needs atomicity |
| **Timeline updates** | **CLI** | `bb5 timeline:update` | Explicit milestone tracking |
| **State synchronization** | **CLI** | `bb5 sync` | On-demand reconciliation |
| **Queue integrity check** | **CLI** | `bb5 queue:validate` | Diagnostic tool |
| **Auto-sync on completion** | **CLI** | Called by agent | Agent invokes after completing work |

### 3.4 Git Operations

| Operation | Hook or CLI? | Decision | Rationale |
|-----------|--------------|----------|-----------|
| **Git safety enforcement** | **Hook** | PreToolUse | Block force push, rm -rf automatically |
| **Commit message validation** | **Hook** | PreToolUse | Enforce BB5 format before commit |
| **Auto-commit on complete** | **CLI** | `bb5 commit` | Explicit or agent-invoked, not automatic |
| **Git status check** | **CLI** | `bb5 git:status` | Information lookup |
| **Branch creation** | **CLI** | `bb5 git:branch` | Workflow operation |

### 3.5 Monitoring & Maintenance Operations

| Operation | Hook or CLI? | Decision | Rationale |
|-----------|--------------|----------|-----------|
| **Health checks** | **CLI** | `bb5 health` | On-demand diagnostic |
| **System dashboard** | **CLI** | `bb5 dashboard` | Information display |
| **Orphaned task detection** | **CLI** | `bb5 queue:audit` | Maintenance operation |
| **Run folder cleanup** | **CLI** | `bb5 cleanup:runs` | Explicit maintenance |
| **Metrics collection** | **CLI** | `bb5 metrics:collect` | Explicit or cron-scheduled |
| **Storage monitoring** | **Hook** | SessionStart | Check disk space before work begins |
| **Session notification** | **Hook** | Stop | Notify on session end (RALF Monitor) |

### 3.6 Memory & Learning Operations

| Operation | Hook or CLI? | Decision | Rationale |
|-----------|--------------|----------|-----------|
| **Memory injection (RECALL)** | **Hook** | SessionStart | Load relevant memories automatically |
| **Memory extraction (RETAIN)** | **Hook** | Stop | Extract learnings on session end |
| **Memory search** | **CLI** | `bb5 memory:search` | Explicit query |
| **Learning capture** | **CLI** | Agent writes directly | Agent appends to LEARNINGS.md |
| **Skill metrics update** | **CLI** | `bb5 skill:log` | Called after skill usage |

---

## 4. Anti-Patterns

### 4.1 What Should NEVER Be a Hook

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| **Task claiming as hook** | Violates explicitness, poor error handling | Use `bb5 claim` CLI |
| **Documentation validation as Stop hook** | Stop hooks cannot block; validation too late | Agent validates before exit |
| **Git commit as automatic hook** | Commits should be intentional | Agent or user runs `git commit` |
| **Queue updates as PostToolUse** | Creates race conditions, hidden side effects | Agent updates queue explicitly |
| **Intent detection via regex** | Fragile, false positives/negatives | Explicit CLI commands |
| **File watcher triggers** | Hidden magic, race conditions, hard to debug | Explicit CLI or agent action |
| **Timeline auto-updates** | Agent knows milestones better than hook | Agent updates at milestones |
| **Auto-state-sync on every change** | Performance impact, unnecessary | Periodic or explicit sync |

### 4.2 What Should NEVER Be a CLI

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| **Safety enforcement as CLI** | Agents cannot self-police | PreToolUse hook |
| **Run folder creation as CLI** | Agent needs workspace before working | SessionStart hook |
| **Session cleanup as CLI** | Won't run if agent crashes | SessionEnd hook |
| **Context preservation as CLI** | Must happen automatically | PreCompact hook |
| **Tool-level validation as CLI** | Must block before tool executes | PreToolUse hook |
| **Mandatory notifications as CLI** | Must happen reliably | Stop hook |

### 4.3 Common Mistakes to Avoid

#### Mistake 1: "Convenience Hooks"
**Wrong:** Adding hooks for things that are "nice to have" automatic behavior.

**Example:** Auto-updating timeline on every file change.
```bash
# BAD - PostToolUse hook
if [ "$tool_name" = "Write" ]; then
    update_timeline "file_modified"
fi
```

**Correct:** Agent updates timeline at milestones.
```bash
# GOOD - Agent action
# In THOUGHTS.md: "Reached milestone X, updating timeline"
bb5 timeline:update --milestone "phase-1-complete"
```

#### Mistake 2: "Stop Hook Validation"
**Wrong:** Trying to validate or block in Stop hook.

**Example:** Preventing exit if documentation incomplete.
```bash
# BAD - Stop hook (cannot block)
if [ ! -f "$RUN_DIR/RESULTS.md" ]; then
    echo "ERROR: Cannot exit without RESULTS.md"
    exit 1  # Too late - session already ended!
fi
```

**Correct:** Agent validates before exit; UserPromptSubmit can warn.
```bash
# GOOD - Agent responsibility
# Before exit, agent checks:
bb5 validate-docs || echo "Warning: Documentation incomplete"
```

#### Mistake 3: "Hidden Side Effects"
**Wrong:** Hooks that modify state the user doesn't expect.

**Example:** SessionStart claiming tasks automatically.
```python
# BAD - SessionStart hook
if detect_task_context():
    claim_task()  # Surprise! Task was claimed.
```

**Correct:** Explicit CLI command.
```bash
# GOOD - Explicit CLI
bb5 claim TASK-001  # User knows exactly what happened
```

#### Mistake 4: "Tight Coupling"
**Wrong:** Hooks that know too much about internal structure.

**Example:** Hook that parses task.md format directly.
```bash
# BAD - Fragile hook
task_title=$(grep "^# " "$task_file" | head -1)
```

**Correct:** CLI command with stable interface.
```bash
# GOOD - Stable CLI
bb5 task:show TASK-001 --format json | jq -r '.title'
```

#### Mistake 5: "Regex Intent Detection"
**Wrong:** Parsing natural language in hooks.

**Example:** UserPromptSubmit detecting "claim task" patterns.
```python
# BAD - Fragile regex
if re.search(r'claim\s+(TASK-\d+)', prompt):
    claim_task(match.group(1))
```

**Correct:** Explicit command.
```bash
# GOOD - Explicit
bb5 claim TASK-001
```

---

## 5. Examples: Correct vs Incorrect Choices

### Example 1: Task Claiming

**Incorrect (Hook Approach):**
```yaml
# hooks/UserPromptSubmit/task-claim.yaml
matcher: "claim*"
action: |
  # Parse task ID from prompt
  # Create run folder
  # Update queue
  # Inject context
```

**Problems:**
- Fragile regex matching
- Hidden side effects
- Poor error handling
- No idempotency
- Hard to debug

**Correct (CLI Approach):**
```bash
$ bb5 claim TASK-001
Validating task... OK
Checking availability... OK
Creating run folder... runs/run-20260206-143200-TASK-001/
Generating THOUGHTS.md... OK
Updating queue... OK
Task TASK-001 claimed successfully.
```

**Benefits:**
- Explicit intent
- Clear feedback
- Atomic operation
- Idempotent
- Easy to debug

---

### Example 2: Documentation Validation

**Incorrect (Stop Hook):**
```bash
#!/bin/bash
# hooks/Stop/validate-docs.sh
if [ ! -f "$RUN_DIR/RESULTS.md" ]; then
    echo "ERROR: RESULTS.md missing"
    exit 1  # Cannot block - session already ended!
fi
```

**Problems:**
- Cannot actually prevent exit
- False sense of enforcement
- Error appears after user already at shell

**Correct (Agent Responsibility):**
```bash
# Agent validates before exit
bb5 validate-docs
if [ $? -ne 0 ]; then
    echo "Documentation incomplete. Continue anyway? (y/n)"
    # Or use UserPromptSubmit to warn on "exit" intent
fi
```

**Benefits:**
- Actual enforcement
- User can fix before exit
- Clear feedback

---

### Example 3: Safety Enforcement

**Incorrect (CLI Approach):**
```bash
$ bb5 safety-check "rm -rf /"
DANGER: This command is destructive!
Continue? (y/n): n
$ rm -rf /  # User can bypass!
```

**Problems:**
- User can ignore or bypass
- Not automatic
- Inconsistent enforcement

**Correct (PreToolUse Hook):**
```python
#!/usr/bin/env python3
# hooks/PreToolUse/security.py
import sys, json

data = json.load(sys.stdin)
if data['tool_name'] == 'Bash':
    cmd = data['tool_input']['command']
    if 'rm -rf /' in cmd or 'rm -rf ~' in cmd:
        print("BLOCKED: Dangerous command", file=sys.stderr)
        sys.exit(2)  # Actually blocks!
```

**Benefits:**
- Automatic enforcement
- Cannot be bypassed
- Consistent protection

---

### Example 4: Timeline Updates

**Incorrect (PostToolUse Hook):**
```bash
# hooks/PostToolUse/timeline-update.sh
# Fires on every tool use - wasteful!
if [ "$tool_name" = "Write" ] && [[ "$file" == *"milestone"* ]]; then
    update_timeline "milestone_reached"
fi
```

**Problems:**
- Fires constantly
- Wasteful
- May miss actual milestones
- Race conditions

**Correct (Agent-Driven):**
```markdown
<!-- In THOUGHTS.md -->
## Progress

- [x] Phase 1: Design
- [x] Phase 2: Implementation  <- Agent reaches here
- [ ] Phase 3: Testing

Milestone: Implementation complete. Updating timeline.
```

```bash
# Agent explicitly updates
bb5 timeline:update --event "milestone" --data "phase-2-complete"
```

**Benefits:**
- Only updates at actual milestones
- Accurate
- No wasted operations
- Agent knows context

---

## 6. Implementation Guidelines

### 6.1 When Creating a New Hook

**Checklist:**
- [ ] Does this enforce safety or policy? (Must be PreToolUse)
- [ ] Does this create the environment before work? (SessionStart)
- [ ] Does this clean up after crashes? (SessionEnd/Stop)
- [ ] Can the agent NOT do this itself?
- [ ] Is this truly automatic, not workflow?
- [ ] Can this complete in <100ms (or appropriate budget)?
- [ ] Does this avoid hidden side effects?

**If any check fails:** Use CLI instead.

### 6.2 When Creating a New CLI

**Checklist:**
- [ ] Is this an explicit user workflow action?
- [ ] Does this need clear success/failure feedback?
- [ ] Should this be idempotent?
- [ ] Might this be used in scripts or automation?
- [ ] Does this modify state transactionally?
- [ ] Is this an information lookup or diagnostic?

**If any check passes:** CLI is appropriate.

### 6.3 Migration Path from Hook to CLI

If you have an existing hook that should be a CLI:

1. **Create CLI command** with same functionality
2. **Update CLAUDE.md** to instruct agents to use CLI
3. **Disable hook** (rename to .disabled)
4. **Monitor** for issues during transition
5. **Remove hook** after confidence period

---

## 7. Summary

### The Golden Rules

1. **Hooks are infrastructure, not logic.**
   - Create environment (SessionStart)
   - Enforce safety (PreToolUse)
   - Clean up crashes (SessionEnd)

2. **CLI commands are workflow, not infrastructure.**
   - Explicit actions (claim, complete)
   - Information lookup (list, show)
   - Maintenance operations (cleanup, validate)

3. **If an agent can do it, don't use a hook.**
   - Timeline updates? Agent does it.
   - State synchronization? Agent does it.
   - Documentation validation? Agent does it.

4. **If it can't block, don't use it for enforcement.**
   - Stop hooks cannot block - don't validate in them
   - SessionStart cannot block - only initialize

5. **Prefer explicit over implicit.**
   - `bb5 claim TASK-001` > magic task claiming
   - `bb5 validate-docs` > hidden validation

### Quick Reference

| Question | Hook | CLI |
|----------|------|-----|
| Must happen automatically? | Yes | No |
| Must block dangerous actions? | Yes (PreToolUse) | No |
| Needs explicit user intent? | No | Yes |
| Is part of normal workflow? | No | Yes |
| Needs clear feedback? | No | Yes |
| Agent can do it instead? | No | Yes |

---

## Appendix: BB5 Operation Classification

### Confirmed CLI Commands
- `bb5 claim TASK-001` - Task claiming
- `bb5 task:list`, `bb5 task:show`, `bb5 task:current` - Task queries
- `bb5 goal:list`, `bb5 goal:show` - Goal queries
- `bb5 plan:list`, `bb5 plan:show` - Plan queries
- `bb5 link:goal`, `bb5 link:plan` - Linking operations
- `bb5 goto`, `bb5 up`, `bb5 down`, `bb5 root` - Navigation
- `bb5 validate-docs` - Documentation validation
- `bb5 health` - System health check
- `bb5 timeline` - Timeline operations
- `bb5 create` - Goal/plan/task creation

### Confirmed Hooks
- `SessionStart` - Run folder creation, context loading
- `PreToolUse` - Safety enforcement, dangerous command blocking
- `Stop` - Session notification, cleanup (non-blocking)
- `SessionEnd` - Final archive (non-blocking)
- `PreCompact` - Context preservation
- `UserPromptSubmit` - Intent validation (exit warnings)

### To Be Determined
- Queue integrity validation (recommend: CLI)
- State synchronization (recommend: CLI)
- Metrics collection (recommend: CLI + cron)
- Orphaned task cleanup (recommend: CLI)
- Skill metrics logging (recommend: CLI called by agent)

---

*Document based on analysis in:*
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/hook-research/FIRST_PRINCIPLES_HOOKS.md`
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/hook-research/TASK_CLAIM_HOOK_DESIGN.md`
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/hook-reviews/TASK_CLAIM_ALTERNATIVES.md`
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/hook-research/OPERATIONS_HOOKS.md`
