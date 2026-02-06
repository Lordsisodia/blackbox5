# BB5 CLI Architecture Design

## Executive Summary

This document defines the cohesive architecture for the BlackBox5 (BB5) Command Line Interface. The BB5 CLI provides a unified interface for managing goals, plans, tasks, and the autonomous agent system.

**Status:** Draft
**Last Updated:** 2026-02-06
**Author:** CLI Architecture Expert

---

## 1. Command Structure Philosophy

### 1.1 Convention: Colon-Based Namespacing

**Decision:** Use `bb5 <noun>:<verb>` syntax consistently.

**Rationale:**
- Shell-friendly (no subcommand parsing required)
- Easy to implement as individual scripts
- Clear hierarchy: domain + action
- Tab-completion friendly
- Works with simple `case` statements in bash

**Examples:**
```bash
bb5 task:list           # List all tasks
bb5 task:show TASK-001  # Show specific task
bb5 task:current        # Show current task from context
bb5 task:create "Name"  # Create new task
bb5 task:claim TASK-001 # Claim task for work
bb5 task:complete       # Mark current task complete
```

### 1.2 Command Naming Rules

| Pattern | Usage | Example |
|---------|-------|---------|
| `bb5 <noun>:list` | List all items | `bb5 task:list` |
| `bb5 <noun>:show [ID]` | Show specific item | `bb5 plan:show plan-id` |
| `bb5 <noun>:current` | Show context-derived item | `bb5 task:current` |
| `bb5 <noun>:create "Name"` | Create new item | `bb5 goal:create "Name"` |
| `bb5 <noun>:<action>` | Domain-specific actions | `bb5 task:claim ID` |
| `bb5 <verb>` | Global actions | `bb5 up`, `bb5 root` |

### 1.3 Reserved Global Commands

These commands operate without a noun prefix:

```bash
bb5 whereami            # Show current context
bb5 up                  # Navigate up one level
bb5 down [ID]           # Navigate down to child
bb5 root                # Go to project root
bb5 goto [ID]           # Jump to any item by ID
bb5 status              # System status overview
bb5 help                # Show help
bb5 version             # Show version
```

---

## 2. Command Taxonomy

### 2.1 Core Hierarchy Commands

#### Task Management (`bb5 task:*`)
```bash
bb5 task:list [--status STATUS] [--priority PRIORITY]
bb5 task:show [TASK-ID]
bb5 task:current
bb5 task:create "Task Name"
bb5 task:claim [TASK-ID]    # NEW: Claim task for work
bb5 task:release [TASK-ID]  # NEW: Release claimed task
bb5 task:start [TASK-ID]    # NEW: Mark as in_progress
bb5 task:complete [TASK-ID] # NEW: Mark as completed
bb5 task:block [TASK-ID]    # NEW: Mark as blocked
bb5 task:archive [TASK-ID]  # NEW: Move to completed/
```

#### Goal Management (`bb5 goal:*`)
```bash
bb5 goal:list [--status STATUS]
bb5 goal:show [GOAL-ID]
bb5 goal:create "Goal Name"
bb5 goal:archive [GOAL-ID]  # NEW: Archive completed goal
```

#### Plan Management (`bb5 plan:*`)
```bash
bb5 plan:list [--status STATUS]
bb5 plan:show [PLAN-ID]
bb5 plan:create "Plan Name"
bb5 plan:archive [PLAN-ID]  # NEW: Archive completed plan
```

### 2.2 Linking Commands (`bb5 link:*`)

```bash
bb5 link:goal [GOAL-ID]     # Link current plan to goal
bb5 link:plan [PLAN-ID]     # Link current task to plan
bb5 link:task [TASK-ID]     # Link current item to task (subtask)
bb5 link:unlink [TYPE]      # NEW: Remove link
bb5 link:show               # NEW: Show current links
```

### 2.3 Navigation Commands (`bb5 goto`, `bb5 up`, etc.)

