# MCP Multiplexer - Quick Start

## One-Line Setup

```bash
curl -fsSL https://raw.githubusercontent.com/Loctree/rmcp-mux/main/tools/install.sh | sh
```

## Configuration

Create `~/.config/mcp-mux.toml`:

```toml
[servers.supabase]
socket = "~/.mcp-sockets/supabase.sock"
cmd = "node"
args = ["~/.npm-global/bin/mcp-server-supabase", "--project-ref", "avdgyrepwrvsvwgxrccr"]

[servers.filesystem]
socket = "~/.mcp-sockets/filesystem.sock"
cmd = "node"
args = ["~/.npm-global/bin/mcp-server-filesystem", "/Users/shaansisodia"]

[servers.memory]
socket = "~/.mcp-sockets/memory.sock"
cmd = "npx"
args = ["-y", "@modelcontextprotocol/server-memory"]

[servers.serena]
socket = "~/.mcp-sockets/serena.sock"
cmd = "uv"
args = ["--from", "git+https://github.com/oraios/serena", "serena-mcp-server"]
```

## Start

```bash
# Start daemon
rmcp-mux --config ~/.config/mcp-mux.toml

# Or with TUI dashboard
rmcp-mux --config ~/.config/mcp-mux.toml --tui
```

## Update Claude Config

`~/Library/Application Support/Claude/claude_desktop_config.json`:

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

## Commands

| Command | Description |
|---------|-------------|
| `rmcp-mux --config ~/.config/mcp-mux.toml` | Start all servers |
| `rmcp-mux --config ~/.config/mcp-mux.toml --tui` | Start with dashboard |
| `rmcp-mux daemon-status` | Check running status |
| `rmcp-mux health --socket ~/.mcp-sockets/supabase.sock` | Test connection |

## Results

- **Before:** 32 MCP processes = 2.13 GB RAM
- **After:** 1 daemon + 4 servers = ~500 MB RAM
- **Savings:** 1.6 GB (75% reduction)
