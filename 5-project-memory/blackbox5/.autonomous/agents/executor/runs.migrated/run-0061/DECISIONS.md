# Decisions - TASK-1769957262

**Feature:** F-011 (GitHub Integration Suite)
**Run:** 61
**Date:** 2026-02-01

---

## Decision 1: Use PyGithub Library

**Context:** Need to interact with GitHub API for PR/issue/release management

**Options:**
1. **PyGithub** (Chosen): Official GitHub library for Python, mature, well-maintained
2. **requests**: Manual HTTP requests, more control but more code
3. **github3.py**: Alternative library, less popular

**Selected:** PyGithub

**Rationale:**
- Official GitHub library with active maintenance
- High-level API reduces boilerplate code
- Built-in retry logic and rate limit handling
- Comprehensive documentation
- Large community and support

**Reversibility:** LOW - Can switch to requests if needed, but would require refactoring all API calls

---

## Decision 2: Environment Variables for Sensitive Data

**Context:** Need to store GitHub credentials (PAT, webhook secret)

**Options:**
1. **Environment Variables** (Chosen): Store tokens in GITHUB_TOKEN, GITHUB_WEBHOOK_SECRET
2. **Config File Only**: Store tokens in github-config.yaml
3. **Keyring System**: Use OS keyring for secure storage

**Selected:** Environment Variables

**Rationale:**
- Security best practice (never commit tokens to git)
- Easy to rotate tokens without editing files
- Works across different environments (dev, CI, production)
- Config file can reference environment variables: `${GITHUB_TOKEN}`
- Standard pattern used by most CLI tools (gh, aws, etc.)

**Reversibility:** LOW - Can add keyring support later without breaking existing config

---

## Decision 3: Webhook Signature Verification

**Context:** Need to secure webhook endpoint from malicious payloads

**Options:**
1. **HMAC-SHA256** (Chosen): GitHub's recommended signature verification
2. **No Verification**: Accept all webhooks (insecure)
3. **IP Whitelisting**: Only accept GitHub IP addresses

**Selected:** HMAC-SHA256 Signature Verification

**Rationale:**
- GitHub's recommended security practice
- Protects against webhook spoofing
- Prevents replay attacks with timestamp checking
- Minimal performance overhead
- Industry standard for webhook security

**Reversibility:** LOW - Signature verification is foundational security feature

---

## Decision 4: Separate Libraries for Each Feature

**Context:** GitHub integration has multiple features (PR, issues, releases, webhooks, health)

**Options:**
1. **Separate Libraries** (Chosen): 7 focused libraries (client, pr_manager, issue_manager, etc.)
2. **Single Monolithic Library**: One github_integration.py with all features
3. **Plugin Architecture**: Base library with feature plugins

**Selected:** Separate Libraries

**Rationale:**
- Clear separation of concerns
- Each library can be used independently
- Easier to test and maintain
- Follows Unix philosophy (small, focused tools)
- Reduces cognitive load when reading code
- Allows selective imports (only what you need)

**Reversibility:** MEDIUM - Can consolidate into monolithic library if needed, but would reduce flexibility

---

## Decision 5: Draft PRs by Default

**Context:** Auto-created PRs should be in draft mode or ready for review?

**Options:**
1. **Draft PRs** (Chosen): Create as draft, manual convert to ready for review
2. **Ready PRs**: Create directly as ready for review
3. **Configurable**: Let user decide via config flag

**Selected:** Configurable with Draft Default

**Rationale:**
- Draft PRs allow last-minute adjustments before review
- Prevents premature notifications to reviewers
- Safety net for automated systems
- Configurable via `create_as_draft` flag in config
- User can override per-task if needed

**Reversibility:** LOW - Can change default in config or code

---

## Decision 6: Commit Categorization Patterns

**Context:** Release notes need to group commits by category (Features, Fixes, etc.)

**Options:**
1. **Regex Patterns** (Chosen): Commit message patterns (e.g., "^feat" → Features)
2. **Conventional Commits**: Enforce Conventional Commits spec
3. **AI Classification**: Use LLM to classify commits
4. **Manual Labels**: Require manual labels for all commits

