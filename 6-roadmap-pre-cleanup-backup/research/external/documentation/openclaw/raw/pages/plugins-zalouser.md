---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/plugins/zalouser",
    "fetched_at": "2026-02-07T10:11:43.784394",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 544573
  },
  "metadata": {
    "title": "Zalo Personal Plugin",
    "section": "zalouser",
    "tier": 2,
    "type": "reference"
  }
}
---

- Zalo Personal Plugin - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationSkills and extensionsZalo Personal Plugin[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Zalo Personal (plugin)](#zalo-personal-plugin)- [Naming](#naming)- [Where it runs](#where-it-runs)- [Install](#install)- [Option A: install from npm](#option-a-install-from-npm)- [Option B: install from a local folder (dev)](#option-b-install-from-a-local-folder-dev)- [Prerequisite: zca-cli](#prerequisite-zca-cli)- [Config](#config)- [CLI](#cli)- [Agent tool](#agent-tool)Skills and extensions# Zalo Personal Plugin# [​](#zalo-personal-plugin)Zalo Personal (plugin)

Zalo Personal support for OpenClaw via a plugin, using `zca-cli` to automate a normal Zalo user account.

**Warning:** Unofficial automation may lead to account suspension/ban. Use at your own risk.

## [​](#naming)Naming

Channel id is `zalouser` to make it explicit this automates a **personal Zalo user account** (unofficial). We keep `zalo` reserved for a potential future official Zalo API integration.

## [​](#where-it-runs)Where it runs

This plugin runs **inside the Gateway process**.

If you use a remote Gateway, install/configure it on the **machine running the Gateway**, then restart the Gateway.

## [​](#install)Install

### [​](#option-a-install-from-npm)Option A: install from npm

Copy```

openclaw plugins install @openclaw/zalouser

```

Restart the Gateway afterwards.

### [​](#option-b-install-from-a-local-folder-dev)Option B: install from a local folder (dev)

Copy```

openclaw plugins install ./extensions/zalouser

cd ./extensions/zalouser && pnpm install

```

Restart the Gateway afterwards.

## [​](#prerequisite-zca-cli)Prerequisite: zca-cli

The Gateway machine must have `zca` on `PATH`:

Copy```

zca --version

```

## [​](#config)Config

Channel config lives under `channels.zalouser` (not `plugins.entries.*`):

Copy```

{

channels: {

zalouser: {

enabled: true,

dmPolicy: "pairing",

},

},

}

```

## [​](#cli)CLI

Copy```

openclaw channels login --channel zalouser

openclaw channels logout --channel zalouser

openclaw channels status --probe

openclaw message send --channel zalouser --target <threadId> --message "Hello from OpenClaw"

openclaw directory peers list --channel zalouser --query "name"

```

## [​](#agent-tool)Agent tool

Tool name: `zalouser`

Actions: `send`, `image`, `link`, `friends`, `groups`, `me`, `status`[Voice Call Plugin](/plugins/voice-call)[Hooks](/hooks)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)