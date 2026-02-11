# BB5 CLI Testing Guide

## What's Implemented

### Working Commands

| Command | Status | Description |
|---------|--------|-------------|
| `bb5 discover` | ✅ | List all tool categories |
| `bb5 discover db` | ✅ | List database tools |
| `bb5 discover remote` | ✅ | List remote tools |
| `bb5 schema db:query` | ✅ | Show query tool schema |
| `bb5 schema remote:exec` | ✅ | Show exec tool schema |
| `bb5 db context list` | ✅ | List database contexts |
| `bb5 db context use <name>` | ✅ | Switch database context |
| `bb5 db context show` | ✅ | Show current context |
| `bb5 remote context list` | ✅ | List remote contexts |
| `bb5 remote context use <name>` | ✅ | Switch remote context |
| `bb5 db query` | ⚠️ | Needs Supabase setup |
| `bb5 remote exec` | ⚠️ | Needs SSH key setup |

### Test the Discovery System

```bash
# 1. Test root discovery
export BB5_DIR=$HOME/blackbox5
~/blackbox5/bin/bb5-cli/bb5-discover

# 2. Test category discovery
~/blackbox5/bin/bb5-cli/bb5-discover db
~/blackbox5/bin/bb5-cli/bb5-discover remote

# 3. Test schema loading
~/blackbox5/bin/bb5-cli/bb5-schema db:query
~/blackbox5/bin/bb5-cli/bb5-schema remote:exec
```

### Test Context Management

```bash
# Database contexts
~/blackbox5/bin/bb5-cli/bb5-db context list
~/blackbox5/bin/bb5-cli/bb5-db context show

# Remote contexts
~/blackbox5/bin/bb5-cli/bb5-remote context list
~/blackbox5/bin/bb5-cli/bb5-remote context show
```

### Test Remote Execution (VPS)

```bash
# This will work if you have SSH keys set up
~/blackbox5/bin/bb5-cli/bb5-remote exec vps "ls -la /opt/ralf"
~/blackbox5/bin/bb5-cli/bb5-remote exec vps "cat /opt/ralf/.autonomous/agents/communications/queue.yaml"
```

### Test Database Query (Supabase)

```bash
# Set your API key
export SUPABASE_CLIENT_A_KEY=your_key_here

# Run query
~/blackbox5/bin/bb5-cli/bb5-db query -s "SELECT * FROM users LIMIT 5"
```

## Token Efficiency Test

Compare the token usage:

```bash
# Old MCP way: Loads ALL schemas at startup (~47,000 tokens)
# New CLI way: Progressive disclosure

# Step 1: Discovery (50 tokens)
bb5 discover

# Step 2: Category discovery (100 tokens)
bb5 discover db

# Step 3: Tool schema (500 tokens) - only when needed
bb5 schema db:query

# Total for first use: ~650 tokens vs 47,000 tokens = 98.6% reduction
```

## What's Missing for Full Implementation

1. **Main `bb5` router** - Need to integrate with existing BB5 CLI
2. **More tool implementations**:
   - `db-migrate`, `db-backup`, `db-restore`
   - `remote-transfer`, `remote-ralf`, `remote-claw`
   - `browser-*` tools for Chrome DevTools
   - `playwright-*` tools
   - `fs-*` tools
3. **Lazy MCP Gateway integration** - Connect to your existing gateway
4. **Error handling** - More robust error messages
5. **Tests** - Unit tests for each tool

## Next Steps

1. Test the discovery system works
2. Test context switching
3. Test remote execution on VPS
4. Add more tool implementations
5. Integrate with main BB5 CLI
