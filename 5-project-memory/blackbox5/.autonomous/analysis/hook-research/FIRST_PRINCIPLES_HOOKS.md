# BB5 Hooks: First Principles Design

**Date:** 2026-02-06
**Author:** First Principles Architect
**Status:** Analysis Document

---

## 1. First Principles Breakdown

### What is BB5 Fundamentally Trying to Do?

Strip away all assumptions. At its core, BB5 is:

1. **A task execution system** - Run AI agents on real work
2. **A memory system** - Remember what happened across sessions
3. **An improvement system** - Get better over time through feedback
4. **A coordination system** - Multiple agents working together

That's it. Everything else is implementation detail.

### What Are the Irreducible Requirements?

From first principles, BB5 needs:

| Requirement | Why It Exists | Minimum Need |
|-------------|---------------|--------------|
| **Context** | Agent needs to know what to do | Current task, relevant history |
| **Recording** | System needs to know what was done | What changed, what was learned |
| **Coordination** | Multiple agents must not conflict | Who is doing what, when |
| **Consistency** | State must be trustworthy | Single source of truth for task status |

### What Can Be Done Without Hooks?

Most of BB5's functionality does NOT require hooks:

- **Task execution** - Agent reads task file, does work, updates task file
- **Documentation** - Agent writes to THOUGHTS.md, RESULTS.md directly
- **Learning capture** - Agent appends to LEARNINGS.md before exiting
- **Git operations** - Agent runs git commands as part of work
- **State updates** - Agent updates queue.yaml when claiming/completing tasks

**Key insight:** An agent with clear instructions can do all of this manually.

### What Actually Requires Hooks?

Only these things truly need hooks:

1. **Session initialization** - Create run folder before agent starts working
2. **Safety enforcement** - Block dangerous operations (rm -rf, force push)
3. **Cleanup on exit** - Archive run folder, update metadata when session ends

Everything else is convenience, not necessity.

---

## 2. Current Hook Inventory: Ruthless Audit

BB5 currently has **13 hooks** across 6 events. Let's audit each:

### SessionStart (2 hooks)

| Hook | Purpose | Essential? | Verdict |
|------|---------|------------|---------|
| `session-start-blackbox5.sh` | Create run folder, load context | Partially | Run folder creation is essential; context loading is convenience |
| `session-start-navigation.sh` | Discover hierarchy | No | Agent can run `bb5 whereami` itself |

**Analysis:**
- Run folder creation IS essential - agent needs a place to work
- Context loading is NOT essential - agent can read files directly
- Navigation discovery is NOT essential - agent can explore

**First Principles Reduction:** Keep run folder creation only.

### PreToolUse (3 hooks)

| Hook | Purpose | Essential? | Verdict |
|------|---------|------------|---------|
| `pre-tool-security.py` | Block dangerous commands | Yes | Safety cannot be left to agent |
| `pre-tool-validation.sh` | Validate file structure | No | Agent can validate itself |
| `architecture-consistency.sh` | Enforce naming conventions | No | Convention enforcement is nice-to-have |

**Analysis:**
- Security IS essential - agents make mistakes, safety must be enforced
- Structure validation is NOT essential - agent knows what it's writing
- Naming conventions are NOT essential - consistency is preference, not requirement

**First Principles Reduction:** Keep security hook only.

### PostToolUse (2 hooks)

| Hook | Purpose | Essential? | Verdict |
|------|---------|------------|---------|
| `timeline-maintenance.sh` | Auto-update timeline | No | Agent can update timeline when milestones reached |
| `context-synchronization.sh` | Sync goal progress | No | Agent updates goal when completing task |

**Analysis:**
- Both hooks are reactive automation
- Agent knows when milestones happen - can update timeline directly
- Agent knows when tasks complete - can update goals directly
- These hooks add complexity for marginal convenience

**First Principles Reduction:** Eliminate both. Agent handles updates.

### SubagentStart/Stop (1 hook)

