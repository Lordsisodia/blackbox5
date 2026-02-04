#!/bin/bash
# Setup YouTube Transcript Pipeline on Server
# Run on 77.42.66.40

set -e

REPO_URL="https://github.com/Lordsisodia/AI-Improvement-Research.git"
PIPELINE_DIR="/opt/youtube-pipeline"
REPO_DIR="$PIPELINE_DIR/repo"
CONTENT_DIR="$PIPELINE_DIR/content"
STATE_DIR="$PIPELINE_DIR/state"
LOG_DIR="$PIPELINE_DIR/logs"

echo "=========================================="
echo "YouTube Transcript Pipeline Setup"
echo "=========================================="
echo ""

# Create user
echo "[1/10] Creating youtube-pipeline user..."
useradd -m -s /bin/bash youtube-pipeline 2>/dev/null || true

# Create directories
echo "[2/10] Creating directories..."
mkdir -p "$CONTENT_DIR" "$STATE_DIR" "$LOG_DIR"
chown -R youtube-pipeline:youtube-pipeline "$PIPELINE_DIR"

# Install dependencies
echo "[3/10] Installing dependencies..."
apt-get update -qq
apt-get install -y -qq git python3 python3-pip python3-venv sqlite3

# Clone repository
echo "[4/10] Cloning repository..."
if [ -d "$REPO_DIR/.git" ]; then
    echo "  Repo exists, pulling latest..."
    cd "$REPO_DIR"
    sudo -u youtube-pipeline git pull
else
    sudo -u youtube-pipeline git clone "$REPO_URL" "$REPO_DIR"
fi

# Setup Python environment
echo "[5/10] Setting up Python environment..."
cd "$REPO_DIR"
sudo -u youtube-pipeline python3 -m venv venv
sudo -u youtube-pipeline venv/bin/pip install -q --upgrade pip
sudo -u youtube-pipeline venv/bin/pip install -q youtube-transcript-api pyyaml

# Copy queue database
echo "[6/10] Setting up queue database..."
if [ -f "$REPO_DIR/database/queue.db" ]; then
    echo "  Queue database exists"
else
    echo "  WARNING: queue.db not found in repo"
    echo "  You'll need to copy it manually:"
    echo "  scp database/queue.db root@77.42.66.40:$REPO_DIR/database/"
fi

# Create transcript worker service
echo "[7/10] Creating transcript worker service..."
cat > /etc/systemd/system/transcript-worker.service << EOF
[Unit]
Description=YouTube Transcript Worker
After=network.target

[Service]
Type=simple
User=youtube-pipeline
Group=youtube-pipeline
WorkingDirectory=$REPO_DIR
Environment="PYTHONPATH=$REPO_DIR/scripts"
Environment="HOME=/home/youtube-pipeline"
ExecStart=$REPO_DIR/venv/bin/python scripts/worker/worker.py \
    --output-dir $CONTENT_DIR \
    --state-dir $STATE_DIR \
    --daily-limit 200 \
    --request-delay 2.0 \
    --batch-size 10 \
    --continuous
Restart=always
RestartSec=60
StandardOutput=append:$LOG_DIR/worker.log
StandardError=append:$LOG_DIR/worker-error.log

[Install]
WantedBy=multi-user.target
EOF

# Create git sync script
echo "[8/10] Creating git sync script..."
cat > "$PIPELINE_DIR/sync-to-github.sh" << 'EOF'
#!/bin/bash
# Sync transcripts to GitHub

REPO_DIR="/opt/youtube-pipeline/repo"
CONTENT_DIR="/opt/youtube-pipeline/content"
LOG_FILE="/opt/youtube-pipeline/logs/sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cd "$REPO_DIR" || exit 1

# Pull latest (get new queue.db, avoid conflicts)
log "Pulling latest from GitHub..."
git pull origin main

# Check if there are new transcripts to commit
if [ -d "$CONTENT_DIR" ] && [ "$(ls -A $CONTENT_DIR 2>/dev/null)" ]; then
    # Copy transcripts to repo
    mkdir -p content/transcripts
    rsync -a "$CONTENT_DIR/" content/transcripts/

    # Check for changes
    if git diff --quiet HEAD -- content/transcripts/; then
        log "No new transcripts to commit"
    else
        # Commit and push
        git add content/transcripts/
        git commit -m "transcripts: $(date -u '+%Y-%m-%d %H:%M UTC')"
        git push origin main
        log "Pushed transcripts to GitHub"
    fi
