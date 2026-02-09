---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/tools/llm-task",
    "fetched_at": "2026-02-07T10:23:48.110172",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 553819
  },
  "metadata": {
    "title": "LLM Task",
    "section": "llm-task",
    "tier": 3,
    "type": "reference"
  }
}
---

- LLM Task - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationBuilt-in toolsLLM Task[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [LLM Task](#llm-task)- [Enable the plugin](#enable-the-plugin)- [Config (optional)](#config-optional)- [Tool parameters](#tool-parameters)- [Output](#output)- [Example: Lobster workflow step](#example-lobster-workflow-step)- [Safety notes](#safety-notes)Built-in tools# LLM Task# [​](#llm-task)LLM Task

`llm-task` is an **optional plugin tool** that runs a JSON-only LLM task and

returns structured output (optionally validated against JSON Schema).

This is ideal for workflow engines like Lobster: you can add a single LLM step

without writing custom OpenClaw code for each workflow.

## [​](#enable-the-plugin)Enable the plugin

- Enable the plugin:

Copy```

{

"plugins": {

"entries": {

"llm-task": { "enabled": true }

}

}

}

```

- Allowlist the tool (it is registered with `optional: true`):

Copy```

{

"agents": {

"list": [

{

"id": "main",

"tools": { "allow": ["llm-task"] }

}

]

}

}

```

## [​](#config-optional)Config (optional)

Copy```

{

"plugins": {

"entries": {

"llm-task": {

"enabled": true,

"config": {

"defaultProvider": "openai-codex",

"defaultModel": "gpt-5.2",

"defaultAuthProfileId": "main",

"allowedModels": ["openai-codex/gpt-5.3-codex"],

"maxTokens": 800,

"timeoutMs": 30000

}

}

}

}

}

```

`allowedModels` is an allowlist of `provider/model` strings. If set, any request

outside the list is rejected.

## [​](#tool-parameters)Tool parameters

- `prompt` (string, required)

- `input` (any, optional)

- `schema` (object, optional JSON Schema)

- `provider` (string, optional)

- `model` (string, optional)

- `authProfileId` (string, optional)

- `temperature` (number, optional)

- `maxTokens` (number, optional)

- `timeoutMs` (number, optional)

## [​](#output)Output

Returns `details.json` containing the parsed JSON (and validates against

`schema` when provided).

## [​](#example-lobster-workflow-step)Example: Lobster workflow step

Copy```

openclaw.invoke --tool llm-task --action json --args-json '{

"prompt": "Given the input email, return intent and draft.",

"input": {

"subject": "Hello",

"body": "Can you help?"

},

"schema": {

"type": "object",

"properties": {

"intent": { "type": "string" },

"draft": { "type": "string" }

},

"required": ["intent", "draft"],

"additionalProperties": false

}

}'

```

## [​](#safety-notes)Safety notes

- The tool is **JSON-only** and instructs the model to output only JSON (no

code fences, no commentary).

- No tools are exposed to the model for this run.

- Treat output as untrusted unless you validate with `schema`.

- Put approvals before any side-effecting step (send, post, exec).

[Lobster](/tools/lobster)[Exec Tool](/tools/exec)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)