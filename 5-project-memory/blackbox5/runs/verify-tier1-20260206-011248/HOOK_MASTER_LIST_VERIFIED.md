# BB5 Hook Master List - VERIFIED with GitHub Repos

**Date:** 2026-02-06
**Sources:** 5 research sub-agents + comprehensive GitHub repo search (19 repos)
**Total Hooks Found in Repos:** 109+ actual implementations
**Total Hook Opportunities for BB5:** 150+

---

## Verified Hook Sources

### 1. multi-agent-ralph-loop (83+ hooks)
**Location:** `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/multi-agent-ralph-loop/.claude/hooks/`

This is the MOST COMPREHENSIVE hook collection found.

#### SessionStart Hooks (6)
| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 1 | `session-start-ledger.sh` | Initialize session ledger tracking | HIGH - Track session history |
| 2 | `session-start-restore-context.sh` | Restore context after compaction | HIGH - Context preservation |
| 3 | `auto-migrate-plan-state.sh` | Auto-migrate plan-state.json schema | MEDIUM - Schema versioning |
| 4 | `session-start-welcome.sh` | Display welcome message | LOW - UX enhancement |
| 5 | `session-start-tldr.sh` | Show session TLDR summary | MEDIUM - Context briefing |
| 6 | `skill-pre-warm.sh` | Pre-warm skills for performance | MEDIUM - Performance |

#### PreToolUse Hooks (12)
| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 7 | `smart-memory-search.sh` | Parallel memory search before Task | HIGH - Memory retrieval |
| 8 | `agent-memory-auto-init.sh` | Auto-initialize agent memory buffers | HIGH - Agent setup |
| 9 | `procedural-inject.sh` | Inject procedural rules into prompts | MEDIUM - Pattern learning |
| 10 | `orchestrator-auto-learn.sh` | Detect knowledge gaps, trigger learning | HIGH - Auto-improvement |
| 11 | `fast-path-check.sh` | Detect trivial tasks for fast-path routing | HIGH - Task routing |
| 12 | `lsa-pre-step.sh` | Lead Software Architect pre-check | HIGH - Architecture validation |
| 13 | `checkpoint-smart-save.sh` | Smart checkpoint before risky edits | HIGH - Risk management |
| 14 | `inject-session-context.sh` | Inject session context into tasks | HIGH - Context preservation |
| 15 | `ralph-context-injector.sh` | Ralph-specific context injection | MEDIUM - Loop context |
| 16 | `git-safety-guard.py` | Block destructive git commands | CRITICAL - Security |
| 17 | `skill-validator.sh` | Validate skill invocations | HIGH - Skill checking |
| 18 | `promptify-security.sh` | Security validation for prompts | HIGH - Prompt security |

#### PostToolUse Hooks (18)
| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 19 | `plan-sync-post-step.sh` | Detect plan drift, sync downstream | HIGH - Plan sync |
| 20 | `decision-extractor.sh` | Extract architectural decisions | HIGH - Decision tracking |
| 21 | `semantic-realtime-extractor.sh` | Real-time semantic memory extraction | HIGH - Memory extraction |
| 22 | `status-auto-check.sh` | Auto-show status every 5 operations | MEDIUM - Monitoring |
| 23 | `sec-context-validate.sh` | Security context validation | HIGH - Security |
| 24 | `quality-gates-v2.sh` | Quality gates with caching | HIGH - Quality validation |
| 25 | `checkpoint-auto-save.sh` | Auto-save checkpoints | MEDIUM - Backup |
| 26 | `ralph-quality-gates.sh` | Ralph-specific quality checks | MEDIUM - Loop validation |
| 27 | `parallel-explore.sh` | Launch 5 concurrent exploration tasks | HIGH - Parallelization |
| 28 | `recursive-decompose.sh` | Trigger sub-orchestrators | HIGH - Recursive planning |
| 29 | `plan-analysis-cleanup.sh` | Cleanup after plan mode exit | LOW - Cleanup |
| 30 | `post-commit-command-verify.sh` | Verify post-commit commands | MEDIUM - Validation |
| 31 | `todo-plan-sync.sh` | Sync todos with plan-state.json | HIGH - Task sync |
| 32 | `auto-save-context.sh` | Auto-save context after operations | MEDIUM - Context preservation |
| 33 | `progress-tracker.sh` | Track progress across operations | HIGH - Progress tracking |
| 34 | `auto-plan-state.sh` | Auto-create plan-state.json | MEDIUM - State automation |
| 35 | `global-task-sync.sh` | Sync with Claude Code Task primitive | HIGH - Task integration |
| 36 | `verification-subagent.sh` | Suggest verification subagent | HIGH - Auto-verification |

