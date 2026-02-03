#!/bin/bash
# RALF Stop Hook
# Validates completion, syncs queue, commits, and archives run folder
# This is a COMMAND hook - runs bash directly, zero LLM tokens
#
# Triggered by: Stop event in .claude/settings.json
# Purpose: Enforce run completion and archive (Phase 7 of 7-phase execution flow)
#
# Usage: Automatically triggered when Claude Code session ends

set -e

# =============================================================================
# CONFIGURATION - Detect from environment or use defaults
# =============================================================================

PROJECT_NAME="${RALF_PROJECT_NAME:-blackbox5}"
AGENT_TYPE="${RALF_AGENT_TYPE:-unknown}"
RUN_ID="${RALF_RUN_ID:-unknown}"
RUN_DIR="${RALF_RUN_DIR:-}"

# Project root directory
if [ -n "$RALF_PROJECT_ROOT" ]; then
    PROJECT_ROOT="$RALF_PROJECT_ROOT"
elif [ -n "$CLAUDE_CODE_ROOT" ]; then
    PROJECT_ROOT="$CLAUDE_CODE_ROOT"
else
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

# Determine paths
PROJECT_MEMORY_DIR="$PROJECT_ROOT/5-project-memory/$PROJECT_NAME"
COMMUNICATIONS_DIR="$PROJECT_ROOT/2-engine/.autonomous/communications"

# Colors for output
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
    log_warning "RUN_DIR not set or doesn't exist: $RUN_DIR"
    log_info "Skipping archive - no run folder to process"
    exit 0
fi

if [ "$RUN_ID" = "unknown" ]; then
    log_warning "RUN_ID not set, cannot archive properly"
    exit 0
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

# =============================================================================
# PHASE 7.3: SYNC QUEUE (if executor completed a task)
# =============================================================================

log "Phase 7.3: Syncing queue..."

QUEUE_FILE="$COMMUNICATIONS_DIR/queue.yaml"
EVENTS_FILE="$COMMUNICATIONS_DIR/events.yaml"

if [ "$AGENT_TYPE" = "executor" ] && [ -f "$QUEUE_FILE" ]; then
    # Find task claimed by this run
    CURRENT_TASK=$(awk -F': ' -v run_id="$RUN_ID" '
        /^  - task_id: / { task_id = $2 }
        /^    claimed_by: / { claimed_by = $2; gsub(/"/, "", claimed_by) }
        claimed_by == run_id { print task_id; exit }
    ' "$QUEUE_FILE" 2>/dev/null || echo "")

    if [ -n "$CURRENT_TASK" ]; then
        log "Found in-progress task: $CURRENT_TASK"

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
                in_target_task = ($2 == task_id)
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
        TASK_ACTIVE_DIR="$PROJECT_MEMORY_DIR/tasks/active/$CURRENT_TASK"
        TASK_COMPLETED_DIR="$PROJECT_MEMORY_DIR/tasks/completed/$CURRENT_TASK"

        if [ -d "$TASK_ACTIVE_DIR" ]; then
            mkdir -p "$(dirname "$TASK_COMPLETED_DIR")"
            mv "$TASK_ACTIVE_DIR" "$TASK_COMPLETED_DIR"
            log_success "Task moved from active/ to completed/"
        fi

        # Archive task working directory
        TASK_WORKING_DIR="$PROJECT_MEMORY_DIR/tasks/working/$CURRENT_TASK/$RUN_ID"
        if [ -d "$TASK_WORKING_DIR" ]; then
            mkdir -p "$TASK_COMPLETED_DIR/working"
            mv "$TASK_WORKING_DIR" "$TASK_COMPLETED_DIR/working/"
            log_success "Task working directory archived"
        fi
    else
        log_info "No active task found for this run"
    fi
else
    log_info "Skipping queue sync (not executor or no queue file)"
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
        COMMIT_MSG="ralf: [$RUN_ID] [$AGENT_TYPE] - run completion

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

# Create completed directory
COMPLETED_DIR="$PROJECT_MEMORY_DIR/runs/$AGENT_TYPE/completed"
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
echo "  Agent: ${AGENT_TYPE}"
echo "  Run: ${RUN_ID}"
echo "  Location: ${ARCHIVE_DIR/#$HOME/~}"
echo "═══════════════════════════════════════════════════════════════"
echo ""

exit 0
