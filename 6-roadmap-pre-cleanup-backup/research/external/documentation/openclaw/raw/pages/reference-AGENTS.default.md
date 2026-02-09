---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/reference/AGENTS.default",
    "fetched_at": "2026-02-07T10:21:17.437377",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 566909
  },
  "metadata": {
    "title": "null",
    "section": "AGENTS.default",
    "tier": 3,
    "type": "reference"
  }
}
---

- AGENTS.default - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...Navigation[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)CLI commands- [CLI Reference](/cli)- [agent](/cli/agent)- [agents](/cli/agents)- [approvals](/cli/approvals)- [browser](/cli/browser)- [channels](/cli/channels)- [configure](/cli/configure)- [cron](/cli/cron)- [dashboard](/cli/dashboard)- [directory](/cli/directory)- [dns](/cli/dns)- [docs](/cli/docs)- [doctor](/cli/doctor)- [gateway](/cli/gateway)- [health](/cli/health)- [hooks](/cli/hooks)- [logs](/cli/logs)- [memory](/cli/memory)- [message](/cli/message)- [models](/cli/models)- [nodes](/cli/nodes)- [onboard](/cli/onboard)- [pairing](/cli/pairing)- [plugins](/cli/plugins)- [reset](/cli/reset)- [Sandbox CLI](/cli/sandbox)- [security](/cli/security)- [sessions](/cli/sessions)- [setup](/cli/setup)- [skills](/cli/skills)- [status](/cli/status)- [system](/cli/system)- [tui](/cli/tui)- [uninstall](/cli/uninstall)- [update](/cli/update)- [voicecall](/cli/voicecall)RPC and API- [RPC Adapters](/reference/rpc)- [Device Model Database](/reference/device-models)Templates- [AGENTS.default](/reference/AGENTS.default)- [AGENTS](/reference/templates/AGENTS)- [BOOT](/reference/templates/BOOT)- [BOOTSTRAP](/reference/templates/BOOTSTRAP)- [HEARTBEAT](/reference/templates/HEARTBEAT)- [IDENTITY](/reference/templates/IDENTITY)- [SOUL](/reference/templates/SOUL)- [TOOLS](/reference/templates/TOOLS)- [USER](/reference/templates/USER)Technical reference- [Wizard Reference](/reference/wizard)- [TypeBox](/concepts/typebox)- [Markdown Formatting](/concepts/markdown-formatting)- [Typing Indicators](/concepts/typing-indicators)- [Usage Tracking](/concepts/usage-tracking)- [Timezones](/concepts/timezone)- [Token Use and Costs](/token-use)Project- [Credits](/reference/credits)Release notes- [RELEASING](/reference/RELEASING)- [Tests](/reference/test)On this page- [AGENTS.md — OpenClaw Personal Assistant (default)](#agents-md-%E2%80%94-openclaw-personal-assistant-default)- [First run (recommended)](#first-run-recommended)- [Safety defaults](#safety-defaults)- [Session start (required)](#session-start-required)- [Soul (required)](#soul-required)- [Shared spaces (recommended)](#shared-spaces-recommended)- [Memory system (recommended)](#memory-system-recommended)- [Tools & skills](#tools-%26-skills)- [Backup tip (recommended)](#backup-tip-recommended)- [What OpenClaw Does](#what-openclaw-does)- [Core Skills (enable in Settings → Skills)](#core-skills-enable-in-settings-%E2%86%92-skills)- [Usage Notes](#usage-notes)Templates# AGENTS.default# [​](#agents-md-—-openclaw-personal-assistant-default)AGENTS.md — OpenClaw Personal Assistant (default)

## [​](#first-run-recommended)First run (recommended)

OpenClaw uses a dedicated workspace directory for the agent. Default: `~/.openclaw/workspace` (configurable via `agents.defaults.workspace`).

- Create the workspace (if it doesn’t already exist):

Copy```

mkdir -p ~/.openclaw/workspace

```

- Copy the default workspace templates into the workspace:

Copy```

cp docs/reference/templates/AGENTS.md ~/.openclaw/workspace/AGENTS.md

cp docs/reference/templates/SOUL.md ~/.openclaw/workspace/SOUL.md

cp docs/reference/templates/TOOLS.md ~/.openclaw/workspace/TOOLS.md

```

- Optional: if you want the personal assistant skill roster, replace AGENTS.md with this file:

Copy```

cp docs/reference/AGENTS.default.md ~/.openclaw/workspace/AGENTS.md

```

- Optional: choose a different workspace by setting `agents.defaults.workspace` (supports `~`):

Copy```

{

agents: { defaults: { workspace: "~/.openclaw/workspace" } },

}

```

## [​](#safety-defaults)Safety defaults

- Don’t dump directories or secrets into chat.

- Don’t run destructive commands unless explicitly asked.

- Don’t send partial/streaming replies to external messaging surfaces (only final replies).

## [​](#session-start-required)Session start (required)

- Read `SOUL.md`, `USER.md`, `memory.md`, and today+yesterday in `memory/`.

- Do it before responding.

## [​](#soul-required)Soul (required)

- `SOUL.md` defines identity, tone, and boundaries. Keep it current.

- If you change `SOUL.md`, tell the user.

- You are a fresh instance each session; continuity lives in these files.

## [​](#shared-spaces-recommended)Shared spaces (recommended)

- You’re not the user’s voice; be careful in group chats or public channels.

- Don’t share private data, contact info, or internal notes.

## [​](#memory-system-recommended)Memory system (recommended)

- Daily log: `memory/YYYY-MM-DD.md` (create `memory/` if needed).

- Long-term memory: `memory.md` for durable facts, preferences, and decisions.

- On session start, read today + yesterday + `memory.md` if present.

- Capture: decisions, preferences, constraints, open loops.

- Avoid secrets unless explicitly requested.

## [​](#tools-&-skills)Tools & skills

- Tools live in skills; follow each skill’s `SKILL.md` when you need it.

- Keep environment-specific notes in `TOOLS.md` (Notes for Skills).

## [​](#backup-tip-recommended)Backup tip (recommended)

If you treat this workspace as Clawd’s “memory”, make it a git repo (ideally private) so `AGENTS.md` and your memory files are backed up.

Copy```

cd ~/.openclaw/workspace

git init

git add AGENTS.md

git commit -m "Add Clawd workspace"

# Optional: add a private remote + push

```

## [​](#what-openclaw-does)What OpenClaw Does

- Runs WhatsApp gateway + Pi coding agent so the assistant can read/write chats, fetch context, and run skills via the host Mac.

- macOS app manages permissions (screen recording, notifications, microphone) and exposes the `openclaw` CLI via its bundled binary.

- Direct chats collapse into the agent’s `main` session by default; groups stay isolated as `agent:<agentId>:<channel>:group:<id>` (rooms/channels: `agent:<agentId>:<channel>:channel:<id>`); heartbeats keep background tasks alive.

## [​](#core-skills-enable-in-settings-→-skills)Core Skills (enable in Settings → Skills)

- **mcporter** — Tool server runtime/CLI for managing external skill backends.

- **Peekaboo** — Fast macOS screenshots with optional AI vision analysis.

- **camsnap** — Capture frames, clips, or motion alerts from RTSP/ONVIF security cams.

- **oracle** — OpenAI-ready agent CLI with session replay and browser control.

- **eightctl** — Control your sleep, from the terminal.

- **imsg** — Send, read, stream iMessage & SMS.

- **wacli** — WhatsApp CLI: sync, search, send.

- **discord** — Discord actions: react, stickers, polls. Use `user:<id>` or `channel:<id>` targets (bare numeric ids are ambiguous).

- **gog** — Google Suite CLI: Gmail, Calendar, Drive, Contacts.

- **spotify-player** — Terminal Spotify client to search/queue/control playback.

- **sag** — ElevenLabs speech with mac-style say UX; streams to speakers by default.

- **Sonos CLI** — Control Sonos speakers (discover/status/playback/volume/grouping) from scripts.

- **blucli** — Play, group, and automate BluOS players from scripts.

- **OpenHue CLI** — Philips Hue lighting control for scenes and automations.

- **OpenAI Whisper** — Local speech-to-text for quick dictation and voicemail transcripts.

- **Gemini CLI** — Google Gemini models from the terminal for fast Q&A.

- **bird** — X/Twitter CLI to tweet, reply, read threads, and search without a browser.

- **agent-tools** — Utility toolkit for automations and helper scripts.

## [​](#usage-notes)Usage Notes

- Prefer the `openclaw` CLI for scripting; mac app handles permissions.

- Run installs from the Skills tab; it hides the button if a binary is already present.

- Keep heartbeats enabled so the assistant can schedule reminders, monitor inboxes, and trigger camera captures.

- Canvas UI runs full-screen with native overlays. Avoid placing critical controls in the top-left/top-right/bottom edges; add explicit gutters in the layout and don’t rely on safe-area insets.

- For browser-driven verification, use `openclaw browser` (tabs/status/screenshot) with the OpenClaw-managed Chrome profile.

- For DOM inspection, use `openclaw browser eval|query|dom|snapshot` (and `--json`/`--out` when you need machine output).

- For interactions, use `openclaw browser click|type|hover|drag|select|upload|press|wait|navigate|back|evaluate|run` (click/type require snapshot refs; use `evaluate` for CSS selectors).

[Device Model Database](/reference/device-models)[AGENTS](/reference/templates/AGENTS)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)