| Hook | Purpose | Essential? | Verdict |
|------|---------|------------|---------|
| `subagent-tracking.sh` | Log agent lifecycle | No | Agent can log its own lifecycle |

**Analysis:**
- Tracking is useful for coordination
- BUT agent can write to events.yaml when spawning/completing
- Hook adds complexity for centralized logging

**First Principles Reduction:** Eliminate. Agent self-reports.

### Stop (2 hooks)

| Hook | Purpose | Essential? | Verdict |
|------|---------|------------|---------|
| `stop-validate-docs.sh` | Validate documentation | No | Stop hooks cannot block (see analysis below) |
| `stop-hierarchy-update.sh` | Update parent timelines | No | Agent should update parent before exiting |

**Analysis:**
- **Critical finding:** Stop hooks CANNOT block session end
- Stop hooks fire AFTER session ends - they can only clean up
- Documentation validation must happen BEFORE exit, not after
- Parent timeline updates should happen when task completes, not at session stop

**First Principles Reduction:** Eliminate both. They create false sense of enforcement.

### SessionEnd (1 hook)

| Hook | Purpose | Essential? | Verdict |
|------|---------|------------|---------|
| `session-end-context-update.sh` | Context cleanup | Partially | Cleanup is needed, but can be minimal |

**Analysis:**
- SessionEnd fires after Stop
- Useful for final cleanup, archiving
- BUT most cleanup should happen when task completes, not at session end

**First Principles Reduction:** Keep minimal cleanup only.

---

## 3. The Minimum Viable Hook System

### The 3-Hook System

From first principles, BB5 needs exactly **3 hooks**:

```
┌─────────────────────────────────────────────────────────────┐
│                    MINIMUM VIABLE HOOKS                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. SessionStart: Initialize Run Folder                     │
│     - Create run-YYYYMMDD_HHMMSS/ directory                 │
│     - Create template files (THOUGHTS.md, RESULTS.md)       │
│     - Set RALF_RUN_DIR environment variable                 │
│                                                             │
│  2. PreToolUse: Safety Enforcement                          │
│     - Block rm -rf / dangerous patterns                     │
│     - Block git push --force                                │
│     - Block .env file exposure                              │
│     - Exit code 2 = block, 0 = allow                        │
│                                                             │
│  3. SessionEnd: Archive Run Folder                          │
│     - Move run folder to runs/completed/                    │
│     - Update metadata with end timestamp                    │
│     - Git commit run folder (optional)                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Why These Three?

| Hook | Irreducible Purpose |
|------|---------------------|
| **SessionStart** | Agent needs a workspace before it can work |
| **PreToolUse** | Safety cannot be optional - must be enforced |
| **SessionEnd** | Cleanup must happen even if agent crashes |

### What Each Hook Must Do (and NOT Do)

#### SessionStart Hook

**MUST do:**
- Create unique run directory
- Create minimal template files (THOUGHTS.md, RESULTS.md)
- Export RALF_RUN_DIR for agent to use

**MUST NOT do:**
- Load agent context (agent does this)
- Detect agent type (agent knows what it is)
- Discover hierarchy (agent explores)
- Complex initialization (keep it fast)

```bash
# Minimum viable SessionStart
#!/bin/bash
RUN_DIR="$PROJECT_ROOT/runs/run-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$RUN_DIR"
echo "# Run $(basename $RUN_DIR)" > "$RUN_DIR/THOUGHTS.md"
echo "# Results" > "$RUN_DIR/RESULTS.md"
export RALF_RUN_DIR="$RUN_DIR"
```

#### PreToolUse Hook

**MUST do:**
- Read tool_name and tool_input from stdin
- Check against dangerous patterns
- Exit 2 to block, 0 to allow

**MUST NOT do:**
- Validate file structure (not safety)
- Check naming conventions (not safety)
- Log tool usage (PostToolUse can do this if needed)
- Be agent-aware (security rules apply to all)

```python
# Minimum viable PreToolUse
import sys, json

