# PLAN-010: BB5 Hook System Implementation

**Goal:** IG-010 - Implement World-Class Hook System for BB5
**Status:** in_progress
**Created:** 2026-02-06
**Target Completion:** 2026-02-28

---

## Overview

This plan implements a comprehensive, industry-leading hook system for BlackBox5. It combines best practices from 19+ GitHub repositories with custom BB5-specific innovations.

---

## Phase 1: Research & Analysis (COMPLETE)

**Status:** COMPLETE
**Duration:** 2026-02-06

### Deliverables:
- [x] HOOK_MASTER_LIST_VERIFIED.md - 150+ hook opportunities documented
- [x] Analysis of multi-agent-ralph-loop (83+ hooks)
- [x] Analysis of juno-code, SWE-agent, smart-ralph, Claudeman
- [x] BB5-specific hook gaps identified

### Key Findings:
- 109 actual hook implementations found in GitHub repos
- multi-agent-ralph-loop has the most comprehensive system (83+ hooks)
- Top 30 hooks identified for BB5 implementation
- 8 CRITICAL priority hooks for immediate implementation

---

## Phase 2: Core Lifecycle Hooks (IN PROGRESS)

**Status:** in_progress
**Duration:** Week 1 (2026-02-06 to 2026-02-13)

### Tasks:

#### TASK-010-001: SessionStart Enhanced Hook
**Status:** pending
**Priority:** CRITICAL
**Description:** Implement enhanced SessionStart hook combining BB5 context loading with ralph-loop run folder creation

**What it does:**
- Detects agent type (planner/executor/architect)
- Creates run folder: `runs/{agent_type}/run-{timestamp}/`
- Creates required files: THOUGHTS.md, RESULTS.md, DECISIONS.md, ASSUMPTIONS.md, LEARNINGS.md, metadata.yaml
- Loads relevant memories from vector store
- Injects context via AGENT_CONTEXT.md
- Exports RALF_RUN_DIR, RALF_RUN_ID environment variables

**Best practices from:**
- BB5: session-start-blackbox5.sh (agent detection)
- ralph-loop: session-start-ledger.sh (session tracking)
- ralph-loop: orchestrator-init.sh (memory initialization)

**Files to create:**
- `.claude/hooks/session-start-enhanced.sh`
- `.claude/hooks/lib/run-initializer.sh`

**Acceptance Criteria:**
- [ ] Run folder created automatically on session start
- [ ] All required files populated from templates
- [ ] Agent type detected correctly
- [ ] Context loaded from vector store
- [ ] Environment variables exported
- [ ] Works for planner, executor, and architect agents

---

#### TASK-010-002: SessionEnd Comprehensive Hook
**Status:** pending
**Priority:** CRITICAL
**Description:** Implement 8-step finalization pipeline for SessionEnd

**What it does (8-step pipeline):**
1. **Task Completion Validation** - Check task.md success criteria, verify RESULTS.md exists, validate checkboxes
2. **Memory Extraction (RETAIN)** - Parse THOUGHTS.md, DECISIONS.md, LEARNINGS.md, store in vector store
3. **Skill Usage Logging** - Parse THOUGHTS.md for skill mentions, log to skill-usage.yaml
4. **Timeline Finalization** - Add completion event to timeline.yaml, update goal progress
5. **Queue Synchronization** - Update task status to "completed", unblock dependent tasks
6. **Task Archival** - Move task from active/ to completed/, create COMPLETION.md
7. **Git Commit (Optional)** - Stage changes, create standardized commit message
8. **Run Finalization** - Update metadata.yaml, move run to completed/

**Best practices from:**
- ralph-loop: reflection-engine.sh (session analysis)
- ralph-loop: semantic-auto-extractor.sh (git diff analysis)
- ralph-loop: episodic-auto-convert.sh (experience logging)
- BB5: session-end-context-update.sh (context updates)

**Files to create:**
- `.claude/hooks/session-end-finalize.sh`
- `.claude/hooks/lib/task-validator.sh`
- `.claude/hooks/lib/memory-extractor.sh`
- `.claude/hooks/lib/skill-logger.sh`
- `.claude/hooks/lib/timeline-updater.sh`
- `.claude/hooks/lib/queue-sync.sh`

**Acceptance Criteria:**
- [ ] All 8 steps execute in sequence
- [ ] Task validation blocks incomplete tasks
- [ ] Memories extracted and stored
- [ ] Skills logged to skill-usage.yaml
- [ ] Timeline updated with completion event
- [ ] Queue synchronized
- [ ] Task moved to completed/
- [ ] Git commit created (if enabled)

---

#### TASK-010-003: Stop Checkpoint Hook
**Status:** pending
**Priority:** HIGH
**Description:** Implement checkpoint save on Stop hook

**What it does:**
- Validates documentation (THOUGHTS.md, RESULTS.md filled)
- Saves checkpoint: current THOUGHTS.md state, task progress, metadata snapshot
- Updates parent timelines
- Can block if critical issues found

**Best practices from:**
- BB5: stop-validate-docs.sh (documentation validation)
- BB5: stop-hierarchy-update.sh (hierarchy updates)
- ralph-loop: checkpoint-smart-save.sh (smart checkpointing)

