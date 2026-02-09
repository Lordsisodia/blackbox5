---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/hooks",
    "fetched_at": "2026-02-07T10:11:05.435768",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 700107
  },
  "metadata": {
    "title": "hooks",
    "section": "hooks",
    "tier": 2,
    "type": "reference"
  }
}
---

- hooks - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandshooks[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw hooks](#openclaw-hooks)- [List All Hooks](#list-all-hooks)- [Get Hook Information](#get-hook-information)- [Check Hooks Eligibility](#check-hooks-eligibility)- [Enable a Hook](#enable-a-hook)- [Disable a Hook](#disable-a-hook)- [Install Hooks](#install-hooks)- [Update Hooks](#update-hooks)- [Bundled Hooks](#bundled-hooks)- [session-memory](#session-memory)- [command-logger](#command-logger)- [soul-evil](#soul-evil)- [boot-md](#boot-md)CLI commands# hooks# [​](#openclaw-hooks)`openclaw hooks`

Manage agent hooks (event-driven automations for commands like `/new`, `/reset`, and gateway startup).

Related:

- Hooks: [Hooks](/hooks)

- Plugin hooks: [Plugins](/plugin#plugin-hooks)

## [​](#list-all-hooks)List All Hooks

Copy```

openclaw hooks list

```

List all discovered hooks from workspace, managed, and bundled directories.

**Options:**

- `--eligible`: Show only eligible hooks (requirements met)

- `--json`: Output as JSON

- `-v, --verbose`: Show detailed information including missing requirements

**Example output:**

Copy```

Hooks (4/4 ready)

Ready:

🚀 boot-md ✓ - Run BOOT.md on gateway startup

📝 command-logger ✓ - Log all command events to a centralized audit file

💾 session-memory ✓ - Save session context to memory when /new command is issued

😈 soul-evil ✓ - Swap injected SOUL content during a purge window or by random chance

```

**Example (verbose):**

Copy```

openclaw hooks list --verbose

```

Shows missing requirements for ineligible hooks.

**Example (JSON):**

Copy```

openclaw hooks list --json

```

Returns structured JSON for programmatic use.

## [​](#get-hook-information)Get Hook Information

Copy```

openclaw hooks info <name>

```

Show detailed information about a specific hook.

**Arguments:**

- `<name>`: Hook name (e.g., `session-memory`)

**Options:**

- `--json`: Output as JSON

**Example:**

Copy```

openclaw hooks info session-memory

```

**Output:**

Copy```

💾 session-memory ✓ Ready

Save session context to memory when /new command is issued

Details:

Source: openclaw-bundled

Path: /path/to/openclaw/hooks/bundled/session-memory/HOOK.md

Handler: /path/to/openclaw/hooks/bundled/session-memory/handler.ts

Homepage: https://docs.openclaw.ai/hooks#session-memory

Events: command:new

Requirements:

Config: ✓ workspace.dir

```

## [​](#check-hooks-eligibility)Check Hooks Eligibility

Copy```

openclaw hooks check

```

Show summary of hook eligibility status (how many are ready vs. not ready).

**Options:**

- `--json`: Output as JSON

**Example output:**

Copy```

Hooks Status

Total hooks: 4

Ready: 4

Not ready: 0

```

## [​](#enable-a-hook)Enable a Hook

Copy```

openclaw hooks enable <name>

```

Enable a specific hook by adding it to your config (`~/.openclaw/config.json`).

**Note:** Hooks managed by plugins show `plugin:<id>` in `openclaw hooks list` and

can’t be enabled/disabled here. Enable/disable the plugin instead.

**Arguments:**

- `<name>`: Hook name (e.g., `session-memory`)

**Example:**

Copy```

openclaw hooks enable session-memory

```

**Output:**

Copy```

✓ Enabled hook: 💾 session-memory

```

**What it does:**

- Checks if hook exists and is eligible

- Updates `hooks.internal.entries.<name>.enabled = true` in your config

- Saves config to disk

**After enabling:**

- Restart the gateway so hooks reload (menu bar app restart on macOS, or restart your gateway process in dev).

## [​](#disable-a-hook)Disable a Hook

Copy```

openclaw hooks disable <name>

```

Disable a specific hook by updating your config.

**Arguments:**

- `<name>`: Hook name (e.g., `command-logger`)

**Example:**

Copy```

openclaw hooks disable command-logger

```

**Output:**

Copy```

⏸ Disabled hook: 📝 command-logger

```

**After disabling:**

- Restart the gateway so hooks reload

## [​](#install-hooks)Install Hooks

Copy```

openclaw hooks install <path-or-spec>

```

Install a hook pack from a local folder/archive or npm.

**What it does:**

- Copies the hook pack into `~/.openclaw/hooks/<id>`

- Enables the installed hooks in `hooks.internal.entries.*`

- Records the install under `hooks.internal.installs`

**Options:**

- `-l, --link`: Link a local directory instead of copying (adds it to `hooks.internal.load.extraDirs`)

**Supported archives:** `.zip`, `.tgz`, `.tar.gz`, `.tar`

**Examples:**

Copy```

# Local directory

openclaw hooks install ./my-hook-pack

# Local archive

openclaw hooks install ./my-hook-pack.zip

# NPM package

openclaw hooks install @openclaw/my-hook-pack

# Link a local directory without copying

openclaw hooks install -l ./my-hook-pack

```

## [​](#update-hooks)Update Hooks

Copy```

openclaw hooks update <id>

openclaw hooks update --all

```

Update installed hook packs (npm installs only).

**Options:**

- `--all`: Update all tracked hook packs

- `--dry-run`: Show what would change without writing

## [​](#bundled-hooks)Bundled Hooks

### [​](#session-memory)session-memory

Saves session context to memory when you issue `/new`.

**Enable:**

Copy```

openclaw hooks enable session-memory

```

**Output:** `~/.openclaw/workspace/memory/YYYY-MM-DD-slug.md`

**See:** [session-memory documentation](/hooks#session-memory)

### [​](#command-logger)command-logger

Logs all command events to a centralized audit file.

**Enable:**

Copy```

openclaw hooks enable command-logger

```

**Output:** `~/.openclaw/logs/commands.log`

**View logs:**

Copy```

# Recent commands

tail -n 20 ~/.openclaw/logs/commands.log

# Pretty-print

cat ~/.openclaw/logs/commands.log | jq .

# Filter by action

grep '"action":"new"' ~/.openclaw/logs/commands.log | jq .

```

**See:** [command-logger documentation](/hooks#command-logger)

### [​](#soul-evil)soul-evil

Swaps injected `SOUL.md` content with `SOUL_EVIL.md` during a purge window or by random chance.

**Enable:**

Copy```

openclaw hooks enable soul-evil

```

**See:** [SOUL Evil Hook](/hooks/soul-evil)

### [​](#boot-md)boot-md

Runs `BOOT.md` when the gateway starts (after channels start).

**Events**: `gateway:startup`

**Enable**:

Copy```

openclaw hooks enable boot-md

```

**See:** [boot-md documentation](/hooks#boot-md)[health](/cli/health)[logs](/cli/logs)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)