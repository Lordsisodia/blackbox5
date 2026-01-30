# Blackbox5 Hybrid MCP Implementation Plan

## Overview
Build a hybrid MCP system where local MCPs auto-start with Blackbox5 and Railway MCPs are always available, all managed through a smart gateway that provides lazy loading and failover.

---

## Phase 1: Foundation (Local Setup)

### 1.1 Create Local MCP Manager
**File:** `~/bin/blackbox5-mcp-manager`
**Purpose:** Start/stop/status local MCPs as a unit

**Features:**
- Start all 4 local MCPs: filesystem, supabase, memory, serena
- Track PIDs in state file
- Health checking
- Graceful shutdown
- Status reporting

**Commands:** `start`, `stop`, `status`, `restart`

### 1.2 Create Gateway Configuration
**File:** `~/.config/blackbox5/gateway-config.json`
**Purpose:** Define which MCPs are local vs Railway

**Structure:**
- Local MCPs with Unix socket paths
- Railway MCPs with HTTP URLs
- Auto-switching configuration
- Failover rules

### 1.3 Integrate with Blackbox5 Startup
**Modify:** `blackbox5/start.sh`
**Changes:**
- Call `blackbox5-mcp-manager start` before starting services
- Call `blackbox5-mcp-manager stop` on shutdown
- Add status messages for clarity

**Files Created:**
- `~/bin/blackbox5-mcp-manager`
- `~/.config/blackbox5/gateway-config.json`
- Modified: `blackbox5/start.sh`

---

## Phase 2: Railway Gateway

### 2.1 Build Gateway Service
**Location:** `/tmp/blackbox5-mcp-gateway/`
**Technology:** Node.js + Express + MCP SDK

**Components:**
- Express server with SSE endpoint
- MCP client for local Unix sockets
- HTTP client for Railway MCPs
- Tool registry (metadata only)
- Lazy loading logic
- Failover handling

**Files Created:**
- `gateway/package.json`
- `gateway/index.js`
- `gateway/mcp-client.js`
- `gateway/config.js`
- `gateway/.railwayignore`

### 2.2 Gateway Configuration
**File:** `gateway/config.json`
**Purpose:** Runtime configuration for gateway

**Features:**
- Local MCP connection settings
- Railway MCP URLs
- Tool caching duration
- Health check intervals
- Logging configuration

### 2.3 Deploy to Railway
**Process:**
1. Create Railway project: `railway new`
2. Link local directory: `railway link`
3. Deploy: `railway up`
4. Get domain: `railway domain`

**Expected Output:**
- Gateway URL: `https://blackbox5-gateway.railway.app`
- SSE endpoint: `https://blackbox5-gateway.railway.app/sse`

**Files Created:**
- Deployed Railway service
- `gateway/README.railway`

---

## Phase 3: Testing

### 3.1 Test Local MCP Manager
**Command:** `~/bin/blackbox5-mcp-manager status`

**Verify:**
- All 4 MCPs start correctly
- PID tracking works
- Logs are being written
- Status command shows correct state

**Expected Output:**
```
📊 Blackbox5 MCP Status:
   Local MCPs:
      ✅ filesystem (PID: 12345)
      ✅ supabase (PID: 12346)
      ✅ memory (PID: 12347)
      ✅ serena (PID: 12348)
```

### 3.2 Verify Gateway Connectivity
**Test:** `curl https://blackbox5-gateway.railway.app/health`

**Verify:**
- Gateway responds to health checks
- Local MCPs are connected
- Railway MCPs are registered
- Tool registry is accessible

**Expected Output:**
```json
{
  "status": "healthy",
  "localMCPs": ["filesystem", "supabase", "memory", "serena"],
  "railwayMCPs": ["github", "slack", "postgres"],
  "toolRegistrySize": 50
}
```

### 3.3 Test Tool Loading
**Test:** Connect via Claude Desktop, call `list_tools`

**Verify:**
- Only registry metadata is returned initially (~100 tokens)
- Tools can be loaded on-demand
- Loaded tools are cached
- Multiple sessions share tools

**Test Procedure:**
1. Start Claude Desktop
2. Send: `list_tools`
3. Verify tool list has metadata only
4. Use a tool (e.g., `filesystem:read`)
5. Verify tool loads and works

### 3.4 Test Failover
**Test:** Stop local MCP, verify Railway fallback

