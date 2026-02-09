#!/bin/bash
# RALF Verifier Agent Script
# Runs verification suite on completed executor tasks
# Decides: AUTO_COMMIT | QUEUE_REVIEW | HUMAN_REVIEW

set -e

# =============================================================================
# SELF-DISCOVERY
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Source libraries
source "${SCRIPT_DIR}/../../2-engine/helpers/legacy/paths.sh"
source "${SCRIPT_DIR}/../../2-engine/helpers/legacy/error_handler.sh"

PROJECT_NAME="${RALF_PROJECT_NAME:-blackbox5}"
PROJECT_DIR="$(get_project_path)"
COMMUNICATIONS_DIR="$(get_project_path)/.autonomous/agents/communications"

# Ensure communications directory exists
if ! eh_dir_exists "$COMMUNICATIONS_DIR" "communications"; then
    eh_ensure_dir "$COMMUNICATIONS_DIR" || {
        error "Cannot create communications directory"
        exit 1
    }
fi

EVENTS_FILE="$COMMUNICATIONS_DIR/events.yaml"
VERIFY_FILE="$COMMUNICATIONS_DIR/verify.yaml"
HUMAN_REVIEW_FILE="$COMMUNICATIONS_DIR/human-review.yaml"
QUEUE_FILE="$COMMUNICATIONS_DIR/queue.yaml"

# Thresholds
THRESHOLD_AUTO="${RALF_VERIFY_THRESHOLD_AUTO:-0.85}"
THRESHOLD_REVIEW="${RALF_VERIFY_THRESHOLD_REVIEW:-0.60}"
MAX_RETRIES="${RALF_VERIFY_MAX_RETRIES:-2}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${BLUE}[VERIFIER]${NC} $1"; }
success() { echo -e "${GREEN}[VERIFIER]${NC} $1"; }
warning() { echo -e "${YELLOW}[VERIFIER]${NC} $1"; }
error() { echo -e "${RED}[VERIFIER]${NC} $1"; }
info() { echo -e "${CYAN}[VERIFIER]${NC} $1"; }

# =============================================================================
# VERIFICATION FUNCTIONS
# =============================================================================

verify_files_exist() {
    local task_id=$1
    local task_dir="$PROJECT_DIR/tasks/active/$task_id"

    if [ ! -d "$task_dir" ]; then
        echo "FAIL: Task directory not found"
        return 1
    fi

    # Check task.md exists
    if [ ! -f "$task_dir/task.md" ]; then
        echo "FAIL: task.md not found"
        return 1
    fi

    echo "PASS"
}

verify_code_imports() {
    local task_id=$1

    # Check if events file exists for comparison
    if ! eh_file_exists "$EVENTS_FILE" "code import verification"; then
        echo "SKIP: events.yaml not found, cannot determine modified files"
        return 0
    fi

    # Find modified Python files
    local py_files=$(find "$PROJECT_ROOT" -name "*.py" -newer "$EVENTS_FILE" 2>/dev/null | head -10)

    if [ -z "$py_files" ]; then
        echo "SKIP: No Python files modified"
        return 0
    fi

    local failures=0
    for file in $py_files; do
        if ! python3 -m py_compile "$file" 2>/dev/null; then
            error "Syntax error in $file"
            failures=$((failures + 1))
        fi
    done

    if [ $failures -gt 0 ]; then
        echo "FAIL: $failures files have syntax errors"
        return 1
    fi

    echo "PASS"
}

verify_tests() {
    local task_id=$1

    # Check if test files exist
    if [ ! -d "$PROJECT_ROOT/tests" ]; then
        echo "SKIP: No tests directory"
        return 0
    fi

    # Run tests (if pytest available)
    if command -v pytest &> /dev/null; then
        if pytest "$PROJECT_ROOT/tests" -x --tb=short -q 2>/dev/null; then
            echo "PASS"
            return 0
        else
            echo "FAIL: Tests failed"
            return 1
        fi
    fi

    echo "SKIP: pytest not available"
    return 0
}