Already implemented:
```bash
bb5 up                      # Go up one level (task -> plan -> goal)
bb5 down [ID]               # Go down to specific child
bb5 root                    # Go to project root
bb5 goto [ID]               # Jump to any item by ID
bb5 whereami                # Show current context
```

### 2.4 Queue Management (`bb5 queue:*`) - NEW

```bash
bb5 queue:show              # Show prioritized queue
bb5 queue:status            # Show queue statistics
bb5 queue:add [TASK-ID]     # Add task to queue
bb5 queue:remove [TASK-ID]  # Remove task from queue
bb5 queue:prioritize        # Re-run prioritization
bb5 queue:next              # Show next task to work
bb5 queue:resolve           # Resolve dependencies
```

### 2.5 Validation Commands (`bb5 validate:*`) - NEW

```bash
bb5 validate:docs [TASK-ID] # Validate task documentation
bb5 validate:links          # Validate all symlinks
bb5 validate:structure      # Validate directory structure
bb5 validate:ssot           # Validate single sources of truth
bb5 validate:all            # Run all validations
```

### 2.6 Status Commands (`bb5 status:*`) - NEW

```bash
bb5 status                  # Overall system status
bb5 status:goals            # Goal completion status
bb5 status:tasks            # Task statistics
bb5 status:queue            # Queue status
bb5 status:skills           # Skill effectiveness
bb5 status:timeline         # Timeline summary
```

### 2.7 Timeline Commands (`bb5 timeline:*`)

Already implemented:
```bash
bb5 timeline show           # Show full timeline
bb5 timeline recent [N]     # Show last N events
bb5 timeline add            # Add event interactively
bb5 timeline add-quick "Title"  # Quick add
bb5 timeline milestones     # Show milestones
bb5 timeline stats          # Show statistics
bb5 timeline search "TERM"  # Search timeline
```

### 2.8 Skill Commands (`bb5 skill:*`) - NEW

```bash
bb5 skill:list              # List all skills
bb5 skill:show [SKILL-NAME] # Show skill details
bb5 skill:dashboard         # Show skill dashboard
bb5 skill:metrics           # Show skill metrics
bb5 skill:log [TASK-ID]     # Log skill usage
```

### 2.9 Run Commands (`bb5 run:*`) - NEW

```bash
bb5 run:list                # List recent runs
bb5 run:show [RUN-ID]       # Show run details
bb5 run:create [TASK-ID]    # Create new run for task
bb5 run:current             # Show current run
bb5 run:archive [RUN-ID]    # Archive run
```

---

## 3. Implementation Patterns

### 3.1 Script Structure Template

All bash-based CLI commands MUST follow this structure:

```bash
#!/bin/bash
# bb5-<name> - Brief description
# Usage: bb5 <noun>:<verb> [options]

set -e

# =============================================================================
# CONFIGURATION
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BLACKBOX5_DIR="$PROJECT_ROOT/5-project-memory/blackbox5"

# Source shared libraries
source "$SCRIPT_DIR/../lib/bb5_colors.sh" 2>/dev/null || true
source "$SCRIPT_DIR/../lib/bb5_utils.sh" 2>/dev/null || true
source "$SCRIPT_DIR/../lib/dry_run.sh" 2>/dev/null || true

# =============================================================================
# FUNCTIONS
# =============================================================================

show_help() {
    cat << 'EOF'
bb5 <noun>:<verb> - Description

USAGE:
    bb5 <noun>:<verb> [OPTIONS]

OPTIONS:
    --dry-run       Show what would be done without executing
    --verbose, -v   Show detailed output
    --help, -h      Show this help message

EXAMPLES:
    bb5 <noun>:<verb> arg1
    bb5 <noun>:<verb> --dry-run
EOF
}

# =============================================================================
# COMMAND IMPLEMENTATION
# =============================================================================

command_list() {
    # Implementation
}

command_show() {
    local id="${1:-}"
    # Implementation
}

# =============================================================================
# MAIN
# =============================================================================

COMMAND="${1:-list}"
shift || true

case "$COMMAND" in
    list)
        command_list "$@"
        ;;
    show)
        command_show "$@"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $COMMAND"
        show_help
        exit 1
        ;;
esac
```

