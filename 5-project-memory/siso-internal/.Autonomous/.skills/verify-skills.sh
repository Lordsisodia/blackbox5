#!/bin/bash
# Skill Discovery System Verification
# Simple verification that skills are properly configured

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INDEX_FILE="$SKILLS_DIR/skills-index.yaml"

echo "========================================"
echo "Legacy Skill Discovery Verification"
echo "========================================"
echo ""

ERRORS=0

check_file() {
    if [ -f "$1" ]; then
        echo "✓ $2"
    else
        echo "✗ $2 (missing)"
        ((ERRORS++))
    fi
}

check_yaml_field() {
    if grep -q "$1" "$INDEX_FILE"; then
        echo "✓ $2"
    else
        echo "✗ $2 (not found)"
        ((ERRORS++))
    fi
}

echo "1. Checking Index File"
echo "----------------------"
check_file "$INDEX_FILE" "skills-index.yaml exists"

echo ""
echo "2. Checking Core Skills in Index"
echo "---------------------------------"
check_yaml_field "id: truth-seeking" "truth-seeking listed"
check_yaml_field "id: task-selection" "task-selection listed"
check_yaml_field "id: run-initialization" "run-initialization listed"
check_yaml_field "id: git-commit" "git-commit listed"

echo ""
echo "3. Checking Triggered Skills in Index"
echo "--------------------------------------"
check_yaml_field "id: deep-research" "deep-research listed"
check_yaml_field "id: code-implementation" "code-implementation listed"
check_yaml_field "id: architecture-design" "architecture-design listed"
check_yaml_field "id: testing-validation" "testing-validation listed"

echo ""
echo "4. Checking Skill Files Exist"
echo "-----------------------------"
check_file "$SKILLS_DIR/truth-seeking.yaml" "truth-seeking.yaml"
check_file "$SKILLS_DIR/task-selection.yaml" "task-selection.yaml"
check_file "$SKILLS_DIR/code-implementation.yaml" "code-implementation.yaml"
check_file "$SKILLS_DIR/deep-research.yaml" "deep-research.yaml"

echo ""
echo "5. Checking Trigger Configuration"
echo "----------------------------------"
if grep -A10 "id: code-implementation" "$INDEX_FILE" | grep -q "keywords:"; then
    echo "✓ code-implementation has triggers"
else
    echo "✗ code-implementation missing triggers"
    ((ERRORS++))
fi

if grep -A10 "id: deep-research" "$INDEX_FILE" | grep -q "keywords:"; then
    echo "✓ deep-research has triggers"
else
    echo "✗ deep-research missing triggers"
    ((ERRORS++))
fi

echo ""
echo "========================================"
if [ $ERRORS -eq 0 ]; then
    echo "✓ All checks passed!"
    echo "Skill discovery system is ready."
    exit 0
else
    echo "✗ $ERRORS check(s) failed"
    exit 1
fi
