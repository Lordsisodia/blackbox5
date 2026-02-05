# BB5 Hook Master List

**Date:** 2026-02-06
**Sources:** 5 parallel research sub-agents
**Total Hook Opportunities Identified:** 100+

---

## How to Use This List

1. **Review** all hooks organized by category
2. **Filter** using the criteria at the end
3. **Prioritize** using Critical/High/Medium/Low ratings
4. **Consolidate** similar hooks
5. **Implement** in phases

---

## Category 1: Claude Code Native Hook Events (13)

From official Claude Code documentation:

| # | Hook Event | When It Fires | Can Block? | BB5 Priority |
|---|------------|---------------|------------|--------------|
| 1 | **SessionStart** | Session begins/resumes | No | CRITICAL |
| 2 | **UserPromptSubmit** | Before processing user prompt | Yes | HIGH |
| 3 | **PreToolUse** | Before tool executes | Yes | CRITICAL |
| 4 | **PermissionRequest** | Permission dialog appears | Yes | MEDIUM |
| 5 | **PostToolUse** | After tool succeeds | No | HIGH |
| 6 | **PostToolUseFailure** | After tool fails | No | MEDIUM |
| 7 | **Notification** | When notification sent | No | LOW |
| 8 | **SubagentStart** | Subagent spawned | No | CRITICAL |
| 9 | **SubagentStop** | Subagent finishes | Yes | CRITICAL |
| 10 | **Stop** | Claude finishes responding | Yes | CRITICAL |
| 11 | **PreCompact** | Before context compaction | No | MEDIUM |
| 12 | **SessionEnd** | Session terminates | No | CRITICAL |
| 13 | **SessionEnd** (reason) | clear/logout/prompt_input_exit | No | MEDIUM |

---

## Category 2: BB5 Task Lifecycle Hooks (12)

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 14 | **pre-task-create** | Before task creation | Validate task structure, check for duplicates | HIGH |
| 15 | **post-task-create** | After task created | Auto-populate templates, create run directory, add to queue | CRITICAL |
| 16 | **pre-task-claim** | Before agent claims task | Check dependencies, validate availability | HIGH |
| 17 | **post-task-claim** | After task claimed | Create working directory, update agent state | HIGH |
| 18 | **pre-task-execute** | Before agent execution | Validate requirements, load context | HIGH |
| 19 | **post-task-execute** | After agent execution | Log results, update progress | HIGH |
| 20 | **pre-task-complete** | Before marking complete | Validate acceptance criteria, check data layers | CRITICAL |
| 21 | **post-task-complete** | After task completed | Update queue, sync goal progress, archive | CRITICAL |
| 22 | **pre-task-status-change** | Before status update | Validate transition rules | HIGH |
| 23 | **post-task-status-change** | After status update | Sync to queue.yaml, trigger dependents | HIGH |
| 24 | **on-task-failure** | When task fails | Analyze failure, create recovery task | MEDIUM |
| 25 | **pre-task-validate** | Before task validation | Run quality checks | MEDIUM |

---

## Category 3: BB5 Goal/Plan Hierarchy Hooks (10)

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 26 | **pre-goal-create** | Before goal creation | Validate against existing goals | MEDIUM |
| 27 | **post-goal-create** | After goal created | Initialize goal journal, create skeleton | MEDIUM |
| 28 | **pre-plan-create** | Before plan creation | Link to parent goal, validate hierarchy | MEDIUM |
| 29 | **post-plan-create** | After plan created | Create initial tasks from template | MEDIUM |
| 30 | **post-goal-progress** | When goal progress changes | Recalculate from linked plans | CRITICAL |
| 31 | **post-plan-progress** | When plan progress changes | Update parent goal, check completion | HIGH |
| 32 | **pre-link-validation** | Before linking items | Verify target exists, check circular deps | HIGH |
| 33 | **post-link-created** | After link created | Update INDEX.yaml, sync metadata | MEDIUM |
| 34 | **on-orphan-detected** | Periodic scan | Alert on orphaned goals/plans/tasks | LOW |
| 35 | **pre-index-regenerate** | Before INDEX.yaml update | Validate all paths exist | MEDIUM |

---

