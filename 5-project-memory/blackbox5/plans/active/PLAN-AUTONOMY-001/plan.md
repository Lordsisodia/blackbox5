# PLAN-AUTONOMY-001: Close the Feedback Loops Implementation

**Goal:** IG-AUTONOMY-001 - Make BB5 Actually Autonomous
**Status:** in_progress
**Created:** 2026-02-06
**Target Completion:** 2026-03-06

---

## Overview

This plan implements the automation layer that closes BB5's critical feedback loops:
1. Task lifecycle automation (no manual status updates)
2. Skill auto-invocation (no manual skill checking)
3. Learning extraction (automated REFLECT operation)
4. System health monitoring (24/7 visibility)

---

## Phase 1: Task Lifecycle Automation (Week 1)

### TASK-AUTONOMY-001: Task State Machine Hook Library
**Status:** pending
**Priority:** CRITICAL
**Estimated Tokens:** 50K

Implement the core state machine for task lifecycle management.

**Files to create:**
- `.claude/hooks/lib/task-state-machine.sh` - State transition logic
- `.claude/hooks/lib/task-claim.sh` - Auto-claim from queue
- `.claude/hooks/lib/task-complete.sh` - Auto-complete workflow

**Acceptance Criteria:**
- [ ] States: pending → claimed → in_progress → completed → archived
- [ ] SessionStart auto-claims task, sets to in_progress
- [ ] PreToolUse blocks TaskUpdate if task not claimed
- [ ] SessionEnd auto-transitions to completed

---

### TASK-AUTONOMY-002: Queue Synchronization Automation
**Status:** pending
**Priority:** CRITICAL
**Estimated Tokens:** 50K

Auto-synchronize queue.yaml, events.yaml, and task status.

**Files to create:**
- `.claude/hooks/lib/queue-sync-auto.sh` - Auto-sync all queue files
- `.claude/hooks/lib/events-logger.sh` - Auto-log events

**Acceptance Criteria:**
- [ ] queue.yaml updated on every state change
- [ ] events.yaml appended with timestamped events
- [ ] No manual queue updates required

---

### TASK-AUTONOMY-003: Task Archival Automation
**Status:** pending
**Priority:** HIGH
**Estimated Tokens:** 50K

Auto-move completed tasks and create completion summaries.

**Files to create:**
- `.claude/hooks/lib/task-archival.sh` - Move task to completed/
- `.claude/hooks/lib/completion-generator.sh` - Create COMPLETION.md

**Acceptance Criteria:**
- [ ] Task moved from active/ to completed/ on completion
- [ ] COMPLETION.md generated with summary
- [ ] All subtasks handled correctly

---

### TASK-AUTONOMY-004: Goal Progress Auto-Calculation
**Status:** pending
**Priority:** HIGH
**Estimated Tokens:** 50K

Auto-calculate goal progress from linked plans/tasks.

**Files to create:**
- `.claude/hooks/lib/goal-progress-calculator.sh` - Calculate % complete
- `.claude/hooks/lib/goal-sync.sh` - Update goal.yaml files

**Acceptance Criteria:**
- [ ] Progress calculated from linked plan completion
- [ ] goal.yaml updated automatically
- [ ] Goal completion triggered when all plans complete

---

## Phase 2: Skill Auto-Invocation (Week 2)

### TASK-AUTONOMY-005: Skill Auto-Selector
**Status:** pending
**Priority:** CRITICAL
**Estimated Tokens:** 50K

Pre-select skills based on task analysis.

**Files to create:**
- `.claude/hooks/lib/skill-auto-selector.sh` - Analyze task, select skills
- `.claude/hooks/lib/skill-injector.sh` - Inject skill context

**Acceptance Criteria:**
- [ ] Task analyzed on SessionStart
- [ ] Skills pre-selected based on keywords
- [ ] Selection injected into AGENT_CONTEXT.md

---

### TASK-AUTONOMY-006: Skill Enforcement Hook
**Status:** pending
**Priority:** CRITICAL
**Estimated Tokens:** 50K

Block execution if skill check skipped.

**Files to modify/create:**
- `.claude/hooks/pre-tool-validation.sh` - Add skill check validation

**Acceptance Criteria:**
- [ ] Detects if skill check was performed
- [ ] Warns if skill check skipped
- [ ] Optionally blocks TaskUpdate

---

### TASK-AUTONOMY-007: Skill Metrics Auto-Updater
**Status:** pending
**Priority:** MEDIUM
**Estimated Tokens:** 50K

Auto-update skill-registry.yaml with usage data.

**Files to create:**
- `.claude/hooks/lib/skill-metrics-updater.sh` - Update metrics

