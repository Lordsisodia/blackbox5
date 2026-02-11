# BB5 CLI Architecture Design: Replacing MCP Servers with Pattern 3

**Date:** 2026-02-10
**Status:** Design Complete - Ready for Implementation
**Pattern:** Progressive Disclosure Architecture (Pattern 3) + kubectl-style Context Switching

---

## Executive Summary

This design replaces all current MCP servers with a unified CLI architecture following **Pattern 3 (Progressive Disclosure)** with **kubectl-style context switching**. The architecture reduces token usage by ~99% through on-demand tool discovery while maintaining full functionality.

### Key Benefits

| Metric | Current MCP | New BB5 CLI | Improvement |
|--------|-------------|-------------|-------------|
| Startup Tokens | ~47,000 | ~50 | 99.9% reduction |
| Per-Tool Tokens | 0 (pre-loaded) | ~500 (on-demand) | Pay-per-use |
| Multi-Client Support | Separate MCPs per client | Context switching | Unified interface |
| Agent Autonomy | Limited to MCP tools | Full shell composability | Maximum flexibility |

---

## Current MCP Inventory → CLI Mapping

| Current MCP | Purpose | CLI Equivalent |
|-------------|---------|----------------|
| `supabase` (multiple clients) | Database operations | `bb5 db <command>` with context switching |
| `moltbot-vps` | SSH to VPS (77.42.66.40) | `bb5 remote exec vps <command>` |
| `moltbot-macmini` | SSH to Mac Mini | `bb5 remote exec macmini <command>` |
| Chrome DevTools | Browser control | `bb5 browser <command>` |
| Playwright | Browser automation | `bb5 playwright <command>` |
| Filesystem | File operations | `bb5 fs <command>` |
| Sequential Thinking | Reasoning chains | `bb5 think <command>` |
| Fetch | HTTP requests | `bb5 http <command>` or native `curl` |
| Code Parser | AST analysis | `bb5 code parse <file>` |
| Auto-claude | Automation | `bb5 auto <command>` |

---

## Directory Structure

```
~/blackbox5/
├── bin/
│   ├── bb5                          # Main CLI router
│   └── bb5-cli/                     # NEW: MCP-replacement CLI tools
│       ├── bb5-db                   # Database/Supabase operations
│       ├── bb5-remote               # Remote execution (SSH/VPS/MoltBot)
│       ├── bb5-browser              # Chrome DevTools integration
│       ├── bb5-playwright           # Playwright automation
│       ├── bb5-fs                   # Filesystem operations
│       ├── bb5-think                # Sequential thinking
│       ├── bb5-http                 # HTTP/fetch operations
│       ├── bb5-code                 # Code parsing
│       ├── bb5-auto                 # Auto-claude operations
│       ├── bb5-discover             # Tool discovery
│       ├── bb5-schema               # Schema loader
│       └── lib/                     # Shared libraries
│           ├── bb5_cli_colors.sh
│           ├── bb5_cli_context.sh   # kubectl-style context mgmt
│           ├── bb5_cli_discovery.sh # On-demand discovery
│           └── bb5_cli_config.sh
├── config/
│   └── bb5-cli/                     # CLI configuration
│       ├── bb5-cli.yaml             # Main config
│       └── contexts/                # kubectl-style contexts
│           ├── supabase/
│           │   ├── client-a.yaml    # Per-client configs
│           │   ├── client-b.yaml
│           │   └── default          # Symlink to current
│           ├── remote/
│           │   ├── vps.yaml         # VPS SSH config
│           │   ├── macmini.yaml     # Mac Mini config
│           │   └── default
│           └── browser/
│               ├── default.yaml
│               └── headless.yaml
└── lib/
    └── bb5-cli/                     # Python libraries (optional)
        ├── discovery.py
        ├── context_manager.py
        └── tool_runner.py
```

---

## Progressive Disclosure Architecture

### Three-Level Discovery

