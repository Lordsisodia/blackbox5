#!/bin/bash
# RALF Session Start Hook
# Creates run folder and templates when Claude Code starts
# This is a COMMAND hook - runs bash directly, zero LLM tokens
#
# Triggered by: SessionStart event in .claude/settings.json
# Purpose: Enforce run folder structure (Phase 1 of 7-phase execution flow)
#
# Usage: Set these environment variables before running Claude:
#   export RALF_PROJECT_NAME="blackbox5"
#   export RALF_AGENT_TYPE="executor"  # or "planner", "architect"
#   export RALF_PROJECT_ROOT="/Users/shaansisodia/.blackbox5"

set -e

# =============================================================================
# CONFIGURATION - Detect from environment or use defaults
# =============================================================================

# Project name (e.g., "blackbox5", "siso-internal")
PROJECT_NAME="${RALF_PROJECT_NAME:-blackbox5}"

# Agent type (planner/executor/architect)
AGENT_TYPE="${RALF_AGENT_TYPE:-unknown}"

# Project root directory
if [ -n "$RALF_PROJECT_ROOT" ]; then
    PROJECT_ROOT="$RALF_PROJECT_ROOT"
elif [ -n "$CLAUDE_CODE_ROOT" ]; then
    # Claude Code sets this when it starts
    PROJECT_ROOT="$CLAUDE_CODE_ROOT"
else
    # Fallback: detect from hook location
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

# Determine project memory path based on project name
# This follows the SISO standard: 5-project-memory/{project}/
PROJECT_MEMORY_DIR="$PROJECT_ROOT/5-project-memory/$PROJECT_NAME"
RUNS_DIR="$PROJECT_MEMORY_DIR/runs"

# Generate run ID from timestamp
RUN_TIMESTAMP=$(date +%Y%m%d-%H%M%S)
RUN_ID="run-$RUN_TIMESTAMP"
RUN_DIR="$RUNS_DIR/$AGENT_TYPE/$RUN_ID"

# Uppercase agent type for display (bash 3.x compatible)
AGENT_TYPE_UPPER=$(echo "$AGENT_TYPE" | tr '[:lower:]' '[:upper:]')

