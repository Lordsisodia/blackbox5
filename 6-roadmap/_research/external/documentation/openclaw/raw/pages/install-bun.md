---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/install/bun",
    "fetched_at": "2026-02-07T10:19:00.895111",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 497574
  },
  "metadata": {
    "title": "Bun (Experimental)",
    "section": "bun",
    "tier": 3,
    "type": "reference"
  }
}
---

- Bun (Experimental) - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationOther install methodsBun (Experimental)[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Install overview- [Install](/install)- [Installer Internals](/install/installer)Other install methods- [Docker](/install/docker)- [Nix](/install/nix)- [Ansible](/install/ansible)- [Bun (Experimental)](/install/bun)Maintenance- [Updating](/install/updating)- [Migration Guide](/install/migrating)- [Uninstall](/install/uninstall)Hosting and deployment- [Fly.io](/install/fly)- [Hetzner](/install/hetzner)- [GCP](/install/gcp)- [macOS VMs](/install/macos-vm)- [exe.dev](/install/exe-dev)- [Deploy on Railway](/install/railway)- [Deploy on Render](/install/render)- [Deploy on Northflank](/install/northflank)Advanced- [Development Channels](/install/development-channels)On this page- [Bun (experimental)](#bun-experimental)- [Status](#status)- [Install](#install)- [Build / Test (Bun)](#build-%2F-test-bun)- [Bun lifecycle scripts (blocked by default)](#bun-lifecycle-scripts-blocked-by-default)- [Caveats](#caveats)Other install methods# Bun (Experimental)# [​](#bun-experimental)Bun (experimental)

Goal: run this repo with **Bun** (optional, not recommended for WhatsApp/Telegram)

without diverging from pnpm workflows.

⚠️ **Not recommended for Gateway runtime** (WhatsApp/Telegram bugs). Use Node for production.

## [​](#status)Status

- Bun is an optional local runtime for running TypeScript directly (`bun run …`, `bun --watch …`).

- `pnpm` is the default for builds and remains fully supported (and used by some docs tooling).

- Bun cannot use `pnpm-lock.yaml` and will ignore it.

## [​](#install)Install

Default:

Copy```

bun install

```

Note: `bun.lock`/`bun.lockb` are gitignored, so there’s no repo churn either way. If you want *no lockfile writes*:

Copy```

bun install --no-save

```

## [​](#build-/-test-bun)Build / Test (Bun)

Copy```

bun run build

bun run vitest run

```

## [​](#bun-lifecycle-scripts-blocked-by-default)Bun lifecycle scripts (blocked by default)

Bun may block dependency lifecycle scripts unless explicitly trusted (`bun pm untrusted` / `bun pm trust`).

For this repo, the commonly blocked scripts are not required:

- `@whiskeysockets/baileys` `preinstall`: checks Node major >= 20 (we run Node 22+).

- `protobufjs` `postinstall`: emits warnings about incompatible version schemes (no build artifacts).

If you hit a real runtime issue that requires these scripts, trust them explicitly:

Copy```

bun pm trust @whiskeysockets/baileys protobufjs

```

## [​](#caveats)Caveats

- Some scripts still hardcode pnpm (e.g. `docs:build`, `ui:*`, `protocol:check`). Run those via pnpm for now.

[Ansible](/install/ansible)[Updating](/install/updating)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)