### 3.2 Color Coding Standards

All commands MUST use consistent color coding:

```bash
# Standard color palette
GREEN='\033[0;32m'      # Success, completed
YELLOW='\033[1;33m'     # In progress, warning
BLUE='\033[0;34m'       # Pending, info
CYAN='\033[0;36m'       # Headers, IDs
RED='\033[0;31m'        # Error, blocked
MAGENTA='\033[0;35m'    # Highlights
NC='\033[0m'            # No color (reset)

# Status color mapping
case "$status" in
    completed|done)         color="$GREEN" ;;
    in_progress|in-progress) color="$YELLOW" ;;
    pending|todo)           color="$BLUE" ;;
    blocked)                color="$RED" ;;
    *)                      color="$NC" ;;
esac
```

### 3.3 Header/Footer Pattern

All list/show commands MUST use consistent headers:

```bash
echo "═══════════════════════════════════════════════════════════════"
printf "  ${CYAN}%s${NC}\n" "Section Title"
echo "═══════════════════════════════════════════════════════════════"
```

### 3.4 Error Handling Pattern

```bash
# Check prerequisites
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory not found: $TARGET_DIR" >&2
    exit 1
fi

# Check arguments
if [ -z "$REQUIRED_ARG" ]; then
    echo "Error: Missing required argument" >&2
    show_help >&2
    exit 1
fi

# Set error trap
trap 'echo "Error on line $LINENO" >&2' ERR
```

### 3.5 Dry-Run Support

All commands that modify state MUST support `--dry-run`:

```bash
# Source dry-run library
source "$SCRIPT_DIR/../lib/dry_run.sh"

# Initialize
dry_run_init "$@"

# Use dry-run aware functions
dry_run_mkdir "$NEW_DIR"
dry_run_write "$FILE" "$CONTENT"
dry_run_mv "$SOURCE" "$DEST"

# Or check manually
if dry_run_is_active; then
    echo "[DRY-RUN] Would create: $FILE"
else
    echo "$CONTENT" > "$FILE"
fi
```

---

## 4. Shared Libraries

### 4.1 Library Structure

```
~/.blackbox5/
├── bin/                    # CLI commands
│   ├── bb5-task
│   ├── bb5-goal
│   └── ...
└── lib/                    # Shared libraries (NEW)
    ├── bb5_colors.sh       # Color definitions
    ├── bb5_utils.sh        # Common utilities
    ├── bb5_context.sh      # Context discovery
    ├── bb5_yaml.sh         # YAML operations
    ├── bb5_queue.sh        # Queue operations
    └── dry_run.sh          # Dry-run support (exists)
```

### 4.2 bb5_colors.sh

```bash
#!/bin/bash
# BB5 Color Definitions - Source this for consistent colors

if [ -t 1 ]; then
    BB5_GREEN='\033[0;32m'
    BB5_YELLOW='\033[1;33m'
    BB5_BLUE='\033[0;34m'
    BB5_CYAN='\033[0;36m'
    BB5_RED='\033[0;31m'
    BB5_MAGENTA='\033[0;35m'
    BB5_BOLD='\033[1m'
    BB5_DIM='\033[2m'
    BB5_NC='\033[0m'
else
    BB5_GREEN=''
    BB5_YELLOW=''
    BB5_BLUE=''
    BB5_CYAN=''
    BB5_RED=''
    BB5_MAGENTA=''
    BB5_BOLD=''
    BB5_DIM=''
    BB5_NC=''
fi

# Status color helper
bb5_status_color() {
    local status="$1"
    case "$status" in
        completed|done|success) echo "$BB5_GREEN" ;;
        in_progress|in-progress|active) echo "$BB5_YELLOW" ;;
        pending|todo|waiting) echo "$BB5_BLUE" ;;
        blocked|error|failed) echo "$BB5_RED" ;;
        *) echo "$BB5_NC" ;;
    esac
}

# Priority color helper
bb5_priority_color() {
    local priority="$1"
    case "$priority" in
        critical) echo "$BB5_RED" ;;
        high) echo "$BB5_YELLOW" ;;
        medium) echo "$BB5_BLUE" ;;
        low) echo "$BB5_DIM" ;;
        *) echo "$BB5_NC" ;;
    esac
}
```

