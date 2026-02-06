# BB5 Claim Command Implementation Plan

## Overview

Implementation plan for `bb5 claim` and `bb5 unclaim` commands to enable task claiming with run folder creation and queue.yaml tracking.

---

## Commands

### 1. `bb5 claim TASK-ID [--force]`

**Purpose:** Claim a task for execution, creating a run folder and initializing data layer files.

**Flow:**
1. Parse TASK-ID and --force flag
2. Validate task exists in `tasks/active/TASK-ID/`
3. Check if already claimed in queue.yaml (unless --force)
4. Create run folder: `runs/run-YYYYMMDD-HHMMSS-TASK-ID/`
5. Generate THOUGHTS.md with full goal→plan→task hierarchy
6. Create DECISIONS.md, ASSUMPTIONS.md, LEARNINGS.md, RESULTS.md
7. Update queue.yaml (mark claimed, set claimed_by, claimed_at)
8. Add event to events.yaml
9. Output confirmation with run folder path

### 2. `bb5 unclaim TASK-ID`

**Purpose:** Release a claimed task.

**Flow:**
1. Validate task exists
2. Check if task is claimed by current user
3. Update queue.yaml (clear claimed_by, set status back to pending)
4. Archive run folder to `runs/archived/YYYYMMDD-HHMMSS-TASK-ID/`
5. Add event to events.yaml
6. Output confirmation

---

## Implementation: bb5-claim

