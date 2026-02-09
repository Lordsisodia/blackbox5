---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/install/uninstall",
    "fetched_at": "2026-02-07T10:19:41.689598",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 574875
  },
  "metadata": {
    "title": "Uninstall",
    "section": "uninstall",
    "tier": 3,
    "type": "reference"
  }
}
---

- Uninstall - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationMaintenanceUninstall[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Install overview- [Install](/install)- [Installer Internals](/install/installer)Other install methods- [Docker](/install/docker)- [Nix](/install/nix)- [Ansible](/install/ansible)- [Bun (Experimental)](/install/bun)Maintenance- [Updating](/install/updating)- [Migration Guide](/install/migrating)- [Uninstall](/install/uninstall)Hosting and deployment- [Fly.io](/install/fly)- [Hetzner](/install/hetzner)- [GCP](/install/gcp)- [macOS VMs](/install/macos-vm)- [exe.dev](/install/exe-dev)- [Deploy on Railway](/install/railway)- [Deploy on Render](/install/render)- [Deploy on Northflank](/install/northflank)Advanced- [Development Channels](/install/development-channels)On this page- [Uninstall](#uninstall)- [Easy path (CLI still installed)](#easy-path-cli-still-installed)- [Manual service removal (CLI not installed)](#manual-service-removal-cli-not-installed)- [macOS (launchd)](#macos-launchd)- [Linux (systemd user unit)](#linux-systemd-user-unit)- [Windows (Scheduled Task)](#windows-scheduled-task)- [Normal install vs source checkout](#normal-install-vs-source-checkout)- [Normal install (install.sh / npm / pnpm / bun)](#normal-install-install-sh-%2F-npm-%2F-pnpm-%2F-bun)- [Source checkout (git clone)](#source-checkout-git-clone)Maintenance# Uninstall# [​](#uninstall)Uninstall

Two paths:

- **Easy path** if `openclaw` is still installed.

- **Manual service removal** if the CLI is gone but the service is still running.

## [​](#easy-path-cli-still-installed)Easy path (CLI still installed)

Recommended: use the built-in uninstaller:

Copy```

openclaw uninstall

```

Non-interactive (automation / npx):

Copy```

openclaw uninstall --all --yes --non-interactive

npx -y openclaw uninstall --all --yes --non-interactive

```

Manual steps (same result):

- Stop the gateway service:

Copy```

openclaw gateway stop

```

- Uninstall the gateway service (launchd/systemd/schtasks):

Copy```

openclaw gateway uninstall

```

- Delete state + config:

Copy```

rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"

```

If you set `OPENCLAW_CONFIG_PATH` to a custom location outside the state dir, delete that file too.

- Delete your workspace (optional, removes agent files):

Copy```

rm -rf ~/.openclaw/workspace

```

- Remove the CLI install (pick the one you used):

Copy```

npm rm -g openclaw

pnpm remove -g openclaw

bun remove -g openclaw

```

- If you installed the macOS app:

Copy```

rm -rf /Applications/OpenClaw.app

```

Notes:

- If you used profiles (`--profile` / `OPENCLAW_PROFILE`), repeat step 3 for each state dir (defaults are `~/.openclaw-<profile>`).

- In remote mode, the state dir lives on the **gateway host**, so run steps 1-4 there too.

## [​](#manual-service-removal-cli-not-installed)Manual service removal (CLI not installed)

Use this if the gateway service keeps running but `openclaw` is missing.

### [​](#macos-launchd)macOS (launchd)

Default label is `bot.molt.gateway` (or `bot.molt.<profile>`; legacy `com.openclaw.*` may still exist):

Copy```

launchctl bootout gui/$UID/bot.molt.gateway

rm -f ~/Library/LaunchAgents/bot.molt.gateway.plist

```

If you used a profile, replace the label and plist name with `bot.molt.<profile>`. Remove any legacy `com.openclaw.*` plists if present.

### [​](#linux-systemd-user-unit)Linux (systemd user unit)

Default unit name is `openclaw-gateway.service` (or `openclaw-gateway-<profile>.service`):

Copy```

systemctl --user disable --now openclaw-gateway.service

rm -f ~/.config/systemd/user/openclaw-gateway.service

systemctl --user daemon-reload

```

### [​](#windows-scheduled-task)Windows (Scheduled Task)

Default task name is `OpenClaw Gateway` (or `OpenClaw Gateway (<profile>)`).

The task script lives under your state dir.

Copy```

schtasks /Delete /F /TN "OpenClaw Gateway"

Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"

```

If you used a profile, delete the matching task name and `~\.openclaw-<profile>\gateway.cmd`.

## [​](#normal-install-vs-source-checkout)Normal install vs source checkout

### [​](#normal-install-install-sh-/-npm-/-pnpm-/-bun)Normal install (install.sh / npm / pnpm / bun)

If you used `https://openclaw.ai/install.sh` or `install.ps1`, the CLI was installed with `npm install -g openclaw@latest`.

Remove it with `npm rm -g openclaw` (or `pnpm remove -g` / `bun remove -g` if you installed that way).

### [​](#source-checkout-git-clone)Source checkout (git clone)

If you run from a repo checkout (`git clone` + `openclaw ...` / `bun run openclaw ...`):

- Uninstall the gateway service **before** deleting the repo (use the easy path above or manual service removal).

- Delete the repo directory.

- Remove state + workspace as shown above.

[Migration Guide](/install/migrating)[Fly.io](/install/fly)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)