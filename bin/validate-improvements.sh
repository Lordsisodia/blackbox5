#!/bin/bash
# =============================================================================
# Improvement Validation Script
# =============================================================================
# Purpose: Validate that improvement tasks actually produced measurable improvements
# Version: 1.0.0
# Created: 2026-02-09
# Task: TASK-PROC-027
# =============================================================================

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${HOME}/.blackbox5"
OPERATIONS_DIR="${PROJECT_ROOT}/5-project-memory/blackbox5/operations"
RUNS_DIR="${PROJECT_ROOT}/5-project-memory/blackbox5/runs"
VALIDATION_DIR="${PROJECT_ROOT}/5-project-memory/blackbox5/.autonomous/validations"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="${VALIDATION_DIR}/improvement-validation-${TIMESTAMP}.yaml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# Utility Functions
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# =============================================================================
# Validation Functions
# =============================================================================

validate_before_after_metrics() {
    local improvement_id="$1"
    local category="$2"
    local quiet="${3:-}"

    if [[ -z "$quiet" ]]; then
        log_info "Validating before/after metrics for ${improvement_id}..."
    fi

    case "$category" in
        "process")
            validate_process_metrics "$improvement_id"
            ;;
        "infrastructure")
            validate_infrastructure_metrics "$improvement_id"
            ;;
        "guidance")
            validate_guidance_metrics "$improvement_id"
            ;;
        "technical")
            validate_technical_metrics "$improvement_id"
            ;;
        *)
            log_warning "Unknown category: $category"
            return 1
            ;;
    esac
}

validate_process_metrics() {
    local improvement_id="$1"

    # Check task completion times
    local before_avg=$(calculate_avg_task_time "before" "$improvement_id")
    local after_avg=$(calculate_avg_task_time "after" "$improvement_id")

    if [[ -n "$before_avg" && -n "$after_avg" ]]; then
        local improvement=$(echo "scale=2; ($before_avg - $after_avg) / $before_avg * 100" | bc 2>/dev/null || echo "0")
        echo "  task_completion_time:"
        echo "    before: ${before_avg}s"
        echo "    after: ${after_avg}s"
        echo "    improvement: ${improvement}%"

        if (( $(echo "$improvement > 10" | bc -l 2>/dev/null || echo "0") )); then
            echo "    status: improved"
        elif (( $(echo "$improvement < -10" | bc -l 2>/dev/null || echo "0") )); then
            echo "    status: degraded"
        else
            echo "    status: stable"
        fi
    else
        echo "  task_completion_time:"
        echo "    status: insufficient_data"
    fi
}

validate_infrastructure_metrics() {
    local improvement_id="$1"

    # Check error rates and system health
    local before_errors=$(count_errors "before" "$improvement_id")
    local after_errors=$(count_errors "after" "$improvement_id")

    echo "  error_rate:"
    echo "    before: ${before_errors}"
    echo "    after: ${after_errors}"

    if [[ "$after_errors" -lt "$before_errors" ]]; then
        echo "    status: improved"
    elif [[ "$after_errors" -gt "$before_errors" ]]; then
        echo "    status: degraded"
    else
        echo "    status: stable"
    fi
}

validate_guidance_metrics() {
    local improvement_id="$1"

    # Check documentation effectiveness
    local before_confusion=$(count_confusion_markers "before" "$improvement_id")
    local after_confusion=$(count_confusion_markers "after" "$improvement_id")

    echo "  confusion_markers:"
    echo "    before: ${before_confusion}"
    echo "    after: ${after_confusion}"

    if [[ "$after_confusion" -lt "$before_confusion" ]]; then
        echo "    status: improved"
    elif [[ "$after_confusion" -gt "$before_confusion" ]]; then
        echo "    status: degraded"
    else
        echo "    status: stable"
    fi
}

validate_technical_metrics() {
    local improvement_id="$1"

    # Check code quality metrics
    local before_issues=$(count_code_issues "before" "$improvement_id")
    local after_issues=$(count_code_issues "after" "$improvement_id")

    echo "  code_issues:"
    echo "    before: ${before_issues}"
    echo "    after: ${after_issues}"

    if [[ "$after_issues" -lt "$before_issues" ]]; then
        echo "    status: improved"
    elif [[ "$after_issues" -gt "$before_issues" ]]; then
        echo "    status: degraded"
    else
        echo "    status: stable"
    fi
}

