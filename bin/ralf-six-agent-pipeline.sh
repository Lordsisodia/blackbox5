#!/bin/bash
#
# 6-Agent RALF Pipeline Orchestrator
# 3 Workers + 3 Validators for intelligent GitHub repo analysis
#

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="${RALF_BASE_DIR:-$HOME/.blackbox5}"
PROJECT_DIR="$BASE_DIR/5-project-memory/blackbox5"
AGENTS_DIR="$PROJECT_DIR/.autonomous/agents"
COMM_DIR="$AGENTS_DIR/communications"
LOG_FILE="$PROJECT_DIR/.autonomous/six-agent-pipeline.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${BLUE}[PIPELINE]${NC} $*" | tee -a "$LOG_FILE"; }
success() { echo -e "${GREEN}[OK]${NC} $*" | tee -a "$LOG_FILE"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*" | tee -a "$LOG_FILE"; }
error() { echo -e "${RED}[ERROR]${NC} $*" | tee -a "$LOG_FILE"; }

# Initialize queue files
init_queues() {
    log "Initializing queue system..."

    mkdir -p "$COMM_DIR"
    mkdir -p "$AGENTS_DIR"/scout-{worker,validator}
    mkdir -p "$AGENTS_DIR"/analyzer-{worker,validator}
    mkdir -p "$AGENTS_DIR"/planner-{worker,validator}
    mkdir -p "$PROJECT_DIR/.autonomous/research-pipeline"/{knowledge,assessments,plans,tasks/ready}

    # Scout Queue
    cat > "$COMM_DIR/scout-queue.yaml" << 'EOF'
queue: []
metadata:
  initialized: "2026-02-04"
  status: waiting_for_repos
EOF

    # Analyzer Queue
    cat > "$COMM_DIR/analyzer-queue.yaml" << 'EOF'
queue: []
metadata:
  initialized: "2026-02-04"
  status: waiting_for_knowledge
EOF

    # Planner Queue
    cat > "$COMM_DIR/planner-queue.yaml" << 'EOF'
queue: []
metadata:
  initialized: "2026-02-04"
  status: waiting_for_assessments
EOF

    # Executor Queue
    cat > "$COMM_DIR/executor-queue.yaml" << 'EOF'
queue: []
metadata:
  initialized: "2026-02-04"
  status: waiting_for_plans
EOF

    # Heartbeat
    cat > "$COMM_DIR/heartbeat.yaml" << 'EOF'
heartbeats:
  scout-worker:
    status: idle
    last_seen: null
  scout-validator:
    status: idle
    last_seen: null
  analyzer-worker:
    status: idle
    last_seen: null
  analyzer-validator:
    status: idle
    last_seen: null
  planner-worker:
    status: idle
    last_seen: null
  planner-validator:
    status: idle
    last_seen: null
EOF

    success "Queue system initialized"
}

# Load repos from repo-list into scout queue
load_repos() {
    log "Loading repos from repo-list.yaml..."

    REPO_LIST="$BASE_DIR/6-roadmap/.research/external/GitHub/repo-list.yaml"

    if [[ ! -f "$REPO_LIST" ]]; then
        error "Repo list not found: $REPO_LIST"
        exit 1
    fi

    # Parse repo-list.yaml and add to scout queue
    python3 << PYEOF
import yaml
import sys
from datetime import datetime, timezone

repo_list_path = "$REPO_LIST"
queue_path = "$COMM_DIR/scout-queue.yaml"

try:
    with open(repo_list_path, 'r') as f:
        repo_data = yaml.safe_load(f)

    repos = repo_data.get('repositories', [])

    queue_items = []
    for repo in repos:
        queue_items.append({
            'repo_url': repo.get('url'),
            'repo_name': repo.get('name'),
            'status': 'pending',
            'assigned_worker': None,
            'knowledge_doc': None,
            'validation_status': 'pending',
            'added_at': datetime.now(timezone.utc).isoformat()
        })

    with open(queue_path, 'r') as f:
        queue_data = yaml.safe_load(f) or {}

    queue_data['queue'] = queue_items
    queue_data['metadata']['status'] = 'ready'
    queue_data['metadata']['total_repos'] = len(queue_items)
    queue_data['metadata']['loaded_at'] = datetime.now(timezone.utc).isoformat()

    with open(queue_path, 'w') as f:
        yaml.dump(queue_data, f, default_flow_style=False)

    print(f"Loaded {len(queue_items)} repos into scout queue")

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
PYEOF

    success "Repos loaded into scout queue"
}

# Start an agent in tmux
start_agent() {
    local agent_name="$1"
    local prompt_file="$2"
    local queue_file="$3"

    log "Starting $agent_name..."

    # Create agent run directory
    AGENT_RUN_DIR="$AGENTS_DIR/$agent_name/runs/run-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$AGENT_RUN_DIR"

    # Create tmux session
    tmux new-session -d -s "$agent_name" -n main "cd $BASE_DIR && export RALF_RUN_DIR=$AGENT_RUN_DIR && export RALF_AGENT_TYPE=$agent_name && cat $prompt_file | claude -p --dangerously-skip-permissions 2>&1 | tee -a $AGENT_RUN_DIR/agent.log" 2>/dev/null || {
        warn "Tmux session $agent_name already exists or failed to create"
        return 1
    }

    success "$agent_name started in tmux session"
}

# Main execution
main() {
    log "════════════════════════════════════════════════════════════"
    log "  6-Agent RALF Pipeline"
    log "  3 Workers + 3 Validators"
    log "════════════════════════════════════════════════════════════"
    log ""

    # Initialize
    init_queues
    load_repos

    log ""
    log "Starting agents..."
    log ""

    # Start all 6 agents
    # Stage 1: Scout
    start_agent "scout-worker" "$BASE_DIR/2-engine/.autonomous/prompts/agents/deep-repo-scout.md" "$COMM_DIR/scout-queue.yaml"
    sleep 2
    start_agent "scout-validator" "$BASE_DIR/2-engine/.autonomous/prompts/agents/scout-validator.md" "$COMM_DIR/scout-queue.yaml"
    sleep 2

    # Stage 2: Analyzer
    start_agent "analyzer-worker" "$BASE_DIR/2-engine/.autonomous/prompts/agents/integration-analyzer.md" "$COMM_DIR/analyzer-queue.yaml"
    sleep 2
    start_agent "analyzer-validator" "$BASE_DIR/2-engine/.autonomous/prompts/agents/analyzer-validator.md" "$COMM_DIR/analyzer-queue.yaml"
    sleep 2

    # Stage 3: Planner
    start_agent "planner-worker" "$BASE_DIR/2-engine/.autonomous/prompts/agents/implementation-planner.md" "$COMM_DIR/planner-queue.yaml"
    sleep 2
    start_agent "planner-validator" "$BASE_DIR/2-engine/.autonomous/prompts/agents/planner-validator.md" "$COMM_DIR/planner-queue.yaml"

    log ""
    success "All 6 agents started"
    log ""
    log "Monitor with:"
    log "  tmux ls"
    log "  tail -f $LOG_FILE"
    log ""
    log "View agent logs:"
    log "  ls $AGENTS_DIR/*/runs/"
    log ""
}

# Show status
status() {
    log "Pipeline Status:"
    log ""

    # Check tmux sessions
    log "Active tmux sessions:"
    tmux ls 2>/dev/null || log "  No active sessions"
    log ""

    # Check queue depths
    log "Queue depths:"
    for queue in scout analyzer planner executor; do
        count=$(python3 -c "import yaml; print(len(yaml.safe_load(open('$COMM_DIR/${queue}-queue.yaml'))['queue']))" 2>/dev/null || echo "0")
        log "  $queue-queue: $count items"
    done
    log ""

    # Check outputs
    log "Output counts:"
    log "  Knowledge docs: $(ls $PROJECT_DIR/.autonomous/research-pipeline/knowledge/*.md 2>/dev/null | wc -l)"
    log "  Assessments: $(ls $PROJECT_DIR/.autonomous/research-pipeline/assessments/*.md 2>/dev/null | wc -l)"
    log "  Plans: $(ls $PROJECT_DIR/.autonomous/research-pipeline/plans/*.md 2>/dev/null | wc -l)"
    log "  Ready tasks: $(ls $PROJECT_DIR/.autonomous/research-pipeline/tasks/ready/TASK-*.md 2>/dev/null | wc -l)"
}

# Stop all agents
stop() {
    log "Stopping all agents..."

    for agent in scout-worker scout-validator analyzer-worker analyzer-validator planner-worker planner-validator; do
        tmux kill-session -t "$agent" 2>/dev/null && log "  Stopped $agent" || true
    done

    pkill -f "claude.*6-agent" 2>/dev/null || true

    success "All agents stopped"
}

# Command dispatch
case "${1:-start}" in
    start)
        main
        ;;
    status)
        status
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 2
        main
        ;;
    *)
        echo "Usage: $0 {start|status|stop|restart}"
        exit 1
        ;;
esac
