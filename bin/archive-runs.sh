#!/usr/bin/env bash
#
# BlackBox5 Run Archival Script
# Archives old run folders based on archive-policy.yaml
#

set -euo pipefail
shopt -s assoc_expand_once 2>/dev/null || true

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_MEMORY="${HOME}/.blackbox5/5-project-memory"
POLICY_FILE="${PROJECT_MEMORY}/blackbox5/.autonomous/archive-policy.yaml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
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

# Check dependencies
check_dependencies() {
    local deps=("tar" "gzip" "find" "date" "awk")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            log_error "Required dependency '$dep' not found"
            exit 1
        fi
    done

    # Check for yq or python-yaml for parsing
    if command -v yq &> /dev/null; then
        YAML_PARSER="yq"
    elif python3 -c "import yaml" 2>/dev/null; then
        YAML_PARSER="python"
    else
        log_warn "No YAML parser found (yq or python-yaml). Using default values."
        YAML_PARSER="none"
    fi
}

# Parse YAML value
get_yaml_value() {
    local key="$1"
    local default="${2:-}"

    if [[ "$YAML_PARSER" == "yq" ]]; then
        yq eval "$key" "$POLICY_FILE" 2>/dev/null || echo "$default"
    elif [[ "$YAML_PARSER" == "python" ]]; then
        python3 -c "import yaml; print(yaml.safe_load(open('$POLICY_FILE'))$key)" 2>/dev/null || echo "$default"
    else
        echo "$default"
    fi
}

# Load policy configuration
load_policy() {
    if [[ ! -f "$POLICY_FILE" ]]; then
        log_error "Policy file not found: $POLICY_FILE"
        exit 1
    fi

    # Load retention settings
    KEEP_LAST_RUNS=$(get_yaml_value ".retention.keep_last_runs" "50")
    ARCHIVE_AFTER_DAYS=$(get_yaml_value ".retention.archive_after_days" "30")
    DELETE_AFTER_DAYS=$(get_yaml_value ".retention.delete_after_days" "365")
    PRESERVE_ACTIVE_TASKS=$(get_yaml_value ".retention.preserve_active_tasks" "true")

    # Load compression settings
    COMPRESSION_FORMAT=$(get_yaml_value ".compression.format" "tar.gz")
    COMPRESSION_LEVEL=$(get_yaml_value ".compression.level" "6")

    # Load archive settings
    ARCHIVE_DIR=$(get_yaml_value ".archive.archive_dir" "archive/runs")
    MAX_ARCHIVE_SIZE_MB=$(get_yaml_value ".archive.max_archive_size_mb" "500")

    # Load index settings
    INDEX_FILE=$(get_yaml_value ".index.index_file" "archive/runs-index.json")

    # Load log settings
    LOG_FILE=$(get_yaml_value ".notifications.log_file" "archive/archival.log")

    log "Policy loaded: keep_last=$KEEP_LAST_RUNS, archive_after=${ARCHIVE_AFTER_DAYS}d, delete_after=${DELETE_AFTER_DAYS}d"
}

# Get archive directory for a project
get_project_archive_dir() {
    local project_path="$1"
    echo "${project_path}/.autonomous/${ARCHIVE_DIR}"
}

# Get index file path for a project
get_project_index_file() {
    local project_path="$1"
    echo "${project_path}/.autonomous/${INDEX_FILE}"
}

# Get log file path for a project
get_project_log_file() {
    local project_path="$1"
    echo "${project_path}/.autonomous/${LOG_FILE}"
}

# Initialize archive directory
init_archive_dir() {
    local project_path="$1"
    local archive_dir=$(get_project_archive_dir "$project_path")

    if [[ ! -d "$archive_dir" ]]; then
        mkdir -p "$archive_dir"
        log "Created archive directory: $archive_dir"
    fi

    # Create temp directory for restores
    local temp_dir="${archive_dir}/../temp"
    if [[ ! -d "$temp_dir" ]]; then
        mkdir -p "$temp_dir"
    fi
}

