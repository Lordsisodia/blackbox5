# BB5 Architecture Analysis for SessionStart Hook

**Date:** 2026-02-06
**Purpose:** Deep dive into BB5 architecture to inform SessionStart hook design
**Research:** Multi-project support, context system, environment variables

---

## 1. BB5 Directory Structure

```
~/.blackbox5/
├── .autonomous/              # Global autonomous state
│   ├── communications/       # Global events, queue, heartbeat
│   ├── routes.yaml           # Global route configuration
│   └── goals.yaml            # Global goals index
├── .claude/                  # Claude Code hooks and settings
│   ├── hooks/                # 13 smart hooks
│   ├── settings.json         # Hook registration
│   └── HOOKS.md              # Hook documentation
├── 5-project-memory/         # Project workspaces (MULTI-PROJECT)
│   ├── _template/            # Project template
│   ├── blackbox5/            # Main BB5 project
│   ├── siso-internal/        # Internal project
│   └── team-entrepreneurship-memory/
├── bin/                      # CLI commands (bb5-*)
├── 2-engine/                 # RALF engine components
└── AGENT_CONTEXT.md          # Auto-generated context
```

**Key Insight:** BB5 already has infrastructure for multiple projects in `5-project-memory/`

---

## 2. Multi-Project Support

### Current State
- Multiple projects exist: `blackbox5/`, `siso-internal/`, etc.
- Most commands default to `blackbox5` (hardcoded)
- No `bb5 project:switch` command
- Each project has its own `routes.yaml`

### What SessionStart Hook Needs

1. **Project Detection:**
```bash
detect_current_project() {
    local cwd="$(pwd)"
    if [[ "$cwd" == *"5-project-memory/blackbox5"* ]]; then
        echo "blackbox5"
    elif [[ "$cwd" == *"5-project-memory/siso-internal"* ]]; then
        echo "siso-internal"
    else
        # Check for .bb5-project file
        if [ -f ".bb5-project" ]; then
            cat ".bb5-project"
        else
            echo "blackbox5"  # Default
        fi
    fi
}
```

2. **Project-Specific Context Loading:**
```bash
PROJECT=$(detect_current_project)
ROUTES_FILE="$BB5_DIR/5-project-memory/$PROJECT/.autonomous/context/routes.yaml"
GOALS_DIR="$BB5_DIR/5-project-memory/$PROJECT/goals/active"
QUEUE_FILE="$BB5_DIR/5-project-memory/$PROJECT/.autonomous/agents/communications/queue.yaml"
```

---

## 3. Project Memory Structure (Per Project)

Each project has:
```
project-name/
├── goals/active/IG-XXX/      # Goal hierarchy
│   ├── goal.yaml
│   ├── timeline.yaml
│   └── plans/                # Symlinks to linked plans
├── plans/active/             # Plan hierarchy
│   └── PLAN-NAME/
│       ├── plan.md
│       └── tasks/            # Symlinks to linked tasks
├── tasks/active/TASK-XXX/    # Task hierarchy
│   ├── task.md
│   ├── THOUGHTS.md
│   ├── RESULTS.md
│   └── DECISIONS.md
├── .autonomous/
│   ├── agents/               # Agent runs
│   │   ├── planner/runs/
│   │   ├── executor/runs/
│   │   └── communications/
│   │       ├── queue.yaml
│   │       ├── events.yaml
│   │       └── heartbeat.yaml
│   └── context/routes.yaml
├── runs/                     # Run folders
├── timeline.yaml             # Project timeline
└── STATE.yaml                # Project state
```

---

## 4. Context Discovery System

### How BB5 Discovers Context

The `bb5-discover-context` command uses **path pattern matching**:

```bash
# Check if in goals
if echo "$CWD" | grep -q "/goals/active/"; then
    CURRENT_TYPE="goal"
    CURRENT_ID="$(basename "$CURRENT_PATH")"
fi

# Check if in plans
if echo "$CWD" | grep -q "/plans/active/"; then
    CURRENT_TYPE="plan"
    # Find parent goal via symlinks
fi

# Check if in tasks
if echo "$CWD" | grep -q "/tasks/active/"; then
    CURRENT_TYPE="task"
    # Find parent plan via symlinks
fi
```

### For SessionStart Hook

The hook needs to:
1. Detect which project we're in
2. Detect where we are in the hierarchy (goal/plan/task)
3. Load appropriate context

---

## 5. Environment Variables

### Available to Hooks

| Variable | Source | Purpose |
|----------|--------|---------|
| `CLAUDE_PROJECT_DIR` | Claude Code | Project root path |
| `CLAUDE_ENV_FILE` | SessionStart only | File to persist env vars |
| `RALF_RUN_DIR` | RALF hooks | Current run directory |
| `RALF_RUN_ID` | RALF hooks | Run identifier |

### Setting Environment Variables (SessionStart Only)

```bash
# Only SessionStart hooks can set env vars for the session
if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo "export RALF_RUN_DIR=$RUN_DIR" >> "$CLAUDE_ENV_FILE"
    echo "export RALF_RUN_ID=$RUN_ID" >> "$CLAUDE_ENV_FILE"
    echo "export BB5_PROJECT=$PROJECT" >> "$CLAUDE_ENV_FILE"
fi
```

