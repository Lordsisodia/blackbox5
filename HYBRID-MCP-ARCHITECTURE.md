# Blackbox5 Hybrid MCP Architecture: Local + Railway

## The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│                     Blackbox5 Startup                         │
├─────────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Blackbox5 starts                                         │
│  2. Auto-launches local MCPs:                              │
│     ├─ Filesystem (for /Users/shaansisodia)                  │
│     ├─ Supabase (local instance)                             │
│     ├─ Memory (session cache)                                │
│     └─ Serena (code search)                                  │
│  3. Connects to Railway Gateway:                             │
│     ├─ GitHub (repositories)                                 │
│     ├─ Slack (messaging)                                     │
│     ├─ Postgres (databases)                                  │
│     └─ Custom APIs (your services)                           │
│                                                              │
└─────────────────────────────────────────────────────────────────┘
```

## The Gateway Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MCP Gateway (Railway)                        │
│                                                              │
│  ONE Endpoint: https://your-gateway.railway.app/sse         │
│                                                              │
│  Internal Registry:                                         │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Local MCPs (managed by Blackbox5)                      │    │
│  │  • filesystem     → Unix socket                      │    │
│  │  • supabase       → Unix socket                      │    │
│  │  • memory         → Unix socket                      │    │
│  │  • serena         → Unix socket                      │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Railway MCPs (HTTP/SSE endpoints)                     │    │
│  │  • github         → https://github-mcp.railway.app    │    │
│  │  • slack           → https://slack-mcp.railway.app     │    │
│  │  • postgres        → https://postgres-mcp.railway.app  │    │
│  │  • custom-api     → https://api.railway.app          │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  Interchangeable:                                          │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ config.json can switch any MCP:                       │    │
│  │  • filesystem: local OR railway                        │    │
│  │  • supabase: local OR railway                          │    │
│  │  • All controlled via config, no code changes         │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────────┘
```

## Key Innovation: Smart Routing

The gateway intelligently routes to local OR Railway based on:

```javascript
// Gateway routing logic
function routeToMCP(toolName) {
  const config = loadConfig();  // Load from config.json

  // Check if MCP is local or Railway
  const mcpConfig = config.mcpServers[toolName];

  if (mcpConfig.type === "local") {
    // Route to local Unix socket
    return connectToUnixSocket(mcpConfig.socket);
  } else if (mcpConfig.type === "railway") {
    // Route to Railway HTTP endpoint
    return connectToHTTP(mcpConfig.url);
  } else if (mcpConfig.type === "auto") {
    // Smart routing: try local first, fallback to Railway
    if (isLocalAvailable(toolName)) {
      return connectToUnixSocket(mcpConfig.socket);
    } else {
      return connectToHTTP(mcpConfig.railwayUrl);
    }
  }
}
```

---

## Implementation Plan

### Layer 1: Blackbox5 Local MCP Auto-Start

Create `blackbox5-mcp-manager`:

