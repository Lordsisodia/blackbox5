#!/bin/bash
#
# Blackbox5 Hook: Analyze Change Impact
# Event: PreToolUse (Edit/Write)
# Purpose: Understand blast radius before editing
#

set -euo pipefail

data=$(cat)
tool_name=$(echo "$data" | jq -r '.tool_name // empty')
file_path=$(echo "$data" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null || echo "")

# Only analyze Edit operations
if [[ "$tool_name" != "Edit" ]]; then
  exit 0
fi

# Skip if no file path
if [[ -z "$file_path" ]] || [[ ! -f "$file_path" ]]; then
  exit 0
fi

# Find what this file imports (Python)
if [[ "$file_path" == *.py ]]; then
  imports=$(grep -E "^import |^from " "$file_path" 2>/dev/null | head -20 || echo "")

  # Find what imports this file (basic heuristic)
  filename=$(basename "$file_path" .py)
  importers=$(find . -name "*.py" -exec grep -l "from.*$filename\|import.*$filename" {} \; 2>/dev/null | head -5 || echo "")

# Find what this file imports (TypeScript/JavaScript)
elif [[ "$file_path" == *.ts ]] || [[ "$file_path" == *.tsx ]] || [[ "$file_path" == *.js ]]; then
  imports=$(grep -E "^import |from " "$file_path" 2>/dev/null | head -20 || echo "")

  filename=$(basename "$file_path" .ts)
  importers=$(find . -name "*.ts" -o -name "*.tsx" | xargs grep -l "from.*$filename\|import.*$filename" 2>/dev/null | head -5 || echo "")

else
  # Generic fallback
  imports="(import analysis not available for this file type)"
  importers="(importer analysis not available)"
fi

# Show impact if significant
if [[ -n "$importers" ]] && [[ "$importers" != "(importer analysis not available)" ]]; then
  echo ""
  echo "📊 Change Impact Analysis for: $file_path"
  echo ""

  if [[ -n "$imports" ]] && [[ "$imports" != "(import analysis not available for this file type)" ]]; then
    echo "This file imports:"
    echo "$imports" | head -5
    echo ""
  fi

  if [[ -n "$importers" ]]; then
    echo "This file is used by:"
    echo "$importers"
    echo ""
  fi

  echo "⚠️  Changes here may affect dependent files."
  echo ""
fi

exit 0