### Using Environment Variables (All Hooks)

```bash
# Use with fallback
RUN_DIR="${RALF_RUN_DIR:-$(pwd)}"
PROJECT="${BB5_PROJECT:-blackbox5}"

# Detect from filesystem if env var not set
if [ -z "$PROJECT" ]; then
    PROJECT=$(detect_current_project)
fi
```

---

## 6. Agent Type Detection

Current BB5 detection (from session-start-blackbox5.sh):

```bash
detect_agent_type() {
    local cwd="$(pwd)"
    local run_dir="${RALF_RUN_DIR:-$cwd}"

    # Method 1: Check run directory path
    if [[ "$run_dir" == *"/planner/"* ]]; then
        echo "planner"
        return
    elif [[ "$run_dir" == *"/executor/"* ]]; then
        echo "executor"
        return
    elif [[ "$run_dir" == *"/architect/"* ]]; then
        echo "architect"
        return
    fi

    # Method 2: Check for agent-specific files
    if [ -f "queue.yaml" ]; then
        echo "planner"
        return
    elif ls task-*-spec.md 1>/dev/null 2>&1; then
        echo "executor"
        return
    fi

    # Method 3: Check parent directories
    if [[ "$cwd" == *".autonomous/agents/planner"* ]]; then
        echo "planner"
        return
    fi

    # Method 4: Check git branch
    local git_branch="$(git branch --show-current 2>/dev/null || echo "")"
    if [[ "$git_branch" == *"planner"* ]]; then
        echo "planner"
        return
    fi

    # Default
    echo "unknown"
}
```

---

## 7. What SessionStart Hook Must Do

### For Multi-Project Support:

1. **Detect Project:**
   - Check working directory path
   - Check for `.bb5-project` file
   - Default to `blackbox5`

2. **Load Project Routes:**
   - Read `routes.yaml` for current project
   - Validate paths exist

3. **Detect Agent Type:**
   - Use path patterns, file existence, git branch
   - Support planner/executor/architect/developer

4. **Create Run Folder:**
   - Location: `5-project-memory/{project}/runs/{agent_type}/run-{timestamp}/`
   - Create all required files

5. **Load Context:**
   - Project-specific: goals, plans, tasks
   - Agent-specific: queue status, claimed tasks
   - Universal: commands, documentation

6. **Set Environment Variables:**
   - `BB5_PROJECT` - Current project name
   - `RALF_RUN_DIR` - Run directory path
   - `RALF_RUN_ID` - Run identifier
   - `BB5_AGENT_TYPE` - Detected agent type

7. **Generate Output:**
   - Create `AGENT_CONTEXT.md`
   - Return JSON with `additionalContext`

---

## 8. BB5 CLI Commands Available

The hook should reference these commands:

```bash
# Navigation
bb5 whereami              # Show current location
bb5 goal:list             # List all goals
bb5 goal:show [ID]        # Show goal details
bb5 plan:list             # List all plans
bb5 plan:show [ID]        # Show plan details
bb5 task:list             # List all tasks
bb5 task:show [ID]        # Show task details
bb5 task:current          # Show current task
bb5 up                    # Go up one level
bb5 down [ID]             # Go down to child
bb5 root                  # Go to project root
bb5 goto [ID]             # Jump to specific item

# Creation
bb5 goal:create [NAME]    # Create new goal
bb5 plan:create [NAME]    # Create new plan
bb5 task:create [NAME]    # Create new task
bb5 subtask:create [NAME] # Create subtask

# Linking
bb5 link:goal [ID]        # Link plan to goal
bb5 link:plan [ID]        # Link task to plan

# Project (NEW - needs implementation)
bb5 project:list          # List all projects
bb5 project:switch [NAME] # Switch to project
bb5 project:show [NAME]   # Show project details
```

---

## 9. Best Practices from BB5

### What Works Well:

1. **Self-Discovery:** No reliance on environment variables
2. **Symlink-Based Hierarchy:** Goals → Plans → Tasks
3. **Agent-Aware Context:** Different context per agent type
4. **Template System:** Consistent structure
5. **Queue-Based Tasks:** Central prioritization
6. **Event Logging:** Complete lifecycle tracking
7. **Data Layer Pattern:** THOUGHTS.md, DECISIONS.md, LEARNINGS.md

### What Needs Improvement:

1. **Hardcoded Project:** Most tools default to `blackbox5`
2. **No Project Context:** SessionStart doesn't detect which project
3. **No Cross-Project Links:** Can't link tasks across projects

---

## 10. Recommended SessionStart Flow

