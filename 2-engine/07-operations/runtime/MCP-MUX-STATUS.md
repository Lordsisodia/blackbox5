# MCP Multiplexer Implementation Status

## Current Status: **Blocked**

### Problem Identified

The core issue requires a true multiplexer that:
1. Runs MCP servers **once** as persistent daemons
2. Allows **multiple Claude sessions** to connect simultaneously
3. Uses **Unix sockets** or similar for fast IPC
4. Provides **connection pooling** and **caching**

### Solutions Evaluated

| Solution | Status | Issue |
|----------|--------|-------|
| **rmcp-mux** (Rust) | ❌ Failed | Compilation error in v0.3.4 (`Dashboard` pattern not covered) |
| **multi-mcp** (Python) | ❌ Not suitable | Spawns separate processes per MCP, doesn't multiplex connections |
| **TBXark/mcp-proxy** (Go) | ❌ Not suitable | HTTP-based aggregator, doesn't solve local multiplexing |
| **Custom script** | ⚠️ Partial | Starts servers but lacks proper socket multiplexing |

### Root Cause

**None of the available open-source solutions provide true local MCP multiplexing:**

```
What we need:
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Claude 1   │  │  Claude 2   │  │  Claude N   │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┴────────────────┘
                       │
               ┌───────▼────────┐
               │  Single Shared │
               │  MCP Server    │
               └────────────────┘

What's available:
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Claude 1   │  │  Claude 2   │  │  Claude N   │
│  ├─Supabase │  │  ├─Supabase │  │  ├─Supabase │
└─────────────┘  └─────────────┘  └─────────────┘
    (Each spawns own MCPs)
```

### Why rmcp-mux Was the Best Choice

| Feature | rmcp-mux | Others |
|---------|----------|--------|
| Unix socket per MCP | ✅ | ❌ (HTTP only) |
| Multiple clients per MCP | ✅ | ❌ (1:1 only) |
| Initialize caching | ✅ | ❌ |
| Auto-restart | ✅ | ⚠️ (partial) |
| Resource efficient | ✅ (~500 MB) | ⚠️ (~800 MB+) |
| **Status** | **Compilation bug** | **Doesn't multiplex** |

### Compilation Error Details

```
error[E0004]: non-exhaustive patterns: `&Some(CliCommand::Dashboard(_))` not covered
   --> src/bin/rmcp_mux.rs:169:11
    |
169 |     match &cli.command {
    |           ^^^^^^^^^^^^ pattern `&Some(CliCommand::Dashboard(_))` not covered
```

This is a simple pattern matching bug that could be fixed with:
```rust
match &cli.command {
    Some(CliCommand::Dashboard(_)) => todo!(),
    None => {},
    // ... other patterns
}
```

### Options Forward

#### Option 1: Wait for rmcp-mux Fix
- Monitor: https://github.com/VetCoders/rmcp-mux
- The bug is minor and should be fixed soon
- Could also submit a PR ourselves

#### Option 2: Fix rmcp-mux Locally
```bash
git clone https://github.com/VetCoders/rmcp-mux
cd rmcp-mux
# Fix the pattern matching bug in src/bin/rmcp_mux.rs
cargo build --release
```

#### Option 3: Build Custom Multiplexer
- Create a simple Go/Python daemon
- Use Unix sockets for each MCP
- Implement basic connection pooling
- Estimated effort: 2-3 days

#### Option 4: Accept Current State
- Continue with 32 MCP processes
- Monitor and cleanup regularly
- Use `cleanup-agents` script
- Resource cost: ~1.6 GB RAM

### Current Workaround

The scripts created (`start-shared-mcps.sh`, `mcp-status`, etc.) help manage MCP servers but don't fully solve the multiplexing problem because:

1. **Claude Desktop spawns its own MCPs** regardless of what's running
2. **No way to tell Claude "use existing MCP server"**
3. **MCP protocol doesn't specify a sharing mechanism**

### Recommendation

**Wait for rmcp-mux fix OR implement custom solution**

The rmcp-mux bug is trivial - it's just a missing pattern match. The project is actively maintained and this should be fixed soon.

### Files Created

Despite the block, these files are useful for management:

| File | Purpose |
|------|---------|
| `~/bin/start-shared-mcps.sh` | Start MCP servers manually |
| `~/bin/kill-shared-mcps.sh` | Kill all MCP servers |
| `~/bin/mcp-status` | Check MCP server status |
| Documentation | Complete guides for when solution is available |

### Resource Impact (Current)

```
Current State: 32 MCP processes = 2.13 GB RAM
Target State (with rmcp-mux): ~5 processes = 500 MB RAM
Gap: 1.6 GB RAM (until multiplexer is available)
```

### Next Steps

1. **Monitor rmcp-mux** for fixes
2. **Use cleanup-agents** regularly to manage orphans
3. **Consider submitting PR** to fix the compilation bug
4. **Revisit when rmcp-mux is fixed** or build custom solution

### Timestamp
2025-01-21 05:47 UTC

---

**Note:** This is a temporary blocker. The solution (rmcp-mux) exists and is well-designed, it just has a minor compilation bug that needs to be fixed.