## Category 4: BB5 Queue Management Hooks (8)

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 36 | **pre-queue-update** | Before queue.yaml update | Validate task_id, check duplicates | CRITICAL |
| 37 | **post-queue-update** | After queue.yaml update | Sync to events.yaml, notify agents | HIGH |
| 38 | **pre-task-claim** | Before claiming | Check race conditions, validate state | HIGH |
| 39 | **post-task-claim** | After claiming | Create run directory, update heartbeat | HIGH |
| 40 | **on-queue-priority-recalc** | Periodic/nightly | Recalculate priority scores | MEDIUM |
| 41 | **on-dependency-resolved** | When blocker completes | Unblock dependent tasks | HIGH |
| 42 | **post-task-archive** | After task completed | Move to queue-archive.yaml | LOW |
| 43 | **on-queue-empty** | When queue empty | Trigger task generation | LOW |

---

## Category 5: BB5 Agent Lifecycle Hooks (10)

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 44 | **pre-agent-start** | Before agent starts | Load context, validate environment | HIGH |
| 45 | **post-agent-start** | After agent starts | Log to events.yaml, update state | HIGH |
| 46 | **pre-agent-stop** | Before agent stops | Validate output, check completion | HIGH |
| 47 | **post-agent-stop** | After agent stops | Persist state, update metrics, cleanup | HIGH |
| 48 | **on-agent-error** | When agent errors | Capture context, suggest recovery | MEDIUM |
| 49 | **on-agent-heartbeat** | Periodic | Validate agent still alive | MEDIUM |
| 50 | **pre-subagent-spawn** | Before spawning subagent | Inherit parent context | HIGH |
| 51 | **post-subagent-complete** | After subagent finishes | Capture results, update parent | HIGH |
| 52 | **on-agent-timeout** | When agent times out | Escalate or reassign | MEDIUM |
| 53 | **post-agent-handoff** | After handoff | Transfer context, update ledger | MEDIUM |

---

## Category 6: BB5 Timeline & Events Hooks (8)

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 54 | **pre-timeline-append** | Before adding event | Deduplicate, batch rapid events | HIGH |
| 55 | **post-timeline-append** | After adding event | Sync to goal timelines | MEDIUM |
| 56 | **pre-event-write** | Before events.yaml write | Validate schema | MEDIUM |
| 57 | **post-event-write** | After events.yaml write | Trigger notifications | LOW |
| 58 | **on-milestone-detected** | Significant achievement | Suggest milestone creation | LOW |
| 59 | **pre-timeline-sort** | Before sorting | Ensure chronological order | LOW |
| 60 | **on-timeline-duplicate** | Duplicate detected | Merge or suppress | MEDIUM |
| 61 | **post-timeline-sync** | After timeline update | Update STATE.yaml | MEDIUM |

---

## Category 7: BB5 Skill System Hooks (8)

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 62 | **pre-skill-check** | Before task execution | Remind to check skill-selection.yaml | HIGH |
| 63 | **post-skill-invoked** | After skill used | Log to skill-usage.yaml | CRITICAL |
| 64 | **post-skill-completed** | After skill completes | Record outcome, update metrics | CRITICAL |
| 65 | **on-skill-missing** | No skill matches task | Suggest skill creation | LOW |
| 66 | **pre-skill-validation** | Before using skill | Validate skill exists | MEDIUM |
| 67 | **post-skill-metrics-update** | After metrics change | Recalculate effectiveness | MEDIUM |
| 68 | **on-skill-threshold-breach** | Skill accuracy low | Alert for skill review | LOW |
| 69 | **post-skill-recommendation** | Task analysis | Suggest appropriate skills | MEDIUM |

---

## Category 8: BB5 State & Metrics Hooks (10)

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 70 | **pre-state-update** | Before STATE.yaml update | Validate structure | MEDIUM |
| 71 | **post-state-update** | After STATE.yaml update | Sync to related files | MEDIUM |
| 72 | **on-state-stale** | Periodic check | Detect and fix stale state | HIGH |
| 73 | **post-metric-calculate** | After metrics change | Update STATE.yaml activity | MEDIUM |
| 74 | **on-improvement-complete** | Improvement finished | Update improvement_metrics | MEDIUM |
| 75 | **post-learning-extracted** | Learning captured | Increment learnings count | MEDIUM |
| 76 | **on-risk-threshold** | Risk condition met | Alert and suggest mitigation | LOW |
| 77 | **pre-activity-sync** | Before activity update | Calculate from git/fs | MEDIUM |
| 78 | **post-run-complete** | Run finished | Update run counters | MEDIUM |
| 79 | **on-metrics-threshold** | Metric exceeds threshold | Trigger alert | LOW |

