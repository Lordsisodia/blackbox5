---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/tools/browser-login",
    "fetched_at": "2026-02-07T10:23:14.450589",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 515346
  },
  "metadata": {
    "title": "Browser Login",
    "section": "browser-login",
    "tier": 3,
    "type": "reference"
  }
}
---

- Browser Login - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationBrowserBrowser Login[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Browser login + X/Twitter posting](#browser-login-%2B-x%2Ftwitter-posting)- [Manual login (recommended)](#manual-login-recommended)- [Which Chrome profile is used?](#which-chrome-profile-is-used)- [X/Twitter: recommended flow](#x%2Ftwitter-recommended-flow)- [Sandboxing + host browser access](#sandboxing-%2B-host-browser-access)Browser# Browser Login# [​](#browser-login-+-x/twitter-posting)Browser login + X/Twitter posting

## [​](#manual-login-recommended)Manual login (recommended)

When a site requires login, **sign in manually** in the **host** browser profile (the openclaw browser).

Do **not** give the model your credentials. Automated logins often trigger anti‑bot defenses and can lock the account.

Back to the main browser docs: [Browser](/tools/browser).

## [​](#which-chrome-profile-is-used)Which Chrome profile is used?

OpenClaw controls a **dedicated Chrome profile** (named `openclaw`, orange‑tinted UI). This is separate from your daily browser profile.

Two easy ways to access it:

- **Ask the agent to open the browser** and then log in yourself.

- **Open it via CLI**:

Copy```

openclaw browser start

openclaw browser open https://x.com

```

If you have multiple profiles, pass `--browser-profile <name>` (the default is `openclaw`).

## [​](#x/twitter-recommended-flow)X/Twitter: recommended flow

- **Read/search/threads:** use the **bird** CLI skill (no browser, stable).

Repo: [https://github.com/steipete/bird](https://github.com/steipete/bird)

- **Post updates:** use the **host** browser (manual login).

## [​](#sandboxing-+-host-browser-access)Sandboxing + host browser access

Sandboxed browser sessions are **more likely** to trigger bot detection. For X/Twitter (and other strict sites), prefer the **host** browser.

If the agent is sandboxed, the browser tool defaults to the sandbox. To allow host control:

Copy```

{

agents: {

defaults: {

sandbox: {

mode: "non-main",

browser: {

allowHostControl: true,

},

},

},

},

}

```

Then target the host browser:

Copy```

openclaw browser open https://x.com --browser-profile openclaw --target host

```

Or disable sandboxing for the agent that posts updates.[Browser (OpenClaw-managed)](/tools/browser)[Chrome Extension](/tools/chrome-extension)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)