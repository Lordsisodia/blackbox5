---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/tools/apply-patch",
    "fetched_at": "2026-02-07T10:23:12.409366",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 498414
  },
  "metadata": {
    "title": "apply_patch Tool",
    "section": "apply-patch",
    "tier": 3,
    "type": "reference"
  }
}
---

- apply_patch Tool - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationBuilt-in toolsapply_patch Tool[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [apply_patch tool](#apply_patch-tool)- [Parameters](#parameters)- [Notes](#notes)- [Example](#example)Built-in tools# apply_patch Tool# [​](#apply_patch-tool)apply_patch tool

Apply file changes using a structured patch format. This is ideal for multi-file

or multi-hunk edits where a single `edit` call would be brittle.

The tool accepts a single `input` string that wraps one or more file operations:

Copy```

*** Begin Patch

*** Add File: path/to/file.txt

+line 1

+line 2

*** Update File: src/app.ts

@@

-old line

+new line

*** Delete File: obsolete.txt

*** End Patch

```

## [​](#parameters)Parameters

- `input` (required): Full patch contents including `*** Begin Patch` and `*** End Patch`.

## [​](#notes)Notes

- Paths are resolved relative to the workspace root.

- Use `*** Move to:` within an `*** Update File:` hunk to rename files.

- `*** End of File` marks an EOF-only insert when needed.

- Experimental and disabled by default. Enable with `tools.exec.applyPatch.enabled`.

- OpenAI-only (including OpenAI Codex). Optionally gate by model via

`tools.exec.applyPatch.allowModels`.

- Config is only under `tools.exec`.

## [​](#example)Example

Copy```

{

"tool": "apply_patch",

"input": "*** Begin Patch\n*** Update File: src/index.ts\n@@\n-const foo = 1\n+const foo = 2\n*** End Patch"

}

```[Web Tools](/tools/web)[Elevated Mode](/tools/elevated)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)