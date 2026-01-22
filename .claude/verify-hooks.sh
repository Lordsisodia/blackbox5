#!/bin/bash
#
# Blackbox5 Hooks Verification Script
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$SCRIPT_DIR/hooks"

echo "Blackbox5 Hooks Verification"
echo "=========================="
echo ""

# Check if hooks directory exists
if [[ ! -d "$HOOKS_DIR" ]]; then
  echo "❌ Hooks directory not found: $HOOKS_DIR"
  exit 1
fi

echo "✓ Hooks directory exists"
echo ""

# Check hook executability
echo "Checking hook executability..."
non_executable=0

for hook in "$HOOKS_DIR"/*.sh; do
  if [[ -f "$hook" ]]; then
    if [[ -x "$hook" ]]; then
      echo "  ✓ $(basename "$hook")"
    else
      echo "  ✗ $(basename "$hook") (not executable)"
      non_executable=$((non_executable + 1))
    fi
  fi
done

if [[ $non_executable -gt 0 ]]; then
  echo ""
  echo "⚠️  $non_executable hooks are not executable"
  echo "Run: chmod +x .claude/hooks/*.sh"
fi

echo ""
echo "Checking settings.json..."

SETTINGS_FILE="$SCRIPT_DIR/settings.json"
if [[ -f "$SETTINGS_FILE" ]]; then
  echo "✓ settings.json exists"

  # Validate JSON
  if command -v jq > /dev/null 2>&1 && jq empty "$SETTINGS_FILE" > /dev/null 2>&1; then
    echo "✓ settings.json is valid JSON"
  else
    echo "⚠️  jq not installed or settings.json has errors"
  fi
else
  echo "✗ settings.json not found at $SETTINGS_FILE"
fi

echo ""
echo "Checking git hooks..."

GIT_HOOKS=".git/hooks/commit-msg .git/hooks/pre-commit"

for hook in $GIT_HOOKS; do
  if [[ -f "$hook" ]]; then
    if [[ -x "$hook" ]]; then
      echo "  ✓ $(basename "$hook")"
    else
      echo "  ✗ $(basename "$hook") (not executable)"
    fi
  else
    echo "  ✗ $(basename "$hook") (not found)"
  fi
done

echo ""
echo "Verification complete!"
echo ""
echo "Next steps:"
echo "  1. Start Claude Code in this directory"
echo "  2. Hooks will run automatically"
echo "  3. Check .claude/hooks/README.md for documentation"
