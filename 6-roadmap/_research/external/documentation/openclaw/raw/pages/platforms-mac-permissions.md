---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/permissions",
    "fetched_at": "2026-02-07T10:11:03.185189",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 483214
  },
  "metadata": {
    "title": "macOS Permissions",
    "section": "permissions",
    "tier": 1,
    "type": "reference"
  }
}
---

- macOS Permissions - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appmacOS Permissions[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [macOS permissions (TCC)](#macos-permissions-tcc)- [Requirements for stable permissions](#requirements-for-stable-permissions)- [Recovery checklist when prompts disappear](#recovery-checklist-when-prompts-disappear)- [Files and folders permissions (Desktop/Documents/Downloads)](#files-and-folders-permissions-desktop%2Fdocuments%2Fdownloads)macOS companion app# macOS Permissions# [​](#macos-permissions-tcc)macOS permissions (TCC)

macOS permission grants are fragile. TCC associates a permission grant with the

app’s code signature, bundle identifier, and on-disk path. If any of those change,

macOS treats the app as new and may drop or hide prompts.

## [​](#requirements-for-stable-permissions)Requirements for stable permissions

- Same path: run the app from a fixed location (for OpenClaw, `dist/OpenClaw.app`).

- Same bundle identifier: changing the bundle ID creates a new permission identity.

- Signed app: unsigned or ad-hoc signed builds do not persist permissions.

- Consistent signature: use a real Apple Development or Developer ID certificate

so the signature stays stable across rebuilds.

Ad-hoc signatures generate a new identity every build. macOS will forget previous

grants, and prompts can disappear entirely until the stale entries are cleared.

## [​](#recovery-checklist-when-prompts-disappear)Recovery checklist when prompts disappear

- Quit the app.

- Remove the app entry in System Settings -> Privacy & Security.

- Relaunch the app from the same path and re-grant permissions.

- If the prompt still does not appear, reset TCC entries with `tccutil` and try again.

- Some permissions only reappear after a full macOS restart.

Example resets (replace bundle ID as needed):

Copy```

sudo tccutil reset Accessibility bot.molt.mac

sudo tccutil reset ScreenCapture bot.molt.mac

sudo tccutil reset AppleEvents

```

## [​](#files-and-folders-permissions-desktop/documents/downloads)Files and folders permissions (Desktop/Documents/Downloads)

macOS may also gate Desktop, Documents, and Downloads for terminal/background processes. If file reads or directory listings hang, grant access to the same process context that performs file operations (for example Terminal/iTerm, LaunchAgent-launched app, or SSH process).

Workaround: move files into the OpenClaw workspace (`~/.openclaw/workspace`) if you want to avoid per-folder grants.

If you are testing permissions, always sign with a real certificate. Ad-hoc

builds are only acceptable for quick local runs where permissions do not matter.[macOS Logging](/platforms/mac/logging)[Remote Control](/platforms/mac/remote)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)