---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/tools/skills-config",
    "fetched_at": "2026-02-07T10:11:46.406154",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 528063
  },
  "metadata": {
    "title": "Skills Config",
    "section": "skills-config",
    "tier": 2,
    "type": "reference"
  }
}
---

- Skills Config - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationSkills and extensionsSkills Config[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Skills Config](#skills-config)- [Fields](#fields)- [Notes](#notes)- [Sandboxed skills + env vars](#sandboxed-skills-%2B-env-vars)Skills and extensions# Skills Config# [​](#skills-config)Skills Config

All skills-related configuration lives under `skills` in `~/.openclaw/openclaw.json`.

Copy```

{

skills: {

allowBundled: ["gemini", "peekaboo"],

load: {

extraDirs: ["~/Projects/agent-scripts/skills", "~/Projects/oss/some-skill-pack/skills"],

watch: true,

watchDebounceMs: 250,

},

install: {

preferBrew: true,

nodeManager: "npm", // npm | pnpm | yarn | bun (Gateway runtime still Node; bun not recommended)

},

entries: {

"nano-banana-pro": {

enabled: true,

apiKey: "GEMINI_KEY_HERE",

env: {

GEMINI_API_KEY: "GEMINI_KEY_HERE",

},

},

peekaboo: { enabled: true },

sag: { enabled: false },

},

},

}

```

## [​](#fields)Fields

- `allowBundled`: optional allowlist for **bundled** skills only. When set, only

bundled skills in the list are eligible (managed/workspace skills unaffected).

- `load.extraDirs`: additional skill directories to scan (lowest precedence).

- `load.watch`: watch skill folders and refresh the skills snapshot (default: true).

- `load.watchDebounceMs`: debounce for skill watcher events in milliseconds (default: 250).

- `install.preferBrew`: prefer brew installers when available (default: true).

- `install.nodeManager`: node installer preference (`npm` | `pnpm` | `yarn` | `bun`, default: npm).

This only affects **skill installs**; the Gateway runtime should still be Node

(Bun not recommended for WhatsApp/Telegram).

- `entries.<skillKey>`: per-skill overrides.

Per-skill fields:

- `enabled`: set `false` to disable a skill even if it’s bundled/installed.

- `env`: environment variables injected for the agent run (only if not already set).

- `apiKey`: optional convenience for skills that declare a primary env var.

## [​](#notes)Notes

- Keys under `entries` map to the skill name by default. If a skill defines

`metadata.openclaw.skillKey`, use that key instead.

- Changes to skills are picked up on the next agent turn when the watcher is enabled.

### [​](#sandboxed-skills-+-env-vars)Sandboxed skills + env vars

When a session is **sandboxed**, skill processes run inside Docker. The sandbox

does **not** inherit the host `process.env`.

Use one of:

- `agents.defaults.sandbox.docker.env` (or per-agent `agents.list[].sandbox.docker.env`)

- bake the env into your custom sandbox image

Global `env` and `skills.entries.<skill>.env/apiKey` apply to **host** runs only.[Skills](/tools/skills)[ClawHub](/tools/clawhub)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)