# =============================================================================
# Metric Calculation Functions
# =============================================================================

calculate_avg_task_time() {
    local period="$1"
    local improvement_id="$2"

    # Get the completion date of the improvement
    local completion_date=$(get_improvement_completion_date "$improvement_id")
    if [[ -z "$completion_date" ]]; then
        return 1
    fi

    # Calculate date range
    local start_date
    local end_date

    if [[ "$period" == "before" ]]; then
        end_date="$completion_date"
        start_date=$(date -v-7d -j -f "%Y-%m-%d" "$completion_date" "+%Y-%m-%d" 2>/dev/null || echo "")
    else
        start_date="$completion_date"
        end_date=$(date -v+7d -j -f "%Y-%m-%d" "$completion_date" "+%Y-%m-%d" 2>/dev/null || echo "")
    fi

    # Calculate average from metrics files
    local total_duration=0
    local count=0

    while IFS= read -r metrics_file; do
        if [[ -f "$metrics_file" ]]; then
            local duration=$(jq -r '.duration_seconds // 0' "$metrics_file" 2>/dev/null || echo "0")
            if [[ "$duration" =~ ^[0-9]+$ && "$duration" -gt 0 ]]; then
                total_duration=$((total_duration + duration))
                count=$((count + 1))
            fi
        fi
    done < <(find "$RUNS_DIR" -name "metrics.json" -type f 2>/dev/null | head -20)

    if [[ $count -gt 0 ]]; then
        echo $((total_duration / count))
    fi
}

count_errors() {
    local period="$1"
    local improvement_id="$2"

    # Count error markers in run logs
    local error_count=0

    while IFS= read -r run_dir; do
        if [[ -d "$run_dir" ]]; then
            local error_markers=$(find "$run_dir" -name "*.md" -o -name "*.json" 2>/dev/null | \
                xargs grep -l "ERROR\|FAIL\|exception" 2>/dev/null | wc -l)
            error_count=$((error_count + error_markers))
        fi
    done < <(find "$RUNS_DIR" -maxdepth 1 -type d 2>/dev/null | head -10)

    echo "$error_count"
}

count_confusion_markers() {
    local period="$1"
    local improvement_id="$2"

    # Count confusion-related keywords in learnings
    local confusion_keywords="confused|unclear|ambiguous|don't understand|not sure"
    local count=0

    while IFS= read -r learnings_file; do
        if [[ -f "$learnings_file" ]]; then
            local matches=$(grep -iE "$confusion_keywords" "$learnings_file" 2>/dev/null | wc -l)
            count=$((count + matches))
        fi
    done < <(find "$PROJECT_ROOT/5-project-memory/blackbox5" -name "LEARNINGS.md" -type f 2>/dev/null | head -10)

    echo "$count"
}

count_code_issues() {
    local period="$1"
    local improvement_id="$2"

    # Count code quality issues
    local issue_count=0

    # Check for shellcheck warnings if applicable
    if command -v shellcheck &> /dev/null; then
        while IFS= read -r script_file; do
            if [[ -f "$script_file" ]]; then
                local issues=$(shellcheck "$script_file" 2>/dev/null | wc -l)
                issue_count=$((issue_count + issues))
            fi
        done < <(find "$PROJECT_ROOT/bin" -name "*.sh" -type f 2>/dev/null | head -10)
    fi

    echo "$issue_count"
}

# =============================================================================
# Data Retrieval Functions
# =============================================================================

get_improvement_completion_date() {
    local improvement_id="$1"

    # Extract from improvement backlog
    if [[ -f "${OPERATIONS_DIR}/improvement-backlog.yaml" ]]; then
        local date=$(grep -A 20 "id: ${improvement_id}" "${OPERATIONS_DIR}/improvement-backlog.yaml" 2>/dev/null | \
            grep "completed_at:" | head -1 | cut -d: -f2- | tr -d ' ' | cut -dT -f1)
        if [[ -n "$date" ]]; then
            echo "$date"
            return 0
        fi
    fi

    return 1
}

