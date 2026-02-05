# BB5 Hook Requirements - Comprehensive Analysis

**Date:** 2026-02-06
**Sources:** BB5 Implementation Analysis + External GitHub Research

---

## Executive Summary

Based on thorough analysis, we need **31 distinct hooks** across 12 categories. The current system has **two parallel hook systems** that need unification.

**Key Finding:** You're absolutely right - updating timelines on every PostToolUse is overkill. Most updates should happen at checkpoints (Stop) or session end (SessionEnd), not per-tool.

---

## Current Hook Inventory

### BB5 Smart Hooks (Active)
| Hook | Purpose | Status |
|------|---------|--------|
| session-start-blackbox5.sh | Agent detection + context loading | ✅ Working |
| session-start-navigation.sh | Navigation context | ✅ Working |
| pre-tool-security.py | Security blocking | ✅ Working |
| pre-tool-validation.sh | Validation | ✅ Working |
| architecture-consistency.sh | Naming enforcement | ✅ Working |
| timeline-maintenance.sh | Timeline updates | ⚠️ **Too frequent** |
| context-synchronization.sh | Context sync | ✅ Working |
| subagent-tracking.sh | Agent lifecycle | ✅ Working |
| stop-validate-docs.sh | Doc validation | ✅ Working |
| stop-hierarchy-update.sh | Hierarchy updates | ✅ Working |
| session-end-context-update.sh | Context update | ❌ **Insufficient** |

### RALF Hooks (Inactive)
| Hook | Purpose | Status |
|------|---------|--------|
| ralf-session-start-hook.sh | Run folder creation | ❌ NOT WIRED |
| ralf-stop-hook.sh | Completion + archival | ❌ NOT WIRED |
| ralf-post-tool-hook.sh | File change detection | ❌ NOT WIRED |

---

## Revised Hook Architecture (Your Feedback Incorporated)

### Principle: "Checkpoint-Based, Not Per-Tool"

**OLD (Wrong):** Update timeline on every PostToolUse
**NEW (Right):** Update timeline at checkpoints (Stop) and session end (SessionEnd)

### Proposed Hook Events

| Hook Event | Current | Proposed | Rationale |
|------------|---------|----------|-----------|
| **SessionStart** | Keep | **Enhanced** | Add run folder creation |
| **PreToolUse** | Keep | **Keep** | Security + validation |
| **PostToolUse** | timeline + context | **REMOVE** | Move to Stop/SessionEnd |
| **SubagentStart** | Keep | **Enhanced** | Add context inheritance |
| **SubagentStop** | Keep | **Enhanced** | Add result capture + validation |
| **Stop** | docs + hierarchy | **Enhanced** | Add checkpoint save |
| **SessionEnd** | context update | **REPLACE** | Comprehensive finalization |

---

## Critical Hook Requirements (From Analysis)

### 1. SessionStart Hook (Enhanced)
**Current:** Loads context
**Missing:** Run folder creation

**Should Do:**
1. Detect agent type (planner/executor/architect)
2. Create run folder: `runs/{agent_type}/run-{timestamp}/`
3. Create required files:
   - THOUGHTS.md
   - RESULTS.md
   - DECISIONS.md
   - ASSUMPTIONS.md
   - LEARNINGS.md
   - metadata.yaml
4. Load relevant memories from vector store
5. Inject context via AGENT_CONTEXT.md

---

### 2. PreToolUse Hook (Keep + Enhance)
**Current:** Security + validation
**Missing:** Skill check enforcement

**Should Do:**
1. Security blocking (rm -rf, .env, force push)
2. Architecture validation
3. **NEW:** Skill selection validation (CLAUDE.md Phase 1.5)
4. **NEW:** File access validation (stay within routes.yaml permissions)

---

### 3. SubagentStart Hook (Enhanced)
**Current:** Logs to events.yaml
**Missing:** Context inheritance

**Should Do:**
1. Log subagent spawn to events.yaml
2. **NEW:** Pass parent context to subagent
3. **NEW:** Track parent-child relationship
4. **NEW:** Inherit task context

---

### 4. SubagentStop Hook (Enhanced)
**Current:** Logs completion
**Missing:** Result validation

