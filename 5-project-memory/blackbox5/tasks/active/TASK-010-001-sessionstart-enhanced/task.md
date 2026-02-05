# TASK-010-001: SessionStart Enhanced Hook

**Goal:** IG-010 - Implement World-Class Hook System for BB5
**Plan:** PLAN-010 - BB5 Hook System Implementation
**Status:** pending
**Priority:** CRITICAL
**Created:** 2026-02-06
**Estimated Effort:** 4 hours

---

## Objective

Implement an enhanced SessionStart hook that combines the best of BB5's context loading with ralph-loop's run folder creation. This is the foundation of our hook system - it runs every time a session starts and sets up everything the agent needs.

---

## What This Hook Actually Does

### The Problem

When an agent starts working, it needs:
1. A place to store its work (run folder)
2. Required documentation files (THOUGHTS.md, RESULTS.md, etc.)
3. Context about what it's supposed to be doing
4. Access to relevant memories from past work
5. Environment variables for other hooks to use

**Without this hook:** Agents manually create folders, forget to create files, work without context, and can't find their previous work.

**With this hook:** Everything is set up automatically, consistently, every time.

---

## How It Works (Step-by-Step)

### Step 1: Self-Discovery (No Environment Variables Needed)

The hook figures out where it is and what project it's working on:

```bash
# Hook knows where it lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Discover project memory
PROJECT_MEMORY_DIR="$PROJECT_ROOT/5-project-memory"
PROJECT_NAME="blackbox5"  # Default, can be overridden
```

**Why this matters:** The hook doesn't need environment variables set. It discovers everything from the filesystem. This makes it robust and portable.

**Best practice from:** ralph-loop's self-discovering hooks

---

### Step 2: Agent Type Detection

The hook figures out what type of agent is running:

```bash
detect_agent_type() {
    local cwd="$(pwd)"

    # Method 1: Check run directory path
    if [[ "$cwd" == *"/planner/"* ]]; then
        echo "planner"
        return
    elif [[ "$cwd" == *"/executor/"* ]]; then
        echo "executor"
        return
    elif [[ "$cwd" == *"/architect/"* ]]; then
        echo "architect"
        return
    fi

    # Method 2: Check for agent-specific files
    if [ -f "queue.yaml" ]; then
        echo "planner"
        return
    elif [ -f ".task-claimed" ]; then
        echo "executor"
        return
    fi

    # Method 3: Check git branch name
    local git_branch="$(git branch --show-current 2>/dev/null || echo "")"
    if [[ "$git_branch" == *"planner"* ]]; then
        echo "planner"
        return
    fi

    # Default
    echo "unknown"
}
```

**Why this matters:** Different agents need different context. Planners need queue status. Executors need task details. Architects need goal information.

**Best practice from:** BB5's session-start-blackbox5.sh

---

### Step 3: Run Folder Creation

Creates the run directory structure:

```bash
RUN_TIMESTAMP=$(date +%Y%m%d-%H%M%S)
RUN_ID="run-$RUN_TIMESTAMP"
RUNS_DIR="$PROJECT_DIR/runs"
RUN_DIR="$RUNS_DIR/$AGENT_TYPE/$RUN_ID"

mkdir -p "$RUN_DIR"
```

**Directory structure created:**
```
runs/
├── planner/
│   └── run-20260206-143022/
├── executor/
│   └── run-20260206-143022/
└── architect/
    └── run-20260206-143022/
```

**Why this matters:** Every agent run gets its own folder. No overwriting. No confusion. Easy to find later.

**Best practice from:** ralph-loop's run initialization

---

### Step 4: Required File Creation

Creates all the files an agent needs to do its work:

```bash
# THOUGHTS.md - Agent reasoning and analysis
cat > "$RUN_DIR/THOUGHTS.md" << EOF
# THOUGHTS - Run $RUN_ID

**Project:** $PROJECT_NAME
**Agent:** $AGENT_TYPE
**Run ID:** $RUN_ID
**Started:** $TIMESTAMP

---

## State Assessment

### Current System Status
- **Active Tasks:**
- **Queue Depth:**
- **Previous Run Status:**

### Context
- **Git Branch:** $GIT_BRANCH
- **Git Commit:** $GIT_COMMIT

---

## Analysis

[Agent reasoning goes here]

---

## Next Steps

1.
2.
3.

---

*Hook-generated template. Edit as needed.*
EOF
```

