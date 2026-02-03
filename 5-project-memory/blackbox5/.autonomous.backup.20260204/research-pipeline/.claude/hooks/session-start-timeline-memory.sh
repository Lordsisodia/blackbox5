#!/bin/bash
# SessionStart Hook - Inject Timeline Memory for Research Pipeline Agents
# VERSION: 1.0.0
# Purpose: Load agent-specific timeline memory into context at session start
#
# This hook detects which agent is running and injects their timeline memory

set -euo pipefail

readonly VERSION="1.0.0"

# Read input from stdin (JSON)
INPUT=$(head -c 100000)

# Parse session info
SOURCE=$(echo "$INPUT" | jq -r '.source // "startup"' 2>/dev/null || echo "startup")
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")

# Detect which agent is running based on environment variables
detect_agent() {
    # Check RALF_AGENT_TYPE first
    if [[ -n "${RALF_AGENT_TYPE:-}" ]]; then
        echo "$RALF_AGENT_TYPE"
        return 0
    fi

    # Check prompt file path for agent type
    if [[ -n "${RALF_PROMPT_FILE:-}" ]]; then
        if [[ "$RALF_PROMPT_FILE" == *"scout-worker"* ]]; then
            echo "scout-worker"
        elif [[ "$RALF_PROMPT_FILE" == *"scout-validator"* ]]; then
            echo "scout-validator"
        elif [[ "$RALF_PROMPT_FILE" == *"analyst-worker"* ]]; then
            echo "analyst-worker"
        elif [[ "$RALF_PROMPT_FILE" == *"analyst-validator"* ]]; then
            echo "analyst-validator"
        elif [[ "$RALF_PROMPT_FILE" == *"planner-worker"* ]]; then
            echo "planner-worker"
        elif [[ "$RALF_PROMPT_FILE" == *"planner-validator"* ]]; then
            echo "planner-validator"
        else
            echo "unknown"
        fi
        return 0
    fi

    echo "unknown"
}

# Get timeline memory path for agent
get_timeline_path() {
    local agent="$1"
    local project_dir="${RALF_PROJECT_DIR:-$(pwd)}"

    echo "$project_dir/.autonomous/research-pipeline/agents/$agent/timeline-memory.md"
}

# Build context block from timeline memory
build_context_block() {
    local agent="$1"
    local timeline_path="$2"

    local context=""

    # Add agent identification
    context+="## Agent Identity\n"
    context+="You are the **$agent** in the Dual-RALF Research Pipeline.\n"
    context+="Session: $SESSION_ID | Source: $SOURCE\n\n"

    # Add timeline memory if it exists
    if [[ -f "$timeline_path" ]]; then
        context+="## Your Timeline Memory (Long-Term Context)\n\n"
        context+=$(cat "$timeline_path" 2>/dev/null || echo "Error reading timeline memory")
        context+="\n\n"
    else
        context+="## ⚠️ Timeline Memory Not Found\n"
        context+="Expected at: $timeline_path\n"
        context+="This is your first run or the file needs to be created.\n\n"
    fi

    # Add work assignment instructions
    context+="## Work Assignment Instructions\n\n"
    context+=$(get_work_instructions "$agent")
    context+="\n\n"

    echo "$context"
}

# Get work assignment instructions for each agent type
get_work_instructions() {
    local agent="$1"

    case "$agent" in
        "scout-worker")
            echo "**How you know what to do:**
1. Check your timeline-memory.md work_queue.priority_sources
2. If empty, check communications/scout-state.yaml for shared queue
3. Select ONE source (never batch)
4. Update work_queue.in_progress in your timeline
5. Extract patterns from the source
6. Save patterns to data/patterns/
7. Publish event to communications/events.yaml
8. Update your timeline-memory.md with results"
            ;;
        "scout-validator")
            echo "**How you know what to validate:**
1. Check scout-worker's timeline-memory.md for their current work
2. Read their THOUGHTS.md and RESULTS.md from their run directory
3. Validate extraction quality
4. Write feedback to communications/chat-log.yaml
5. Update your timeline-memory.md with observations"
            ;;
        "analyst-worker")
            echo "**How you know what to analyze:**
1. Check your timeline-memory.md work_queue.priority_patterns
2. If empty, check communications/events.yaml for pattern.extracted events
3. Find patterns in data/patterns/ without matching analysis in data/analysis/
4. Select ONE pattern (never batch)
5. Analyze value and complexity
6. Save analysis to data/analysis/
7. Publish event to communications/events.yaml
8. Update your timeline-memory.md with results"
            ;;
        "analyst-validator")
            echo "**How you know what to validate:**
1. Check analyst-worker's timeline-memory.md for their current analysis
2. Read their analysis from data/analysis/
3. Validate scoring accuracy against your model_accuracy history
4. Write feedback to communications/chat-log.yaml
5. Update your timeline-memory.md with validation results"
            ;;
        "planner-worker")
            echo "**How you know what to plan:**
1. Check your timeline-memory.md work_queue.priority_recommendations
2. If empty, check communications/events.yaml for analysis.complete with decision: recommend
3. Find recommendations in data/analysis/ not yet in communications/queue.yaml
4. Select ONE recommendation (never batch)
5. Create BB5 task package
6. Add to communications/queue.yaml
7. Update your timeline-memory.md with plan details"
            ;;
        "planner-validator")
            echo "**How you know what to validate:**
1. Check planner-worker's timeline-memory.md for their current plan
2. Read their task from communications/queue.yaml
3. Validate plan quality against your plan_quality benchmarks
4. Write feedback to communications/chat-log.yaml
5. Update your timeline-memory.md with validation results"
            ;;
        *)
            echo "**Work Assignment:** Could not determine agent type. Check RALF_AGENT_TYPE environment variable."
            ;;
    esac
}

# Main execution
main() {
    local agent=$(detect_agent)

    if [[ "$agent" == "unknown" ]]; then
        # Not a research pipeline agent, exit silently
        echo '{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ""}}'
        exit 0
    fi

    local timeline_path=$(get_timeline_path "$agent")
    local context_block=$(build_context_block "$agent" "$timeline_path")

    # Escape for JSON
    local escaped_context=$(python3 -c "
import json
import sys
content = sys.stdin.read()
print(json.dumps(content))
" <<< "$context_block")

    # Output JSON
    cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": $escaped_context
  }
}
EOF
}

main
