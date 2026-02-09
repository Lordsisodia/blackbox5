---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/tools/browser-linux-troubleshooting",
    "fetched_at": "2026-02-07T10:23:13.887207",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 595131
  },
  "metadata": {
    "title": "Browser Troubleshooting",
    "section": "browser-linux-troubleshooting",
    "tier": 3,
    "type": "reference"
  }
}
---

- Browser Troubleshooting - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationBrowserBrowser Troubleshooting[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Tools](/tools)Built-in tools- [Lobster](/tools/lobster)- [LLM Task](/tools/llm-task)- [Exec Tool](/tools/exec)- [Web Tools](/tools/web)- [apply_patch Tool](/tools/apply-patch)- [Elevated Mode](/tools/elevated)- [Thinking Levels](/tools/thinking)- [Reactions](/tools/reactions)Browser- [Browser (OpenClaw-managed)](/tools/browser)- [Browser Login](/tools/browser-login)- [Chrome Extension](/tools/chrome-extension)- [Browser Troubleshooting](/tools/browser-linux-troubleshooting)Agent coordination- [Agent Send](/tools/agent-send)- [Sub-Agents](/tools/subagents)- [Multi-Agent Sandbox & Tools](/multi-agent-sandbox-tools)Skills and extensions- [Slash Commands](/tools/slash-commands)- [Skills](/tools/skills)- [Skills Config](/tools/skills-config)- [ClawHub](/tools/clawhub)- [Plugins](/plugin)- [Voice Call Plugin](/plugins/voice-call)- [Zalo Personal Plugin](/plugins/zalouser)Automation- [Hooks](/hooks)- [SOUL Evil Hook](/hooks/soul-evil)- [Cron Jobs](/automation/cron-jobs)- [Cron vs Heartbeat](/automation/cron-vs-heartbeat)- [Webhooks](/automation/webhook)- [Gmail PubSub](/automation/gmail-pubsub)- [Polls](/automation/poll)- [Auth Monitoring](/automation/auth-monitoring)Media and devices- [Nodes](/nodes)- [Image and Media Support](/nodes/images)- [Audio and Voice Notes](/nodes/audio)- [Camera Capture](/nodes/camera)- [Talk Mode](/nodes/talk)- [Voice Wake](/nodes/voicewake)- [Location Command](/nodes/location-command)On this page- [Browser Troubleshooting (Linux)](#browser-troubleshooting-linux)- [Problem: “Failed to start Chrome CDP on port 18800”](#problem-%E2%80%9Cfailed-to-start-chrome-cdp-on-port-18800%E2%80%9D)- [Root Cause](#root-cause)- [Solution 1: Install Google Chrome (Recommended)](#solution-1-install-google-chrome-recommended)- [Solution 2: Use Snap Chromium with Attach-Only Mode](#solution-2-use-snap-chromium-with-attach-only-mode)- [Verifying the Browser Works](#verifying-the-browser-works)- [Config Reference](#config-reference)- [Problem: “Chrome extension relay is running, but no tab is connected”](#problem-%E2%80%9Cchrome-extension-relay-is-running-but-no-tab-is-connected%E2%80%9D)Browser# Browser Troubleshooting# [​](#browser-troubleshooting-linux)Browser Troubleshooting (Linux)

## [​](#problem-“failed-to-start-chrome-cdp-on-port-18800”)Problem: “Failed to start Chrome CDP on port 18800”

OpenClaw’s browser control server fails to launch Chrome/Brave/Edge/Chromium with the error:

Copy```

{"error":"Error: Failed to start Chrome CDP on port 18800 for profile \"openclaw\"."}

```

### [​](#root-cause)Root Cause

On Ubuntu (and many Linux distros), the default Chromium installation is a **snap package**. Snap’s AppArmor confinement interferes with how OpenClaw spawns and monitors the browser process.

The `apt install chromium` command installs a stub package that redirects to snap:

Copy```

Note, selecting 'chromium-browser' instead of 'chromium'

chromium-browser is already the newest version (2:1snap1-0ubuntu2).

```

This is NOT a real browser — it’s just a wrapper.

### [​](#solution-1-install-google-chrome-recommended)Solution 1: Install Google Chrome (Recommended)

Install the official Google Chrome `.deb` package, which is not sandboxed by snap:

Copy```

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo dpkg -i google-chrome-stable_current_amd64.deb

sudo apt --fix-broken install -y  # if there are dependency errors

```

Then update your OpenClaw config (`~/.openclaw/openclaw.json`):

Copy```

{

"browser": {

"enabled": true,

"executablePath": "/usr/bin/google-chrome-stable",

"headless": true,

"noSandbox": true

}

}

```

### [​](#solution-2-use-snap-chromium-with-attach-only-mode)Solution 2: Use Snap Chromium with Attach-Only Mode

If you must use snap Chromium, configure OpenClaw to attach to a manually-started browser:

- Update config:

Copy```

{

"browser": {

"enabled": true,

"attachOnly": true,

"headless": true,

"noSandbox": true

}

}

```

- Start Chromium manually:

Copy```

chromium-browser --headless --no-sandbox --disable-gpu \

--remote-debugging-port=18800 \

--user-data-dir=$HOME/.openclaw/browser/openclaw/user-data \

about:blank &

```

- Optionally create a systemd user service to auto-start Chrome:

Copy```

# ~/.config/systemd/user/openclaw-browser.service

[Unit]

Description=OpenClaw Browser (Chrome CDP)

After=network.target

[Service]

ExecStart=/snap/bin/chromium --headless --no-sandbox --disable-gpu --remote-debugging-port=18800 --user-data-dir=%h/.openclaw/browser/openclaw/user-data about:blank

Restart=on-failure

RestartSec=5

[Install]

WantedBy=default.target

```

Enable with: `systemctl --user enable --now openclaw-browser.service`

### [​](#verifying-the-browser-works)Verifying the Browser Works

Check status:

Copy```

curl -s http://127.0.0.1:18791/ | jq '{running, pid, chosenBrowser}'

```

Test browsing:

Copy```

curl -s -X POST http://127.0.0.1:18791/start

curl -s http://127.0.0.1:18791/tabs

```

### [​](#config-reference)Config Reference

OptionDescriptionDefault`browser.enabled`Enable browser control`true``browser.executablePath`Path to a Chromium-based browser binary (Chrome/Brave/Edge/Chromium)auto-detected (prefers default browser when Chromium-based)`browser.headless`Run without GUI`false``browser.noSandbox`Add `--no-sandbox` flag (needed for some Linux setups)`false``browser.attachOnly`Don’t launch browser, only attach to existing`false``browser.cdpPort`Chrome DevTools Protocol port`18800`

### [​](#problem-“chrome-extension-relay-is-running-but-no-tab-is-connected”)Problem: “Chrome extension relay is running, but no tab is connected”

You’re using the `chrome` profile (extension relay). It expects the OpenClaw

browser extension to be attached to a live tab.

Fix options:

- **Use the managed browser:** `openclaw browser start --browser-profile openclaw`

(or set `browser.defaultProfile: "openclaw"`).

- **Use the extension relay:** install the extension, open a tab, and click the

OpenClaw extension icon to attach it.

Notes:

- The `chrome` profile uses your **system default Chromium browser** when possible.

- Local `openclaw` profiles auto-assign `cdpPort`/`cdpUrl`; only set those for remote CDP.

[Chrome Extension](/tools/chrome-extension)[Agent Send](/tools/agent-send)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)