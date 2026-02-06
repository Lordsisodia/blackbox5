# Task Claim Hook: Alternative Approaches Analysis

**Status:** Review Complete
**Analyst:** Solutions Architect
**Date:** 2026-02-06
**Original Design:** /Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/hook-research/TASK_CLAIM_HOOK_DESIGN.md

---

## Executive Summary

**Verdict: The TaskClaim hook is a bad idea. Use Option B (CLI-driven) instead.**

The proposed TaskClaim hook attempts to solve a real problem (automatic task context setup) but uses the wrong mechanism. Hooks should be reserved for lifecycle events that the agent cannot control, not for workflow operations that the agent or user should explicitly trigger.

---

## 1. Fundamental Questions

### 1.1 Is a hook the right solution for this problem?

**No.**

Hooks are appropriate when:
- The event is outside agent control (session start/end)
- Automatic validation is needed (stop conditions)
- Cross-cutting concerns need enforcement (logging, metrics)

Hooks are **inappropriate** when:
- The action is part of normal workflow (claiming a task)
- User intent needs to be explicitly captured
- State changes need to be transactional

Task claiming is a **deliberate workflow action**, not a lifecycle event. It should be explicit, not automatic.

### 1.2 Could this be done in the agent prompt instead?

**Partially, but insufficient.**

The existing CLAUDE.md already instructs agents to:
- Use `bb5 task:list` to see pending tasks
- Use `bb5 task:current` to see current task
- Create run folders with required files
- Read task files completely before starting

**The problem is not lack of instructions—it's lack of enforcement and automation.**

Adding more prompt text won't solve the friction of:
- Manually creating run folders
- Copying templates
- Setting up context files
- Updating queue status

### 1.3 Could this be a CLI command (`bb5 claim`) rather than a hook?

**Yes. This is the correct approach.**

A CLI command provides:
- Explicit user intent ("I want to claim this task")
- Clear success/failure feedback
- Transactional state changes
- Idempotent operations (can check if already claimed)
- Better error handling

### 1.4 Should this be part of SessionStart instead?

**No.**

SessionStart should remain focused on:
- Loading project context
- Setting up environment
- Discovering current location

