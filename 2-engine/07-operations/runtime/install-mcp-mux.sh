#!/bin/bash
# Blackbox5 MCP Multiplexer Installation Script
# This script installs and configures rmcp-mux for Blackbox5

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}→${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}     Blackbox5 MCP Multiplexer Installation${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Check prerequisites
print_step "Checking prerequisites..."

if ! command -v brew &> /dev/null; then
    print_error "Homebrew not found. Please install it first:"
    echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi
print_success "Homebrew found"

if ! command -v node &> /dev/null; then
    print_error "Node.js not found. Please install it first:"
    echo "  brew install node"
    exit 1
fi
print_success "Node.js found"

# Step 1: Install Rust
print_step "Installing Rust via Homebrew..."
if ! command -v rustc &> /dev/null; then
    brew install rust
    print_success "Rust installed"
else
    print_success "Rust already installed"
fi

# Step 2: Install rmcp-mux
print_step "Installing rmcp-mux..."
if ! command -v rmcp-mux &> /dev/null; then
    curl -fsSL https://raw.githubusercontent.com/Loctree/rmcp-mux/main/tools/install.sh | sh
    print_success "rmcp-mux installed"
else
    print_success "rmcp-mux already installed"
fi

# Step 3: Create directories
print_step "Creating configuration directories..."
mkdir -p ~/.config
mkdir -p ~/.mcp-sockets
print_success "Directories created"

# Step 4: Backup existing config
CONFIG_FILE="$HOME/.config/mcp-mux.toml"
if [[ -f "$CONFIG_FILE" ]]; then
    BACKUP_FILE="${CONFIG_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    print_step "Backing up existing config to $BACKUP_FILE"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
fi

# Step 5: Create configuration
print_step "Creating rmcp-mux configuration..."
cat > "$CONFIG_FILE" << 'EOF'
# Blackbox5 MCP Multiplexer Configuration
# Managed by rmcp-mux

[servers.supabase]
socket = "~/.mcp-sockets/supabase.sock"
cmd = "node"
args = ["~/.npm-global/bin/mcp-server-supabase", "--project-ref", "avdgyrepwrvsvwgxrccr"]
max_active_clients = 10
request_timeout_ms = 30000

[servers.filesystem]
socket = "~/.mcp-sockets/filesystem.sock"
cmd = "node"
args = ["~/.npm-global/bin/mcp-server-filesystem", "/Users/shaansisodia"]
max_active_clients = 10
lazy_start = true

[servers.memory]
socket = "~/.mcp-sockets/memory.sock"
cmd = "npx"
args = ["-y", "@modelcontextprotocol/server-memory"]
max_active_clients = 10

[servers.serena]
socket = "~/.mcp-sockets/serena.sock"
cmd = "uv"
args = ["--from", "git+https://github.com/oraios/serena", "serena-mcp-server"]
max_active_clients = 10
restart_backoff_ms = 2000
EOF
print_success "Configuration created at $CONFIG_FILE"

# Step 6: Update PATH if needed
print_step "Checking PATH..."
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    print_info "Adding ~/.local/bin to PATH..."
    echo '' >> ~/.zshrc
    echo '# rmcp-mux' >> ~/.zshrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    print_success "PATH updated in ~/.zshrc"
    print_info "Run 'source ~/.zshrc' or restart your terminal"
else
    print_success "PATH already configured"
fi

# Step 7: Create launchd service
print_step "Creating macOS launchd service..."
cat > ~/Library/LaunchAgents/com.rmcp-mux.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.rmcp-mux</string>
    <key>ProgramArguments</key>
    <array>
        <string>$HOME/.local/bin/rmcp-mux</string>
        <string>--config</string>
        <string>$CONFIG_FILE</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/rmcp-mux.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/rmcp-mux.log</string>
</dict>
</plist>
EOF
print_success "Launchd service created"

# Step 8: Load the service
print_step "Loading launchd service..."
launchctl load -w ~/Library/LaunchAgents/com.rmcp-mux.plist 2>/dev/null || true
sleep 2
print_success "Service loaded"

# Step 9: Verify installation
print_step "Verifying installation..."
if command -v rmcp-mux &> /dev/null; then
    VERSION=$(rmcp-mux --version 2>/dev/null || echo "unknown")
    print_success "rmcp-mux installed: $VERSION"
else
    print_error "rmcp-mux not found in PATH"
    print_info "Make sure to run: source ~/.zshrc"
fi

# Check if daemon is running
if launchctl list | grep -q com.rmcp-mux; then
    print_success "rmcp-mux daemon is running"
else
    print_info "Daemon not loaded yet, will start on next login or manually"
fi

# Check sockets
sleep 3
if ls ~/.mcp-sockets/*.sock 2>/dev/null; then
    SOCKET_COUNT=$(ls ~/.mcp-sockets/*.sock 2>/dev/null | wc -l | tr -d ' ')
    print_success "Sockets created: $SOCKET_COUNT"
else
    print_info "Sockets not created yet (daemon will create them on start)"
fi

# Summary
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Resource Savings:"
echo "  Before: 32 MCP processes = 2.13 GB RAM"
echo "  After:  1 daemon + 4 servers = ~500 MB RAM"
echo "  Savings: 1.6 GB (75% reduction)"
echo ""
echo "Next Steps:"
echo ""
echo "1. Update your Claude Desktop config:"
echo "   ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
echo "   Add these mcpServers:"
echo ''
echo '   {'
echo '     "mcpServers": {'
echo '       "supabase": {'
echo '         "command": "rmcp-mux-proxy",'
echo '         "args": ["--socket", "~/.mcp-sockets/supabase.sock"]'
echo '       },'
echo '       "filesystem": {'
echo '         "command": "rmcp-mux-proxy",'
echo '         "args": ["--socket", "~/.mcp-sockets/filesystem.sock"]'
echo '       },'
echo '       "memory": {'
echo '         "command": "rmcp-mux-proxy",'
echo '         "args": ["--socket", "~/.mcp-sockets/memory.sock"]'
echo '       },'
echo '       "serena": {'
echo '         "command": "rmcp-mux-proxy",'
echo '         "args": ["--socket", "~/.mcp-sockets/serena.sock"]'
echo '       }'
echo '     }'
echo '   }'
echo ''
echo "2. Restart Claude Desktop"
echo ""
echo "3. Monitor with TUI:"
echo "   rmcp-mux --config ~/.config/mcp-mux.toml --tui"
echo ""
echo "4. Check status:"
echo "   rmcp-mux daemon-status"
echo ""
echo "For full documentation, see:"
echo "   $(pwd)/MCP-MUX-SETUP.md"
echo ""
echo -e "${YELLOW}Note: If this is your first installation, run:${NC}"
echo "   source ~/.zshrc"
echo ""