**Should Do:**
1. Log subagent completion to events.yaml
2. **NEW:** Validate subagent output
3. **NEW:** Capture results for parent
4. **NEW:** Update parent task progress
5. **NEW:** Trigger parent continuation

---

### 5. Stop Hook (Enhanced Checkpoint)
**Current:** Doc validation + hierarchy update
**Missing:** Checkpoint save

**Should Do:**
1. Validate documentation (THOUGHTS.md, RESULTS.md filled)
2. Update parent timelines
3. **NEW:** Save checkpoint:
   - Current THOUGHTS.md state
   - Task progress
   - Metadata snapshot
4. **NEW:** Timeline checkpoint event
5. **NEW:** Can block if critical issues found

---

### 6. SessionEnd Hook (Comprehensive Finalization)
**Current:** Simple context update
**Missing:** Everything else

**Should Do (8-Step Pipeline):**

```
SessionEnd Pipeline:
├── 1. Task Completion Validation
│   ├── Check task.md success criteria
│   ├── Verify RESULTS.md exists and non-empty
│   ├── Validate all checkboxes marked
│   └── BLOCK if incomplete (with warning)
│
├── 2. Memory Extraction (RETAIN)
│   ├── Parse THOUGHTS.md for insights
│   ├── Parse DECISIONS.md for decisions
│   ├── Parse LEARNINGS.md for learnings
│   └── Store in vector store
│
├── 3. Skill Usage Logging
│   ├── Parse THOUGHTS.md for skill mentions
│   ├── Log to operations/skill-usage.yaml
│   └── Update operations/skill-metrics.yaml
│
├── 4. Timeline Finalization
│   ├── Add completion event to timeline.yaml
│   ├── Update goal progress
│   └── Update plan status
│
├── 5. Queue Synchronization
│   ├── Update task status to "completed"
│   ├── Add completion timestamp
│   ├── Log to events.yaml
│   └── Unblock dependent tasks
│
├── 6. Task Archival
│   ├── Move task from active/ to completed/
│   ├── Update task.md status
│   └── Create COMPLETION.md summary
│
├── 7. Git Commit (Optional)
│   ├── Stage all changes
│   ├── Create standardized commit message
│   └── Commit with task reference
│
└── 8. Run Finalization
    ├── Update metadata.yaml
    ├── Move run to completed/ (optional)
    └── Generate run summary
```

---

## Missing Hooks Identified (31 Total)

### CRITICAL Priority
| # | Hook | Purpose |
|---|------|---------|
| 1 | Queue Priority Recalculation | Dynamic priority based on context changes |
| 2 | Dependency Resolution | Unblock tasks when dependencies complete |
| 3 | Duplicate Task Detection | Prevent duplicate task creation |
| 4 | Agent Loop Health | Detect infinite loops, excessive iterations |

### HIGH Priority
| # | Hook | Purpose |
|---|------|---------|
| 5 | Task Status Validation | Verify acceptance criteria before completion |
| 6 | Task Creation Sync | Auto-add to queue.yaml on creation |
| 7 | Goal Progress Calculation | Auto-calculate from plan completion |
| 8 | Skill Metrics Update | Record usage, update counts |
| 9 | Required File Enforcement | Ensure THOUGHTS.md, RESULTS.md exist |
| 10 | File Access Validation | Enforce routes.yaml permissions |
| 11 | Sensitive Data Detection | Block credential writes |

### MEDIUM Priority
| # | Hook | Purpose |
|---|------|---------|
| 12 | Plan Metadata Sync | Update effort, status from tasks |
| 13 | Timeline Deduplication | Prevent duplicate events |
| 14 | STATE.yaml Sync | Keep state file current |
| 15 | Routes Validation | Validate paths exist |
| 16 | Decision Propagation | Copy decisions to /decisions/ |
| 17 | Documentation Drift | Flag stale docs |
| 18 | Estimation Accuracy | Track estimate vs actual |

### LOW Priority (19-31)
- Event correlation, Cross-agent comms, Template consistency, Link validation, Skill ROI, etc.

---

