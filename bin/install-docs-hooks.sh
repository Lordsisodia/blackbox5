#!/bin/bash
"""
Install git hooks for auto-generating documentation index
"""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"

echo "Installing documentation index hooks..."

# Create pre-commit hook
cat > "$HOOKS_DIR/pre-commit" << 'HOOK_EOF'
#!/bin/bash
# Auto-generate docs index before commit

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
INDEX_SCRIPT="$SCRIPT_DIR/bin/generate-docs-index.py"

if [ -f "$INDEX_SCRIPT" ]; then
    echo "📚 Auto-generating documentation index..."
    python3 "$INDEX_SCRIPT"

    # Check if INDEX.md was modified
    if git diff --name-only | grep -q "INDEX.md"; then
        echo "📄 INDEX.md updated, adding to commit..."
        git add "$SCRIPT_DIR/1-docs/INDEX.md"
    fi
fi

exit 0
HOOK_EOF

chmod +x "$HOOKS_DIR/pre-commit"
echo "✅ pre-commit hook installed"

# Create post-merge hook (for pulls)
cat > "$HOOKS_DIR/post-merge" << 'HOOK_EOF'
#!/bin/bash
# Auto-generate docs index after pull/merge

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
INDEX_SCRIPT="$SCRIPT_DIR/bin/generate-docs-index.py"

if [ -f "$INDEX_SCRIPT" ]; then
    echo "📚 Regenerating documentation index after merge..."
    python3 "$INDEX_SCRIPT"
fi

exit 0
HOOK_EOF

chmod +x "$HOOKS_DIR/post-merge"
echo "✅ post-merge hook installed"

echo ""
echo "Hooks installed successfully!"
echo "The index will now auto-generate when you:"
echo "  - Make a commit (pre-commit)"
echo "  - Pull/merge changes (post-merge)"
