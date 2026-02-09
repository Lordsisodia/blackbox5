#!/bin/bash
# Monitor VPS BlackBox5 agent status

VPS_IP="77.42.66.40"
VPS_USER="root"
SSH_KEY="$HOME/.ssh/ralf_hetzner"
LOG_FILE="$HOME/.blackbox5/.logs/vps-monitor.log"
ALERT_FILE="$HOME/.blackbox5/.logs/vps-alerts.log"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

alert() {
    echo "[$(date -Iseconds)] ALERT: $1" | tee -a "$ALERT_FILE"
}

# Check if VPS is reachable
if ! ssh -i "$SSH_KEY" -o ConnectTimeout=5 "$VPS_USER@$VPS_IP" "echo 'ping'" > /dev/null 2>&1; then
    alert "VPS is not reachable!"
    exit 1
fi

# Check if agent service is running
SERVICE_STATUS=$(ssh -i "$SSH_KEY" "$VPS_USER@$VPS_IP" "systemctl is-active blackbox5-agent" 2>/dev/null || echo "unknown")

if [ "$SERVICE_STATUS" != "active" ]; then
    alert "BlackBox5 agent is not running (status: $SERVICE_STATUS)"

    # Try to restart
    log "Attempting to restart agent..."
    ssh -i "$SSH_KEY" "$VPS_USER@$VPS_IP" "systemctl restart blackbox5-agent" 2>/dev/null || true

    sleep 5

    # Check again
    NEW_STATUS=$(ssh -i "$SSH_KEY" "$VPS_USER@$VPS_IP" "systemctl is-active blackbox5-agent" 2>/dev/null || echo "unknown")
    if [ "$NEW_STATUS" = "active" ]; then
        log "Agent restarted successfully"
    else
        alert "Failed to restart agent (status: $NEW_STATUS)"
    fi
else
    log "Agent is running normally"
fi

# Get latest run info
LATEST_RUN=$(ssh -i "$SSH_KEY" "$VPS_USER@$VPS_IP" "ls -1t /opt/blackbox5/5-project-memory/blackbox5/.autonomous/runs/ 2>/dev/null | head -1" || echo "none")
if [ "$LATEST_RUN" != "none" ]; then
    RUN_STATUS=$(ssh -i "$SSH_KEY" "$VPS_USER@$VPS_IP" "cat /opt/blackbox5/5-project-memory/blackbox5/.autonomous/runs/$LATEST_RUN/status.txt 2>/dev/null || echo 'unknown'")
    log "Latest run: $LATEST_RUN (status: $RUN_STATUS)"
fi

# Check disk space
DISK_USAGE=$(ssh -i "$SSH_KEY" "$VPS_USER@$VPS_IP" "df -h / | tail -1 | awk '{print \$5}' | sed 's/%//'" 2>/dev/null || echo "0")
if [ "$DISK_USAGE" -gt 80 ]; then
    alert "VPS disk usage is high: ${DISK_USAGE}%"
fi
