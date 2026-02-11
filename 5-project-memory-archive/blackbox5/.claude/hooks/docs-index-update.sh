#!/bin/bash
"""
Claude Code Hook: Auto-generate documentation index
Triggered after file operations in 1-docs/
"""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
INDEX_SCRIPT="$SCRIPT_DIR/bin/generate-docs-index.py"
DOCS_DIR="$SCRIPT_DIR/1-docs"

# Check if we're in the docs directory
if pwd | grep -q "$DOCS_DIR"; then
    if [ -f "$INDEX_SCRIPT" ]; then
        echo "📚 Auto-regenerating documentation index..."
        python3 "$INDEX_SCRIPT" 2>/dev/null
    fi
fi
