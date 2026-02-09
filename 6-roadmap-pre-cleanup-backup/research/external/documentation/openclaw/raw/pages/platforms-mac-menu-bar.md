---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/platforms/mac/menu-bar",
    "fetched_at": "2026-02-07T10:20:58.961025",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 497870
  },
  "metadata": {
    "title": "Menu Bar",
    "section": "menu-bar",
    "tier": 3,
    "type": "reference"
  }
}
---

- Menu Bar - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationmacOS companion appMenu Bar[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Platforms overview- [Platforms](/platforms)- [macOS App](/platforms/macos)- [Linux App](/platforms/linux)- [Windows (WSL2)](/platforms/windows)- [Android App](/platforms/android)- [iOS App](/platforms/ios)macOS companion app- [macOS Dev Setup](/platforms/mac/dev-setup)- [Menu Bar](/platforms/mac/menu-bar)- [Voice Wake](/platforms/mac/voicewake)- [Voice Overlay](/platforms/mac/voice-overlay)- [WebChat](/platforms/mac/webchat)- [Canvas](/platforms/mac/canvas)- [Gateway Lifecycle](/platforms/mac/child-process)- [Health Checks](/platforms/mac/health)- [Menu Bar Icon](/platforms/mac/icon)- [macOS Logging](/platforms/mac/logging)- [macOS Permissions](/platforms/mac/permissions)- [Remote Control](/platforms/mac/remote)- [macOS Signing](/platforms/mac/signing)- [macOS Release](/platforms/mac/release)- [Gateway on macOS](/platforms/mac/bundled-gateway)- [macOS IPC](/platforms/mac/xpc)- [Skills](/platforms/mac/skills)- [Peekaboo Bridge](/platforms/mac/peekaboo)On this page- [Menu Bar Status Logic](#menu-bar-status-logic)- [What is shown](#what-is-shown)- [State model](#state-model)- [IconState enum (Swift)](#iconstate-enum-swift)- [ActivityKind → glyph](#activitykind-%E2%86%92-glyph)- [Visual mapping](#visual-mapping)- [Status row text (menu)](#status-row-text-menu)- [Event ingestion](#event-ingestion)- [Debug override](#debug-override)- [Testing checklist](#testing-checklist)macOS companion app# Menu Bar# [​](#menu-bar-status-logic)Menu Bar Status Logic

## [​](#what-is-shown)What is shown

- We surface the current agent work state in the menu bar icon and in the first status row of the menu.

- Health status is hidden while work is active; it returns when all sessions are idle.

- The “Nodes” block in the menu lists **devices** only (paired nodes via `node.list`), not client/presence entries.

- A “Usage” section appears under Context when provider usage snapshots are available.

## [​](#state-model)State model

- Sessions: events arrive with `runId` (per-run) plus `sessionKey` in the payload. The “main” session is the key `main`; if absent, we fall back to the most recently updated session.

- Priority: main always wins. If main is active, its state is shown immediately. If main is idle, the most recently active non‑main session is shown. We do not flip‑flop mid‑activity; we only switch when the current session goes idle or main becomes active.

- Activity kinds:

`job`: high‑level command execution (`state: started|streaming|done|error`).

- `tool`: `phase: start|result` with `toolName` and `meta/args`.

## [​](#iconstate-enum-swift)IconState enum (Swift)

- `idle`

- `workingMain(ActivityKind)`

- `workingOther(ActivityKind)`

- `overridden(ActivityKind)` (debug override)

### [​](#activitykind-→-glyph)ActivityKind → glyph

- `exec` → 💻

- `read` → 📄

- `write` → ✍️

- `edit` → 📝

- `attach` → 📎

- default → 🛠️

### [​](#visual-mapping)Visual mapping

- `idle`: normal critter.

- `workingMain`: badge with glyph, full tint, leg “working” animation.

- `workingOther`: badge with glyph, muted tint, no scurry.

- `overridden`: uses the chosen glyph/tint regardless of activity.

## [​](#status-row-text-menu)Status row text (menu)

- While work is active: `<Session role> · <activity label>`

Examples: `Main · exec: pnpm test`, `Other · read: apps/macos/Sources/OpenClaw/AppState.swift`.

- When idle: falls back to the health summary.

## [​](#event-ingestion)Event ingestion

- Source: control‑channel `agent` events (`ControlChannel.handleAgentEvent`).

- Parsed fields:

`stream: "job"` with `data.state` for start/stop.

- `stream: "tool"` with `data.phase`, `name`, optional `meta`/`args`.

- Labels:

`exec`: first line of `args.command`.

- `read`/`write`: shortened path.

- `edit`: path plus inferred change kind from `meta`/diff counts.

- fallback: tool name.

## [​](#debug-override)Debug override

- Settings ▸ Debug ▸ “Icon override” picker:

`System (auto)` (default)

- `Working: main` (per tool kind)

- `Working: other` (per tool kind)

- `Idle`

- Stored via `@AppStorage("iconOverride")`; mapped to `IconState.overridden`.

## [​](#testing-checklist)Testing checklist

- Trigger main session job: verify icon switches immediately and status row shows main label.

- Trigger non‑main session job while main idle: icon/status shows non‑main; stays stable until it finishes.

- Start main while other active: icon flips to main instantly.

- Rapid tool bursts: ensure badge does not flicker (TTL grace on tool results).

- Health row reappears once all sessions idle.

[macOS Dev Setup](/platforms/mac/dev-setup)[Voice Wake](/platforms/mac/voicewake)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)