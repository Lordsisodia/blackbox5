#!/bin/bash
# validate-run-templates.sh - Validates that run folder templates have actual content
# Not just headers/placeholders
#
# Usage: validate-run-templates.sh [run_directory]
# If no directory provided, uses current directory
#
# Exit codes:
#   0 - All validations passed
#   1 - One or more validations failed
#   2 - Invalid run directory

# Note: Don't use 'set -e' - we need to count errors across multiple validations

# =============================================================================
# CONFIGURATION
# =============================================================================

# Minimum content thresholds
MIN_THOUGHTS_LINES=10        # Beyond headers
MIN_DECISIONS_ENTRIES=1      # At least one decision block
MIN_RESULTS_LINES=5          # Beyond headers
MIN_LEARNINGS_SECTIONS=2     # At least "what worked" and "what was hard"
MIN_ASSUMPTIONS_LINES=3      # Beyond headers

# Content markers that indicate actual content (not placeholders)
THOUGHTS_MARKERS=("Analysis" "Decision" "Progress" "Outcome" "## " "- [x]" "- [ ]")
DECISIONS_MARKERS=("## Decision" "Context:" "Rationale:" "Consequences:")
RESULTS_MARKERS=("Summary" "Changes" "Verification" "Test" "Result:" "PASS" "FAIL")
LEARNINGS_MARKERS=("Worked" "Harder" "Differently" "Patterns" "## ")
ASSUMPTIONS_MARKERS=("Assumption" "## " "- ")

# =============================================================================
# COLORS & LOGGING
# =============================================================================

if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    CYAN='\033[0;36m'
    NC='\033[0m'
else
    GREEN=''
    YELLOW=''
    RED=''
    CYAN=''
    NC=''
fi

log_pass() { echo -e "${GREEN}[PASS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_fail() { echo -e "${RED}[FAIL]${NC} $1"; }
log_info() { echo -e "${CYAN}[INFO]${NC} $1"; }

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

# Count lines excluding markdown headers and empty lines
count_content_lines() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "0"
        return
    fi
    # Count non-empty lines that aren't just headers or comments
    grep -v '^#' "$file" 2>/dev/null | grep -v '^$' | grep -v '^\s*$' | wc -l | tr -d ' '
}

# Check if file contains any of the specified markers
has_content_markers() {
    local file="$1"
    shift
    local markers=("$@")

    if [ ! -f "$file" ]; then
        return 1
    fi

    for marker in "${markers[@]}"; do
        if grep -q "$marker" "$file" 2>/dev/null; then
            return 0
        fi
    done
    return 1
}

# Count decision entries (## Decision headers)
count_decision_entries() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "0"
        return
    fi
    local count=$(grep -c '^## Decision' "$file" 2>/dev/null)
    echo "${count:-0}"
}

# Count learning sections (## headers beyond title)
count_learning_sections() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "0"
        return
    fi
    # Count ## headers excluding the main title
    local count=$(grep -c '^## ' "$file" 2>/dev/null)
    echo "${count:-0}"
}

# Check if file is just a template/placeholder
is_placeholder_content() {
    local file="$1"
    local filename=$(basename "$file")

    if [ ! -f "$file" ]; then
        return 0  # Missing files are considered placeholders
    fi

    # Check for placeholder patterns
    local placeholder_patterns=(
        "Add thoughts here"
        "Document decisions here"
        "Add results here"
        "Document learnings here"
        "List assumptions here"
        "_Add.*as you work"
        "TODO"
        "FIXME"
        "placeholder"
        "TBD"
        "Coming soon"
    )

    for pattern in "${placeholder_patterns[@]}"; do
        if grep -qi "$pattern" "$file" 2>/dev/null; then
            return 0  # Found placeholder text
        fi
    done

    # Check if file only has a title/header and nothing else
    local content_lines=$(count_content_lines "$file")
    if [ "$content_lines" -le 2 ]; then
        return 0  # Essentially empty
    fi

    return 1  # Has actual content
}

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

validate_thoughts() {
    local file="$1"
    local errors=0

    echo ""
    log_info "Validating THOUGHTS.md..."

    if [ ! -f "$file" ]; then
        log_fail "THOUGHTS.md not found"
        return 1
    fi

    if is_placeholder_content "$file"; then
        log_fail "THOUGHTS.md appears to be a placeholder (no actual thoughts recorded)"
        errors=$((errors + 1))
    fi

    local content_lines=$(count_content_lines "$file")
    if [ "$content_lines" -lt "$MIN_THOUGHTS_LINES" ]; then
        log_warn "THOUGHTS.md has only $content_lines lines of content (min: $MIN_THOUGHTS_LINES)"
        errors=$((errors + 1))
    fi

    if ! has_content_markers "$file" "${THOUGHTS_MARKERS[@]}"; then
        log_warn "THOUGHTS.md missing expected content markers (Analysis, Progress, Outcome, etc.)"
        errors=$((errors + 1))
    fi

    if [ $errors -eq 0 ]; then
        log_pass "THOUGHTS.md has meaningful content ($content_lines lines)"
    fi

    return $errors
}