```bash
#!/bin/bash
# ~/bin/blackbox5-mcp-manager
# Manages local MCPs for Blackbox5

MCP_DIR="$HOME/.mcp-sockets"
PID_FILE="$HOME/.blackbox5/mcp-pids.txt"

start_local_mcps() {
  echo "🚀 Starting Blackbox5 Local MCPs..."

  # Filesystem MCP
  node ~/.npm-global/bin/mcp-server-filesystem /Users/shaansisodia \
    > /tmp/mcp-filesystem.log 2>&1 &
  echo "filesystem:$!" >> "$PID_FILE"

  # Supabase MCP
  node ~/.npm-global/bin/mcp-server-supabase \
    --project-ref avdgyrepwrvsvwgxrccr \
    > /tmp/mcp-supabase.log 2>&1 &
  echo "supabase:$!" >> "$PID_FILE"

  # Memory MCP
  npx -y @modelcontextprotocol/server-memory \
    > /tmp/mcp-memory.log 2>&1 &
  echo "memory:$!" >> "$PID_FILE"

  # Serena MCP
  uv serena-mcp-server \
    > /tmp/mcp-serena.log 2>&1 &
  echo "serena:$!" >> "$PID_FILE"

  echo "✅ Local MCPs started"
  echo "   PIDs saved to: $PID_FILE"
}

stop_local_mcps() {
  echo "🛑 Stopping Blackbox5 Local MCPs..."

  if [[ -f "$PID_FILE" ]]; then
    while IFS=: read -r name pid; do
      kill "$pid" 2>/dev/null
    done < "$PID_FILE"
    rm -f "$PID_FILE"
  fi

  # Also kill any stray processes
  pkill -f "mcp-server-filesystem" 2>/dev/null
  pkill -f "mcp-server-supabase" 2>/dev/null
  pkill -f "server-memory" 2>/dev/null
  pkill -f "serena-mcp-server" 2>/dev/null

  echo "✅ Local MCPs stopped"
}

status_mcps() {
  echo "📊 Blackbox5 MCP Status:"
  echo "   Local MCPs:"

  if [[ -f "$PID_FILE" ]]; then
    while IFS=: read -r name pid; do
      if ps -p "$pid" > /dev/null 2>&1; then
        echo "      ✅ $name (PID: $pid)"
      else
        echo "      ❌ $name (dead)"
      fi
    done < "$PID_FILE"
  else
    echo "      ⚪  No local MCPs running"
  fi
}

case "${1:-}" in
  start) start_local_mcps ;;
  stop) stop_local_mcps ;;
  status) status_mcps ;;
  restart)
    stop_local_mcps
    sleep 1
    start_local_mcps
    ;;
  *)
    echo "Usage: $0 {start|stop|status|restart}"
    exit 1
    ;;
esac
```

### Layer 2: Railway Gateway Configuration

Create `gateway-config.json`:

```json
{
  "gatewayName": "blackbox5-mcp-gateway",
  "version": "1.0",

  "mcpServers": {
    // LOCAL MCPs (run by Blackbox5)
    "filesystem": {
      "type": "local",
      "socket": "~/.mcp-sockets/filesystem.sock",
      "railwayFallback": "https://filesystem-mcp.railway.app"
    },

    "supabase": {
      "type": "local",
      "socket": "~/.mcp-sockets/supabase.sock",
      "railwayFallback": null  // No fallback, local only
    },

    "memory": {
      "type": "local",
      "socket": "~/.mcp-sockets/memory.sock",
      "railwayFallback": "https://memory-mcp.railway.app"
    },

    "serena": {
      "type": "local",
      "socket": "~/.mcp-sockets/serena.sock",
      "railwayFallback": null
    },

    // RAILWAY MCPs (cloud-hosted)
    "github": {
      "type": "railway",
      "url": "https://github-mcp.railway.app/sse",
      "localFallback": null  // Railway only
    },

    "slack": {
      "type": "railway",
      "url": "https://slack-mcp.railway.app/sse",
      "localFallback": null
    },

    "postgres": {
      "type": "railway",
      "url": "https://postgres-mcp.railway.app/sse",
      "localFallback": null
    },

    // INTERCHANGEABLE (can switch between local/Railway)
    "database": {
      "type": "auto",
      "local": {
        "socket": "~/.mcp-sockets/postgres.sock"
      },
      "railway": {
        "url": "https://postgres-mcp.railway.app/sse"
      }
    },

    "analytics": {
      "type": "auto",
      "local": {
        "socket": "~/.mcp-sockets/analytics.sock"
      },
      "railway": {
        "url": "https://analytics-mcp.railway.app/sse"
      }
    }
  },

  "toolRegistry": {
    "enabled": true,
    "lazyLoading": true,
    "cacheDuration": "session"
  },

  "monitoring": {
    "enabled": true,
    "logLevel": "info"
  }
}
```

### Layer 3: Gateway Implementation (Deploy to Railway)

