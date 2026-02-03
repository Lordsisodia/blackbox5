#!/bin/bash
# RALF Stop Hook - Self-Discovering Version
# Validates completion, syncs queue, commits, and archives run folder
# This is a COMMAND hook - runs bash directly, zero LLM tokens
#
# Triggered by: Stop event in .claude/settings.json
# Purpose: Enforce run completion and archive (Phase 7 of 7-phase execution flow)
#
# This hook is INTELLIGENT - it discovers configuration from filesystem,
# not environment variables. This makes it robust and self-contained.

set -e

# =============================================================================
# SELF-DISCOVERY: Find project root from hook location
# =============================================================================

# Hook knows where it lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Discover project memory
PROJECT_MEMORY_DIR="$PROJECT_ROOT/5-project-memory"
if [ ! -d "$PROJECT_MEMORY_DIR" ]; then
    echo "[RALF-STOP] ERROR: Project memory not found at $PROJECT_MEMORY_DIR"
    exit 1
fi

# Use first available project (or blackbox5 as default)
PROJECT_NAME="blackbox5"
PROJECT_DIR="$PROJECT_MEMORY_DIR/$PROJECT_NAME"

if [ ! -d "$PROJECT_DIR" ]; then
    PROJECT_NAME=$(ls -1 "$PROJECT_MEMORY_DIR" | head -1)
    PROJECT_DIR="$PROJECT_MEMORY_DIR/$PROJECT_NAME"
fi

# =============================================================================
# DISCOVER RUN: Find the most recent run folder
# =============================================================================

# Look for runs in unknown/ (where SessionStart creates them)
RUNS_DIR="$PROJECT_DIR/runs"
RUN_DIR=""
RUN_ID=""
AGENT_TYPE="unknown"

# Try to find run from environment first (for backward compatibility)
if [ -n "$RALF_RUN_DIR" ] && [ -d "$RALF_RUN_DIR" ]; then
    RUN_DIR="$RALF_RUN_DIR"
    RUN_ID="${RALF_RUN_ID:-unknown}"
    AGENT_TYPE="${RALF_AGENT_TYPE:-unknown}"
