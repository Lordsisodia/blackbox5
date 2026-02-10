# BB5 CLI - Agent Guide

**How AI Agents Discover and Use BB5 CLI Tools**

---

## Discovery Workflow

When you need a tool, follow this discovery process:

### Step 1: List Categories

```bash
bb5 discover
```

**Output:**
```
BB5 CLI Tool Categories
======================

db        - Database operations (Supabase)
remote    - Remote SSH execution
browser   - Chrome DevTools integration
playwright- Browser automation
fs        - Filesystem operations
think     - Sequential thinking
http      - HTTP requests
code      - Code parsing
```

### Step 2: List Tools in Category

```bash
bb5 discover db
```

**Output:**
```
Database Tools (Context: client-a)
==================================

query      - Execute SQL queries
migrate    - Run database migrations
backup     - Create database backup
restore    - Restore from backup
seed       - Seed database with data
edge       - Edge function operations
```

### Step 3: Get Tool Schema

```bash
bb5 schema db:query
```

**Output:**
```yaml
tool: db:query
description: Execute SQL query against Supabase database
context: Uses current context (see 'bb5 db context current')

arguments:
  - name: sql
    type: string
    required: true
    description: SQL query to execute

  - name: format
    type: enum
    options: [table, json, csv]
    default: table
    description: Output format

  - name: context
    type: string
    required: false
    description: Override context for this command only

examples:
  - bb5 db query -s "SELECT * FROM users LIMIT 10"
  - bb5 db query -s "SELECT * FROM orders" -f json
  - bb5 db query -s "SELECT *" -c client-b
```

### Step 4: Execute Tool

```bash
bb5 db query -s "SELECT * FROM users LIMIT 10"
```

---

## Context Management

### When to Switch Contexts

Switch contexts when working with different clients:

```bash
# Working on Client A
bb5 db context use client-a
bb5 db query -s "SELECT * FROM client_a_table"

# Switch to Client B
bb5 db context use client-b
bb5 db query -s "SELECT * FROM client_b_table"
```

### One-Off Context Override

Use `-c` flag for single commands without switching:

```bash
bb5 db query -s "SELECT *" -c client-a
bb5 db query -s "SELECT *" -c client-b
```

### View Current Context

```bash
bb5 db context current
# Output: client-a

bb5 db context show
# Output: Full context details
```

---

## Common Patterns

### Pattern 1: Database Query + Processing

```bash
# Query and pipe to jq for processing
bb5 db query -s "SELECT * FROM users" -f json | jq '.[] | select(.active == true)'
```

### Pattern 2: Remote Command + Local Processing

```bash
# Get RALF status from VPS
bb5 remote exec vps "cat /opt/ralf/.autonomous/agents/communications/queue.yaml"

# Stream logs
bb5 remote exec vps "tail -f /opt/ralf/logs/ralf.log"
```

### Pattern 3: Browser Screenshot + Analysis

```bash
# Take screenshot
bb5 browser navigate --url https://example.com
bb5 browser screenshot --output /tmp/screenshot.png

# Now analyze the screenshot
```

### Pattern 4: Multi-Context Comparison

```bash
# Compare data across clients
bb5 db query -s "SELECT COUNT(*) FROM users" -c client-a
bb5 db query -s "SELECT COUNT(*) FROM users" -c client-b
bb5 db query -s "SELECT COUNT(*) FROM users" -c client-c
```

---

## Tool Reference

### Database (bb5 db)

| Command | Purpose | Example |
|---------|---------|---------|
| `bb5 db query` | Execute SQL | `bb5 db query -s "SELECT *"` |
| `bb5 db migrate up` | Run migrations | `bb5 db migrate up` |
| `bb5 db migrate status` | Check migration status | `bb5 db migrate status` |
| `bb5 db backup` | Create backup | `bb5 db backup --name backup-2024` |
| `bb5 db restore` | Restore backup | `bb5 db restore --from backup-2024` |
| `bb5 db context use <name>` | Switch context | `bb5 db context use client-b` |

### Remote (bb5 remote)

| Command | Purpose | Example |
|---------|---------|---------|
| `bb5 remote exec <host> <cmd>` | Execute SSH command | `bb5 remote exec vps "ls -la"` |
| `bb5 remote exec <host> -i` | Interactive SSH | `bb5 remote exec vps -i` |
| `bb5 remote transfer <host>` | Transfer files | `bb5 remote transfer vps --local file.txt --remote /opt/` |
| `bb5 remote ralf <host> status` | RALF status | `bb5 remote ralf vps status` |
| `bb5 remote claw <host> message` | Send message | `bb5 remote claw vps message send --channel telegram ...` |

### Browser (bb5 browser)

| Command | Purpose | Example |
|---------|---------|---------|
| `bb5 browser navigate` | Navigate to URL | `bb5 browser navigate --url https://example.com` |
| `bb5 browser screenshot` | Take screenshot | `bb5 browser screenshot --output screenshot.png` |
| `bb5 browser click` | Click element | `bb5 browser click --selector "#button"` |
| `bb5 browser fill` | Fill input | `bb5 browser fill --selector "#email" --value "test@test.com"` |
| `bb5 browser evaluate` | Execute JS | `bb5 browser evaluate --script "document.title"` |

---

## Troubleshooting

### Tool Not Found

```bash
# Check if tool exists
bb5 discover <category>

# Check tool schema
bb5 schema <category>:<tool>
```

### Context Not Found

```bash
# List available contexts
bb5 db context list

# Create new context
bb5 db context create <name> --project-ref <ref> --url <url>
```

### Command Failed

All tools return exit codes:
- `0`: Success
- `1`: General error
- `2`: Invalid arguments
- `3`: Context not found
- `4`: Connection failed

---

## Best Practices

1. **Discover first**: Always use `bb5 discover` to see available tools
2. **Check schema**: Use `bb5 schema` before executing unfamiliar tools
3. **Use contexts**: Switch contexts instead of hardcoding connection details
4. **Pipe output**: Tools output JSON for easy piping to `jq`
5. **Check exit codes**: Always check if commands succeeded
