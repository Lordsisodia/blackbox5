#!/bin/bash
# Mac Mini Setup Script - No Admin Required
# Sets up MoltBot, YouTube pipeline, and all services

set -e

echo "=========================================="
echo "Mac Mini Setup (User Space)"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create directory structure
log_info "Creating directory structure..."
mkdir -p ~/Projects
mkdir -p ~/.local/bin
mkdir -p ~/.local/lib
mkdir -p ~/.local/share
mkdir -p ~/Library/LaunchAgents
mkdir -p ~/.logs
mkdir -p ~/.config/openclaw

# Add local bin to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    log_info "Adding ~/.local/bin to PATH..."
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install Node.js (user space)
log_info "Installing Node.js (user space)..."
if ! command -v node &> /dev/null; then
    NODE_VERSION="20.11.0"
    NODE_DIR="$HOME/.local/lib/nodejs"
    mkdir -p "$NODE_DIR"

    cd /tmp
    curl -O "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-darwin-arm64.tar.gz"
    tar xzf "node-v${NODE_VERSION}-darwin-arm64.tar.gz" -C "$NODE_DIR" --strip-components=1
    rm "node-v${NODE_VERSION}-darwin-arm64.tar.gz"

    # Create symlinks
    ln -sf "$NODE_DIR/bin/node" ~/.local/bin/node
    ln -sf "$NODE_DIR/bin/npm" ~/.local/bin/npm
    ln -sf "$NODE_DIR/bin/npx" ~/.local/bin/npx

    log_info "Node.js installed: $(~/.local/bin/node --version)"
else
    log_info "Node.js already installed: $(node --version)"
fi

# Install OpenClaw
log_info "Installing OpenClaw..."
if ! command -v openclaw &> /dev/null; then
    # Create a wrapper script for openclaw
    cat > ~/.local/bin/openclaw << 'EOF'
#!/bin/bash
# OpenClaw wrapper - runs from user install
export NODE_PATH="$HOME/.local/lib/node_modules"
node "$HOME/.local/lib/node_modules/openclaw/openclaw.mjs" "$@"
EOF
    chmod +x ~/.local/bin/openclaw

    # Try to install via npm, fallback to local
    if npm install -g openclaw 2>/dev/null; then
        log_info "OpenClaw installed globally via npm"
    else
        # Install locally
        mkdir -p ~/.local/lib/node_modules
        cd ~/.local/lib
        npm install openclaw 2>/dev/null || {
            log_warn "Could not install OpenClaw via npm"
            log_info "Creating placeholder - you'll need to manually install"
        }
    fi
else
    log_info "OpenClaw already installed"
fi

# Set up MoltBot LaunchAgent
log_info "Setting up MoltBot LaunchAgent..."

MOLTBOT_PLIST="$HOME/Library/LaunchAgents/com.siso.moltbot.plist"

cat > "$MOLTBOT_PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.siso.moltbot</string>
    <key>ProgramArguments</key>
    <array>
        <string>$HOME/.local/bin/openclaw</string>
        <string>gateway</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$HOME/Projects/moltbot</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>HOME</key>
        <string>$HOME</string>
        <key>OPENCLAW_CONFIG</key>
        <string>$HOME/.openclaw</string>
        <key>PATH</key>
        <string>$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
        <key>Crashed</key>
        <true/>
    </dict>
    <key>ThrottleInterval</key>
    <integer>30</integer>
    <key>StandardOutPath</key>
    <string>$HOME/Projects/moltbot/logs/moltbot.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/Projects/moltbot/logs/moltbot-error.log</string>
</dict>
</plist>
EOF

log_info "MoltBot LaunchAgent created"

# Set up YouTube Worker LaunchAgent
log_info "Setting up YouTube Worker LaunchAgent..."

YOUTUBE_PLIST="$HOME/Library/LaunchAgents/com.siso.youtube-worker.plist"

cat > "$YOUTUBE_PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.siso.youtube-worker</string>
    <key>ProgramArguments</key>
    <array>
        <string>$HOME/Projects/youtube-ai-research/venv/bin/python</string>
        <string>$HOME/Projects/youtube-ai-research/scripts/worker/worker.py</string>
        <string>--output-dir</string>
        <string>$HOME/Projects/youtube-ai-research/content/transcripts</string>
        <string>--state-dir</string>
        <string>$HOME/Projects/youtube-ai-research/.state</string>
        <string>--daily-limit</string>
        <string>100</string>
        <string>--request-delay</string>
        <string>3.0</string>
        <string>--batch-size</string>
        <string>5</string>
        <string>--continuous</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$HOME/Projects/youtube-ai-research</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONPATH</key>
        <string>$HOME/Projects/youtube-ai-research/scripts</string>
        <key>PATH</key>
        <string>$HOME/Projects/youtube-ai-research/venv/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
        <key>Crashed</key>
        <true/>
    </dict>
    <key>ThrottleInterval</key>
    <integer>60</integer>
    <key>StandardOutPath</key>
    <string>$HOME/Projects/youtube-ai-research/.logs/worker.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/Projects/youtube-ai-research/.logs/worker-error.log</string>
    <key>Nice</key>
    <integer>10</integer>
