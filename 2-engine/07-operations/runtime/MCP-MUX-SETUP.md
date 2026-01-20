# MCP Multiplexer Setup Guide for Blackbox5

## Overview

This guide will help you set up **rmcp-mux** to eliminate duplicate MCP servers and save ~1.6 GB of RAM.

**Current State:** 32 MCP processes = 2.13 GB RAM
**After Setup:** 1 rmcp-mux daemon + 4 servers = ~500 MB RAM
**Savings:** 1.6 GB RAM (75% reduction)

## What is rmcp-mux?

rmcp-mux is a **Rust daemon** that:
- Manages ALL MCP servers from a single process
- Provides Unix sockets for each service
- Enables sharing across ALL Claude sessions
- Auto-restarts crashed servers
- Caches initialization (faster startup)
- Includes TUI dashboard for monitoring

## Architecture

```
Before (Current):
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Claude 1    │  │ Claude 2    │  │ Claude N    │
│ ├─Supabase  │  │ ├─Supabase  │  │ ├─Supabase  │
│ ├─Filesystem│  │ ├─Filesystem│  │ ├─Filesystem│
│ ├─Memory    │  │ ├─Memory    │  │ ├─Memory    │
│ └─Serena    │  │ └─Serena    │  │ └─Serena    │
└─────────────┘  └─────────────┘  └─────────────┘
    4 MCPs            4 MCPs            4 MCPs
    = 12 for 3 sessions (32 for your current setup)

After (with rmcp-mux):
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Claude 1    │  │ Claude 2    │  │ Claude N    │
│ └─socket──┐ │  │ └─socket──┐ │  │ └─socket──┐ │
└───────────┼─┘  └───────────┼─┘  └───────────┼─┘
            │              │              │
            └──────────────┼──────────────┘
                           ▼
                    ┌──────────────┐
                    │   rmcp-mux   │
                    ├──────────────┤
                    │ Supabase     │
                    │ Filesystem   │
                    │ Memory       │
                    │ Serena       │
                    └──────────────┘
                    = 4 MCPs total (shared by all Claude sessions)
```

## Prerequisites

- macOS (your current system)
- Homebrew (for installing Rust)
- Claude Desktop or Claude Code CLI
- Existing MCP servers installed

## Installation Steps

### Step 1: Install Rust

```bash
# Install Rust via Homebrew
brew install rust

# Verify installation
rustc --version
cargo --version
```

### Step 2: Install rmcp-mux

```bash
# One-line installer
curl -fsSL https://raw.githubusercontent.com/Loctree/rmcp-mux/main/tools/install.sh | sh

# Verify installation
rmcp-mux --version
rmcp-mux-proxy --help
```

The binaries will be installed to `~/.local/bin/` by default.

### Step 3: Create Configuration Directory

```bash
mkdir -p ~/.config
mkdir -p ~/.mcp-sockets
```

### Step 4: Create MCP Multiplexer Configuration

```bash
cat > ~/.config/mcp-mux.toml << 'EOF'
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
```

### Step 5: Update Claude Desktop Configuration

Find your Claude Desktop config file:

```bash
# macOS
~/Library/Application Support/Claude/claude_desktop_config.json
```

Update the `mcpServers` section:

```json
{
  "mcpServers": {
    "supabase": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "~/.mcp-sockets/supabase.sock"]
    },
    "filesystem": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "~/.mcp-sockets/filesystem.sock"]
    },
    "memory": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "~/.mcp-sockets/memory.sock"]
    },
    "serena": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "~/.mcp-sockets/serena.sock"]
    }
  }
}
```

### Step 6: Start the Multiplexer Daemon

```bash
# Start all MCP servers
rmcp-mux --config ~/.config/mcp-mux.toml

# Or start with TUI dashboard
rmcp-mux --config ~/.config/mcp-mux.toml --tui
```

### Step 7: Configure Auto-Start (Optional)

Create a macOS launchd service:

```bash
cat > ~/Library/LaunchAgents/com.rmcp-mux.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.rmcp-mux</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/shaansisodia/.local/bin/rmcp-mux</string>
        <string>--config</string>
        <string>/Users/shaansisodia/.config/mcp-mux.toml</string>
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

# Load the service
launchctl load -w ~/Library/LaunchAgents/com.rmcp-mux.plist

# Check status
launchctl list | grep rmcp-mux
```

## Verification

### Check if rmcp-mux is running:

```bash
# Check process
ps aux | grep rmcp-mux | grep -v grep

# Check sockets
ls -la ~/.mcp-sockets/

# Check status
rmcp-mux --config ~/.config/mcp-mux.toml --show-status
```

### Test MCP connections:

```bash
# Test individual MCP
rmcp-mux health --config ~/.config/mcp-mux.toml --service supabase

# View all status
rmcp-mux daemon-status
```