```bash
#!/bin/bash
# bb5-claim - Task claiming commands
# Usage: bb5 claim [TASK-ID] [--force] | bb5 unclaim [TASK-ID]
#
# Commands:
#   bb5 claim TASK-ID        Claim a task for execution
#   bb5 claim --force TASK-ID Force claim (override existing)
#   bb5 unclaim TASK-ID      Release a claimed task

set -e

# Source dry-run utility library
source "$(dirname "$0")/../2-engine/.autonomous/lib/dry_run.sh" 2>/dev/null || true

# =============================================================================
# CONFIGURATION
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BLACKBOX5_DIR="$PROJECT_ROOT/5-project-memory/blackbox5"
TASKS_DIR="$BLACKBOX5_DIR/tasks/active"
RUNS_DIR="$BLACKBOX5_DIR/runs"
QUEUE_FILE="$BLACKBOX5_DIR/.autonomous/agents/communications/queue.yaml"
EVENTS_FILE="$BLACKBOX5_DIR/.autonomous/agents/communications/events.yaml"

# =============================================================================
# COLORS
# =============================================================================

if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    RED='\033[0;31m'
    NC='\033[0m'
else
    GREEN=''
    YELLOW=''
    BLUE=''
    CYAN=''
    RED=''
    NC=''
fi

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

# Get current user/agent identifier
get_current_agent() {
    # Priority: RALF_AGENT_ID > USER > whoami > unknown
    echo "${RALF_AGENT_ID:-${USER:-$(whoami 2>/dev/null || echo "unknown")}}"
}

# Get current timestamp in ISO format
get_timestamp() {
    date -Iseconds
}

# Generate run folder name
generate_run_id() {
    local task_id="$1"
    echo "run-$(date +%Y%m%d-%H%M%S)-${task_id}"
}

# Validate task exists
validate_task_exists() {
    local task_id="$1"
    local task_dir="$TASKS_DIR/$task_id"

    if [ ! -d "$task_dir" ]; then
        echo -e "${RED}Error: Task not found: $task_id${NC}"
        echo ""
        echo "Available tasks:"
        "$SCRIPT_DIR/bb5-task" list
        return 1
    fi
    return 0
}

# Get task info from queue.yaml
get_task_info() {
    local task_id="$1"
    local field="$2"

    if [ -f "$QUEUE_FILE" ]; then
        grep -A 50 "^  - id: \"$task_id\"" "$QUEUE_FILE" 2>/dev/null | \
            grep "^    $field:" | head -1 | sed 's/.*: "\(.*\)".*/\1/'
    fi
}

# Check if task is claimed
check_task_claimed() {
    local task_id="$1"
    local claimed_by

    claimed_by=$(get_task_info "$task_id" "claimed_by")
    if [ -n "$claimed_by" ] && [ "$claimed_by" != "null" ] && [ "$claimed_by" != "" ]; then
        echo "$claimed_by"
        return 0
    fi
    return 1
}

# Update queue.yaml with claim status
update_queue_claim() {
    local task_id="$1"
    local agent="$2"
    local timestamp="$3"
    local status="$4"

    if [ ! -f "$QUEUE_FILE" ]; then
        echo -e "${YELLOW}Warning: queue.yaml not found at $QUEUE_FILE${NC}"
        return 1
    fi

    # Create backup
    dry_run_exec "cp \"$QUEUE_FILE\" \"$QUEUE_FILE.backup.$(date +%Y%m%d%H%M%S)\"" "Backup queue.yaml"

    if dry_run_is_active; then
        dry_run_echo "Update queue.yaml: Set $task_id claimed_by=$agent, status=$status"
        return 0
    fi

    # Use sed to update the task entry
    # This is a simplified approach - in production, use yq or similar
    local temp_file=$(mktemp)
    local in_task=0
    local task_found=0

    while IFS= read -r line; do
        # Check if we're entering our task
        if echo "$line" | grep -q "^  - id: \"$task_id\""; then
            in_task=1
            task_found=1
        fi

        # If we're in our task and find status line, update it
        if [ $in_task -eq 1 ] && echo "$line" | grep -q "^    status:"; then
            line="    status: \"$status\""
        fi

        # If we're in our task and find claimed_by line, update it
        if [ $in_task -eq 1 ] && echo "$line" | grep -q "^    claimed_by:"; then
            line="    claimed_by: \"$agent\""
        fi

        # If we're in our task and find claimed_at line, update it
        if [ $in_task -eq 1 ] && echo "$line" | grep -q "^    claimed_at:"; then
            line="    claimed_at: \"$timestamp\""
        fi

        # Check if we're leaving our task (next task or end of tasks section)
        if [ $in_task -eq 1 ] && echo "$line" | grep -q "^  - id:" && ! echo "$line" | grep -q "\"$task_id\""; then
            in_task=0
        fi

        echo "$line" >> "$temp_file"
    done < "$QUEUE_FILE"

    # If task was found but didn't have claimed fields, we need to add them
    # For simplicity, we'll append them before the next task or at end of task block
    # This is a basic implementation - production should use proper YAML manipulation

    mv "$temp_file" "$QUEUE_FILE"

    if [ $task_found -eq 0 ]; then
        echo -e "${YELLOW}Warning: Task $task_id not found in queue.yaml${NC}"
        return 1
    fi

    return 0
}

# Add event to events.yaml
add_event() {
    local task_id="$1"
    local event_type="$2"
    local agent="$3"
    local run_id="$4"
    local notes="${5:-}"

    if dry_run_is_active; then
        dry_run_echo "Add event: type=$event_type, task=$task_id, agent=$agent"
        return 0
    fi

    if [ ! -f "$EVENTS_FILE" ]; then
        # Create events file with header
        cat > "$EVENTS_FILE" << EOF
# BlackBox5 Events Log
# Generated: $(get_timestamp)
#
EOF
    fi

    # Append event
    cat >> "$EVENTS_FILE" << EOF

- timestamp: '$(get_timestamp)'
  task_id: '$task_id'
  type: $event_type
  agent: $agent
  run_id: $run_id
  notes: '$notes'
EOF
}

# Find parent plan for a task
find_parent_plan() {
    local task_id="$1"

    # Search through plans for symlinks to this task
    if [ -d "$BLACKBOX5_DIR/plans/active" ]; then
        for plan_dir in "$BLACKBOX5_DIR/plans/active"/*/; do
            if [ -d "$plan_dir/tasks" ]; then
                for task_link in "$plan_dir/tasks"/*; do
                    if [ -L "$task_link" ]; then
                        local link_target
                        link_target=$(readlink "$task_link")
                        if [ "$(basename "$link_target")" = "$task_id" ]; then
                            basename "$plan_dir"
                            return 0
                        fi
                    fi
                done
            fi
        done
    fi
    return 1
}

# Find parent goal for a plan
find_parent_goal() {
    local plan_id="$1"

    # Search through goals for references to this plan
    if [ -d "$BLACKBOX5_DIR/goals/active" ]; then
        for goal_dir in "$BLACKBOX5_DIR/goals/active"/*/; do
            if [ -f "$goal_dir/goal.yaml" ]; then
                if grep -q "$plan_id" "$goal_dir/goal.yaml" 2>/dev/null; then
                    basename "$goal_dir"
                    return 0
                fi
            fi
        done
    fi
    return 1
}

# Get task details for THOUGHTS.md
get_task_details() {
    local task_id="$1"
    local task_file="$TASKS_DIR/$task_id/task.md"

    if [ -f "$task_file" ]; then
        local title
        title=$(grep "^# " "$task_file" 2>/dev/null | head -1 | sed 's/^# //' || echo "$task_id")
        echo "$title"
    else
        echo "$task_id"
    fi
}

# Get plan details
get_plan_details() {
    local plan_id="$1"
    local plan_file="$BLACKBOX5_DIR/plans/active/$plan_id/plan.md"
    local metadata_file="$BLACKBOX5_DIR/plans/active/$plan_id/metadata.yaml"

    if [ -f "$metadata_file" ]; then
        grep "^name:" "$metadata_file" 2>/dev/null | sed 's/name: "\(.*\)"/\1/' | head -1
    elif [ -f "$plan_file" ]; then
        head -1 "$plan_file" | sed 's/^# //'
    else
        echo "$plan_id"
    fi
}

# Get goal details
get_goal_details() {
    local goal_id="$1"
    local goal_file="$BLACKBOX5_DIR/goals/active/$goal_id/goal.yaml"

    if [ -f "$goal_file" ]; then
        grep "^name:" "$goal_file" 2>/dev/null | sed 's/name: "\(.*\)"/\1/' | head -1
    else
        echo "$goal_id"
    fi
}

# =============================================================================
# CLAIM COMMAND
# =============================================================================

cmd_claim() {
    local task_id=""
    local force=false

    # Parse arguments
    for arg in "$@"; do
        case "$arg" in
            --force)
                force=true
                ;;
            --dry-run)
                # Already handled by dry_run_init
                ;;
            --verbose|-v)
                # Already handled by dry_run_init
                ;;
            -*)
                echo -e "${RED}Unknown option: $arg${NC}"
                exit 1
                ;;
            *)
                if [ -z "$task_id" ]; then
                    task_id="$arg"
                fi
                ;;
        esac
    done

    if [ -z "$task_id" ]; then
        echo "Usage: bb5 claim TASK-ID [--force]"
        echo "       bb5 claim --force TASK-ID"
        echo ""
        echo "Options:"
        echo "  --force    Override existing claim"
        echo "  --dry-run  Show what would happen without making changes"
        echo ""
        echo "Available tasks:"
        "$SCRIPT_DIR/bb5-task" list
        exit 1
    fi

    # Validate task exists
    if ! validate_task_exists "$task_id"; then
        exit 1
    fi

    local task_dir="$TASKS_DIR/$task_id"
    local agent
    agent=$(get_current_agent)
    local timestamp
    timestamp=$(get_timestamp)

    echo "═══════════════════════════════════════════════════════════════"
    echo "  Task Claim"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "Task: $task_id"
    echo "Agent: $agent"
    echo ""

    # Check if already claimed
    local current_claim
    current_claim=$(check_task_claimed "$task_id")
    if [ -n "$current_claim" ]; then
        if [ "$force" = true ]; then
            echo -e "${YELLOW}Warning: Task already claimed by $current_claim${NC}"
            echo -e "${YELLOW}Force flag set - overriding claim${NC}"
            echo ""
        else
            echo -e "${RED}Error: Task already claimed by $current_claim${NC}"
            echo ""
            echo "Use --force to override:"
            echo "  bb5 claim --force $task_id"
            echo ""
            exit 1
        fi
    fi

    # Generate run ID and folder
    local run_id
    run_id=$(generate_run_id "$task_id")
    local run_dir="$RUNS_DIR/$run_id"

    echo "Run ID: $run_id"
    echo "Run Directory: $run_dir"
    echo ""

    # Find hierarchy
    local parent_plan
    parent_plan=$(find_parent_plan "$task_id" || echo "")
    local parent_goal
    if [ -n "$parent_plan" ]; then
        parent_goal=$(find_parent_goal "$parent_plan" || echo "")
    fi

    # Get details for hierarchy
    local task_title
    task_title=$(get_task_details "$task_id")
    local plan_title=""
    local goal_title=""
    [ -n "$parent_plan" ] && plan_title=$(get_plan_details "$parent_plan")
    [ -n "$parent_goal" ] && goal_title=$(get_goal_details "$parent_goal")

    # Create run folder
    dry_run_mkdir "$run_dir"

    # Create THOUGHTS.md with hierarchy
    local thoughts_content="# Thoughts - $task_id

## Task Hierarchy

**Claimed by:** $agent
**Claimed at:** $timestamp
**Run ID:** $run_id

### Goal → Plan → Task Chain

"

    if [ -n "$parent_goal" ]; then
        thoughts_content+="- **Goal:** [$parent_goal] $goal_title
"
    fi
    if [ -n "$parent_plan" ]; then
        thoughts_content+="- **Plan:** [$parent_plan] $plan_title
"
    fi
    thoughts_content+="- **Task:** [$task_id] $task_title
"

    thoughts_content+="
## Thought Log

### $(date '+%Y-%m-%d %H:%M:%S') - Initial Claim

- Task claimed for execution
- Run folder initialized
- Ready to begin work

"

    dry_run_write "$run_dir/THOUGHTS.md" "$thoughts_content"

    # Create other data layer files
    dry_run_write "$run_dir/DECISIONS.md" "# Decisions - $task_id

## Decision Log

### $(date '+%Y-%m-%d %H:%M:%S') - Initial Setup

- Claimed task: $task_id
- Run: $run_id

## Decisions Made

"

    dry_run_write "$run_dir/ASSUMPTIONS.md" "# Assumptions - $task_id

## Assumption Log

### $(date '+%Y-%m-%d %H:%M:%S') - Initial Assumptions

- Task scope is as documented in task.md
- All dependencies are satisfied
- Required resources are available

## Assumptions Being Tested

"

    dry_run_write "$run_dir/LEARNINGS.md" "# Learnings - $task_id

## Learning Log

### $(date '+%Y-%m-%d %H:%M:%S') - Session Start

- Beginning work on $task_id
- Run: $run_id

## Key Learnings

"

    dry_run_write "$run_dir/RESULTS.md" "# Results - $task_id

## Result Log

### $(date '+%Y-%m-%d %H:%M:%S') - Claimed

- Task claimed by $agent
- Run folder: $run_dir

## Outcomes

"

    # Create metadata.yaml
    local metadata_content="run_id: \"$run_id\"
task_id: \"$task_id\"
claimed_by: \"$agent\"
claimed_at: \"$timestamp\"
status: \"in_progress\"
parent_plan: \"${parent_plan:-}\"
parent_goal: \"${parent_goal:-}\"
"
    dry_run_write "$run_dir/metadata.yaml" "$metadata_content"

    # Update queue.yaml
    echo "Updating queue.yaml..."
    update_queue_claim "$task_id" "$agent" "$timestamp" "in_progress"

    # Add event
    echo "Logging event..."
    add_event "$task_id" "claimed" "$agent" "$run_id" "Task claimed for execution"

    # Output summary
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    if dry_run_is_active; then
        echo -e "  ${YELLOW}[DRY-RUN] Would claim task${NC}"
    else
        echo -e "  ${GREEN}✓ Task claimed successfully${NC}"
    fi
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "Task: $task_id"
    echo "Claimed by: $agent"
    echo "Run folder: $run_dir"
    echo ""
    if [ -n "$parent_goal" ]; then
        echo "Hierarchy:"
        echo "  Goal: $parent_goal"
        [ -n "$parent_plan" ] && echo "  Plan: $parent_plan"
        echo "  Task: $task_id"
        echo ""
    fi
    echo "Next steps:"
    echo "  cd $run_dir"
    echo "  bb5 task:show $task_id"
    echo ""
}

# =============================================================================
# UNCLAIM COMMAND
# =============================================================================

cmd_unclaim() {
    local task_id="$1"

    if [ -z "$task_id" ]; then
        echo "Usage: bb5 unclaim TASK-ID"
        echo ""
        echo "Currently claimed tasks:"
        # List claimed tasks
        if [ -f "$QUEUE_FILE" ]; then
            grep -B 5 "claimed_by:" "$QUEUE_FILE" 2>/dev/null | grep "^  - id:" | sed 's/.*: "\(.*\)".*/  \1/' || echo "  (none)"
        fi
        exit 1
    fi

    # Validate task exists
    if ! validate_task_exists "$task_id"; then
        exit 1
    fi

    local agent
    agent=$(get_current_agent)
    local timestamp
    timestamp=$(get_timestamp)

    echo "═══════════════════════════════════════════════════════════════"
    echo "  Task Unclaim"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "Task: $task_id"
    echo "Agent: $agent"
    echo ""

    # Check if task is claimed
    local current_claim
    current_claim=$(check_task_claimed "$task_id")
    if [ -z "$current_claim" ]; then
        echo -e "${YELLOW}Warning: Task is not currently claimed${NC}"
        echo ""
    elif [ "$current_claim" != "$agent" ]; then
        echo -e "${YELLOW}Warning: Task claimed by $current_claim, not you${NC}"
        echo "Proceeding anyway..."
        echo ""
    fi

    # Find and archive run folder(s)
    echo "Archiving run folders..."
    local archived_count=0
    for run_dir in "$RUNS_DIR"/run-*-"$task_id"/; do
        if [ -d "$run_dir" ]; then
            local run_name
            run_name=$(basename "$run_dir")
            local archive_dir="$RUNS_DIR/archived/$(date +%Y%m%d)-$run_name"

            dry_run_mkdir "$(dirname "$archive_dir")"
            dry_run_mv "$run_dir" "$archive_dir"

            echo "  Archived: $run_name"
            archived_count=$((archived_count + 1))
        fi
    done

    if [ $archived_count -eq 0 ]; then
        echo "  (no run folders found)"
    fi
    echo ""

    # Update queue.yaml
    echo "Updating queue.yaml..."
    update_queue_claim "$task_id" "" "" "pending"

    # Add event
    echo "Logging event..."
    add_event "$task_id" "unclaimed" "$agent" "" "Task unclaimed, returned to pending"

    # Output summary
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    if dry_run_is_active; then
        echo -e "  ${YELLOW}[DRY-RUN] Would unclaim task${NC}"
    else
        echo -e "  ${GREEN}✓ Task unclaimed successfully${NC}"
    fi
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "Task: $task_id"
    echo "Status: returned to pending"
    echo "Archived runs: $archived_count"
    echo ""
}

# =============================================================================
# MAIN
# =============================================================================

# Initialize dry-run mode
# Parse --dry-run and --verbose from all arguments
for arg in "$@"; do
    case "$arg" in
        --dry-run)
            DRY_RUN=true
            ;;
        --verbose|-v)
            DRY_RUN_VERBOSE=true
            ;;
    esac
done

if dry_run_is_active; then
    echo -e "${YELLOW}[DRY-RUN MODE ENABLED]${NC}"
    echo -e "${YELLOW}This is a simulation. No changes will be made.${NC}"
    echo ""
fi

# Get the subcommand (claim/unclaim)
SUBCOMMAND="${1:-}"
shift || true

case "$SUBCOMMAND" in
    claim)
        cmd_claim "$@"
        ;;
    unclaim)
        cmd_unclaim "$@"
        ;;
    *)
        echo "BlackBox5 Task Claim Commands"
        echo ""
        echo "Usage:"
        echo "  bb5 claim TASK-ID [--force]     Claim a task for execution"
        echo "  bb5 unclaim TASK-ID             Release a claimed task"
        echo ""
        echo "Options:"
        echo "  --force       Override existing claim"
        echo "  --dry-run     Show what would happen without making changes"
        echo "  --verbose     Show detailed output in dry-run mode"
        echo ""
        echo "Examples:"
        echo "  bb5 claim TASK-ARCH-001"
        echo "  bb5 claim --force TASK-ARCH-001"
        echo "  bb5 unclaim TASK-ARCH-001"
        echo ""
        exit 1
        ;;
esac

# Print dry-run summary if active
dry_run_summary
```

