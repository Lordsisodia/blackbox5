#!/bin/bash
# load-agents-context.sh
# SessionStart hook that auto-loads AGENTS.md for Claude
# This ensures every agent session starts with essential context

# Check if AGENTS.md exists
if [ -f "AGENTS.md" ]; then
    # Output a delimiter to show injected content
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📚 AUTO-LOADED AGENT CONTEXT (AGENTS.md)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    cat AGENTS.md
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
else
    # Fallback if AGENTS.md doesn't exist
    echo "⚠️  AGENTS.md not found. Please create it to auto-load agent context."
fi