```javascript
// gateway/index.js (deployed to Railway)
const express = require('express');
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { SSEServerTransport } = require('@modelcontextprotocol/sdk/server/sse.js');

const app = express();
const config = require('./gateway-config.json');

class HybridMCPGateway {
  constructor() {
    this.localConnections = new Map();
    this.toolRegistry = new Map();
    this.loadedTools = new Map();
  }

  async initialize() {
    // Connect to local Unix sockets
    await this.connectToLocalMCPs();

    // Register Railway MCPs
    this.registerRailwayMCPs();

    // Start SSE server
    this.startSSEServer();
  }

  async connectToLocalMCPs() {
    const localMCPs = Object.entries(config.mcpServers)
      .filter(([_, cfg]) => cfg.type === 'local' || cfg.type === 'auto')
      .filter(([_, cfg]) => cfg.socket)
      .map(([name, cfg]) => [name, this.expandPath(cfg.socket)]);

    for (const [name, socketPath] of localMCPs) {
      try {
        const client = await this.connectToUnixSocket(socketPath);
        this.localConnections.set(name, client);
        console.log(`✅ Connected to local MCP: ${name}`);

        // Register tools from this MCP
        await this.registerTools(name, client);
      } catch (error) {
        console.warn(`⚠️  Failed to connect to ${name}:`, error.message);

        // Check if railway fallback exists
        if (config.mcpServers[name]?.railwayFallback) {
          console.log(`   ↳ Using Railway fallback for ${name}`);
          await this.connectToRailwayMCP(name, config.mcpServers[name].railwayFallback);
        }
      }
    }
  }

  async connectToUnixSocket(socketPath) {
    // Implementation for Unix socket connection
    // Returns MCP client
  }

  async registerTools(mcpName, client) {
    // Get tool list from MCP
    const tools = await client.listTools();

    // Store in registry (metadata only, not full definitions)
    this.toolRegistry.set(mcpName, tools.map(t => ({
      name: `${mcpName}:${t.name}`,
      description: t.description,
      mcp: mcpName
    })));
  }

  async loadTool(toolName) {
    // Check if already loaded
    if (this.loadedTools.has(toolName)) {
      return this.loadedTools.get(toolName);
    }

    // Parse: "mcp:tool"
    const [mcpName, tool] = toolName.split(':');

    // Load from local or Railway
    const toolDef = await this.fetchToolDefinition(mcpName, tool);

    // Cache it
    this.loadedTools.set(toolName, toolDef);

    return toolDef;
  }

  async fetchToolDefinition(mcpName, tool) {
    const mcpConfig = config.mcpServers[mcpName];

    if (mcpConfig.type === 'local' || mcpConfig.type === 'auto') {
      // Try local first
      if (this.localConnections.has(mcpName)) {
        return await this.localConnections.get(mcpName).getToolDefinition(tool);
      }

      // Fallback to Railway if configured
      if (mcpConfig.railwayFallback) {
        return await this.fetchFromRailway(mcpConfig.railwayFallback, tool);
      }
    }

    if (mcpConfig.type === 'railway') {
      return await this.fetchFromRailway(mcpConfig.url, tool);
    }
  }

  getToolRegistry() {
    // Return ONLY tool metadata (not full definitions)
    // This is the key to saving context!
    return Array.from(this.toolRegistry.values()).map(tool => ({
      name: tool.name,
      description: tool.description,
      mcp: tool.mcp
    }));
  }
}

// Start gateway
const gateway = new HybridMCPGateway();
gateway.initialize().then(() => {
  console.log('🚀 Blackbox5 MCP Gateway ready!');
  console.log('   Local MCPs:', Object.keys(config.mcpServers).filter(k =>
    config.mcpServers[k].type === 'local'
  ));
  console.log('   Railway MCPs:', Object.keys(config.mcpServers).filter(k =>
    config.mcpServers[k].type === 'railway'
  ));
});
```

---

## Blackbox5 Integration

### Add to Blackbox5 Startup Script:

```bash
#!/bin/bash
# blackbox5-start.sh

echo "🚀 Starting Blackbox5..."

# 1. Start local MCPs
~/bin/blackbox5-mcp-manager start

# 2. Start Blackbox5 services
./start.sh --api-only

# 3. Connect to Railway Gateway
# (Auto-connects to https://your-gateway.railway.app)

echo "✅ Blackbox5 ready!"
echo "   Local MCPs: 4"
echo "   Railway MCPs: 3+ (via gateway)"
echo "   Total available: 7+ MCPs"
```

### Add to Blackbox5 Shutdown Script:

```bash
#!/bin/bash
# blackbox5-stop.sh

echo "🛑 Stopping Blackbox5..."

# 1. Stop local MCPs
~/bin/blackbox5-mcp-manager stop

# 2. Stop Blackbox5 services
pkill -f "blackbox"

echo "✅ Blackbox5 stopped"
```

