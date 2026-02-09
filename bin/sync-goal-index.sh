#!/bin/bash
# =============================================================================
# Sync Goal Index Script
# =============================================================================
# Purpose: Reads all goals/active/IG-*/goal.yaml files and updates INDEX.yaml
#          with correct statuses, establishing goal.yaml as canonical source.
#
# Usage:
#   sync-goal-index.sh              # Run sync
#   sync-goal-index.sh --dry-run    # Preview changes without applying
#   sync-goal-index.sh --verbose    # Show detailed output
#
# Location: ~/.blackbox5/bin/sync-goal-index.sh
# =============================================================================

set -euo pipefail

# Configuration
GOALS_DIR="${BB5_GOALS_DIR:-$HOME/.blackbox5/5-project-memory/blackbox5/goals}"
ACTIVE_GOALS_DIR="$GOALS_DIR/active"
INDEX_FILE="$GOALS_DIR/INDEX.yaml"
DRY_RUN=false
VERBOSE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# Helper Functions
# =============================================================================

log_info() {
    if [[ "$VERBOSE" == true ]]; then
        echo -e "${BLUE}[INFO]${NC} $1"
    fi
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Extract value from YAML file using grep/sed (lightweight, no external deps)
extract_yaml_value() {
    local file="$1"
    local key="$2"
    local result
    result=$(grep -E "^[[:space:]]*${key}:" "$file" 2>/dev/null | head -1 | sed -E 's/^[^:]+:[[:space:]]*"?([^"]*)"?$/\1/' | sed 's/[[:space:]]*$//' || true)
    echo "$result"
}

# Extract progress percentage from goal.yaml
extract_progress() {
    local file="$1"
    local result
    result=$(grep -E "^[[:space:]]*percentage:" "$file" 2>/dev/null | head -1 | sed -E 's/^[^:]+:[[:space:]]*([0-9]+).*/\1/' || true)
    echo "$result"
}

# Get current timestamp in ISO format
get_timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# =============================================================================
# Parse Arguments
# =============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            echo "Usage: sync-goal-index.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --dry-run     Preview changes without applying"
            echo "  --verbose     Show detailed output"
            echo "  -h, --help    Show this help message"
            echo ""
            echo "Environment Variables:"
            echo "  BB5_GOALS_DIR    Override goals directory path"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# =============================================================================
# Validate Environment
# =============================================================================

if [[ ! -d "$ACTIVE_GOALS_DIR" ]]; then
    log_error "Active goals directory not found: $ACTIVE_GOALS_DIR"
    exit 1
fi

if [[ ! -f "$INDEX_FILE" ]]; then
    log_warn "INDEX.yaml not found at $INDEX_FILE"
    log_info "Will create new INDEX.yaml"
fi

# =============================================================================
# Scan Goal Files
# =============================================================================

# Use temp files to store goal data (macOS bash compatible)
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

GOAL_LIST_FILE="$TEMP_DIR/goals.txt"
touch "$GOAL_LIST_FILE"

log_info "Scanning goal files in $ACTIVE_GOALS_DIR"

# Find all goal.yaml files
GOAL_FILES=$(find "$ACTIVE_GOALS_DIR" -name "goal.yaml" -type f 2>/dev/null | sort)

if [[ -z "$GOAL_FILES" ]]; then
    log_error "No goal.yaml files found in $ACTIVE_GOALS_DIR"
    exit 1
fi

GOAL_COUNT=0

# Process each goal file
while IFS= read -r goal_file; do
    [[ -z "$goal_file" ]] && continue

    goal_id=$(extract_yaml_value "$goal_file" "goal_id")

    if [[ -z "$goal_id" ]]; then
        log_warn "Could not extract goal_id from $goal_file"
        continue
    fi

    status=$(extract_yaml_value "$goal_file" "status")
    name=$(extract_yaml_value "$goal_file" "name")
    priority=$(extract_yaml_value "$goal_file" "priority")
    owner=$(extract_yaml_value "$goal_file" "owner")
    progress=$(extract_progress "$goal_file")

    # Default values if not found
    status=${status:-"not_started"}
    name=${name:-"Unknown Goal"}
    priority=${priority:-"medium"}
    owner=${owner:-"unknown"}
    progress=${progress:-0}

    # Store in temp file (pipe-delimited)
    echo "$goal_id|$status|$progress|$name|$priority|$owner" >> "$GOAL_LIST_FILE"
    ((GOAL_COUNT++))

    log_info "Parsed $goal_id: status=$status, progress=$progress%"
done <<< "$GOAL_FILES"

log_info "Found $GOAL_COUNT goal files"

# =============================================================================
# Generate New INDEX.yaml
# =============================================================================

TIMESTAMP=$(get_timestamp)

# Count by status
COUNT_NOT_STARTED=0
COUNT_IN_PROGRESS=0
COUNT_COMPLETED=0
COUNT_DRAFT=0
COUNT_CANCELLED=0
COUNT_MERGED=0
COUNT_ACTIVE=0

# Build arrays for each status/priority
CRITICAL_GOALS=""
HIGH_GOALS=""
MEDIUM_GOALS=""

NOT_STARTED_GOALS=""
IN_PROGRESS_GOALS=""
COMPLETED_GOALS=""
DRAFT_GOALS=""
CANCELLED_GOALS=""
MERGED_GOALS=""
ACTIVE_GOALS=""

GOALS_DETAIL=""

# Process each goal
while IFS='|' read -r goal_id status progress name priority owner; do
    [[ -z "$goal_id" ]] && continue

    # Count by status
    case "$status" in
        not_started) ((COUNT_NOT_STARTED++)); NOT_STARTED_GOALS="$NOT_STARTED_GOALS    - $goal_id