else
    # Self-discover: find most recent run folder
    # Check all agent type directories
    for agent_dir in "$RUNS_DIR"/*; do
        [ -d "$agent_dir" ] || continue

        # Find most recent run in this agent directory
        for run_dir in "$agent_dir"/run-*; do
            [ -d "$run_dir" ] || continue

            # Check if this run has a .hook_initialized marker (not yet archived)
            if [ -f "$run_dir/.hook_initialized" ]; then
                # Get modification time and track most recent
                mtime=$(stat -f "%m" "$run_dir/.hook_initialized" 2>/dev/null || stat -c "%Y" "$run_dir/.hook_initialized" 2>/dev/null || echo "0")
                if [ -z "$RUN_DIR" ] || [ "$mtime" -gt "$last_mtime" 2>/dev/null ]; then
                    RUN_DIR="$run_dir"
                    last_mtime="$mtime"
                    AGENT_TYPE=$(basename "$agent_dir")
                fi
            fi
        done
    done

    # Extract RUN_ID from directory name
    if [ -n "$RUN_DIR" ]; then
        RUN_ID=$(basename "$RUN_DIR")
    fi
fi

# =============================================================================
# COLORS & LOGGING
# =============================================================================

if [ -t 1 ]; then
    BLUE='\033[0;34m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    CYAN='\033[0;36m'
    NC='\033[0m'
else
    BLUE=''
    GREEN=''
    YELLOW=''
    RED=''
    CYAN=''
    NC=''
fi

log() { echo -e "${BLUE}[RALF-STOP]${NC} $1"; }
log_success() { echo -e "${GREEN}[RALF-STOP]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[RALF-STOP]${NC} $1"; }
log_error() { echo -e "${RED}[RALF-STOP]${NC} $1"; }
log_info() { echo -e "${CYAN}[RALF-STOP]${NC} $1"; }

# =============================================================================
# VALIDATION - Check if we have required context
# =============================================================================

log "Stop hook fired - Phase 7: Archive"

if [ -z "$RUN_DIR" ] || [ ! -d "$RUN_DIR" ]; then
    log_warning "No run folder found to process"
    log_info "Skipping archive - session may have been a quick check"
    exit 0
fi

if [ "$RUN_ID" = "unknown" ]; then
    log_warning "Could not determine RUN_ID"
    exit 0
fi

log_info "Discovered run: $RUN_ID (agent: $AGENT_TYPE)"

# =============================================================================
# READ METADATA - Load context from .ralf-metadata if available
# =============================================================================

METADATA_FILE="$RUN_DIR/.ralf-metadata"
if [ -f "$METADATA_FILE" ]; then
    log "Loading metadata from .ralf-metadata..."
    # Source the metadata file for easy access to variables
    # This gives us: run_id, timestamp, project, agent_type, git_branch, git_commit
    while IFS=': ' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue
        # Clean up key and value
        key=$(echo "$key" | tr -d ' ' | tr '-' '_')
        value=$(echo "$value" | sed 's/^[ "]*//;s/[ "]*$//')
        # Export as variable
        export "meta_$key=$value" 2>/dev/null || true
    done < "$METADATA_FILE"
fi

# =============================================================================
# PHASE 7.1: VALIDATE COMPLETION
# =============================================================================

log "Phase 7.1: Validating completion..."

VALIDATION_FAILED=0

# Check for required files
for file in THOUGHTS.md RESULTS.md DECISIONS.md; do
    if [ ! -f "$RUN_DIR/$file" ]; then
        log_error "Missing required file: $file"
        VALIDATION_FAILED=1
    elif [ ! -s "$RUN_DIR/$file" ]; then
        log_warning "Empty file: $file"
    fi
done

# Check metadata.yaml exists
if [ ! -f "$RUN_DIR/metadata.yaml" ]; then
    log_error "Missing metadata.yaml"
    VALIDATION_FAILED=1
fi

if [ $VALIDATION_FAILED -eq 1 ]; then
    log_error "Validation failed - run incomplete"
    log_info "Run folder preserved at: ${RUN_DIR/#$HOME/~}"
    exit 0
fi

log_success "Validation passed"

# =============================================================================
# PHASE 7.2: UPDATE METADATA
# =============================================================================

log "Phase 7.2: Updating metadata..."

COMPLETION_TIME=$(date -Iseconds)

# Update metadata.yaml with completion timestamp
if [ -f "$RUN_DIR/metadata.yaml" ]; then
    # Use sed to update timestamp_end (macOS compatible)
    sed -i.bak "s/timestamp_end: null/timestamp_end: \"$COMPLETION_TIME\"/" "$RUN_DIR/metadata.yaml" 2>/dev/null || true
    rm -f "$RUN_DIR/metadata.yaml.bak"

    # Calculate duration if start timestamp exists
    START_TIME=$(grep "timestamp_start:" "$RUN_DIR/metadata.yaml" | cut -d'"' -f2)
    if [ -n "$START_TIME" ] && [ "$START_TIME" != "null" ]; then
        # Convert to epoch seconds and calculate duration
        START_EPOCH=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${START_TIME:0:19}" +%s 2>/dev/null || echo "0")
        END_EPOCH=$(date +%s)
        if [ "$START_EPOCH" != "0" ]; then
            DURATION=$((END_EPOCH - START_EPOCH))
            sed -i.bak "s/duration_seconds: null/duration_seconds: $DURATION/" "$RUN_DIR/metadata.yaml" 2>/dev/null || true
            rm -f "$RUN_DIR/metadata.yaml.bak"
        fi
    fi

    log_success "Metadata updated"
fi

# Update .ralf-metadata with completion info
cat >> "$RUN_DIR/.ralf-metadata" << EOF

# Completion Info (added by stop hook)
completion:
  timestamp: "$COMPLETION_TIME"
  status: archived
EOF

# =============================================================================
# PHASE 7.3: SYNC QUEUE (if executor completed a task)
# =============================================================================

log "Phase 7.3: Syncing queue..."

COMMUNICATIONS_DIR="$PROJECT_DIR/.autonomous/agents/communications"
QUEUE_FILE="$COMMUNICATIONS_DIR/queue.yaml"
EVENTS_FILE="$COMMUNICATIONS_DIR/events.yaml"

# Determine actual agent type from metadata or file content
ACTUAL_AGENT_TYPE="$AGENT_TYPE"
if [ -f "$RUN_DIR/THOUGHTS.md" ]; then
    # Try to detect agent type from THOUGHTS.md content
    if grep -q "Agent: executor" "$RUN_DIR/THOUGHTS.md" 2>/dev/null; then
        ACTUAL_AGENT_TYPE="executor"
    elif grep -q "Agent: planner" "$RUN_DIR/THOUGHTS.md" 2>/dev/null; then
        ACTUAL_AGENT_TYPE="planner"
    elif grep -q "Agent: architect" "$RUN_DIR/THOUGHTS.md" 2>/dev/null; then
        ACTUAL_AGENT_TYPE="architect"
    fi
fi

if [ "$ACTUAL_AGENT_TYPE" = "executor" ] && [ -f "$QUEUE_FILE" ]; then
    log "Executor run detected - checking for completed task..."

    # Find task claimed by this run (search by RUN_ID in claimed_by field)
    CURRENT_TASK=$(awk -F': ' -v run_id="$RUN_ID" '
        /^  - task_id: / { task_id = $2; gsub(/"/, "", task_id) }
        /^    claimed_by: / {
            claimed_by = $2
            gsub(/"/, "", claimed_by)
            if (claimed_by == run_id) {
                print task_id
                exit
            }
        }
    ' "$QUEUE_FILE" 2>/dev/null || echo "")

    if [ -n "$CURRENT_TASK" ]; then
        log "Found task claimed by this run: $CURRENT_TASK"

        # Mark task as completed in events
        if [ -f "$EVENTS_FILE" ]; then
            cat >> "$EVENTS_FILE" << EOF

- timestamp: "$COMPLETION_TIME"
  task_id: "$CURRENT_TASK"
  type: completed
  agent: executor
  run_id: "$RUN_ID"
EOF
            log_success "Task $CURRENT_TASK marked as completed in events"
        fi

        # Update queue.yaml - set task status to completed
        awk -F': ' -v task_id="$CURRENT_TASK" -v timestamp="$COMPLETION_TIME" '
            /^  - task_id: / {
                current_task = $2
                gsub(/"/, "", current_task)
                in_target_task = (current_task == task_id)
            }
            in_target_task && /^    status: / {
                print "    status: completed"
                print "    completed_at: \"" timestamp "\""
                next
            }
            { print }
        ' "$QUEUE_FILE" > "$QUEUE_FILE.tmp" && mv "$QUEUE_FILE.tmp" "$QUEUE_FILE"

        log_success "Task status updated to 'completed' in queue.yaml"

        # Move task from active/ to completed/
        TASK_ACTIVE_DIR="$PROJECT_DIR/tasks/active/$CURRENT_TASK"
        TASK_COMPLETED_DIR="$PROJECT_DIR/tasks/completed/$CURRENT_TASK"

        if [ -d "$TASK_ACTIVE_DIR" ]; then
            mkdir -p "$(dirname "$TASK_COMPLETED_DIR")"
            mv "$TASK_ACTIVE_DIR" "$TASK_COMPLETED_DIR"
            log_success "Task moved from active/ to completed/"
        fi

        # Archive task working directory
        TASK_WORKING_DIR="$PROJECT_DIR/tasks/working/$CURRENT_TASK/$RUN_ID"
        if [ -d "$TASK_WORKING_DIR" ]; then
            mkdir -p "$TASK_COMPLETED_DIR/working"
            mv "$TASK_WORKING_DIR" "$TASK_COMPLETED_DIR/working/"
            log_success "Task working directory archived"
        fi
    else
        log_info "No active task found for this run"
    fi
else
    log_info "Skipping queue sync (agent: $ACTUAL_AGENT_TYPE)"
fi

# =============================================================================
# PHASE 7.4: COMMIT CHANGES
# =============================================================================

log "Phase 7.4: Committing changes..."

if [ -d "$PROJECT_ROOT/.git" ]; then
    cd "$PROJECT_ROOT"

    # Check if there are changes to commit
    if ! git diff --quiet HEAD 2>/dev/null || ! git diff --cached --quiet HEAD 2>/dev/null; then
        # Stage all changes
        git add -A 2>/dev/null || true

        # Create commit message
        COMMIT_MSG="ralf: [$RUN_ID] [$ACTUAL_AGENT_TYPE] - run completion

- Phase 7: Archive completed
- Validation: passed
- Queue: synced
- Run: $RUN_ID"

        # Commit (may fail if no changes or pre-commit hooks fail)
        if git commit -m "$COMMIT_MSG" 2>/dev/null; then
            COMMIT_HASH=$(git rev-parse --short HEAD)
            log_success "Changes committed: $COMMIT_HASH"

            # Update metadata with commit hash
            if [ -f "$RUN_DIR/metadata.yaml" ]; then
                sed -i.bak "s/commit_hash: .*/commit_hash: \"$COMMIT_HASH\"/" "$RUN_DIR/metadata.yaml" 2>/dev/null || true
                rm -f "$RUN_DIR/metadata.yaml.bak"
            fi
        else
            log_warning "No changes to commit or commit failed"
        fi
    else
        log_info "No changes to commit"
    fi
else
    log_info "Not a git repository, skipping commit"
fi

# =============================================================================
# PHASE 7.5: ARCHIVE RUN FOLDER
# =============================================================================

log "Phase 7.5: Archiving run folder..."

# Create completed directory using the actual agent type
COMPLETED_DIR="$PROJECT_DIR/runs/$ACTUAL_AGENT_TYPE/completed"
mkdir -p "$COMPLETED_DIR"

# Move run folder to completed
ARCHIVE_DIR="$COMPLETED_DIR/$RUN_ID"

if [ -d "$ARCHIVE_DIR" ]; then
    log_warning "Archive directory already exists, removing old one"
    rm -rf "$ARCHIVE_DIR"
fi

mv "$RUN_DIR" "$ARCHIVE_DIR"

if [ -d "$ARCHIVE_DIR" ]; then
    log_success "Run archived to: ${ARCHIVE_DIR/#$HOME/~}"
else
    log_error "Archive failed"
fi

# =============================================================================
# SUMMARY
# =============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  RALF Run Completed & Archived"
echo "  Project: ${PROJECT_NAME}"
echo "  Agent: ${ACTUAL_AGENT_TYPE}"
echo "  Run: ${RUN_ID}"
echo "  Location: ${ARCHIVE_DIR/#$HOME/~}"
echo "═══════════════════════════════════════════════════════════════"
echo ""

exit 0
