#!/bin/bash
# deploy-vps-full.sh - Complete BlackBox5 VPS Deployment
# Deploys BlackBox5 to VPS with autonomous operation setup

set -e

VPS_IP="77.42.66.40"
VPS_USER="root"
SSH_KEY="$HOME/.ssh/ralf_hetzner"
BB5_DIR="$HOME/.blackbox5"
VPS_BB5_DIR="/opt/blackbox5"
BRANCH="autonomous-improvement"

echo "═══════════════════════════════════════════════════════════"
echo "  BlackBox5 VPS Deployment"
echo "═══════════════════════════════════════════════════════════"
echo "VPS: $VPS_USER@$VPS_IP"
echo "Branch: $BRANCH"
echo "Local: $BB5_DIR"
echo "Remote: $VPS_BB5_DIR"
echo ""

# Step 1: Ensure we're on the right branch locally
echo "[1/6] Preparing local branch..."
cd "$BB5_DIR"
git checkout "$BRANCH"
git pull origin "$BRANCH" 2>/dev/null || true
git push origin "$BRANCH" 2>/dev/null || true
echo "    Local branch ready"

# Step 2: Sync files to VPS
echo ""
echo "[2/6] Syncing BlackBox5 to VPS..."
echo "    This may take a few minutes..."

rsync -avz --progress \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    --exclude='*.log' \
    --exclude='6-roadmap-backup-*' \
    -e "ssh -i $SSH_KEY" \
    "$BB5_DIR/" \
    "$VPS_USER@$VPS_IP:$VPS_BB5_DIR/"

echo "    Sync complete"

# Step 3: Setup VPS environment
echo ""
echo "[3/6] Setting up VPS environment..."

ssh -i "$SSH_KEY" "$VPS_USER@$VPS_IP" << 'VPS_SETUP'
set -e

BB5_DIR="/opt/blackbox5"

# Create required directories
mkdir -p /root/.claude/hooks
mkdir -p /root/.claude/agents
mkdir -p /root/.claude/skills
mkdir -p "$BB5_DIR/.autonomous/logs"
mkdir -p "$BB5_DIR/.autonomous/runs"
mkdir -p "$BB5_DIR/.autonomous/signals"
mkdir -p "$BB5_DIR/5-project-memory/blackbox5/.autonomous/runs"
mkdir -p "$BB5_DIR/5-project-memory/blackbox5/.autonomous/logs"
mkdir -p "$BB5_DIR/5-project-memory/blackbox5/.autonomous/communications"
mkdir -p "$BB5_DIR/5-project-memory/blackbox5/.autonomous/state"
mkdir -p "$BB5_DIR/5-project-memory/blackbox5/tasks/active"
mkdir -p "$BB5_DIR/5-project-memory/blackbox5/tasks/completed"

# Copy .claude configuration
cp -r "$BB5_DIR/.claude/hooks/"* /root/.claude/hooks/ 2>/dev/null || true
cp -r "$BB5_DIR/.claude/agents/"* /root/.claude/agents/ 2>/dev/null || true
cp -r "$BB5_DIR/.claude/skills/"* /root/.claude/skills/ 2>/dev/null || true

