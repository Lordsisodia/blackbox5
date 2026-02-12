#!/bin/bash
# RALF Stop Hook - Phase 6-7: Logging and Completion
#
# This hook runs when Claude stops a session and enforces:
# 1. Task completion validation
# 2. Queue synchronization
# 3. Git commit of changes
# 4. Finalize metadata.yaml
#
# Enforcement: Code-guaranteed (0ms LLM involvement)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
BLACKBOX5_HOME="${BLACKBOX5_HOME:-/opt/blackbox5}"
PROJECT_NAME="${PROJECT_NAME:-blackbox5}"
PROJECT_DIR="${BLACKBOX5_HOME}/5-project-memory/${PROJECT_NAME}"
AUTONOMOUS_DIR="${PROJECT_DIR}/.autonomous"
RUN_DIR="${RUN_DIR:-}"
QUEUE_FILE="${AUTONOMOUS_DIR}/communications/queue.yaml"

log() {
    echo -e "${GREEN}[StopHook]${NC} $1" >&2
}

warn() {
    echo -e "${YELLOW}[StopHook]${NC} $1" >&2
}

error() {
    echo -e "${RED}[StopHook]${NC} $1" >&2
}

info() {
    echo -e "${BLUE}[StopHook]${NC} $1" >&2
}

# Finalize metadata.yaml
finalize_metadata() {
    if [[ -n "$RUN_DIR" && -f "$RUN_DIR/metadata.yaml" ]]; then
        local metadata_file="$RUN_DIR/metadata.yaml"
        local start_time
        local end_time

        # Extract start_time from metadata
        start_time=$(grep "^metrics:" -A 3 "$metadata_file" | grep "start_time:" | awk '{print $2}' || echo "0")
        end_time=$(date +%s)

        # Calculate duration
        local duration=$(( (end_time - start_time) / 60 ))

        # Update metadata
        if command -v yq &> /dev/null; then
            yq eval -y -i ".run.status = \"completed\"" "$metadata_file"
            yq eval -y -i ".metrics.end_time = $end_time" "$metadata_file"
            yq eval -y -i ".metrics.duration_minutes = $duration" "$metadata_file"
        else
            # Fallback: sed-based update (less reliable)
            sed -i "s/status: in_progress/status: completed/" "$metadata_file"
            sed -i "s/end_time: null/end_time: $end_time/" "$metadata_file"
            sed -i "s/duration_minutes: null/duration_minutes: $duration/" "$metadata_file"
        fi

        log "Finalized metadata for run: $(basename "$RUN_DIR")"
    fi
}

# Validate task completion
validate_task_completion() {
    local task_id=""

    # Try to get task_id from metadata
    if [[ -n "$RUN_DIR" && -f "$RUN_DIR/metadata.yaml" ]]; then
        task_id=$(grep "^task:" -A 5 "$RUN_DIR/metadata.yaml" | grep "id:" | awk '{print $2}' || echo "")
    fi

    # If no task ID found, that's okay - may be a planner run or exploratory
    if [[ -z "$task_id" || "$task_id" == "TBD" ]]; then
        log "No task ID found - skipping task validation (may be planning run)"
        return 0
    fi

    log "Validating task completion: $task_id"

    # Check for required deliverables
    local required_files=(
        "$RUN_DIR/RESULTS.md"
    )

    local missing_files=()
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$(basename "$file")")
        fi
    done

    if [[ ${#missing_files[@]} -gt 0 ]]; then
        warn "Missing deliverables: ${missing_files[*]}"
        warn "Task may not be complete"
    else
        log "All required deliverables present"
    fi
}

# Sync task queue (enqueue completion)
sync_queue() {
    local task_id=""

    # Get task_id from metadata
    if [[ -n "$RUN_DIR" && -f "$RUN_DIR/metadata.yaml" ]]; then
        task_id=$(grep "^task:" -A 5 "$RUN_DIR/metadata.yaml" | grep "id:" | awk '{print $2}' || echo "")
    fi

    # Only enqueue if we have a valid task_id (not "TBD")
    if [[ -n "$task_id" && "$task_id" != "TBD" ]]; then
        log "Enqueuing task completion: $task_id"

        # Use bb5-tools to enqueue (if available)
        if [[ -f "$BLACKBOX5_HOME/bin/bb5-tools/enqueue-completion" ]]; then
            "$BLACKBOX5_HOME/bin/bb5-tools/enqueue-completion" "$task_id"
        else
            warn "enqueue-completion tool not found - task completion not queued"
            warn "Queue file: $QUEUE_FILE"
        fi
    fi
}

# Git commit of changes
git_commit() {
    cd "$PROJECT_DIR"

    # Check if git is available
    if ! command -v git &> /dev/null; then
        warn "git not available - skipping commit"
        return 0
    fi

    # Check if we're in a git repo
    if ! git rev-parse --git-dir &> /dev/null; then
        warn "Not in a git repository - skipping commit"
        return 0
    fi

    # Check for changes
    if git diff --quiet && git diff --cached --quiet; then
        log "No changes to commit"
        return 0
    fi

    # Create commit message
    local run_name=$(basename "$RUN_DIR")
    local commit_msg="[RALF] ${run_name}: Agent execution completed"

    # Stage all changes in autonomous directory
    git add -A

    # Commit
    git commit -m "$commit_msg" || {
        warn "Git commit failed - continuing anyway"
    }

    log "Git commit completed: $commit_msg"
}

# Generate run summary
generate_summary() {
    if [[ -n "$RUN_DIR" ]]; then
        info "=== RUN SUMMARY ==="
        info "Run Directory: $RUN_DIR"
        info "Files Modified: $(find "$RUN_DIR" -type f | wc -l)"

        if [[ -f "$RUN_DIR/metadata.yaml" ]]; then
            info ""
            info "Metadata:"
            grep -E "^(run|task|metrics):" "$RUN_DIR/metadata.yaml" | head -10
        fi

        if [[ -f "$RUN_DIR/RESULTS.md" ]]; then
            info ""
            info "Results Summary:"
            head -20 "$RUN_DIR/RESULTS.md"
        fi
        info "==================="
    fi
}

# Main execution
main() {
    log "Starting Stop hook..."

    # Ensure we're in project directory
    if [[ ! -d "$PROJECT_DIR" ]]; then
        error "Project directory not found: $PROJECT_DIR"
        exit 1
    fi

    # Execute all enforcement steps
    finalize_metadata
    validate_task_completion
    sync_queue
    git_commit
    generate_summary

    log "Stop hook complete. All enforcement steps executed."
}

# Run main function
main "$@"
