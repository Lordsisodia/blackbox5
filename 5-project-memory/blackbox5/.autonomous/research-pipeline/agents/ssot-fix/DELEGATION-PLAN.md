# SSOT Fix Sub-Agent Delegation Plan

**Task:** TASK-ARCH-003 Fix Single Source of Truth Violations
**Approach:** Plan → Audit → Execute → Validate
**Architecture:** Adapted Dual-RALF Worker-Validator Pairs
**Created:** 2026-02-04

---

## Overview

This plan maps TASK-ARCH-003A/B/C/D to specialized sub-agents using the Dual-RALF worker-validator pattern. Instead of Scout/Analyst/Planner, we use **Auditor/Fixer/Validator** roles tailored for SSOT remediation.

```
┌─────────────────────────────────────────────────────────────────┐
│                    SSOT FIX PIPELINE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐                        │
│  │Auditor Worker│◄────►│Auditor Validator│  (Audit Phase)      │
│  │  (RALF Loop) │      │  (RALF Loop)  │                        │
│  └──────┬───────┘      └──────────────┘                        │
│         │                                                        │
│         ▼ audit-report.md                                        │
│  ┌──────────────┐      ┌──────────────┐                        │
│  │ Fixer Worker │◄────►│Fixer Validator│  (Execution Phase)    │
│  │  (RALF Loop) │      │  (RALF Loop)  │                        │
│  └──────┬───────┘      └──────────────┘                        │
│         │                                                        │
│         ▼ fixes.yaml                                             │
│  ┌──────────────┐      ┌──────────────┐                        │
│  │ Final Validator│◄──►│Final Validator│  (Validation Phase)   │
│  │  (Worker)    │      │  (Validator)  │                        │
│  └──────┬───────┘      └──────────────┘                        │
│         │                                                        │
│         ▼ STATE.yaml fixed                                       │
│  ┌──────────────────────────────────────┐                      │
│  │         TASK-ARCH-003 COMPLETE        │                      │
│  └──────────────────────────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Mapping

### Phase 1: AUDIT (TASK-ARCH-003B)

**Auditor Worker** → `bmad-analyst` skill (research/analysis)
- **Purpose:** Inventory all files, document broken references, version mismatches
- **Inputs:** STATE.yaml, project/context.yaml, goals/active/*, bin/validate-ssot.py
- **Outputs:** audit-report.md with findings table
- **Token Budget:** 4,000 (40% of 10K context)

**Auditor Validator** → `bmad-qa` skill (testing/quality)
- **Purpose:** Verify audit completeness, check for missed violations
- **Inputs:** Auditor Worker's audit-report.md, validate-ssot.py output
- **Outputs:** Validation feedback, coverage assessment
- **Token Budget:** 1,500 (40% of 3.75K context)

**Communication:**
```yaml
# communications/ssot-audit-state.yaml
phase: audit
worker_status: in_progress
validator_status: monitoring
findings_count: 0
last_updated: "2026-02-04T07:35:00Z"
```

---

### Phase 2: EXECUTE (TASK-ARCH-003C)

**Fixer Worker** → `bmad-dev` skill (implementation)
- **Purpose:** Execute fixes: YAML syntax, remove deleted refs, sync versions
- **Inputs:** audit-report.md, STATE.yaml, context.yaml
- **Outputs:** Fixed STATE.yaml, git commit
- **Token Budget:** 5,000 (40% of 12.5K context)

**Fixer Validator** → `bmad-architect` skill (system design review)
- **Purpose:** Validate fixes follow SSOT principles, no new violations introduced
- **Inputs:** Fixer Worker's changes, first-principles-checklist.md
- **Outputs:** Architecture review, approval/block decision
- **Token Budget:** 2,000 (40% of 5K context)

**Communication:**
```yaml
# communications/ssot-fixer-state.yaml
phase: execute
worker_status: in_progress
validator_status: monitoring
fixes_applied: []
rollback_point: "STATE.yaml.backup.20260204-073500"
last_updated: "2026-02-04T07:35:00Z"
```

---

### Phase 3: VALIDATE (TASK-ARCH-003D)

**Final Validator Pair** → `bmad-qa` + `bmad-tea`
- **Worker:** Run full validation suite, test RALF context
- **Validator:** Verify all success criteria met
- **Token Budget:** 2,000 combined

**Communication:**
```yaml
# communications/ssot-validation-state.yaml
phase: validate
validation_status: in_progress
checks_passed: 0
checks_total: 6
last_updated: "2026-02-04T07:35:00Z"
```

---

## Directory Structure

```
5-project-memory/blackbox5/
└── .autonomous/
    └── research-pipeline/
        └── agents/
            └── ssot-fix/                    # NEW: SSOT Fix Agents
                ├── README.md
                ├── DELEGATION-PLAN.md       # This file
                │
                ├── auditor-worker/          # TASK-ARCH-003B execution
                │   ├── state/
                │   ├── memory/
                │   │   └── audit-patterns.md
                │   └── runs/
                │       └── run-001/
                │           ├── THOUGHTS.md
                │           ├── RESULTS.md
                │           ├── DECISIONS.md
                │           └── metadata.yaml
                │
                ├── auditor-validator/       # Audit validation
                │   ├── state/
                │   ├── memory/
                │   │   └── coverage-models.md
                │   └── runs/
                │
                ├── fixer-worker/            # TASK-ARCH-003C execution
                │   ├── state/
                │   ├── memory/
                │   │   └── fix-strategies.md
                │   └── runs/
                │
                ├── fixer-validator/         # Fix validation
                │   ├── state/
                │   ├── memory/
                │   │   └── ssot-principles.md
                │   └── runs/
                │
                └── final-validator/         # TASK-ARCH-003D
                    ├── state/
                    └── runs/