" ;;
        in_progress) ((COUNT_IN_PROGRESS++)); IN_PROGRESS_GOALS="$IN_PROGRESS_GOALS    - $goal_id
" ;;
        completed) ((COUNT_COMPLETED++)); COMPLETED_GOALS="$COMPLETED_GOALS    - $goal_id
" ;;
        draft) ((COUNT_DRAFT++)); DRAFT_GOALS="$DRAFT_GOALS    - $goal_id
" ;;
        cancelled) ((COUNT_CANCELLED++)); CANCELLED_GOALS="$CANCELLED_GOALS    - $goal_id
" ;;
        merged) ((COUNT_MERGED++)); MERGED_GOALS="$MERGED_GOALS    - $goal_id
" ;;
        active) ((COUNT_ACTIVE++)); ACTIVE_GOALS="$ACTIVE_GOALS    - $goal_id
" ;;
    esac

    # Count by priority
    case "$priority" in
        critical) CRITICAL_GOALS="$CRITICAL_GOALS    - $goal_id
" ;;
        high) HIGH_GOALS="$HIGH_GOALS    - $goal_id
" ;;
        medium) MEDIUM_GOALS="$MEDIUM_GOALS    - $goal_id
" ;;
    esac

    # Build goals detail
    GOALS_DETAIL="${GOALS_DETAIL}  - id: $goal_id
    name: \"$name\"
    status: $status
    progress: $progress%
    priority: $priority
    owner: $owner
"
done < "$GOAL_LIST_FILE"

# Build the new INDEX.yaml content
cat > "$TEMP_DIR/new_index.yaml" << EOF
# Goals Index
# =============================================================================
# Auto-generated: Quick lookup for all goals
# Generated: $TIMESTAMP
# =============================================================================

meta:
  generated_at: "$TIMESTAMP"
  version: "1.1.0"
  total_goals: $GOAL_COUNT
  last_synced: "$TIMESTAMP"

# =============================================================================
# SUMMARY
# =============================================================================

summary:
  not_started: $COUNT_NOT_STARTED
  in_progress: $COUNT_IN_PROGRESS
  completed: $COUNT_COMPLETED
  draft: $COUNT_DRAFT
  cancelled: $COUNT_CANCELLED
  merged: $COUNT_MERGED
  active: $COUNT_ACTIVE

by_priority:
  critical:
$CRITICAL_GOALS  high:
$HIGH_GOALS  medium:
$MEDIUM_GOALS
by_status:
  not_started:
$NOT_STARTED_GOALS  in_progress:
$IN_PROGRESS_GOALS  completed:
$COMPLETED_GOALS  draft:
$DRAFT_GOALS  cancelled:
$CANCELLED_GOALS  merged:
$MERGED_GOALS  active:
$ACTIVE_GOALS
# =============================================================================
# GOALS DETAIL (Derived from goal.yaml files)
# =============================================================================

goals:
$GOALS_DETAIL
# =============================================================================
# NOTES
# =============================================================================

# This file is auto-generated from goals in active/
# Source of truth: goals/active/IG-*/goal.yaml
# DO NOT EDIT MANUALLY - Run sync-goal-index.sh to regenerate
# Last synced: $TIMESTAMP
EOF

# =============================================================================
# Apply or Preview Changes
# =============================================================================

if [[ "$DRY_RUN" == true ]]; then
    echo "=========================================="
    echo "DRY RUN - Changes would be applied:"
    echo "=========================================="
    echo ""
    echo "Status Summary:"
    [[ $COUNT_NOT_STARTED -gt 0 ]] && echo "  not_started: $COUNT_NOT_STARTED goals"
    [[ $COUNT_IN_PROGRESS -gt 0 ]] && echo "  in_progress: $COUNT_IN_PROGRESS goals"
    [[ $COUNT_COMPLETED -gt 0 ]] && echo "  completed: $COUNT_COMPLETED goals"
    [[ $COUNT_DRAFT -gt 0 ]] && echo "  draft: $COUNT_DRAFT goals"
    [[ $COUNT_CANCELLED -gt 0 ]] && echo "  cancelled: $COUNT_CANCELLED goals"
    [[ $COUNT_MERGED -gt 0 ]] && echo "  merged: $COUNT_MERGED goals"
    [[ $COUNT_ACTIVE -gt 0 ]] && echo "  active: $COUNT_ACTIVE goals"
    echo ""
    echo "Goal Details:"
    while IFS='|' read -r goal_id status progress name priority owner; do
        [[ -z "$goal_id" ]] && continue
        echo "  $goal_id: $status ($progress%)"
    done < "$GOAL_LIST_FILE"
    echo ""
    log_info "Dry run complete. No changes made."
else
    # Backup existing INDEX.yaml
    if [[ -f "$INDEX_FILE" ]]; then
        backup_file="${INDEX_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$INDEX_FILE" "$backup_file"
        log_info "Backup created: $backup_file"
    fi

    # Write new INDEX.yaml
    cp "$TEMP_DIR/new_index.yaml" "$INDEX_FILE"
    log_success "INDEX.yaml updated successfully"
    log_info "Total goals: $GOAL_COUNT"
    log_info "Synced at: $TIMESTAMP"
fi

exit 0
