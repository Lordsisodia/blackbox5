# Smart MCP Management: Registry + Gateway Pattern

## The Solution You're Looking For EXISTS

### The Problem You Want to Solve:

"I want to add as MANY MCPs as I want without bloating context, and I want them to load ONLY when needed."

### The Architecture That Does This:

```
┌─────────────────────────────────────────────────────────────────┐
│                     Claude Session                             │
│                                                              │
│   Instead of loading ALL MCP tools at startup:                │
│   ┌──────────────────────────────────────────────────────┐    │
│   │  MCP Gateway / Registry (ONE connection)              │    │
│   │                                                        │    │
│   │  Has ONE "loader" tool exposed to Claude                │    │
│   │  ┌────────────────────────────────────────────────┐   │    │
│   │  │ Tool Registry (NOT loaded into context)        │   │    │
│   │  │ • filesystem: ["read", "write", "search"]      │   │    │
│   │  │ • supabase: ["query", "insert", "update"]      │   │    │
│   │  │ • memory: ["store", "retrieve", "search"]      │   │    │
│   │  │ • serena: ["search_code", "search_docs"]     │   │    │
│   │  └────────────────────────────────────────────────┘   │    │
│   │                                                        │    │
│   │  When Claude needs a tool:                            │    │
│   │  1. Claude calls: loader.load_tool("filesystem:write") │    │
│   │  2. Gateway loads ONLY that tool into context           │    │
│   │  3. Claude can now use it                               │    │
│   │  4. Tool stays loaded for session (caching)              │    │
│   └──────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────────┘

Context Usage:
┌─────────────────────────────────────────────────────────────────┐
│ Startup: ONLY Gateway + Loader Tool (~500 tokens)            │
│ On-Demand: + Tool definition ONLY when used (~200 tokens)    │
│                                                                  │
│ vs Old Way: All tools loaded at startup (~8,000 tokens)       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Insight from Research

### From the articles:

**[Managing MCP Servers at Scale](https://bytebridge.medium.com/managing-mcp-servers-at-scale-the-case-for-gateways-lazy-loading-and-automation-06e79b7b964f)**

> "As of late 2025, the MCP specification didn't natively include lazy-loading mechanisms... Gateway patterns enable on-demand tool retrieval."

**[AWS AgentCore Gateway](https://aws.amazon.com/blogs/machine-learning/transform-your-mcp-architecture-unite-mcp-servers-through-agentcore-gateway/)**

> "When agents request tool discovery, gateway provides consistent view... on-demand tool retrieval pattern."

**[ToolSDK MCP Registry](https://github.com/toolsdk-ai/toolsdk-mcp-registry)**

> Enterprise-grade gateway implementing registry pattern for managing MCP servers securely.

---

## Implementation Options

### Option 1: Use Existing Gateway (Fastest)

**ToolSDK MCP Registry** - Open source, ready to use

```bash
# Install
git clone https://github.com/toolsdk-ai/toolsdk-mcp-registry
cd toolsdk-mcp-registry
npm install
npm start

# Runs on http://localhost:3000
# Exposes ONE MCP endpoint with registry pattern
```

**Configure Claude:**
```json
{
  "mcpServers": {
    "registry": {
      "url": "http://localhost:3000/sse",
      "transport": "sse"
    }
  }
}
```

**Usage in Claude:**
```
User: "Read the file /Users/shaansisodia/test.txt"