```

---

## Communication Files

### Shared State

```yaml
# communications/ssot-pipeline-state.yaml
pipeline:
  task_id: TASK-ARCH-003
  status: in_progress
  current_phase: audit
  started_at: "2026-02-04T07:35:00Z"

phases:
  audit:
    status: pending
    worker: auditor-worker
    validator: auditor-validator
    deliverable: audit-report.md

  execute:
    status: pending
    worker: fixer-worker
    validator: fixer-validator
    deliverable: fixed STATE.yaml
    depends_on: audit

  validate:
    status: pending
    worker: final-validator
    deliverable: validation report
    depends_on: execute

metadata:
  last_updated: "2026-02-04T07:35:00Z"
  estimated_completion: "2026-02-04T09:00:00Z"
```

### Events

```yaml
# communications/ssot-events.yaml
events:
  - timestamp: "2026-02-04T07:35:00Z"
    event_type: pipeline.started
    agent: system
    data:
      task: TASK-ARCH-003
      phases: 3

  - timestamp: "2026-02-04T07:40:00Z"
    event_type: audit.started
    agent: auditor-worker

  - timestamp: "2026-02-04T07:55:00Z"
    event_type: audit.complete
    agent: auditor-worker
    data:
      findings: 8
      report_path: "tasks/active/TASK-ARCH-003/subtasks/TASK-ARCH-003B/audit-report.md"

  - timestamp: "2026-02-04T08:00:00Z"
    event_type: execute.started
    agent: fixer-worker

  - timestamp: "2026-02-04T08:45:00Z"
    event_type: execute.complete
    agent: fixer-worker
    data:
      files_modified: 3
      commit_hash: "abc123"

  - timestamp: "2026-02-04T08:50:00Z"
    event_type: validate.started
    agent: final-validator

  - timestamp: "2026-02-04T09:00:00Z"
    event_type: validate.complete
    agent: final-validator
    data:
      all_checks_passed: true
      errors_before: 8
      errors_after: 0
```

### Chat Log

```yaml
# communications/ssot-chat-log.yaml
messages:
  # Auditor coordination
  - from: auditor-validator
    to: auditor-worker
    timestamp: "2026-02-04T07:50:00Z"
    type: feedback
    content: "Check goals/active/IG-007/ for additional task references not in STATE.yaml"

  # Fixer coordination
  - from: fixer-validator
    to: fixer-worker
    timestamp: "2026-02-04T08:30:00Z"
    type: block
    content: "Hold on version sync - context.yaml should be canonical, not STATE.yaml"

  - from: fixer-worker
    to: fixer-validator
    timestamp: "2026-02-04T08:35:00Z"
    type: response
    content: "Fixed - now using context.yaml as canonical, STATE.yaml references it"

  - from: fixer-validator
    to: fixer-worker
    timestamp: "2026-02-04T08:36:00Z"
    type: approve
    content: "Approach validated. Proceed with commit."