```
Level 1: Root Manifest (Always Loaded)
├── db: "Database operations"
├── remote: "Remote execution"
├── browser: "Browser automation"
└── ...
(~50 tokens)

Level 2: Category Index (Loaded on Access)
bb5 discover db
├── query: "Execute SQL queries"
├── migrate: "Run migrations"
├── backup: "Create backups"
└── restore: "Restore from backup"
(~100 tokens)

Level 3: Tool Schema (Loaded on Use)
bb5 schema db:query
├── description: "Execute SQL query..."
├── args:
│   ├── sql: {type: string, required: true}
│   └── format: {type: enum, options: [json, table, csv]}
└── examples: [...]
(~500-1000 tokens)
```

### Token Efficiency Comparison

| Scenario | Traditional MCP | BB5 CLI | Savings |
|----------|-----------------|---------|---------|
| Startup (6 servers, 60 tools) | 47,000 tokens | 50 tokens | 99.9% |
| Use 1 tool | 47,000 tokens | 50 + 500 = 550 tokens | 98.8% |
| Use 5 tools | 47,000 tokens | 50 + 2,500 = 2,550 tokens | 94.6% |

---

## Multi-Client Configuration (kubectl-Style)

### Supabase Contexts

```yaml
# ~/blackbox5/config/bb5-cli/contexts/supabase/client-a.yaml
name: client-a
project_ref: avdgyrepwrvsvwgxrccr
url: https://avdgyrepwrvsvwgxrccr.supabase.co
api_key: ${SUPABASE_CLIENT_A_KEY}  # Env var reference
region: us-east-1

# ~/blackbox5/config/bb5-cli/contexts/supabase/client-b.yaml
name: client-b
project_ref: xyz789
url: https://xyz789.supabase.co
api_key: ${SUPABASE_CLIENT_B_KEY}
region: eu-west-1
```

### Context Commands

```bash
# List contexts
bb5 db context list
# → client-a (current)
# → client-b
# → client-c

# Get current context
bb5 db context current
# → client-a

# Switch context
bb5 db context use client-b
# → Switched to context "client-b"

# Show context details
bb5 db context show
# → name: client-a
# → project_ref: avdgyrepwrvsvwgxrccr
# → url: https://avdgyrepwrvsvwgxrccr.supabase.co
# → region: us-east-1

# Create new context
bb5 db context create client-c \
  --project-ref abc123 \
  --url https://abc123.supabase.co \
  --key $SUPABASE_CLIENT_C_KEY

# Use specific context for single command
bb5 db query -s "SELECT * FROM users" -c client-b
```

### Remote Contexts (MoltBot Replacement)

```yaml
# ~/blackbox5/config/bb5-cli/contexts/remote/vps.yaml
name: vps
host: 77.42.66.40
user: root
ssh_key: ~/.ssh/ralf_hetzner
ralf_path: /opt/ralf
openclaw_path: /opt/openclaw

# ~/blackbox5/config/bb5-cli/contexts/remote/macmini.yaml
name: macmini
host: 192.168.1.100
user: shaan
ssh_key: ~/.ssh/macmini
ralf_path: ~/ralf
```

---

## Tool Examples

### 1. Database Operations (Supabase)

```bash
# Query with current context
bb5 db query -s "SELECT * FROM users LIMIT 10"

# Query with specific context
bb5 db query -s "SELECT * FROM orders" -c client-b

# Run migrations
bb5 db migrate up
bb5 db migrate status
bb5 db migrate create add_users_table

# Backup/Restore
bb5 db backup --name backup-$(date +%Y%m%d)
bb5 db restore --from backup-20260210

# Edge functions
bb5 db edge deploy
bb5 db edge logs
```

### 2. Remote Execution (MoltBot Replacement)

```bash
# Execute command on VPS
bb5 remote exec vps "ralf status"
bb5 remote exec vps "cat /opt/ralf/.autonomous/agents/communications/queue.yaml"

# Interactive SSH
bb5 remote exec vps --interactive

# File transfer
bb5 remote transfer vps --local ./file.txt --remote /opt/ralf/
bb5 remote transfer vps --remote /opt/ralf/logs.txt --local ./logs/

# RALF-specific shortcuts
bb5 remote ralf vps status
bb5 remote ralf vps queue
bb5 remote ralf vps events

# OpenClaw/MoltBot commands
bb5 remote claw vps message send --channel telegram --target 7643203581 --message "Hello"
bb5 remote claw vps status
```

### 3. Browser Operations (Chrome DevTools)

