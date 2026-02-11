#!/bin/bash
#
# sync-project-memory.sh
#
# Compares a target project memory against the BlackBox5 template
# and optionally syncs missing files/folders
#
# Usage: ./sync-project-memory.sh [OPTIONS] <target-path>
#
# Options:
#   -d, --dry-run     Show what would be changed without making changes
#   -f, --fix         Actually copy missing files/folders
#   -v, --verbose     Show detailed output
#   -h, --help        Show help
#
# Examples:
#   ./sync-project-memory.sh -d /Users/shaansisodia/DEV/client-projects/lumelle/blackbox5/5-project-memory/lumelle
#   ./sync-project-memory.sh -f /Users/shaansisodia/DEV/client-projects/lumelle/blackbox5/5-project-memory/lumelle

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Template source (where this script lives)
TEMPLATE_DIR="/Users/shaansisodia/blackbox5/5-project-memory/siso-internal"

# Parse arguments
DRY_RUN=false
FIX=false
VERBOSE=false
TARGET_PATH=""

show_help() {
    grep '^#' "$0" | cut -c4-
    exit 0
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
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

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -f|--fix)
            FIX=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            ;;
        -*)
            log_error "Unknown option: $1"
            exit 1
            ;;
        *)
            TARGET_PATH="$1"
            shift
            ;;
    esac
done

# Validate target path
if [[ -z "$TARGET_PATH" ]]; then
    log_error "No target path specified"
    show_help
fi

if [[ ! -d "$TARGET_PATH" ]]; then
    log_error "Target directory does not exist: $TARGET_PATH"
    exit 1
fi

# Resolve absolute paths
TARGET_PATH="$(cd "$TARGET_PATH" && pwd)"
TEMPLATE_DIR="$(cd "$TEMPLATE_DIR" && pwd)"

log_info "Template source: $TEMPLATE_DIR"
log_info "Target path: $TARGET_PATH"
log_info "Mode: $([ "$DRY_RUN" = true ] && echo "DRY RUN" || ([ "$FIX" = true ] && echo "FIX" || echo "CHECK ONLY"))"
echo ""

# Statistics
MISSING_FILES=0
MISSING_DIRS=0
EXTRA_FILES=0
COPIED_FILES=0
COPIED_DIRS=0

# Files and directories to exclude from comparison
# These are project-specific data that shouldn't be synced between projects
EXCLUDE_PATTERNS=(
    "*.archived"
    "*.Autonomous"
    "*/runs/*"
    "*/.git/*"
    "*/sessions/session-*"
    "*/agents/history/sessions/*"
    "*/data/*"
    "*/.session_start"
    "*/ralph.p/*"
    "*/operations/reflections/reflection_*.md"
    "*/test-results/*"
    "*/.archived/*"
    "*/.Autonomous/*"
    "*/*.backup*"
    "*/WORK-LOG.md"
    "*/ACTIVE.md"
    # Project-specific data - don't sync between projects
    "*/plans/active/*"           # Active epics/plans (project-specific)
    "*/plans/archived/*"         # Archived plans (project-specific)
    "*/tasks/active/TASK-*"      # Active task folders (project-specific)
    "*/tasks/completed/TASK-*"   # Completed task folders (project-specific)
    "*/tasks/cancelled/TASK-*"   # Cancelled task folders (project-specific)
    "*/decisions/architectural/DEC-*.md"  # Actual decision records
    "*/decisions/technical/DEC-*.md"
    "*/decisions/scope/DEC-*.md"
    "*/goals/active/IG-*.yaml"   # Active goals (project-specific)
    "*/goals/core/CG-*.yaml"     # Core goals (project-specific)
    "*/knowledge/research/active/*"  # Active research (project-specific)
    "*/knowledge/research/thought-loop-framework/*"  # Research data
    "*/.docs/*"                  # AI-generated docs (project-specific)
    "*/CODE-INDEX.yaml"          # Generated code index
    "*/test_results.yaml"        # Generated test results
    "*/timeline.yaml"            # Project-specific timeline
    "*/AGENT_*.md"               # Agent communication files
    "*/QUERIES.md"               # Project-specific queries
    "*/MIGRATION-GUIDE.md"       # Migration guide (template-specific)
)

