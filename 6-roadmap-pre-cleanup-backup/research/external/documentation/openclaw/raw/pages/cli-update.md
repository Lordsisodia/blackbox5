---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/cli/update",
    "fetched_at": "2026-02-07T10:15:36.248116",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 536886
  },
  "metadata": {
    "title": "update",
    "section": "update",
    "tier": 3,
    "type": "reference"
  }
}
---

- update - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationCLI commandsupdate[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [openclaw update](#openclaw-update)- [Usage](#usage)- [Options](#options)- [update status](#update-status)- [update wizard](#update-wizard)- [What it does](#what-it-does)- [Git checkout flow](#git-checkout-flow)- [--update shorthand](#update-shorthand)- [See also](#see-also)CLI commands# update# [​](#openclaw-update)`openclaw update`

Safely update OpenClaw and switch between stable/beta/dev channels.

If you installed via **npm/pnpm** (global install, no git metadata), updates happen via the package manager flow in [Updating](/install/updating).

## [​](#usage)Usage

Copy```

openclaw update

openclaw update status

openclaw update wizard

openclaw update --channel beta

openclaw update --channel dev

openclaw update --tag beta

openclaw update --no-restart

openclaw update --json

openclaw --update

```

## [​](#options)Options

- `--no-restart`: skip restarting the Gateway service after a successful update.

- `--channel <stable|beta|dev>`: set the update channel (git + npm; persisted in config).

- `--tag <dist-tag|version>`: override the npm dist-tag or version for this update only.

- `--json`: print machine-readable `UpdateRunResult` JSON.

- `--timeout <seconds>`: per-step timeout (default is 1200s).

Note: downgrades require confirmation because older versions can break configuration.

## [​](#update-status)`update status`

Show the active update channel + git tag/branch/SHA (for source checkouts), plus update availability.

Copy```

openclaw update status

openclaw update status --json

openclaw update status --timeout 10

```

Options:

- `--json`: print machine-readable status JSON.

- `--timeout <seconds>`: timeout for checks (default is 3s).

## [​](#update-wizard)`update wizard`

Interactive flow to pick an update channel and confirm whether to restart the Gateway

after updating (default is to restart). If you select `dev` without a git checkout, it

offers to create one.

## [​](#what-it-does)What it does

When you switch channels explicitly (`--channel ...`), OpenClaw also keeps the

install method aligned:

- `dev` → ensures a git checkout (default: `~/openclaw`, override with `OPENCLAW_GIT_DIR`),

updates it, and installs the global CLI from that checkout.

- `stable`/`beta` → installs from npm using the matching dist-tag.

## [​](#git-checkout-flow)Git checkout flow

Channels:

- `stable`: checkout the latest non-beta tag, then build + doctor.

- `beta`: checkout the latest `-beta` tag, then build + doctor.

- `dev`: checkout `main`, then fetch + rebase.

High-level:

- Requires a clean worktree (no uncommitted changes).

- Switches to the selected channel (tag or branch).

- Fetches upstream (dev only).

- Dev only: preflight lint + TypeScript build in a temp worktree; if the tip fails, walks back up to 10 commits to find the newest clean build.

- Rebases onto the selected commit (dev only).

- Installs deps (pnpm preferred; npm fallback).

- Builds + builds the Control UI.

- Runs `openclaw doctor` as the final “safe update” check.

- Syncs plugins to the active channel (dev uses bundled extensions; stable/beta uses npm) and updates npm-installed plugins.

## [​](#update-shorthand)`--update` shorthand

`openclaw --update` rewrites to `openclaw update` (useful for shells and launcher scripts).

## [​](#see-also)See also

- `openclaw doctor` (offers to run update first on git checkouts)

- [Development channels](/install/development-channels)

- [Updating](/install/updating)

- [CLI reference](/cli)

[uninstall](/cli/uninstall)[voicecall](/cli/voicecall)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)