### 4.3 bb5_utils.sh

```bash
#!/bin/bash
# BB5 Utility Functions

# Get project root
bb5_project_root() {
    echo "${BB5_PROJECT_ROOT:-$HOME/.blackbox5}"
}

# Get BlackBox5 directory
bb5_dir() {
    echo "$(bb5_project_root)/5-project-memory/blackbox5"
}

# Check if in BB5 project
bb5_in_project() {
    [ -d "$(bb5_dir)/tasks" ] && [ -d "$(bb5_dir)/goals" ]
}

# Generate timestamp
bb5_timestamp() {
    date -Iseconds
}

# Generate date
bb5_date() {
    date +%Y-%m-%d
}

# Sanitize name for ID
bb5_sanitize_id() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-'
}

# Validate task ID format
bb5_is_task_id() {
    [[ "$1" =~ ^TASK-[0-9]+$ ]]
}

# Validate goal ID format
bb5_is_goal_id() {
    [[ "$1" =~ ^IG-[0-9]+$ ]]
}
```

### 4.4 bb5_context.sh

```bash
#!/bin/bash
# BB5 Context Discovery - Wrapper around bb5-discover-context

BB5_CONTEXT_CACHE=""

# Get context (cached)
bb5_context() {
    if [ -z "$BB5_CONTEXT_CACHE" ]; then
        BB5_CONTEXT_CACHE=$("$(bb5_project_root)/bin/bb5-discover-context" json)
    fi
    echo "$BB5_CONTEXT_CACHE"
}

# Get current type
bb5_current_type() {
    bb5_context | grep '"current_type"' | sed 's/.*: "\([^"]*\)".*/\1/'
}

# Get current ID
bb5_current_id() {
    bb5_context | grep '"current_id"' | sed 's/.*: "\([^"]*\)".*/\1/'
}

# Check if in task
bb5_in_task() {
    [ "$(bb5_current_type)" = "task" ]
}

# Check if in plan
bb5_in_plan() {
    [ "$(bb5_current_type)" = "plan" ]
}

# Check if in goal
bb5_in_goal() {
    [ "$(bb5_current_type)" = "goal" ]
}
```

### 4.5 bb5_yaml.sh

```bash
#!/bin/bash
# BB5 YAML Operations

# Get value from YAML (requires yq)
bb5_yaml_get() {
    local file="$1"
    local path="$2"
    if command -v yq >/dev/null 2>&1; then
        yq eval "$path" "$file" 2>/dev/null
    else
        # Fallback: grep-based extraction
        grep "^${path}:" "$file" | sed 's/.*: //' | sed 's/"//g'
    fi
}

# Set value in YAML (requires yq)
bb5_yaml_set() {
    local file="$1"
    local path="$2"
    local value="$3"
    if command -v yq >/dev/null 2>&1; then
        yq eval -i "${path} = \"${value}\"" "$file"
    else
        echo "Error: yq required for YAML modification" >&2
        return 1
    fi
}
```

### 4.6 bb5_queue.sh

```bash
#!/bin/bash
# BB5 Queue Operations

BB5_QUEUE_FILE="$(bb5_dir)/.autonomous/agents/communications/queue.yaml"

# Load queue
bb5_queue_load() {
    if [ -f "$BB5_QUEUE_FILE" ]; then
        cat "$BB5_QUEUE_FILE"
    else
        echo "queue: { tasks: [] }"
    fi
}

# Get task status from queue
bb5_queue_task_status() {
    local task_id="$1"
    # Implementation using yq or grep
}

# Check if task is claimed
bb5_queue_is_claimed() {
    local task_id="$1"
    # Implementation
}
```

---

## 5. Integration Points

