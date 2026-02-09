---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/install/node",
    "fetched_at": "2026-02-07T10:19:08.961592",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 576699
  },
  "metadata": {
    "title": "Node.js",
    "section": "node",
    "tier": 3,
    "type": "reference"
  }
}
---

- Node.js - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationEnvironment and debuggingNode.js[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Help- [Help](/help)- [Troubleshooting](/help/troubleshooting)- [FAQ](/help/faq)Community- [OpenClaw Lore](/start/lore)Environment and debugging- [Node.js](/install/node)- [Environment Variables](/environment)- [Debugging](/debugging)- [Testing](/testing)- [Scripts](/scripts)- [Session Management Deep Dive](/reference/session-management-compaction)Developer workflows- [Setup](/start/setup)- [Submitting a PR](/help/submitting-a-pr)- [Submitting an Issue](/help/submitting-an-issue)Docs meta- [Docs Hubs](/start/hubs)- [Docs directory](/start/docs-directory)On this page- [Node.js](#node-js)- [Check your version](#check-your-version)- [Install Node](#install-node)- [Troubleshooting](#troubleshooting)- [openclaw: command not found](#openclaw-command-not-found)- [Permission errors on npm install -g (Linux)](#permission-errors-on-npm-install-g-linux)Environment and debugging# Node.js# [​](#node-js)Node.js

OpenClaw requires **Node 22 or newer**. The [installer script](/install#install-methods) will detect and install Node automatically — this page is for when you want to set up Node yourself and make sure everything is wired up correctly (versions, PATH, global installs).

## [​](#check-your-version)Check your version

Copy```

node -v

```

If this prints `v22.x.x` or higher, you’re good. If Node isn’t installed or the version is too old, pick an install method below.

## [​](#install-node)Install Node

-  macOS-  Linux-  Windows**Homebrew** (recommended):Copy```

brew install node

```Or download the macOS installer from [nodejs.org](https://nodejs.org/).**Ubuntu / Debian:**Copy```

curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -

sudo apt-get install -y nodejs

```**Fedora / RHEL:**Copy```

sudo dnf install nodejs

```Or use a version manager (see below).**winget** (recommended):Copy```

winget install OpenJS.NodeJS.LTS

```**Chocolatey:**Copy```

choco install nodejs-lts

```Or download the Windows installer from [nodejs.org](https://nodejs.org/).

Using a version manager (nvm, fnm, mise, asdf)Version managers let you switch between Node versions easily. Popular options:

- [**fnm**](https://github.com/Schniz/fnm) — fast, cross-platform

- [**nvm**](https://github.com/nvm-sh/nvm) — widely used on macOS/Linux

- [**mise**](https://mise.jdx.dev/) — polyglot (Node, Python, Ruby, etc.)

Example with fnm:Copy```

fnm install 22

fnm use 22

```Make sure your version manager is initialized in your shell startup file (`~/.zshrc` or `~/.bashrc`). If it isn’t, `openclaw` may not be found in new terminal sessions because the PATH won’t include Node’s bin directory.

## [​](#troubleshooting)Troubleshooting

### [​](#openclaw-command-not-found)`openclaw: command not found`

This almost always means npm’s global bin directory isn’t on your PATH.

1[](#)Find your global npm prefixCopy```

npm prefix -g

```2[](#)Check if it's on your PATHCopy```

echo "$PATH"

```Look for `<npm-prefix>/bin` (macOS/Linux) or `<npm-prefix>` (Windows) in the output.3[](#)Add it to your shell startup file-  macOS / Linux-  WindowsAdd to `~/.zshrc` or `~/.bashrc`:Copy```

export PATH="$(npm prefix -g)/bin:$PATH"

```Then open a new terminal (or run `rehash` in zsh / `hash -r` in bash).Add the output of `npm prefix -g` to your system PATH via Settings → System → Environment Variables.

### [​](#permission-errors-on-npm-install-g-linux)Permission errors on `npm install -g` (Linux)

If you see `EACCES` errors, switch npm’s global prefix to a user-writable directory:

Copy```

mkdir -p "$HOME/.npm-global"

npm config set prefix "$HOME/.npm-global"

export PATH="$HOME/.npm-global/bin:$PATH"

```

Add the `export PATH=...` line to your `~/.bashrc` or `~/.zshrc` to make it permanent.[OpenClaw Lore](/start/lore)[Environment Variables](/environment)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)