get_improvement_details() {
    local improvement_id="$1"

    if [[ -f "${OPERATIONS_DIR}/improvement-backlog.yaml" ]]; then
        local category=$(grep -A 30 "id: ${improvement_id}" "${OPERATIONS_DIR}/improvement-backlog.yaml" 2>/dev/null | \
            grep "category:" | head -1 | cut -d: -f2 | tr -d ' ')
        local status=$(grep -A 30 "id: ${improvement_id}" "${OPERATIONS_DIR}/improvement-backlog.yaml" 2>/dev/null | \
            grep "status:" | head -1 | cut -d: -f2 | tr -d ' ')
        local impact=$(grep -A 30 "id: ${improvement_id}" "${OPERATIONS_DIR}/improvement-backlog.yaml" 2>/dev/null | \
            grep "impact:" | head -1 | cut -d: -f2- | sed 's/^ *//')

        echo "category:${category}|status:${status}|impact:${impact}"
    fi
}

# =============================================================================
# Report Generation
# =============================================================================

generate_validation_report() {
    log_info "Generating validation report..."

    # Create validation directory if needed
    mkdir -p "$VALIDATION_DIR"

    # Start report
    cat > "$REPORT_FILE" << EOF
# =============================================================================
# Improvement Validation Report
# =============================================================================
# Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
# Script Version: 1.0.0
# Task: TASK-PROC-027
# =============================================================================

meta:
  report_id: "VAL-${TIMESTAMP}"
  generated_at: "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  generated_by: "validate-improvements.sh"
  version: "1.0.0"

summary:
  total_improvements_validated: 0
  improvements_with_measurable_impact: 0
  improvements_without_data: 0
  overall_effectiveness_score: 0

validations:
EOF

    # Process each completed improvement
    local total=0
    local with_impact=0
    local without_data=0

    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            local imp_id=$(echo "$line" | cut -d: -f1)
            local category=$(echo "$line" | cut -d: -f2)

            log_info "Validating ${imp_id} (${category})..."

            # Append to report
            cat >> "$REPORT_FILE" << EOF

  - improvement_id: "${imp_id}"
    category: "${category}"
    validation_timestamp: "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    metrics:
EOF

            # Run validation and capture output (quiet mode for YAML)
            local metrics_output=$(validate_before_after_metrics "$imp_id" "$category" "quiet" 2>/dev/null)
            echo "$metrics_output" >> "$REPORT_FILE"

            # Determine if we have measurable impact
            if echo "$metrics_output" | grep -q "status: improved"; then
                with_impact=$((with_impact + 1))
                echo "    overall_status: improved" >> "$REPORT_FILE"
            elif echo "$metrics_output" | grep -q "status: degraded"; then
                echo "    overall_status: degraded" >> "$REPORT_FILE"
            elif echo "$metrics_output" | grep -q "status: stable"; then
                echo "    overall_status: stable" >> "$REPORT_FILE"
            else
                without_data=$((without_data + 1))
                echo "    overall_status: insufficient_data" >> "$REPORT_FILE"
            fi

            total=$((total + 1))
        fi
    done < <(extract_completed_improvements)

    # Update summary
    local effectiveness_score=0
    if [[ $total -gt 0 ]]; then
        effectiveness_score=$((with_impact * 100 / total))
    fi

    # Create final report with updated summary
    local temp_file="${REPORT_FILE}.tmp"
    sed "s/total_improvements_validated: 0/total_improvements_validated: ${total}/" "$REPORT_FILE" | \
    sed "s/improvements_with_measurable_impact: 0/improvements_with_measurable_impact: ${with_impact}/" | \
    sed "s/improvements_without_data: 0/improvements_without_data: ${without_data}/" | \
    sed "s/overall_effectiveness_score: 0/overall_effectiveness_score: ${effectiveness_score}/" > "$temp_file"
    mv "$temp_file" "$REPORT_FILE"

    log_success "Validation report generated: ${REPORT_FILE}"
    log_info "Total improvements validated: ${total}"
    log_info "Improvements with measurable impact: ${with_impact}"
    log_info "Improvements without sufficient data: ${without_data}"
    log_info "Overall effectiveness score: ${effectiveness_score}%"
}