# Build find exclude arguments
build_exclude_args() {
    local args=""
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        args="$args -not -path '$pattern'"
    done
    echo "$args"
}

# Check if path should be excluded
should_exclude() {
    local path="$1"
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        if [[ "$path" == $pattern ]]; then
            return 0
        fi
    done
    return 1
}

# Get all files from template (templates and infrastructure only)
get_template_files() {
    find "$TEMPLATE_DIR" -type f \
        -not -path "*/.archived/*" \
        -not -path "*/.Autonomous/*" \
        -not -path "*/runs/*" \
        -not -path "*/.git/*" \
        -not -path "*/sessions/session-*" \
        -not -path "*/agents/history/sessions/*" \
        -not -path "*/data/*" \
        -not -name ".session_start" \
        -not -path "*/ralph.p/*" \
        -not -name "reflection_*.md" \
        -not -path "*/test-results/*" \
        -not -name "*.backup*" \
        -not -name "WORK-LOG.md" \
        -not -name "ACTIVE.md" \
        -not -path "*/plans/active/*" \
        -not -path "*/plans/archived/*" \
        -not -path "*/tasks/active/TASK-*" \
        -not -path "*/tasks/completed/TASK-*" \
        -not -path "*/tasks/cancelled/TASK-*" \
        -not -name "DEC-*.md" \
        -not -path "*/goals/active/IG-*.yaml" \
        -not -path "*/goals/core/CG-*.yaml" \
        -not -path "*/knowledge/research/active/*" \
        -not -path "*/knowledge/research/thought-loop-framework/*" \
        -not -path "*/.docs/*" \
        -not -name "CODE-INDEX.yaml" \
        -not -name "test_results.yaml" \
        -not -name "timeline.yaml" \
        -not -name "AGENT_*.md" \
        -not -name "QUERIES.md" \
        -not -name "MIGRATION-GUIDE.md" \
        | sed "s|^$TEMPLATE_DIR/||" | sort
}

# Get all directories from template (templates and infrastructure only)
get_template_dirs() {
    find "$TEMPLATE_DIR" -type d \
        -not -path "*/.archived" \
        -not -path "*/.archived/*" \
        -not -path "*/.Autonomous" \
        -not -path "*/.Autonomous/*" \
        -not -path "*/runs" \
        -not -path "*/runs/*" \
        -not -path "*/.git" \
        -not -path "*/.git/*" \
        -not -path "*/sessions/session-*" \
        -not -path "*/agents/history/sessions" \
        -not -path "*/agents/history/sessions/*" \
        -not -path "*/data" \
        -not -path "*/data/*" \
        -not -path "*/ralph.p" \
        -not -path "*/ralph.p/*" \
        -not -path "*/test-results" \
        -not -path "*/test-results/*" \
        -not -path "*/plans/active" \
        -not -path "*/plans/active/*" \
        -not -path "*/plans/archived" \
        -not -path "*/plans/archived/*" \
        -not -path "*/tasks/active/TASK-*" \
        -not -path "*/tasks/completed/TASK-*" \
        -not -path "*/tasks/cancelled/TASK-*" \
        -not -path "*/goals/active/IG-*" \
        -not -path "*/goals/core/CG-*" \
        -not -path "*/knowledge/research/active" \
        -not -path "*/knowledge/research/active/*" \
        -not -path "*/knowledge/research/thought-loop-framework" \
        -not -path "*/knowledge/research/thought-loop-framework/*" \
        -not -path "*/.docs" \
        -not -path "*/.docs/*" \
        -not -path "$TEMPLATE_DIR" \
        | sed "s|^$TEMPLATE_DIR/||" | grep -v "^$" | sort
}

