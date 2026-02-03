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
# TEMPLATE CREATION
# =============================================================================

cat > "$RUN_DIR/THOUGHTS.md" << EOF
# THOUGHTS - Run $RUN_ID

**Project:** $PROJECT_NAME
**Agent:** $AGENT_TYPE
**Run ID:** $RUN_ID
**Started:** $TIMESTAMP

---

## State Assessment

### Current System Status
- **Active Tasks:**
- **Queue Depth:**
- **Previous Run Status:**

### Context
- **Git Branch:** $GIT_BRANCH
- **Git Commit:** $GIT_COMMIT

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

cat > "$RUN_DIR/RESULTS.md" << EOF
# RESULTS - Run $RUN_ID

**Project:** $PROJECT_NAME
**Status:** in_progress
**Started:** $TIMESTAMP
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

cat > "$RUN_DIR/DECISIONS.md" << EOF
# DECISIONS - Run $RUN_ID

**Project:** $PROJECT_NAME
**Run:** $RUN_ID
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

cat > "$RUN_DIR/metadata.yaml" << EOF
run:
  id: "$RUN_ID"
  project: "$PROJECT_NAME"
  agent: "$AGENT_TYPE"
  timestamp_start: "$TIMESTAMP"
  timestamp_end: null
  duration_seconds: null

state:
  task_claimed: null
  task_status: null
  files_modified: []
  commit_hash: null

results:
  status: "in_progress"
  summary: ""
  tasks_completed: []
  tasks_created: []
  blockers: []
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
