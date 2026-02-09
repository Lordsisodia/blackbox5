---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/help/submitting-a-pr",
    "fetched_at": "2026-02-07T10:18:56.646503",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 737011
  },
  "metadata": {
    "title": "Submitting a PR",
    "section": "submitting-a-pr",
    "tier": 3,
    "type": "reference"
  }
}
---

- Submitting a PR - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationDeveloper workflowsSubmitting a PR[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Help- [Help](/help)- [Troubleshooting](/help/troubleshooting)- [FAQ](/help/faq)Community- [OpenClaw Lore](/start/lore)Environment and debugging- [Node.js](/install/node)- [Environment Variables](/environment)- [Debugging](/debugging)- [Testing](/testing)- [Scripts](/scripts)- [Session Management Deep Dive](/reference/session-management-compaction)Developer workflows- [Setup](/start/setup)- [Submitting a PR](/help/submitting-a-pr)- [Submitting an Issue](/help/submitting-an-issue)Docs meta- [Docs Hubs](/start/hubs)- [Docs directory](/start/docs-directory)On this page- [What makes a good PR](#what-makes-a-good-pr)- [Baseline validation commands (run/fix failures for your change)](#baseline-validation-commands-run%2Ffix-failures-for-your-change)- [Progressive disclosure](#progressive-disclosure)- [Common PR types: specifics](#common-pr-types-specifics)- [Checklist](#checklist)- [General PR Template](#general-pr-template)- [PR Type templates (replace with your type)](#pr-type-templates-replace-with-your-type)- [Fix](#fix)- [Feature](#feature)- [Refactor](#refactor)- [Chore/Maintenance](#chore%2Fmaintenance)- [Docs](#docs)- [Test](#test)- [Perf](#perf)- [UX/UI](#ux%2Fui)- [Infra/Build](#infra%2Fbuild)- [Security](#security)Developer workflows# Submitting a PRGood PRs are easy to review: reviewers should quickly know the intent, verify behavior, and land changes safely. This guide covers concise, high-signal submissions for human and LLM review.

## [​](#what-makes-a-good-pr)What makes a good PR

-  Explain the problem, why it matters, and the change.

-  Keep changes focused. Avoid broad refactors.

-  Summarize user-visible/config/default changes.

-  List test coverage, skips, and reasons.

-  Add evidence: logs, screenshots, or recordings (UI/UX).

-  Code word: put “lobster-biscuit” in the PR description if you read this guide.

-  Run/fix relevant `pnpm` commands before creating PR.

-  Search codebase and GitHub for related functionality/issues/fixes.

-  Base claims on evidence or observation.

-  Good title: verb + scope + outcome (e.g., `Docs: add PR and issue templates`).

Be concise; concise review > grammar. Omit any non-applicable sections.

### [​](#baseline-validation-commands-run/fix-failures-for-your-change)Baseline validation commands (run/fix failures for your change)

- `pnpm lint`

- `pnpm check`

- `pnpm build`

- `pnpm test`

- Protocol changes: `pnpm protocol:check`

## [​](#progressive-disclosure)Progressive disclosure

- Top: summary/intent

- Next: changes/risks

- Next: test/verification

- Last: implementation/evidence

## [​](#common-pr-types-specifics)Common PR types: specifics

-  Fix: Add repro, root cause, verification.

-  Feature: Add use cases, behavior/demos/screenshots (UI).

-  Refactor: State “no behavior change”, list what moved/simplified.

-  Chore: State why (e.g., build time, CI, dependencies).

-  Docs: Before/after context, link updated page, run `pnpm format`.

-  Test: What gap is covered; how it prevents regressions.

-  Perf: Add before/after metrics, and how measured.

-  UX/UI: Screenshots/video, note accessibility impact.

-  Infra/Build: Environments/validation.

-  Security: Summarize risk, repro, verification, no sensitive data. Grounded claims only.

## [​](#checklist)Checklist

-  Clear problem/intent

-  Focused scope

-  List behavior changes

-  List and result of tests

-  Manual test steps (when applicable)

-  No secrets/private data

-  Evidence-based

## [​](#general-pr-template)General PR Template

Copy```

#### Summary

#### Behavior Changes

#### Codebase and GitHub Search

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.

2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:

- Submitter effort (self-reported):

- Agent notes (optional, cite evidence):

```

## [​](#pr-type-templates-replace-with-your-type)PR Type templates (replace with your type)

### [​](#fix)Fix

Copy```

#### Summary

#### Repro Steps

#### Root Cause

#### Behavior Changes

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.

2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:

- Submitter effort:

- Agent notes:

```

### [​](#feature)Feature

Copy```

#### Summary

#### Use Cases

#### Behavior Changes

#### Existing Functionality Check

- [ ] I searched the codebase for existing functionality.

Searches performed (1-3 bullets):

-

-

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.

2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:

- Submitter effort:

- Agent notes:

```

### [​](#refactor)Refactor

Copy```

#### Summary

#### Scope

#### No Behavior Change Statement

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.

2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:

- Submitter effort:

- Agent notes:

```

### [​](#chore/maintenance)Chore/Maintenance

Copy```

#### Summary

#### Why This Matters

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.

2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:

- Submitter effort:

- Agent notes:

```

### [​](#docs)Docs

Copy```

#### Summary

#### Pages Updated

#### Before/After

#### Formatting

pnpm format

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:

- Submitter effort:

- Agent notes:

```

### [​](#test)Test

Copy```

#### Summary

#### Gap Covered

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.

2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:

- Submitter effort:

- Agent notes:

```

### [​](#perf)Perf

Copy```

#### Summary

#### Baseline

#### After

#### Measurement Method

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.

2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:

- Submitter effort:

- Agent notes:

```

### [​](#ux/ui)UX/UI

Copy```

#### Summary

#### Screenshots or Video

#### Accessibility Impact

#### Tests

#### Manual Testing

### Prerequisites

-

### Steps

1.

2. **Sign-Off**

- Models used:

- Submitter effort:

- Agent notes:

```

### [​](#infra/build)Infra/Build

Copy```

#### Summary

#### Environments Affected

#### Validation Steps

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.

2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:

- Submitter effort:

- Agent notes:

```

### [​](#security)Security

Copy```

#### Summary

#### Risk Summary

#### Repro Steps

#### Mitigation or Fix

#### Verification

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.

2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:

- Submitter effort:

- Agent notes:

```[Setup](/start/setup)[Submitting an Issue](/help/submitting-an-issue)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)