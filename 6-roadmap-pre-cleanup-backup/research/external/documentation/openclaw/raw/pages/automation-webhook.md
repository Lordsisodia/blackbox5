---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/automation/webhook",
    "fetched_at": "2026-02-07T10:12:51.422567",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 612329
  },
  "metadata": {
    "title": "Webhooks",
    "section": "webhook",
    "tier": 3,
    "type": "reference"
  }
}
---

- Webhooks - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationAutomationWebhooks[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Webhooks](#webhooks)- [Enable](#enable)- [Auth](#auth)- [Endpoints](#endpoints)- [POST /hooks/wake](#post-%2Fhooks%2Fwake)- [POST /hooks/agent](#post-%2Fhooks%2Fagent)- [POST /hooks/<name> (mapped)](#post-%2Fhooks%2F%3Cname%3E-mapped)- [Responses](#responses)- [Examples](#examples)- [Use a different model](#use-a-different-model)- [Security](#security)Automation# Webhooks# [​](#webhooks)Webhooks

Gateway can expose a small HTTP webhook endpoint for external triggers.

## [​](#enable)Enable

Copy```

{

hooks: {

enabled: true,

token: "shared-secret",

path: "/hooks",

},

}

```

Notes:

- `hooks.token` is required when `hooks.enabled=true`.

- `hooks.path` defaults to `/hooks`.

## [​](#auth)Auth

Every request must include the hook token. Prefer headers:

- `Authorization: Bearer <token>` (recommended)

- `x-openclaw-token: <token>`

- `?token=<token>` (deprecated; logs a warning and will be removed in a future major release)

## [​](#endpoints)Endpoints

### [​](#post-/hooks/wake)`POST /hooks/wake`

Payload:

Copy```

{ "text": "System line", "mode": "now" }

```

- `text` **required** (string): The description of the event (e.g., “New email received”).

- `mode` optional (`now` | `next-heartbeat`): Whether to trigger an immediate heartbeat (default `now`) or wait for the next periodic check.

Effect:

- Enqueues a system event for the **main** session

- If `mode=now`, triggers an immediate heartbeat

### [​](#post-/hooks/agent)`POST /hooks/agent`

Payload:

Copy```

{

"message": "Run this",

"name": "Email",

"sessionKey": "hook:email:msg-123",

"wakeMode": "now",

"deliver": true,

"channel": "last",

"to": "+15551234567",

"model": "openai/gpt-5.2-mini",

"thinking": "low",

"timeoutSeconds": 120

}

```

- `message` **required** (string): The prompt or message for the agent to process.

- `name` optional (string): Human-readable name for the hook (e.g., “GitHub”), used as a prefix in session summaries.

- `sessionKey` optional (string): The key used to identify the agent’s session. Defaults to a random `hook:<uuid>`. Using a consistent key allows for a multi-turn conversation within the hook context.

- `wakeMode` optional (`now` | `next-heartbeat`): Whether to trigger an immediate heartbeat (default `now`) or wait for the next periodic check.

- `deliver` optional (boolean): If `true`, the agent’s response will be sent to the messaging channel. Defaults to `true`. Responses that are only heartbeat acknowledgments are automatically skipped.

- `channel` optional (string): The messaging channel for delivery. One of: `last`, `whatsapp`, `telegram`, `discord`, `slack`, `mattermost` (plugin), `signal`, `imessage`, `msteams`. Defaults to `last`.

- `to` optional (string): The recipient identifier for the channel (e.g., phone number for WhatsApp/Signal, chat ID for Telegram, channel ID for Discord/Slack/Mattermost (plugin), conversation ID for MS Teams). Defaults to the last recipient in the main session.

- `model` optional (string): Model override (e.g., `anthropic/claude-3-5-sonnet` or an alias). Must be in the allowed model list if restricted.

- `thinking` optional (string): Thinking level override (e.g., `low`, `medium`, `high`).

- `timeoutSeconds` optional (number): Maximum duration for the agent run in seconds.

Effect:

- Runs an **isolated** agent turn (own session key)

- Always posts a summary into the **main** session

- If `wakeMode=now`, triggers an immediate heartbeat

### [​](#post-/hooks/<name>-mapped)`POST /hooks/<name>` (mapped)

Custom hook names are resolved via `hooks.mappings` (see configuration). A mapping can

turn arbitrary payloads into `wake` or `agent` actions, with optional templates or

code transforms.

Mapping options (summary):

- `hooks.presets: ["gmail"]` enables the built-in Gmail mapping.

- `hooks.mappings` lets you define `match`, `action`, and templates in config.

- `hooks.transformsDir` + `transform.module` loads a JS/TS module for custom logic.

- Use `match.source` to keep a generic ingest endpoint (payload-driven routing).

- TS transforms require a TS loader (e.g. `bun` or `tsx`) or precompiled `.js` at runtime.

- Set `deliver: true` + `channel`/`to` on mappings to route replies to a chat surface

(`channel` defaults to `last` and falls back to WhatsApp).

- `allowUnsafeExternalContent: true` disables the external content safety wrapper for that hook

(dangerous; only for trusted internal sources).

- `openclaw webhooks gmail setup` writes `hooks.gmail` config for `openclaw webhooks gmail run`.

See [Gmail Pub/Sub](/automation/gmail-pubsub) for the full Gmail watch flow.

## [​](#responses)Responses

- `200` for `/hooks/wake`

- `202` for `/hooks/agent` (async run started)

- `401` on auth failure

- `400` on invalid payload

- `413` on oversized payloads

## [​](#examples)Examples

Copy```

curl -X POST http://127.0.0.1:18789/hooks/wake \

-H 'Authorization: Bearer SECRET' \

-H 'Content-Type: application/json' \

-d '{"text":"New email received","mode":"now"}'

```

Copy```

curl -X POST http://127.0.0.1:18789/hooks/agent \

-H 'x-openclaw-token: SECRET' \

-H 'Content-Type: application/json' \

-d '{"message":"Summarize inbox","name":"Email","wakeMode":"next-heartbeat"}'

```

### [​](#use-a-different-model)Use a different model

Add `model` to the agent payload (or mapping) to override the model for that run:

Copy```

curl -X POST http://127.0.0.1:18789/hooks/agent \

-H 'x-openclaw-token: SECRET' \

-H 'Content-Type: application/json' \

-d '{"message":"Summarize inbox","name":"Email","model":"openai/gpt-5.2-mini"}'

```

If you enforce `agents.defaults.models`, make sure the override model is included there.

Copy```

curl -X POST http://127.0.0.1:18789/hooks/gmail \

-H 'Authorization: Bearer SECRET' \

-H 'Content-Type: application/json' \

-d '{"source":"gmail","messages":[{"from":"Ada","subject":"Hello","snippet":"Hi"}]}'

```

## [​](#security)Security

- Keep hook endpoints behind loopback, tailnet, or trusted reverse proxy.

- Use a dedicated hook token; do not reuse gateway auth tokens.

- Avoid including sensitive raw payloads in webhook logs.

- Hook payloads are treated as untrusted and wrapped with safety boundaries by default.

If you must disable this for a specific hook, set `allowUnsafeExternalContent: true`

in that hook’s mapping (dangerous).

[Cron vs Heartbeat](/automation/cron-vs-heartbeat)[Gmail PubSub](/automation/gmail-pubsub)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)