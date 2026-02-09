---
source: "claude-code"
generated_at: "2026-02-03T23:55:00Z"
pages_processed: 6
---

# Claude Code - Quick Reference

## Installation

```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex

# Homebrew (no auto-update)
brew install --cask claude-code
```

## Basic Commands

| Command | Description |
|---------|-------------|
| `claude` | Start interactive REPL |
| `claude "query"` | Start with initial prompt |
| `claude -p "query"` | Query via SDK, then exit (headless) |
| `claude -c` | Continue most recent conversation |
| `claude -r "name"` | Resume session by name |
| `claude update` | Update to latest version |
| `claude mcp` | Configure MCP servers |

## Permission Modes

| Mode | Description |
|------|-------------|
| `default` | Prompt on first tool use |
| `acceptEdits` | Auto-accept file edits |
| `plan` | Read-only analysis mode |
| `dontAsk` | Auto-deny unless pre-approved |
| `bypassPermissions` | Skip all prompts (dangerous) |

Toggle with `Shift+Tab` or `--permission-mode {mode}`

## Key CLI Flags

```bash
--continue, -c          # Continue recent conversation
--resume, -r <name>     # Resume named session
--print, -p             # Non-interactive mode
--model sonnet|opus     # Select model
--permission-mode plan  # Start in plan mode
--chrome                # Enable browser integration
--add-dir <path>        # Add working directory
--tools "Bash,Edit"     # Restrict available tools
--verbose               # Show turn-by-turn output
```

## MCP Server Commands

```bash
# Add HTTP server
claude mcp add --transport http <name> <url>

# Add stdio server
claude mcp add --transport stdio <name> -- <command>

# List servers
claude mcp list

# Remove server
claude mcp remove <name>

# Add with env vars
claude mcp add --env KEY=value <name> -- npx server
```

## MCP Scopes

| Scope | Storage | Use Case |
|-------|---------|----------|
| `local` (default) | `~/.claude.json` | Personal, project-specific |
| `project` | `.mcp.json` | Team-shared |
| `user` | `~/.claude.json` | Cross-project personal |

## Permission Rules

```json
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Read(./src/**)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Read(./.env)", "Bash(rm -rf /)"]
  }
}
```

### Pattern Syntax

- `Bash(npm run *)` - Match npm commands
- `Read(./src/**)` - Match src directory
- `Read(//absolute/path)` - Absolute path
- `Read(~/file)` - Home directory
- `WebFetch(domain:example.com)` - Domain restriction

## Settings Precedence (High → Low)

1. Managed settings (IT-enforced)
2. Command line flags
3. Local project (`.claude/settings.local.json`)
4. Shared project (`.claude/settings.json`)
5. User settings (`~/.claude/settings.json`)

## Useful Environment Variables

```bash
ANTHROPIC_API_KEY              # API authentication
MAX_THINKING_TOKENS=10000      # Limit thinking budget
MCP_TIMEOUT=10000              # MCP startup timeout
MAX_MCP_OUTPUT_TOKENS=50000    # MCP output limit
ENABLE_TOOL_SEARCH=auto        # Tool search threshold
CLAUDE_CODE_ENABLE_TELEMETRY=1 # Enable telemetry
```

## Interactive Shortcuts

| Shortcut | Action |
|----------|--------|
| `Shift+Tab` | Cycle permission modes |
| `Option+T` / `Alt+T` | Toggle thinking mode |
| `Ctrl+O` | Toggle verbose mode |
| `Ctrl+G` | Open plan in editor |
| `/` | Show commands |
| `@` | Reference files/MCP resources |

## Session Management

```bash
# Resume sessions
claude --continue              # Most recent
claude --resume                # Interactive picker
claude --resume "name"         # By name
claude --from-pr 123           # From PR

# Within Claude
/resume                        # Switch session
/rename "name"                 # Name session
```

## File References

```
> Explain @src/utils/auth.js
> What's in @src/components?
> Check @github:issue://123
```

## Plan Mode

Safe, read-only analysis before making changes:

```bash
claude --permission-mode plan
```

Or toggle with `Shift+Tab` during session.

## Output Formats

```bash
--output-format text       # Plain text (default)
--output-format json       # JSON with metadata
--output-format stream-json # Real-time JSON
```

## Subagents

```bash
# List/create agents
/agents

# Use specific agent
> use the code-reviewer agent

# Create custom agent in .claude/agents/
```

## Common Workflows

```bash
# Explore codebase
> give me an overview of this codebase

# Fix bugs
> I'm seeing an error when I run npm test

# Refactor
> refactor utils.js to use modern JavaScript

# Add tests
> add tests for the notification service

# Create PR
> /commit-push-pr
```

## Security Notes

- `bypassPermissions` is dangerous - only use in containers
- Deny rules take precedence over allow rules
- Use `//` for absolute paths in Read/Edit rules
- Sandboxing adds OS-level restrictions for Bash

## Links

- Main docs: https://code.claude.com/docs
- llms.txt: https://code.claude.com/docs/llms.txt
- Agent SDK: https://docs.claude.com/en/docs/agent-sdk
