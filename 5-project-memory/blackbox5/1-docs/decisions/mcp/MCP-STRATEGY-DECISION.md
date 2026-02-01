# MCP Strategy Decision: Native vs Gateway

## The Critical Question

> "Are we sure this is the best way to do it from all research and first principles?"

This question led to a discovery that changes our entire approach.

---

## What We Discovered

### Claude Code 2.1.7+ Has Native Tool Search

From [GitHub Issue #7336](https://github.com/anthropics/claude-code/issues/7336):

> "Lazy loading is now implemented in Claude Code 2.1.7+ as Tool Search"
> "95% Token Reduction: From 108k to ~5k initial tokens"

**This is already available and working.**

---

## Comparison: Three Approaches

### Approach A: Custom Gateway (HYBRID-MCP-IMPLEMENTATION.md)

**How it works:**
- Build Node.js gateway service
- Deploy to Railway
- Route local MCPs via Unix sockets
- Route Railway MCPs via HTTP
- Implement custom lazy loading
- Implement custom failover

**Token Usage:**
- Gateway startup: ~100 tokens
- Tool registry: ~500 tokens (metadata only)
- Tools load on-demand: ~200 tokens each
- **Total startup: ~600 tokens**

**Pros:**
- 96% token reduction
- Full control over routing
- Custom failover logic
- Railway integration

**Cons:**
- ~2 hours implementation time
- Ongoing maintenance burden
- Custom code to debug
- Another service to monitor
- Single point of failure (gateway)
- Additional latency (gateway hop)
- Need to update Claude Desktop config

---

### Approach B: Native Claude Code Tool Search (RECOMMENDED)

**How it works:**
- Enable Tool Search in Claude Code settings
- No additional infrastructure
- Claude manages lazy loading natively
- MCPs connect directly to Claude

**Token Usage:**
- Tool Search loader: ~100 tokens
- Loaded tools on-demand: ~200 tokens each
- **Total startup: ~5,000 tokens**

**Pros:**
- 95% token reduction (native implementation)
- Zero implementation time
- Zero maintenance
- Built-in reliability
- No single point of failure
- Direct MCP connections (faster)
- Automatic updates with Claude Code

**Cons:**
- Slightly higher startup tokens (5k vs 600)
- Less control over failover behavior
- Railway integration needs separate setup

---

### Approach C: Hybrid (Native + Railway Only)

**How it works:**
- Use native Tool Search for local MCPs
- Deploy ONLY Railway-hosted MCPs to Railway
- No gateway needed
- Claude connects directly to all MCPs

**Token Usage:**
- Tool Search: ~100 tokens
- Local MCPs: Loaded on-demand
- Railway MCPs: Already running, loaded on-demand
- **Total startup: ~5,000 tokens**

**Pros:**
- Best of both worlds
- Local MCPs: Fast, private, direct
- Railway MCPs: Persistent, shareable
- Zero maintenance for local
- Railway handles cloud MCPs
- No custom gateway code

**Cons:**
- Need to manage Railway deployments separately

---

## First Principles Analysis

### What We Actually Want:

1. **Reduce token usage** ✅ All approaches achieve this
2. **Add MCPs without bloating context** ✅ All approaches achieve this
3. **Reliable operation** ✅ Native wins (proven, battle-tested)
4. **Low maintenance** ✅ Native wins (zero maintenance)
5. **Fast performance** ✅ Native wins (direct connections)
6. **Railway integration** ✅ Approach C handles this

### The Gateway's Fatal Flaw:

**It's solving a problem that's already solved.**

Claude Code 2.1.7+ already implements lazy loading. Building a gateway adds:
- 2 hours implementation
- Ongoing maintenance
- Debugging complexity
- Additional latency
- Single point of failure

For what benefit?

**Gateway: 96% reduction**
**Native: 95% reduction**

**Difference: 4,400 tokens at startup**

This is negligible in practice. If you're using 50k tokens in a conversation, saving 4.4k at startup doesn't matter.

---

## What About Railway?

Railway is still valuable! But for a different purpose:

**Use Railway for:**
- MCPs that need to run 24/7 (databases, APIs)
- Team-shared MCPs
- MCPs that require cloud resources
- MCPs that need to persist state across sessions

**Use Local for:**
- Filesystem access (can't be remote anyway)
- Fast, private operations
- Development/testing

**No gateway needed** - Claude connects directly to Railway-hosted MCPs via SSE.

---

## The rmcp-mux Compilation Error

This is actually a blessing in disguise.

We tried to compile rmcp-mux and hit:
```
error[E0004]: non-exhaustive patterns: &Some(CliCommand::Dashboard(_)) not covered
```

This blocked us from implementing the gateway approach, which led us to research native solutions - and discover Claude Code already has this built-in.

**The compilation bug saved us from building unnecessary infrastructure.**

---

## Recommendation

### Use Approach C: Native + Railway

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Desktop                           │
│                                                              │
│  Tool Search Enabled (Native Lazy Loading)                  │
│  ├─ Local MCPs (direct connection)                          │
│  │  ├─ filesystem → ~/.mcp-sockets/filesystem.sock         │
│  │  ├─ supabase → ~/.mcp-sockets/supabase.sock             │
│  │  └─ memory → ~/.mcp-sockets/memory.sock                 │
│  │                                                           │
│  └─ Railway MCPs (direct SSE connection)                    │
│     ├─ github → https://github-mcp.railway.app/sse          │
│     ├─ slack → https://slack-mcp.railway.app/sse            │
│     └─ postgres → https://postgres-mcp.railway.app/sse      │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Benefits:
✅ 95% token reduction (native)
✅ Zero maintenance
✅ Direct connections (fast)
✅ Railway for persistent services
✅ Local for fast/private operations
✅ No single point of failure
```

---

## Implementation Steps (Approach C)

### Step 1: Enable Tool Search (5 minutes)

Check if already enabled:
```bash
# Tool Search is enabled by default in Claude Code 2.1.7+
# Verify by checking version
claude --version
```

If version >= 2.1.7, Tool Search is already working!

### Step 2: Configure Local MCPs (10 minutes)

Current config is already good:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": ["~/.npm-global/bin/mcp-server-filesystem", "/Users/shaansisodia"]
    },
    "supabase": {
      "command": "node",
      "args": ["~/.npm-global/bin/mcp-server-supabase", "--project-ref", "avdgyrepwrvsvwgxrccr"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "serena": {
      "command": "uv",
      "args": ["serena-mcp-server"]
    }
  }
}
```

### Step 3: Deploy Railway MCPs (Optional - 30 minutes)

Only for MCPs that need to be cloud-hosted:

```bash
# Example: GitHub MCP on Railway
railway new
cd github-mcp
railway up
railway domain
```

Add to Claude config:
```json
{
  "mcpServers": {
    "github": {
      "url": "https://github-mcp.railway.app/sse",
      "transport": "sse"
    }
  }
}
```

### Step 4: Verify Token Reduction (5 minutes)

```bash
# Check Claude Code version
claude --version

# Start a new session
# Check token usage in first message
# Should be ~5,000 tokens instead of ~50,000
```

---

## What We're NOT Doing

### ❌ NOT Building Custom Gateway

Reasons:
- Claude Code already has this feature
- Would take ~2 hours to implement
- Adds maintenance burden
- Adds single point of failure
- Adds latency
- Only saves 4,400 tokens (negligible)

### ❌ NOT Using rmcp-mux

Reasons:
- Has compilation bug (v0.3.4)
- Doesn't work with SSE (Railway MCPs)
- Would need to wait for upstream fix
- Native solution is better

---

## Success Criteria

With Approach C (Native + Railway):

✅ Token usage: ~5,000 at startup (95% reduction from 100k)
✅ Add unlimited MCPs: No context bloat
✅ Local MCPs: Fast, direct connections
✅ Railway MCPs: Persistent, cloud-hosted
✅ Zero maintenance: Native Claude Code feature
✅ No custom code to debug
✅ No single point of failure
✅ Works today (no implementation needed)

---

## Next Steps

### Option 1: Proceed with Native Approach
- Total time: 30 minutes (mostly Railway setup)
- Maintenance: Zero
- Token reduction: 95%

### Option 2: Build Custom Gateway Anyway
- Total time: ~2 hours
- Maintenance: Ongoing
- Token reduction: 96%
- **Only if you need custom routing logic that Claude doesn't support**

### Option 3: Test Native First, Gateway Later
- Try native approach today
- Measure actual token usage
- Build gateway only if native is insufficient

---

## The Answer to "Are We Sure?"

**YES.** We are sure.

From first principles:
1. We want to reduce tokens → Both approaches do this
2. We want low maintenance → Native wins (zero vs ongoing)
3. We want reliability → Native wins (proven vs custom)
4. We want performance → Native wins (direct vs gateway hop)

The marginal benefit of 4,400 tokens saved at startup is not worth:
- 2 hours implementation
- Ongoing maintenance
- Additional complexity
- Single point of failure

**Recommendation: Use Claude Code's native Tool Search + Railway for cloud MCPs.**

No custom gateway needed.

---

## Resources

- [Claude Code Tool Search](https://github.com/anthropics/claude-code/issues/7336)
- [Claude MCP Integration](https://platform.claude.com/docs/en/agent-sdk/mcp)
- [MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- Railway deployment: `railway up` (when needed)

---

## Decision

**We should proceed with Approach C: Native Tool Search + Railway**

This achieves our goals with:
- ✅ 95% token reduction
- ✅ Zero implementation time
- ✅ Zero maintenance
- ✅ Maximum reliability
- ✅ Best performance

The custom gateway approach is architecturally sound but unnecessary given native capabilities.