Adding task claiming to SessionStart would:
- Violate single responsibility principle
- Make sessions slower (loading task hierarchy)
- Create ambiguity (what if user doesn't want to claim?)
- Complicate session restoration

---

## 2. Alternative Approaches

### Option A: Agent-Driven (Agent Creates Folder Itself)

**Description:** The agent follows existing CLAUDE.md instructions to manually create run folders and load task context.

**Implementation:**
- Agent reads task file
- Agent creates run folder structure
- Agent populates THOUGHTS.md, etc.
- Agent updates queue.yaml manually

**Pros:**
- No new infrastructure needed
- Agent has full control
- Flexible to task-specific needs

**Cons:**
- Repetitive boilerplate (violates DRY)
- Inconsistent execution (different agents do it differently)
- Error-prone (easy to forget steps)
- Time-consuming (manual context loading)

**Verdict:** Status quo. Works but inefficient.

---

### Option B: CLI-Driven (`bb5 claim TASK-001`) **RECOMMENDED**

**Description:** User or agent runs a CLI command to claim a task. The command handles all setup atomically.

**Implementation:**
```bash
bb5 claim TASK-001
```

**What it does:**
1. Validates task exists and is claimable
2. Creates run folder: `runs/run-YYYYMMDD-HHMMSS-TASK-001/`
3. Generates THOUGHTS.md with full context (goal → plan → task hierarchy)
4. Creates DECISIONS.md, ASSUMPTIONS.md, LEARNINGS.md, RESULTS.md
5. Updates queue.yaml: marks task as "claimed", sets claimed_by, claimed_at
6. Outputs: "Task TASK-001 claimed. Run folder: runs/run-YYYYMMDD-HHMMSS-TASK-001/"
7. Changes to the run directory

**Pros:**
- **Explicit intent** - Clear user action
- **Atomic operation** - All-or-nothing setup
- **Idempotent** - Can check if already claimed, prevent double-claim
- **Better errors** - Clear feedback if task doesn't exist or is blocked
- **Composable** - Can be used in scripts, aliases
- **Familiar** - Matches git checkout, npm install, etc.
- **Testable** - Easy to unit test CLI behavior

**Cons:**
- Requires user to remember command
- One more CLI command to maintain

**Mitigation:**
- Add to bb5 help text prominently
- Auto-suggest when agent lists tasks
- Add shell alias: `claim='bb5 claim'`

**Verdict:** Best approach. Explicit, reliable, maintainable.

---

### Option C: File-Watcher (Detect `.claim-request` Files)

**Description:** Agent creates an empty file `.claim-request` in task directory. A file watcher detects it and triggers setup.

**Implementation:**
```bash
touch tasks/active/TASK-001/.claim-request
# File watcher detects and processes
```

**Pros:**
- Simple trigger mechanism
- Works across different interfaces

**Cons:**
- **Hidden magic** - User doesn't see what happens
- **Race conditions** - What if two agents claim simultaneously?
- **No feedback** - Silent failure modes
- **Complex infrastructure** - Needs file watcher daemon
- **Hard to debug** - Invisible trigger mechanism
- **Platform issues** - File watching is OS-specific

**Verdict:** Over-engineered. Avoid.

---

### Option D: SessionStart Enhancement (Detect Task Context)

**Description:** SessionStart hook detects if session is starting in a task directory and auto-loads context.

**Implementation:**
- SessionStart checks `pwd`
- If in `tasks/active/TASK-XXX/`, loads task context
- Creates run folder if needed

**Pros:**
- Zero user action required
- Automatic context loading

**Cons:**
- **Too magical** - User may not want to claim task
- **Side effects** - Starting session != claiming task
- **Ambiguity** - What if I just want to look at a task?
- **Violates explicitness** - Hidden state changes
- **Hard to override** - How do I start session WITHOUT claiming?

**Verdict:** Violates principle of least surprise. Avoid.

---

### Option E: No Hook At All (Improve Prompts)

**Description:** Rely solely on CLAUDE.md instructions without any automation.

**Implementation:**
- Enhance CLAUDE.md with clearer task claiming instructions
- Add checklist for manual setup
- Trust agents to follow procedure

**Pros:**
- Zero code to maintain
- Maximum flexibility

**Cons:**
- **Doesn't solve the problem** - Friction remains
- **Inconsistent execution** - Humans forget steps
- **Wasted time** - Repetitive manual work
- **Documentation drift** - Instructions get stale

**Verdict:** Insufficient. The problem is real and needs tooling.

---

## 3. Comparison Matrix

| Criteria | Option A (Agent) | Option B (CLI) | Option C (Watcher) | Option D (Session) | Option E (Prompts) |
|----------|------------------|----------------|--------------------|--------------------|--------------------|
| **Complexity** | Low | Low | High | Medium | Lowest |
| **Reliability** | Medium | High | Low | Medium | Low |
| **User Experience** | Poor | Good | Poor | Fair | Poor |
| **Maintenance Burden** | Low | Low | High | Medium | Lowest |
| **Performance** | N/A | Fast | Slow (polling) | Fast | N/A |
| **Explicitness** | Medium | High | Low | Low | Medium |
| **Testability** | Hard | Easy | Hard | Hard | N/A |
| **Debuggability** | Hard | Easy | Very Hard | Hard | Hard |
| **Idempotency** | No | Yes | No | No | N/A |
| **Error Handling** | Poor | Good | Poor | Poor | Poor |

**Scoring:**
- Option A: 5/10 - Works, but inefficient
- **Option B: 9/10 - Best balance of all factors**
- Option C: 2/10 - Over-engineered, fragile
- Option D: 4/10 - Too magical, violates explicitness
- Option E: 3/10 - Doesn't solve the problem

---

## 4. Recommendation

### 4.1 Primary Recommendation: Implement Option B (CLI-Driven)

**Implement `bb5 claim TASK-001` command.**

**Why this is better than the hook approach:**

1. **Explicit over Implicit**
   - Hook: "Did I claim the task? When did that happen?"
   - CLI: "I ran `bb5 claim TASK-001` and got confirmation."

2. **Transactional Safety**
   - Hook: Partial failures leave system in inconsistent state
   - CLI: All-or-nothing operation with rollback on error

3. **Better Error Handling**
   - Hook: Silent failures or cryptic hook errors
   - CLI: Clear error messages: "Task TASK-001 not found", "Task already claimed by run-XXX"

4. **Idempotency**
   - Hook: May trigger multiple times accidentally
   - CLI: Can check state and prevent double-claim

5. **User Control**
   - Hook: Happens whether user wants it or not
   - CLI: User decides when to claim

6. **Debugging**
   - Hook: Invisible execution, hard to trace
   - CLI: Clear command history, reproducible

7. **Composability**
   - Hook: Tied to specific trigger mechanism
   - CLI: Can script, alias, integrate with other tools

### 4.2 Implementation Sketch

```bash
#!/bin/bash
# bb5-claim - Claim a task and set up run environment

TASK_ID="$1"
PROJECT_ROOT="/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5"
TASKS_DIR="$PROJECT_ROOT/tasks/active"
QUEUE_FILE="$PROJECT_ROOT/.autonomous/agents/communications/queue.yaml"

# Validation
if [ -z "$TASK_ID" ]; then
    echo "Usage: bb5 claim TASK-XXX"
    exit 1
fi

TASK_DIR="$TASKS_DIR/$TASK_ID"
if [ ! -d "$TASK_DIR" ]; then
    echo "Error: Task $TASK_ID not found"
    exit 1
fi

# Check if already claimed (idempotency)
if grep -q "task_id: $TASK_ID" "$QUEUE_FILE" 2>/dev/null; then
    CLAIMED_BY=$(grep -A5 "task_id: $TASK_ID" "$QUEUE_FILE" | grep "claimed_by:" | awk '{print $2}')
    if [ -n "$CLAIMED_BY" ] && [ "$CLAIMED_BY" != "null" ]; then
        echo "Error: Task $TASK_ID already claimed by $CLAIMED_BY"
        echo "Use 'bb5 claim --force $TASK_ID' to override"
        exit 1
    fi
fi

# Create run folder
TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
RUN_ID="run-${TIMESTAMP}-${TASK_ID}"
RUN_DIR="$PROJECT_ROOT/runs/$RUN_ID"
mkdir -p "$RUN_DIR"

# Load hierarchy and generate THOUGHTS.md
# ... (parse task.md, find plan, find goal)

# Create documentation files
touch "$RUN_DIR/THOUGHTS.md"
touch "$RUN_DIR/DECISIONS.md"
touch "$RUN_DIR/ASSUMPTIONS.md"
touch "$RUN_DIR/LEARNINGS.md"
touch "$RUN_DIR/RESULTS.md"

# Update queue
# ... (mark task as claimed)

# Change to run directory
cd "$RUN_DIR"
echo "Claimed $TASK_ID. Run folder: $RUN_DIR"
```

### 4.3 Integration with Existing System

**CLAUDE.md Update:**
```markdown
## Task Claiming

To claim a task and set up your workspace:

```bash
bb5 claim TASK-XXX
```

This will:
- Create a run folder with all required documentation
- Load goal → plan → task hierarchy into context
- Mark task as claimed in the queue
- Change to the run directory
```

**Workflow:**
```
User: "bb5 claim TASK-001"
    |
    v
CLI validates task exists
    |
    v
CLI creates run folder
    |
    v
CLI generates THOUGHTS.md with context
    |
    v
CLI updates queue.yaml
    |
    v
CLI changes to run directory
    |
    v
Agent starts work with full context
```

### 4.4 Trade-offs Accepted

| Trade-off | Rationale |
|-----------|-----------|
| Requires explicit command | Explicitness prevents accidental claims |
| One more CLI command | Worth it for reliability and clarity |
| User must remember | Mitigated by prominent help text and aliases |

---

## 5. Conclusion

**Do not implement the TaskClaim hook. Implement `bb5 claim` CLI command instead.**

The hook approach violates the principle that workflow actions should be explicit, while the CLI approach provides the same benefits (automation, context loading) without the drawbacks (magic, fragility, poor error handling).

---

## Appendix: Why Hooks Are Wrong Here

### Hook Anti-Patterns Present in Original Design

1. **Intent Detection via Regex**
   - Parsing natural language is fragile
   - "claim TASK-001" vs "claim task TASK-001" vs "I want to claim..."
   - False positives and negatives inevitable

2. **Hidden Side Effects**
   - User says "claim TASK-001"
   - Hook creates folder, updates queue, changes directory
   - User may not realize all that happened

3. **Tight Coupling**
   - Hook must know about queue.yaml format
   - Hook must know about run folder structure
   - Hook must know about task hierarchy
   - Changes to any of these break the hook

4. **Poor Testability**
   - Testing hooks requires simulating Claude Code environment
   - Integration testing is complex
   - Unit testing is nearly impossible

5. **No Rollback**
   - If hook fails halfway, system is in inconsistent state
   - Partial folder creation
   - Partial queue update
   - Orphaned files

### CLI Benefits Reiterated

| Aspect | Hook | CLI |
|--------|------|-----|
| User Intent | Inferred | Explicit |
| Error Messages | Hidden in logs | Direct to terminal |
| Testing | Hard | Easy |
| Debugging | Trace through hook logs | Run command again |
| Rollback | Manual cleanup | Atomic transactions |
| Documentation | Must document hook behavior | Self-documenting |
| Composability | None | Scripts, aliases, pipes |

---

*Analysis complete. Recommendation: Implement Option B (CLI-driven task claiming).*