# Colors for output (only if terminal supports it)
if [ -t 1 ]; then
    BLUE='\033[0;34m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    CYAN='\033[0;36m'
    NC='\033[0m'
else
    BLUE=''
    GREEN=''
    YELLOW=''
    CYAN=''
    NC=''
fi

log() {
    echo -e "${BLUE}[RALF-HOOK]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[RALF-HOOK]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[RALF-HOOK]${NC} $1"
}

log_info() {
    echo -e "${CYAN}[RALF-HOOK]${NC} $1"
}

# =============================================================================
# VALIDATION
# =============================================================================

# Check if project memory directory exists
if [ ! -d "$PROJECT_MEMORY_DIR" ]; then
    log_warning "Project memory directory not found: $PROJECT_MEMORY_DIR"
    log_info "Creating directory structure..."
    mkdir -p "$PROJECT_MEMORY_DIR/runs/$AGENT_TYPE"
fi

# Check if we're in a git repo (for git info in metadata)
GIT_BRANCH="unknown"
GIT_COMMIT="unknown"
if [ -d "$PROJECT_ROOT/.git" ]; then
    GIT_BRANCH=$(cd "$PROJECT_ROOT" && git branch --show-current 2>/dev/null || echo "unknown")
    GIT_COMMIT=$(cd "$PROJECT_ROOT" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")
fi

# =============================================================================
# RUN FOLDER CREATION
# =============================================================================

log "SessionStart hook fired"
log_info "Project: $PROJECT_NAME"
log_info "Agent: $AGENT_TYPE"
log_info "Run ID: $RUN_ID"

# Create run directory if it doesn't exist
if [ ! -d "$RUN_DIR" ]; then
    mkdir -p "$RUN_DIR"
    log "Created run directory: ${RUN_DIR/#$HOME/~}"
else
    log "Run directory exists: ${RUN_DIR/#$HOME/~}"
fi

# Export RUN_DIR so the agent can use it
export RALF_RUN_DIR="$RUN_DIR"
export RALF_RUN_ID="$RUN_ID"
export RALF_AGENT_TYPE="$AGENT_TYPE"
export RALF_PROJECT_NAME="$PROJECT_NAME"

# Create a marker file to indicate hook ran successfully
HOOK_MARKER="$RUN_DIR/.hook_initialized"
echo "$(date -Iseconds)" > "$HOOK_MARKER"

# =============================================================================
# TEMPLATE CREATION (idempotent - only if files don't exist)
# =============================================================================

TEMPLATES_CREATED=0

# THOUGHTS.md - Narrative reasoning (100% usage based on analysis)
if [ ! -f "$RUN_DIR/THOUGHTS.md" ]; then
cat > "$RUN_DIR/THOUGHTS.md" << EOF
# THOUGHTS - ${AGENT_TYPE_UPPER} Run ${RUN_ID}

**Project:** ${PROJECT_NAME}
**Agent:** ${AGENT_TYPE}
**Run ID:** ${RUN_ID}
**Started:** $(date '+%Y-%m-%d %H:%M:%S')

---

## State Assessment

### Current System Status
- **Active Tasks:**
- **Queue Depth:**
- **Previous Run Status:**

### Context
- **Git Branch:** ${GIT_BRANCH}
- **Git Commit:** ${GIT_COMMIT}

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
    TEMPLATES_CREATED=$((TEMPLATES_CREATED + 1))
fi

# RESULTS.md - Outcomes (99% usage)
if [ ! -f "$RUN_DIR/RESULTS.md" ]; then
cat > "$RUN_DIR/RESULTS.md" << EOF
# RESULTS - ${AGENT_TYPE_UPPER} Run ${RUN_ID}

**Project:** ${PROJECT_NAME}
**Status:** in_progress
**Started:** $(date '+%Y-%m-%d %H:%M:%S')
**Completed:**

---

## Summary

[What was accomplished in this run]

---

## Tasks Completed

- [ ]

---

## Tasks Created

-

---

## Blockers

- None

---

*Hook-generated template. Edit as needed.*
EOF
    TEMPLATES_CREATED=$((TEMPLATES_CREATED + 1))
fi

# DECISIONS.md - Key choices (97% usage)
if [ ! -f "$RUN_DIR/DECISIONS.md" ]; then
cat > "$RUN_DIR/DECISIONS.md" << EOF
# DECISIONS - ${AGENT_TYPE_UPPER} Run ${RUN_ID}

**Project:** ${PROJECT_NAME}
**Run:** ${RUN_ID}
**Date:** $(date '+%Y-%m-%d')

---

## Decisions Made

### D-001: [Decision Title]

**Context:**
**Decision:**
**Rationale:**
**Consequences:**

---

*Hook-generated template. Edit as needed.*
EOF
    TEMPLATES_CREATED=$((TEMPLATES_CREATED + 1))
fi

# metadata.yaml - State + merged learnings + merged assumptions (76% usage)
if [ ! -f "$RUN_DIR/metadata.yaml" ]; then
cat > "$RUN_DIR/metadata.yaml" << EOF
# =============================================================================
# RUN METADATA - ${PROJECT_NAME} ${AGENT_TYPE_UPPER} ${RUN_ID}
# =============================================================================

run:
  id: "${RUN_ID}"
  project: "${PROJECT_NAME}"
  agent: "${AGENT_TYPE}"
  timestamp_start: "$(date -Iseconds)"
  timestamp_end: null
  duration_seconds: null

state:
  active_tasks_count: 0
  completed_tasks_count: 0
  queue_depth: 0
  git_branch: "${GIT_BRANCH}"
  git_commit: "${GIT_COMMIT}"

results:
  status: "in_progress"
  summary: ""
  tasks_completed: []
  tasks_created: []
  blockers: []

decisions: []

# Merged from LEARNINGS.md (13% usage - low, so merged into metadata)
learnings: []
#  - discovery: ""
#    description: ""
#    impact: "low|medium|high"
#    action: ""

# Merged from ASSUMPTIONS.md (12% usage - low, so merged into metadata)
assumptions: []
#  - assumption: ""
#    verified: false
#    evidence: ""
EOF
    TEMPLATES_CREATED=$((TEMPLATES_CREATED + 1))
fi

# =============================================================================
# SUMMARY OUTPUT
# =============================================================================

if [ $TEMPLATES_CREATED -gt 0 ]; then
    log_success "Created $TEMPLATES_CREATED template files"
fi

log_success "Run folder initialized"

# Output for Claude to see (formatted for visibility)
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  RALF Run Initialized"
echo "  Project: ${PROJECT_NAME}"
echo "  Agent: ${AGENT_TYPE}"
echo "  Run: ${RUN_ID}"
echo "  Location: ${RUN_DIR/#$HOME/~}"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Environment variables set:"
echo "  RALF_RUN_DIR=${RUN_DIR}"
echo "  RALF_RUN_ID=${RUN_ID}"
echo "  RALF_AGENT_TYPE=${AGENT_TYPE}"
echo "  RALF_PROJECT_NAME=${PROJECT_NAME}"