**Acceptance Criteria:**
- [ ] Parse THOUGHTS.md for skill mentions
- [ ] Update skill-usage.yaml
- [ ] Calculate effectiveness scores

---

## Phase 3: Learning Extraction (Week 3)

### TASK-AUTONOMY-008: Learning Extractor Hook
**Status:** pending
**Priority:** CRITICAL
**Estimated Tokens:** 75K

Parse THOUGHTS.md and extract structured learnings.

**Files to create:**
- `.claude/hooks/lib/learning-extractor.sh` - Extract insights
- `.claude/hooks/lib/insight-parser.sh` - Parse patterns

**Acceptance Criteria:**
- [ ] Parse THOUGHTS.md for decision patterns
- [ ] Extract what worked, what didn't
- [ ] Structure for storage

---

### TASK-AUTONOMY-009: Improvement Generator
**Status:** pending
**Priority:** HIGH
**Estimated Tokens:** 75K

Auto-create improvement tasks from extracted learnings.

**Files to create:**
- `.claude/hooks/lib/improvement-generator.sh` - Create tasks
- `.claude/hooks/lib/task-creator.sh` - Create task files

**Acceptance Criteria:**
- [ ] Generate improvement tasks from learnings
- [ ] Link to source learning
- [ ] Add to appropriate goal/plan

---

### TASK-AUTONOMY-010: CLAUDE.md Auto-Updater
**Status:** pending
**Priority:** MEDIUM
**Estimated Tokens:** 50K

Suggest instruction updates every 5 runs.

**Files to create:**
- `.claude/hooks/lib/claude-md-updater.sh` - Suggest updates

**Acceptance Criteria:**
- [ ] Track run count
- [ ] Analyze last 5 learnings
- [ ] Synthesize pattern suggestions
- [ ] Create PR for CLAUDE.md updates

---

## Phase 4: System Health (Week 4)

### TASK-AUTONOMY-011: BB5 Health CLI
**Status:** pending
**Priority:** HIGH
**Estimated Tokens:** 75K

Real-time system status command.

**Files to create:**
- `bin/bb5-health` - Health check command

**Acceptance Criteria:**
- [ ] Show current task status
- [ ] Show goal progress
- [ ] Show queue depth
- [ ] Show recent events

---

### TASK-AUTONOMY-012: BB5 Dashboard
**Status:** pending
**Priority:** MEDIUM
**Estimated Tokens:** 75K

Visual dashboard for system metrics.

**Files to create:**
- `bin/bb5-dashboard` - Dashboard command

**Acceptance Criteria:**
- [ ] Token burn rate
- [ ] Task completion velocity
- [ ] Skill effectiveness
- [ ] Goal burndown

---

### TASK-AUTONOMY-013: Bottleneck Detector
**Status:** pending
**Priority:** MEDIUM
**Estimated Tokens:** 50K

Auto-detect stuck tasks and issues.

**Files to create:**
- `.claude/hooks/lib/bottleneck-detector.sh` - Detect issues

**Acceptance Criteria:**
- [ ] Detect tasks stuck >7 days
- [ ] Detect unused skills
- [ ] Detect failed hooks
- [ ] Generate alert tasks

---

## Phase 5: Integration & Testing (Week 5)

### TASK-AUTONOMY-014: Hook Integration Testing
**Status:** pending
**Priority:** CRITICAL
**Estimated Tokens:** 100K

Test all hooks with real tasks.

**Acceptance Criteria:**
- [ ] 3+ real tasks executed end-to-end
- [ ] All automation verified
- [ ] Issues documented

---

### TASK-AUTONOMY-015: Documentation & Handoff
**Status:** pending
**Priority:** HIGH
**Estimated Tokens:** 100K

Document the autonomy system.

**Deliverables:**
- [ ] HOOKS_AUTONOMY.md - How the automation works
- [ ] TROUBLESHOOTING.md - Common issues
- [ ] v2 specification with learnings

---

## Configuration

### settings.json Updates

Add to existing SessionStart, PreToolUse, SessionEnd hooks from IG-010.

---

## Success Metrics

| Phase | Metric | Target |
|-------|--------|--------|
| 1 | Task auto-completion rate | 90%+ |
| 2 | Skill auto-invocation rate | 80%+ |
| 3 | Learning extraction rate | 15%+ |
| 4 | Dashboard coverage | 100% |
| 5 | End-to-end test pass | 3/3 |

---

## Coordination with IG-010

This plan **complements** IG-010:
- IG-010 builds the hook infrastructure
- This plan builds the intelligence layer
- Shared library: `.claude/hooks/lib/`
- Coordinate via THOUGHTS.md in shared runs

---

## Notes

Estimated total tokens: ~1M (as allocated by user)
Each task should be self-contained and testable.
Document learnings in run folders after each task.