**Test Procedure:**
1. Start all systems
2. Use a local MCP tool (works)
3. Kill local MCP: `~/bin/blackbox5-mcp-manager stop`
4. Use the tool again (should auto-switch to Railway)
5. Restart local MCP
6. Use tool again (should switch back to local)

**Expected Behavior:**
- Seamless switching without errors
- User sees no interruption
- Gateway logs show fallback occurred

---

## Phase 4: Claude Desktop Integration

### 4.1 Update Claude Desktop Config
**File:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Change:** Replace all MCP server configs with single gateway:

**Before:**
```json
{
  "mcpServers": {
    "supabase": {"command": "node", "args": [...]},
    "filesystem": {"command": "node", "args": [...]},
    "memory": {"command": "npx", "args": [...]},
    "serena": {"command": "uv", "args": [...]}
  }
}
```

**After:**
```json
{
  "mcpServers": {
    "blackbox5": {
      "url": "https://blackbox5-gateway.railway.app/sse",
      "transport": "sse"
    }
  }
}
```

### 4.2 Test with Real Claude Session
**Procedure:**
1. Restart Claude Desktop
2. Start new chat
3. Test tool access
4. Verify tool loading works
5. Check token usage (if available)

**Success Criteria:**
- Claude connects to gateway successfully
- Tools are discoverable
- Tools can be invoked
- No errors in Claude Desktop logs

---

## Phase 5: Validation

### 5.1 Measure Token Usage
**Method:** Compare token usage before/after

**Before (Current):**
```
MCP tools loaded: ~8,000 tokens
System prompt: ~3,000 tokens
Total: ~11,000 tokens before conversation
```

**After (Gateway):**
```
Gateway loader: ~100 tokens
Tool registry: ~500 tokens (metadata only)
Total: ~600 tokens before conversation
```

**Expected Savings:** ~10,400 tokens (95% reduction in MCP overhead)

### 5.2 Verify Context Savings
**Test:** Use 10 different tools across 20 messages

**Measure:**
- Context size with current setup
- Context size with gateway
- Tool loading performance

**Success Criteria:**
- Gateway uses <5k tokens total for MCPs
- Tools load in <500ms each
- No degradation in tool functionality

---

## Implementation Order

### Step 1: Local MCP Manager (15 min)
```bash
# Create the script
# Make executable
# Test start/stop/status
```

### Step 2: Gateway Service (45 min)
```bash
# Create Node.js gateway
# Implement routing logic
# Add tool registry
# Test locally
# Deploy to Railway
```

### Step 3: Integration (15 min)
```bash
# Update start.sh
# Update Claude config
# Test startup sequence
```

### Step 4: Testing (30 min)
```bash
# Test local MCPs
# Test gateway
# Test failover
# Test with Claude
```

### Step 5: Validation (15 min)
```bash
# Measure tokens
# Verify savings
# Document results
```

**Total Time: ~2 hours**

---

## Success Criteria

✅ Local MCPs auto-start with Blackbox5
✅ Railway MCPs always available
✅ Gateway accessible via single SSE endpoint
✅ Tools lazy-load on demand
✅ Failover works seamlessly
✅ Token usage < 1k for MCPs at startup
✅ All 4 local + 3+ Railway MCPs work
✅ Can add more MCPs without touching Claude config

---

## Rollback Plan

If anything fails:
1. Revert `start.sh` changes
2. Restore Claude Desktop config from backup
3. Stop Railway service
4. Keep local MCP manager as standalone tool

**Rollback command:**
```bash
git checkout start.sh
cp ~/Library/Application\ Support/Claude/claude_desktop_config.json.backup ~/Library/Application\ Support/Claude/claude_desktop_config.json
railway down
```

---

## Files Created/Modified

### New Files:
- `~/bin/blackbox5-mcp-manager`
- `~/.config/blackbox5/gateway-config.json`
- `/tmp/blackbox5-mcp-gateway/` (gateway codebase)
- `HYBRID-MCP-ARCHITECTURE.md` (updated)
- `IMPLEMENTATION_PLAN.md` (this file)

### Modified Files:
- `blackbox5/start.sh`

### Backup Files Created:
- `claude_desktop_config.json.backup`

---

## Next Steps

Run this plan with:
```bash
cd ~/.blackbox5
# Follow the implementation order
```

Ready to start?
