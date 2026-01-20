#!/bin/bash
#
# Blackbox5 Hook: Validate Test Coverage
# Event: PostToolUse (Edit operations)
# Purpose: Maintain quality
#

set -euo pipefail

data=$(cat)
tool_name=$(echo "$data" | jq -r '.tool_name // empty')
file_path=$(echo "$data" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null || echo "")

# Only check Edit operations on code files
if [[ "$tool_name" != "Edit" ]]; then
  exit 0
fi

# Skip if no file path
if [[ -z "$file_path" ]]; then
  exit 0
fi

# Check if it's a code file
if [[ ! "$file_path" =~ \.(ts|tsx|py|js|jsx)$ ]]; then
  exit 0
fi

# Find corresponding test file
if [[ "$file_path" =~ \.ts$ ]]; then
  test_file="${file_path%.ts}.test.ts"
elif [[ "$file_path" =~ \.tsx$ ]]; then
  test_file="${file_path%.tsx}.test.tsx"
elif [[ "$file_path" =~ \.py$ ]]; then
  test_file="${file_path%.py}_test.py"
else
  test_file="${file_path}.test"
fi

# Check if test file exists
if [[ ! -f "$test_file" ]]; then
  echo ""
  echo "🧪 Test Coverage Reminder"
  echo ""
  echo "You edited: $file_path"
  echo "No test file found: $test_file"
  echo ""
  echo "Consider adding tests to maintain code quality."
  echo ""
fi

exit 0
