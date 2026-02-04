#!/bin/bash
# GitHub Analysis Pipeline - 3-Agent RALF System
# Runs Scout → Analyzer → Planner in sequence, looping for 8 hours

set -e

PROJECT_ROOT="/opt/ralf"
AGENTS_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents"
LOG_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/logs"
PID_FILE="/tmp/github-analysis-pipeline.pid"
RUNTIME_HOURS=8
START_TIME=$(date +%s)
END_TIME=$((START_TIME + RUNTIME_HOURS * 3600))

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/pipeline.log"
}

cleanup() {
    log "Pipeline shutting down..."
    rm -f "$PID_FILE"
    exit 0
}

trap cleanup SIGTERM SIGINT

write_pid() {
    echo $$ > "$PID_FILE"
}

run_agent() {
    local agent="$1"
    local script="$AGENTS_DIR/$agent/${agent}-agent.sh"

    if [ ! -f "$script" ]; then
        log "ERROR: Agent script not found: $script"
        return 1
    fi

    log "Starting $agent agent..."
    chmod +x "$script"

    if bash "$script" >> "$LOG_DIR/${agent}.log" 2>&1; then
        log "$agent agent completed successfully"
        return 0
    else
        log "ERROR: $agent agent failed"
        return 1
    fi
}

run_pipeline_cycle() {
    log "=== Starting Pipeline Cycle ==="
    local cycle_start=$(date +%s)

    # Step 1: Scout - Extract repo data
    if ! run_agent "scout"; then
        log "WARNING: Scout had issues, continuing..."
    fi

    # Step 2: Analyzer - Process extractions
    if ! run_agent "analyzer"; then
        log "WARNING: Analyzer had issues, continuing..."
    fi

    # Step 3: Planner - Create integration plans
    if ! run_agent "planner"; then
        log "WARNING: Planner had issues, continuing..."
    fi

    local cycle_end=$(date +%s)
    local cycle_duration=$((cycle_end - cycle_start))
    log "=== Pipeline Cycle Complete (${cycle_duration}s) ==="
}

main() {
    write_pid
    log "GitHub Analysis Pipeline Starting"
    log "Runtime: $RUNTIME_HOURS hours (until $(date -d @$END_TIME '+%H:%M:%S'))"
    log "Project Root: $PROJECT_ROOT"

    local cycle=0
    while [ $(date +%s) -lt $END_TIME ]; do
        cycle=$((cycle + 1))
        log "--- Cycle $cycle ---"
        run_pipeline_cycle

        # Check if we should continue
        local remaining=$((END_TIME - $(date +%s)))
        if [ $remaining -le 0 ]; then
            log "Runtime limit reached"
            break
        fi

        log "Next cycle in 60 seconds ($((remaining / 60)) minutes remaining)"
        sleep 60
    done

    log "Pipeline completed after $cycle cycles"
    log "Results available in:"
    log "  - Extractions: $AGENTS_DIR/scout/extractions/"
    log "  - Summaries: $AGENTS_DIR/analyzer/summaries/"
    log "  - Plans: $AGENTS_DIR/planner/integration-plans/"
    log "  - Logs: $LOG_DIR/"

    cleanup
}

main "$@"
