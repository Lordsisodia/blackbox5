#!/bin/bash
# Task Agent Service Manager

ACTION="$1"
PIDFILE="/var/run/task-agent-bridge.pid"
LOGFILE="/var/log/task-agent-bridge.log"

case "$ACTION" in
  start)
    if [ -f "$PIDFILE" ] && kill -0 "$(cat $PIDFILE)" 2>/dev/null; then
      echo "Task Agent Bridge is already running (PID: $(cat $PIDFILE))"
      exit 0
    fi
    cd /opt/moltbot/agents/task-agent
    nohup node enhanced-bridge.js >> "$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    echo "Task Agent Bridge started (PID: $!)"
    ;;
  stop)
    if [ -f "$PIDFILE" ]; then
      PID=$(cat "$PIDFILE")
      kill "$PID" 2>/dev/null && echo "Task Agent Bridge stopped (PID: $PID)" || echo "Process not running"
      rm -f "$PIDFILE"
    else
      echo "No PID file found, killing all node processes..."
      pkill -f enhanced-bridge.js
    fi
    ;;
  restart)
    $0 stop
    sleep 2
    $0 start
    ;;
  status)
    if [ -f "$PIDFILE" ] && kill -0 "$(cat $PIDFILE)" 2>/dev/null; then
      echo "Task Agent Bridge is running (PID: $(cat $PIDFILE))"
      ps aux | grep "$(cat $PIDFILE)" | grep -v grep
    else
      echo "Task Agent Bridge is not running"
    fi
    ;;
  logs)
    tail -f "$LOGFILE"
    ;;
  test)
    echo "Testing Supabase connection..."
    source /opt/moltbot/agents/task-agent/.env
    curl -s "${SUPABASE_URL}/rest/v1/deep_work_tasks?select=count&user_id=eq.a95135f0-1970-474a-850c-d280fc6ca217" \
      -H "apikey: ${SUPABASE_ANON_KEY}" \
      -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
    echo ""
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status|logs|test}"
    exit 1
    ;;
esac
