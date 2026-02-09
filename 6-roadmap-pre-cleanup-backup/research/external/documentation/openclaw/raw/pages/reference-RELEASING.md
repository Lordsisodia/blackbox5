---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/reference/RELEASING",
    "fetched_at": "2026-02-07T10:21:48.194115",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 543940
  },
  "metadata": {
    "title": "null",
    "section": "RELEASING",
    "tier": 3,
    "type": "reference"
  }
}
---

- RELEASING - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...Navigation[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [Release Checklist (npm + macOS)](#release-checklist-npm-%2B-macos)- [Operator trigger](#operator-trigger)- [Troubleshooting (notes from 2.0.0-beta2 release)](#troubleshooting-notes-from-2-0-0-beta2-release)- [Plugin publish scope (npm)](#plugin-publish-scope-npm)Release notes# RELEASING# [​](#release-checklist-npm-+-macos)Release Checklist (npm + macOS)

Use `pnpm` (Node 22+) from the repo root. Keep the working tree clean before tagging/publishing.

## [​](#operator-trigger)Operator trigger

When the operator says “release”, immediately do this preflight (no extra questions unless blocked):

- Read this doc and `docs/platforms/mac/release.md`.

- Load env from `~/.profile` and confirm `SPARKLE_PRIVATE_KEY_FILE` + App Store Connect vars are set (SPARKLE_PRIVATE_KEY_FILE should live in `~/.profile`).

- Use Sparkle keys from `~/Library/CloudStorage/Dropbox/Backup/Sparkle` if needed.

- **Version & metadata**

-  Bump `package.json` version (e.g., `2026.1.29`).

-  Run `pnpm plugins:sync` to align extension package versions + changelogs.

-  Update CLI/version strings: [`src/cli/program.ts`](https://github.com/openclaw/openclaw/blob/main/src/cli/program.ts) and the Baileys user agent in [`src/provider-web.ts`](https://github.com/openclaw/openclaw/blob/main/src/provider-web.ts).

-  Confirm package metadata (name, description, repository, keywords, license) and `bin` map points to [`openclaw.mjs`](https://github.com/openclaw/openclaw/blob/main/openclaw.mjs) for `openclaw`.

-  If dependencies changed, run `pnpm install` so `pnpm-lock.yaml` is current.

- **Build & artifacts**

-  If A2UI inputs changed, run `pnpm canvas:a2ui:bundle` and commit any updated [`src/canvas-host/a2ui/a2ui.bundle.js`](https://github.com/openclaw/openclaw/blob/main/src/canvas-host/a2ui/a2ui.bundle.js).

-  `pnpm run build` (regenerates `dist/`).

-  Verify npm package `files` includes all required `dist/*` folders (notably `dist/node-host/**` and `dist/acp/**` for headless node + ACP CLI).

-  Confirm `dist/build-info.json` exists and includes the expected `commit` hash (CLI banner uses this for npm installs).

-  Optional: `npm pack --pack-destination /tmp` after the build; inspect the tarball contents and keep it handy for the GitHub release (do **not** commit it).

- **Changelog & docs**

-  Update `CHANGELOG.md` with user-facing highlights (create the file if missing); keep entries strictly descending by version.

-  Ensure README examples/flags match current CLI behavior (notably new commands or options).

- **Validation**

-  `pnpm build`

-  `pnpm check`

-  `pnpm test` (or `pnpm test:coverage` if you need coverage output)

-  `pnpm release:check` (verifies npm pack contents)

-  `OPENCLAW_INSTALL_SMOKE_SKIP_NONROOT=1 pnpm test:install:smoke` (Docker install smoke test, fast path; required before release)

If the immediate previous npm release is known broken, set `OPENCLAW_INSTALL_SMOKE_PREVIOUS=<last-good-version>` or `OPENCLAW_INSTALL_SMOKE_SKIP_PREVIOUS=1` for the preinstall step.

-  (Optional) Full installer smoke (adds non-root + CLI coverage): `pnpm test:install:smoke`

-  (Optional) Installer E2E (Docker, runs `curl -fsSL https://openclaw.ai/install.sh | bash`, onboards, then runs real tool calls):

`pnpm test:install:e2e:openai` (requires `OPENAI_API_KEY`)

- `pnpm test:install:e2e:anthropic` (requires `ANTHROPIC_API_KEY`)

- `pnpm test:install:e2e` (requires both keys; runs both providers)

-  (Optional) Spot-check the web gateway if your changes affect send/receive paths.

- **macOS app (Sparkle)**

-  Build + sign the macOS app, then zip it for distribution.

-  Generate the Sparkle appcast (HTML notes via [`scripts/make_appcast.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/make_appcast.sh)) and update `appcast.xml`.

-  Keep the app zip (and optional dSYM zip) ready to attach to the GitHub release.

-  Follow [macOS release](/platforms/mac/release) for the exact commands and required env vars.

`APP_BUILD` must be numeric + monotonic (no `-beta`) so Sparkle compares versions correctly.

- If notarizing, use the `openclaw-notary` keychain profile created from App Store Connect API env vars (see [macOS release](/platforms/mac/release)).

- **Publish (npm)**

-  Confirm git status is clean; commit and push as needed.

-  `npm login` (verify 2FA) if needed.

-  `npm publish --access public` (use `--tag beta` for pre-releases).

-  Verify the registry: `npm view openclaw version`, `npm view openclaw dist-tags`, and `npx -y [[email protected]](/cdn-cgi/l/email-protection) --version` (or `--help`).

### [​](#troubleshooting-notes-from-2-0-0-beta2-release)Troubleshooting (notes from 2.0.0-beta2 release)

- **npm pack/publish hangs or produces huge tarball**: the macOS app bundle in `dist/OpenClaw.app` (and release zips) get swept into the package. Fix by whitelisting publish contents via `package.json` `files` (include dist subdirs, docs, skills; exclude app bundles). Confirm with `npm pack --dry-run` that `dist/OpenClaw.app` is not listed.

- **npm auth web loop for dist-tags**: use legacy auth to get an OTP prompt:

`NPM_CONFIG_AUTH_TYPE=legacy npm dist-tag add [[email protected]](/cdn-cgi/l/email-protection) latest`

- **`npx` verification fails with `ECOMPROMISED: Lock compromised`**: retry with a fresh cache:

`NPM_CONFIG_CACHE=/tmp/npm-cache-$(date +%s) npx -y [[email protected]](/cdn-cgi/l/email-protection) --version`

- **Tag needs repointing after a late fix**: force-update and push the tag, then ensure the GitHub release assets still match:

`git tag -f vX.Y.Z && git push -f origin vX.Y.Z`

- **GitHub release + appcast**

-  Tag and push: `git tag vX.Y.Z && git push origin vX.Y.Z` (or `git push --tags`).

-  Create/refresh the GitHub release for `vX.Y.Z` with **title `openclaw X.Y.Z`** (not just the tag); body should include the **full** changelog section for that version (Highlights + Changes + Fixes), inline (no bare links), and **must not repeat the title inside the body**.

-  Attach artifacts: `npm pack` tarball (optional), `OpenClaw-X.Y.Z.zip`, and `OpenClaw-X.Y.Z.dSYM.zip` (if generated).

-  Commit the updated `appcast.xml` and push it (Sparkle feeds from main).

-  From a clean temp directory (no `package.json`), run `npx -y [[email protected]](/cdn-cgi/l/email-protection) send --help` to confirm install/CLI entrypoints work.

-  Announce/share release notes.

## [​](#plugin-publish-scope-npm)Plugin publish scope (npm)

We only publish **existing npm plugins** under the `@openclaw/*` scope. Bundled

plugins that are not on npm stay **disk-tree only** (still shipped in

`extensions/**`).

Process to derive the list:

- `npm search @openclaw --json` and capture the package names.

- Compare with `extensions/*/package.json` names.

- Publish only the **intersection** (already on npm).

Current npm plugin list (update as needed):

- @openclaw/bluebubbles

- @openclaw/diagnostics-otel

- @openclaw/discord

- @openclaw/feishu

- @openclaw/lobster

- @openclaw/matrix

- @openclaw/msteams

- @openclaw/nextcloud-talk

- @openclaw/nostr

- @openclaw/voice-call

- @openclaw/zalo

- @openclaw/zalouser

Release notes must also call out **new optional bundled plugins** that are **not

on by default** (example: `tlon`).[Credits](/reference/credits)[Tests](/reference/test)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)