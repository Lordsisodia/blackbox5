# SessionStart Hook - First Principles Analysis

**Date:** 2026-02-06
**Purpose:** Determine what actually needs to happen in BB5's SessionStart hook
**Research Sources:** 5 systems analyzed (BB5, ralph-loop, juno-code, SWE-agent, Claude Code native)

---

## The Core Question

What are the fundamental needs of an agent starting work, regardless of whether it's manual (user-driven) or autonomous (RALF-driven)?

---

## First Principles Breakdown

### Principle 1: An Agent Needs Identity

**The Problem:** An agent must know its role to act appropriately.

**What we found across systems:**
- **BB5:** Detects planner/executor/architect from path, files, git branch
- **Ralph Loop:** Always "orchestrator" - single agent type
- **Juno-Code:** Defined by config.json - user-configurable
- **SWE-agent:** Python class inheritance - developer-defined
- **Claude Code:** No native concept - hook must provide

**First Principles Need:**
The agent must answer: "Who am I and what is my purpose?"

**For BB5 Dual-Purpose:**
- Manual: Detect from context (am I in a task directory? am I planning?)
- Autonomous: Read from plan-state.json (I'm iteration 5 of the orchestrator)
- Both: Provide fallback to "developer" mode if unclear

---

### Principle 2: An Agent Needs Context

**The Problem:** An agent must know what it's working on.

**What we found across systems:**
- **BB5:** Loads queue status, claimed task details, goal progress
- **Ralph Loop:** Loads ledger (session history), handoffs (transfers), plan-state
- **Juno-Code:** Loads init.md prompt, config.json settings
- **SWE-agent:** Loads ProblemStatement, trajectory (conversation history)
- **Claude Code:** Native transcript persistence

**First Principles Need:**
The agent must answer: "What is the current state of the world?"

**For BB5 Dual-Purpose:**
- Manual: Current task (if any), project state, recent activity
- Autonomous: Full plan state, current step, barriers, loop iteration
- Both: Project structure, available commands, relevant memories

---

### Principle 3: An Agent Needs Task Clarity

**The Problem:** An agent must know what to do right now.

**What we found across systems:**
- **BB5:** Shows claimed task with acceptance criteria
- **Ralph Loop:** Shows current plan step with next actions
- **Juno-Code:** init.md contains task description
- **SWE-agent:** ProblemStatement defines the issue to solve
- **Claude Code:** User prompt provides intent

**First Principles Need:**
The agent must answer: "What should I do right now?"

**For BB5 Dual-Purpose:**
- Manual: User will provide intent in their first message (minimal task context OK)
- Autonomous: Must load current step from plan-state (comprehensive task context required)
- Both: Show available commands and how to get started

---

### Principle 4: An Agent Needs Environment Setup

**The Problem:** An agent needs a workspace to operate in.

**What we found across systems:**
- **BB5:** Creates run folder with THOUGHTS.md, RESULTS.md, etc.
- **Ralph Loop:** Initializes agent memory buffers (semantic/episodic/working)
- **Juno-Code:** Sets working directory, loads hooks config
- **SWE-agent:** Installs tools, sets up environment
- **Claude Code:** Native working directory

**First Principles Need:**
The agent must answer: "Where do I work and what tools do I have?"

**For BB5 Dual-Purpose:**
- Manual: Run folder for documentation, BB5 CLI tools available
- Autonomous: Run folder + memory buffers + event bus connection
- Both: Working directory validated, required files created

---

### Principle 5: An Agent Needs Navigation Guidance

**The Problem:** An agent needs to know how to proceed.

**What we found across systems:**
- **BB5:** Shows bb5 commands (whereami, task:status, etc.)
- **Ralph Loop:** Shows next steps from plan, claude-mem hints
- **Juno-Code:** Command reference in context
- **SWE-agent:** Tool descriptions in system prompt
- **Claude Code:** Native slash commands

**First Principles Need:**
The agent must answer: "How do I get started?"

**For BB5 Dual-Purpose:**
- Manual: Simple command reference, suggest first action
- Autonomous: Next step from plan, barrier status, agent coordination info
- Both: Documentation links, help resources

---

## The Dual-Purpose Design Challenge

### What's Different Between Manual and Autonomous?

| Aspect | Manual | Autonomous |
|--------|--------|------------|
| **Intent Source** | User's first message | plan-state.json current step |
| **Context Scope** | Current task only | Full plan + barriers + iterations |
| **State Tracking** | None | loop_state (current/max iteration) |
| **Memory** | User's memory | semantic/episodic/working buffers |
| **Checkpoints** | Not needed | Critical for compaction recovery |
| **Multi-Agent** | N/A | Agent handoffs, event bus |
| **Output Format** | Flexible text | Strict JSON (hookSpecificOutput) |

### What's the Same?

| Aspect | Both Need |
|--------|-----------|
| **Project Discovery** | Detect BB5 project structure |
| **Role Detection** | Know if planning/executing/architecting |
| **Workspace Setup** | Run folder with documentation files |
| **Command Reference** | Available bb5 commands |
| **Context Injection** | AGENT_CONTEXT.md or additionalContext |

---

## The Verdict: Can One Hook Serve Both?

**Answer: YES, with smart mode detection and modular loading.**

### Recommended Architecture

```
session-start-blackbox5.sh (entry point)
├── Step 1: Detect Mode
│   ├── Check for RALF_RUN_DIR → autonomous
│   ├── Check for plan-state.json → autonomous
│   ├── Check for .ralf-metadata → autonomous
│   └── Default → manual
│
├── Step 2: Load Shared Context (always)
│   ├── Detect project root
│   ├── Validate BB5 structure
│   ├── Detect agent type (planner/executor/architect)
│   └── Create run folder
│
├── Step 3: Load Mode-Specific Context
│   ├── IF autonomous:
│   │   ├── Load plan-state.json
│   │   ├── Restore from ledger (if post-compact)
│   │   ├── Initialize agent memory buffers
│   │   └── Load loop state
│   └── IF manual:
│       ├── Load current task (if claimed)
│       ├── Load recent activity
│       └── Simple project context
│
├── Step 4: Create Context Files
│   ├── THOUGHTS.md (template)
│   ├── RESULTS.md (template)
│   ├── DECISIONS.md (template)
│   ├── ASSUMPTIONS.md (template)
│   ├── LEARNINGS.md (template)
│   ├── metadata.yaml (structured data)
│   └── AGENT_CONTEXT.md (injected context)
│
└── Step 5: Output
    ├── Export environment variables
    └── Return JSON with additionalContext
```

### Key Design Decisions

1. **Fast Path for Manual:** Skip all autonomous checks if no RALF indicators present
2. **Progressive Enhancement:** Start with shared context, add mode-specific layers
3. **Self-Discovery:** No environment variables required, but use them if present
4. **Graceful Degradation:** If mode unclear, provide general BB5 context
5. **Unified Output:** Same JSON format for both modes (autonomous just has more data)

---

## Implementation Files

### Core Hook
- `.claude/hooks/session-start-blackbox5.sh` - Main dual-purpose hook

### Libraries
- `.claude/hooks/lib/detect-mode.sh` - Mode detection (manual/autonomous)
- `.claude/hooks/lib/shared-context.sh` - Common context loading
- `.claude/hooks/lib/manual-context.sh` - Manual session specifics
- `.claude/hooks/lib/autonomous-context.sh` - RALF loop specifics
- `.claude/hooks/lib/run-initializer.sh` - Run folder creation
- `.claude/hooks/lib/output-formatter.sh` - JSON output formatting

---

## Testing Strategy

### Manual Mode Tests
1. Start session in project root → Should detect developer mode
2. Start session in planner directory → Should detect planner
3. Start session with claimed task → Should load task context
4. Verify: No plan-state.json checks performed

### Autonomous Mode Tests
1. Start with RALF_RUN_DIR set → Should detect autonomous
2. Start with plan-state.json present → Should load plan state
3. Start post-compaction → Should restore from ledger
4. Verify: Full context loaded including loop state

### Both Modes Tests
1. Run folder created in both modes
2. All template files created in both modes
3. AGENT_CONTEXT.md populated in both modes
4. JSON output valid in both modes

---

## Comparison: What Others Do

### BB5 Current (session-start-blackbox5.sh)
- **Good:** Agent type detection, context loading, AGENT_CONTEXT.md
- **Missing:** Run folder creation, mode detection, autonomous support

### Ralph Loop (session-start-*.sh)
- **Good:** Ledger restoration, memory initialization, plan-state handling
- **Missing:** Generic enough for manual use (RALF-specific)

### Juno-Code (START_RUN)
- **Good:** Configurable, command-based
- **Missing:** Self-discovery (relies on config)

### SWE-agent (on_run_start)
- **Good:** Python class-based, extensible
- **Missing:** BB5-specific context

### Claude Code Native
- **Good:** Event system, JSON I/O
- **Missing:** Application logic (that's our job)

---

## BB5 Dual-Purpose Hook: What It Actually Does

### For Manual Users:
```
User opens Claude in BB5 project
        ↓
Hook detects: No RALF indicators → Manual mode
        ↓
Creates: runs/developer/run-{timestamp}/
        ↓
Loads: Project context, current task (if any), recent activity
        ↓
Creates: THOUGHTS.md, RESULTS.md, DECISIONS.md, etc.
        ↓
Injects: "You're in developer mode. Current task: X. Available commands: ..."
        ↓
User starts typing their request
```

### For Autonomous RALF:
```
RALF loop controller spawns agent
        ↓
Hook detects: RALF_RUN_DIR set → Autonomous mode
        ↓
Creates: runs/orchestrator/run-{timestamp}/
        ↓
Loads: plan-state.json, loop state, ledger, agent memory
        ↓
Restores: Context from previous iteration (if post-compact)
        ↓
Creates: THOUGHTS.md, RESULTS.md, DECISIONS.md, etc.
        ↓
Injects: "Iteration 5/25. Current step: Implement X. Barriers: Y. Next actions: ..."
        ↓
Agent proceeds with plan step
```

---

## Key Insight

The SessionStart hook is about **context reconstruction**. Whether manual or autonomous, the agent needs to reconstruct its understanding of:
1. Who it is (identity)
2. Where it is (project)
3. What it's doing (task)
4. How to proceed (navigation)

The difference is only in **where that context comes from**:
- Manual: User will provide intent, minimal setup needed
- Autonomous: Must load from plan-state, comprehensive setup required

A well-designed dual-purpose hook detects the mode and loads the appropriate context level.

---

## Next Steps

1. **Review this analysis** - Does this align with your understanding?
2. **Approve the dual-purpose approach** - One hook with mode detection?
3. **Prioritize implementation** - Start with shared context, add mode-specific layers?
4. **Define mode detection rules** - What exactly triggers autonomous vs manual?

Once you approve, I'll create the implementation task with full specifications.