#### PreCompact Hooks (1)
| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 37 | `pre-compact-handoff.sh` | Save state before compaction | HIGH - Context handoff |

#### UserPromptSubmit Hooks (8)
| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 38 | `command-router.sh` | Intelligent command suggestion | HIGH - Smart routing |
| 39 | `context-warning.sh` | Context usage warnings | HIGH - Context monitoring |
| 40 | `memory-write-trigger.sh` | Trigger memory writes | MEDIUM - Memory automation |
| 41 | `prompt-analyzer.sh` | Analyze prompt complexity | MEDIUM - Complexity detection |
| 42 | `statusline-health-monitor.sh` | Health checks every 5 min | MEDIUM - Health monitoring |
| 43 | `periodic-reminder.sh` | Periodic user reminders | LOW - Reminders |
| 44 | `curator-suggestion.sh` | Suggest curator when memory empty | MEDIUM - Auto-learning |
| 45 | `repo-boundary-guard.sh` | Prevent work in external repos | HIGH - Repository isolation |

#### Stop Hooks (7)
| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 46 | `sentry-report.sh` | Report to Sentry | LOW - Error tracking |
| 47 | `reflection-engine.sh` | Session reflection analysis | HIGH - Learning extraction |
| 48 | `semantic-auto-extractor.sh` | Auto-extract semantic facts | HIGH - Git diff analysis |
| 49 | `episodic-auto-convert.sh` | Convert experiences to episodic | MEDIUM - Experience logging |
| 50 | `orchestrator-report.sh` | Generate orchestration report | MEDIUM - Loop reporting |
| 51 | `stop-verification.sh` | Verify completion on stop | HIGH - Completion checking |
| 52 | `stop-slop-hook.sh` | Detect AI filler phrases | MEDIUM - Quality monitoring |

#### Additional Utility Hooks (30+)
| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 53-83 | `ai-code-audit.sh`, `auto-background-swarm.sh`, `auto-format-prettier.sh`, `code-review-auto.sh`, `console-log-detector.sh`, `context-injector.sh`, `continuous-learning.sh`, `deslop-auto-clean.sh`, `glm-context-tracker.sh`, `glm-context-update.sh`, `glm-visual-validation.sh`, `orchestrator-init.sh`, `plan-state-adaptive.sh`, `plan-state-init.sh`, `plan-state-lifecycle.sh`, `quality-parallel-async.sh`, `ralph-integration.sh`, `ralph-memory-integration.sh`, `recursive-decompose.sh`, `sanitize-secrets.js`, `security-full-audit.sh`, `semantic-write-helper.sh`, `skill-pre-warm.sh`, `task-orchestration-optimizer.sh`, `task-primitive-sync.sh`, `task-project-tracker.sh`, `typescript-quick-check.sh`, `unified-context-tracker.sh` | Various utilities | MIXED |

---

### 2. smart-ralph (4 hooks)
**Location:** `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/smart-ralph/`

| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 84 | `stop-watcher.sh` (ralph-specum) | Spec execution validation | MEDIUM |
| 85 | `load-spec-context.sh` (ralph-specum) | Load spec context on start | MEDIUM |
| 86 | `stop-watcher.sh` (ralph-speckit) | Spec kit validation | MEDIUM |
| 87 | `hook-linter.sh` | Lint hook scripts | LOW - Dev tool |

---

### 3. Claudeman (3 hooks)
**Location:** `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/Claudeman/`

| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 88 | `Notification` hook | Forward to Claudeman API | LOW - External integration |
| 89 | `Stop` hook | Forward to Claudeman API | LOW - External integration |
| 90 | Hook config generator | Generate settings.local.json | LOW - Dev tool |

---

### 4. SWE-agent (3 hooks)
**Location:** `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/SWE-agent/`

**Python class-based hooks:**

| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 91 | `RunHook` | Run-level lifecycle | MEDIUM - Run management |
| 92 | `EnvHook` | Environment lifecycle | MEDIUM - Environment setup |
| 93 | `AbstractAgentHook` | Agent lifecycle (13 events) | HIGH - Agent orchestration |

**Concrete implementations:**
- `SaveApplyPatchHook` - Save patches to directory
- `OpenPRHook` - Auto-open PRs when issues solved

---

### 5. juno-code (5 hooks)
**Location:** `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/juno-code/`

**Lifecycle hooks:**

| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 94 | `START_RUN` | Beginning of run | HIGH - Run start |
| 95 | `START_ITERATION` | Start of each iteration | HIGH - Iteration tracking |
| 96 | `END_ITERATION` | End of each iteration | HIGH - Iteration completion |
| 97 | `END_RUN` | End of run | HIGH - Run completion |
| 98 | `ON_STALE` | When stale iteration detected | MEDIUM - Stale detection |

**Features:**
- Sequential command execution
- Environment variable passing
- Dangerous command detection
- File size monitoring (CLAUDE.md, AGENTS.md)

---

### 6. ralph-orchestrator (1 hook)
**Location:** `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/ralph-orchestrator/`

| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 99 | `pre-commit` (git hook) | Run cargo fmt and clippy | LOW - Rust dev |

---

### 7. ralphy (2 hooks)
**Location:** `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/ralphy/`

| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 100 | `telemetry-webhook.ts` | Telemetry webhook | LOW - Analytics |
| 101 | `notifications-webhook.ts` | Notification webhook | LOW - Notifications |

---

### 8. OpenHands (8 hooks)
**Location:** `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/OpenHands/`

GitLab webhook implementations:

| # | Hook | Purpose | BB5 Value |
|---|------|---------|-----------|
| 102-109 | Various GitLab webhooks | Event handling | LOW - GitLab specific |

---

## BB5-Specific Hook Opportunities (Additional)

Beyond the 109+ hooks found in repos, here are BB5-specific opportunities:

### Task Lifecycle (12)
| # | Hook | Purpose | Priority |
|---|------|---------|----------|
| 110 | `pre-task-create` | Validate task structure | HIGH |
| 111 | `post-task-create` | Auto-populate templates | CRITICAL |
| 112 | `pre-task-claim` | Check dependencies | HIGH |
| 113 | `post-task-claim` | Create working directory | HIGH |
| 114 | `pre-task-execute` | Validate requirements | HIGH |
| 115 | `post-task-execute` | Log results | HIGH |
| 116 | `pre-task-complete` | Validate acceptance criteria | CRITICAL |
| 117 | `post-task-complete` | Archive, sync, update | CRITICAL |
| 118 | `pre-task-status-change` | Validate transition rules | HIGH |
| 119 | `post-task-status-change` | Sync to queue.yaml | HIGH |
| 120 | `on-task-failure` | Analyze failure | MEDIUM |
| 121 | `pre-task-validate` | Run quality checks | MEDIUM |

### Goal/Plan Hierarchy (10)
| # | Hook | Purpose | Priority |
|---|------|---------|----------|
| 122 | `pre-goal-create` | Validate against existing | MEDIUM |
| 123 | `post-goal-create` | Initialize journal | MEDIUM |
| 124 | `pre-plan-create` | Link to parent goal | MEDIUM |
| 125 | `post-plan-create` | Create initial tasks | MEDIUM |
| 126 | `post-goal-progress` | Recalculate from plans | CRITICAL |
| 127 | `post-plan-progress` | Update parent goal | HIGH |
| 128 | `pre-link-validation` | Check circular deps | HIGH |
| 129 | `post-link-created` | Update INDEX.yaml | MEDIUM |
| 130 | `on-orphan-detected` | Alert on orphans | LOW |
| 131 | `pre-index-regenerate` | Validate paths | MEDIUM |

### Queue Management (8)
| # | Hook | Purpose | Priority |
|---|------|---------|----------|
| 132 | `pre-queue-update` | Validate task_id | CRITICAL |
| 133 | `post-queue-update` | Sync to events.yaml | HIGH |
| 134 | `on-queue-priority-recalc` | Recalculate scores | MEDIUM |
| 135 | `on-dependency-resolved` | Unblock tasks | HIGH |
| 136 | `post-task-archive` | Move to archive | LOW |
| 137 | `on-queue-empty` | Trigger generation | LOW |
| 138 | `pre-task-claim` | Check race conditions | HIGH |
| 139 | `post-task-claim` | Update heartbeat | HIGH |

