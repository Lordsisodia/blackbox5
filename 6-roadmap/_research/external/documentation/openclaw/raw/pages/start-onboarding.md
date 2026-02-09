---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/start/onboarding",
    "fetched_at": "2026-02-07T10:23:07.020145",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 508056
  },
  "metadata": {
    "title": "Onboarding (macOS App)",
    "section": "onboarding",
    "tier": 3,
    "type": "reference"
  }
}
---

- Onboarding (macOS App) - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationFirst stepsOnboarding (macOS App)[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [OpenClaw](/)- [Features](/concepts/features)- [Showcase](/start/showcase)First steps- [Getting Started](/start/getting-started)- [Onboarding: CLI](/start/wizard)- [Onboarding: macOS App](/start/onboarding)Guides- [Personal Assistant Setup](/start/openclaw)On this page- [Onboarding (macOS App)](#onboarding-macos-app)First steps# Onboarding (macOS App)# [​](#onboarding-macos-app)Onboarding (macOS App)

This doc describes the **current** first‑run onboarding flow. The goal is a

smooth “day 0” experience: pick where the Gateway runs, connect auth, run the

wizard, and let the agent bootstrap itself.

1[](#)Approve macOS warning2[](#)Approve find local networks3[](#)Welcome and security notice4[](#)Local vs RemoteWhere does the **Gateway** run?

- **This Mac (Local only):** onboarding can run OAuth flows and write credentials

locally.

- **Remote (over SSH/Tailnet):** onboarding does **not** run OAuth locally;

credentials must exist on the gateway host.

- **Configure later:** skip setup and leave the app unconfigured.

**Gateway auth tip:**

- The wizard now generates a **token** even for loopback, so local WS clients must authenticate.

- If you disable auth, any local process can connect; use that only on fully trusted machines.

- Use a **token** for multi‑machine access or non‑loopback binds.

5[](#)PermissionsOnboarding requests TCC permissions needed for:

- Automation (AppleScript)

- Notifications

- Accessibility

- Screen Recording

- Microphone

- Speech Recognition

- Camera

- Location

6[](#)CLIThis step is optional

The app can install the global `openclaw` CLI via npm/pnpm so terminal

workflows and launchd tasks work out of the box.7[](#)Onboarding Chat (dedicated session)After setup, the app opens a dedicated onboarding chat session so the agent can

introduce itself and guide next steps. This keeps first‑run guidance separate

from your normal conversation. See [Bootstrapping](/start/bootstrapping) for

what happens on the gateway host during the first agent run.[Onboarding: CLI](/start/wizard)[Personal Assistant Setup](/start/openclaw)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)