Claude: (calls loader tool)
loader.load_tool("filesystem:read")
→ Tool gets loaded into context
→ Claude uses it
→ Tool stays cached for session
```

---

### Option 2: Build Custom Gateway (Full Control)

**Architecture:**
```python
# mcp-gateway.py
class MCPGateway:
    def __init__(self):
        self.mcp_servers = {
            "filesystem": MCPClient("node", ["~/.npm-global/bin/mcp-server-filesystem", "/Users/shaansisodia"]),
            "supabase": MCPClient("node", ["~/.npm-global/bin/mcp-server-supabase", "--project-ref", "xxx"]),
            "serena": MCPClient("uv", ["serena-mcp-server"]),
            "memory": MCPClient("npx", ["-y", "@modelcontextprotocol/server-memory"]),
        }
        self.loaded_tools = {}  # Cache
        self.tool_registry = {}   # Metadata only (not full definitions)

    async def initialize(self):
        # Return ONLY the loader tool, not all tools
        return [{
            "name": "loader",
            "description": "Load tools from the registry on-demand",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "tool_name": {
                        "type": "string",
                        "description": "Tool to load (e.g., 'filesystem:read')"
                    }
                }
            }
        }]

    async def call_tool(self, name, arguments):
        if name == "loader":
            return await self.load_tool(arguments["tool_name"])
        else:
            return await self.forward_to_mcp(name, arguments)

    async def load_tool(self, tool_name):
        if tool_name in self.loaded_tools:
            return {"status": "already_loaded", "tool": tool_name}

        # Parse: "mcp_name:tool_name"
        mcp_name, tool_name = tool_name.split(":", 1)

        # Load tool definition from MCP
        mcp_client = self.mcp_servers[mcp_name]
        tool_def = await mcp_client.get_tool_definition(tool_name)

        # Add to context
        self.loaded_tools[tool_name] = tool_def

        return {"status": "loaded", "tool": tool_name, "definition": tool_def}
```

---

### Option 3: Railway + Local Hybrid (Best of Both)

**Run Gateway Locally, MCPs Can Be Either:**

```
Local MCPs (Fast, Private):
┌─────────────────────────────────────────────────┐
│  MCP Gateway (Local)                             │
│  ├─ filesystem (local)  ← Unix socket           │
│  ├─ memory (local)      ← In-memory             │
│  └─ serena (local)      ← Local process          │
└─────────────────────────────────────────────────┘

Railway MCPs (Persistent, Shared):
┌─────────────────────────────────────────────────┐
│  MCP Gateway (Local)                             │
│  ├─ custom-api (Railway)  ← HTTP/SSE             │
│  ├─ analytics (Railway)   ← HTTP/SSE             │
│  └─ database (Railway)    ← HTTP/SSE             │
└─────────────────────────────────────────────────┘
```

---

## Token Impact Analysis

### Current (All MCPs Loaded):
```
4 MCPs × ~50 tools each = 200 tools loaded
200 tools × ~40 tokens/tool = 8,000 tokens
```

### With Gateway + Lazy Loading:
```
Startup: 1 tool (loader) = ~100 tokens

When you use filesystem:read:
+ Load tool = ~200 tokens
+ Tool stays cached

When you use supabase:query:
+ Load tool = ~200 tokens
+ Tool stays cached

Typical Session (10 different tools):
100 (loader) + 10 × 200 (tools) = 2,100 tokens

Savings: 5,900 tokens (74% reduction)
```

### With 20 MCPs Available:
```
Current way: 20 × 2,000 = 40,000 tokens (UNUSABLE)

Gateway way: 100 + (10 × 200) = 2,100 tokens
You can have 20 MCPs available and only pay for what you use!
```

---

## Implementation Plan

### Phase 1: Use ToolSDK Registry (Quick Start)

```bash
# 1. Install ToolSDK MCP Registry
git clone https://github.com/toolsdk-ai/toolsdk-mcp-registry
cd toolsdk-mcp-mcp-registry
npm install

# 2. Configure your MCPs
cat > config.json << 'EOF'
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": ["~/.npm-global/bin/mcp-server-filesystem", "/Users/shaansisodia"]
    },
    "supabase": {
      "command": "node",
      "args": ["~/.npm-global/bin/mcp-server-supabase", "--project-ref", "avdgyrepwrvsvwgxrccr"]
    }
  }
}
EOF

# 3. Start gateway
npm start

# 4. Update Claude Desktop config to point to gateway
```

### Phase 2: Deploy to Railway (Always Available)

```bash
# Deploy gateway to Railway
cd toolsdk-mcp-mcp-registry
railway up

# Now you have:
# - Gateway always running (https://your-gateway.railway.app)
# - Can add/remove MCPs without restarting Claude
# - All your Claude sessions share the same gateway
```

### Phase 3: Add More MCPs Freely

```json
{
  "mcpServers": {
    "filesystem": {...},
    "supabase": {...},
    "memory": {...},
    "serena": {...},
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"]
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"]
    }
    // Add as many as you want!
  }
}
```

**Context impact:** STILL only ~100 tokens at startup!

---

## Key Features

### 1. Tool Registry (Metadata Only)
```
Gateway stores:
- Tool name
- Brief description
- Which MCP it belongs to