**Selected:** Regex Patterns (with Config Support)

**Rationale:**
- Works with existing commit messages (no enforcement needed)
- Flexible and extensible via config
- Common pattern used by many tools
- Low overhead (no AI API calls)
- Supports custom patterns via config file

**Reversibility:** LOW - Can add AI classification or enforce Conventional Commits later

---

## Decision 7: Quality Gates Enabled by Default

**Context:** Should quality gates block merging PRs with failures?

**Options:**
1. **Quality Gates On** (Chosen): Block merge if tests fail
2. **Quality Gates Off**: Allow merge regardless of test status
3. **Warnings Only**: Post warnings but don't block

**Selected:** Quality Gates Enabled (Configurable)

**Rationale:**
- Prevents merging broken code
- Enforces quality standards
- Configurable via `quality_gates.enabled` flag
- Can be disabled if workflow requires manual approval
- Posts clear status comments explaining why merge is blocked

**Reversibility:** LOW - Configurable via yaml, easy to disable

---

## Decision 8: Webhook Server in Python

**Context:** Need HTTP server to receive GitHub webhooks

**Options:**
1. **http.server** (Chosen): Python stdlib HTTP server
2. **Flask**: Lightweight web framework
3. **FastAPI**: Modern async framework
4. **External Service**: Use ngrok or similar

**Selected:** Python stdlib http.server

**Rationale:**
- Zero dependencies beyond Python stdlib
- Sufficient for webhook endpoint (no need for full framework)
- Simple and easy to understand
- Lower resource footprint
- Can be run in background thread
- Can upgrade to Flask/FastAPI if more features needed

**Reversibility:** LOW - Can refactor to Flask/FastAPI if needed, interface stays the same

---

## Decision 9: Health Monitoring Thresholds

**Context:** What thresholds define "stale" for branches, PRs, issues?

**Options:**
1. **Conservative** (Chosen): 30 days for branches, 7 days for PRs, 14 days for issues
2. **Aggressive**: Shorter thresholds (7 days, 3 days, 7 days)
3. **Configurable**: Let user set thresholds

**Selected:** Conservative Defaults (Fully Configurable)

**Rationale:**
- 30 days for branches (long-lived feature branches are common)
- 7 days for PRs (week review cycle is reasonable)
- 14 days for issues (some issues need investigation time)
- All thresholds configurable via yaml
- Aligns with industry standards
- Reduces alert fatigue from aggressive thresholds

**Reversibility:** LOW - Configurable via yaml, easy to adjust

---

## Decision 10: Skill Usage Decision

**Context:** Task evaluation triggered bmad-dev skill with 91.5% confidence

**Options:**
1. **Invoke bmad-dev**: Follow TDD workflow (tests first, implement, refactor)
2. **Direct Execution** (Chosen): Execute with detailed task file guidance
3. **Ask Planner**: Request clarification on approach

**Selected:** Direct Execution

**Rationale:**
- Feature spec is comprehensive with detailed implementation steps
- Task file provides file structure, approach, and success criteria
- bmad-dev skill content is generic (TDD workflow)
- Direct execution more efficient than following generic skill
- Feature spec acts as "specialized skill" for this task
- Documented decision in THOUGHTS.md per skill-selection.yaml requirements

**Reversibility:** N/A - This is a meta-decision about execution approach

---

## Summary

**Decisions Made:** 10
**High Reversibility:** 0
**Medium Reversibility:** 1 (Separate Libraries)
**Low Reversibility:** 9

**Key Patterns:**
- Configurability over hard-coding (most settings are yaml-configurable)
- Security-first approach (env vars, signature verification, quality gates)
- Modularity and separation of concerns (7 focused libraries)
- Pragmatic defaults with user control (draft PRs, thresholds)
- Standard library over dependencies where possible

**No Regrets Expected:** All decisions align with best practices and are reversible if needed.

---

**End of Decisions**