**Files to modify:**
- `.claude/hooks/stop-validate-docs.sh` (keep as-is)
- `.claude/hooks/stop-checkpoint.sh` (new)

**Acceptance Criteria:**
- [ ] Documentation validated
- [ ] Checkpoint saved with timestamp
- [ ] Parent timelines updated
- [ ] Can block on critical issues
- [ ] Resume from checkpoint works

---

## Phase 3: Task Management Hooks (PENDING)

**Status:** pending
**Duration:** Week 2 (2026-02-13 to 2026-02-20)

### Tasks:

#### TASK-010-004: Pre-Task-Complete Validation Hook
**Status:** pending
**Priority:** CRITICAL
**Description:** Validate task completion criteria before allowing completion

**What it does:**
- Checks task.md success criteria (all checkboxes marked)
- Verifies RESULTS.md exists and is non-empty
- Validates THOUGHTS.md has content
- Validates DECISIONS.md documents decisions
- Validates LEARNINGS.md captures insights
- Blocks completion if any criteria not met

**Best practices from:**
- BB5: stop-validate-docs.sh (pattern)
- ralph-loop: stop-verification.sh (completion checking)
- juno-code: quality gates (validation pattern)

**Files to create:**
- `.claude/hooks/lib/task-completion-validator.sh`

**Acceptance Criteria:**
- [ ] All success criteria validated
- [ ] All data layers checked
- [ ] Blocks completion if incomplete
- [ ] Provides clear feedback on what's missing

---

#### TASK-010-005: Post-Task-Complete Sync Hook
**Status:** pending
**Priority:** CRITICAL
**Description:** Synchronize task completion across all systems

**What it does:**
- Updates queue.yaml with "completed" status
- Adds completion timestamp
- Logs to events.yaml
- Unblocks dependent tasks
- Updates goal progress
- Moves task from active/ to completed/

**Best practices from:**
- ralph-loop: global-task-sync.sh (task primitive sync)
- BB5: stop-hierarchy-update.sh (hierarchy updates)

**Files to create:**
- `.claude/hooks/lib/task-completion-sync.sh`

**Acceptance Criteria:**
- [ ] Queue.yaml updated
- [ ] Events.yaml logged
- [ ] Dependent tasks unblocked
- [ ] Goal progress updated
- [ ] Task moved to completed/

---

#### TASK-010-006: Post-Goal-Progress Calculation Hook
**Status:** pending
**Priority:** CRITICAL
**Description:** Auto-calculate goal progress from linked plans

**What it does:**
- Recalculates goal progress percentage based on linked plan completion
- Updates goal.yaml progress.percentage
- Triggers goal completion when all plans complete
- Syncs to STATE.yaml

**Best practices from:**
- BB5: context-synchronization.sh (pattern)
- ralph-loop: plan-sync-post-step.sh (sync pattern)

**Files to create:**
- `.claude/hooks/lib/goal-progress-calculator.sh`

**Acceptance Criteria:**
- [ ] Progress calculated from linked plans
- [ ] goal.yaml updated
- [ ] Goal completion triggered automatically
- [ ] STATE.yaml synced

---

## Phase 4: Quality & Safety Hooks (PENDING)

**Status:** pending
**Duration:** Week 3 (2026-02-20 to 2026-02-27)

### Tasks:

#### TASK-010-007: Git Safety Guard Hook
**Status:** pending
**Priority:** CRITICAL
**Description:** Block destructive git commands

**What it does:**
- Blocks `rm -rf` in git repositories
- Blocks force push (`git push --force`)
- Blocks `git clean -fd`
- Blocks destructive branch operations
- Logs access attempts

**Best practices from:**
- ralph-loop: git-safety-guard.py (Python implementation)
- BB5: pre-tool-security.py (existing security)

**Files to create:**
- `.claude/hooks/git-safety-guard.py`

**Acceptance Criteria:**
- [ ] Destructive commands blocked
- [ ] Access attempts logged
- [ ] Clear error messages provided
- [ ] Override option available for emergencies

---

#### TASK-010-008: Quality Gates Hook
**Status:** pending
**Priority:** HIGH
**Description:** Multi-stage quality validation

**What it does (3-stage pipeline):**
- Stage 1 (CORRECTNESS): Syntax validation (Python, TypeScript, JavaScript, Go, Rust, JSON, YAML, Bash)
- Stage 2 (QUALITY): Type checking (mypy for Python)
- Stage 2.5 (SECURITY): semgrep SAST + gitleaks secret detection
- Stage 3 (CONSISTENCY): Linting (ruff, ESLint, golint) - advisory only

**Best practices from:**
- ralph-loop: quality-gates-v2.sh (comprehensive implementation)
- ralph-loop: typescript-quick-check.sh (caching)

**Files to create:**
- `.claude/hooks/quality-gates.sh`
- `.claude/hooks/lib/syntax-validator.sh`
- `.claude/hooks/lib/security-scanner.sh`