```

---

## Timeline Memory Template

Each agent gets injected timeline memory via SessionStart hook:

### Auditor Worker Timeline

```markdown
## Agent Identity
You are the **Auditor Worker** in the SSOT Fix Pipeline.
Task: TASK-ARCH-003B | Phase: Audit
Session: run-20260204-073535

## Your Timeline Memory

### Work History
- No previous runs

### Work Queue
priority_items:
  - "Inventory STATE.yaml root_files vs actual files"
  - "Document YAML parse error (lines 360-361)"
  - "Compare versions: STATE.yaml vs context.yaml"
  - "Audit goal-task links in IG-006, IG-007"

backlog:
  - "Check folder contents match STATE.yaml"
  - "Validate with bin/validate-ssot.py"

### Current Assignment
in_progress: null
last_completed: null

## Work Assignment Logic

1. Check work_queue.priority_items
2. If empty, check work_queue.backlog
3. If empty, check communications/ssot-events.yaml
4. If empty, EXIT (Status: IDLE)

## Success Criteria
- [ ] All root files inventoried
- [ ] All broken references documented
- [ ] Version mismatch identified
- [ ] Goal-task links audited
- [ ] Audit report written
```

### Fixer Worker Timeline

```markdown
## Agent Identity
You are the **Fixer Worker** in the SSOT Fix Pipeline.
Task: TASK-ARCH-003C | Phase: Execute
Session: run-20260204-073535

## Your Timeline Memory

### Work History
- No previous runs

### Work Queue
priority_items:
  - "Backup STATE.yaml"
  - "Fix YAML parse error (lines 360-361)"
  - "Remove 5 deleted file references"
  - "Update project section to reference context.yaml"
  - "Sync version numbers"
  - "Fix IG-006 goal-task links"

backlog: []

### Dependencies
waiting_for: "TASK-ARCH-003B audit-report.md"

## Rollback Points
- Backup: STATE.yaml.backup.20260204-073500
- Git commit: Pre-change state

## Work Assignment Logic

1. Check if audit-report.md exists
2. If not, EXIT (Status: BLOCKED)
3. Read audit findings
4. Execute fixes in order
5. Validate after each fix
6. Commit when all complete
```

---

## Execution Flow

```
Time ─────────────────────────────────────────────────────────────►

┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: AUDIT (TASK-ARCH-003B)                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Auditor Worker          Auditor Validator          System       │
│      │                        │                        │        │
│      │ 1. Read timeline       │                        │        │
│      │    (injected)          │                        │        │
│      │                        │                        │        │
│      │ 2. Check work_queue    │                        │        │
│      │    → inventory task    │                        │        │
│      │                        │                        │        │
│      ▼                        │                        │        │
│   ┌────────────────┐          │                        │        │
│   │ Inventory      │          │                        │        │
│   │ STATE.yaml     │          │                        │        │
│   │ vs actual      │          │                        │        │
│   │ files          │          │                        │        │
│   └────────┬───────┘          │                        │        │
│            │                  │                        │        │
│            │ 3. Write         │  1. Read timeline      │        │
│            │    THOUGHTS.md   │     (injected)         │        │
│            │    RESULTS.md    │                        │        │
│            │                  │  2. Find worker run    │        │
│            │                  │  3. Read results       │        │
│            │                  │  4. Check coverage     │        │
│            │◄─────────────────│  5. Write feedback     │        │
│            │   chat-log.yaml  │     "Check IG-007..."  │        │
│            │                  │                        │        │
│            │ 4. Update        │  6. Update timeline    │        │
│            │    timeline      │                        │        │
│            │                  │                        │        │
│   ┌────────┴────────┐   ┌────┴────┐                   │        │
│   │   RUN END       │   │ RUN END │                   │        │
│   └─────────────────┘   └─────────┘                   │        │
│            │                  │                        │        │
│            ▼                  ▼                        ▼        │
│   ┌────────────────────────────────────────────────────────┐   │
│   │ NEXT RUN: Apply validator feedback, complete audit     │   │
│   │ Publish: audit.complete event                          │   │
│   └────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: EXECUTE (TASK-ARCH-003C)                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Fixer Worker            Fixer Validator                         │
│      │                        │                                 │
│      │ 1. Read timeline       │                                 │
│      │    See audit.complete  │                                 │
│      │                        │                                 │
│      │ 2. Load audit-report   │                                 │
│      │                        │                                 │
│      ▼                        │                                 │
│   ┌────────────────┐          │                                 │
│   │ Execute fixes  │          │                                 │
│   │ in order:      │          │                                 │
│   │ 1. Backup      │          │                                 │
│   │ 2. YAML fix    │          │                                 │
│   │ 3. Remove refs │          │                                 │
│   │ 4. Update proj │          │                                 │
│   │ 5. Sync ver    │          │                                 │
│   │ 6. Fix goals   │          │                                 │
│   └────────┬───────┘          │                                 │
│            │                  │                                 │
│            │ 3. Validate      │  1. Read timeline               │
│            │    after each    │  2. Monitor fixes                 │
│            │                  │  3. Check SSOT principles       │
│            │◄─────────────────│  4. Block if violation          │
│            │   "Block: use    │     "Use ref, not dup"          │
│            │    reference"    │  5. Approve when fixed          │
│            │                  │                                 │
│            │ 4. Commit        │                                 │
│            │    when approved │                                 │
│            │                  │                                 │
│   ┌────────┴────────┐   ┌────┴────┐                            │
│   │   RUN END       │   │ RUN END │                            │
│   └─────────────────┘   └─────────┘                            │
│            │                  │                                 │
│            ▼                  ▼                                 │
│   Publish: execute.complete event                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: VALIDATE (TASK-ARCH-003D)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Final Validator                                                 │
│      │                                                          │
│      │ 1. Read execute.complete event                            │
│      │                                                          │
│      ▼                                                          │
│   ┌────────────────┐                                            │
│   │ Run validation │                                            │
│   │ checklist:     │                                            │
│   │ - validate-ssot.py                                         │
│   │ - YAML syntax  │                                            │
│   │ - RALF context │                                            │
│   │ - Git status   │                                            │
│   └────────┬───────┘                                            │
│            │                                                     │
│            │ 2. Write RESULTS.md                                 │
│            │    Update task.md                                   │
│            │    Mark complete                                    │
│            │                                                     │
│   ┌────────┴────────┐                                            │
│   │   PIPELINE      │                                            │
│   │   COMPLETE      │                                            │
│   └─────────────────┘                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Token Budget Summary

| Agent | Skill | Target/Run | Context | Frequency | Phase Budget |
|-------|-------|-----------|---------|-----------|--------------|
| Auditor Worker | bmad-analyst | 4,000 | 10K (40%) | 2 runs | 8K |
| Auditor Validator | bmad-qa | 1,500 | 3.75K (40%) | 2 runs | 3K |
| Fixer Worker | bmad-dev | 5,000 | 12.5K (40%) | 3 runs | 15K |
| Fixer Validator | bmad-architect | 2,000 | 5K (40%) | 3 runs | 6K |
| Final Validator | bmad-qa+tea | 2,000 | 5K (40%) | 1 run | 2K |
| **TOTAL** | | | | | **~34K** |

Very efficient - only 34K tokens for complete SSOT fix pipeline.

---

## Success Criteria

- [x] All 4 subtasks have assigned worker-validator pairs
- [x] Communication files defined (state, events, chat-log)
- [x] Timeline memory templates created
- [x] Token budgets allocated
- [x] Execution flow documented
- [x] Rollback points identified

## Next Steps

1. Create agent directories and timeline-memory.md files
2. Set up communication files
3. Launch Auditor Worker (TASK-ARCH-003B)
4. Monitor via communications/ssot-events.yaml
5. Proceed through phases based on events

---

**Ready to execute:** Run initialization → Launch Auditor Worker