---

## Category 9: BB5 Run/Session Hooks (8)

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 80 | **pre-run-create** | Before run directory created | Validate naming convention | MEDIUM |
| 81 | **post-run-create** | After run directory created | Populate templates, init metadata | HIGH |
| 82 | **pre-run-start** | Before run starts | Validate structure, load context | HIGH |
| 83 | **post-run-complete** | After run completes | Validate outputs, update parent | HIGH |
| 84 | **pre-run-archive** | Before archiving | Compress, validate completeness | LOW |
| 85 | **post-run-archive** | After archiving | Cleanup, update indexes | LOW |
| 86 | **on-run-timeout** | Run exceeds time limit | Alert or terminate | MEDIUM |
| 87 | **post-checkpoint-save** | Checkpoint created | Update metadata | MEDIUM |

---

## Category 10: BB5 Security & Validation Hooks (10)

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 88 | **pre-security-check** | Before dangerous operation | Validate safety | CRITICAL |
| 89 | **post-security-violation** | Security rule violated | Log and alert | HIGH |
| 90 | **pre-credential-access** | Before reading .env | Log access audit | HIGH |
| 91 | **post-git-dangerous** | Dangerous git command | Block or require approval | HIGH |
| 92 | **pre-file-size-check** | Before large file write | Warn on >1MB | LOW |
| 93 | **pre-path-traversal-check** | Before file operation | Block .. paths | HIGH |
| 94 | **post-validation-fail** | Validation failed | Suggest fixes | MEDIUM |
| 95 | **pre-ssot-validation** | Before SSOT change | Validate consistency | HIGH |
| 96 | **on-security-alert** | Security condition met | Notify and block | HIGH |
| 97 | **pre-destructive-operation** | Before rm/rm -rf | Require confirmation | CRITICAL |

---

## Category 11: BB5 Memory & Learning Hooks (8)

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 98 | **pre-learning-extract** | Before extracting learnings | Validate THOUGHTS.md content | HIGH |
| 99 | **post-learning-extract** | After learnings extracted | Store in vector store | HIGH |
| 100 | **pre-decision-record** | Before recording decision | Validate decision format | MEDIUM |
| 101 | **post-decision-record** | After decision recorded | Update registry | MEDIUM |
| 102 | **on-memory-retain** | Memory retention triggered | Validate and store | MEDIUM |
| 103 | **post-cross-run-learning** | Cross-run analysis | Apply past learnings | LOW |
| 104 | **pre-relevant-memory-search** | Before task start | Find relevant memories | MEDIUM |
| 105 | **post-memory-apply** | After applying memory | Log usage | LOW |

---

## Category 12: BB5 Context & Routes Hooks (6)

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 106 | **pre-routes-validate** | Before routes.yaml update | Check path existence | MEDIUM |
| 107 | **post-routes-update** | After routes.yaml update | Sync to related files | LOW |
| 108 | **on-route-broken** | Broken route detected | Alert and suggest fix | MEDIUM |
| 109 | **pre-context-refresh** | Before context refresh | Save current state | LOW |
| 110 | **post-context-refresh** | After context refresh | Validate freshness | LOW |
| 111 | **on-context-stale** | Context outdated | Trigger refresh | LOW |

---

## Category 13: SDLC/DevOps Inspired Hooks (10)

From CI/CD, testing, deployment patterns:

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 112 | **pre-commit-validation** | Before git commit | Validate commit message, files | MEDIUM |
| 113 | **post-commit-sync** | After git commit | Update STATE.yaml activity | MEDIUM |
| 114 | **pre-branch-create** | Before branch creation | Validate naming | LOW |
| 115 | **post-merge-sync** | After git merge | Update task status | MEDIUM |
| 116 | **on-quality-gate-fail** | Quality check fails | Block and suggest fixes | HIGH |
| 117 | **post-quality-check** | After quality check | Update metrics | MEDIUM |
| 118 | **pre-test-execution** | Before running tests | Setup environment | LOW |
| 119 | **post-test-complete** | After tests complete | Update test results | LOW |
| 120 | **on-deployment-trigger** | Deployment initiated | Validate readiness | LOW |
| 121 | **post-deployment-verify** | After deployment | Verify success | LOW |