```bash
#!/bin/bash
# BB5 Dual-Purpose SessionStart Hook

# 1. DETECT PROJECT
PROJECT=$(detect_current_project)
export BB5_PROJECT="$PROJECT"

# 2. DETECT AGENT TYPE
AGENT_TYPE=$(detect_agent_type)
export BB5_AGENT_TYPE="$AGENT_TYPE"

# 3. DETECT MODE (manual vs autonomous)
MODE=$(detect_mode)  # Checks for RALF indicators

# 4. CREATE RUN FOLDER
RUN_TIMESTAMP=$(date +%Y%m%d-%H%M%S)
RUN_ID="run-$RUN_TIMESTAMP"
RUN_DIR="$BB5_DIR/5-project-memory/$PROJECT/runs/$AGENT_TYPE/$RUN_ID"
mkdir -p "$RUN_DIR"
export RALF_RUN_DIR="$RUN_DIR"
export RALF_RUN_ID="$RUN_ID"

# 5. LOAD PROJECT-SPECIFIC CONTEXT
ROUTES_FILE="$BB5_DIR/5-project-memory/$PROJECT/.autonomous/context/routes.yaml"
GOALS_INDEX="$BB5_DIR/5-project-memory/$PROJECT/goals/INDEX.yaml"
QUEUE_FILE="$BB5_DIR/5-project-memory/$PROJECT/.autonomous/agents/communications/queue.yaml"

# 6. LOAD MODE-SPECIFIC CONTEXT
case "$MODE" in
    autonomous)
        # Load plan-state.json, loop state, etc.
        load_autonomous_context "$PROJECT"
        ;;
    manual)
        # Load current task, recent activity
        load_manual_context "$PROJECT"
        ;;
esac

# 7. CREATE CONTEXT FILES
create_thoughts_template "$RUN_DIR" "$PROJECT" "$AGENT_TYPE"
create_results_template "$RUN_DIR" "$PROJECT" "$AGENT_TYPE"
create_decisions_template "$RUN_DIR" "$PROJECT" "$AGENT_TYPE"
create_learnings_template "$RUN_DIR" "$PROJECT" "$AGENT_TYPE"
create_metadata_yaml "$RUN_DIR" "$PROJECT" "$AGENT_TYPE" "$RUN_ID"

# 8. GENERATE AGENT_CONTEXT.md
cat > "$RUN_DIR/AGENT_CONTEXT.md" << EOF
# Agent Context (Auto-Generated)

**Project:** $PROJECT
**Agent Type:** $AGENT_TYPE
**Mode:** $MODE
**Run Directory:** $RUN_DIR

## Project Context
$(load_project_context "$PROJECT")

## Agent Context
$(load_agent_context "$AGENT_TYPE" "$PROJECT")

## Available Commands
\`\`\`bash
bb5 whereami                    # Show current location
bb5 project:list                # List all projects
bb5 project:switch [NAME]       # Switch to project
bb5 goal:list                   # List goals in $PROJECT
bb5 task:list                   # List tasks in $PROJECT
\`\`\`
EOF

# 9. PERSIST ENVIRONMENT VARIABLES
if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo "export BB5_PROJECT=$PROJECT" >> "$CLAUDE_ENV_FILE"
    echo "export BB5_AGENT_TYPE=$AGENT_TYPE" >> "$CLAUDE_ENV_FILE"
    echo "export RALF_RUN_DIR=$RUN_DIR" >> "$CLAUDE_ENV_FILE"
    echo "export RALF_RUN_ID=$RUN_ID" >> "$CLAUDE_ENV_FILE"
fi

# 10. RETURN JSON OUTPUT
echo "{
  \"hookSpecificOutput\": {
    \"hookEventName\": \"SessionStart\",
    \"additionalContext\": \"You are working on project: $PROJECT as a $AGENT_TYPE agent. Run directory: $RUN_DIR\",
    \"project\": \"$PROJECT\",
    \"agentType\": \"$AGENT_TYPE\",
    \"mode\": \"$MODE\",
    \"runDir\": \"$RUN_DIR\",
    \"runId\": \"$RUN_ID\"
  }
}"
```

---

## Key Files to Reference

| File | Purpose |
|------|---------|
| `~/.blackbox5/.claude/hooks/session-start-blackbox5.sh` | Current implementation |
| `~/.blackbox5/.claude/settings.json` | Hook registration |
| `~/.blackbox5/bin/bb5-discover-context` | Context discovery |
| `~/.blackbox5/5-project-memory/blackbox5/.autonomous/context/routes.yaml` | Project routes |
| `~/.blackbox5/5-project-memory/blackbox5/goals/INDEX.yaml` | Goals index |
| `~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` | Task queue |

---

## Summary

The SessionStart hook must:

1. **Detect the project** from working directory or `.bb5-project` file
2. **Detect the agent type** from path, files, or git branch
3. **Detect the mode** (manual vs autonomous) from RALF indicators
4. **Create a run folder** in the correct project location
5. **Load project-specific context** (goals, plans, tasks for that project)
6. **Set environment variables** for other hooks to use
7. **Generate AGENT_CONTEXT.md** with project and agent info
8. **Return JSON** with additionalContext for Claude

This ensures the hook works for:
- **Multiple projects** (blackbox5, siso-internal, etc.)
- **Multiple agent types** (planner, executor, architect, developer)
- **Both modes** (manual user sessions and autonomous RALF loops)