### Skill System (8)
| # | Hook | Purpose | Priority |
|---|------|---------|----------|
| 140 | `pre-skill-check` | Remind to check skills | HIGH |
| 141 | `post-skill-invoked` | Log to skill-usage.yaml | CRITICAL |
| 142 | `post-skill-completed` | Record outcome | CRITICAL |
| 143 | `on-skill-missing` | Suggest creation | LOW |
| 144 | `pre-skill-validation` | Validate skill exists | MEDIUM |
| 145 | `post-skill-metrics-update` | Recalculate effectiveness | MEDIUM |
| 146 | `on-skill-threshold-breach` | Alert for review | LOW |
| 147 | `post-skill-recommendation` | Suggest skills | MEDIUM |

### State & Metrics (10)
| # | Hook | Purpose | Priority |
|---|------|---------|----------|
| 148 | `pre-state-update` | Validate structure | MEDIUM |
| 149 | `post-state-update` | Sync to related files | MEDIUM |
| 150 | `on-state-stale` | Detect and fix stale state | HIGH |
| 151 | `post-metric-calculate` | Update STATE.yaml | MEDIUM |
| 152 | `on-improvement-complete` | Update improvement_metrics | MEDIUM |
| 153 | `post-learning-extracted` | Increment learnings count | MEDIUM |
| 154 | `on-risk-threshold` | Alert and suggest mitigation | LOW |
| 155 | `pre-activity-sync` | Calculate from git/fs | MEDIUM |
| 156 | `post-run-complete` | Update run counters | MEDIUM |
| 157 | `on-metrics-threshold` | Trigger alert | LOW |

---

## Unique/Creative Hook Patterns (Top 20)

From the GitHub repos, these are the most innovative patterns:

| # | Pattern | Source | Description |
|---|---------|--------|-------------|
| 1 | **Command Router** | multi-agent-ralph-loop | Multilingual intent classification with confidence |
| 2 | **Fast-Path Check** | multi-agent-ralph-loop | Auto complexity classification for routing |
| 3 | **Smart Checkpoint** | multi-agent-ralph-loop | Risk-based checkpointing with atomic ops |
| 4 | **Git Safety Guard** | multi-agent-ralph-loop | Python-based destructive command blocking |
| 5 | **Orchestrator Auto-Learn** | multi-agent-ralph-loop | Proactive learning trigger on knowledge gaps |
| 6 | **Parallel Explore** | multi-agent-ralph-loop | Spawn 5 concurrent exploration tasks |
| 7 | **Context Warning** | multi-agent-ralph-loop | Dual-metric context monitoring |
| 8 | **Stop-Slop Detection** | multi-agent-ralph-loop | AI filler phrase detection |
| 9 | **Repo Boundary Guard** | multi-agent-ralph-loop | Prevent accidental external repo work |
| 10 | **Decision Extractor** | multi-agent-ralph-loop | Auto-extract architectural decisions |
| 11 | **Semantic Realtime Extractor** | multi-agent-ralph-loop | Live fact extraction from edits |
| 12 | **Verification Subagent** | multi-agent-ralph-loop | Auto-suggest verification after completion |
| 13 | **Global Task Sync** | multi-agent-ralph-loop | Sync with Claude Code Task primitive |
| 14 | **Plan Sync Post-Step** | multi-agent-ralph-loop | Detect drift, sync downstream |
| 15 | **Status Auto-Check** | multi-agent-ralph-loop | Auto-show status every 5 operations |
| 16 | **Agent Memory Auto-Init** | multi-agent-ralph-loop | Auto-initialize agent memory buffers |
| 17 | **Procedural Inject** | multi-agent-ralph-loop | Inject learned rules into prompts |
| 18 | **File Size Monitor** | juno-code | Monitor CLAUDE.md/AGENTS.md size |
| 19 | **Stale Detection** | juno-code | Detect when iteration becomes stale |
| 20 | **Python Class Hooks** | SWE-agent | Abstract base classes for hooks |

---

## Consolidated Priority List (Top 30)

After analyzing all 150+ hooks, here are the top 30 for BB5:

### CRITICAL (Implement First)
| Rank | Hook | Source | Purpose |
|------|------|--------|---------|
| 1 | **SessionStart** (enhanced) | BB5 + ralph-loop | Initialize context + run folder |
| 2 | **SessionEnd** (comprehensive) | BB5 | 8-step finalization pipeline |
| 3 | **pre-task-complete** | BB5 | Validate acceptance criteria |
| 4 | **post-task-complete** | BB5 | Archive, sync goal progress |
| 5 | **post-goal-progress** | BB5 | Auto-calculate from plans |
| 6 | **post-skill-invoked** | BB5 | Log skill usage |
| 7 | **git-safety-guard.py** | ralph-loop | Block destructive git commands |
| 8 | **quality-gates-v2.sh** | ralph-loop | Multi-stage quality validation |

### HIGH (Implement Second)
| Rank | Hook | Source | Purpose |
|------|------|--------|---------|
| 9 | **Stop** (checkpoint) | BB5 | Mid-session saves |
| 10 | **SubagentStart** (enhanced) | BB5 + ralph-loop | Context inheritance |
| 11 | **SubagentStop** (enhanced) | BB5 + ralph-loop | Result capture |
| 12 | **pre-queue-update** | BB5 | Validate queue changes |
| 13 | **on-state-stale** | BB5 | Detect/fix stale STATE.yaml |
| 14 | **command-router.sh** | ralph-loop | Intelligent routing |
| 15 | **context-warning.sh** | ralph-loop | Context usage warnings |
| 16 | **smart-memory-search.sh** | ralph-loop | Parallel memory retrieval |
| 17 | **fast-path-check.sh** | ralph-loop | Auto complexity classification |
| 18 | **checkpoint-smart-save.sh** | ralph-loop | Risk-based checkpointing |
| 19 | **decision-extractor.sh** | ralph-loop | Auto-extract decisions |
| 20 | **semantic-auto-extractor.sh** | ralph-loop | Git diff analysis |
| 21 | **pre-timeline-append** | BB5 | Deduplication |
| 22 | **post-learning-extract** | BB5 | Memory retention |
| 23 | **on-dependency-resolved** | BB5 | Unblock tasks |
| 24 | **verification-subagent.sh** | ralph-loop | Auto-verification suggestion |

### MEDIUM (Implement Third)
| Rank | Hook | Source | Purpose |
|------|------|--------|---------|
| 25 | **repo-boundary-guard.sh** | ralph-loop | Prevent external repo work |
| 26 | **stop-verification.sh** | ralph-loop | Completion checking |
| 27 | **reflection-engine.sh** | ralph-loop | Session analysis |
| 28 | **plan-sync-post-step.sh** | ralph-loop | Plan drift detection |
| 29 | **status-auto-check.sh** | ralph-loop | Auto status every 5 ops |
| 30 | **skill-validator.sh** | ralph-loop | Validate skill invocations |

---

## Implementation Recommendations

### Phase 1: Core Lifecycle (Week 1)
1. Enhanced SessionStart (merge BB5 + ralph-loop patterns)
2. Comprehensive SessionEnd (8-step pipeline)
3. Enhanced Stop (checkpoint + validation)

### Phase 2: Task Management (Week 2)
4. pre-task-complete validation
5. post-task-complete sync
6. post-goal-progress calculation
7. on-dependency-resolution

### Phase 3: Quality & Safety (Week 3)
8. git-safety-guard.py
9. quality-gates-v2.sh
10. context-warning.sh
11. command-router.sh

### Phase 4: Intelligence (Week 4)
12. smart-memory-search.sh
13. decision-extractor.sh
14. semantic-auto-extractor.sh
15. verification-subagent.sh

---

## Files Referenced

**Primary Sources:**
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/multi-agent-ralph-loop/.claude/hooks/` (83+ hooks)
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/smart-ralph/plugins/` (4 hooks)
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/Claudeman/src/hooks-config.ts` (3 hooks)
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/SWE-agent/sweagent/run/hooks/` (3 hooks)
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/juno-code/src/utils/hooks.ts` (5 hooks)

**BB5 Current Hooks:**
- `/Users/shaansisodia/.blackbox5/.claude/hooks/` (10+ hooks)

---

*This verified master list contains 150+ hook opportunities from actual GitHub implementations. The top 30 provide maximum value for BB5.*