validate_decisions() {
    local file="$1"
    local errors=0

    echo ""
    log_info "Validating DECISIONS.md..."

    if [ ! -f "$file" ]; then
        log_fail "DECISIONS.md not found"
        return 1
    fi

    if is_placeholder_content "$file"; then
        log_fail "DECISIONS.md appears to be a placeholder (no actual decisions recorded)"
        errors=$((errors + 1))
    fi

    local decision_count=$(count_decision_entries "$file")
    if [ "$decision_count" -lt "$MIN_DECISIONS_ENTRIES" ]; then
        log_fail "DECISIONS.md has $decision_count decision entries (min: $MIN_DECISIONS_ENTRIES)"
        errors=$((errors + 1))
    fi

    if ! has_content_markers "$file" "${DECISIONS_MARKERS[@]}"; then
        log_warn "DECISIONS.md missing expected structure (Context, Rationale, Consequences)"
        errors=$((errors + 1))
    fi

    if [ $errors -eq 0 ]; then
        log_pass "DECISIONS.md has $decision_count decision entries"
    fi

    return $errors
}

validate_results() {
    local file="$1"
    local errors=0

    echo ""
    log_info "Validating RESULTS.md..."

    if [ ! -f "$file" ]; then
        log_fail "RESULTS.md not found"
        return 1
    fi

    if is_placeholder_content "$file"; then
        log_fail "RESULTS.md appears to be a placeholder (no actual results recorded)"
        errors=$((errors + 1))
    fi

    local content_lines=$(count_content_lines "$file")
    if [ "$content_lines" -lt "$MIN_RESULTS_LINES" ]; then
        log_warn "RESULTS.md has only $content_lines lines of content (min: $MIN_RESULTS_LINES)"
        errors=$((errors + 1))
    fi

    if ! has_content_markers "$file" "${RESULTS_MARKERS[@]}"; then
        log_warn "RESULTS.md missing expected content (Summary, Changes, Verification)"
        errors=$((errors + 1))
    fi

    if [ $errors -eq 0 ]; then
        log_pass "RESULTS.md has meaningful content ($content_lines lines)"
    fi

    return $errors
}

validate_learnings() {
    local file="$1"
    local errors=0

    echo ""
    log_info "Validating LEARNINGS.md..."

    if [ ! -f "$file" ]; then
        log_fail "LEARNINGS.md not found"
        return 1
    fi

    if is_placeholder_content "$file"; then
        log_fail "LEARNINGS.md appears to be a placeholder (no actual learnings recorded)"
        errors=$((errors + 1))
    fi

    local section_count=$(count_learning_sections "$file")
    if [ "$section_count" -lt "$MIN_LEARNINGS_SECTIONS" ]; then
        log_warn "LEARNINGS.md has only $section_count sections (min: $MIN_LEARNINGS_SECTIONS)"
        errors=$((errors + 1))
    fi

    if ! has_content_markers "$file" "${LEARNINGS_MARKERS[@]}"; then
        log_warn "LEARNINGS.md missing expected sections (What Worked, What Was Harder, etc.)"
        errors=$((errors + 1))
    fi

    if [ $errors -eq 0 ]; then
        log_pass "LEARNINGS.md has $section_count sections of insights"
    fi

    return $errors
}

validate_assumptions() {
    local file="$1"
    local errors=0

    echo ""
    log_info "Validating ASSUMPTIONS.md..."

    if [ ! -f "$file" ]; then
        log_warn "ASSUMPTIONS.md not found (optional but recommended)"
        return 0  # Assumptions is optional
    fi

    if is_placeholder_content "$file"; then
        log_warn "ASSUMPTIONS.md appears to be a placeholder"
        errors=$((errors + 1))
    fi

    local content_lines=$(count_content_lines "$file")
    if [ "$content_lines" -lt "$MIN_ASSUMPTIONS_LINES" ]; then
        log_warn "ASSUMPTIONS.md has only $content_lines lines of content"
        errors=$((errors + 1))
    fi

    if [ $errors -eq 0 ]; then
        log_pass "ASSUMPTIONS.md has meaningful content ($content_lines lines)"
    fi

    return $errors
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    local run_dir="${1:-.}"

    # Validate directory
    if [ ! -d "$run_dir" ]; then
        log_fail "Invalid run directory: $run_dir"
        exit 2
    fi

    # Convert to absolute path
    run_dir=$(cd "$run_dir" && pwd)

    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Run Template Validation"
    echo "  Directory: ${run_dir/#$HOME/~}"
    echo "═══════════════════════════════════════════════════════════════"

    local total_errors=0

    # Validate each file
    validate_thoughts "$run_dir/THOUGHTS.md"
    total_errors=$((total_errors + $?))

    validate_decisions "$run_dir/DECISIONS.md"
    total_errors=$((total_errors + $?))

    validate_results "$run_dir/RESULTS.md"
    total_errors=$((total_errors + $?))

    validate_learnings "$run_dir/LEARNINGS.md"
    total_errors=$((total_errors + $?))

    validate_assumptions "$run_dir/ASSUMPTIONS.md"
    total_errors=$((total_errors + $?))

    # Summary
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    if [ $total_errors -eq 0 ]; then
        log_pass "All validations passed - run documentation is complete"
        echo "═══════════════════════════════════════════════════════════════"
        exit 0
    else
        log_fail "$total_errors validation(s) failed - run documentation incomplete"
        echo "═══════════════════════════════════════════════════════════════"
        exit 1
    fi
}

# Run main function
main "$@"
