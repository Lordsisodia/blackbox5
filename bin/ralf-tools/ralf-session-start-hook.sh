#!/bin/bash
# RALF Session Start Hook - Self-Discovering Version
# Creates run folder and templates when Claude Code starts
#
# Triggered by: SessionStart event in .claude/settings.json
# Purpose: Enforce run folder structure (Phase 1 of 7-phase execution flow)
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

# Discover available projects
PROJECT_MEMORY_DIR="$PROJECT_ROOT/5-project-memory"
if [ ! -d "$PROJECT_MEMORY_DIR" ]; then
    echo "[RALF-HOOK] ERROR: Project memory not found at $PROJECT_MEMORY_DIR"
    exit 1
fi

# For now, use blackbox5 as default (can be made configurable)
PROJECT_NAME="blackbox5"
PROJECT_DIR="$PROJECT_MEMORY_DIR/$PROJECT_NAME"

if [ ! -d "$PROJECT_DIR" ]; then
    # Fallback: use first available project
    PROJECT_NAME=$(ls -1 "$PROJECT_MEMORY_DIR" | head -1)
    PROJECT_DIR="$PROJECT_MEMORY_DIR/$PROJECT_NAME"
fi

# =============================================================================
# AGENT TYPE DISCOVERY
# =============================================================================

# Strategy: Check if we're being called in context of a specific agent
# The agent type can be determined by:
# 1. Prompt content (if we could read it)
# 2. Working directory patterns
# 3. Default to "unknown" and let agent self-identify later

AGENT_TYPE="unknown"
RUN_TIMESTAMP=$(date +%Y%m%d-%H%M%S)
RUN_ID="run-$RUN_TIMESTAMP"

# Create runs directory structure
RUNS_DIR="$PROJECT_DIR/runs"
mkdir -p "$RUNS_DIR"

# For now, create in "unknown" - agent will move or reclassify
RUN_DIR="$RUNS_DIR/$AGENT_TYPE/$RUN_ID"
mkdir -p "$RUN_DIR"

# =============================================================================
# METADATA - Write self-describing metadata file
# =============================================================================

TIMESTAMP=$(date -Iseconds)
GIT_BRANCH="unknown"
GIT_COMMIT="unknown"

if [ -d "$PROJECT_ROOT/.git" ]; then
    GIT_BRANCH=$(cd "$PROJECT_ROOT" && git branch --show-current 2>/dev/null || echo "unknown")
    GIT_COMMIT=$(cd "$PROJECT_ROOT" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")
fi

# Write metadata file that other hooks can read
cat > "$RUN_DIR/.ralf-metadata" << EOF
# RALF Run Metadata
# This file is read by other hooks to understand the run context

run:
  id: "$RUN_ID"
  timestamp: "$TIMESTAMP"
  project: "$PROJECT_NAME"
  agent_type: "$AGENT_TYPE"  # Will be updated by agent
  status: initialized

git:
  branch: "$GIT_BRANCH"
  commit: "$GIT_COMMIT"

paths:
  project_root: "$PROJECT_ROOT"
  project_memory: "$PROJECT_DIR"
  run_dir: "$RUN_DIR"
EOF

# Also export for current session
export RALF_RUN_DIR="$RUN_DIR"
export RALF_RUN_ID="$RUN_ID"
export RALF_PROJECT_ROOT="$PROJECT_ROOT"
export RALF_PROJECT_NAME="$PROJECT_NAME"

# =============================================================================
# UNIFIED RUN OUTPUT - RUN.yaml
# =============================================================================

cat > "$RUN_DIR/RUN.yaml" << EOF
# Unified Run Output
# Generated: $TIMESTAMP

---

# Metadata
run_id: "$RUN_ID"
timestamp: "$TIMESTAMP"
project: "$PROJECT_NAME"
agent: "$AGENT_TYPE"
status: initialized
git_branch: "$GIT_BRANCH"
git_commit: "$GIT_COMMIT"

# State Assessment
context:
  active_tasks: []
  queue_depth: 0
  previous_run_status: unknown
  git_branch: "$GIT_BRANCH"
  git_commit: "$GIT_COMMIT"

# Thoughts and Reasoning
thoughts: |
  [Agent reasoning goes here]

  ## State Assessment

  ### Current System Status
  - Active Tasks: []
  - Queue Depth: 0
  - Previous Run Status: unknown

  ### Context
  - Git Branch: $GIT_BRANCH
  - Git Commit: $GIT_COMMIT

  ## Analysis

  [Initial observations and analysis]

  ## Next Steps

  1.
  2.
  3.

# Decisions Made
decisions:
  - id: "DEC-001"
    title: "[Decision Title]"
    context: "[Context for decision]"
    decision: "[What was decided]"
    rationale: "[Why this decision was made]"
    consequences: "[Expected outcomes]"

# Assumptions
assumptions:
  - id: "ASM-001"
    assumption: "[Assumption being made]"
    validation_method: "[How to validate]"
    validation_result: "pending"
    confidence: "MEDIUM"

# Results and Outcomes
results:
  status: in_progress
  summary: "[What was accomplished in this run]"
  tasks_completed: []
  tasks_created: []
  blockers: []

# Learnings
learnings:
  - id: "LRN-001"
    title: "[Learning Title]"
    what_worked: "[What worked well]"
    takeaway: "[Key takeaway for future runs]"

# Source Files Reference (legacy compatibility)
source_files:
  - RUN.yaml
EOF

# Create initialization marker
echo "$TIMESTAMP" > "$RUN_DIR/.hook_initialized"

# =============================================================================
# OUTPUT
# =============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  RALF Run Initialized"
echo "  Project: $PROJECT_NAME"
echo "  Agent: $AGENT_TYPE (will be auto-detected)"
echo "  Run: $RUN_ID"
echo "  Location: ${RUN_DIR/#$HOME/~}"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Environment:"
echo "  RALF_RUN_DIR=$RUN_DIR"
echo "  RALF_RUN_ID=$RUN_ID"
echo "  RALF_PROJECT_ROOT=$PROJECT_ROOT"
echo ""
