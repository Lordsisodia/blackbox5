#!/bin/bash
# ============================================================================
# BLACKBOX5 - TEST RUNNER
# ============================================================================
# Purpose: Unified test runner for CI/CD pipeline and local development
# Usage: bin/run-tests.sh [unit|integration|lint|yaml|all] [options]
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Test directories
TEST_DIR="2-engine/tests"
UNIT_DIR="$TEST_DIR/unit"
INTEGRATION_DIR="$TEST_DIR/integration"

# Python version
PYTHON_VERSION="${PYTHON_VERSION:-3.12}"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking dependencies..."

    if ! command -v python &> /dev/null; then
        log_error "Python not found. Please install Python $PYTHON_VERSION"
        exit 1
    fi

    if ! python -c "import pytest" &> /dev/null; then
        log_error "pytest not installed. Run: pip install -r requirements-dev.txt"
        exit 1
    fi

    log_info "Dependencies OK"
}

# ============================================================================
# TEST FUNCTIONS
# ============================================================================

run_unit_tests() {
    log_info "Running unit tests..."

    local extra_args="$@"

    if [ -d "$UNIT_DIR" ]; then
        python -m pytest "$UNIT_DIR" \
            -v \
            --tb=short \
            --disable-warnings \
            -m "unit and not integration and not slow" \
            $extra_args
    else
        log_warn "Unit test directory not found: $UNIT_DIR"
        return 0
    fi
}

run_integration_tests() {
    log_info "Running integration tests..."

    local extra_args="$@"

    if [ -d "$INTEGRATION_DIR" ]; then
        python -m pytest "$INTEGRATION_DIR" \
            -v \
            --tb=short \
            --disable-warnings \
            -m "integration" \
            $extra_args
    else
        log_warn "Integration test directory not found: $INTEGRATION_DIR"
        return 0
    fi
}

run_all_tests() {
    log_info "Running all tests..."

    local extra_args="$@"

    if [ -d "$TEST_DIR" ]; then
        python -m pytest "$TEST_DIR" \
            -v \
            --tb=short \
            --disable-warnings \
            $extra_args
    else
        log_warn "Test directory not found: $TEST_DIR"
        return 0
    fi
}

# ============================================================================
# LINTING FUNCTIONS
# ============================================================================

run_linting() {
    log_info "Running linting checks..."

    local has_error=0

    # Check black formatting
    log_info "  Checking code formatting (black)..."
    if black --check --diff . 2>&1 | grep -q "would reformat"; then
        log_error "Code formatting issues found. Run: black ."
        has_error=1
    else
        log_info "  Code formatting OK"
    fi

    # Check import sorting
    log_info "  Checking import sorting (isort)..."
    if isort --check-only --diff . 2>&1 | grep -q "Fixing"; then
        log_error "Import sorting issues found. Run: isort ."
        has_error=1
    else
        log_info "  Import sorting OK"
    fi

    # Check flake8
    log_info "  Running flake8..."
    if flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; then
        log_info "  Flake8 OK (no critical errors)"
    else
        log_error "Critical flake8 errors found"
        has_error=1
    fi

    return $has_error
}

# ============================================================================
# YAML VALIDATION
# ============================================================================

validate_yaml() {
    log_info "Validating YAML files..."

    local has_error=0

    # Find all YAML files
    while IFS= read -r -d '' yaml_file; do
        log_info "  Checking: $yaml_file"

        # Check if yamllint is available
        if command -v yamllint &> /dev/null; then
            if ! yamllint -d "{extends: default, rules: {line-length: {max: 120}}}" "$yaml_file" 2>&1; then
                log_error "YAML validation failed for: $yaml_file"
                has_error=1
            fi
        else
            # Basic Python YAML validation as fallback
            if ! python -c "import yaml; yaml.safe_load(open('$yaml_file'))" 2>&1; then
                log_error "Invalid YAML: $yaml_file"
                has_error=1
            fi
        fi
    done < <(find . -type f \( -name "*.yaml" -o -name "*.yml" \) -not -path "./.git/*" -print0)

    if [ $has_error -eq 0 ]; then
        log_info "YAML validation OK"
    fi

    return $has_error
}

# ============================================================================
# QUALITY GATE
# ============================================================================

run_quality_gate() {
    log_info "Running quality gate..."

    local all_passed=true

    # Run unit tests
    if ! run_unit_tests; then
        log_error "Unit tests failed"
        all_passed=false
    fi

    # Run linting
    if ! run_linting; then
        log_error "Linting failed"
        all_passed=false
    fi

    # Validate YAML
    if ! validate_yaml; then
        log_error "YAML validation failed"
        all_passed=false
    fi

    if [ "$all_passed" = true ]; then
        log_info "Quality gate: PASSED"
        return 0
    else
        log_error "Quality gate: FAILED"
        return 1
    fi
}

# ============================================================================
# MAIN ENTRYPOINT
# ============================================================================

print_usage() {
    cat << EOF
Usage: bin/run-tests.sh [command] [options]

Commands:
  unit           Run unit tests only
  integration    Run integration tests only
  all            Run all tests (unit + integration)
  lint           Run linting checks (black, isort, flake8)
  yaml           Validate YAML files
  quality-gate   Run full quality gate (tests + linting + validation)
  help           Show this help message

Options:
  --fast-only    Run only fast tests (skip slow/integration tests)
  --cov          Run with coverage report
  --verbose      Enable verbose output

Examples:
  bin/run-tests.sh unit                    # Run unit tests
  bin/run-tests.sh unit --fast-only        # Run only fast unit tests
  bin/run-tests.sh quality-gate            # Run full quality gate
  bin/run-tests.sh all --cov              # Run all tests with coverage

EOF
}

main() {
    local command="${1:-help}"
    shift || true

    # Parse options
    local extra_args=""
    local fast_only=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --fast-only)
                fast_only=true
                extra_args="$extra_args -m 'not slow'"
                shift
                ;;
            --cov)
                extra_args="$extra_args --cov=2-engine --cov-report=term-missing"
                shift
                ;;
            --verbose)
                extra_args="$extra_args -vv"
                shift
                ;;
            *)
                log_warn "Unknown option: $1"
                shift
                ;;
        esac
    done

    # Execute command
    case "$command" in
        unit)
            check_dependencies
            run_unit_tests $extra_args
            ;;
        integration)
            check_dependencies
            run_integration_tests $extra_args
            ;;
        all)
            check_dependencies
            run_all_tests $extra_args
            ;;
        lint)
            run_linting
            ;;
        yaml)
            validate_yaml
            ;;
        quality-gate)
            check_dependencies
            run_quality_gate
            ;;
        help|--help|-h)
            print_usage
            exit 0
            ;;
        *)
            log_error "Unknown command: $command"
            print_usage
            exit 1
            ;;
    esac
}

main "$@"