# Get all files from target (templates and infrastructure only)
get_target_files() {
    find "$TARGET_PATH" -type f \
        -not -path "*/.archived/*" \
        -not -path "*/.Autonomous/*" \
        -not -path "*/runs/*" \
        -not -path "*/.git/*" \
        -not -path "*/sessions/session-*" \
        -not -path "*/agents/history/sessions/*" \
        -not -path "*/data/*" \
        -not -name ".session_start" \
        -not -path "*/ralph.p/*" \
        -not -name "reflection_*.md" \
        -not -path "*/test-results/*" \
        -not -name "*.backup*" \
        -not -name "WORK-LOG.md" \
        -not -name "ACTIVE.md" \
        -not -path "*/plans/active/*" \
        -not -path "*/plans/archived/*" \
        -not -path "*/tasks/active/TASK-*" \
        -not -path "*/tasks/completed/TASK-*" \
        -not -path "*/tasks/cancelled/TASK-*" \
        -not -name "DEC-*.md" \
        -not -path "*/goals/active/IG-*.yaml" \
        -not -path "*/goals/core/CG-*.yaml" \
        -not -path "*/knowledge/research/active/*" \
        -not -path "*/knowledge/research/thought-loop-framework/*" \
        -not -path "*/.docs/*" \
        -not -name "CODE-INDEX.yaml" \
        -not -name "test_results.yaml" \
        -not -name "timeline.yaml" \
        -not -name "AGENT_*.md" \
        -not -name "QUERIES.md" \
        -not -name "MIGRATION-GUIDE.md" \
        | sed "s|^$TARGET_PATH/||" | sort
}

# Get all directories from target (templates and infrastructure only)
get_target_dirs() {
    find "$TARGET_PATH" -type d \
        -not -path "*/.archived" \
        -not -path "*/.archived/*" \
        -not -path "*/.Autonomous" \
        -not -path "*/.Autonomous/*" \
        -not -path "*/runs" \
        -not -path "*/runs/*" \
        -not -path "*/.git" \
        -not -path "*/.git/*" \
        -not -path "*/sessions/session-*" \
        -not -path "*/agents/history/sessions" \
        -not -path "*/agents/history/sessions/*" \
        -not -path "*/data" \
        -not -path "*/data/*" \
        -not -path "*/ralph.p" \
        -not -path "*/ralph.p/*" \
        -not -path "*/test-results" \
        -not -path "*/test-results/*" \
        -not -path "*/plans/active" \
        -not -path "*/plans/active/*" \
        -not -path "*/plans/archived" \
        -not -path "*/plans/archived/*" \
        -not -path "*/tasks/active/TASK-*" \
        -not -path "*/tasks/completed/TASK-*" \
        -not -path "*/tasks/cancelled/TASK-*" \
        -not -path "*/goals/active/IG-*" \
        -not -path "*/goals/core/CG-*" \
        -not -path "*/knowledge/research/active" \
        -not -path "*/knowledge/research/active/*" \
        -not -path "*/knowledge/research/thought-loop-framework" \
        -not -path "*/knowledge/research/thought-loop-framework/*" \
        -not -path "*/.docs" \
        -not -path "*/.docs/*" \
        | sed "s|^$TARGET_PATH/||" | grep -v "^$" | sort
}

# Copy file from template to target
copy_file() {
    local rel_path="$1"
    local src="$TEMPLATE_DIR/$rel_path"
    local dst="$TARGET_PATH/$rel_path"

    if [[ ! -f "$dst" ]]; then
        if [[ "$DRY_RUN" = true ]]; then
            log_warn "Would copy file: $rel_path"
        else
            mkdir -p "$(dirname "$dst")"
            cp "$src" "$dst"
            log_success "Copied: $rel_path"
            ((COPIED_FILES++))
        fi
    fi
}