extract_completed_improvements() {
    # Extract completed improvements from backlog
    if [[ -f "${OPERATIONS_DIR}/improvement-backlog.yaml" ]]; then
        local in_high=false
        local in_medium=false
        local in_low=false

        while IFS= read -r line; do
            # Track which section we're in
            if [[ "$line" =~ ^high_priority: ]]; then
                in_high=true
                in_medium=false
                in_low=false
            elif [[ "$line" =~ ^medium_priority: ]]; then
                in_high=false
                in_medium=true
                in_low=false
            elif [[ "$line" =~ ^low_priority: ]]; then
                in_high=false
                in_medium=false
                in_low=true
            elif [[ "$line" =~ ^themes: ]]; then
                break
            fi

            # Extract improvement ID and category
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*id:[[:space:]]*(IMP-[0-9]+) ]]; then
                current_id="${BASH_REMATCH[1]}"
            elif [[ "$line" =~ ^[[:space:]]*category:[[:space:]]*(.+)$ ]]; then
                current_category="${BASH_REMATCH[1]}"
            elif [[ "$line" =~ ^[[:space:]]*status:[[:space:]]*completed ]]; then
                if [[ -n "$current_id" && -n "$current_category" ]]; then
                    echo "${current_id}:${current_category}"
                fi
            fi
        done < "${OPERATIONS_DIR}/improvement-backlog.yaml"
    fi
}

# =============================================================================
# Command Handlers
# =============================================================================

show_help() {
    cat << EOF
Improvement Validation Script

Usage: $(basename "$0") [COMMAND] [OPTIONS]

Commands:
    validate [IMP-ID]    Validate specific improvement or all improvements
    report               Generate full validation report
    compare [IMP-ID]     Compare before/after metrics for improvement
    list                 List completed improvements
    help                 Show this help message

Options:
    --output [FILE]      Save report to specific file
    --format [yaml|json] Output format (default: yaml)
    --verbose            Show detailed output

Examples:
    $(basename "$0") validate              # Validate all improvements
    $(basename "$0") validate IMP-001      # Validate specific improvement
    $(basename "$0") report                # Generate full report
    $(basename "$0") list                  # List completed improvements

EOF
}

list_improvements() {
    log_info "Completed Improvements:"
    echo ""

    printf "%-20s %-15s %-12s %s\n" "ID" "Category" "Status" "Impact"
    printf "%-20s %-15s %-12s %s\n" "---" "--------" "------" "------"

    while IFS=: read -r id category; do
        local details=$(get_improvement_details "$id")
        local status=$(echo "$details" | cut -d'|' -f2 | cut -d: -f2)
        local impact=$(echo "$details" | cut -d'|' -f3 | cut -d: -f2-)

        printf "%-20s %-15s %-12s %s\n" "$id" "$category" "$status" "$impact"
    done < <(extract_completed_improvements)
}

validate_single() {
    local imp_id="$1"

    log_info "Validating improvement: ${imp_id}"

    local details=$(get_improvement_details "$imp_id")
    if [[ -z "$details" ]]; then
        log_error "Improvement ${imp_id} not found"
        return 1
    fi

    local category=$(echo "$details" | cut -d'|' -f1 | cut -d: -f2)
    local status=$(echo "$details" | cut -d'|' -f2 | cut -d: -f2)

    if [[ "$status" != "completed" ]]; then
        log_warning "Improvement ${imp_id} is not completed (status: ${status})"
        return 1
    fi

    echo ""
    echo "Improvement: ${imp_id}"
    echo "Category: ${category}"
    echo "Status: ${status}"
    echo ""
    echo "Metrics:"
    validate_before_after_metrics "$imp_id" "$category"
}

# =============================================================================
# Main Entry Point
# =============================================================================

main() {
    local command="${1:-report}"

    case "$command" in
        validate)
            if [[ -n "${2:-}" ]]; then
                validate_single "$2"
            else
                generate_validation_report
            fi
            ;;
        report)
            generate_validation_report
            ;;
        list)
            list_improvements
            ;;
        compare)
            if [[ -n "${2:-}" ]]; then
                validate_single "$2"
            else
                log_error "Please specify an improvement ID"
                exit 1
            fi
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