```bash
# Navigation
bb5 browser navigate --url https://example.com
bb5 browser navigate --url https://example.com --wait-for "#content"

# Screenshots
bb5 browser screenshot --output screenshot.png
bb5 browser screenshot --full-page --output full.png
bb5 browser screenshot --selector "#chart" --output chart.png

# Interaction
bb5 browser click --selector "#submit-button"
bb5 browser fill --selector "#email" --value "test@example.com"
bb5 browser scroll --direction down --amount 500

# JavaScript execution
bb5 browser evaluate --script "document.title"
bb5 browser evaluate --script "JSON.stringify(window.performance)"

# Network
bb5 browser network --list-requests
bb5 browser network --har-output network.har

# Console
bb5 browser console --execute "console.log('test')"
bb5 browser console --listen --filter "error"
```

### 4. Playwright

```bash
# Run tests
bb5 playwright test
bb5 playwright test --headed
bb5 playwright test --project chromium

# Codegen
bb5 playwright codegen --url https://example.com --output test.js

# Record
bb5 playwright record --output recording.js

# Debug
bb5 playwright test --debug
bb5 playwright show-report
```

### 5. Filesystem

```bash
# Read/Write
bb5 fs read --path /path/to/file
bb5 fs write --path /path/to/file --content "Hello World"
bb5 fs append --path /path/to/file --content "More content"

# Search
bb5 fs search --pattern "*.py" --path /project
bb5 fs grep --pattern "TODO" --path /project
bb5 fs grep --pattern "class.*:" --path /project --type python

# Tree
bb5 fs tree --path /project --depth 3
bb5 fs tree --path /project --include "*.ts" --exclude "node_modules"

# Watch
bb5 fs watch --path /project --on-change "echo 'File changed'"
```

### 6. Sequential Thinking

```bash
# Start thinking session
bb5 think start --topic "Architecture Decision: MCP vs CLI"

# Add steps
bb5 think step --content "MCP provides standardization but adds overhead"
bb5 think step --content "CLI is more flexible and token-efficient"

# Branch
bb5 think branch --from-step 1 --topic "Alternative: Hybrid approach"
bb5 think step --content "Use MCP for external APIs, CLI for internal tools"

# View
bb5 think list
bb5 think show --id think-001
bb5 think export --id think-001 --format markdown
```

---

## Implementation Priority

### Phase 1: Foundation (Week 1)
1. Create directory structure
2. Implement `bb5` router
3. Implement context management library
4. Implement discovery mechanism

### Phase 2: Core Tools (Week 2)
1. `bb5-db` with Supabase support
2. `bb5-remote` replacing MoltBot MCP
3. Context switching for both

### Phase 3: Browser Tools (Week 3)
1. `bb5-browser` (Chrome DevTools)
2. `bb5-playwright`
3. `bb5-fs`

### Phase 4: Specialized Tools (Week 4)
1. `bb5-think`
2. `bb5-http`
3. `bb5-code`
4. `bb5-auto`

### Phase 5: Migration (Week 5)
1. Update MCP configs to use CLI
2. Deprecate MCP servers
3. Documentation

---

## Key Design Decisions

### 1. Why kubectl-style contexts?
- **Proven pattern**: Industry standard for multi-cluster/tenant systems
- **Familiar**: DevOps teams already know it
- **Flexible**: Easy to add new context types
- **Composable**: Works with shell scripts

### 2. Why Progressive Disclosure?
- **Token efficiency**: 99% reduction in context usage
- **Scalable**: Can support 1000+ tools without bloat
- **Discoverable**: Agents can explore capabilities dynamically
- **Maintainable**: Each tool is self-contained

### 3. Why Shell-based vs Python?
- **Universal**: Works on any Unix system
- **Composable**: Pipes, redirects, shell integration
- **Debuggable**: Direct error visibility
- **Fast**: No interpreter startup overhead

---

## References

- [kubectl Context Management](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)
- [philschmid/mcp-cli](https://github.com/philschmid/mcp-cli) - On-demand discovery pattern
- [oclif Command Discovery](https://oclif.io/docs/command_discovery_strategies/) - CLI organization
- [MCP vs CLI Benchmark](https://mariozechner.at/posts/2025-08-15-mcp-vs-cli/) - Performance comparison
- Pattern 3: Progressive Disclosure Architecture from research
