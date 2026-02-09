---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/install/development-channels",
    "fetched_at": "2026-02-07T10:19:01.478763",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 498221
  },
  "metadata": {
    "title": "Development Channels",
    "section": "development-channels",
    "tier": 3,
    "type": "reference"
  }
}
---

- Development Channels - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationAdvancedDevelopment Channels[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Install overview- [Install](/install)- [Installer Internals](/install/installer)Other install methods- [Docker](/install/docker)- [Nix](/install/nix)- [Ansible](/install/ansible)- [Bun (Experimental)](/install/bun)Maintenance- [Updating](/install/updating)- [Migration Guide](/install/migrating)- [Uninstall](/install/uninstall)Hosting and deployment- [Fly.io](/install/fly)- [Hetzner](/install/hetzner)- [GCP](/install/gcp)- [macOS VMs](/install/macos-vm)- [exe.dev](/install/exe-dev)- [Deploy on Railway](/install/railway)- [Deploy on Render](/install/render)- [Deploy on Northflank](/install/northflank)Advanced- [Development Channels](/install/development-channels)On this page- [Development channels](#development-channels)- [Switching channels](#switching-channels)- [Plugins and channels](#plugins-and-channels)- [Tagging best practices](#tagging-best-practices)- [macOS app availability](#macos-app-availability)Advanced# Development Channels# [​](#development-channels)Development channels

Last updated: 2026-01-21

OpenClaw ships three update channels:

- **stable**: npm dist-tag `latest`.

- **beta**: npm dist-tag `beta` (builds under test).

- **dev**: moving head of `main` (git). npm dist-tag: `dev` (when published).

We ship builds to **beta**, test them, then **promote a vetted build to `latest`**

without changing the version number — dist-tags are the source of truth for npm installs.

## [​](#switching-channels)Switching channels

Git checkout:

Copy```

openclaw update --channel stable

openclaw update --channel beta

openclaw update --channel dev

```

- `stable`/`beta` check out the latest matching tag (often the same tag).

- `dev` switches to `main` and rebases on the upstream.

npm/pnpm global install:

Copy```

openclaw update --channel stable

openclaw update --channel beta

openclaw update --channel dev

```

This updates via the corresponding npm dist-tag (`latest`, `beta`, `dev`).

When you **explicitly** switch channels with `--channel`, OpenClaw also aligns

the install method:

- `dev` ensures a git checkout (default `~/openclaw`, override with `OPENCLAW_GIT_DIR`),

updates it, and installs the global CLI from that checkout.

- `stable`/`beta` installs from npm using the matching dist-tag.

Tip: if you want stable + dev in parallel, keep two clones and point your gateway at the stable one.

## [​](#plugins-and-channels)Plugins and channels

When you switch channels with `openclaw update`, OpenClaw also syncs plugin sources:

- `dev` prefers bundled plugins from the git checkout.

- `stable` and `beta` restore npm-installed plugin packages.

## [​](#tagging-best-practices)Tagging best practices

- Tag releases you want git checkouts to land on (`vYYYY.M.D` or `vYYYY.M.D-<patch>`).

- Keep tags immutable: never move or reuse a tag.

- npm dist-tags remain the source of truth for npm installs:

`latest` → stable

- `beta` → candidate build

- `dev` → main snapshot (optional)

## [​](#macos-app-availability)macOS app availability

Beta and dev builds may **not** include a macOS app release. That’s OK:

- The git tag and npm dist-tag can still be published.

- Call out “no macOS build for this beta” in release notes or changelog.

[Deploy on Northflank](/install/northflank)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)