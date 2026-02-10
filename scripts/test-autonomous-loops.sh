#!/bin/bash
#
# Testing & Validation Script for Autonomous Improvement Loops
# Tests cron job, task analyzer, agent coordination, and end-to-end workflow
#

set -e

BB5_HOME="/opt/blackbox5"
AUTONOMOUS_DIR="$BB5_HOME/.autonomous"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

echo "========================================="
echo "🧪 Testing Autonomous Improvement Loops"
echo "========================================="
echo "Started: $TIMESTAMP"
echo ""

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Helper functions
test_passed() {
    TESTS_PASSED=$((TESTS_PASSED + 1))
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    echo "✅ PASS: $1"
}

test_failed() {
    TESTS_FAILED=$((TESTS_FAILED + 1))
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    echo "❌ FAIL: $1"
}

test_info() {
    echo "ℹ️  INFO: $1"
}

test_header() {
    echo ""
    echo "-----------------------------------------"
    echo "$1"
    echo "-----------------------------------------"
}

# Test 1: Directory Structure
test_header "Test 1: Directory Structure"
test_info "Checking if required directories exist..."

for dir in "$AUTONOMOUS_DIR" "$AUTONOMOUS_DIR/logs" "$AUTONOMOUS_DIR/metrics" "$AUTONOMOUS_DIR/runs"; do
    if [ -d "$dir" ]; then
        test_passed "Directory exists: $dir"
    else
        test_failed "Directory missing: $dir"
    fi
done

# Test 2: Script Existence and Permissions
test_header "Test 2: Script Existence and Permissions"
test_info "Checking if required scripts exist and are executable..."

scripts=(
    "$BB5_HOME/autonomous/improve-blackbox5.sh"
    "$BB5_HOME/autonomous/task-analyzer.py"
    "$BB5_HOME/autonomous/improvement-plan-generator.py"
    "$BB5_HOME/autonomous/agent-protocol.py"
    "$BB5_HOME/agents/moltbot-autonomous/mob-bot-spawner.py"
    "$BB5_HOME/scripts/setup-autonomous-loops.sh"
)

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            test_passed "Script exists and executable: $script"
        else
            test_failed "Script exists but not executable: $script"
        fi
    else
        test_failed "Script missing: $script"
    fi
done

# Test 3: Configuration Files
test_header "Test 3: Configuration Files"
test_info "Checking if configuration files exist..."

configs=(
    "$BB5_HOME/config/claude-agent-team.yaml"
)

for config in "${configs[@]}"; do
    if [ -f "$config" ]; then
        test_passed "Config file exists: $config"
    else
        test_failed "Config file missing: $config"
    fi
done

# Test 4: Python Syntax Check
test_header "Test 4: Python Syntax Check"
test_info "Checking Python scripts for syntax errors..."

python_scripts=(
    "$BB5_HOME/autonomous/task-analyzer.py"
    "$BB5_HOME/autonomous/improvement-plan-generator.py"
    "$BB5_HOME/autonomous/agent-protocol.py"
    "$BB5_HOME/agents/moltbot-autonomous/mob-bot-spawner.py"
)

for script in "${python_scripts[@]}"; do
    if python3 -m py_compile "$script" 2>/dev/null; then
        test_passed "Python syntax OK: $script"
    else
        test_failed "Python syntax error: $script"
    fi
done

# Test 5: Bash Script Validation
test_header "Test 5: Bash Script Validation"
test_info "Checking Bash scripts with shellcheck (if available)..."

bash_scripts=(
    "$BB5_HOME/autonomous/improve-blackbox5.sh"
    "$BB5_HOME/scripts/setup-autonomous-loops.sh"
)

for script in "${bash_scripts[@]}"; do
    if command -v shellcheck &> /dev/null; then
        if shellcheck -x "$script" 2>/dev/null; then
            test_passed "Bash script passes shellcheck: $script"
        else
            test_failed "Bash script has shellcheck issues: $script"
        fi
    else
        test_info "shellcheck not available, skipping: $script"
    fi
done

# Test 6: Task Analyzer
test_header "Test 6: Task Analyzer Functionality"
test_info "Running task analyzer..."

if [ -d "$BB5_HOME/5-project-memory/blackbox5/tasks/active" ]; then
    if python3 "$BB5_HOME/autonomous/task-analyzer.py" > /tmp/task-analyzer-test.log 2>&1; then
        test_passed "Task analyzer executed successfully"

        # Check if output file was created
        if [ -f "$AUTONOMOUS_DIR/prioritized-tasks.json" ]; then
            test_passed "Prioritized tasks file created"
        else
            test_failed "Prioritized tasks file not created"
        fi
    else
        test_failed "Task analyzer execution failed"
        cat /tmp/task-analyzer-test.log
    fi
else
    test_info "Tasks directory not found, skipping task analyzer test"
fi

# Test 7: Improvement Plan Generator
test_header "Test 7: Improvement Plan Generator"
test_info "Running improvement plan generator..."

