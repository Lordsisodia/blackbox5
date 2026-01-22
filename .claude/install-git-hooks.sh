#!/bin/bash
#
# Blackbox5 Git Hooks Installation Script
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Installing Blackbox5 Git Hooks..."

# Copy hooks to .git/hooks
cp "$PROJECT_ROOT/.git/hooks/"* "$PROJECT_ROOT/.git/hooks/" 2>/dev/null || true

# Make hooks executable
chmod +x "$PROJECT_ROOT/.git/hooks/"*

echo "✓ Git hooks installed"
echo ""
echo "Hooks installed:"
echo "  - pre-commit: Validates .env files, large files"
echo "  - commit-msg: Enforces conventional commits"
echo ""
echo "Bypass with: git commit --no-verify"