verify_lint() {
    local task_id=$1

    # Find modified files
    local files=$(git -C "$PROJECT_ROOT" diff --name-only HEAD 2>/dev/null | head -20)

    if [ -z "$files" ]; then
        echo "SKIP: No modified files"
        return 0
    fi

    # Check Python files
    local py_files=$(echo "$files" | grep '\.py$' || true)
    if [ -n "$py_files" ] && command -v flake8 &> /dev/null; then
        if echo "$py_files" | xargs flake8 --max-line-length=120 2>/dev/null; then
            echo "PASS"
            return 0
        else
            echo "FAIL: Linting errors"
            return 1
        fi
    fi

    echo "SKIP: No lintable files or linter not available"
    return 0
}

verify_documentation() {
    local task_id=$1

    # Check if runs directory exists
    if ! eh_dir_exists "$PROJECT_DIR/runs" "runs directory"; then
        echo "SKIP: No runs directory found"
        return 0
    fi

    # Find the most recent run folder for this task
    local run_dir=$(find "$PROJECT_DIR/runs" -name "run-*" -type d -exec stat -f "%m %N" {} \; 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

    if [ -z "$run_dir" ]; then
        echo "SKIP: No run folder found"
        return 0
    fi

    # Check required files
    local missing=0
    local empty=0
    for file in THOUGHTS.md RESULTS.md DECISIONS.md; do
        if ! eh_file_exists "$run_dir/$file" "documentation check"; then
            error "Missing $file"
            missing=$((missing + 1))
        elif [ ! -s "$run_dir/$file" ]; then
            warning "Empty $file"
            empty=$((empty + 1))
        fi
    done

    if [ $missing -gt 0 ]; then
        echo "FAIL: $missing required files missing"
        return 1
    fi

    if [ $empty -gt 0 ]; then
        warning "$empty documentation files are empty"
    fi

    echo "PASS"
}

verify_git() {
    local task_id=$1

    cd "$PROJECT_ROOT"

    # Check if there are changes to commit
    if git diff --cached --quiet HEAD 2>/dev/null && git diff --quiet HEAD 2>/dev/null; then
        echo "FAIL: No changes to commit"
        return 1
    fi

    # Check for merge conflicts
    if git diff --name-only --diff-filter=U | grep -q .; then
        echo "FAIL: Merge conflicts detected"
        return 1
    fi

    echo "PASS"
}

# =============================================================================
# SCORING
# =============================================================================

calculate_confidence() {
    local results="$1"

    # Weights
    local w_file=20
    local w_import=15
    local w_test=20
    local w_lint=10
    local w_doc=20
    local w_git=15

    local score=0

    if echo "$results" | grep -q "file_existence:PASS"; then
        score=$((score + w_file))
    fi
    if echo "$results" | grep -q "code_imports:PASS"; then
        score=$((score + w_import))
    elif echo "$results" | grep -q "code_imports:SKIP"; then
        score=$((score + w_import / 2))
    fi
    if echo "$results" | grep -q "tests:PASS"; then
        score=$((score + w_test))
    elif echo "$results" | grep -q "tests:SKIP"; then
        score=$((score + w_test / 2))
    fi
    if echo "$results" | grep -q "lint:PASS"; then
        score=$((score + w_lint))
    elif echo "$results" | grep -q "lint:SKIP"; then
        score=$((score + w_lint / 2))
    fi
    if echo "$results" | grep -q "documentation:PASS"; then
        score=$((score + w_doc))
    fi
    if echo "$results" | grep -q "git:PASS"; then
        score=$((score + w_git))
    fi

    # Convert to 0.00-1.00
    echo "scale=2; $score / 100" | bc
}

# =============================================================================
# DECISION & ACTION
# =============================================================================

decide_action() {
    local confidence=$1

    if (( $(echo "$confidence >= $THRESHOLD_AUTO" | bc -l) )); then
        echo "AUTO_COMMIT"
    elif (( $(echo "$confidence >= $THRESHOLD_REVIEW" | bc -l) )); then
        echo "QUEUE_REVIEW"
    else
        echo "HUMAN_REVIEW"
    fi
}

auto_commit() {
    local task_id=$1
    local confidence=$2
    local results="$3"

    cd "$PROJECT_ROOT"

    # Stage and commit
    git add -A

    local commit_msg="ralf: [$task_id] verified auto-commit

- Confidence: $confidence
- Verifier: ${RALF_RUN_ID:-unknown}
- Auto-committed: true"

    if git commit -m "$commit_msg" 2>/dev/null; then
        local commit_hash=$(git rev-parse --short HEAD)
        success "Auto-committed: $commit_hash"

        # Push if configured
        if [ -n "$RALF_AUTO_PUSH" ]; then
            git push origin HEAD 2>/dev/null || warning "Push failed"
        fi

        echo "$commit_hash"
        return 0
    else
        error "Commit failed"
        return 1
    fi
}

queue_review() {
    local task_id=$1
    local confidence=$2
    local results="$3"
    local executor_run=$4

    # Ensure verify file exists
    if ! eh_file_exists "$VERIFY_FILE" "queue review"; then
        eh_ensure_dir "$(dirname "$VERIFY_FILE")"
        echo "# Verification queue" > "$VERIFY_FILE"
    fi

    # Add to verify queue for another agent (with file locking)
    (
        flock -x 200
        cat >> "$VERIFY_FILE" << EOF

- task_id: "$task_id"
  status: pending_review
  confidence: $confidence
  executor_run: "$executor_run"
  verifier_run: "${RALF_RUN_ID:-unknown}"
  created_at: "$(date -Iseconds)"
  reason: "Medium confidence ($confidence), needs second opinion"
EOF
    ) 200>"$COMMUNICATIONS_DIR/.verify.lock"

    success "Queued for review: $task_id"
}

human_review() {
    local task_id=$1
    local confidence=$2
    local results="$3"
    local failures="$4"
    local executor_run=$5

    # Ensure human review file exists
    if ! eh_file_exists "$HUMAN_REVIEW_FILE" "human review"; then
        eh_ensure_dir "$(dirname "$HUMAN_REVIEW_FILE")"
        echo "# Human review queue" > "$HUMAN_REVIEW_FILE"
    fi

    # Add to human review queue (with file locking)
    (
        flock -x 200
        cat >> "$HUMAN_REVIEW_FILE" << EOF

- task_id: "$task_id"
  status: human_required
  confidence: $confidence
  failures: "$failures"
  executor_run: "$executor_run"
  created_at: "$(date -Iseconds)"
EOF
    ) 200>"$COMMUNICATIONS_DIR/.human-review.lock"

    # Notify if webhook configured
    if [ -n "$RALF_NOTIFY_WEBHOOK" ]; then
        curl -s -X POST "$RALF_NOTIFY_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"task\": \"$task_id\", \"confidence\": $confidence, \"action\": \"human_review\"}" \
            2>/dev/null || true
    fi

    warning "Escalated to human review: $task_id"
}

# =============================================================================
# MAIN VERIFICATION LOOP
# =============================================================================

verify_task() {
    local task_id=$1
    local executor_run=$2

    log "Verifying task: $task_id"

    # Run verification suite
    local results=""
    local failures=""

    info "Checking file existence..."
    local result=$(verify_files_exist "$task_id")
    results="${results}file_existence:$result;"
    if [ "$result" = "FAIL" ]; then
        failures="${failures}file_existence,"
    fi

    info "Checking code imports..."
    result=$(verify_code_imports "$task_id")
    results="${results}code_imports:$result;"
    if [ "$result" = "FAIL" ]; then
        failures="${failures}code_imports,"
    fi

    info "Running tests..."
    result=$(verify_tests "$task_id")
    results="${results}tests:$result;"
    if [ "$result" = "FAIL" ]; then
        failures="${failures}tests,"
    fi

    info "Checking lint..."
    result=$(verify_lint "$task_id")
    results="${results}lint:$result;"
    if [ "$result" = "FAIL" ]; then
        failures="${failures}lint,"
    fi

    info "Checking documentation..."
    result=$(verify_documentation "$task_id")
    results="${results}documentation:$result;"
    if [ "$result" = "FAIL" ]; then
        failures="${failures}documentation,"
    fi

    info "Checking git state..."
    result=$(verify_git "$task_id")
    results="${results}git:$result;"
    if [ "$result" = "FAIL" ]; then
        failures="${failures}git,"
    fi

    # Calculate confidence
    local confidence=$(calculate_confidence "$results")
    info "Confidence score: $confidence"

    # Decide action
    local action=$(decide_action "$confidence")
    info "Decision: $action"

    # Execute decision
    case "$action" in
        AUTO_COMMIT)
            local commit_hash=$(auto_commit "$task_id" "$confidence" "$results")
            ;;
        QUEUE_REVIEW)
            queue_review "$task_id" "$confidence" "$results" "$executor_run"
            ;;
        HUMAN_REVIEW)
            human_review "$task_id" "$confidence" "$results" "$failures" "$executor_run"
            ;;
    esac

    # Log verification (with file locking)
    # Ensure verify file exists
    if ! eh_file_exists "$VERIFY_FILE" "verification logging"; then
        eh_ensure_dir "$(dirname "$VERIFY_FILE")"
        echo "# Verification log" > "$VERIFY_FILE"
    fi

    (
        flock -x 200
        cat >> "$VERIFY_FILE" << EOF

- task_id: "$task_id"
  timestamp: "$(date -Iseconds)"
  verifier_run: "${RALF_RUN_ID:-unknown}"
  executor_run: "$executor_run"
  confidence: $confidence
  decision: $action
  results: "$results"
  commit_hash: "${commit_hash:-null}"
  status: "${action,,}"
EOF
    ) 200>"$COMMUNICATIONS_DIR/.verify.lock"

    log "Verification complete for $task_id"
}

