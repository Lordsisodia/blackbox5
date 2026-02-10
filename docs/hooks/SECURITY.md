# Pre-Tool-Use Security Hook

This hook provides security blocking for dangerous commands in the BlackBox5 autonomous system.

## Purpose

Prevents accidental execution of dangerous commands that could cause data loss or security issues.

## Features

### 1. rm -rf Blocking

Blocks the following dangerous rm patterns:
- `rm -rf` / `rm -fr` / `rm -Rf` (standard destructive commands)
- `rm --recursive --force`
- `rm --force --recursive`
- `rm -r ... -f` (any combination with -r and -f flags)
- Commands targeting dangerous paths:
  - `/` (root directory)
  - `~/` (home directory)
  - `$HOME` (home environment variable)
  - Wildcards (`/*`, `*`, `..`)

### 2. .env File Protection

Blocks access to `.env` files containing sensitive data while allowing `.env.sample` templates.

Blocked operations:
- Reading `.env` files
- Editing `.env` files
- Writing to `.env` files
- `cat .env`, `echo > .env`, `touch .env`, `cp .env`, `mv .env`

Allowed:
- `.env.sample` files (template references)

## Exit Code Semantics

For autonomous systems:

- `exit 0` = Allow tool execution
- `exit 2` = Block tool with error message to stderr

## Usage

The hook is automatically registered in `.claude/settings.json`:

```json
{
  "hooks": {
    "pre_tool_use": {
      "enabled": true,
      "path": ".claude/hooks/pre_tool_use.py"
    }
  }
}
```

## Testing

### Safe Commands (Should Allow)
- `rm -r mydir` (non-destructive)
- `rm file.txt` (single file)
- `Read .env.sample`
- `Edit .env.sample`
- `Bash echo "test"` (no file operations)

### Dangerous Commands (Should Block)
- `rm -rf /` (root deletion)
- `rm -rf .`
- `rm -rf ~`
- `rm --recursive --force /tmp`
- `cat .env` (sensitive data)
- `echo "key=value" > .env` (overwrite)

## Log File

All tool calls are logged to `logs/pre_tool_use.json` for audit purposes.

## Implementation Details

The hook uses regex pattern matching to detect dangerous commands:
- Command normalization (lowercase, single spaces)
- Pattern matching for rm flags and dangerous paths
- File path checking for .env access
- JSON logging of all tool calls

## Rollback

To disable the hook:

```bash
mv .claude/hooks/pre_tool_use.py .claude/hooks/pre_tool_use.py.disabled
```

To re-enable:

```bash
mv .claude/hooks/pre_tool_use.py.disabled .claude/hooks/pre_tool_use.py
```

## References

- Source: `6-roadmap/_research/external/GitHub/Claude-Code/data/repos/claude-code-hooks-mastery/.claude/hooks/pre_tool_use.py`
- Implementation: `.claude/hooks/pre_tool_use.py`
- Utilities: `.claude/hooks/utils/security_patterns.py`
