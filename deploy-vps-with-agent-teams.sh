#!/bin/bash
# Deploy BB5 with Agent Teams to Hetzner VPS
# Usage: ./deploy-vps-with-agent-teams.sh

set -e

VPS_IP="77.42.66.40"
VPS_USER="root"
BB5_DIR="/opt/blackbox5"
REPO_URL="https://github.com/shaansisodia/blackbox5.git"

echo "🚀 Deploying BB5 with Agent Teams to VPS..."

# 1. SSH and setup
echo "📡 Connecting to VPS..."
ssh ${VPS_USER}@${VPS_IP} << 'REMOTE_SCRIPT'

# Install dependencies if needed
if ! command -v git &> /dev/null; then
    apt-get update
    apt-get install -y git curl nodejs npm
fi

# Install Claude Code if not present
if ! command -v claude &> /dev/null; then
    curl -fsSL https://claude.ai/install.sh | sh
fi

# Setup BB5 directory
mkdir -p /opt
cd /opt

# Clone or pull
if [ -d "blackbox5" ]; then
    echo "📥 Pulling latest..."
    cd blackbox5
    git pull origin main
else
    echo "📥 Cloning repository..."
    git clone ${REPO_URL} blackbox5
    cd blackbox5
fi

# Ensure directory structure
mkdir -p .autonomous/tasks/active
mkdir -p .autonomous/tasks/completed
mkdir -p .autonomous/memory/data
mkdir -p .autonomous/agents/communications
mkdir -p runs

# Make hooks executable
chmod +x .claude/hooks/*.sh 2>/dev/null || true

echo "✅ BB5 deployed to ${BB5_DIR}"

REMOTE_SCRIPT

# 2. Copy local configuration
echo "📋 Copying local config..."
scp .mcp-moltbot.json ${VPS_USER}@${VPS_IP}:${BB5_DIR}/

# 3. Create systemd service for RALF with Agent Teams
echo "⚙️ Creating systemd service..."
ssh ${VPS_USER}@${VPS_IP} << 'SERVICE_SCRIPT'

cat > /etc/systemd/system/bb5-agent-teams.service << 'EOF'
[Unit]
Description=BB5 Agent Teams Autonomous Loop
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/blackbox5
Environment="CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1"
Environment="BB5_MODE=autonomous"
ExecStart=/opt/blackbox5/bin/ralf-loops/loops/ralf-core.sh --continuous --agent-teams
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable bb5-agent-teams.service

echo "✅ Service created"

SERVICE_SCRIPT

echo ""
echo "🎉 Deployment Complete!"
echo ""
echo "Next steps:"
echo "1. SSH to VPS: ssh root@${VPS_IP}"
echo "2. Set API keys: export ANTHROPIC_API_KEY=your_key"
echo "3. Start service: systemctl start bb5-agent-teams"
echo "4. Check status: systemctl status bb5-agent-teams"
echo "5. View logs: journalctl -u bb5-agent-teams -f"