data = json.load(sys.stdin)
tool = data.get('tool_name', '')
input_data = data.get('tool_input', {})

# Block dangerous operations
if tool == 'Bash':
    cmd = input_data.get('command', '')
    if 'rm -rf /' in cmd or 'rm -rf ~' in cmd:
        print("Blocked: dangerous rm command", file=sys.stderr)
        sys.exit(2)
    if 'git push --force' in cmd:
        print("Blocked: force push", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
```

#### SessionEnd Hook

**MUST do:**
- Find the run folder (from RALF_RUN_DIR or most recent)
- Move to completed/ directory
- Update metadata with end time

**MUST NOT do:**
- Validate documentation (too late - session ended)
- Update parent timelines (agent should do this)
- Sync queue state (agent should do this)
- Block or warn (session already ended)

```bash
# Minimum viable SessionEnd
#!/bin/bash
RUN_DIR="${RALF_RUN_DIR:-$(find_runs_dir)}"
if [ -d "$RUN_DIR" ]; then
    COMPLETED_DIR="$(dirname $RUN_DIR)/completed"
    mkdir -p "$COMPLETED_DIR"
    mv "$RUN_DIR" "$COMPLETED_DIR/"
fi
exit 0
```

---

## 4. What We Should Cut/Eliminate

### Immediate Cuts (High Confidence)

| Hook | Reason for Elimination |
|------|------------------------|
| `session-start-navigation.sh` | Agent can navigate itself |
| `pre-tool-validation.sh` | Agent validates its own work |
| `architecture-consistency.sh` | Conventions are guidelines, not requirements |
| `timeline-maintenance.sh` | Agent updates timeline at milestones |
| `context-synchronization.sh` | Agent syncs state when completing tasks |
| `subagent-tracking.sh` | Agent logs its own lifecycle |
| `stop-validate-docs.sh` | Cannot block; validation must be pre-exit |
| `stop-hierarchy-update.sh` | Agent updates parent before exiting |
| `session-end-context-update.sh` | Redundant with SessionEnd archive |

### Why These Can Be Eliminated

**Navigation/Discovery Hooks:**
- Agent has `bb5` CLI commands
- Agent can explore filesystem
- Self-discovery is more robust than hook-injected context

**Validation/Consistency Hooks:**
- Agent knows what it's writing
- Structure validation is the agent's responsibility
- Pre-tool validation adds latency for marginal benefit

**Reactive Update Hooks (PostToolUse):**
- Agent knows when milestones happen
- Reactive updates create race conditions
- Agent-driven updates are more reliable

**Stop Hooks (except minimal archive):**
- Stop hooks fire AFTER session ends
- Cannot block or prevent exit
- Any validation must happen before user types "exit"

---

## 5. Philosophical Stance on Hook Complexity

### The Hook Complexity Trap

BB5 fell into a common trap: **using hooks for convenience rather than necessity**.

Each hook added seemed useful:
- "Let's auto-update the timeline"
- "Let's validate documentation on stop"
- "Let's track subagent lifecycle"

But collectively they create:
- **Fragility** - More hooks = more failure points
- **Obscurity** - Magic behavior agents don't understand
- **Coupling** - Hooks assume specific directory structures
- **False security** - Stop hooks can't actually enforce

### The First Principles Stance

**Hooks should only do what agents cannot do themselves.**

Agents CAN:
- Read context files
- Write documentation
- Update timelines
- Sync state
- Validate their own work
- Log their lifecycle

Agents CANNOT:
- Create their run folder before existing
- Enforce safety policies on themselves
- Run cleanup after they crash

### Minimalism is Robustness

A 3-hook system is:
- **Understandable** - Developers can reason about it
- **Testable** - Fewer interactions to verify
- **Maintainable** - Less code to break
- **Portable** - Easier to adapt to other projects

---

## 6. Migration Path: From 13 Hooks to 3

### Phase 1: Disable Non-Essential Hooks (Immediate)

```bash
# Rename non-essential hooks to .disabled
mv session-start-navigation.sh session-start-navigation.sh.disabled
mv pre-tool-validation.sh pre-tool-validation.sh.disabled
mv architecture-consistency.sh architecture-consistency.sh.disabled
mv timeline-maintenance.sh timeline-maintenance.sh.disabled
mv context-synchronization.sh context-synchronization.sh.disabled
mv subagent-tracking.sh subagent-tracking.sh.disabled
mv stop-validate-docs.sh stop-validate-docs.sh.disabled
mv stop-hierarchy-update.sh stop-hierarchy-update.sh.disabled
mv session-end-context-update.sh session-end-context-update.sh.disabled
```

### Phase 2: Update Agent Prompts (Short-term)

Add to RALF prompt:
```markdown
## Responsibilities Previously Handled by Hooks

You are now responsible for:

1. **Timeline Updates** - When you reach a milestone, update timeline.yaml
2. **State Synchronization** - When you complete a task, update queue.yaml and move to completed/
3. **Documentation Validation** - Before exiting, verify THOUGHTS.md and RESULTS.md are complete
4. **Parent Updates** - When completing work, update parent goal/plan status
```

### Phase 3: Simplify Remaining Hooks (Medium-term)

- Reduce `session-start-blackbox5.sh` to folder creation only
- Reduce `pre-tool-security.py` to core safety rules only
- Reduce `session-end-context-update.sh` to archive only

### Phase 4: Document the New Contract (Long-term)

Update HOOKS.md to reflect the 3-hook philosophy:
- What hooks do (minimal)
- What agents do (everything else)
- Why this separation exists

---

## 7. Addressing Counter-Arguments

### "But agents forget to update state!"

**Response:** That's a prompt/training issue, not a hook issue.
- Improve the prompt to emphasize state updates
- Add explicit checklists in THOUGHTS.md template
- Use validation in the agent's own workflow

Hooks that "fix" agent forgetfulness mask the real problem.

### "But reactive updates are more reliable!"

**Response:** Reactive updates create race conditions and hidden dependencies.
- Agent-driven updates are explicit and testable
- Reactive hooks fire on patterns that might change
- Debugging is harder when logic is split between agent and hooks

### "But stop hooks validate before exit!"

**Response:** Stop hooks fire AFTER the session has ended.
- User types "exit"
- Session terminates
- Stop hook fires (too late to block)
- User is already back at shell

Validation must happen in the agent's workflow, not at stop.

### "But 13 hooks give us more control!"

**Response:** More hooks = more complexity, not more control.
- Control comes from clear contracts, not automation
- Hooks that agents don't understand create magic behavior
- Simpler systems are easier to control and reason about

---

## 8. Conclusion

### The Essential Truth

BB5 hooks should be **infrastructure**, not **logic**.

- **Infrastructure** creates the environment (run folder, safety, cleanup)
- **Logic** does the work (updates, validation, synchronization)

Current BB5 blurs this line. Hooks do logic that agents should do.

### The Minimum Viable System

**3 hooks:**
1. SessionStart - Create workspace
2. PreToolUse - Enforce safety
3. SessionEnd - Archive workspace

**Everything else:** Agent responsibility

### The Ruthless Bottom Line

If an agent can do it, the hook shouldn't.

If a hook can't actually enforce (like Stop hooks), don't pretend it can.

If it feels like convenience, it probably isn't essential.

---

## Appendix: Hook Decision Framework

When considering a new hook, ask:

| Question | If Yes | If No |
|----------|--------|-------|
| Can the agent do this itself? | Don't add hook | Consider hook |
| Does this enforce safety? | Add hook | Don't add for convenience |
| Does this create the environment? | Add hook | Don't add for logic |
| Does this clean up after crashes? | Add hook | Don't add for normal flow |
| Can this actually block/prevent? | Add as PreToolUse | Don't add as Stop hook |

**Default position:** Reject. Require justification.

---

*Document written from first principles. Strip away assumptions. Keep only the essential.*
