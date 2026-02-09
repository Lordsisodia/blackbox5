---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/tools/lobster",
    "fetched_at": "2026-02-07T10:23:48.741618",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 784861
  },
  "metadata": {
    "title": "Lobster",
    "section": "lobster",
    "tier": 3,
    "type": "reference"
  }
}
---

- Lobster - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationBuilt-in toolsLobster[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Lobster](#lobster)- [Hook](#hook)- [Why](#why)- [Why a DSL instead of plain programs?](#why-a-dsl-instead-of-plain-programs)- [How it works](#how-it-works)- [Pattern: small CLI + JSON pipes + approvals](#pattern-small-cli-%2B-json-pipes-%2B-approvals)- [JSON-only LLM steps (llm-task)](#json-only-llm-steps-llm-task)- [Workflow files (.lobster)](#workflow-files-lobster)- [Install Lobster](#install-lobster)- [Enable the tool](#enable-the-tool)- [Example: Email triage](#example-email-triage)- [Tool parameters](#tool-parameters)- [run](#run)- [resume](#resume)- [Optional inputs](#optional-inputs)- [Output envelope](#output-envelope)- [Approvals](#approvals)- [OpenProse](#openprose)- [Safety](#safety)- [Troubleshooting](#troubleshooting)- [Learn more](#learn-more)- [Case study: community workflows](#case-study-community-workflows)Built-in tools# LobsterTyped workflow runtime for OpenClaw — composable pipelines with approval gates.# [​](#lobster)Lobster

Lobster is a workflow shell that lets OpenClaw run multi-step tool sequences as a single, deterministic operation with explicit approval checkpoints.

## [​](#hook)Hook

Your assistant can build the tools that manage itself. Ask for a workflow, and 30 minutes later you have a CLI plus pipelines that run as one call. Lobster is the missing piece: deterministic pipelines, explicit approvals, and resumable state.

## [​](#why)Why

Today, complex workflows require many back-and-forth tool calls. Each call costs tokens, and the LLM has to orchestrate every step. Lobster moves that orchestration into a typed runtime:

- **One call instead of many**: OpenClaw runs one Lobster tool call and gets a structured result.

- **Approvals built in**: Side effects (send email, post comment) halt the workflow until explicitly approved.

- **Resumable**: Halted workflows return a token; approve and resume without re-running everything.

## [​](#why-a-dsl-instead-of-plain-programs)Why a DSL instead of plain programs?

Lobster is intentionally small. The goal is not “a new language,” it’s a predictable, AI-friendly pipeline spec with first-class approvals and resume tokens.

- **Approve/resume is built in**: A normal program can prompt a human, but it can’t *pause and resume* with a durable token without you inventing that runtime yourself.

- **Determinism + auditability**: Pipelines are data, so they’re easy to log, diff, replay, and review.

- **Constrained surface for AI**: A tiny grammar + JSON piping reduces “creative” code paths and makes validation realistic.

- **Safety policy baked in**: Timeouts, output caps, sandbox checks, and allowlists are enforced by the runtime, not each script.

- **Still programmable**: Each step can call any CLI or script. If you want JS/TS, generate `.lobster` files from code.

## [​](#how-it-works)How it works

OpenClaw launches the local `lobster` CLI in **tool mode** and parses a JSON envelope from stdout.

If the pipeline pauses for approval, the tool returns a `resumeToken` so you can continue later.

## [​](#pattern-small-cli-+-json-pipes-+-approvals)Pattern: small CLI + JSON pipes + approvals

Build tiny commands that speak JSON, then chain them into a single Lobster call. (Example command names below — swap in your own.)

Copy```

inbox list --json

inbox categorize --json

inbox apply --json

```

Copy```

{

"action": "run",

"pipeline": "exec --json --shell 'inbox list --json' | exec --stdin json --shell 'inbox categorize --json' | exec --stdin json --shell 'inbox apply --json' | approve --preview-from-stdin --limit 5 --prompt 'Apply changes?'",

"timeoutMs": 30000

}

```

If the pipeline requests approval, resume with the token:

Copy```

{

"action": "resume",

"token": "<resumeToken>",

"approve": true

}

```

AI triggers the workflow; Lobster executes the steps. Approval gates keep side effects explicit and auditable.

Example: map input items into tool calls:

Copy```

gog.gmail.search --query 'newer_than:1d' \

| openclaw.invoke --tool message --action send --each --item-key message --args-json '{"provider":"telegram","to":"..."}'

```

## [​](#json-only-llm-steps-llm-task)JSON-only LLM steps (llm-task)

For workflows that need a **structured LLM step**, enable the optional

`llm-task` plugin tool and call it from Lobster. This keeps the workflow

deterministic while still letting you classify/summarize/draft with a model.

Enable the tool:

Copy```

{

"plugins": {

"entries": {

"llm-task": { "enabled": true }

}

},

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

Use it in a pipeline:

Copy```

openclaw.invoke --tool llm-task --action json --args-json '{

"prompt": "Given the input email, return intent and draft.",

"input": { "subject": "Hello", "body": "Can you help?" },

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

See [LLM Task](/tools/llm-task) for details and configuration options.

## [​](#workflow-files-lobster)Workflow files (.lobster)

Lobster can run YAML/JSON workflow files with `name`, `args`, `steps`, `env`, `condition`, and `approval` fields. In OpenClaw tool calls, set `pipeline` to the file path.

Copy```

name: inbox-triage

args:

tag:

default: "family"

steps:

- id: collect

command: inbox list --json

- id: categorize

command: inbox categorize --json

stdin: $collect.stdout

- id: approve

command: inbox apply --approve

stdin: $categorize.stdout

approval: required

- id: execute

command: inbox apply --execute

stdin: $categorize.stdout

condition: $approve.approved

```

Notes:

- `stdin: $step.stdout` and `stdin: $step.json` pass a prior step’s output.

- `condition` (or `when`) can gate steps on `$step.approved`.

## [​](#install-lobster)Install Lobster

Install the Lobster CLI on the **same host** that runs the OpenClaw Gateway (see the [Lobster repo](https://github.com/openclaw/lobster)), and ensure `lobster` is on `PATH`.

If you want to use a custom binary location, pass an **absolute** `lobsterPath` in the tool call.

## [​](#enable-the-tool)Enable the tool

Lobster is an **optional** plugin tool (not enabled by default).

Recommended (additive, safe):

Copy```

{

"tools": {

"alsoAllow": ["lobster"]

}

}

```

Or per-agent:

Copy```

{

"agents": {

"list": [

{

"id": "main",

"tools": {

"alsoAllow": ["lobster"]

}

}

]

}

}

```

Avoid using `tools.allow: ["lobster"]` unless you intend to run in restrictive allowlist mode.

Note: allowlists are opt-in for optional plugins. If your allowlist only names

plugin tools (like `lobster`), OpenClaw keeps core tools enabled. To restrict core

tools, include the core tools or groups you want in the allowlist too.

## [​](#example-email-triage)Example: Email triage

Without Lobster:

Copy```

User: "Check my email and draft replies"

→ openclaw calls gmail.list

→ LLM summarizes

→ User: "draft replies to #2 and #5"

→ LLM drafts

→ User: "send #2"

→ openclaw calls gmail.send

(repeat daily, no memory of what was triaged)

```

With Lobster:

Copy```

{

"action": "run",

"pipeline": "email.triage --limit 20",

"timeoutMs": 30000

}

```

Returns a JSON envelope (truncated):

Copy```

{

"ok": true,

"status": "needs_approval",

"output": [{ "summary": "5 need replies, 2 need action" }],

"requiresApproval": {

"type": "approval_request",

"prompt": "Send 2 draft replies?",

"items": [],

"resumeToken": "..."

}

}

```

User approves → resume:

Copy```

{

"action": "resume",

"token": "<resumeToken>",

"approve": true

}

```

One workflow. Deterministic. Safe.

## [​](#tool-parameters)Tool parameters

### [​](#run)`run`

Run a pipeline in tool mode.

Copy```

{

"action": "run",

"pipeline": "gog.gmail.search --query 'newer_than:1d' | email.triage",

"cwd": "/path/to/workspace",

"timeoutMs": 30000,

"maxStdoutBytes": 512000

}

```

Run a workflow file with args:

Copy```

{

"action": "run",

"pipeline": "/path/to/inbox-triage.lobster",

"argsJson": "{\"tag\":\"family\"}"

}

```

### [​](#resume)`resume`

Continue a halted workflow after approval.

Copy```

{

"action": "resume",

"token": "<resumeToken>",

"approve": true

}

```

### [​](#optional-inputs)Optional inputs

- `lobsterPath`: Absolute path to the Lobster binary (omit to use `PATH`).

- `cwd`: Working directory for the pipeline (defaults to the current process working directory).

- `timeoutMs`: Kill the subprocess if it exceeds this duration (default: 20000).

- `maxStdoutBytes`: Kill the subprocess if stdout exceeds this size (default: 512000).

- `argsJson`: JSON string passed to `lobster run --args-json` (workflow files only).

## [​](#output-envelope)Output envelope

Lobster returns a JSON envelope with one of three statuses:

- `ok` → finished successfully

- `needs_approval` → paused; `requiresApproval.resumeToken` is required to resume

- `cancelled` → explicitly denied or cancelled

The tool surfaces the envelope in both `content` (pretty JSON) and `details` (raw object).

## [​](#approvals)Approvals

If `requiresApproval` is present, inspect the prompt and decide:

- `approve: true` → resume and continue side effects

- `approve: false` → cancel and finalize the workflow

Use `approve --preview-from-stdin --limit N` to attach a JSON preview to approval requests without custom jq/heredoc glue. Resume tokens are now compact: Lobster stores workflow resume state under its state dir and hands back a small token key.

## [​](#openprose)OpenProse

OpenProse pairs well with Lobster: use `/prose` to orchestrate multi-agent prep, then run a Lobster pipeline for deterministic approvals. If a Prose program needs Lobster, allow the `lobster` tool for sub-agents via `tools.subagents.tools`. See [OpenProse](/prose).

## [​](#safety)Safety

- **Local subprocess only** — no network calls from the plugin itself.

- **No secrets** — Lobster doesn’t manage OAuth; it calls OpenClaw tools that do.

- **Sandbox-aware** — disabled when the tool context is sandboxed.

- **Hardened** — `lobsterPath` must be absolute if specified; timeouts and output caps enforced.

## [​](#troubleshooting)Troubleshooting

- **`lobster subprocess timed out`** → increase `timeoutMs`, or split a long pipeline.

- **`lobster output exceeded maxStdoutBytes`** → raise `maxStdoutBytes` or reduce output size.

- **`lobster returned invalid JSON`** → ensure the pipeline runs in tool mode and prints only JSON.

- **`lobster failed (code …)`** → run the same pipeline in a terminal to inspect stderr.

## [​](#learn-more)Learn more

- [Plugins](/plugin)

- [Plugin tool authoring](/plugins/agent-tools)

## [​](#case-study-community-workflows)Case study: community workflows

One public example: a “second brain” CLI + Lobster pipelines that manage three Markdown vaults (personal, partner, shared). The CLI emits JSON for stats, inbox listings, and stale scans; Lobster chains those commands into workflows like `weekly-review`, `inbox-triage`, `memory-consolidation`, and `shared-task-sync`, each with approval gates. AI handles judgment (categorization) when available and falls back to deterministic rules when not.

- Thread: [https://x.com/plattenschieber/status/2014508656335770033](https://x.com/plattenschieber/status/2014508656335770033)

- Repo: [https://github.com/bloomedai/brain-cli](https://github.com/bloomedai/brain-cli)

[Tools](/tools)[LLM Task](/tools/llm-task)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)