# =============================================================================
# POLLING LOOP
# =============================================================================

poll_for_completions() {
    log "Starting verifier polling loop..."
    log "Thresholds: AUTO=$THRESHOLD_AUTO, REVIEW=$THRESHOLD_REVIEW"

    local last_check=""

    while true; do
        # Check for new completion events
        if eh_file_exists "$EVENTS_FILE" "polling for completions"; then
            # Find completed events we haven't processed
            local new_completions=$(grep -A 5 "type: completed" "$EVENTS_FILE" 2>/dev/null | grep -B 3 "agent: executor" || true)

            if [ -n "$new_completions" ] && [ "$new_completions" != "$last_check" ]; then
                # Extract task_id and run_id
                local task_id=$(echo "$new_completions" | grep "task_id:" | tail -1 | cut -d':' -f2 | tr -d ' "')
                local run_id=$(echo "$new_completions" | grep "run_id:" | tail -1 | cut -d':' -f2 | tr -d ' "')

                if [ -n "$task_id" ]; then
                    verify_task "$task_id" "$run_id"
                fi

                last_check="$new_completions"
            fi
        else
            warning "events.yaml not found - waiting for it to be created"
        fi

        # Sleep before next poll
        sleep 10
    done
}

# =============================================================================
# CLI
# =============================================================================