</dict>
</plist>
EOF

log_info "YouTube Worker LaunchAgent created"

# Create convenience scripts
log_info "Creating convenience scripts..."

cat > ~/.local/bin/moltbot-start << 'EOF'
#!/bin/bash
launchctl load ~/Library/LaunchAgents/com.siso.moltbot.plist 2>/dev/null || echo "Already loaded or error occurred"
echo "MoltBot started (check logs with: tail -f ~/Projects/moltbot/logs/moltbot.log)"
EOF
chmod +x ~/.local/bin/moltbot-start

cat > ~/.local/bin/moltbot-stop << 'EOF'
#!/bin/bash
launchctl unload ~/Library/LaunchAgents/com.siso.moltbot.plist 2>/dev/null
echo "MoltBot stopped"
EOF
chmod +x ~/.local/bin/moltbot-stop

cat > ~/.local/bin/moltbot-logs << 'EOF'
#!/bin/bash
tail -f ~/Projects/moltbot/logs/moltbot.log
EOF
chmod +x ~/.local/bin/moltbot-logs

cat > ~/.local/bin/youtube-start << 'EOF'
#!/bin/bash
launchctl load ~/Library/LaunchAgents/com.siso.youtube-worker.plist 2>/dev/null || echo "Already loaded or error occurred"
echo "YouTube worker started (check logs with: tail -f ~/Projects/youtube-ai-research/.logs/worker.log)"
EOF
chmod +x ~/.local/bin/youtube-start

cat > ~/.local/bin/youtube-stop << 'EOF'
#!/bin/bash
launchctl unload ~/Library/LaunchAgents/com.siso.youtube-worker.plist 2>/dev/null
echo "YouTube worker stopped"
EOF
chmod +x ~/.local/bin/youtube-stop

cat > ~/.local/bin/youtube-logs << 'EOF'
#!/bin/bash
tail -f ~/Projects/youtube-ai-research/.logs/worker.log
EOF
chmod +x ~/.local/bin/youtube-logs

cat > ~/.local/bin/youtube-status << 'EOF'
#!/bin/bash
cd ~/Projects/youtube-ai-research
source venv/bin/activate
sqlite3 database/queue.db "SELECT status, COUNT(*) FROM video_queue GROUP BY status;"
EOF
chmod +x ~/.local/bin/youtube-status

# Create status checker script
log_info "Creating status checker..."

cat > ~/.local/bin/server-status << 'EOF'
#!/bin/bash
echo "=========================================="
echo "Mac Mini Server Status"
echo "=========================================="
echo ""

echo "MoltBot:"
if launchctl list | grep -q com.siso.moltbot; then
    echo "  ✅ Running"
else
    echo "  ❌ Not running"
fi
echo ""

echo "YouTube Worker:"
if launchctl list | grep -q com.siso.youtube-worker; then
    echo "  ✅ Running"
else
    echo "  ❌ Not running"
fi
echo ""

echo "Queue Status:"
cd ~/Projects/youtube-ai-research 2>/dev/null && source venv/bin/activate 2>/dev/null && sqlite3 database/queue.db "SELECT '  ' || status || ': ' || COUNT(*) FROM video_queue GROUP BY status;" 2>/dev/null || echo "  Could not read database"
echo ""

echo "Recent Logs:"
echo "  MoltBot: tail -f ~/Projects/moltbot/logs/moltbot.log"
echo "  YouTube: tail -f ~/Projects/youtube-ai-research/.logs/worker.log"
echo ""

echo "Commands:"
echo "  moltbot-start    - Start MoltBot"
echo "  moltbot-stop     - Stop MoltBot"
echo "  moltbot-logs     - View MoltBot logs"
echo "  youtube-start    - Start YouTube worker"
echo "  youtube-stop     - Stop YouTube worker"
echo "  youtube-logs     - View YouTube logs"
echo "  youtube-status   - Check queue status"
EOF
chmod +x ~/.local/bin/server-status

# Create SSH wrapper for remote access
log_info "Creating SSH wrapper scripts..."

cat > ~/.local/bin/remote-moltbot-status << 'EOF'
#!/bin/bash
ssh mac-mini "server-status"
EOF
chmod +x ~/.local/bin/remote-moltbot-status

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Reload your shell or run:"
echo "   export PATH=\"$HOME/.local/bin:$PATH\""
echo ""
echo "2. Start services:"
echo "   moltbot-start"
echo "   youtube-start"
echo ""
echo "3. Check status:"
echo "   server-status"
echo ""
echo "4. View logs:"
echo "   moltbot-logs"
echo "   youtube-logs"
echo ""
echo "5. From your laptop, check remotely:"
echo "   ssh mac-mini 'server-status'"
echo ""
echo "Note: If OpenClaw installation failed, you may need to install it manually:"
echo "   npm install -g openclaw"
echo ""