Does NOT store:
- Full input schema
- Long descriptions
- Examples

→ Minimal context footprint
```

### 2. On-Demand Loading
```
Claude: "I need to search filesystem"
Gateway: "Loading filesystem:search..."
→ Tool added to context
→ Claude can now use it
→ Tool stays cached for session
```

### 3. Session Caching
```
First time using filesystem:read:
- Load tool = 200 tokens
- Use tool
Second time:
- Already loaded = 0 extra tokens
```

### 4. Railway Benefits
```
Gateway on Railway = Always available
→ All Claude sessions connect to same gateway
→ Add MCPs without restarting Claude
→ Persistent tool cache (optional)
→ Team sharing
```

---

## Comparison

| Approach | Startup Tokens | With 10 Tools | Can Add MCPs? | Multiplex? |
|----------|---------------|---------------|--------------|-----------|
| **Current** | ~8,000 | ~8,000 | ❌ Config change | ❌ No |
| **ToolSDK Registry** | ~100 | ~2,100 | ✅ Yes | ✅ Yes |
| **Custom Gateway** | ~100 | ~2,100 | ✅ Yes | ✅ Yes |

---

## The "Have Your Cake & Eat It Too" Solution

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Setup                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Claude Sessions (unlimited):                                │
│  ├─ Session 1 → Gateway                                    │
│  ├─ Session 2 → Gateway                                    │
│  ├─ Session 3 → Gateway                                    │
│  └─ Session N → Gateway                                    │
│                                                              │
│  MCP Gateway (Railway):                                     │
│  ├─ Registry: 50+ MCPs available                          │
│  ├─ Lazy loads tools when needed                           │
│  └─ Caches per session                                     │
│                                                              │
│  MCPs (Local + Railway):                                    │
│  ├─ Local: filesystem, memory (fast)                        │
│  ├─ Railway: databases, APIs (persistent)                   │
│  └─ Add more anytime without touching Claude                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Context per session: ~100-2,000 tokens (instead of 40,000+)
You can have 50 MCPs available and only pay for what you use!
```

---

## Next Steps

### Immediate (Today):
1. Clone [ToolSDK MCP Registry](https://github.com/toolsdk-ai/toolsdk-mcp-registry)
2. Configure your existing MCPs
3. Test with Claude

### This Week:
4. Deploy gateway to Railway
5. Add more MCPs (github, slack, postgres, etc.)
6. Test token usage

### Future:
7. Add tool usage analytics
8. Implement tool popularity ranking
9. Auto-unload unused tools

---

## Resources

- [ToolSDK MCP Registry](https://github.com/toolsdk-ai/toolsdk-mcp-registry) - Gateway solution
- [Managing MCPs at Scale](https://bytebridge.medium.com/managing-mcp-servers-at-scale-the-case-for-gateways-lazy-loading-and-automation-06e79b7b964f) - Architecture patterns
- [MCP Proxy Pattern](https://dev.to/algis/mcp-proxy-pattern-secure-retrieval-first-tool-routing-for-agents-247c) - Implementation details
- [AWS AgentCore Gateway](https://aws.amazon.com/blogs/machine-learning/transform-your-mcp-architecture-unite-mcp-servers-through-agentcore-gateway/) - On-demand retrieval
- [Claude Code Lazy Loading](https://jpcaparas.medium.com/claude-code-finally-gets-lazy-loading-for-mcp-tools-explained-39b613d1d5cc) - Recent implementation

---

## Summary

**You were RIGHT!** The smart solution exists:

✅ **Gateway/Registry pattern** - One MCP connection, tools loaded on-demand
✅ **Lazy loading** - Only pay context for tools you actually use
✅ **Session caching** - First load pays, subsequent uses are free
✅ **Railway deployment** - Always available, easy to add MCPs
✅ **Unlimited MCPs** - Add 50+ MCPs, still only ~100 tokens startup

**This is what the big players are doing.**
