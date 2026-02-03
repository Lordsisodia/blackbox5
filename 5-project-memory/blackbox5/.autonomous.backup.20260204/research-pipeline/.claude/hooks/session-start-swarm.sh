#!/bin/bash
# SessionStart Hook - Inject Swarm Memory for Agent Coordination
# VERSION: 1.0.0
# Purpose: Load swarm-level, pipeline-level, and agent-specific memory
#
# This hook provides THREE layers of memory:
# 1. Swarm Context (Global coordination)
# 2. Pipeline Context (Phase coordination)
# 3. Agent Context (Individual memory)

set -euo pipefail

readonly VERSION="1.0.0"

# Read input from stdin (JSON)
INPUT=$(head -c 100000)

# Parse session info
SOURCE=$(echo "$INPUT" | jq -r '.source // "startup"' 2>/dev/null || echo "startup")
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")

# Detect agent type
detect_agent() {
    if [[ -n "${RALF_AGENT_TYPE:-}" ]]; then
        echo "$RALF_AGENT_TYPE"
        return 0
    fi

    if [[ -n "${RALF_PROMPT_FILE:-}" ]]; then
        case "$RALF_PROMPT_FILE" in
            *scout-worker*) echo "scout-worker" ;;
            *scout-validator*) echo "scout-validator" ;;
            *analyst-worker*) echo "analyst-worker" ;;
            *analyst-validator*) echo "analyst-validator" ;;
            *planner-worker*) echo "planner-worker" ;;
            *planner-validator*) echo "planner-validator" ;;
            *) echo "unknown" ;;
        esac
        return 0
    fi

    echo "unknown"
}

# Get project directory
get_project_dir() {
    echo "${RALF_PROJECT_DIR:-$(pwd)}"
}

# Read swarm context
get_swarm_context() {
    local project_dir="$1"
    local swarm_dir="$project_dir/.autonomous/research-pipeline/swarm"

    local context=""
    context+="## Layer 1: Swarm Context (Global Coordination)\n\n"

    # Read heartbeat
    if [[ -f "$swarm_dir/heartbeat.yaml" ]]; then
        context+="### Swarm Health Status\n"
        context+="\`\`\`yaml\n"
        context+=$(cat "$swarm_dir/heartbeat.yaml" 2>/dev/null | head -50)
        context+="\n\`\`\`\n\n"
    fi

    # Read state
    if [[ -f "$swarm_dir/state.yaml" ]]; then
        context+="### Pipeline State\n"
        context+="\`\`\`yaml\n"
        context+=$(cat "$swarm_dir/state.yaml" 2>/dev/null | grep -A 20 "pipeline_state:")
        context+="\n\`\`\`\n\n"
    fi

    echo "$context"
}

# Read pipeline context
get_pipeline_context() {
    local project_dir="$1"
    local agent="$2"
    local comms_dir="$project_dir/.autonomous/research-pipeline/communications"

    local context=""
    context+="## Layer 2: Pipeline Context (Phase Coordination)\n\n"

    # Determine which phase this agent belongs to
    local phase=""
    case "$agent" in
        scout-*)
            phase="scout"
            ;;
        analyst-*)
            phase="analyst"
            ;;
        planner-*)
            phase="planner"
            ;;
    esac

    if [[ -n "$phase" && -f "$comms_dir/${phase}-state.yaml" ]]; then
        context+="### $phase Phase State\n"
        context+="\`\`\`yaml\n"
        context+=$(cat "$comms_dir/${phase}-state.yaml" 2>/dev/null | head -30)
        context+="\n\`\`\`\n\n"
    fi

    # Recent events
    if [[ -f "$comms_dir/events.yaml" ]]; then
        context+="### Recent Events\n"
        context+="\`\`\`yaml\n"
        context+=$(cat "$comms_dir/events.yaml" 2>/dev/null | tail -50)
        context+="\n\`\`\`\n\n"
    fi

    echo "$context"
}

# Read agent context
get_agent_context() {
    local project_dir="$1"
    local agent="$2"
    local agent_dir="$project_dir/.autonomous/research-pipeline/agents/$agent"

    local context=""
    context+="## Layer 3: Agent Context (Individual Memory)\n\n"
    context+="### Agent Identity\n"
    context+="You are the **$agent** in the Dual-RALF Research Pipeline.\n"
    context+="Session: $SESSION_ID | Source: $SOURCE\n\n"

    # Timeline memory
    if [[ -f "$agent_dir/timeline-memory.md" ]]; then
        context+="### Timeline Memory (Long-Term)\n"
        context+=$(cat "$agent_dir/timeline-memory.md" 2>/dev/null)
        context+="\n\n"
    else
        context+="⚠️ Timeline memory not found at: $agent_dir/timeline-memory.md\n\n"
    fi

    # Running memory
    if [[ -f "$agent_dir/running-memory.md" ]]; then
        context+="### Running Memory (Current Session)\n"
        context+=$(cat "$agent_dir/running-memory.md" 2>/dev/null)
        context+="\n\n"
    fi

    echo "$context"
}