---

## Integration with bb5 Main CLI

Add to `/Users/shaansisodia/.blackbox5/bin/bb5`:

```bash
# Claim commands
claim)
    "$SCRIPT_DIR/bb5-claim" claim "$@"
    ;;
unclaim)
    "$SCRIPT_DIR/bb5-claim" unclaim "$@"
    ;;
```

And update the help text:

```bash
TASK CLAIMING
  bb5 claim TASK-ID [--force]  Claim a task for execution
  bb5 unclaim TASK-ID          Release a claimed task
```

---

## Testing Plan

### Unit Tests

1. **Task Validation**
   - Test with valid TASK-ID
   - Test with non-existent TASK-ID
   - Test with empty TASK-ID

2. **Claim Logic**
   - Test claiming unclaimed task
   - Test claiming already claimed task (should fail)
   - Test force claim on already claimed task (should succeed)

3. **Run Folder Creation**
   - Verify folder structure created correctly
   - Verify THOUGHTS.md contains hierarchy
   - Verify all data layer files exist

4. **Queue Updates**
   - Verify queue.yaml updated correctly
   - Verify events.yaml entry added
   - Verify backup created

5. **Unclaim Logic**
   - Test unclaiming claimed task
   - Test unclaiming unclaimed task (warning)
   - Test unclaiming by different agent (warning)
   - Verify run folder archived