# Check if run has preserve tags
check_preserve_tags() {
    local run_dir="$1"
    local run_name=$(basename "$run_dir")

    # Check for TAGS file or metadata
    if [[ -f "${run_dir}/TAGS" ]]; then
        while IFS= read -r tag; do
            case "$tag" in
                milestone|important|reference|audit|compliance)
                    return 0
                    ;;
            esac
        done < "${run_dir}/TAGS"
    fi

    # Check metadata file if exists
    if [[ -f "${run_dir}/metadata.yaml" ]]; then
        if grep -qE "(milestone|important|reference|audit|compliance)" "${run_dir}/metadata.yaml" 2>/dev/null; then
            return 0
        fi
    fi

    return 1
}

# Check if run is associated with active task
check_active_task() {
    local run_dir="$1"
    local project_path="$2"

    # Extract task ID from run path if possible
    local run_path_relative="${run_dir#$project_path/.autonomous/}"

    # Check if run is in tasks/active directory
    if [[ "$run_path_relative" == tasks/active/* ]]; then
        return 0
    fi

    # Check for active task link
    if [[ -L "${run_dir}/task" ]]; then
        local task_path=$(readlink "${run_dir}/task")
        if [[ -d "$task_path" ]]; then
            # Check if task is still active
            local task_status_file="${task_path}/task.md"
            if [[ -f "$task_status_file" ]]; then
                if grep -q "Status.*completed" "$task_status_file" 2>/dev/null; then
                    return 1
                else
                    return 0
                fi
            fi
        fi
    fi

    return 1
}

# Calculate age of run in days
get_run_age_days() {
    local run_dir="$1"
    local run_mtime=$(stat -f %m "$run_dir" 2>/dev/null || stat -c %Y "$run_dir" 2>/dev/null)
    local current_time=$(date +%s)
    local age_seconds=$((current_time - run_mtime))
    local age_days=$((age_seconds / 86400))
    echo "$age_days"
}

# Get run date for grouping
get_run_date() {
    local run_dir="$1"
    local run_mtime=$(stat -f %m "$run_dir" 2>/dev/null || stat -c %Y "$run_dir" 2>/dev/null)
    date -r "$run_mtime" "+%Y-%m" 2>/dev/null || date -d "@$run_mtime" "+%Y-%m"
}

# Get run metadata
get_run_metadata() {
    local run_dir="$1"
    local run_name=$(basename "$run_dir")
    local run_date=$(get_run_date "$run_dir")
    local run_age=$(get_run_age_days "$run_dir")

    # Try to extract agent type from path
    local agent_type="unknown"
    if [[ "$run_dir" == *"/agents/"* ]]; then
        agent_type=$(echo "$run_dir" | sed -n 's|.*/agents/\([^/]*\)/.*|\1|p')
    fi

    # Try to get task ID
    local task_id="none"
    if [[ -f "${run_dir}/task.md" ]]; then
        task_id=$(grep -oE "TASK-[A-Z0-9-]+" "${run_dir}/task.md" 2>/dev/null | head -1 || echo "none")
    fi

    echo "{\"run_id\":\"$run_name\",\"agent_type\":\"$agent_type\",\"task_id\":\"$task_id\",\"date\":\"$run_date\",\"age_days\":$run_age,\"path\":\"$run_dir\"}"
}

# Archive a single run
archive_run() {
    local run_dir="$1"
    local archive_file="$2"
    local run_name=$(basename "$run_dir")

    log "Archiving: $run_name -> $(basename "$archive_file")"

    # Create tar.gz archive
    if tar -czf "$archive_file" -C "$(dirname "$run_dir")" "$run_name" 2>/dev/null; then
        # Verify archive was created
        if [[ -f "$archive_file" ]]; then
            # Remove original directory
            rm -rf "$run_dir"
            log_success "Archived: $run_name"
            return 0
        else
            log_error "Archive creation failed for: $run_name"
            return 1
        fi
    else
        log_error "Tar command failed for: $run_name"
        return 1
    fi
}

# Update archive index
update_index() {
    local project_path="$1"
    local index_file=$(get_project_index_file "$project_path")
    local run_metadata="$2"
    local archive_location="$3"

    # Create index directory if needed
    mkdir -p "$(dirname "$index_file")"

    # Initialize index if it doesn't exist
    if [[ ! -f "$index_file" ]]; then
        echo '{"runs":[],"archives":[],"last_updated":""}' > "$index_file"
    fi

    # Add entry to index using Python for JSON manipulation
    python3 << EOF
import json
import sys
from datetime import datetime

try:
    with open('$index_file', 'r') as f:
        index = json.load(f)
except:
    index = {"runs": [], "archives": [], "last_updated": ""}

run_data = json.loads('$run_metadata')
run_data['archive_location'] = '$archive_location'
run_data['archived_at'] = datetime.now().isoformat()

# Check if entry already exists
existing = [r for r in index['runs'] if r['run_id'] == run_data['run_id']]
if not existing:
    index['runs'].append(run_data)

# Update archive list if not present
if '$archive_location' not in index['archives']:
    index['archives'].append('$archive_location')

index['last_updated'] = datetime.now().isoformat()

with open('$index_file', 'w') as f:
    json.dump(index, f, indent=2)
EOF
}

# Process runs for a project
process_project() {
    local project_path="$1"
    local project_name=$(basename "$project_path")

    log "Processing project: $project_name"

    # Initialize archive directory
    init_archive_dir "$project_path"

    local archive_dir=$(get_project_archive_dir "$project_path")
    local runs_archived=0
    local runs_skipped=0
    local runs_total=0

    # Find all run directories
    local runs=()
    while IFS= read -r -d '' run_dir; do
        runs+=("$run_dir")
    done < <(find "$project_path/.autonomous" -type d -name "run-*" -print0 2>/dev/null || true)

    runs_total=${#runs[@]}
    log "Found $runs_total run directories"

    # Sort runs by modification time (oldest first)
    IFS=$'\n' runs=($(sort -t$'\t' -k2 -n < <(for run in "${runs[@]}"; do
        mtime=$(stat -f %m "$run" 2>/dev/null || stat -c %Y "$run" 2>/dev/null)
        echo -e "$run\t$mtime"
    done)))
    unset IFS

    # Keep track of runs per agent type using temp files
    local counts_dir=$(mktemp -d)
    trap "rm -rf $counts_dir" EXIT

    # Process each run
    for run_dir in "${runs[@]}"; do
        local run_name=$(basename "$run_dir")
        local run_age=$(get_run_age_days "$run_dir")

        # Get agent type
        local agent_type="unknown"
        if [[ "$run_dir" == *"/agents/"* ]]; then
            agent_type=$(echo "$run_dir" | sed -n 's|.*/agents/\([^/]*\)/.*|\1|p')
        fi

        # Count runs for this agent using temp file
        local count_file="$counts_dir/$agent_type"
        local current_count=0
        if [[ -f "$count_file" ]]; then
            current_count=$(cat "$count_file")
        fi
        current_count=$((current_count + 1))
        echo "$current_count" > "$count_file"

        # Skip if within keep_last limit
        if [[ $current_count -le $KEEP_LAST_RUNS ]]; then
            log "Skipping (within keep_last): $run_name"
            ((runs_skipped++))
            continue
        fi

        # Skip if too new
        if [[ $run_age -lt $ARCHIVE_AFTER_DAYS ]]; then
            log "Skipping (too new, ${run_age}d): $run_name"
            ((runs_skipped++))
            continue
        fi

        # Skip if has preserve tags
        if check_preserve_tags "$run_dir"; then
            log "Skipping (preserve tags): $run_name"
            ((runs_skipped++))
            continue
        fi

        # Skip if associated with active task
        if [[ "$PRESERVE_ACTIVE_TASKS" == "true" ]] && check_active_task "$run_dir" "$project_path"; then
            log "Skipping (active task): $run_name"
            ((runs_skipped++))
            continue
        fi

        # Get run date for archive grouping
        local run_date=$(get_run_date "$run_dir")
        local archive_name="archive-${run_date}.tar.gz"
        local archive_path="${archive_dir}/${archive_name}"

        # Create archive if it doesn't exist
        if [[ ! -f "$archive_path" ]]; then
            log "Creating new archive: $archive_name"
        fi

        # Get run metadata
        local run_metadata=$(get_run_metadata "$run_dir")

        # Archive the run
        if archive_run "$run_dir" "$archive_path"; then
            # Update index
            update_index "$project_path" "$run_metadata" "$archive_path"
            ((runs_archived++))
        fi
    done

    log_success "Project $project_name: $runs_archived archived, $runs_skipped skipped, $runs_total total"

    # Return stats
    echo "$runs_archived $runs_skipped $runs_total"
}

# Restore a run from archive
restore_run() {
    local project_name="$2"
    local run_id="$3"
    local project_path="${PROJECT_MEMORY}/${project_name}"
    local index_file=$(get_project_index_file "$project_path")

    if [[ ! -f "$index_file" ]]; then
        log_error "Index file not found for project: $project_name"
        exit 1
    fi

    # Find run in index
    local archive_location=$(python3 << EOF
import json
with open('$index_file', 'r') as f:
    index = json.load(f)
for run in index['runs']:
    if run['run_id'] == '$run_id':
        print(run['archive_location'])
        break
EOF
)

    if [[ -z "$archive_location" ]]; then
        log_error "Run not found in index: $run_id"
        exit 1
    fi

    if [[ ! -f "$archive_location" ]]; then
        log_error "Archive file not found: $archive_location"
        exit 1
    fi

    # Extract run
    local temp_dir=$(get_project_archive_dir "$project_path")/../temp
    local extract_dir="${temp_dir}/restore-${run_id}-$$"

    mkdir -p "$extract_dir"

    log "Extracting $run_id from $(basename "$archive_location")"

    if tar -xzf "$archive_location" -C "$extract_dir" "$run_id"; then
        local restored_path="${extract_dir}/${run_id}"
        log_success "Restored to: $restored_path"
        echo "$restored_path"
    else
        log_error "Failed to extract run from archive"
        exit 1
    fi
}

# List archived runs
list_archived() {
    local project_name="$2"
    local project_path="${PROJECT_MEMORY}/${project_name}"
    local index_file=$(get_project_index_file "$project_path")

    if [[ ! -f "$index_file" ]]; then
        log_warn "No archive index found for project: $project_name"
        return
    fi

    log "Archived runs for project: $project_name"
    echo ""
    printf "%-20s %-15s %-20s %-30s\n" "RUN ID" "AGENT" "DATE" "ARCHIVE"
    printf "%-20s %-15s %-20s %-30s\n" "--------------------" "---------------" "--------------------" "------------------------------"

    python3 << EOF
import json
with open('$index_file', 'r') as f:
    index = json.load(f)
for run in sorted(index['runs'], key=lambda x: x['date'], reverse=True):
    archive_name = run['archive_location'].split('/')[-1]
    print(f"{run['run_id'][:20]:<20} {run['agent_type'][:15]:<15} {run['date']:<20} {archive_name:<30}")
EOF
}

# Clean up old archives
cleanup_old_archives() {
    local project_path="$1"
    local archive_dir=$(get_project_archive_dir "$project_path")

    if [[ ! -d "$archive_dir" ]]; then
        return
    fi

    log "Checking for old archives to delete (> ${DELETE_AFTER_DAYS} days)"

    local deleted=0
    while IFS= read -r archive_file; do
        local archive_age=$(get_run_age_days "$archive_file")
        if [[ $archive_age -gt $DELETE_AFTER_DAYS ]]; then
            log "Deleting old archive: $(basename "$archive_file") (${archive_age} days old)"
            rm -f "$archive_file"
            ((deleted++))
        fi
    done < <(find "$archive_dir" -name "archive-*.tar.gz" -type f 2>/dev/null)

    if [[ $deleted -gt 0 ]]; then
        log_success "Deleted $deleted old archives"
    else
        log "No old archives to delete"
    fi
}

# Generate report
generate_report() {
    local project_path="$1"
    local archived="$2"
    local skipped="$3"
    local total="$4"

    local log_file=$(get_project_log_file "$project_path")
    mkdir -p "$(dirname "$log_file")"

    cat >> "$log_file" << EOF
[$(date '+%Y-%m-%d %H:%M:%S')] Archival Report
================================================
Total runs processed: $total
Runs archived: $archived
Runs skipped: $skipped
Archive location: $(get_project_archive_dir "$project_path")
Index file: $(get_project_index_file "$project_path")

EOF

    log "Report appended to: $log_file"
}

# Main execution
main() {
    local command="${1:-archive}"

    log "BlackBox5 Run Archival Script v1.0"
    log "=================================="

    check_dependencies
    load_policy

    case "$command" in
        archive)
            log "Starting archival process..."
            local total_archived=0
            local total_skipped=0
            local total_runs=0

            # Process all projects
            for project_path in "$PROJECT_MEMORY"/*; do
                if [[ -d "$project_path/.autonomous" ]]; then
                    # Run process_project and capture stats from the last line (which contains the numbers)
                    output=$(process_project "$project_path" 2>&1)
                    stats=$(echo "$output" | tail -1)
                    read -r archived skipped total <<< "$stats"
                    # Print all output except the last line (stats)
                    echo "$output" | sed '$d'
                    total_archived=$((total_archived + archived))
                    total_skipped=$((total_skipped + skipped))
                    total_runs=$((total_runs + total))

                    # Clean up old archives
                    cleanup_old_archives "$project_path"

                    # Generate report
                    generate_report "$project_path" "$archived" "$skipped" "$total"
                fi
            done

            log_success "Archival complete: $total_archived archived, $total_skipped skipped, $total_runs total"
            ;;

        restore)
            if [[ $# -lt 3 ]]; then
                echo "Usage: $0 restore <project-name> <run-id>"
                exit 1
            fi
            restore_run "$@"
            ;;

        list)
            if [[ $# -lt 2 ]]; then
                echo "Usage: $0 list <project-name>"
                exit 1
            fi
            list_archived "$@"
            ;;

        status)
            log "Archive Status"
            log "=============="
            for project_path in "$PROJECT_MEMORY"/*; do
                if [[ -d "$project_path/.autonomous" ]]; then
                    local project_name=$(basename "$project_path")
                    local run_count=$(find "$project_path/.autonomous" -type d -name "run-*" 2>/dev/null | wc -l)
                    local archive_dir=$(get_project_archive_dir "$project_path")
                    local archive_count=0
                    if [[ -d "$archive_dir" ]]; then
                        archive_count=$(find "$archive_dir" -name "archive-*.tar.gz" 2>/dev/null | wc -l)
                    fi
                    printf "%-30s: %3d runs, %3d archives\n" "$project_name" "$run_count" "$archive_count"
                fi
            done
            ;;

        *)
            echo "Usage: $0 {archive|restore|list|status}"
            echo ""
            echo "Commands:"
            echo "  archive           Archive old runs based on policy"
            echo "  restore <proj> <id>  Restore a specific run from archive"
            echo "  list <project>    List archived runs for a project"
            echo "  status            Show archive status for all projects"
            echo ""
            echo "Policy file: $POLICY_FILE"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