## Usage Commands

```bash
# Start all servers
rmcp-mux --config ~/.config/mcp-mux.toml

# Start with TUI dashboard
rmcp-mux --config ~/.config/mcp-mux.toml --tui

# Start specific servers only
rmcp-mux --config ~/.config/mcp-mux.toml --only supabase,filesystem

# Start all except specific servers
rmcp-mux --config ~/.config/mcp-mux.toml --except serena

# Show status
rmcp-mux --config ~/.config/mcp-mux.toml --show-status

# Restart a specific server
rmcp-mux --config ~/.config/mcp-mux.toml --restart-service memory

# Get daemon status (JSON)
rmcp-mux daemon-status --json
```

## TUI Dashboard Controls

| Key | Action |
|-----|--------|
| `j` / `↓` | Move selection down |
| `k` / `↑` | Move selection up |
| `r` | Restart selected server |
| `s` | Stop selected server |
| `S` | Start selected server |
| `q` / `Esc` | Quit |

## Troubleshooting

### rmcp-mux not found

```bash
# Add to PATH if not already there
export PATH="$HOME/.local/bin:$PATH"

# Add to ~/.zshrc for persistence
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Socket connection errors

```bash
# Check if sockets exist
ls -la ~/.mcp-sockets/

# Check socket permissions
stat ~/.mcp-sockets/supabase.sock

# Remove stale sockets
rm -f ~/.mcp-sockets/*.sock
# Restart rmcp-mux
```

### MCP server won't start

```bash
# Check individual server logs
rmcp-mux --config ~/.config/mcp-mux.toml --show-status

# Test server manually
node ~/.npm-global/bin/mcp-server-supabase --project-ref avdgyrepwrvsvwgxrccr

# Check for port conflicts
lsof -i :8000
```

### High memory usage

```bash
# Check active clients per server
rmcp-mux daemon-status

# Reduce max_active_clients in config
# Edit ~/.config/mcp-mux.toml and set max_active_clients = 5
```

## Performance Monitoring

### Monitor resource usage:

```bash
# Check rmcp-mux resource usage
ps aux | grep rmcp-mux

# Check all MCP processes
ps aux | grep mcp-server

# Count total MCP processes (should be ~5-6)
ps aux | grep mcp-server | wc -l
```

### Expected resource usage:

```
rmcp-mux daemon:     ~50 MB
Supabase server:     ~100 MB
Filesystem server:   ~80 MB
Memory server:       ~60 MB
Serena server:       ~100 MB
────────────────────────────
Total:              ~390 MB (vs 2.13 GB before)
```

## Maintenance

### Update rmcp-mux:

```bash
# Reinstall latest version
curl -fsSL https://raw.githubusercontent.com/Loctree/rmcp-mux/main/tools/install.sh | sh

# Or build from source
cd ~/.local/share/rmcp-mux
git pull
cargo install --path .
```

### Clean up old MCP processes:

```bash
# Kill orphaned MCP processes
cleanup-agents

# Or manually
pkill -f mcp-server

# Then restart rmcp-mux
launchctl kickstart -k gui/$(id -u)/com.rmcp-mux
```

### View logs:

```bash
# View rmcp-mux logs
tail -f /tmp/rmcp-mux.log

# View specific server logs
rmcp-mux --config ~/.config/mcp-mux.toml --show-status | jq '.servers.supabase.logs'
```

## Integration with Railway

For cloud-hosted MCPs (via Railway), add them directly to Claude config:

```json
{
  "mcpServers": {
    "supabase": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "~/.mcp-sockets/supabase.sock"]
    },
    "railway-custom": {
      "url": "https://your-mcp.railway.app/sse",
      "transport": "sse"
    }
  }
}
```

Railway-hosted MCPs don't need multiplexing since they're already shared via HTTP.

## Next Steps

1. ✅ Install rmcp-mux
2. ✅ Configure multiplexer
3. ✅ Update Claude Desktop config
4. ✅ Start daemon
5. ✅ Verify connections
6. ✅ Test with Claude

## Resources

- [rmcp-mux GitHub](https://github.com/VetCoders/rmcp-mux)
- [rmcp-mux Documentation](https://github.com/VetCoders/rmcp-mux/blob/main/README.md)
- [MCP Protocol Specs](https://modelcontextprotocol.io/)
- [Blackbox5 MCP Strategy](./MCP-STRATEGY-WITH-RAILWAY.md)

## Support

For issues or questions:
- Check logs: `tail -f /tmp/rmcp-mux.log`
- Run diagnostics: `rmcp-mux --config ~/.config/mcp-mux.toml --show-status`
- Review TUI dashboard: `rmcp-mux --config ~/.config/mcp-mux.toml --tui`