# Create directory in target
create_dir() {
    local rel_path="$1"
    local dst="$TARGET_PATH/$rel_path"

    if [[ ! -d "$dst" ]]; then
        if [[ "$DRY_RUN" = true ]]; then
            log_warn "Would create directory: $rel_path"
        else
            mkdir -p "$dst"
            log_success "Created directory: $rel_path"
            ((COPIED_DIRS++))
        fi
    fi
}

echo "========================================"
echo "Project Memory Sync Tool"
echo "========================================"
echo ""

# Check directories
echo "Checking directory structure..."
echo ""

TEMPLATE_DIRS=$(get_template_dirs)
TARGET_DIRS=$(get_target_dirs)

MISSING_DIRS_LIST=()
while IFS= read -r dir; do
    if [[ -n "$dir" ]] && ! echo "$TARGET_DIRS" | grep -qx "$dir"; then
        MISSING_DIRS_LIST+=("$dir")
        ((MISSING_DIRS++))
        if [[ "$VERBOSE" = true ]]; then
            log_warn "Missing directory: $dir"
        fi
        if [[ "$FIX" = true ]] || [[ "$DRY_RUN" = true ]]; then
            create_dir "$dir"
        fi
    fi
done <<< "$TEMPLATE_DIRS"

# Remove the template directory itself from missing list
MISSING_DIRS_LIST=($(printf '%s\n' "${MISSING_DIRS_LIST[@]}" | grep -v "^/Users/shaansisodia/blackbox5/5-project-memory/siso-internal$" || true))

# Check files
echo ""
echo "Checking files..."
echo ""

TEMPLATE_FILES=$(get_template_files)
TARGET_FILES=$(get_target_files)

MISSING_FILES_LIST=()
while IFS= read -r file; do
    if [[ -n "$file" ]] && ! echo "$TARGET_FILES" | grep -qx "$file"; then
        MISSING_FILES_LIST+=("$file")
        ((MISSING_FILES++))
        if [[ "$VERBOSE" = true ]]; then
            log_warn "Missing file: $file"
        fi
        if [[ "$FIX" = true ]] || [[ "$DRY_RUN" = true ]]; then
            copy_file "$file"
        fi
    fi
done <<< "$TEMPLATE_FILES"

# Check for extra files in target
echo ""
echo "Checking for extra files in target..."
echo ""

EXTRA_FILES_LIST=()
while IFS= read -r file; do
    if [[ -n "$file" ]] && ! echo "$TEMPLATE_FILES" | grep -qx "$file"; then
        EXTRA_FILES_LIST+=("$file")
        ((EXTRA_FILES++))
        if [[ "$VERBOSE" = true ]]; then
            log_info "Extra file: $file"
        fi
    fi
done <<< "$TARGET_FILES"

# Summary
echo ""
echo "========================================"
echo "Summary"
echo "========================================"
echo ""
echo "Template: $TEMPLATE_DIR"
echo "Target: $TARGET_PATH"
echo ""
echo "Statistics:"
echo "  Missing directories: $MISSING_DIRS"
echo "  Missing files: $MISSING_FILES"
echo "  Extra files in target: $EXTRA_FILES"

if [[ "$FIX" = true ]]; then
    echo "  Directories created: $COPIED_DIRS"
    echo "  Files copied: $COPIED_FILES"
fi

echo ""

if [[ $MISSING_DIRS -eq 0 ]] && [[ $MISSING_FILES -eq 0 ]]; then
    log_success "Project memory is fully synchronized!"
    exit 0
else
    if [[ "$DRY_RUN" = false ]] && [[ "$FIX" = false ]]; then
        log_warn "Project memory is NOT synchronized. Run with -f to fix."
        echo ""
        echo "Missing directories:"
        for dir in "${MISSING_DIRS_LIST[@]}"; do
            echo "  - $dir"
        done
        echo ""
        echo "Missing files:"
        for file in "${MISSING_FILES_LIST[@]}"; do
            echo "  - $file"
        done
    elif [[ "$DRY_RUN" = true ]]; then
        log_info "Dry run complete. Run with -f to apply changes."
    else
        log_success "Synchronization complete!"
    fi
    exit 1
fi