## Subagent-Specific Requirements

Subagents need the same hooks as main agents PLUS:

| Hook | Subagent Addition |
|------|-------------------|
| **SessionStart** | Inherit parent context, link to parent task |
| **SubagentStop** | Report results to parent, update parent progress |
| **SessionEnd** | Compact results for parent consumption, don't duplicate parent work |

**Key Principle:** Subagents should update their own task progress, which then triggers parent updates via the Dependency Resolution hook.

---

## Implementation Phases

### Phase 1: Core Lifecycle (Critical)
1. Enhanced SessionStart (run folder creation)
2. Comprehensive SessionEnd (8-step pipeline)
3. Enhanced Stop (checkpoint save)

### Phase 2: Validation & Safety (High)
4. PreToolUse skill check enforcement
5. Task status validation
6. File access validation

### Phase 3: Automation (Medium)
7. Queue sync on task creation
8. Goal progress auto-calculation
9. Dependency resolution

### Phase 4: Intelligence (Lower)
10. Duplicate detection
11. Health monitoring
12. Metrics calculation

---

## Files to Create/Modify

### New Hooks
```
.claude/hooks/
├── session-start-enhanced.sh      # Merge BB5 + RALF session start
├── session-end-finalize.sh        # 8-step finalization pipeline
├── stop-checkpoint.sh             # Enhanced checkpoint (merge existing)
├── lib/
│   ├── bb5-common.sh              # Shared functions
│   ├── task-validator.sh          # Task completion validation
│   ├── memory-extractor.sh        # RETAIN operation
│   ├── skill-logger.sh            # Skill usage logging
│   ├── timeline-updater.sh        # Timeline management
│   └── queue-sync.sh              # Queue operations
```

### Modified Hooks
```
.claude/hooks/
├── pre-tool-validation.sh         # Add skill check
├── subagent-tracking.sh           # Add context inheritance
└── stop-validate-docs.sh          # Keep as-is (working well)
```

### Archived (No Longer Needed)
```
bin/ralf-session-start-hook.sh     # Functionality merged
bin/ralf-stop-hook.sh              # Functionality merged
bin/ralf-post-tool-hook.sh         # Not needed (checkpoint-based)
timeline-maintenance.sh            # Move to Stop/SessionEnd
context-synchronization.sh         # Move to SessionEnd
session-end-context-update.sh      # Replaced by finalize
```

---

## Configuration Changes

### settings.json Updates

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
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /Users/shaansisodia/.blackbox5/.claude/hooks/pre-tool-security.py"
          },
          {
            "type": "command",
            "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/pre-tool-validation.sh"
          }
        ]
      }
    ],
    "SubagentStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/subagent-tracking.sh start"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/subagent-tracking.sh stop"
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

**Key Changes:**
- Removed PostToolUse hooks (timeline-maintenance, context-sync)
- Merged session-start hooks into one enhanced hook
- Replaced session-end-context-update with comprehensive finalize
- Added stop-checkpoint for mid-session saves

---

## Success Criteria

- [ ] SessionStart creates run folder with all required files
- [ ] SessionEnd validates task completion before allowing exit
- [ ] SessionEnd extracts and stores memories in vector store
- [ ] SessionEnd logs skill usage to skill-usage.yaml
- [ ] SessionEnd updates timeline.yaml with completion event
- [ ] SessionEnd syncs queue.yaml and unblocks dependent tasks
- [ ] SessionEnd moves task from active/ to completed/
- [ ] Stop hook saves checkpoint (THOUGHTS.md snapshot)
- [ ] PreToolUse validates skill selection for TaskUpdate
- [ ] SubagentStop captures results and updates parent
- [ ] All hooks use self-discovery (no env var dependencies)
- [ ] Hooks follow fail-silent pattern

---

## Next Steps

1. **Review this design** with you
2. **Create implementation tasks** for Phase 1 (Core Lifecycle)
3. **Begin implementation** with session-start-enhanced.sh
4. **Test incrementally** before moving to Phase 2

---

*This design incorporates your feedback about checkpoint-based updates instead of per-tool updates, and addresses all 31 hook gaps identified in the analysis.*
