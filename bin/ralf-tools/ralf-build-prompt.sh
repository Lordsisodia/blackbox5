#!/bin/bash
# RALF Prompt Builder
# Builds dynamic prompts by concatenating context files
# Context files are self-updating - agents modify them, next run gets updates

set -e

# Get script directory and source paths library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../../2-engine/helpers/legacy/paths.sh"

AGENT_TYPE="${1:-executor}"
PROJECT_NAME="${RALF_PROJECT_NAME:-blackbox5}"
PROJECT_ROOT="$(get_blackbox5_root)"
PROJECT_MEMORY="$(get_project_path)"

# =============================================================================
# CONTEXT FILE LOCATIONS (self-updating documents)
# =============================================================================

# Core context files that agents can update
PROJECT_STRUCTURE="$PROJECT_MEMORY/project-structure.md"
ARCHITECTURE_MAP="$PROJECT_MEMORY/architecture/map.md"
ACTIVE_DECISIONS="$PROJECT_MEMORY/decisions/active.md"
GOALS_YAML="$PROJECT_MEMORY/goals.yaml"
RECENT_LEARNINGS="$PROJECT_MEMORY/learnings/recent.md"
STATE_CURRENT="$PROJECT_MEMORY/state/current.md"

# Communication files (from project .autonomous/communications/)
COMMUNICATIONS_DIR="$PROJECT_MEMORY/.autonomous/communications"
COMMUNICATIONS_QUEUE="$COMMUNICATIONS_DIR/queue.yaml"
COMMUNICATIONS_TASKS="$COMMUNICATIONS_DIR/tasks.yaml"
COMMUNICATIONS_EVENTS="$COMMUNICATIONS_DIR/events.yaml"
COMMUNICATIONS_CHAT="$COMMUNICATIONS_DIR/chat-log.yaml"

# Static files
SYSTEM_IDENTITY="$(get_engine_path)/instructions/system/${AGENT_TYPE}-identity.md"
AGENT_PROTOCOL="$(get_engine_path)/instructions/procedures/${AGENT_TYPE}-protocol.md"

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

section() {
    echo ""
    echo "# ============================================================================="
    echo "# $1"
    echo "# ============================================================================="
    echo ""
}

subsection() {
    echo ""
    echo "## $1"
    echo ""
}

include_file() {
    local file="$1"
    local description="$2"

    if [ -f "$file" ]; then
        subsection "$description"
        cat "$file"
    else
        subsection "$description"
        echo "*File not found: ${file#$PROJECT_ROOT/}*"
        echo "*This context is not yet available.*"
    fi
}

include_yaml() {
    local file="$1"
    local description="$2"

    if [ -f "$file" ]; then
        subsection "$description"
        echo "\`\`\`yaml"
        cat "$file"
        echo "\`\`\`"
    else
        subsection "$description"
        echo "*File not found: ${file#$PROJECT_ROOT/}*"
        echo "*This context is not yet available.*"
    fi
}

# =============================================================================
# BUILD PROMPT
# =============================================================================

# 1. SYSTEM IDENTITY (static)
if [ -f "$SYSTEM_IDENTITY" ]; then
    cat "$SYSTEM_IDENTITY"
else
    echo "# RALF ${AGENT_TYPE^^} Agent"
    echo ""
    echo "You are a ${AGENT_TYPE} agent in the RALF system."
fi

section "DYNAMIC CONTEXT (Self-Updating)"

echo "The following context is loaded from files that are updated throughout"
echo "the project lifecycle. These files may have been modified by previous"
echo "agent runs, so the information is always current."

# 2. PROJECT STRUCTURE (self-updating)
include_file "$PROJECT_STRUCTURE" "Project Structure"

# 3. ARCHITECTURE MAP (self-updating)
include_file "$ARCHITECTURE_MAP" "Architecture Map"

# 4. ACTIVE DECISIONS (self-updating)
include_file "$ACTIVE_DECISIONS" "Active Architectural Decisions"

# 5. GOALS (from YAML - self-updating)
include_yaml "$GOALS_YAML" "Current Goals"

# 6. RECENT LEARNINGS (self-updating)
include_file "$RECENT_LEARNINGS" "Recent Learnings"

# 7. CURRENT STATE (self-updating)
include_file "$STATE_CURRENT" "Current System State"

# 8. COMMUNICATIONS QUEUE (from YAML - self-updating)
include_yaml "$COMMUNICATIONS_QUEUE" "Task Queue (Next Task)"

# 9. COMMUNICATIONS TASKS (from YAML - self-updating)
include_yaml "$COMMUNICATIONS_TASKS" "All Tasks (Master List)"

# 10. RECENT EVENTS (from YAML - self-updating)
if [ -f "$COMMUNICATIONS_EVENTS" ]; then
    subsection "Recent Events"
    echo "```yaml"
    # Show last 20 events
    tail -50 "$COMMUNICATIONS_EVENTS"
    echo "```"
fi

# 11. UNRESOLVED CHAT (from YAML - self-updating)
if [ -f "$COMMUNICATIONS_CHAT" ]; then
    subsection "Unresolved Messages"
    echo "```yaml"
    # Show unresolved messages
    grep -A 10 "resolved: false" "$COMMUNICATIONS_CHAT" 2>/dev/null || echo "No unresolved messages"
    echo "```"
fi

section "AGENT INSTRUCTIONS"

# 9. AGENT-SPECIFIC PROTOCOL (static)
if [ -f "$AGENT_PROTOCOL" ]; then
    cat "$AGENT_PROTOCOL"
else
    echo "Execute tasks according to your role as ${AGENT_TYPE}."
fi

section "CONTEXT UPDATE RESPONSIBILITIES"

echo "As you work, you MUST update the context files when relevant changes occur:"
echo ""
echo "| Context File | Update When... |"
echo "|--------------|----------------|"
echo "| project-structure.md | Folder structure changes |"
echo "| architecture/map.md | Code architecture changes |"
echo "| decisions/active.md | New decisions made |"
echo "| learnings/recent.md | New discoveries made |"
echo "| state/current.md | System state changes |"
echo "| communications/tasks.yaml | New tasks identified |"
echo "| communications/events.yaml | Significant events occur |"
echo ""
echo "This ensures the next agent run has current context automatically."