# Get work instructions
get_work_instructions() {
    local agent="$1"

    echo "### Work Assignment Instructions\n\n"

    case "$agent" in
        "scout-worker")
            echo "**Your Role:** Extract patterns from external sources\n"
            echo "**Work Flow:**"
            echo "1. Check timeline-memory.md work_queue.priority_sources"
            echo "2. If empty, check swarm/events.yaml for source.added events"
            echo "3. Select ONE source (never batch)"
            echo "4. Update work_queue.in_progress in timeline"
            echo "5. Extract patterns → data/patterns/"
            echo "6. Publish pattern.extracted event to swarm/events.yaml"
            echo "7. Update timeline-memory.md with results"
            ;;
        "scout-validator")
            echo "**Your Role:** Validate scout extractions\n"
            echo "**Work Flow:**"
            echo "1. Check swarm/heartbeat.yaml for scout-worker status"
            echo "2. Read scout-worker's latest run from agents/scout-worker/runs/"
            echo "3. Validate extraction quality"
            echo "4. Write feedback to communications/chat-log.yaml"
            echo "5. Update timeline-memory.md with validation results"
            ;;
        "analyst-worker")
            echo "**Your Role:** Analyze pattern value to BB5\n"
            echo "**Work Flow:**"
            echo "1. Check timeline-memory.md work_queue.priority_patterns"
            echo "2. If empty, check swarm/events.yaml for pattern.extracted events"
            echo "3. Find patterns in data/patterns/ without analysis"
            echo "4. Select ONE pattern (never batch)"
            echo "5. Analyze → data/analysis/"
            echo "6. Publish analysis.complete event to swarm/events.yaml"
            echo "7. Update timeline-memory.md with results"
            ;;
        "analyst-validator")
            echo "**Your Role:** Validate analysis scoring\n"
            echo "**Work Flow:**"
            echo "1. Check swarm/heartbeat.yaml for analyst-worker status"
            echo "2. Read analyst-worker's analysis from data/analysis/"
            echo "3. Validate scoring accuracy"
            echo "4. Write feedback to communications/chat-log.yaml"
            echo "5. Update timeline-memory.md with validation results"
            ;;
        "planner-worker")
            echo "**Your Role:** Create BB5 tasks from recommendations\n"
            echo "**Work Flow:**"
            echo "1. Check timeline-memory.md work_queue.priority_recommendations"
            echo "2. If empty, check swarm/events.yaml for analysis.complete events"
            echo "3. Find recommendations (decision: recommend) in data/analysis/"
            echo "4. Select ONE recommendation (never batch)"
            echo "5. Create BB5 task → tasks/active/"
            echo "6. Add to communications/queue.yaml"
            echo "7. Publish task.created event to swarm/events.yaml"
            echo "8. Update timeline-memory.md with results"
            ;;
        "planner-validator")
            echo "**Your Role:** Validate task planning quality\n"
            echo "**Work Flow:**"
            echo "1. Check swarm/heartbeat.yaml for planner-worker status"
            echo "2. Read planner-worker's task from communications/queue.yaml"
            echo "3. Validate plan quality (subtasks, estimates, dependencies)"
            echo "4. Write feedback to communications/chat-log.yaml"
            echo "5. Update timeline-memory.md with validation results"
            ;;
        *)
            echo "**Work Assignment:** Unknown agent type: $agent"
            echo "Please set RALF_AGENT_TYPE environment variable."
            ;;
    esac

    echo ""
}

# Main execution
main() {
    local agent=$(detect_agent)

    if [[ "$agent" == "unknown" ]]; then
        echo '{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ""}}'
        exit 0
    fi

    local project_dir=$(get_project_dir)

    # Build three-layer context
    local swarm_context=$(get_swarm_context "$project_dir")
    local pipeline_context=$(get_pipeline_context "$project_dir" "$agent")
    local agent_context=$(get_agent_context "$project_dir" "$agent")
    local work_instructions=$(get_work_instructions "$agent")

    # Combine all layers
    local full_context="$swarm_context\n$pipeline_context\n$agent_context\n$work_instructions"

    # Escape for JSON
    local escaped_context=$(python3 -c "
import json
import sys
content = sys.stdin.read()
print(json.dumps(content))
" <<< "$full_context")

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