---

## Category 14: RALF/Multi-Agent Hooks (10)

From multi-agent orchestration patterns:

| # | Hook Name | Trigger | Purpose | Priority |
|---|-----------|---------|---------|----------|
| 122 | **pre-swarm-spawn** | Before spawning team | Validate resources | MEDIUM |
| 123 | **post-swarm-complete** | After swarm finishes | Aggregate results | MEDIUM |
| 124 | **on-agent-handoff** | Agent handoff | Transfer context | HIGH |
| 125 | **post-micro-gate** | Micro-gate complete | Validate step output | HIGH |
| 126 | **on-checkpoint-restore** | Checkpoint restored | Validate state | MEDIUM |
| 127 | **pre-phase-gate** | Before phase transition | Validate exit criteria | HIGH |
| 128 | **post-phase-gate** | After phase transition | Update plan-state | HIGH |
| 129 | **on-drift-detected** | Plan drift detected | Suggest correction | MEDIUM |
| 130 | **post-adversarial-check** | After cross-validation | Record results | LOW |
| 131 | **on-rollback-trigger** | Rollback initiated | Execute rollback plan | MEDIUM |

---

## Consolidation Opportunities

### Hooks That Can Be Combined:

1. **post-task-create** + **post-run-create** → Single "initialization" hook
2. **pre-security-check** + **pre-path-traversal-check** + **pre-destructive-operation** → Unified security hook
3. **post-timeline-append** + **post-event-write** → Single logging hook
4. **post-skill-invoked** + **post-skill-completed** → Single skill tracking hook
5. **pre-agent-start** + **pre-run-start** → Unified context loading

### Hooks That Should Remain Separate:

1. **SessionStart** vs **pre-agent-start** - Different contexts
2. **Stop** vs **SessionEnd** - Stop is checkpoint, SessionEnd is finalization
3. **PreToolUse** vs **pre-security-check** - Security is subset of validation
4. **post-task-complete** vs **post-run-complete** - Task vs run granularity

---

## Filtering Criteria

Use these criteria to filter the master list:

### Must Have (All Yes):
- [ ] Does BB5 need this?
- [ ] Can it be automated?
- [ ] Is complexity worth the benefit?

### Priority Scoring:
- **Critical:** Failure causes data loss or corruption
- **High:** Failure causes inconsistency or manual work
- **Medium:** Nice to have, reduces friction
- **Low:** Optimization, can live without

### Implementation Complexity:
- **Simple:** Single file operation, <1 hour
- **Medium:** Multiple files, coordination, 1-4 hours
- **Complex:** Cross-system, state management, 4+ hours

---

## Recommended Filtered List (Phase 1)

After applying criteria, implement these 15 hooks first:

| Priority | Hook | Complexity | Value |
|----------|------|------------|-------|
| 1 | **SessionStart** (enhanced) | Medium | CRITICAL |
| 2 | **SessionEnd** (comprehensive) | Complex | CRITICAL |
| 3 | **Stop** (checkpoint) | Medium | HIGH |
| 4 | **pre-task-complete** | Medium | CRITICAL |
| 5 | **post-task-complete** | Medium | CRITICAL |
| 6 | **post-goal-progress** | Simple | CRITICAL |
| 7 | **post-skill-invoked** | Simple | HIGH |
| 8 | **pre-security-check** | Medium | CRITICAL |
| 9 | **SubagentStart** (enhanced) | Medium | HIGH |
| 10 | **SubagentStop** (enhanced) | Medium | HIGH |
| 11 | **pre-queue-update** | Simple | HIGH |
| 12 | **on-state-stale** | Medium | HIGH |
| 13 | **pre-timeline-append** | Simple | MEDIUM |
| 14 | **post-learning-extract** | Medium | MEDIUM |
| 15 | **on-dependency-resolved** | Medium | HIGH |

---

## Next Steps

1. **Review this master list** - Mark which hooks to keep/discard
2. **Consolidate similar hooks** - Merge where appropriate
3. **Create implementation tasks** for Phase 1 hooks
4. **Design hook architecture** - Shared libraries, patterns
5. **Implement incrementally** - One hook at a time, test thoroughly

---

*This master list contains 130+ hook opportunities. The key is filtering to the 15-20 that provide maximum value with reasonable implementation effort.*
