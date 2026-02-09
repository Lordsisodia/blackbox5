---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/install/index",
    "fetched_at": "2026-02-07T10:19:04.986164",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 645895
  },
  "metadata": {
    "title": "Install",
    "section": "index",
    "tier": 3,
    "type": "reference"
  }
}
---

- Install - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationInstall overviewInstall[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Install overview- [Install](/install)- [Installer Internals](/install/installer)Other install methods- [Docker](/install/docker)- [Nix](/install/nix)- [Ansible](/install/ansible)- [Bun (Experimental)](/install/bun)Maintenance- [Updating](/install/updating)- [Migration Guide](/install/migrating)- [Uninstall](/install/uninstall)Hosting and deployment- [Fly.io](/install/fly)- [Hetzner](/install/hetzner)- [GCP](/install/gcp)- [macOS VMs](/install/macos-vm)- [exe.dev](/install/exe-dev)- [Deploy on Railway](/install/railway)- [Deploy on Render](/install/render)- [Deploy on Northflank](/install/northflank)Advanced- [Development Channels](/install/development-channels)On this page- [Install](#install)- [System requirements](#system-requirements)- [Install methods](#install-methods)- [Other install methods](#other-install-methods)- [After install](#after-install)- [Troubleshooting: openclaw not found](#troubleshooting-openclaw-not-found)- [Update / uninstall](#update-%2F-uninstall)Install overview# Install# [​](#install)Install

Already followed [Getting Started](/start/getting-started)? You’re all set — this page is for alternative install methods, platform-specific instructions, and maintenance.

## [​](#system-requirements)System requirements

- **[Node 22+](/install/node)** (the [installer script](#install-methods) will install it if missing)

- macOS, Linux, or Windows

- `pnpm` only if you build from source

On Windows, we strongly recommend running OpenClaw under [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).

## [​](#install-methods)Install methods

The **installer script** is the recommended way to install OpenClaw. It handles Node detection, installation, and onboarding in one step.

Installer scriptDownloads the CLI, installs it globally via npm, and launches the onboarding wizard.-  macOS / Linux / WSL2-  Windows (PowerShell)Copy```

curl -fsSL https://openclaw.ai/install.sh | bash

```Copy```

iwr -useb https://openclaw.ai/install.ps1 | iex

```That’s it — the script handles Node detection, installation, and onboarding.To skip onboarding and just install the binary:-  macOS / Linux / WSL2-  Windows (PowerShell)Copy```

curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard

```Copy```

& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard

```For all flags, env vars, and CI/automation options, see [Installer internals](/install/installer).npm / pnpmIf you already have Node 22+ and prefer to manage the install yourself:-  npm-  pnpmCopy```

npm install -g openclaw@latest

openclaw onboard --install-daemon

```sharp build errors?If you have libvips installed globally (common on macOS via Homebrew) and `sharp` fails, force prebuilt binaries:Copy```

SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest

```If you see `sharp: Please add node-gyp to your dependencies`, either install build tooling (macOS: Xcode CLT + `npm install -g node-gyp`) or use the env var above.Copy```

pnpm add -g openclaw@latest

pnpm approve-builds -g        # approve openclaw, node-llama-cpp, sharp, etc.

openclaw onboard --install-daemon

```pnpm requires explicit approval for packages with build scripts. After the first install shows the “Ignored build scripts” warning, run `pnpm approve-builds -g` and select the listed packages.From sourceFor contributors or anyone who wants to run from a local checkout.1[](#)Clone and buildClone the [OpenClaw repo](https://github.com/openclaw/openclaw) and build:Copy```

git clone https://github.com/openclaw/openclaw.git

cd openclaw

pnpm install

pnpm ui:build

pnpm build

```2[](#)Link the CLIMake the `openclaw` command available globally:Copy```

pnpm link --global

```Alternatively, skip the link and run commands via `pnpm openclaw ...` from inside the repo.3[](#)Run onboardingCopy```

openclaw onboard --install-daemon

```For deeper development workflows, see [Setup](/start/setup).

## [​](#other-install-methods)Other install methods

[## DockerContainerized or headless deployments.](/install/docker)[## NixDeclarative install via Nix.](/install/nix)[## AnsibleAutomated fleet provisioning.](/install/ansible)[## BunCLI-only usage via the Bun runtime.](/install/bun)

## [​](#after-install)After install

Verify everything is working:

Copy```

openclaw doctor         # check for config issues

openclaw status         # gateway status

openclaw dashboard      # open the browser UI

```

## [​](#troubleshooting-openclaw-not-found)Troubleshooting: `openclaw` not found

PATH diagnosis and fixQuick diagnosis:Copy```

node -v

npm -v

npm prefix -g

echo "$PATH"

```If `$(npm prefix -g)/bin` (macOS/Linux) or `$(npm prefix -g)` (Windows) is **not** in your `$PATH`, your shell can’t find global npm binaries (including `openclaw`).Fix — add it to your shell startup file (`~/.zshrc` or `~/.bashrc`):Copy```

export PATH="$(npm prefix -g)/bin:$PATH"

```On Windows, add the output of `npm prefix -g` to your PATH.Then open a new terminal (or `rehash` in zsh / `hash -r` in bash).

## [​](#update-/-uninstall)Update / uninstall

[## UpdatingKeep OpenClaw up to date.](/install/updating)[## MigratingMove to a new machine.](/install/migrating)[## UninstallRemove OpenClaw completely.](/install/uninstall)[Installer Internals](/install/installer)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)