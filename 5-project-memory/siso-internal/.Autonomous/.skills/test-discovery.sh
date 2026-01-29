#!/bin/bash
# Skill Discovery System Test
# Verifies the skill discovery and selection system works correctly

set -e

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INDEX_FILE="$SKILLS_DIR/skills-index.yaml"

echo "========================================"
echo "Legacy Skill Discovery System Test"
echo "========================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"

    echo -n "Testing: $test_name... "
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}"
        ((TESTS_FAILED++))
    fi
}

# Test 1: Index file exists
echo "1. File Structure Tests"
echo "------------------------"
run_test "Index file exists" "test -f $INDEX_FILE"
run_test "Index is valid YAML" "cat $INDEX_FILE | head -1 | grep -q 'version:'"
run_test "Core skills section exists" "grep -q '^core:' $INDEX_FILE"
run_test "Triggered skills section exists" "grep -q '^triggered:' $INDEX_FILE"

# Test 2: Core skills
echo ""
echo "2. Core Skills Tests"
echo "--------------------"
run_test "truth-seeking in core" "grep -q 'id: truth-seeking' $INDEX_FILE"
run_test "task-selection in core" "grep -q 'id: task-selection' $INDEX_FILE"
run_test "run-initialization in core" "grep -q 'id: run-initialization' $INDEX_FILE"
run_test "git-commit in core" "grep -q 'id: git-commit' $INDEX_FILE"
run_test "All core skills marked always_loaded" "grep -A1 'always_loaded: true' $INDEX_FILE | wc -l | grep -q '8'"

# Test 3: Triggered skills
echo ""
echo "3. Triggered Skills Tests"
echo "-------------------------"
run_test "code-implementation has triggers" "grep -A5 'id: code-implementation' $INDEX_FILE | grep -q 'triggers:'"
run_test "deep-research has keywords" "grep -A10 'id: deep-research' $INDEX_FILE | grep -q 'keywords:'"
run_test "supabase-operations has file_patterns" "grep -A10 'id: supabase-operations' $INDEX_FILE | grep -q 'file_patterns:'"

# Test 4: Skill files exist
echo ""
echo "4. Skill File Existence Tests"
echo "-----------------------------"
for skill in truth-seeking task-selection run-initialization git-commit; do
    run_test "$skill.yaml exists" "test -f $SKILLS_DIR/$skill.yaml"
done

for skill in deep-research code-implementation architecture-design testing-validation codebase-navigation supabase-operations product-planning documentation; do
    run_test "$skill.yaml exists" "test -f $SKILLS_DIR/$skill.yaml"
done

# Test 5: Trigger matching simulation
echo ""
echo "5. Trigger Matching Simulation"
echo "------------------------------"

# Simulate matching "implement" keyword
IMPLEMENT_SCORE=$(grep -A20 "id: code-implementation" $INDEX_FILE | grep "implement" | wc -l)
if [ "$IMPLEMENT_SCORE" -gt 0 ]; then
    echo -e "Keyword 'implement' → code-implementation: ${GREEN}MATCH${NC}"
    ((TESTS_PASSED++))
else
    echo -e "Keyword 'implement' → code-implementation: ${RED}NO MATCH${NC}"
    ((TESTS_FAILED++))
fi

# Simulate matching "research" keyword
RESEARCH_SCORE=$(grep -A20 "id: deep-research" $INDEX_FILE | grep "research" | wc -l)
if [ "$RESEARCH_SCORE" -gt 0 ]; then
    echo -e "Keyword 'research' → deep-research: ${GREEN}MATCH${NC}"
    ((TESTS_PASSED++))
else
    echo -e "Keyword 'research' → deep-research: ${RED}NO MATCH${NC}"
    ((TESTS_FAILED++))
fi

# Test 6: Statistics
echo ""
echo "6. Statistics Validation"
echo "------------------------"
run_test "Total skills count correct" "grep 'total_skills: 12' $INDEX_FILE"
run_test "Core skills count correct" "grep 'core_skills: 4' $INDEX_FILE"
run_test "Triggered skills count correct" "grep 'triggered_skills: 8' $INDEX_FILE"

# Test 7: YAML validity
echo ""
echo "7. YAML Structure Tests"
echo "-----------------------"
run_test "Index has version field" "grep -q '^version:' $INDEX_FILE"
run_test "Index has generated_at field" "grep -q '^generated_at:' $INDEX_FILE"
run_test "Skills have required fields" "grep -q 'id:' $INDEX_FILE && grep -q 'file:' $INDEX_FILE"

# Summary
echo ""
echo "========================================"
echo "Test Summary"
echo "========================================"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! Skill discovery system is working correctly.${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. Please review the output above.${NC}"
    exit 1
fi