---

## Configuration: Interchangeable MCPs

### Scenario 1: Run Supabase Locally

```json
{
  "mcpServers": {
    "supabase": {
      "type": "local",
      "socket": "~/.mcp-sockets/supabase.sock"
    }
  }
}
```

### Scenario 2: Switch Supabase to Railway

```json
{
  "mcpServers": {
    "supabase": {
      "type": "railway",
      "url": "https://supabase-mcp.railway.app/sse"
    }
  }
}
```

**No code changes - just config!**

---

## Auto-Switching / Failover

```json
{
  "mcpServers": {
    "supabase": {
      "type": "auto",
      "local": {
        "socket": "~/.mcp-sockets/supabase.sock",
        "priority": 1
      },
      "railway": {
        "url": "https://supabase-mcp.railway.app/sse",
        "priority": 2
      },
      "healthCheck": {
        "endpoint": "/health",
        "interval": 30000
      }
    }
  }
}
```

**Behavior:**
- Always tries local first (faster)
- Falls back to Railway if local fails
- Auto-switches back when local recovers

---

## Railway Deployment

### Deploy Gateway to Railway:

```bash
# 1. Create Railway project
railway new

# 2. Deploy gateway
cd gateway
railway up

# 3. Get URL
railway domain

# 4. Update Claude config
```

### Railway Services Structure:

```
your-blackbox5-gateway.railway.app
├─ gateway/           ← Main gateway service
├─ filesystem-mcp/   ← Optional: Filesystem as Railway fallback
├─ github-mcp/       ← GitHub integration
├─ slack-mcp/        ← Slack integration
└─ postgres-mcp/     ← PostgreSQL integration
```

---

## Usage in Claude

### Initial Setup (One-time):

```json
{
  "mcpServers": {
    "blackbox5": {
      "url": "https://your-blackbox5-gateway.railway.app/sse",
      "transport": "sse"
    }
  }
}
```

### Then Use Any Tool:

```
User: "Read the file /Users/shaansisodia/test.txt"

Claude: (calls blackbox5.list_tools())
Gateway: Returns [
  {name: "filesystem:read", description: "..."},
  {name: "filesystem:write", description: "..."},
  {name: "github:get_repo", description: "..."},
  {name: "slack:send_message", description: "..."},
  ...
]

Claude: (calls blackbox5.load_tool("filesystem:read"))
Gateway: Loads ONLY filesystem:read tool
Claude: Now uses the tool
```

---

## Token Impact

### Configuration 1: All Local MCPs
```
Gateway: ~100 tokens
Local MCPs connect overhead: ~200 tokens
Total startup: ~300 tokens
```

### Configuration 2: Mix Local + Railway
```
Gateway: ~100 tokens
Local MCPs: ~200 tokens
Railway ready: ~0 (already running)
Total startup: ~300 tokens
```

### Current Way:
```
All MCP tools loaded: ~8,000 tokens
```

### Savings: **96% reduction!**

---

## Benefits

### 1. **Interchangeable**
```
Switch local ↔ Railway via config change
No code changes required
Auto-failover when local fails
```

### 2. **Auto-Start**
```
Blackbox5 starts → local MCPs start automatically
Gateway connects automatically
Railway MCPs already running
```

### 3. **Minimal Context**
```
Startup: ~300 tokens (vs 8,000 current)
Per-tool: ~200 tokens (only when used)
```

### 4. **Scalable**
```
Add 50 MCPs? No problem.
Context still ~300 tokens at startup.
```

### 5. **Reliable**
```
Local fails? Railway fallback.
Railway down? Local fallback.
Best of both worlds.
```

---

## Implementation Checklist

- [ ] Create `blackbox5-mcp-manager` script
- [ ] Create `gateway-config.json`
- [ ] Build gateway service
- [ ] Deploy gateway to Railway
- [ ] Update Blackbox5 startup/shutdown scripts
- [ ] Update Claude Desktop config
- [ ] Test local MCPs
- [ ] Test Railway MCPs
- [ ] Test failover
- [ ] Test tool loading
- [ ] Monitor token usage
