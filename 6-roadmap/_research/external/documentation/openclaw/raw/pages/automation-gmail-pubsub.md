---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/automation/gmail-pubsub",
    "fetched_at": "2026-02-07T10:12:19.179523",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 730738
  },
  "metadata": {
    "title": "Gmail PubSub",
    "section": "gmail-pubsub",
    "tier": 3,
    "type": "reference"
  }
}
---

- Gmail PubSub - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationAutomationGmail PubSub[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Gmail Pub/Sub -> OpenClaw](#gmail-pub%2Fsub-%3E-openclaw)- [Prereqs](#prereqs)- [Wizard (recommended)](#wizard-recommended)- [One-time setup](#one-time-setup)- [Start the watch](#start-the-watch)- [Run the push handler](#run-the-push-handler)- [Expose the handler (advanced, unsupported)](#expose-the-handler-advanced-unsupported)- [Test](#test)- [Troubleshooting](#troubleshooting)- [Cleanup](#cleanup)Automation# Gmail PubSub# [​](#gmail-pub/sub->-openclaw)Gmail Pub/Sub -> OpenClaw

Goal: Gmail watch -> Pub/Sub push -> `gog gmail watch serve` -> OpenClaw webhook.

## [​](#prereqs)Prereqs

- `gcloud` installed and logged in ([install guide](https://docs.cloud.google.com/sdk/docs/install-sdk)).

- `gog` (gogcli) installed and authorized for the Gmail account ([gogcli.sh](https://gogcli.sh/)).

- OpenClaw hooks enabled (see [Webhooks](/automation/webhook)).

- `tailscale` logged in ([tailscale.com](https://tailscale.com/)). Supported setup uses Tailscale Funnel for the public HTTPS endpoint.

Other tunnel services can work, but are DIY/unsupported and require manual wiring.

Right now, Tailscale is what we support.

Example hook config (enable Gmail preset mapping):

Copy```

{

hooks: {

enabled: true,

token: "OPENCLAW_HOOK_TOKEN",

path: "/hooks",

presets: ["gmail"],

},

}

```

To deliver the Gmail summary to a chat surface, override the preset with a mapping

that sets `deliver` + optional `channel`/`to`:

Copy```

{

hooks: {

enabled: true,

token: "OPENCLAW_HOOK_TOKEN",

presets: ["gmail"],

mappings: [

{

match: { path: "gmail" },

action: "agent",

wakeMode: "now",

name: "Gmail",

sessionKey: "hook:gmail:{{messages[0].id}}",

messageTemplate: "New email from {{messages[0].from}}\nSubject: {{messages[0].subject}}\n{{messages[0].snippet}}\n{{messages[0].body}}",

model: "openai/gpt-5.2-mini",

deliver: true,

channel: "last",

// to: "+15551234567"

},

],

},

}

```

If you want a fixed channel, set `channel` + `to`. Otherwise `channel: "last"`

uses the last delivery route (falls back to WhatsApp).

To force a cheaper model for Gmail runs, set `model` in the mapping

(`provider/model` or alias). If you enforce `agents.defaults.models`, include it there.

To set a default model and thinking level specifically for Gmail hooks, add

`hooks.gmail.model` / `hooks.gmail.thinking` in your config:

Copy```

{

hooks: {

gmail: {

model: "openrouter/meta-llama/llama-3.3-70b-instruct:free",

thinking: "off",

},

},

}

```

Notes:

- Per-hook `model`/`thinking` in the mapping still overrides these defaults.

- Fallback order: `hooks.gmail.model` → `agents.defaults.model.fallbacks` → primary (auth/rate-limit/timeouts).

- If `agents.defaults.models` is set, the Gmail model must be in the allowlist.

- Gmail hook content is wrapped with external-content safety boundaries by default.

To disable (dangerous), set `hooks.gmail.allowUnsafeExternalContent: true`.

To customize payload handling further, add `hooks.mappings` or a JS/TS transform module

under `hooks.transformsDir` (see [Webhooks](/automation/webhook)).

## [​](#wizard-recommended)Wizard (recommended)

Use the OpenClaw helper to wire everything together (installs deps on macOS via brew):

Copy```

openclaw webhooks gmail setup \

--account [[email protected]](/cdn-cgi/l/email-protection)

```

Defaults:

- Uses Tailscale Funnel for the public push endpoint.

- Writes `hooks.gmail` config for `openclaw webhooks gmail run`.

- Enables the Gmail hook preset (`hooks.presets: ["gmail"]`).

Path note: when `tailscale.mode` is enabled, OpenClaw automatically sets

`hooks.gmail.serve.path` to `/` and keeps the public path at

`hooks.gmail.tailscale.path` (default `/gmail-pubsub`) because Tailscale

strips the set-path prefix before proxying.

If you need the backend to receive the prefixed path, set

`hooks.gmail.tailscale.target` (or `--tailscale-target`) to a full URL like

`http://127.0.0.1:8788/gmail-pubsub` and match `hooks.gmail.serve.path`.

Want a custom endpoint? Use `--push-endpoint <url>` or `--tailscale off`.

Platform note: on macOS the wizard installs `gcloud`, `gogcli`, and `tailscale`

via Homebrew; on Linux install them manually first.

Gateway auto-start (recommended):

- When `hooks.enabled=true` and `hooks.gmail.account` is set, the Gateway starts

`gog gmail watch serve` on boot and auto-renews the watch.

- Set `OPENCLAW_SKIP_GMAIL_WATCHER=1` to opt out (useful if you run the daemon yourself).

- Do not run the manual daemon at the same time, or you will hit

`listen tcp 127.0.0.1:8788: bind: address already in use`.

Manual daemon (starts `gog gmail watch serve` + auto-renew):

Copy```

openclaw webhooks gmail run

```

## [​](#one-time-setup)One-time setup

- Select the GCP project **that owns the OAuth client** used by `gog`.

Copy```

gcloud auth login

gcloud config set project <project-id>

```

Note: Gmail watch requires the Pub/Sub topic to live in the same project as the OAuth client.

- Enable APIs:

Copy```

gcloud services enable gmail.googleapis.com pubsub.googleapis.com

```

- Create a topic:

Copy```

gcloud pubsub topics create gog-gmail-watch

```

- Allow Gmail push to publish:

Copy```

gcloud pubsub topics add-iam-policy-binding gog-gmail-watch \

--member=serviceAccount:[[email protected]](/cdn-cgi/l/email-protection) \

--role=roles/pubsub.publisher

```

## [​](#start-the-watch)Start the watch

Copy```

gog gmail watch start \

--account [[email protected]](/cdn-cgi/l/email-protection) \

--label INBOX \

--topic projects/<project-id>/topics/gog-gmail-watch

```

Save the `history_id` from the output (for debugging).

## [​](#run-the-push-handler)Run the push handler

Local example (shared token auth):

Copy```

gog gmail watch serve \

--account [[email protected]](/cdn-cgi/l/email-protection) \

--bind 127.0.0.1 \

--port 8788 \

--path /gmail-pubsub \

--token <shared> \

--hook-url http://127.0.0.1:18789/hooks/gmail \

--hook-token OPENCLAW_HOOK_TOKEN \

--include-body \

--max-bytes 20000

```

Notes:

- `--token` protects the push endpoint (`x-gog-token` or `?token=`).

- `--hook-url` points to OpenClaw `/hooks/gmail` (mapped; isolated run + summary to main).

- `--include-body` and `--max-bytes` control the body snippet sent to OpenClaw.

Recommended: `openclaw webhooks gmail run` wraps the same flow and auto-renews the watch.

## [​](#expose-the-handler-advanced-unsupported)Expose the handler (advanced, unsupported)

If you need a non-Tailscale tunnel, wire it manually and use the public URL in the push

subscription (unsupported, no guardrails):

Copy```

cloudflared tunnel --url http://127.0.0.1:8788 --no-autoupdate

```

Use the generated URL as the push endpoint:

Copy```

gcloud pubsub subscriptions create gog-gmail-watch-push \

--topic gog-gmail-watch \

--push-endpoint "https://<public-url>/gmail-pubsub?token=<shared>"

```

Production: use a stable HTTPS endpoint and configure Pub/Sub OIDC JWT, then run:

Copy```

gog gmail watch serve --verify-oidc --oidc-email <svc@...>

```

## [​](#test)Test

Send a message to the watched inbox:

Copy```

gog gmail send \

--account [[email protected]](/cdn-cgi/l/email-protection) \

--to [[email protected]](/cdn-cgi/l/email-protection) \

--subject "watch test" \

--body "ping"

```

Check watch state and history:

Copy```

gog gmail watch status --account [[email protected]](/cdn-cgi/l/email-protection)

gog gmail history --account [[email protected]](/cdn-cgi/l/email-protection) --since <historyId>

```

## [​](#troubleshooting)Troubleshooting

- `Invalid topicName`: project mismatch (topic not in the OAuth client project).

- `User not authorized`: missing `roles/pubsub.publisher` on the topic.

- Empty messages: Gmail push only provides `historyId`; fetch via `gog gmail history`.

## [​](#cleanup)Cleanup

Copy```

gog gmail watch stop --account [[email protected]](/cdn-cgi/l/email-protection)

gcloud pubsub subscriptions delete gog-gmail-watch-push

gcloud pubsub topics delete gog-gmail-watch

```[Webhooks](/automation/webhook)[Polls](/automation/poll)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)