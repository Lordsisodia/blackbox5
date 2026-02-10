#!/bin/bash
# SessionStart Enhanced Hook
# VERSION: 1.0.0
# Purpose: Initialize agent session with run folder, templates, context, and environment
#
# This hook:
# - Discovers project root and structure (no env vars needed)
# - Detects agent type (planner/executor/architect/unknown)
# - Creates run folder with all required templates
# - Loads relevant memories from vector store
# - Creates AGENT_CONTEXT.md with task details
# - Exports environment variables for other hooks
# - Returns JSON to Claude Code with context

set -euo pipefail

VERSION="1.0.0"

# Script directory for self-discovery
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Project directories
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROJECT_MEMORY_DIR="$PROJECT_ROOT/5-project-memory"
PROJECT_NAME="blackbox5"

# Library paths
LIB_DIR="$SCRIPT_DIR/lib"
AGENT_DETECTOR="$LIB_DIR/agent-detector.sh"
RUN_INITIALIZER="$LIB_DIR/run-initializer.sh"

# Source libraries
source "$AGENT_DETECTOR"
source "$RUN_INITIALIZER"

# Read input from stdin (JSON)
INPUT=$(head -c 100000)

# Parse session info
SOURCE=$(echo "$INPUT" | jq -r '.source // "startup"' 2>/dev/null || echo "startup")
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")

# Detect agent type
AGENT_TYPE=$(detect_agent_type)

# Get current task information (if available)
CURRENT_TASK_ID=""
CURRENT_TASK_TITLE=""
ACCEPTANCE_CRITERIA=""

# Check if we're in a task directory
TASK_MARKER=""
if [ -f ".task-claimed" ]; then
    CURRENT_TASK_ID=$(cat .task-claimed 2>/dev/null || echo "")
elif [ -f ".current-task" ]; then
    CURRENT_TASK_ID=$(cat .current-task 2>/dev/null || echo "")
fi

# Try to get task details from queue.yaml if we have a task ID
if [ -n "$CURRENT_TASK_ID" ] && [ -f "$PROJECT_ROOT/.autonomous/agents/communications/queue.yaml" ]; then
    CURRENT_TASK_TITLE=$(yq eval ".tasks[] | select(.id == \"$CURRENT_TASK_ID\") | .title" "$PROJECT_ROOT/.autonomous/agents/communications/queue.yaml" 2>/dev/null || echo "")
    ACCEPTANCE_CRITERIA=$(yq eval ".tasks[] | select(.id == \"$CURRENT_TASK_ID\") | .acceptance_criteria // \"Not specified\"" "$PROJECT_ROOT/.autonomous/agents/communications/queue.yaml" 2>/dev/null || echo "Not specified")
fi

# Create run folder with all templates
RUN_DIR=$(initialize_run_folder "$PROJECT_ROOT" "$AGENT_TYPE" "$CURRENT_TASK_ID" "$CURRENT_TASK_TITLE" "$ACCEPTANCE_CRITERIA")
RUN_ID=$(basename "$RUN_DIR")

# Update AGENT_CONTEXT.md with queue status
if [ -f "$PROJECT_ROOT/.autonomous/agents/communications/queue.yaml" ]; then
    ACTIVE_TASKS=$(yq eval '.tasks[] | select(.status == "pending" or .status == "in_progress") | length' "$PROJECT_ROOT/.autonomous/agents/communications/queue.yaml" 2>/dev/null || echo "0")
    COMPLETED_TASKS=$(yq eval '.tasks[] | select(.status == "completed") | length' "$PROJECT_ROOT/.autonomous/agents/communications/queue.yaml" 2>/dev/null || echo "0")

    # Update AGENT_CONTEXT.md with queue status
    sed -i "s/Checking queue status.../- Active Tasks: $ACTIVE_TASKS\n- Completed Tasks: $COMPLETED_TASKS/" "$RUN_DIR/AGENT_CONTEXT.md"
fi

# Load relevant memories (if memory system exists)
MEMORY_LOADED="false"
MEMORY_PATH="$PROJECT_ROOT/.autonomous/memory/hooks/session_memory_loader.py"

if [ -f "$MEMORY_PATH" ] && [ -n "$CURRENT_TASK_ID" ]; then
    # Try to load relevant memories for current task
    if python3 "$MEMORY_PATH" --task "$CURRENT_TASK_ID" --output "$RUN_DIR/RELEVANT_MEMORIES.md" 2>/dev/null; then
        MEMORY_LOADED="true"
    fi
fi

