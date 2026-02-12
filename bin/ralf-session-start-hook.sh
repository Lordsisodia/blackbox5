#!/bin/bash
# RALF SessionStart Hook - Phase 1: Runtime Initialization
#
# This hook runs when Claude starts a session and ensures:
# 1. Run folder exists (created by ralf-loop.sh or this hook)
# 2. Required template files are created
# 3. Environment is validated
#
# Enforcement: Code-guaranteed (0ms LLM involvement)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paths
BLACKBOX5_HOME="${BLACKBOX5_HOME:-/opt/blackbox5}"
PROJECT_NAME="${PROJECT_NAME:-blackbox5}"
PROJECT_DIR="${BLACKBOX5_HOME}/5-project-memory/${PROJECT_NAME}"
AUTONOMOUS_DIR="${PROJECT_DIR}/.autonomous"
RUN_DIR="${RUN_DIR:-}"

# Template files (simplified 4-file structure)
TEMPLATES=(
    "THOUGHTS.md"
    "RESULTS.md"
    "DECISIONS.md"
    "metadata.yaml"
)

log() {
    echo -e "${GREEN}[SessionStart]${NC} $1" >&2
}

warn() {
    echo -e "${YELLOW}[SessionStart]${NC} $1" >&2
}

error() {
    echo -e "${RED}[SessionStart]${NC} $1" >&2
}

# Create run folder if it doesn't exist
ensure_run_folder() {
    if [[ -z "$RUN_DIR" ]]; then
        # No RUN_DIR set by loop script - create one
        TIMESTAMP=$(date +%Y%m%d-%H%M%S)
        RUN_DIR="${AUTONOMOUS_DIR}/runs/run-${TIMESTAMP}"
        mkdir -p "$RUN_DIR"
        log "Created run folder: $RUN_DIR"
    else
        # RUN_DIR exists - verify it's valid
        if [[ ! -d "$RUN_DIR" ]]; then
            error "RUN_DIR set but doesn't exist: $RUN_DIR"
            exit 1
        fi
        log "Using existing run folder: $RUN_DIR"
    fi
}

# Create template files
create_templates() {
    for template in "${TEMPLATES[@]}"; do
        local template_path="$RUN_DIR/$template"

        if [[ ! -f "$template_path" ]]; then
            case "$template" in
                "THOUGHTS.md")
                    cat > "$template_path" << 'EOF'
# THOUGHTS.md - Narrative Reasoning

This file captures the thought process and reasoning during this run.

## Initial Thoughts

- Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
- Agent: Claude (RALF executor)
- Task: TBD

## Reasoning Chain

[Document your thinking process here as you work through the task]

## Key Insights

[Any major realizations or breakthroughs]

## Assumptions Made

[Any assumptions you're making - should be verified later]

---

*Last updated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")*
EOF
                    ;;

                "RESULTS.md")
                    cat > "$template_path" << 'EOF'
# RESULTS.md - Outcomes

This file captures what actually happened during this run.

## Summary

[Brief description of what was accomplished]

## Deliverables Created

- [ ] File/feature 1
- [ ] File/feature 2
- [ ] Documentation updated

## Test Results

[Any tests run and their outcomes]

## Issues Encountered

[Any problems found and how they were resolved]

## Metrics

- Duration: TBD
- Files modified: TBD
- Lines added/removed: TBD

---

*Last updated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")*
EOF
                    ;;

                "DECISIONS.md")
                    cat > "$template_path" << 'EOF'
# DECISIONS.md - Key Choices

This file captures important decisions and the rationale behind them.

## Decision 1: [Title]

**Date:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")

**Context:** [Why this decision was needed]

**Options Considered:**
1. Option A - [pros/cons]
2. Option B - [pros/cons]

**Decision Chosen:** Option B

**Rationale:** [Why this option was selected]

**Impact:** [What effect this has on the system]

---

## Future Decisions

[Any pending decisions that need to be made later]

---

*Last updated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")*
EOF
                    ;;

                "metadata.yaml")
                    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
                    cat > "$template_path" << EOF
# Run Metadata
# This file tracks state, learnings, and assumptions for this run

run:
  id: "run-${TIMESTAMP}"
  timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
  agent: claude
  role: executor
  status: in_progress

task:
  id: "TBD"
  title: "TBD"
  priority: "TBD"
  type: "TBD"  # architecture, feature, fix, etc.

context:
  previous_runs: []
  dependencies: []

learnings: []
assumptions: []

# Track metrics for ROI calculation
metrics:
  start_time: $(date +%s)
  end_time: null
  duration_minutes: null
  files_modified: 0
  lines_added: 0
  lines_removed: 0

# Track skill usage (if applicable)
skill_used: null
skill_effectiveness: null
EOF
                    ;;
            esac

            log "Created template: $template"
        fi
    done
}

# Validate environment
validate_environment() {
    # Check BlackBox5 structure
    if [[ ! -d "$BLACKBOX5_HOME" ]]; then
        error "BlackBox5 home not found: $BLACKBOX5_HOME"
        exit 1
    fi

    if [[ ! -d "$AUTONOMOUS_DIR" ]]; then
        error "Autonomous directory not found: $AUTONOMOUS_DIR"
        exit 1
    fi

    # Check for critical directories
    local critical_dirs=(
        "$AUTONOMOUS_DIR/skills"
        "$AUTONOMOUS_DIR/prompts"
        "$AUTONOMOUS_DIR/lib"
    )

    for dir in "${critical_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            warn "Missing critical directory: $dir"
        fi
    done
}

# Main execution
main() {
    log "Starting SessionStart hook..."

    validate_environment
    ensure_run_folder
    create_templates

    log "SessionStart hook complete. Run folder: $RUN_DIR"
}

# Run main function
main "$@"