### Integration Tests

1. **Full Workflow**
   ```bash
   bb5 claim TASK-TEST-001
   # Verify run folder created
   ls runs/run-*-TASK-TEST-001/

   bb5 unclaim TASK-TEST-001
   # Verify run folder archived
   ls runs/archived/*-run-*-TASK-TEST-001/
   ```

2. **Dry-Run Mode**
   ```bash
   bb5 claim --dry-run TASK-TEST-001
   # Verify no actual changes
   ```

3. **Hierarchy Discovery**
   ```bash
   bb5 claim TASK-ARCH-021
   # Verify THOUGHTS.md contains:
   # - Goal: IG-007
   # - Plan: navigation-system
   # - Task: TASK-ARCH-021
   ```

---

## Error Handling Strategy

### Error Categories

| Error | Handling | Exit Code |
|-------|----------|-----------|
| Task not found | Show available tasks, exit | 1 |
| Already claimed | Show current owner, suggest --force | 1 |
| Queue file not found | Warning, continue | 0 |
| Permission denied | Error message, exit | 1 |
| Invalid arguments | Show usage, exit | 1 |

### User-Friendly Messages

- **Success**: Green checkmark with clear confirmation
- **Warning**: Yellow text with explanation
- **Error**: Red text with actionable next steps

---

## Edge Cases

1. **Concurrent Claims**: Two agents claim same task simultaneously
   - Solution: Check claim status immediately before writing

2. **Orphaned Run Folders**: Task unclaimed but run folder exists
   - Solution: Archive all matching run folders on unclaim

3. **Missing queue.yaml**: Queue file doesn't exist
   - Solution: Warning only, don't fail

4. **Malformed queue.yaml**: YAML parsing fails
   - Solution: Backup and attempt line-based manipulation

5. **Circular Hierarchy**: Task linked to plan linked to itself
   - Solution: Detect and break at reasonable depth

---

## File Locations

| File | Path |
|------|------|
| Implementation | `/Users/shaansisodia/.blackbox5/bin/bb5-claim` |
| Integration | `/Users/shaansisodia/.blackbox5/bin/bb5` |
| Queue | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` |
| Events | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml` |
| Run Folders | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/runs/run-YYYYMMDD-HHMMSS-TASK-ID/` |
| Archive | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/runs/archived/YYYYMMDD-run-.../` |

---

## Future Enhancements

1. **List Claimed Tasks**: `bb5 claim:list` to show all claimed tasks
2. **Steal with Reason**: `bb5 claim --steal TASK-ID --reason "urgent"`
3. **Claim Timeout**: Auto-release claims after N hours
4. **Claim Notifications**: Notify previous owner on force claim
5. **Parallel Claims**: Allow multiple agents to claim (pair programming mode)