# Build additional context message
ADDITIONAL_CONTEXT=""

# Add memory info if loaded
if [ "$MEMORY_LOADED" == "true" ]; then
    ADDITIONAL_CONTEXT+="\n\n## Memory Loaded\n"
    ADDITIONAL_CONTEXT+="Relevant memories from past work have been loaded into RELEVANT_MEMORIES.md in your run directory.\n"
fi

# Add task context if available
if [ -n "$CURRENT_TASK_ID" ]; then
    ADDITIONAL_CONTEXT+="\n\n## Current Assignment\n"
    ADDITIONAL_CONTEXT+="You are working on task: **$CURRENT_TASK_ID** - $CURRENT_TASK_TITLE\n"
    if [ -n "$ACCEPTANCE_CRITERIA" ] && [ "$ACCEPTANCE_CRITERIA" != "Not specified" ]; then
        ADDITIONAL_CONTEXT+="\nReview the acceptance criteria in AGENT_CONTEXT.md for success criteria.\n"
    fi
fi

# Add environment info
ADDITIONAL_CONTEXT+="\n\n## Environment Setup\n"
ADDITIONAL_CONTEXT+="- Run Directory: $RUN_DIR\n"
ADDITIONAL_CONTEXT+="- Agent Type: $AGENT_TYPE\n"
ADDITIONAL_CONTEXT+="- Session ID: $SESSION_ID\n"
ADDITIONAL_CONTEXT+="- Source: $SOURCE\n"

# Add file structure reminder
ADDITIONAL_CONTEXT+="\n\n## Available Files in Run Directory\n"
ADDITIONAL_CONTEXT+="- **THOUGHTS.md** - Document your reasoning and analysis\n"
ADDITIONAL_CONTEXT+="- **RESULTS.md** - Record what was accomplished\n"
ADDITIONAL_CONTEXT+="- **DECISIONS.md** - Log key decisions with rationale\n"
ADDITIONAL_CONTEXT+="- **ASSUMPTIONS.md** - Document assumptions and validation\n"
ADDITIONAL_CONTEXT+="- **LEARNINGS.md** - Capture lessons learned\n"
ADDITIONAL_CONTEXT+="- **metadata.yaml** - Structured run data\n"
ADDITIONAL_CONTEXT+="- **AGENT_CONTEXT.md** - Your current task and context\n"
if [ "$MEMORY_LOADED" == "true" ]; then
    ADDITIONAL_CONTEXT+="- **RELEVANT_MEMORIES.md** - Memories from similar past work\n"
fi

# Main context message
MAIN_MESSAGE="You are running as a **$AGENT_TYPE** agent in the BlackBox5 system."
MAIN_MESSAGE+="\n\nYour run directory is: \`$RUN_DIR\`"
MAIN_MESSAGE+="\n\nAll required documentation files have been created from templates."
MAIN_MESSAGE+="\n\nReview AGENT_CONTEXT.md for your current task and available commands."
MAIN_MESSAGE+="$ADDITIONAL_CONTEXT"

# Build JSON output
OUTPUT=$(cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": $(echo "$MAIN_MESSAGE" | python3 -c "import json, sys; print(json.dumps(sys.stdin.read()))" 2>/dev/null || echo "\"$MAIN_MESSAGE\""),
    "agentType": "$AGENT_TYPE",
    "runId": "$RUN_ID",
    "runDir": "$RUN_DIR",
    "contextFile": "$RUN_DIR/AGENT_CONTEXT.md",
    "memoryLoaded": $MEMORY_LOADED,
    "taskId": "$CURRENT_TASK_ID",
    "taskTitle": "$CURRENT_TASK_TITLE",
    "projectId": "$PROJECT_NAME",
    "sessionSource": "$SOURCE",
    "sessionId": "$SESSION_ID"
  }
}
EOF
)

echo "$OUTPUT"

# Log session start to events.yaml if available
EVENTS_FILE="$PROJECT_ROOT/.autonomous/agents/communications/events.yaml"
if [ -f "$EVENTS_FILE" ]; then
    TEMP_FILE=$(mktemp)
    yq eval '.events += [{"timestamp": "'$(date -Iseconds)'", "type": "session_start", "agent": "'$AGENT_TYPE'", "run_id": "'$RUN_ID'", "session_id": "'$SESSION_ID'", "task_id": "'$CURRENT_TASK_ID'"}]' "$EVENTS_FILE" > "$TEMP_FILE" && mv "$TEMP_FILE" "$EVENTS_FILE" 2>/dev/null || true
fi