**Acceptance Criteria:**
- [ ] All 3 stages execute
- [ ] Syntax errors caught
- [ ] Security issues detected
- [ ] Type checking works
- [ ] Results cached for performance

---

#### TASK-010-009: Context Warning Hook
**Status:** pending
**Priority:** HIGH
**Description:** Monitor context usage and warn on thresholds

**What it does:**
- Monitors cumulative context usage
- Monitors current window context usage
- Warns at 70% threshold
- Alerts at 85% threshold
- Suggests compaction at 90% threshold

**Best practices from:**
- ralph-loop: context-warning.sh (dual-metric monitoring)
- juno-code: file size monitoring (CLAUDE.md, AGENTS.md)

**Files to create:**
- `.claude/hooks/context-warning.sh`

**Acceptance Criteria:**
- [ ] Context usage monitored
- [ ] Warnings at 70%
- [ ] Alerts at 85%
- [ ] Compaction suggested at 90%
- [ ] Works for both cumulative and window metrics

---

## Phase 5: Intelligence Hooks (PENDING)

**Status:** pending
**Duration:** Week 4 (2026-02-27 to 2026-03-06)

### Tasks:

#### TASK-010-010: Smart Memory Search Hook
**Status:** pending
**Priority:** HIGH
**Description:** Parallel memory retrieval before task execution

**What it does:**
- Performs 4-way parallel memory search
- Searches semantic memory (facts, concepts)
- Searches episodic memory (past experiences)
- Searches procedural memory (learned rules)
- Searches working memory (current context)
- Injects relevant memories into context

**Best practices from:**
- ralph-loop: smart-memory-search.sh (4-way parallel search)
- ralph-loop: agent-memory-auto-init.sh (memory initialization)

**Files to create:**
- `.claude/hooks/smart-memory-search.sh`
- `.claude/hooks/lib/memory-retriever.sh`

**Acceptance Criteria:**
- [ ] 4-way parallel search implemented
- [ ] All memory tiers searched
- [ ] Relevant memories injected
- [ ] Performance optimized

---

#### TASK-010-011: Decision Extractor Hook
**Status:** pending
**Priority:** HIGH
**Description:** Auto-extract architectural decisions from work

**What it does:**
- Parses THOUGHTS.md for decision patterns
- Parses DECISIONS.md for structured decisions
- Extracts: context, decision, rationale, consequences
- Updates decisions/registry.md
- Links related decisions

**Best practices from:**
- ralph-loop: decision-extractor.sh (pattern recognition)
- BB5: existing DECISIONS.md structure

**Files to create:**
- `.claude/hooks/decision-extractor.sh`
- `.claude/hooks/lib/decision-parser.sh`

**Acceptance Criteria:**
- [ ] Decisions parsed from THOUGHTS.md
- [ ] Decisions extracted from DECISIONS.md
- [ ] Registry updated
- [ ] Related decisions linked

---

#### TASK-010-012: Verification Subagent Hook
**Status:** pending
**Priority:** HIGH
**Description:** Suggest verification subagent after task completion

**What it does:**
- Detects high-complexity tasks (complexity >= 7)
- Detects security-related tasks (auth, password, credential)
- Suggests appropriate verification agent
- Spawns verification subagent
- Captures verification results

**Best practices from:**
- ralph-loop: verification-subagent.sh (auto-verification)
- ralph-loop: lsa-pre-step.sh (architecture validation)

**Files to create:**
- `.claude/hooks/verification-subagent.sh`

**Acceptance Criteria:**
- [ ] High-complexity tasks detected
- [ ] Security tasks identified
- [ ] Appropriate verifier selected
- [ ] Subagent spawned
- [ ] Results captured

---

## Configuration Updates

### settings.json Changes

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/session-start-enhanced.sh"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /Users/shaansisodia/.blackbox5/.claude/hooks/git-safety-guard.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/stop-validate-docs.sh"
          },
          {
            "type": "command",
            "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/stop-checkpoint.sh"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/session-end-finalize.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Testing Strategy

### Unit Tests
- Each hook tested in isolation
- Mock inputs for all hook events
- Exit code validation
- JSON output validation

### Integration Tests
- Full hook chain testing
- Session start to end workflow
- Task lifecycle testing
- Error condition testing

### Performance Tests
- Hook execution time < 1 second each
- Parallel hook execution
- Memory usage monitoring

---

## Documentation

### Hook Developer Guide
- How to create new hooks
- Hook event reference
- JSON input/output schemas
- Best practices

### Hook User Guide
- What hooks do
- When hooks fire
- How to customize
- Troubleshooting

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Hook fails and loses data | Critical | Fail-safe design, always backup before operations |
| Hook too slow | High | Async hooks, caching, performance optimization |
| Hook blocks workflow | High | Override options, graceful degradation |
| Hook conflicts | Medium | Clear hook ordering, isolated responsibilities |

---

## Success Metrics

- Task completion automation: 90%+
- Data consistency: 99%+
- Hook execution time: < 1s average
- Zero data loss incidents
- User satisfaction: 4.5/5+

---

## Notes

This plan implements the top 12 hooks from our research of 150+ hook opportunities. Additional hooks can be added in future iterations based on user feedback and observed needs.
