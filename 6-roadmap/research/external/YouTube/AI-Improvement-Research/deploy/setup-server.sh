#!/bin/bash
# Setup script for dedicated transcript server
# Run on new Hetzner CX23 (or similar) Ubuntu 22.04 server

set -e

echo "=========================================="
echo "Transcript Server Setup"
echo "=========================================="
echo ""

# Update system
echo "[1/8] Updating system packages..."
apt-get update
apt-get upgrade -y

# Install dependencies
echo "[2/8] Installing dependencies..."
apt-get install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    sqlite3 \
    htop \
    tmux

# Create user
echo "[3/8] Creating transcript user..."
useradd -m -s /bin/bash transcript || true
usermod -aG sudo transcript

# Setup directories
echo "[4/8] Setting up directories..."
mkdir -p /opt/transcripts/{content,state,repo}
chown -R transcript:transcript /opt/transcripts

# Clone repository
echo "[5/8] Cloning repository..."
cd /opt/transcripts/repo
sudo -u transcript git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .

# Setup Python environment
echo "[6/8] Setting up Python environment..."
cd /opt/transcripts/repo
sudo -u transcript python3 -m venv venv
sudo -u transcript venv/bin/pip install --upgrade pip
sudo -u transcript venv/bin/pip install youtube-transcript-api

# Install systemd service
echo "[7/8] Installing systemd service..."
cat > /etc/systemd/system/transcript-worker.service << 'EOF'
[Unit]
Description=YouTube Transcript Worker
After=network.target

[Service]
Type=simple
User=transcript
WorkingDirectory=/opt/transcripts/repo
Environment="PYTHONPATH=/opt/transcripts/repo/scripts"
Environment="TRANSFORMERS_CACHE=/opt/transcripts/.cache"
ExecStart=/opt/transcripts/repo/venv/bin/python scripts/worker/worker.py \
    --output-dir /opt/transcripts/content \
    --state-dir /opt/transcripts/state \
    --daily-limit 200 \
    --request-delay 2.0 \
    --batch-size 10 \
    --continuous
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable transcript-worker

# Setup log rotation
echo "[8/8] Setting up log rotation..."
cat > /etc/logrotate.d/transcript-worker << 'EOF'
/opt/transcripts/state/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 transcript transcript
}
EOF

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy queue.db to /opt/transcripts/repo/database/"
echo "2. Start the worker: sudo systemctl start transcript-worker"
echo "3. Check status: sudo systemctl status transcript-worker"
echo "4. View logs: sudo journalctl -u transcript-worker -f"
echo ""
echo "Daily throughput: ~200 videos/day"
echo "Time to complete 7,814 videos: ~39 days"
echo ""
