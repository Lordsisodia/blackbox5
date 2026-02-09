---
fetch:
  url: "https://code.claude.com/docs/en/settings"
  fetched_at: "2026-02-03T23:42:00Z"
  status: 200
  content_type: "text/html"

metadata:
  title: "Settings"
  section: "settings"
  tier: 1
  type: "reference"
---

# Settings

> Configure Claude Code to match your workflow with settings files, environment variables, and permission rules.

## Settings files

Claude Code loads settings from multiple locations, following a specific precedence order. Settings defined in higher-precedence sources override those in lower-precedence sources.

### Settings precedence (highest to lowest)

| Precedence | Source | Location | Use case |
| :--------- | :----- | :------- | :------- |
| 1 (highest) | **Managed settings** | System directories | IT-enforced policies that cannot be overridden |
| 2 | **Command line** | Runtime flags | Temporary session overrides |
| 3 | **Local project** | `.claude/settings.local.json` | Personal project-specific settings (gitignored) |
| 4 | **Shared project** | `.claude/settings.json` | Team-shared project settings |
| 5 (lowest) | **User settings** | `~/.claude/settings.json` | Personal global settings |

### File locations by platform

**macOS:**

* User settings: `~/.claude/settings.json`
* Local project settings: `.claude/settings.local.json`
* Shared project settings: `.claude/settings.json`
* Managed settings: `/Library/Application Support/ClaudeCode/managed-settings.json`

**Linux and WSL:**

* User settings: `~/.claude/settings.json`
* Local project settings: `.claude/settings.local.json`
* Shared project settings: `.claude/settings.json`
* Managed settings: `/etc/claude-code/managed-settings.json`

**Windows:**

* User settings: `%USERPROFILE%\.claude\settings.json`
* Local project settings: `.claude\settings.local.json`
* Shared project settings: `.claude\settings.json`
* Managed settings: `C:\Program Files\ClaudeCode\managed-settings.json`

### Example `settings.json`

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": ["Bash(npm run lint)", "Bash(npm run test *)"],
    "deny": ["Bash(curl *)", "Read(./.env)", "Read(./secrets/**)"]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1"
  },
  "companyAnnouncements": ["Welcome to Acme Corp!"]
}
```

## Available settings

### `permissions`

Controls which tools Claude Code can use and which files or domains it can access.

| Setting | Type | Description |
| :------ | :--- | :---------- |
| `allow` | string[] | Tools that execute without prompting for permission |
| `ask` | string[] | Tools that prompt for confirmation before executing |
| `deny` | string[] | Tools that cannot be used |
| `defaultMode` | string | Default permission mode: `"default"`, `"acceptEdits"`, `"plan"`, `"dontAsk"`, or `"bypassPermissions"` |
| `additionalDirectories` | string[] | Additional working directories Claude can access |

See [Permissions](/en/permissions) for detailed documentation on permission rules and syntax.

### `sandbox`

Configures OS-level filesystem and network isolation for Bash commands.

| Setting | Type | Description |
| :------ | :--- | :---------- |
| `enabled` | boolean | Enable sandboxing for Bash commands |
| `autoAllowBashIfSandboxed` | boolean | Automatically allow Bash commands when sandbox is enabled |
| `excludedCommands` | string[] | Bash commands that bypass sandbox restrictions |
| `network.allowedDomains` | string[] | Domains Bash commands can access when sandboxed |

See [Sandboxing](/en/sandboxing) for detailed documentation.

### `attribution`

Controls how Claude Code attributes its contributions.

| Setting | Type | Description |
| :------ | :--- | :---------- |
| `commit` | boolean | Add "Co-authored-by: Claude" to git commits |
| `pr` | boolean | Add "Co-authored-by: Claude" to PR descriptions |

### `mcp`

MCP server configuration options.

| Setting | Type | Description |
| :------ | :--- | :---------- |
| `enableAllProjectMcpServers` | boolean | Automatically enable all MCP servers defined in `.mcp.json` |
| `enabledMcpjsonServers` | string[] | Specific MCP server names to enable from `.mcp.json` |
| `allowedMcpServers` | object[] | Allowlist for MCP servers (managed settings only) |
| `deniedMcpServers` | object[] | Denylist for MCP servers (managed settings only) |

See [MCP](/en/mcp) for detailed documentation.

### `plugins`

Plugin system configuration.

| Setting | Type | Description |
| :------ | :--- | :---------- |
| `enabledPlugins` | string[] | List of plugin names to enable |
| `extraKnownMarketplaces` | string[] | Additional plugin marketplace URLs |
| `strictKnownMarketplaces` | boolean | Only allow plugins from known marketplaces (managed settings only) |

See [Plugins](/en/plugins) for detailed documentation.

### `hooks`

Lifecycle hooks for extending Claude Code behavior.

| Setting | Type | Description |
| :------ | :--- | :---------- |
| `hooks` | object[] | Custom hooks to run at various lifecycle points |
| `disableAllHooks` | boolean | Disable all hooks |
| `allowManagedHooksOnly` | boolean | Only run hooks defined in managed settings (managed settings only) |

See [Hooks](/en/hooks) for detailed documentation.

### `env`

Environment variables to set for Claude Code sessions.

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "MAX_THINKING_TOKENS": "10000"
  }
}
```

### `companyAnnouncements`

Custom announcements displayed at the start of Claude Code sessions.

