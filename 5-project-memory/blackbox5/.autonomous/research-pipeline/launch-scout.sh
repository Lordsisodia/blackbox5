#!/bin/bash
# Launch Scout Pair (Worker + Validator)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
ENGINE_DIR="$(cd "$SCRIPT_DIR/../../../2-engine/.autonomous" && pwd)"

echo "================================"
echo "Launching Scout Pair"
echo "================================"
echo ""

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs/scout"

echo "[1/2] Starting Scout Worker..."
export RALF_PROJECT_DIR="$PROJECT_DIR"
export RALF_ENGINE_DIR="$ENGINE_DIR"
export RALF_AGENT_TYPE="scout-worker"
export RALF_PROMPT_FILE="$PROJECT_DIR/.templates/prompts/scout-worker.md"

"$ENGINE_DIR/shell/ralf-loop.sh" \
  --project "$PROJECT_DIR" \
  --prompt "$RALF_PROMPT_FILE" \
  --agent-type scout-worker \
  > "$SCRIPT_DIR/logs/scout/worker.log" 2>&1 &

WORKER_PID=$!
echo "        PID: $WORKER_PID"
echo "        Log: logs/scout/worker.log"

echo ""
echo "[2/2] Starting Scout Validator..."
export RALF_AGENT_TYPE="scout-validator"
export RALF_PROMPT_FILE="$PROJECT_DIR/.templates/prompts/scout-validator.md"

"$ENGINE_DIR/shell/ralf-loop.sh" \
  --project "$PROJECT_DIR" \
  --prompt "$RALF_PROMPT_FILE" \
  --agent-type scout-validator \
  > "$SCRIPT_DIR/logs/scout/validator.log" 2>&1 &

VALIDATOR_PID=$!
echo "        PID: $VALIDATOR_PID"
echo "        Log: logs/scout/validator.log"

echo ""
echo "================================"
echo "Scout Pair Launched!"
echo "================================"
echo ""
echo "Worker PID:   $WORKER_PID"
echo "Validator PID: $VALIDATOR_PID"
echo ""
echo "To stop:  kill $WORKER_PID $VALIDATOR_PID"
echo "To check: cat communications/heartbeat.yaml"
echo ""

# Save PIDs
cat > "$SCRIPT_DIR/.scout-pids" << EOF
WORKER_PID=$WORKER_PID
VALIDATOR_PID=$VALIDATOR_PID
EOF