case "${1:---poll}" in
    --poll|-p)
        poll_for_completions
        ;;
    --verify|-v)
        if [ -z "$2" ]; then
            error "Usage: $0 --verify TASK-ID"
            exit 1
        fi
        verify_task "$2" "manual"
        ;;
    --thresholds|-t)
        info "Current thresholds:"
        echo "  AUTO_COMMIT: >= $THRESHOLD_AUTO"
        echo "  QUEUE_REVIEW: $THRESHOLD_REVIEW - $THRESHOLD_AUTO"
        echo "  HUMAN_REVIEW: < $THRESHOLD_REVIEW"
        ;;
    --help|-h)
        echo "RALF Verifier Agent"
        echo ""
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  --poll, -p       Poll for completed tasks (default)"
        echo "  --verify TASK    Verify specific task"
        echo "  --thresholds, -t Show confidence thresholds"
        echo "  --help, -h       Show this help"
        echo ""
        echo "Environment:"
        echo "  RALF_VERIFY_THRESHOLD_AUTO   Auto-commit threshold (default: 0.85)"
        echo "  RALF_VERIFY_THRESHOLD_REVIEW Review queue threshold (default: 0.60)"
        echo "  RALF_NOTIFY_WEBHOOK          Notification webhook URL"
        echo "  RALF_AUTO_PUSH               Auto-push after commit"
        ;;
    *)
        error "Unknown command: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac
