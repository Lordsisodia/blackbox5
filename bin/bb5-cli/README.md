# BB5 CLI - MCP Replacement

**Purpose**: Replace MCP servers with discoverable, token-efficient CLI tools.

**Location**: `~/.blackbox5/bin/bb5-cli/`

---

## Quick Start

```bash
# Discover available tools
bb5 discover

# Discover database tools
bb5 discover db

# Get help for a specific tool
bb5 schema db:query

# Execute a tool
bb5 db query -s "SELECT * FROM users"
```

---

## Architecture

### Progressive Disclosure

Tools are discovered in 3 levels:

1. **Root** (~50 tokens): Categories only
   ```
   bb5 discover
   → db: Database operations
   → remote: Remote execution
   → browser: Browser automation
   ```

2. **Category** (~100 tokens): Tool names only
   ```
   bb5 discover db
   → query: Execute SQL queries
   → migrate: Run migrations
   → backup: Create backups
   ```

3. **Tool** (~500 tokens): Full schema loaded on-demand
   ```
   bb5 schema db:query
   → Full argument schema, examples, etc.
   ```

### Context Switching

Multi-client support via kubectl-style contexts:

```bash
# List contexts
bb5 db context list

# Switch context
bb5 db context use client-b

# Use specific context for one command
bb5 db query -s "SELECT *" -c client-a
```

---

## Tool Categories

| Category | Command | Description |
|----------|---------|-------------|
| Database | `bb5 db` | Supabase operations with multi-client support |
| Remote | `bb5 remote` | SSH execution (replaces MoltBot MCP) |
| Browser | `bb5 browser` | Chrome DevTools integration |
| Playwright | `bb5 playwright` | Browser automation |
| Filesystem | `bb5 fs` | File operations |
| Think | `bb5 think` | Sequential thinking chains |
| HTTP | `bb5 http` | HTTP requests |
| Code | `bb5 code` | Code parsing/analysis |

---

## Configuration

Contexts stored in: `~/.blackbox5/config/bb5-cli/contexts/`

```yaml
# Example: ~/.blackbox5/config/bb5-cli/contexts/supabase/client-a.yaml
name: client-a
project_ref: abc123
url: https://abc123.supabase.co
api_key: ${SUPABASE_CLIENT_A_KEY}
```

---

## For Agents

See [AGENT_GUIDE.md](./AGENT_GUIDE.md) for how AI agents discover and use these tools.
