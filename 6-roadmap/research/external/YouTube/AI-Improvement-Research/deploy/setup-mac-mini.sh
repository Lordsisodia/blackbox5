#!/bin/bash
# Setup YouTube Transcript Worker on Mac Mini (Home Server)
# Run this on your 16GB Mac Mini

set -e

echo "=========================================="
echo "YouTube Transcript Worker - Mac Mini Setup"
echo "=========================================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script is for macOS only"
    exit 1
fi

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    echo "[1/8] Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "[1/8] Homebrew already installed"
fi

# Install dependencies
echo "[2/8] Installing dependencies..."
brew install git python@3.11 sqlite3

# Create user
echo "[3/8] Creating youtube-pipeline user..."
sudo sysadminctl -addUser youtube-pipeline -fullName "YouTube Pipeline" -password "$(openssl rand -base64 12)" 2>/dev/null || echo "User may already exist"

# Setup directories
echo "[4/8] Setting up directories..."
PIPELINE_DIR="/Users/youtube-pipeline/youtube-pipeline"
sudo mkdir -p "$PIPELINE_DIR/content" "$PIPELINE_DIR/state" "$PIPELINE_DIR/logs"
sudo chown -R youtube-pipeline:staff "$PIPELINE_DIR"

# Clone repository
echo "[5/8] Cloning repository..."
sudo -u youtube-pipeline git clone https://github.com/lordsisodia/youtube-ai-research.git "$PIPELINE_DIR/repo"

# Setup Python environment
echo "[6/8] Setting up Python environment..."
cd "$PIPELINE_DIR/repo"
sudo -u youtube-pipeline python3.11 -m venv venv
sudo -u youtube-pipeline venv/bin/pip install --upgrade pip
sudo -u youtube-pipeline venv/bin/pip install youtube-transcript-api pyyaml

# Copy queue database
echo "[7/8] Setting up queue database..."
if [ ! -f "$PIPELINE_DIR/repo/database/queue.db" ]; then
    echo "  WARNING: queue.db not found in repo"
    echo "  You'll need to copy it manually:"
    echo "  scp database/queue.db youtube-pipeline@mac-mini-ip:$PIPELINE_DIR/repo/database/"
fi

# Create LaunchAgent plist for auto-start
echo "[8/8] Creating LaunchAgent for auto-start..."
sudo -u youtube-pipeline mkdir -p /Users/youtube-pipeline/Library/LaunchAgents

cat > /Users/youtube-pipeline/Library/LaunchAgents/com.youtube.transcript-worker.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.youtube.transcript-worker</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/youtube-pipeline/youtube-pipeline/repo/venv/bin/python</string>
        <string>scripts/worker/worker.py</string>
        <string>--output-dir</string>
        <string>/Users/youtube-pipeline/youtube-pipeline/content</string>
        <string>--state-dir</string>
        <string>/Users/youtube-pipeline/youtube-pipeline/state</string>
        <string>--daily-limit</string>
        <string>300</string>
        <string>--request-delay</string>
        <string>1.5</string>
        <string>--batch-size</string>
        <string>20</string>
        <string>--continuous</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/youtube-pipeline/youtube-pipeline/repo</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONPATH</key>
        <string>/Users/youtube-pipeline/youtube-pipeline/repo/scripts</string>
        <key>USE_TOR</key>
        <string>false</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/youtube-pipeline/youtube-pipeline/logs/worker.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/youtube-pipeline/youtube-pipeline/logs/worker-error.log</string>
</dict>
</plist>
EOF

sudo chown youtube-pipeline:staff /Users/youtube-pipeline/Library/LaunchAgents/com.youtube.transcript-worker.plist

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy queue.db to the Mac Mini:"
echo "   scp database/queue.db youtube-pipeline@YOUR_MAC_MINI_IP:/Users/youtube-pipeline/youtube-pipeline/repo/database/"
echo ""
echo "2. Start the worker:"
echo "   sudo -u youtube-pipeline launchctl load /Users/youtube-pipeline/Library/LaunchAgents/com.youtube.transcript-worker.plist"
echo ""
echo "3. Check status:"
echo "   tail -f /Users/youtube-pipeline/youtube-pipeline/logs/worker.log"
echo ""
echo "Expected throughput: 200-300 videos/day"
echo "Time to complete 7,814 videos: ~26-39 days"
echo ""
echo "To stop:"
echo "   sudo -u youtube-pipeline launchctl unload /Users/youtube-pipeline/Library/LaunchAgents/com.youtube.transcript-worker.plist"
echo ""
