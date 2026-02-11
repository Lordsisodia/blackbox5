#!/bin/bash
# BB5 CI Service Wrapper
# Manages the CI orchestrator as a system service

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIDFILE="/tmp/bb5-ci-orchestrator.pid"
LOGFILE="/Users/shaansisodia/blackbox5/5-project-memory/blackbox5/.autonomous/ci/logs/orchestrator.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOGFILE")"

start() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        echo "BB5 CI Orchestrator is already running (PID: $(cat "$PIDFILE"))"
        exit 1
    fi

    echo "Starting BB5 CI Orchestrator..."
    nohup python3 -u "$SCRIPT_DIR/ci_orchestrator.py" start >> "$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    echo "Started (PID: $!)"
    echo "Logs: $LOGFILE"
}

stop() {
    if [ ! -f "$PIDFILE" ]; then
        echo "BB5 CI Orchestrator is not running"
        exit 1
    fi

    PID=$(cat "$PIDFILE")
    echo "Stopping BB5 CI Orchestrator (PID: $PID)..."
    kill "$PID" 2>/dev/null
    rm -f "$PIDFILE"
    echo "Stopped"
}

status() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        echo "BB5 CI Orchestrator is running (PID: $(cat "$PIDFILE"))"
        python3 "$SCRIPT_DIR/ci_orchestrator.py" status
    else
        echo "BB5 CI Orchestrator is not running"
        rm -f "$PIDFILE"
    fi
}

trigger() {
    TARGET="${1:-logs}"
    echo "Triggering error detection for: $TARGET"
    python3 "$SCRIPT_DIR/ci_orchestrator.py" trigger --target "$TARGET"
}

case "${1:-}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    status)
        status
        ;;
    trigger)
        trigger "${2:-logs}"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|trigger [target]}"
        exit 1
        ;;
esac
