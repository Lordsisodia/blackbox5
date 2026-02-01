#!/bin/bash
###############################################################################
# RALF Test Runner
# ================
#
# Executes the RALF test suite with various options.
#
# Usage:
#   ./run_tests.sh [options]
#
# Options:
#   --unit          Run unit tests only
#   --integration   Run integration tests only
#   --all           Run all tests (default)
#   --verbose       Verbose output
#   --coverage      Run with coverage reporting (requires coverage.py)
#   --help          Show this help message
#
# Examples:
#   ./run_tests.sh              # Run all tests
#   ./run_tests.sh --unit       # Run unit tests only
#   ./run_tests.sh --verbose    # Run with verbose output
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
TEST_TYPE="all"
VERBOSE=""
COVERAGE=""
PYTEST_ARGS="-v"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --unit)
            TEST_TYPE="unit"
            shift
            ;;
        --integration)
            TEST_TYPE="integration"
            shift
            ;;
        --all)
            TEST_TYPE="all"
            shift
            ;;
        --verbose)
            VERBOSE="-v"
            shift
            ;;
        --coverage)
            COVERAGE="--cov=2-engine/.autonomous/lib --cov-report=term-missing --cov-report=html"
            shift
            ;;
        --help)
            echo "RALF Test Runner"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --unit          Run unit tests only"
            echo "  --integration   Run integration tests only"
            echo "  --all           Run all tests (default)"
            echo "  --verbose       Verbose output"
            echo "  --coverage      Run with coverage reporting"
            echo "  --help          Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0              # Run all tests"
            echo "  $0 --unit       # Run unit tests only"
            echo "  $0 --verbose    # Run with verbose output"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Change to project root
cd "$(dirname "$0")/.."

# Print header
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}RALF Test Runner${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest is not installed${NC}"
    echo "Install it with: pip install pytest"
    exit 1
fi

# Determine test path based on test type
case $TEST_TYPE in
    unit)
        TEST_PATH="tests/unit"
        echo -e "${YELLOW}Running unit tests...${NC}"
        ;;
    integration)
        TEST_PATH="tests/integration"
        echo -e "${YELLOW}Running integration tests...${NC}"
        ;;
    all)
        TEST_PATH="tests"
        echo -e "${YELLOW}Running all tests...${NC}"
        ;;
esac

echo ""

# Run pytest
PYTEST_CMD="pytest $TEST_PATH $PYTEST_ARGS $VERBOSE $COVERAGE"

# Check if coverage is requested
if [ -n "$COVERAGE" ]; then
    if ! python -c "import coverage" &> /dev/null; then
        echo -e "${YELLOW}Warning: coverage.py not installed, skipping coverage${NC}"
        PYTEST_CMD="pytest $TEST_PATH $PYTEST_ARGS $VERBOSE"
    fi
fi

# Execute tests
if eval $PYTEST_CMD; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}All tests passed!${NC}"
    echo -e "${GREEN}========================================${NC}"

    # Show coverage report if generated
    if [ -n "$COVERAGE" ] && [ -f "htmlcov/index.html" ]; then
        echo ""
        echo -e "${YELLOW}Coverage report generated: htmlcov/index.html${NC}"
    fi

    exit 0
else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}Some tests failed!${NC}"
    echo -e "${RED}========================================${NC}"
    exit 1
fi
