# How rmcp-mux Works & Connecting to Claude

## How rmcp-mux Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     rmcp-mux (Single Process)                   │
│                                                                  │
│  Manages 4 MCP servers:                                         │
│  ├─ filesystem → /tmp/mcp-fs.sock                              │
│  ├─ memory → /tmp/mcp-memory.sock                               │
│  ├─ serena → /tmp/mcp-serena.sock                               │
│  └─ supabase → /tmp/mcp-supabase.sock                          │
│                                                                  │
│  Each MCP gets:                                                 │
│  • Unix socket for fast IPC                                     │
│  • Auto-restart on failure                                      │
│  • Health monitoring (heartbeat)                                │
│  • Max 5 concurrent clients                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## How Claude Connects

There are **3 ways** to connect Claude to rmcp-mux:

---

## Option 1: Via rmcp-mux-proxy (RECOMMENDED)

**Each MCP connects individually via the proxy binary**

### How It Works

```
Claude Desktop → rmcp-mux-proxy → Unix Socket → MCP Server
```

The proxy translates stdio (what Claude expects) to Unix socket (what rmcp-mux provides).

### Claude Desktop Config

Update `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "/tmp/mcp-fs.sock"]
    },
    "memory": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "/tmp/mcp-memory.sock"]
    },
    "serena": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "/tmp/mcp-serena.sock"]
    },
    "supabase": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "/tmp/mcp-supabase.sock"]
    }
  }
}
```

### Pros/Cons

| Pros | Cons |
|------|------|
| ✅ Familiar Claude config | ❌ Still 4 MCP entries |
| ✅ Each MCP independent | ❌ More config entries |
| ✅ Can restart individual MCPs | ❌ Higher token usage |

---

## Option 2: Single Gateway (Best for Tokens)

**One gateway connects to all MCPs internally**

This is what we designed earlier in `HYBRID-MCP-ARCHITECTURE.md` - build a gateway that exposes all tools from all MCPs through a single endpoint.

### How It Works

```
Claude Desktop → Gateway → Routes to appropriate MCP
```

The gateway would:
1. Expose ONE MCP server to Claude
2. Receive tool calls
3. Route to the correct underlying MCP
4. Return result to Claude

### This Requires Building

We'd need to build a gateway service that:
- Connects to all 4 rmcp-mux sockets
- Implements MCP server protocol
- Exposes all tools from all MCPs
- Routes tool calls to correct MCP

**This is what Airis, IBM Context Forge, and Agent Gateway do.**

---

## Option 3: Use Airis Gateway (QUICKEST)

**Airis provides the gateway functionality already built**

### How It Works

```
Claude Desktop → Airis Gateway → Your MCPs (stdio or HTTP)
```

### Setup

```bash
# 1. Clone and start Airis
git clone https://github.com/agiletec-inc/airis-mcp-gateway.git
cd airis-mcp-gateway
docker compose up -d

# 2. Configure Airis to connect to your MCPs
# Edit docker-compose.yml to add your MCPs

# 3. Add to Claude
claude mcp add --scope user --transport sse airis-mcp-gateway http://localhost:9400/sse
```

### Pros/Cons

| Pros | Cons |
|------|------|
| ✅ ONE connection to Claude | ❌ Docker-based |
| ✅ 98% token reduction | ❌ Need to configure your MCPs |
| ✅ 60+ tools included | ❌ Extra layer |
| ✅ Already built | |

---

## Recommendation

### For Testing NOW: Use Option 1 (rmcp-mux-proxy)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "/tmp/mcp-fs.sock"]
    },
    "memory": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "/tmp/mcp-memory.sock"]
    },
    "serena": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "/tmp/mcp-serena.sock"]
    }
  }
}
```

This gets you working **right now** with rmcp-mux managing your MCPs.

### For Best Experience: Use Option 3 (Airis Gateway)

Airis provides:
- Single endpoint
- Lazy loading (98% token reduction)
- 60+ included tools
- Can add your custom MCPs

---

## Current Status

```
Server                State    Socket
────────────────────────────────────────────────────────────────
filesystem             ✓ UP     /tmp/mcp-fs.sock
memory                 ✓ UP     /tmp/mcp-memory.sock
serena                 ✓ UP     /tmp/mcp-serena.sock
supabase               ⚠ DOWN  /tmp/mcp-supabase.sock (needs SUPABASE_ACCESS_TOKEN)
```

### Fix Supabase

```bash
# Get your token from Supabase dashboard
export SUPABASE_ACCESS_TOKEN="your-token-here"

# Then restart supabase in rmcp-mux
rmcp-mux --config ~/.rmcp_servers/mux.toml --restart-service supabase
```

---

## Testing Connection

After updating Claude Desktop config:

1. Restart Claude Desktop
2. In a new chat, ask: "List all available tools"
3. You should see tools from filesystem, memory, and serena

---

## Files Created

| File | Purpose |
|------|---------|
| `~/bin/rmcp-mux` | Main multiplexer binary |
| `~/bin/rmcp-mux-proxy` | Proxy for stdio clients |
| `~/.rmcp_servers/mux.toml` | MCP configuration |
| `/tmp/rmcp-mux.log` | Runtime logs |
| `/tmp/rmcp-mux.status.sock` | Status queries |

---

Want me to update your Claude Desktop config with Option 1 (proxy) to test now?