### 5.1 CLI to Hook Integration

CLIs and hooks interact through:

1. **File System** - Both read/write to task/plan/goal files
2. **queue.yaml** - Shared queue state
3. **Context Discovery** - Both use `bb5-discover-context`
4. **Events** - CLIs can trigger events that hooks process

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   bb5 CLI   │────▶│  queue.yaml  │◀────│    Hooks    │
│  Commands   │     │  task files  │     │  (stop/,    │
│             │◀────│  run folders │────▶│  post-)     │
└─────────────┘     └──────────────┘     └─────────────┘
```

### 5.2 Safe Queue Updates

All queue modifications MUST use atomic operations:

```bash
# Pattern for safe queue updates
update_queue() {
    local queue_file="$1"
    local temp_file="${queue_file}.tmp.$$"
    local backup_file="${queue_file}.backup.$(date +%Y%m%d_%H%M%S)"

    # Create backup
    cp "$queue_file" "$backup_file"

    # Modify and write to temp
    # ... modification logic ...
    cat "$modified_content" > "$temp_file"

    # Atomic move
    mv "$temp_file" "$queue_file"

    # Clean up old backups (keep last 5)
    ls -t "${queue_file}.backup."* 2>/dev/null | tail -n +6 | xargs rm -f
}
```

### 5.3 Hook Trigger Points

CLIs should trigger hooks at appropriate points:

```bash
# After task state change
trigger_hooks() {
    local event="$1"
    local task_id="$2"

    # Set environment for hooks
    export BB5_EVENT="$event"
    export BB5_TASK_ID="$task_id"

    # Run relevant hooks
    if [ -d "$BLACKBOX5_DIR/.autonomous/hooks/$event" ]; then
        for hook in "$BLACKBOX5_DIR/.autonomous/hooks/$event"/*; do
            if [ -x "$hook" ]; then
                "$hook" "$task_id" || true
            fi
        done
    fi
}
```

---

## 6. Consistency Requirements

### 6.1 Required Consistency

| Aspect | Requirement | Enforcement |
|--------|-------------|-------------|
| Colors | Use `bb5_colors.sh` | Code review |
| Headers | Use `═` pattern | Template |
| Error messages | Print to stderr | Code review |
| Exit codes | 0=success, 1=error, 2=usage | Testing |
| Help format | Standard template | Code review |
| Dry-run | All state changes | Testing |
| Logging | Use stderr for debug | Code review |

### 6.2 Exit Code Standards

```bash
0   # Success
1   # General error
2   # Usage error (bad arguments)
3   # Not found (task/goal/plan doesn't exist)
4   # Already exists (duplicate)
5   # Permission denied
6   # Validation failed
7   # Dependency not met
```

### 6.3 Output Format Standards

**Human-readable (default):**
- Use colors for status
- Box-drawing characters for headers
- Clear section separation
- Actionable next steps

**JSON (`--json` flag):**
- Machine-parseable
- Complete data
- No colors or formatting

```bash
# Support both formats
FORMAT="${FORMAT:-human}"

if [ "$FORMAT" = "json" ]; then
    echo '{"tasks": [...]}'
else
    # Human-readable output
fi
```

---

## 7. Migration Path

### 7.1 Phase 1: Library Creation (Immediate)

1. Create `~/.blackbox5/lib/` directory
2. Create shared libraries:
   - `bb5_colors.sh`
   - `bb5_utils.sh`
   - `bb5_context.sh`
3. Update existing CLIs to source libraries

### 7.2 Phase 2: Consistency Updates (Week 1)

1. Update all existing commands to use shared colors
2. Standardize header/footer patterns
3. Add `--dry-run` support where missing
4. Add `--json` support where appropriate

### 7.3 Phase 3: New Commands (Week 2)

1. Implement `bb5 task:claim`
2. Implement `bb5 task:complete`
3. Implement `bb5 queue:*` commands
4. Implement `bb5 validate:*` commands

### 7.4 Phase 4: Polish (Week 3)

1. Add comprehensive help text
2. Add shell completion scripts
3. Add integration tests
4. Document all commands

---

## 8. File Locations

### 8.1 CLI Binaries

All CLI commands live in:
```
~/.blackbox5/bin/
├── bb5-task
├── bb5-goal
├── bb5-plan
├── bb5-link
├── bb5-create
├── bb5-goto
├── bb5-whereami
├── bb5-timeline
├── bb5-skill-dashboard
├── bb5-queue-manager.py
└── bb5-* (new commands)
```

### 8.2 Shared Libraries

```
~/.blackbox5/lib/
├── bb5_colors.sh
├── bb5_utils.sh
├── bb5_context.sh
├── bb5_yaml.sh
├── bb5_queue.sh
└── dry_run.sh (moved from 2-engine)
```

### 8.3 Configuration

```
~/.blackbox5/5-project-memory/blackbox5/
├── .autonomous/
│   ├── agents/communications/queue.yaml
│   └── hooks/
├── operations/
│   ├── skill-metrics.yaml
│   └── skill-selection.yaml
├── tasks/active/
├── plans/active/
└── goals/active/
```

---

## 9. Implementation Checklist

### Existing Commands to Update

- [ ] `bb5-task` - Standardize colors, add dry-run support
- [ ] `bb5-goal` - Standardize colors, add dry-run support
- [ ] `bb5-plan` - Standardize colors, add dry-run support
- [ ] `bb5-link` - Standardize colors
- [ ] `bb5-create` - Standardize colors, add dry-run support
- [ ] `bb5-goto` - Standardize colors
- [ ] `bb5-whereami` - Already minimal
- [ ] `bb5-timeline` - Standardize colors
- [ ] `bb5-skill-dashboard` - Add `--json` support

### New Commands to Create

- [ ] `bb5 task:claim`
- [ ] `bb5 task:release`
- [ ] `bb5 task:start`
- [ ] `bb5 task:complete`
- [ ] `bb5 task:block`
- [ ] `bb5 task:archive`
- [ ] `bb5 queue:show`
- [ ] `bb5 queue:status`
- [ ] `bb5 queue:add`
- [ ] `bb5 queue:remove`
- [ ] `bb5 queue:next`
- [ ] `bb5 validate:docs`
- [ ] `bb5 validate:links`
- [ ] `bb5 validate:structure`
- [ ] `bb5 status`

### Libraries to Create

- [ ] `lib/bb5_colors.sh`
- [ ] `lib/bb5_utils.sh`
- [ ] `lib/bb5_context.sh`
- [ ] `lib/bb5_yaml.sh`
- [ ] `lib/bb5_queue.sh`

---

## 10. Appendix: Command Reference

### Quick Reference Card

```
Navigation:
  bb5 whereami              Show current location
  bb5 up                    Go up one level
  bb5 down [ID]             Go down to child
  bb5 root                  Go to project root
  bb5 goto [ID]             Jump to item

Task Management:
  bb5 task:list             List tasks
  bb5 task:show [ID]        Show task details
  bb5 task:current          Show current task
  bb5 task:create "Name"    Create task
  bb5 task:claim [ID]       Claim task
  bb5 task:complete [ID]    Complete task

Goal/Plan Management:
  bb5 goal:list             List goals
  bb5 goal:show [ID]        Show goal
  bb5 plan:list             List plans
  bb5 plan:show [ID]        Show plan

Linking:
  bb5 link:goal [ID]        Link plan to goal
  bb5 link:plan [ID]        Link task to plan

Queue:
  bb5 queue:show            Show queue
  bb5 queue:next            Show next task
  bb5 queue:status          Queue statistics

Validation:
  bb5 validate:docs [ID]    Validate documentation
  bb5 validate:all          Run all validations

Status:
  bb5 status                System status
  bb5 status:tasks          Task statistics

Timeline:
  bb5 timeline show         Show timeline
  bb5 timeline recent [N]   Recent events

Skills:
  bb5 skill:dashboard       Skill metrics
```

---

*End of BB5 CLI Architecture Design Document*
