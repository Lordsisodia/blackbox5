---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/start/showcase",
    "fetched_at": "2026-02-07T10:23:09.399443",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 713534
  },
  "metadata": {
    "title": "Showcase",
    "section": "showcase",
    "tier": 3,
    "type": "guide"
  }
}
---

- Showcase - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationOverviewShowcase[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [OpenClaw](/)- [Features](/concepts/features)- [Showcase](/start/showcase)First steps- [Getting Started](/start/getting-started)- [Onboarding: CLI](/start/wizard)- [Onboarding: macOS App](/start/onboarding)Guides- [Personal Assistant Setup](/start/openclaw)On this page- [Showcase](#showcase)- [🎥 OpenClaw in Action](#-openclaw-in-action)- [🆕 Fresh from Discord](#-fresh-from-discord)- [🤖 Automation & Workflows](#-automation-%26-workflows)- [🧠 Knowledge & Memory](#-knowledge-%26-memory)- [🎙️ Voice & Phone](#-voice-%26-phone)- [🏗️ Infrastructure & Deployment](#-infrastructure-%26-deployment)- [🏠 Home & Hardware](#-home-%26-hardware)- [🌟 Community Projects](#-community-projects)- [Submit Your Project](#submit-your-project)Overview# ShowcaseReal-world OpenClaw projects from the community# [​](#showcase)Showcase

Real projects from the community. See what people are building with OpenClaw.

**Want to be featured?** Share your project in [#showcase on Discord](https://discord.gg/clawd) or [tag @openclaw on X](https://x.com/openclaw).

## [​](#-openclaw-in-action)🎥 OpenClaw in Action

Full setup walkthrough (28m) by VelvetShark.

[Watch on YouTube](https://www.youtube.com/watch?v=SaWSPZoPX34)

[Watch on YouTube](https://www.youtube.com/watch?v=mMSKQvlmFuQ)

[Watch on YouTube](https://www.youtube.com/watch?v=5kkIJNUGFho)

## [​](#-fresh-from-discord)🆕 Fresh from Discord

[## PR Review → Telegram Feedback**@bangnokia** • `review` `github` `telegram`OpenCode finishes the change → opens a PR → OpenClaw reviews the diff and replies in Telegram with “minor suggestions” plus a clear merge verdict (including critical fixes to apply first).](https://x.com/i/status/2010878524543131691)[## Wine Cellar Skill in Minutes**@prades_maxime** • `skills` `local` `csv`Asked “Robby” (@openclaw) for a local wine cellar skill. It requests a sample CSV export + where to store it, then builds/tests the skill fast (962 bottles in the example).](https://x.com/i/status/2010916352454791216)[## Tesco Shop Autopilot**@marchattonhere** • `automation` `browser` `shopping`Weekly meal plan → regulars → book delivery slot → confirm order. No APIs, just browser control.](https://x.com/i/status/2009724862470689131)[## SNAG Screenshot-to-Markdown**@am-will** • `devtools` `screenshots` `markdown`Hotkey a screen region → Gemini vision → instant Markdown in your clipboard.](https://github.com/am-will/snag)[## Agents UI**@kitze** • `ui` `skills` `sync`Desktop app to manage skills/commands across Agents, Claude, Codex, and OpenClaw.](https://releaseflow.net/kitze/agents-ui)[## Telegram Voice Notes (papla.media)**Community** • `voice` `tts` `telegram`Wraps papla.media TTS and sends results as Telegram voice notes (no annoying autoplay).](https://papla.media/docs)[## CodexMonitor**@odrobnik** • `devtools` `codex` `brew`Homebrew-installed helper to list/inspect/watch local OpenAI Codex sessions (CLI + VS Code).](https://clawhub.com/odrobnik/codexmonitor)[## Bambu 3D Printer Control**@tobiasbischoff** • `hardware` `3d-printing` `skill`Control and troubleshoot BambuLab printers: status, jobs, camera, AMS, calibration, and more.](https://clawhub.com/tobiasbischoff/bambu-cli)[## Vienna Transport (Wiener Linien)**@hjanuschka** • `travel` `transport` `skill`Real-time departures, disruptions, elevator status, and routing for Vienna’s public transport.](https://clawhub.com/hjanuschka/wienerlinien)[## ParentPay School Meals**@George5562** • `automation` `browser` `parenting`Automated UK school meal booking via ParentPay. Uses mouse coordinates for reliable table cell clicking.](#)[## R2 Upload (Send Me My Files)**@julianengel** • `files` `r2` `presigned-urls`Upload to Cloudflare R2/S3 and generate secure presigned download links. Perfect for remote OpenClaw instances.](https://clawhub.com/skills/r2-upload)[## iOS App via Telegram**@coard** • `ios` `xcode` `testflight`Built a complete iOS app with maps and voice recording, deployed to TestFlight entirely via Telegram chat.](#)[## Oura Ring Health Assistant**@AS** • `health` `oura` `calendar`Personal AI health assistant integrating Oura ring data with calendar, appointments, and gym schedule.](#)[## Kev's Dream Team (14+ Agents)**@adam91holt** • `multi-agent` `orchestration` `architecture` `manifesto`14+ agents under one gateway with Opus 4.5 orchestrator delegating to Codex workers. Comprehensive technical write-up](https://github.com/adam91holt/orchestrated-ai-articles) covering the Dream Team roster, model selection, sandboxing, webhooks, heartbeats, and delegation flows. [Clawdspace](https://github.com/adam91holt/clawdspace) for agent sandboxing. [Blog post](https://adams-ai-journey.ghost.io/2026-the-year-of-the-orchestrator/).[## Linear CLI**@NessZerra** • `devtools` `linear` `cli` `issues`CLI for Linear that integrates with agentic workflows (Claude Code, OpenClaw). Manage issues, projects, and workflows from the terminal. First external PR merged!](https://github.com/Finesssee/linear-cli)[## Beeper CLI**@jules** • `messaging` `beeper` `cli` `automation`Read, send, and archive messages via Beeper Desktop. Uses Beeper local MCP API so agents can manage all your chats (iMessage, WhatsApp, etc.) in one place.](https://github.com/blqke/beepcli)

## [​](#-automation-&-workflows)🤖 Automation & Workflows

[## Winix Air Purifier Control**@antonplex** • `automation` `hardware` `air-quality`Claude Code discovered and confirmed the purifier controls, then OpenClaw takes over to manage room air quality.](https://x.com/antonplex/status/2010518442471006253)[## Pretty Sky Camera Shots**@signalgaining** • `automation` `camera` `skill` `images`Triggered by a roof camera: ask OpenClaw to snap a sky photo whenever it looks pretty — it designed a skill and took the shot.](https://x.com/signalgaining/status/2010523120604746151)[## Visual Morning Briefing Scene**@buddyhadry** • `automation` `briefing` `images` `telegram`A scheduled prompt generates a single “scene” image each morning (weather, tasks, date, favorite post/quote) via a OpenClaw persona.](https://x.com/buddyhadry/status/2010005331925954739)[## Padel Court Booking**@joshp123** • `automation` `booking` `cli`Playtomic availability checker + booking CLI. Never miss an open court again.](https://github.com/joshp123/padel-cli)## Accounting Intake**Community** • `automation` `email` `pdf`Collects PDFs from email, preps documents for tax consultant. Monthly accounting on autopilot.[## Couch Potato Dev Mode**@davekiss** • `telegram` `website` `migration` `astro`Rebuilt entire personal site via Telegram while watching Netflix — Notion → Astro, 18 posts migrated, DNS to Cloudflare. Never opened a laptop.](https://davekiss.com)## Job Search Agent**@attol8** • `automation` `api` `skill`Searches job listings, matches against CV keywords, and returns relevant opportunities with links. Built in 30 minutes using JSearch API.[## Jira Skill Builder**@jdrhyne** • `automation` `jira` `skill` `devtools`OpenClaw connected to Jira, then generated a new skill on the fly (before it existed on ClawHub).](https://x.com/jdrhyne/status/2008336434827002232)[## Todoist Skill via Telegram**@iamsubhrajyoti** • `automation` `todoist` `skill` `telegram`Automated Todoist tasks and had OpenClaw generate the skill directly in Telegram chat.](https://x.com/iamsubhrajyoti/status/2009949389884920153)## TradingView Analysis**@bheem1798** • `finance` `browser` `automation`Logs into TradingView via browser automation, screenshots charts, and performs technical analysis on demand. No API needed—just browser control.## Slack Auto-Support**@henrymascot** • `slack` `automation` `support`Watches company Slack channel, responds helpfully, and forwards notifications to Telegram. Autonomously fixed a production bug in a deployed app without being asked.

## [​](#-knowledge-&-memory)🧠 Knowledge & Memory

[## xuezh Chinese Learning**@joshp123** • `learning` `voice` `skill`Chinese learning engine with pronunciation feedback and study flows via OpenClaw.](https://github.com/joshp123/xuezh)## WhatsApp Memory Vault**Community** • `memory` `transcription` `indexing`Ingests full WhatsApp exports, transcribes 1k+ voice notes, cross-checks with git logs, outputs linked markdown reports.[## Karakeep Semantic Search**@jamesbrooksco** • `search` `vector` `bookmarks`Adds vector search to Karakeep bookmarks using Qdrant + OpenAI/Ollama embeddings.](https://github.com/jamesbrooksco/karakeep-semantic-search)## Inside-Out-2 Memory**Community** • `memory` `beliefs` `self-model`Separate memory manager that turns session files into memories → beliefs → evolving self model.

## [​](#-voice-&-phone)🎙️ Voice & Phone

[## Clawdia Phone Bridge**@alejandroOPI** • `voice` `vapi` `bridge`Vapi voice assistant ↔ OpenClaw HTTP bridge. Near real-time phone calls with your agent.](https://github.com/alejandroOPI/clawdia-bridge)[## OpenRouter Transcription**@obviyus** • `transcription` `multilingual` `skill`Multi-lingual audio transcription via OpenRouter (Gemini, etc). Available on ClawHub.](https://clawhub.com/obviyus/openrouter-transcribe)

## [​](#-infrastructure-&-deployment)🏗️ Infrastructure & Deployment

[## Home Assistant Add-on**@ngutman** • `homeassistant` `docker` `raspberry-pi`OpenClaw gateway running on Home Assistant OS with SSH tunnel support and persistent state.](https://github.com/ngutman/openclaw-ha-addon)[## Home Assistant Skill**ClawHub** • `homeassistant` `skill` `automation`Control and automate Home Assistant devices via natural language.](https://clawhub.com/skills/homeassistant)[## Nix Packaging**@openclaw** • `nix` `packaging` `deployment`Batteries-included nixified OpenClaw configuration for reproducible deployments.](https://github.com/openclaw/nix-openclaw)[## CalDAV Calendar**ClawHub** • `calendar` `caldav` `skill`Calendar skill using khal/vdirsyncer. Self-hosted calendar integration.](https://clawhub.com/skills/caldav-calendar)

## [​](#-home-&-hardware)🏠 Home & Hardware

[## GoHome Automation**@joshp123** • `home` `nix` `grafana`Nix-native home automation with OpenClaw as the interface, plus beautiful Grafana dashboards.](https://github.com/joshp123/gohome)[## Roborock Vacuum**@joshp123** • `vacuum` `iot` `plugin`Control your Roborock robot vacuum through natural conversation.](https://github.com/joshp123/gohome/tree/main/plugins/roborock)

## [​](#-community-projects)🌟 Community Projects

[## StarSwap Marketplace**Community** • `marketplace` `astronomy` `webapp`Full astronomy gear marketplace. Built with/around the OpenClaw ecosystem.](https://star-swap.com/)

## [​](#submit-your-project)Submit Your Project

Have something to share? We’d love to feature it!

1[](#)Share ItPost in [#showcase on Discord](https://discord.gg/clawd) or [tweet @openclaw](https://x.com/openclaw)2[](#)Include DetailsTell us what it does, link to the repo/demo, share a screenshot if you have one3[](#)Get FeaturedWe’ll add standout projects to this page[Features](/concepts/features)[Getting Started](/start/getting-started)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)