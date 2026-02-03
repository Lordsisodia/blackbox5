#!/bin/bash
# Launch Planner Pair (Worker + Validator)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
ENGINE_DIR="$(cd "$SCRIPT_DIR/../../../2-engine/.autonomous" && pwd)"

echo "================================"
echo "Launching Planner Pair"
echo "================================"
echo ""

mkdir -p "$SCRIPT_DIR/logs/planner"

echo "[1/2] Starting Planner Worker..."
export RALF_PROJECT_DIR="$PROJECT_DIR"
export RALF_ENGINE_DIR="$ENGINE_DIR"
export RALF_AGENT_TYPE="planner-worker"
export RALF_PROMPT_FILE="$PROJECT_DIR/.templates/prompts/planner-worker.md"

"$ENGINE_DIR/shell/ralf-loop.sh" \
  --project "$PROJECT_DIR" \
  --prompt "$RALF_PROMPT_FILE" \
  --agent-type planner-worker \
  > "$SCRIPT_DIR/logs/planner/worker.log" 2>&1 &

WORKER_PID=$!
echo "        PID: $WORKER_PID"

echo ""
echo "[2/2] Starting Planner Validator..."
export RALF_AGENT_TYPE="planner-validator"
export RALF_PROMPT_FILE="$PROJECT_DIR/.templates/prompts/planner-validator.md"

"$ENGINE_DIR/shell/ralf-loop.sh" \
  --project "$PROJECT_DIR" \
  --prompt "$RALF_PROMPT_FILE" \
  --agent-type planner-validator \
  > "$SCRIPT_DIR/logs/planner/validator.log" 2>&1 &

VALIDATOR_PID=$!
echo "        PID: $VALIDATOR_PID"

echo ""
echo "================================"
echo "Planner Pair Launched!"
echo "================================"
echo ""
echo "Worker PID:    $WORKER_PID"
echo "Validator PID: $VALIDATOR_PID"
echo ""

cat > "$SCRIPT_DIR/.planner-pids" << EOF
WORKER_PID=$WORKER_PID
VALIDATOR_PID=$VALIDATOR_PID
EOF