**Files created:**
1. **THOUGHTS.md** - Where the agent thinks through problems
2. **RESULTS.md** - What was accomplished
3. **DECISIONS.md** - Key decisions made and why
4. **ASSUMPTIONS.md** - Assumptions being made
5. **LEARNINGS.md** - What was learned
6. **metadata.yaml** - Structured data about the run

**Why this matters:** Consistent documentation across all runs. Every agent follows the same pattern. No missing files.

**Best practice from:** BB5's data layer pattern + ralph-loop's template creation

---

### Step 5: Memory Loading

Loads relevant memories from the vector store:

```bash
# Search for memories related to current task
if [ -f "$RUN_DIR/../.current-task" ]; then
    CURRENT_TASK=$(cat "$RUN_DIR/../.current-task")

    # Query vector store for relevant memories
    python3 "$BB5_DIR/.autonomous/memory/hooks/session_memory_loader.py" \
        --task "$CURRENT_TASK" \
        --output "$RUN_DIR/RELEVANT_MEMORIES.md"
fi
```

**What this does:**
- Finds memories from past work on similar tasks
- Loads relevant decisions and learnings
- Injects them into the agent's context

**Why this matters:** Agents learn from past work. Don't repeat mistakes. Build on previous insights.

**Best practice from:** ralph-loop's smart-memory-search.sh

---

### Step 6: Context Injection

Creates AGENT_CONTEXT.md with everything the agent needs to know:

```bash
CONTEXT_FILE="$RUN_DIR/AGENT_CONTEXT.md"

cat > "$CONTEXT_FILE" << EOF
# Agent Context (Auto-Generated)

**Detected Agent Type:** $AGENT_TYPE
**Run Directory:** $RUN_DIR
**Timestamp:** $(date -Iseconds)

---

## Current Task

**Task ID:** $CLAIMED_TASK
**Task Title:** $TASK_TITLE

### Acceptance Criteria
$ACCEPTANCE_CRITERIA

---

## Queue Status

- Active Tasks: $ACTIVE_TASKS
- Completed Tasks: $COMPLETED_TASKS

---

## Available Commands

\`\`\`bash
bb5 whereami              # Show current location
bb5 task:status           # Check task status
bb5 task:complete         # Mark task complete
\`\`\`

---

*Context auto-generated by session-start-enhanced.sh*
EOF
```

**Why this matters:** The agent immediately knows what it's supposed to be doing. No confusion. No hunting for context.

**Best practice from:** BB5's session-start-blackbox5.sh

---

### Step 7: Environment Variable Export

Exports variables for other hooks to use:

```bash
# Export for current session
export RALF_RUN_DIR="$RUN_DIR"
export RALF_RUN_ID="$RUN_ID"
export RALF_PROJECT_ROOT="$PROJECT_ROOT"
export RALF_PROJECT_NAME="$PROJECT_NAME"
export RALF_AGENT_TYPE="$AGENT_TYPE"

# Persist for sub-processes
if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo "export RALF_RUN_DIR=$RUN_DIR" >> "$CLAUDE_ENV_FILE"
    echo "export RALF_RUN_ID=$RUN_ID" >> "$CLAUDE_ENV_FILE"
    echo "export RALF_AGENT_TYPE=$AGENT_TYPE" >> "$CLAUDE_ENV_FILE"
fi
```

**Why this matters:** Other hooks can use these variables. Consistent paths. No guessing.

**Best practice from:** ralph-loop's environment persistence

---

## JSON Output for Claude Code

The hook returns JSON that Claude Code uses:

```bash
OUTPUT=$(cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "You are running as a $AGENT_TYPE agent in the BlackBox5 system. Run directory: $RUN_DIR. Review AGENT_CONTEXT.md for your current task.",
    "agentType": "$AGENT_TYPE",
    "runId": "$RUN_ID",
    "runDir": "$RUN_DIR",
    "contextFile": "$CONTEXT_FILE"
  }
}
EOF
)

echo "$OUTPUT"
```

