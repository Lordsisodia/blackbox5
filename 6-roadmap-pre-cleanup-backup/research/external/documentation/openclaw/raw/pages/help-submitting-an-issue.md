---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/help/submitting-an-issue",
    "fetched_at": "2026-02-07T10:18:57.973771",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 561663
  },
  "metadata": {
    "title": "Submitting an Issue",
    "section": "submitting-an-issue",
    "tier": 3,
    "type": "reference"
  }
}
---

- Submitting an Issue - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationDeveloper workflowsSubmitting an Issue[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Help- [Help](/help)- [Troubleshooting](/help/troubleshooting)- [FAQ](/help/faq)Community- [OpenClaw Lore](/start/lore)Environment and debugging- [Node.js](/install/node)- [Environment Variables](/environment)- [Debugging](/debugging)- [Testing](/testing)- [Scripts](/scripts)- [Session Management Deep Dive](/reference/session-management-compaction)Developer workflows- [Setup](/start/setup)- [Submitting a PR](/help/submitting-a-pr)- [Submitting an Issue](/help/submitting-an-issue)Docs meta- [Docs Hubs](/start/hubs)- [Docs directory](/start/docs-directory)On this page- [Submitting an Issue](#submitting-an-issue)- [What to include](#what-to-include)- [Templates](#templates)- [Bug report](#bug-report)- [Security issue](#security-issue)- [Regression report](#regression-report)- [Feature request](#feature-request)- [Enhancement](#enhancement)- [Investigation](#investigation)- [Submitting a fix PR](#submitting-a-fix-pr)Developer workflows# Submitting an Issue## [​](#submitting-an-issue)Submitting an Issue

Clear, concise issues speed up diagnosis and fixes. Include the following for bugs, regressions, or feature gaps:

### [​](#what-to-include)What to include

-  Title: area & symptom

-  Minimal repro steps

-  Expected vs actual

-  Impact & severity

-  Environment: OS, runtime, versions, config

-  Evidence: redacted logs, screenshots (non-PII)

-  Scope: new, regression, or longstanding

-  Code word: lobster-biscuit in your issue

-  Searched codebase & GitHub for existing issue

-  Confirmed not recently fixed/addressed (esp. security)

-  Claims backed by evidence or repro

Be brief. Terseness > perfect grammar.

Validation (run/fix before PR):

- `pnpm lint`

- `pnpm check`

- `pnpm build`

- `pnpm test`

- If protocol code: `pnpm protocol:check`

### [​](#templates)Templates

#### [​](#bug-report)Bug report

Copy```

- [ ] Minimal repro

- [ ] Expected vs actual

- [ ] Environment

- [ ] Affected channels, where not seen

- [ ] Logs/screenshots (redacted)

- [ ] Impact/severity

- [ ] Workarounds

### Summary

### Repro Steps

### Expected

### Actual

### Environment

### Logs/Evidence

### Impact

### Workarounds

```

#### [​](#security-issue)Security issue

Copy```

### Summary

### Impact

### Versions

### Repro Steps (safe to share)

### Mitigation/workaround

### Evidence (redacted)

```

*Avoid secrets/exploit details in public. For sensitive issues, minimize detail and request private disclosure.*

#### [​](#regression-report)Regression report

Copy```

### Summary

### Last Known Good

### First Known Bad

### Repro Steps

### Expected

### Actual

### Environment

### Logs/Evidence

### Impact

```

#### [​](#feature-request)Feature request

Copy```

### Summary

### Problem

### Proposed Solution

### Alternatives

### Impact

### Evidence/examples

```

#### [​](#enhancement)Enhancement

Copy```

### Summary

### Current vs Desired Behavior

### Rationale

### Alternatives

### Evidence/examples

```

#### [​](#investigation)Investigation

Copy```

### Summary

### Symptoms

### What Was Tried

### Environment

### Logs/Evidence

### Impact

```

### [​](#submitting-a-fix-pr)Submitting a fix PR

Issue before PR is optional. Include details in PR if skipping. Keep the PR focused, note issue number, add tests or explain absence, document behavior changes/risks, include redacted logs/screenshots as proof, and run proper validation before submitting.[Submitting a PR](/help/submitting-a-pr)[Docs Hubs](/start/hubs)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)