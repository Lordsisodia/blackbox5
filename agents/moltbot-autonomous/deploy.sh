#!/bin/bash
# Deploy MoltBot Autonomous Agent to VPS

set -e

echo "🤖 Deploying MoltBot Autonomous Agent..."

# Configuration
VPS_IP="77.42.66.40"
SSH_KEY="~/.ssh/ralf_hetzner"
BB5_DIR="/opt/blackbox5"
AGENT_DIR="$BB5_DIR/agents/moltbot-autonomous"

# Check if we can connect
echo "Checking VPS connection..."
ssh -i $SSH_KEY -o ConnectTimeout=5 root@$VPS_IP "echo 'Connected!'" || {
    echo "❌ Cannot connect to VPS. Check SSH key and network."
    exit 1
}

# Create agent directory on VPS
echo "Creating agent directory..."
ssh -i $SSH_KEY root@$VPS_IP "mkdir -p $AGENT_DIR/state $BB5_DIR/.logs/moltbot"

# Copy agent files
echo "Copying agent files..."
scp -i $SSH_KEY -r \
    agents/moltbot-autonomous/moltbot-agent.py \
    agents/moltbot-autonomous/MOLTBOT-SPEC.md \
    root@$VPS_IP:$AGENT_DIR/

# Install Python dependencies
echo "Installing dependencies..."
ssh -i $SSH_KEY root@$VPS_IP "pip3 install -q pyyaml requests schedule 2>/dev/null || true"

# Create systemd service
echo "Creating systemd service..."
ssh -i $SSH_KEY root@$VPS_IP "cat > /etc/systemd/system/moltbot-autonomous.service << 'EOF'
[Unit]
Description=MoltBot Autonomous Agent for BlackBox5
After=network.target moltbot.service
Wants=moltbot.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/blackbox5
Environment="HOME=/root"
Environment="TELEGRAM_BOT_TOKEN=8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo"
Environment="TELEGRAM_CHAT_ID=7643203581"
Environment="GITHUB_TOKEN=${GITHUB_TOKEN:-}"
Environment="RALF_ENGINE_DIR=/opt/blackbox5/2-engine/.autonomous"
Environment="RALF_PROJECT_DIR=/opt/blackbox5/5-project-memory/blackbox5"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/usr/bin/python3 /opt/blackbox5/agents/moltbot-autonomous/moltbot-agent.py
Restart=always
RestartSec=60
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF"

# Reload and start
echo "Starting service..."
ssh -i $SSH_KEY root@$VPS_IP "
    systemctl daemon-reload
    systemctl enable moltbot-autonomous
    systemctl restart moltbot-autonomous
    sleep 2
    systemctl status moltbot-autonomous --no-pager
"

echo ""
echo "✅ MoltBot Autonomous Agent deployed!"
echo ""
echo "Commands:"
echo "  Check status:  ssh -i $SSH_KEY root@$VPS_IP 'systemctl status moltbot-autonomous'"
echo "  View logs:     ssh -i $SSH_KEY root@$VPS_IP 'journalctl -u moltbot-autonomous -f'"
echo "  Stop:          ssh -i $SSH_KEY root@$VPS_IP 'systemctl stop moltbot-autonomous'"
echo "  Restart:       ssh -i $SSH_KEY root@$VPS_IP 'systemctl restart moltbot-autonomous'"
echo ""
echo "Telegram: You should receive a 'MoltBot is online' message shortly"
