#!/bin/bash
"""
Claude Code Hook: Auto-regenerate docs index after file operations
Triggered after Write, Edit, or Bash operations in 1-docs/
"""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
INDEX_SCRIPT="$SCRIPT_DIR/bin/generate-docs-index.py"
DOCS_DIR="$SCRIPT_DIR/1-docs"

# Check if the last operation affected 1-docs/
if [ -f "/tmp/claude_last_op_path" ]; then
    LAST_PATH=$(cat /tmp/claude_last_op_path)

    if echo "$LAST_PATH" | grep -q "$DOCS_DIR"; then
        if [ -f "$INDEX_SCRIPT" ]; then
            echo "📚 Documentation change detected. Regenerating index..."
            python3 "$INDEX_SCRIPT" 2>/dev/null

            if [ $? -eq 0 ]; then
                echo "✅ INDEX.md regenerated"

                # Auto-commit the index update if in a git repo
                if [ -d "$SCRIPT_DIR/.git" ]; then
                    cd "$SCRIPT_DIR"
                    if git diff --quiet HEAD -- "$DOCS_DIR/INDEX.md" 2>/dev/null; then
                        : # No changes
                    else
                        git add "$DOCS_DIR/INDEX.md" 2>/dev/null
                        echo "📄 INDEX.md staged for commit"
                    fi
                fi
            fi
        fi
    fi
fi
