#!/bin/bash
# Launch Analyst Pair (Worker + Validator)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
ENGINE_DIR="$(cd "$SCRIPT_DIR/../../../2-engine/.autonomous" && pwd)"

echo "================================"
echo "Launching Analyst Pair"
echo "================================"
echo ""

mkdir -p "$SCRIPT_DIR/logs/analyst"

echo "[1/2] Starting Analyst Worker..."
export RALF_PROJECT_DIR="$PROJECT_DIR"
export RALF_ENGINE_DIR="$ENGINE_DIR"
export RALF_AGENT_TYPE="analyst-worker"
export RALF_PROMPT_FILE="$PROJECT_DIR/.templates/prompts/analyst-worker.md"

"$ENGINE_DIR/shell/ralf-loop.sh" \
  --project "$PROJECT_DIR" \
  --prompt "$RALF_PROMPT_FILE" \
  --agent-type analyst-worker \
  > "$SCRIPT_DIR/logs/analyst/worker.log" 2>&1 &

WORKER_PID=$!
echo "        PID: $WORKER_PID"

echo ""
echo "[2/2] Starting Analyst Validator..."
export RALF_AGENT_TYPE="analyst-validator"
export RALF_PROMPT_FILE="$PROJECT_DIR/.templates/prompts/analyst-validator.md"

"$ENGINE_DIR/shell/ralf-loop.sh" \
  --project "$PROJECT_DIR" \
  --prompt "$RALF_PROMPT_FILE" \
  --agent-type analyst-validator \
  > "$SCRIPT_DIR/logs/analyst/validator.log" 2>&1 &

VALIDATOR_PID=$!
echo "        PID: $VALIDATOR_PID"

echo ""
echo "================================"
echo "Analyst Pair Launched!"
echo "================================"
echo ""
echo "Worker PID:    $WORKER_PID"
echo "Validator PID: $VALIDATOR_PID"
echo ""

cat > "$SCRIPT_DIR/.analyst-pids" << EOF
WORKER_PID=$WORKER_PID
VALIDATOR_PID=$VALIDATOR_PID
EOF
