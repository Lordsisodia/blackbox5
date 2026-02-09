---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/sandbox",
    "fetched_at": "2026-02-07T10:15:30.972804",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 626132
  },
  "metadata": {
    "title": "Sandbox CLI",
    "section": "sandbox",
    "tier": 3,
    "type": "reference"
  }
}
---

- Sandbox CLI - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandsSandbox CLI[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [Sandbox CLI](#sandbox-cli)- [Overview](#overview)- [Commands](#commands)- [openclaw sandbox explain](#openclaw-sandbox-explain)- [openclaw sandbox list](#openclaw-sandbox-list)- [openclaw sandbox recreate](#openclaw-sandbox-recreate)- [Use Cases](#use-cases)- [After updating Docker images](#after-updating-docker-images)- [After changing sandbox configuration](#after-changing-sandbox-configuration)- [After changing setupCommand](#after-changing-setupcommand)- [For a specific agent only](#for-a-specific-agent-only)- [Why is this needed?](#why-is-this-needed)- [Configuration](#configuration)- [See Also](#see-also)CLI commands# Sandbox CLI# [​](#sandbox-cli)Sandbox CLI

Manage Docker-based sandbox containers for isolated agent execution.

## [​](#overview)Overview

OpenClaw can run agents in isolated Docker containers for security. The `sandbox` commands help you manage these containers, especially after updates or configuration changes.

## [​](#commands)Commands

### [​](#openclaw-sandbox-explain)`openclaw sandbox explain`

Inspect the **effective** sandbox mode/scope/workspace access, sandbox tool policy, and elevated gates (with fix-it config key paths).

Copy```

openclaw sandbox explain

openclaw sandbox explain --session agent:main:main

openclaw sandbox explain --agent work

openclaw sandbox explain --json

```

### [​](#openclaw-sandbox-list)`openclaw sandbox list`

List all sandbox containers with their status and configuration.

Copy```

openclaw sandbox list

openclaw sandbox list --browser  # List only browser containers

openclaw sandbox list --json     # JSON output

```

**Output includes:**

- Container name and status (running/stopped)

- Docker image and whether it matches config

- Age (time since creation)

- Idle time (time since last use)

- Associated session/agent

### [​](#openclaw-sandbox-recreate)`openclaw sandbox recreate`

Remove sandbox containers to force recreation with updated images/config.

Copy```

openclaw sandbox recreate --all                # Recreate all containers

openclaw sandbox recreate --session main       # Specific session

openclaw sandbox recreate --agent mybot        # Specific agent

openclaw sandbox recreate --browser            # Only browser containers

openclaw sandbox recreate --all --force        # Skip confirmation

```

**Options:**

- `--all`: Recreate all sandbox containers

- `--session <key>`: Recreate container for specific session

- `--agent <id>`: Recreate containers for specific agent

- `--browser`: Only recreate browser containers

- `--force`: Skip confirmation prompt

**Important:** Containers are automatically recreated when the agent is next used.

## [​](#use-cases)Use Cases

### [​](#after-updating-docker-images)After updating Docker images

Copy```

# Pull new image

docker pull openclaw-sandbox:latest

docker tag openclaw-sandbox:latest openclaw-sandbox:bookworm-slim

# Update config to use new image

# Edit config: agents.defaults.sandbox.docker.image (or agents.list[].sandbox.docker.image)

# Recreate containers

openclaw sandbox recreate --all

```

### [​](#after-changing-sandbox-configuration)After changing sandbox configuration

Copy```

# Edit config: agents.defaults.sandbox.* (or agents.list[].sandbox.*)

# Recreate to apply new config

openclaw sandbox recreate --all

```

### [​](#after-changing-setupcommand)After changing setupCommand

Copy```

openclaw sandbox recreate --all

# or just one agent:

openclaw sandbox recreate --agent family

```

### [​](#for-a-specific-agent-only)For a specific agent only

Copy```

# Update only one agent's containers

openclaw sandbox recreate --agent alfred

```

## [​](#why-is-this-needed)Why is this needed?

**Problem:** When you update sandbox Docker images or configuration:

- Existing containers continue running with old settings

- Containers are only pruned after 24h of inactivity

- Regularly-used agents keep old containers running indefinitely

**Solution:** Use `openclaw sandbox recreate` to force removal of old containers. They’ll be recreated automatically with current settings when next needed.

Tip: prefer `openclaw sandbox recreate` over manual `docker rm`. It uses the

Gateway’s container naming and avoids mismatches when scope/session keys change.

## [​](#configuration)Configuration

Sandbox settings live in `~/.openclaw/openclaw.json` under `agents.defaults.sandbox` (per-agent overrides go in `agents.list[].sandbox`):

Copy```

{

"agents": {

"defaults": {

"sandbox": {

"mode": "all", // off, non-main, all

"scope": "agent", // session, agent, shared

"docker": {

"image": "openclaw-sandbox:bookworm-slim",

"containerPrefix": "openclaw-sbx-",

// ... more Docker options

},

"prune": {

"idleHours": 24, // Auto-prune after 24h idle

"maxAgeDays": 7, // Auto-prune after 7 days

},

},

},

},

}

```

## [​](#see-also)See Also

- [Sandbox Documentation](/gateway/sandboxing)

- [Agent Configuration](/concepts/agent-workspace)

- [Doctor Command](/gateway/doctor) - Check sandbox setup

[reset](/cli/reset)[security](/cli/security)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)