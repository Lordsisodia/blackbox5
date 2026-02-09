---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/install/installer",
    "fetched_at": "2026-02-07T10:19:05.601243",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 867799
  },
  "metadata": {
    "title": "Installer Internals",
    "section": "installer",
    "tier": 3,
    "type": "reference"
  }
}
---

- Installer Internals - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationInstall overviewInstaller Internals[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Install overview- [Install](/install)- [Installer Internals](/install/installer)Other install methods- [Docker](/install/docker)- [Nix](/install/nix)- [Ansible](/install/ansible)- [Bun (Experimental)](/install/bun)Maintenance- [Updating](/install/updating)- [Migration Guide](/install/migrating)- [Uninstall](/install/uninstall)Hosting and deployment- [Fly.io](/install/fly)- [Hetzner](/install/hetzner)- [GCP](/install/gcp)- [macOS VMs](/install/macos-vm)- [exe.dev](/install/exe-dev)- [Deploy on Railway](/install/railway)- [Deploy on Render](/install/render)- [Deploy on Northflank](/install/northflank)Advanced- [Development Channels](/install/development-channels)On this page- [Installer internals](#installer-internals)- [Quick commands](#quick-commands)- [install.sh](#install-sh)- [Flow (install.sh)](#flow-install-sh)- [Source checkout detection](#source-checkout-detection)- [Examples (install.sh)](#examples-install-sh)- [install-cli.sh](#install-cli-sh)- [Flow (install-cli.sh)](#flow-install-cli-sh)- [Examples (install-cli.sh)](#examples-install-cli-sh)- [install.ps1](#install-ps1)- [Flow (install.ps1)](#flow-install-ps1)- [Examples (install.ps1)](#examples-install-ps1)- [CI and automation](#ci-and-automation)- [Troubleshooting](#troubleshooting)Install overview# Installer Internals# [​](#installer-internals)Installer internals

OpenClaw ships three installer scripts, served from `openclaw.ai`.

ScriptPlatformWhat it does[`install.sh`](#installsh)macOS / Linux / WSLInstalls Node if needed, installs OpenClaw via npm (default) or git, and can run onboarding.[`install-cli.sh`](#install-clish)macOS / Linux / WSLInstalls Node + OpenClaw into a local prefix (`~/.openclaw`). No root required.[`install.ps1`](#installps1)Windows (PowerShell)Installs Node if needed, installs OpenClaw via npm (default) or git, and can run onboarding.

## [​](#quick-commands)Quick commands

-  install.sh-  install-cli.sh-  install.ps1Copy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash

```Copy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --help

```Copy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash

```Copy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --help

```Copy```

iwr -useb https://openclaw.ai/install.ps1 | iex

```Copy```

& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -Tag beta -NoOnboard -DryRun

```

If install succeeds but `openclaw` is not found in a new terminal, see [Node.js troubleshooting](/install/node#troubleshooting).

## [​](#install-sh)install.sh

Recommended for most interactive installs on macOS/Linux/WSL.

### [​](#flow-install-sh)Flow (install.sh)

1[](#)Detect OSSupports macOS and Linux (including WSL). If macOS is detected, installs Homebrew if missing.2[](#)Ensure Node.js 22+Checks Node version and installs Node 22 if needed (Homebrew on macOS, NodeSource setup scripts on Linux apt/dnf/yum).3[](#)Ensure GitInstalls Git if missing.4[](#)Install OpenClaw

- `npm` method (default): global npm install

- `git` method: clone/update repo, install deps with pnpm, build, then install wrapper at `~/.local/bin/openclaw`

5[](#)Post-install tasks

- Runs `openclaw doctor --non-interactive` on upgrades and git installs (best effort)

- Attempts onboarding when appropriate (TTY available, onboarding not disabled, and bootstrap/config checks pass)

- Defaults `SHARP_IGNORE_GLOBAL_LIBVIPS=1`

### [​](#source-checkout-detection)Source checkout detection

If run inside an OpenClaw checkout (`package.json` + `pnpm-workspace.yaml`), the script offers:

- use checkout (`git`), or

- use global install (`npm`)

If no TTY is available and no install method is set, it defaults to `npm` and warns.

The script exits with code `2` for invalid method selection or invalid `--install-method` values.

### [​](#examples-install-sh)Examples (install.sh)

-  Default-  Skip onboarding-  Git install-  Dry runCopy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash

```Copy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-onboard

```Copy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git

```Copy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --dry-run

```

Flags referenceFlagDescription`--install-method npm|git`Choose install method (default: `npm`). Alias: `--method``--npm`Shortcut for npm method`--git`Shortcut for git method. Alias: `--github``--version <version|dist-tag>`npm version or dist-tag (default: `latest`)`--beta`Use beta dist-tag if available, else fallback to `latest``--git-dir <path>`Checkout directory (default: `~/openclaw`). Alias: `--dir``--no-git-update`Skip `git pull` for existing checkout`--no-prompt`Disable prompts`--no-onboard`Skip onboarding`--onboard`Enable onboarding`--dry-run`Print actions without applying changes`--verbose`Enable debug output (`set -x`, npm notice-level logs)`--help`Show usage (`-h`)Environment variables referenceVariableDescription`OPENCLAW_INSTALL_METHOD=git|npm`Install method`OPENCLAW_VERSION=latest|next|<semver>`npm version or dist-tag`OPENCLAW_BETA=0|1`Use beta if available`OPENCLAW_GIT_DIR=<path>`Checkout directory`OPENCLAW_GIT_UPDATE=0|1`Toggle git updates`OPENCLAW_NO_PROMPT=1`Disable prompts`OPENCLAW_NO_ONBOARD=1`Skip onboarding`OPENCLAW_DRY_RUN=1`Dry run mode`OPENCLAW_VERBOSE=1`Debug mode`OPENCLAW_NPM_LOGLEVEL=error|warn|notice`npm log level`SHARP_IGNORE_GLOBAL_LIBVIPS=0|1`Control sharp/libvips behavior (default: `1`)

## [​](#install-cli-sh)install-cli.sh

Designed for environments where you want everything under a local prefix (default `~/.openclaw`) and no system Node dependency.

### [​](#flow-install-cli-sh)Flow (install-cli.sh)

1[](#)Install local Node runtimeDownloads Node tarball (default `22.22.0`) to `<prefix>/tools/node-v<version>` and verifies SHA-256.2[](#)Ensure GitIf Git is missing, attempts install via apt/dnf/yum on Linux or Homebrew on macOS.3[](#)Install OpenClaw under prefixInstalls with npm using `--prefix <prefix>`, then writes wrapper to `<prefix>/bin/openclaw`.

### [​](#examples-install-cli-sh)Examples (install-cli.sh)

-  Default-  Custom prefix + version-  Automation JSON output-  Run onboardingCopy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash

```Copy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --prefix /opt/openclaw --version latest

```Copy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw

```Copy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --onboard

```

Flags referenceFlagDescription`--prefix <path>`Install prefix (default: `~/.openclaw`)`--version <ver>`OpenClaw version or dist-tag (default: `latest`)`--node-version <ver>`Node version (default: `22.22.0`)`--json`Emit NDJSON events`--onboard`Run `openclaw onboard` after install`--no-onboard`Skip onboarding (default)`--set-npm-prefix`On Linux, force npm prefix to `~/.npm-global` if current prefix is not writable`--help`Show usage (`-h`)Environment variables referenceVariableDescription`OPENCLAW_PREFIX=<path>`Install prefix`OPENCLAW_VERSION=<ver>`OpenClaw version or dist-tag`OPENCLAW_NODE_VERSION=<ver>`Node version`OPENCLAW_NO_ONBOARD=1`Skip onboarding`OPENCLAW_NPM_LOGLEVEL=error|warn|notice`npm log level`OPENCLAW_GIT_DIR=<path>`Legacy cleanup lookup path (used when removing old `Peekaboo` submodule checkout)`SHARP_IGNORE_GLOBAL_LIBVIPS=0|1`Control sharp/libvips behavior (default: `1`)

## [​](#install-ps1)install.ps1

### [​](#flow-install-ps1)Flow (install.ps1)

1[](#)Ensure PowerShell + Windows environmentRequires PowerShell 5+.2[](#)Ensure Node.js 22+If missing, attempts install via winget, then Chocolatey, then Scoop.3[](#)Install OpenClaw

- `npm` method (default): global npm install using selected `-Tag`

- `git` method: clone/update repo, install/build with pnpm, and install wrapper at `%USERPROFILE%\.local\bin\openclaw.cmd`

4[](#)Post-install tasksAdds needed bin directory to user PATH when possible, then runs `openclaw doctor --non-interactive` on upgrades and git installs (best effort).

### [​](#examples-install-ps1)Examples (install.ps1)

-  Default-  Git install-  Custom git directory-  Dry runCopy```

iwr -useb https://openclaw.ai/install.ps1 | iex

```Copy```

& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git

```Copy```

& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git -GitDir "C:\openclaw"

```Copy```

& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -DryRun

```

Flags referenceFlagDescription`-InstallMethod npm|git`Install method (default: `npm`)`-Tag <tag>`npm dist-tag (default: `latest`)`-GitDir <path>`Checkout directory (default: `%USERPROFILE%\openclaw`)`-NoOnboard`Skip onboarding`-NoGitUpdate`Skip `git pull``-DryRun`Print actions onlyEnvironment variables referenceVariableDescription`OPENCLAW_INSTALL_METHOD=git|npm`Install method`OPENCLAW_GIT_DIR=<path>`Checkout directory`OPENCLAW_NO_ONBOARD=1`Skip onboarding`OPENCLAW_GIT_UPDATE=0`Disable git pull`OPENCLAW_DRY_RUN=1`Dry run mode

If `-InstallMethod git` is used and Git is missing, the script exits and prints the Git for Windows link.

## [​](#ci-and-automation)CI and automation

Use non-interactive flags/env vars for predictable runs.

-  install.sh (non-interactive npm)-  install.sh (non-interactive git)-  install-cli.sh (JSON)-  install.ps1 (skip onboarding)Copy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-prompt --no-onboard

```Copy```

OPENCLAW_INSTALL_METHOD=git OPENCLAW_NO_PROMPT=1 \

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash

```Copy```

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw

```Copy```

& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard

```

## [​](#troubleshooting)Troubleshooting

Why is Git required?Git is required for `git` install method. For `npm` installs, Git is still checked/installed to avoid `spawn git ENOENT` failures when dependencies use git URLs.Why does npm hit EACCES on Linux?Some Linux setups point npm global prefix to root-owned paths. `install.sh` can switch prefix to `~/.npm-global` and append PATH exports to shell rc files (when those files exist).sharp/libvips issuesThe scripts default `SHARP_IGNORE_GLOBAL_LIBVIPS=1` to avoid sharp building against system libvips. To override:Copy```

SHARP_IGNORE_GLOBAL_LIBVIPS=0 curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash

```Windows: "npm error spawn git / ENOENT"Install Git for Windows, reopen PowerShell, rerun installer.Windows: "openclaw is not recognized"Run `npm config get prefix`, append `\bin`, add that directory to user PATH, then reopen PowerShell.openclaw not found after installUsually a PATH issue. See [Node.js troubleshooting](/install/node#troubleshooting).[Install](/install)[Docker](/install/docker)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)