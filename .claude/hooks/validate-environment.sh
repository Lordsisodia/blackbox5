#!/bin/bash
#
# Blackbox5 Hook: Validate Environment
# Event: SessionStart
# Purpose: Prevent production accidents
#

set -euo pipefail

# Check git branch
if git rev-parse --git-dir > /dev/null 2>&1; then
  current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")

  if [[ "$current_branch" == "main" ]] || [[ "$current_branch" == "master" ]]; then
    echo ""
    echo "⚠️  Environment Warning"
    echo ""
    echo "You are on the $current_branch branch."
    echo ""
    echo "Best practice: Create a feature branch for your work:"
    echo "  git checkout -b feature/your-feature-name"
    echo ""
  fi
fi

# Check for production environment variables
if [[ -n "${PRODUCTION:-}" ]] && [[ "$PRODUCTION" == "1" ]]; then
  echo ""
  echo "🚨 PRODUCTION ENVIRONMENT DETECTED"
  echo ""
  echo "You are working in a production environment."
  echo ""
  echo "Be extra careful:"
  echo "  - Double-check all changes"
  echo "  - Test in staging first"
  echo "  - Have a rollback plan ready"
  echo ""
fi

# Check working directory
cwd=$(pwd)
if [[ "$cwd" =~ (node_modules|\.git|dist|build) ]]; then
  echo ""
  echo "📍 Directory Warning"
  echo ""
  echo "You are in: $cwd"
  echo ""
  echo "This may not be the ideal working directory."
  echo "Consider navigating to the project root."
  echo ""
fi

exit 0