else
    log "No transcript files found"
fi

# Also commit queue.db updates (status changes)
if ! git diff --quiet HEAD -- database/queue.db; then
    git add database/queue.db
    git commit -m "queue: update status $(date -u '+%Y-%m-%d %H:%M UTC')"
    git push origin main
    log "Pushed queue.db updates"
fi
EOF

chmod +x "$PIPELINE_DIR/sync-to-github.sh"
chown youtube-pipeline:youtube-pipeline "$PIPELINE_DIR/sync-to-github.sh"

# Create cron job for git sync
echo "[9/10] Setting up git sync cron job..."
cat > /etc/cron.d/youtube-pipeline << EOF
# Sync transcripts to GitHub every hour
0 * * * * youtube-pipeline /opt/youtube-pipeline/sync-to-github.sh >> /opt/youtube-pipeline/logs/sync.log 2>&1

# Clean old logs weekly
0 0 * * 0 root find /opt/youtube-pipeline/logs -name "*.log" -mtime +7 -delete
EOF

chmod 644 /etc/cron.d/youtube-pipeline

# Create status check script
echo "[10/10] Creating status check script..."
cat > "$PIPELINE_DIR/status.sh" << 'EOF'
#!/bin/bash
echo "=========================================="
echo "YouTube Pipeline Status"
echo "=========================================="
echo ""

echo "Services:"
systemctl is-active transcript-worker 2>/dev/null && echo "  ✓ transcript-worker: RUNNING" || echo "  ✗ transcript-worker: STOPPED"
echo ""

echo "Queue Status:"
cd /opt/youtube-pipeline/repo
/opt/youtube-pipeline/repo/venv/bin/python -c "
import sys
sys.path.insert(0, 'scripts')
from queue.manager import QueueManager
m = QueueManager()
stats = m.get_stats()
priority = m.get_priority_distribution()
print(f\"  Total: {stats['total']}\")
print(f\"  Pending: {stats['pending']}\")
print(f\"  Completed: {stats['completed']}\")
print(f\"  Failed: {stats['failed']}\")
print(f\"  Priority: P0={priority.get('P0',0)}, P1={priority.get('P1',0)}, P2={priority.get('P2',0)}, P3={priority.get('P3',0)}\")
" 2>/dev/null || echo "  (Could not read queue)"
echo ""

echo "Transcripts:"
TRANSCRIPT_COUNT=$(find /opt/youtube-pipeline/content -name "*.md" 2>/dev/null | wc -l)
echo "  Total transcripts: $TRANSCRIPT_COUNT"
echo ""

echo "Disk Usage:"
df -h /opt/youtube-pipeline | tail -1 | awk '{print "  Used: " $3 " / " $2 " (" $5 ")"}'
echo ""

echo "Recent Log:"
tail -5 /opt/youtube-pipeline/logs/worker.log 2>/dev/null || echo "  (No log yet)"
echo ""
EOF

chmod +x "$PIPELINE_DIR/status.sh"
chown youtube-pipeline:youtube-pipeline "$PIPELINE_DIR/status.sh"

# Reload systemd
systemctl daemon-reload

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy queue.db to the server:"
echo "   scp database/queue.db root@77.42.66.40:$REPO_DIR/database/"
echo ""
echo "2. Setup GitHub SSH key for youtube-pipeline user:"
echo "   sudo -u youtube-pipeline ssh-keygen -t ed25519"
echo "   sudo -u youtube-pipeline cat /home/youtube-pipeline/.ssh/id_ed25519.pub"
echo "   # Add to GitHub: https://github.com/settings/keys"
echo ""
echo "3. Configure git user:"
echo "   sudo -u youtube-pipeline git config --global user.email 'bot@example.com'"
echo "   sudo -u youtube-pipeline git config --global user.name 'Transcript Bot'"
echo ""
echo "4. Start the worker:"
echo "   sudo systemctl start transcript-worker"
echo "   sudo systemctl enable transcript-worker"
echo ""
echo "5. Check status:"
echo "   /opt/youtube-pipeline/status.sh"
echo ""
echo "Logs:"
echo "   Worker: tail -f /opt/youtube-pipeline/logs/worker.log"
echo "   Sync:   tail -f /opt/youtube-pipeline/logs/sync.log"
echo ""