# Make scripts executable
chmod +x "$BB5_DIR/bin/"*.sh 2>/dev/null || true
chmod +x "$BB5_DIR/bin/"*.py 2>/dev/null || true
chmod +x "$BB5_DIR/bin/ralf-loops/loops/"*.sh 2>/dev/null || true
chmod +x "$BB5_DIR/agents/moltbot-autonomous/"*.sh 2>/dev/null || true
chmod +x /root/.claude/hooks/*.sh 2>/dev/null || true

# Install bb5 CLI if exists
if [ -f "$BB5_DIR/bb5" ]; then
    cp "$BB5_DIR/bb5" /usr/local/bin/bb5
    chmod +x /usr/local/bin/bb5
fi

echo "    VPS environment setup complete"
VPS_SETUP

# Step 4: Setup systemd service
echo ""
echo "[4/6] Setting up systemd service..."

ssh -i "$SSH_KEY" "$VPS_USER@$VPS_IP" << 'SYSTEMD_SETUP'
set -e

BB5_DIR="/opt/blackbox5"

# Create systemd service file
cat > /etc/systemd/system/blackbox5-agent.service << 'EOF'
[Unit]
Description=BlackBox5 Autonomous Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/blackbox5
Environment=BB5_DIR=/opt/blackbox5
Environment=HOME=/root
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=PYTHONUNBUFFERED=1

# Start the Moltbot RALF Manager (which runs RALF cycles continuously)
ExecStart=/opt/blackbox5/agents/moltbot-autonomous/moltbot-ralf-manager.sh

# Restart configuration
Restart=always
RestartSec=10
StartLimitInterval=60
StartLimitBurst=3

# Logging
StandardOutput=append:/var/log/blackbox5-agent.log
StandardError=append:/var/log/blackbox5-agent.log

[Install]
WantedBy=multi-user.target
EOF

# Create log directory and file
touch /var/log/blackbox5-agent.log
chmod 644 /var/log/blackbox5-agent.log

# Reload systemd
systemctl daemon-reload

echo "    Systemd service created"
SYSTEMD_SETUP

# Step 5: Setup log rotation
echo ""
echo "[5/6] Setting up log rotation..."

ssh -i "$SSH_KEY" "$VPS_USER@$VPS_IP" << 'LOGROTATE_SETUP'
set -e

# Create logrotate config
cat > /etc/logrotate.d/blackbox5 << 'EOF'
/var/log/blackbox5-agent.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
    postrotate
        systemctl reload blackbox5-agent 2>/dev/null || true
    endscript
}

/opt/blackbox5/.autonomous/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}

/opt/blackbox5/5-project-memory/blackbox5/.autonomous/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}
EOF

echo "    Log rotation configured"
LOGROTATE_SETUP

# Step 6: Initialize and start service
echo ""
echo "[6/6] Initializing service..."

ssh -i "$SSH_KEY" "$VPS_USER@$VPS_IP" << 'INIT_SERVICE'
set -e

BB5_DIR="/opt/blackbox5"

# Initialize git in VPS directory if needed
cd "$BB5_DIR"
if [ ! -d "$BB5_DIR/.git" ]; then
    git init
    git remote add origin https://github.com/shaansisodia/blackbox5.git 2>/dev/null || true
fi

# Configure git
git config user.email "vps@blackbox5.local"
git config user.name "BlackBox5 VPS"

# Fetch and checkout the autonomous-improvement branch
git fetch origin autonomous-improvement || true
git checkout -B autonomous-improvement origin/autonomous-improvement 2>/dev/null || git checkout autonomous-improvement 2>/dev/null || true

# Create initial spawn queue if it doesn't exist
QUEUE_FILE="$BB5_DIR/5-project-memory/blackbox5/.autonomous/communications/queue-core.yaml"
if [ ! -f "$QUEUE_FILE" ]; then
    echo "[]" > "$QUEUE_FILE"
fi

# Enable and start the service
systemctl enable blackbox5-agent.service
systemctl start blackbox5-agent.service

echo "    Service initialized and started"
INIT_SERVICE

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Deployment Complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "VPS BlackBox5 Status:"
ssh -i "$SSH_KEY" "$VPS_USER@$VPS_IP" "systemctl status blackbox5-agent --no-pager -l" 2>/dev/null || echo "    (Check status manually)"
echo ""
echo "Useful Commands:"
echo "  ssh -i ~/.ssh/ralf_hetzner root@$VPS_IP"
echo "  systemctl status blackbox5-agent"
echo "  tail -f /var/log/blackbox5-agent.log"
echo "  journalctl -u blackbox5-agent -f"
echo ""
echo "Logs:"
echo "  Service log: /var/log/blackbox5-agent.log"
echo "  RALF runs: /opt/blackbox5/5-project-memory/blackbox5/.autonomous/runs/"
echo ""