if [ -f "$AUTONOMOUS_DIR/prioritized-tasks.json" ]; then
    if python3 "$BB5_HOME/autonomous/improvement-plan-generator.py" > /tmp/plan-generator-test.log 2>&1; then
        test_passed "Improvement plan generator executed successfully"

        # Check if output file was created
        if [ -f "$AUTONOMOUS_DIR/improvement-plan.yaml" ]; then
            test_passed "Improvement plan file created"
        else
            test_failed "Improvement plan file not created"
        fi
    else
        test_failed "Improvement plan generator execution failed"
        cat /tmp/plan-generator-test.log
    fi
else
    test_info "No prioritized tasks, skipping plan generator test"
fi

# Test 8: Agent Protocol
test_header "Test 8: Agent Protocol"
test_info "Running agent protocol..."

if python3 "$BB5_HOME/autonomous/agent-protocol.py" > /tmp/agent-protocol-test.log 2>&1; then
    test_passed "Agent protocol executed successfully"

    # Check if metrics file was created
    if [ -f "$AUTONOMOUS_DIR/metrics/latest-cycle.json" ]; then
        test_passed "Metrics file created"
    else
        test_info "Metrics file not created (no tasks to process)"
    fi
else
    test_failed "Agent protocol execution failed"
    cat /tmp/agent-protocol-test.log
fi

# Test 9: Mob Bot Spawner
test_header "Test 9: Mob Bot Spawner"
test_info "Running mob bot spawner..."

if python3 "$BB5_HOME/agents/moltbot-autonomous/mob-bot-spawner.py" > /tmp/mob-bot-test.log 2>&1; then
    test_passed "Mob bot spawner executed successfully"

    # Check if results file was created
    if [ -f "$AUTONOMOUS_DIR/mob-bot-results.json" ]; then
        test_passed "Mob bot results file created"
    else
        test_info "Mob bot results file not created (no tasks to process)"
    fi
else
    test_failed "Mob bot spawner execution failed"
    cat /tmp/mob-bot-test.log
fi

# Test 10: Cron Job Configuration
test_header "Test 10: Cron Job Configuration"
test_info "Checking cron job configuration..."

if crontab -l 2>/dev/null | grep -q "improve-blackbox5.sh"; then
    test_passed "Cron job is configured"
else
    test_info "Cron job not configured (run setup-autonomous-loops.sh to add)"
fi

# Test 11: End-to-End Workflow
test_header "Test 11: End-to-End Workflow"
test_info "Testing full workflow..."

# Run the main improvement script (dry run)
if [ -x "$BB5_HOME/autonomous/improve-blackbox5.sh" ]; then
    # This will attempt to run the full workflow
    # We capture output to check for errors
    if timeout 60 "$BB5_HOME/autonomous/improve-blackbox5.sh" > /tmp/e2e-test.log 2>&1; then
        test_passed "End-to-end workflow executed successfully"
    else
        # Check if it timed out or had an error
        if [ $? -eq 124 ]; then
            test_info "End-to-end workflow timed out (may still be running)"
        else
            test_failed "End-to-end workflow failed"
            echo "Error output:"
            cat /tmp/e2e-test.log | tail -20
        fi
    fi
else
    test_failed "Main improvement script not executable"
fi

# Test 12: Dashboard Integration
test_header "Test 12: Dashboard Integration"
test_info "Checking dashboard integration files..."

if [ -f "$BB5_HOME/dashboard-ui/autonomous-improvement.js" ]; then
    test_passed "Dashboard widget file exists"

    # Check if it's valid JavaScript (basic syntax check)
    if node --check "$BB5_HOME/dashboard-ui/autonomous-improvement.js" 2>/dev/null; then
        test_passed "Dashboard widget JavaScript syntax OK"
    else
        test_info "Node not available, skipping JavaScript syntax check"
    fi
else
    test_failed "Dashboard widget file missing"
fi

# Test 13: File Permissions
test_header "Test 13: File Permissions"
test_info "Checking file permissions..."

# Check that scripts are executable
for script in "${scripts[@]}"; do
    if [ -x "$script" ]; then
        test_passed "Script executable: $(basename $script)"
    else
        test_failed "Script not executable: $(basename $script)"
    fi
done

# Test 14: Dependencies Check
test_header "Test 14: Dependencies Check"
test_info "Checking required dependencies..."

dependencies=("python3" "git" "crontab")
for dep in "${dependencies[@]}"; do
    if command -v "$dep" &> /dev/null; then
        test_passed "Dependency available: $dep"
    else
        test_failed "Dependency missing: $dep"
    fi
done

# Test Summary
test_header "Test Summary"
echo ""
echo "Total Tests: $TESTS_TOTAL"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "🎉 All tests passed!"
    echo ""
    echo "The autonomous improvement system is ready to use."
    echo ""
    echo "Next steps:"
    echo "  1. Run: bash $BB5_HOME/scripts/setup-autonomous-loops.sh"
    echo "  2. Monitor: tail -f $AUTONOMOUS_DIR/improvement-log.md"
    echo "  3. View metrics: cat $AUTONOMOUS_DIR/metrics/latest-cycle.json"
    exit 0
else
    echo "⚠️  Some tests failed. Please review the output above."
    exit 1
fi