```json
{
  "companyAnnouncements": ["Welcome to Acme Corp!", "Check out our style guide at /docs/style.md"]
}
```

### `autoCompact`

Controls automatic context compaction behavior.

| Setting | Type | Description |
| :------ | :--- | :---------- |
| `enabled` | boolean | Enable automatic compaction (default: true) |
| `threshold` | number | Context usage threshold to trigger compaction (0-1, default: 0.8) |

### `alwaysThinkingEnabled`

Whether extended thinking mode is enabled by default.

| Setting | Type | Description |
| :------ | :--- | :---------- |
| `alwaysThinkingEnabled` | boolean | Enable thinking mode by default (default: true) |

## Permission rule syntax

Permission rules follow the format `Tool` or `Tool(specifier)`.

### Match all uses of a tool

To match all uses of a tool, use just the tool name without parentheses:

| Rule | Effect |
| :--- | :----- |
| `Bash` | Matches all Bash commands |
| `WebFetch` | Matches all web fetch requests |
| `Read` | Matches all file reads |

### Use specifiers for fine-grained control

Add a specifier in parentheses to match specific tool uses:

| Rule | Effect |
| :--- | :----- |
| `Bash(npm run build)` | Matches the exact command `npm run build` |
| `Read(./.env)` | Matches reading the `.env` file |
| `WebFetch(domain:example.com)` | Matches fetch requests to example.com |

### Wildcard patterns

Bash rules support glob patterns with `*`:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

### Read and Edit patterns

Read and Edit rules follow gitignore-style patterns:

| Pattern | Meaning | Example |
| :------ | :------ | :------ |
| `//path` | Absolute path from filesystem root | `Read(//Users/alice/secrets/**)` |
| `~/path` | Path from home directory | `Read(~/Documents/*.pdf)` |
| `/path` | Path relative to settings file | `Edit(/src/**/*.ts)` |
| `path` or `./path` | Path relative to current directory | `Read(*.env)` |

## Environment variables

Claude Code recognizes several environment variables:

### API and authentication

| Variable | Description |
| :------- | :---------- |
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `CLAUDE_CODE_USE_BEDROCK` | Use Amazon Bedrock instead of Anthropic API |
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex AI instead of Anthropic API |
| `CLAUDE_CODE_USE_FOUNDRY` | Use Microsoft Azure Foundry instead of Anthropic API |

### Behavior

| Variable | Description |
| :------- | :---------- |
| `MAX_THINKING_TOKENS` | Maximum tokens for extended thinking |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | Enable OpenTelemetry instrumentation |
| `DISABLE_TELEMETRY` | Disable telemetry collection |
| `DISABLE_ERROR_REPORTING` | Disable error reporting |
| `DISABLE_AUTOUPDATER` | Disable automatic updates |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | Override auto-compaction threshold |

### MCP

| Variable | Description |
| :------- | :---------- |
| `MCP_TIMEOUT` | MCP server startup timeout in milliseconds |
| `MAX_MCP_OUTPUT_TOKENS` | Maximum MCP tool output tokens |
| `ENABLE_TOOL_SEARCH` | MCP tool search behavior: `auto`, `true`, `false`, or `auto:N` |

## Tools available to Claude

Claude Code has access to these tools:

### No permission required

* `AskUserQuestion` - Ask the user a question
* `Glob` - Find files matching a pattern
* `Grep` - Search file contents
* `Read` - Read a file
* `MCPSearch` - Search for MCP tools

### Permission required

* `Bash` - Execute shell commands
* `Edit` - Edit files
* `NotebookEdit` - Edit Jupyter notebooks
* `Skill` - Invoke skills
* `WebFetch` - Fetch web content
* `MCP` - Use MCP tools
* `TaskOutput` - Get output from subagents
* `KillShell` - Kill running shell processes

## Managed-only settings

These settings can only be defined in managed settings files:

| Setting | Description |
| :------ | :---------- |
| `disableBypassPermissionsMode` | Prevent use of `bypassPermissions` mode |
| `allowManagedPermissionRulesOnly` | Only use permission rules from managed settings |
| `allowManagedHooksOnly` | Only run hooks from managed settings |
| `strictKnownMarketplaces` | Restrict plugin marketplaces |

See [Permissions - Managed settings](/en/permissions#managed-settings) for details.

## Example configurations

### Basic project settings

```json
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Bash(git *)"],
    "deny": ["Bash(curl *)", "Read(./.env)"]
  }
}
```

### Team settings with MCP

```json
{
  "permissions": {
    "allow": ["Bash(npm *)", "Bash(git *)"],
    "defaultMode": "acceptEdits"
  },
  "mcp": {
    "enableAllProjectMcpServers": true
  },
  "companyAnnouncements": ["Welcome to the team! Check out our wiki at wiki.company.com"]
}
```

### Personal productivity settings

```json
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Bash(git *)", "Bash(docker *)"],
    "deny": ["Bash(rm -rf /)"]
  },
  "env": {
    "MAX_THINKING_TOKENS": "15000",
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1"
  },
  "attribution": {
    "commit": true,
    "pr": true
  }
}
```

## See also

* [Permissions](/en/permissions) - Detailed permission system documentation
* [Sandboxing](/en/sandboxing) - OS-level isolation for Bash commands
* [MCP](/en/mcp) - MCP server configuration
* [Hooks](/en/hooks) - Lifecycle hooks
* [Plugins](/en/plugins) - Plugin system
