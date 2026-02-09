#!/bin/bash
# validate-task-completion.sh
# Validates that tasks marked complete actually meet success criteria
#
# Usage: validate-task-completion.sh [task-path]
#   If no task-path provided, validates all completed tasks

set -e

# Colors for output
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    RED='\033[0;31m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    GREEN=''
    RED=''
    YELLOW=''
    BLUE=''
    NC=''
fi

log() { echo -e "${BLUE}[VALIDATE]${NC} $1"; }
success() { echo -e "${GREEN}[PASS]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

validate_task_file() {
    local task_file="$1"
    local errors=0
    local warnings=0

    if [ ! -f "$task_file" ]; then
        fail "Task file not found: $task_file"
        return 1
    fi

    log "Validating: $(basename $(dirname "$task_file"))"

    # Check 1: Status is marked as completed
    local status=$(grep -E "^\*\*Status:\*\*" "$task_file" | sed 's/.*:\*\*//' | tr -d ' ')
    if [ "$status" != "completed" ]; then
        fail "Status is '$status', expected 'completed'"
        ((errors++))
    else
        success "Status is 'completed'"
    fi

    # Check 2: All success criteria checkboxes are marked complete
    local unchecked=$(grep -E "^- \[ \]" "$task_file" | wc -l)
    if [ "$unchecked" -gt 0 ]; then
        fail "Found $unchecked unchecked success criteria"
        ((errors++))
    else
        success "All success criteria checked"
    fi

    # Check 3: Required deliverables exist (LEARNINGS.md, THOUGHTS.md)
    local task_dir=$(dirname "$task_file")

    if [ -f "$task_dir/LEARNINGS.md" ]; then
        # Check if LEARNINGS.md has meaningful content (more than just headers)
        local learnings_content=$(grep -v "^#" "$task_dir/LEARNINGS.md" | grep -v "^$" | grep -v "^-" | wc -l)
        if [ "$learnings_content" -gt 0 ]; then
            success "LEARNINGS.md exists with content"
        else
            warn "LEARNINGS.md exists but may lack substantive content"
            ((warnings++))
        fi
    else
        fail "LEARNINGS.md not found"
        ((errors++))
    fi

    if [ -f "$task_dir/THOUGHTS.md" ]; then
        # Check if THOUGHTS.md has meaningful content
        local thoughts_content=$(grep -v "^#" "$task_dir/THOUGHTS.md" | grep -v "^$" | wc -l)
        if [ "$thoughts_content" -gt 0 ]; then
            success "THOUGHTS.md exists with content"
        else
            warn "THOUGHTS.md exists but may lack substantive content"
            ((warnings++))
        fi
    else
        fail "THOUGHTS.md not found"
        ((errors++))
    fi

    # Check 4: Results section exists and is populated
    if grep -q "^## Results" "$task_file"; then
        local results_content=$(sed -n '/^## Results/,/^## /p' "$task_file" | grep -v "^## Results" | grep -v "^## " | grep -v "^$" | wc -l)
        if [ "$results_content" -gt 0 ]; then
            success "Results section populated"
        else
            warn "Results section exists but may be empty"
            ((warnings++))
        fi
    else
        warn "No Results section found"
        ((warnings++))
    fi

    # Summary for this task
    if [ "$errors" -eq 0 ]; then
        success "Validation passed ($warnings warnings)"
        return 0
    else
        fail "Validation failed: $errors errors, $warnings warnings"
        return 1
    fi
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

PROJECT_MEMORY_DIR="${HOME}/.blackbox5/5-project-memory"

# If specific task path provided, validate just that task
if [ -n "$1" ]; then
    task_path="$1"
    if [ -f "$task_path/task.md" ]; then
        validate_task_file "$task_path/task.md"
        exit $?
    elif [ -f "$task_path" ]; then
        validate_task_file "$task_path"
        exit $?
    else
        fail "Task not found: $task_path"
        exit 1
    fi
fi

# Otherwise, validate all completed tasks
log "Scanning for completed tasks..."

completed_dir="${PROJECT_MEMORY_DIR}/blackbox5/tasks/completed"
if [ ! -d "$completed_dir" ]; then
    fail "Completed tasks directory not found: $completed_dir"
    exit 1
fi

total_tasks=0
passed_tasks=0
failed_tasks=0

# Find all task.md files in completed directories
while IFS= read -r task_file; do
    ((total_tasks++))
    if validate_task_file "$task_file"; then
        ((passed_tasks++))
    else
        ((failed_tasks++))
    fi
    echo ""
done < <(find "$completed_dir" -name "task.md" -type f 2>/dev/null)

# Summary
echo "═══════════════════════════════════════════════════════════════"
echo "  Validation Summary"
echo "  Total tasks checked: $total_tasks"
echo "  Passed: $passed_tasks"
echo "  Failed: $failed_tasks"
echo "═══════════════════════════════════════════════════════════════"

if [ "$failed_tasks" -gt 0 ]; then
    exit 1
else
    exit 0
fi