**What this does:** Injects context directly into Claude's system prompt. The AI immediately knows its role and context.

---

## Complete Hook Flow

```
SessionStart Triggered
        ↓
Step 1: Self-Discovery
  - Find project root
  - Discover project name
        ↓
Step 2: Agent Type Detection
  - Check path patterns
  - Check file patterns
  - Check git branch
        ↓
Step 3: Run Folder Creation
  - Create runs/{agent_type}/run-{timestamp}/
        ↓
Step 4: Required File Creation
  - THOUGHTS.md
  - RESULTS.md
  - DECISIONS.md
  - ASSUMPTIONS.md
  - LEARNINGS.md
  - metadata.yaml
        ↓
Step 5: Memory Loading
  - Query vector store
  - Load relevant memories
        ↓
Step 6: Context Injection
  - Create AGENT_CONTEXT.md
  - Load task details
  - Show queue status
        ↓
Step 7: Environment Export
  - Export RALF_RUN_DIR
  - Export RALF_RUN_ID
  - Export RALF_AGENT_TYPE
        ↓
Return JSON to Claude Code
```

---

## Files to Create

1. `.claude/hooks/session-start-enhanced.sh` - Main hook script
2. `.claude/hooks/lib/run-initializer.sh` - Shared library for run creation
3. `.claude/hooks/lib/agent-detector.sh` - Agent type detection library

---

## Testing

### Test 1: Basic Execution
```bash
# Start a new session
# Verify: Run folder created
# Verify: All files exist
# Verify: AGENT_CONTEXT.md populated
```

### Test 2: Agent Type Detection
```bash
# Test from planner directory
# Verify: Agent type = "planner"

# Test from executor directory
# Verify: Agent type = "executor"

# Test from unknown directory
# Verify: Agent type = "unknown"
```

### Test 3: Context Injection
```bash
# Start session with claimed task
# Verify: Task details in AGENT_CONTEXT.md
# Verify: Acceptance criteria loaded
```

### Test 4: Memory Loading
```bash
# Start session on similar task to previous
# Verify: RELEVANT_MEMORIES.md created
# Verify: Past learnings loaded
```

---

## Acceptance Criteria

- [ ] Run folder created automatically on session start
- [ ] All required files populated from templates
- [ ] Agent type detected correctly (planner/executor/architect/unknown)
- [ ] Context loaded from vector store
- [ ] Environment variables exported (RALF_RUN_DIR, RALF_RUN_ID, RALF_AGENT_TYPE)
- [ ] AGENT_CONTEXT.md created with task details
- [ ] JSON output returned to Claude Code
- [ ] Works for all agent types
- [ ] Self-discovering (no env vars required)
- [ ] Fails gracefully on errors

---

## Integration Points

**Calls:**
- `bb5-discover-context` - Get current context
- `bb5-whereami` - Show location
- `session_memory_loader.py` - Load relevant memories

**Called by:**
- `.claude/settings.json` - SessionStart event

**Provides context to:**
- All other hooks via environment variables
- Agent via AGENT_CONTEXT.md
- Claude Code via JSON output

---

## Best Practices Applied

1. **Self-Discovery** - No environment variables needed (from ralph-loop)
2. **Agent Detection** - Multiple detection methods (from BB5)
3. **Template Creation** - Consistent file structure (from BB5 + ralph-loop)
4. **Memory Loading** - Relevant context injection (from ralph-loop)
5. **Context Injection** - AGENT_CONTEXT.md pattern (from BB5)
6. **Environment Persistence** - CLAUDE_ENV_FILE usage (from Claude Code docs)

---

## Questions for Review

1. Should we support additional agent types beyond planner/executor/architect?
2. Should the hook detect if resuming a previous run vs starting fresh?
3. How much memory history should we load? Last 5? Last 10? All relevant?
4. Should we include git status in the context?
5. Should we check for uncommitted changes and warn?

---

## Next Steps After Implementation

1. Test with planner agent
2. Test with executor agent
3. Test with architect agent
4. Verify integration with SessionEnd hook
5. Document for hook developers

---

*This is the foundation hook. Everything else builds on this.*
