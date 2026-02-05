# BB5 Unified Hook System - Design Specification

**Version:** 2.0
**Date:** 2026-02-06
**Status:** Design Phase

---

## 1. Current State Analysis

### What Exists (Two Parallel Systems)

**BB5 Smart Hooks (Active in .claude/settings.json):**
- ✅ Agent type detection (planner/executor/architect)
- ✅ Context loading via AGENT_CONTEXT.md
- ✅ Security rules (rm -rf, .env, force push blocking)
- ✅ Documentation validation (blocks on unfilled templates)
- ✅ Timeline maintenance
- ❌ No run folder creation
- ❌ No queue synchronization
- ❌ No automatic task completion

**RALF Hooks (Inactive in bin/):**
- ✅ Run folder creation (THOUGHTS.md, RESULTS.md, DECISIONS.md, metadata.yaml)
- ✅ Queue synchronization
- ✅ Git commit on completion
- ❌ Assumes environment variables
- ❌ No agent detection
- ❌ No security rules

### Research Insights (from claude-code-hooks-mastery)

**13 Hook Events Available:**
1. UserPromptSubmit - Prompt validation, context injection
2. PreToolUse - Security blocking, validation
3. PostToolUse - Logging, validation
4. PostToolUseFailure - Error logging
5. Notification - TTS alerts
6. Stop - AI-generated completion (can block)
7. SubagentStart - Subagent spawn logging
8. SubagentStop - Subagent completion (can block)
9. PreCompact - Transcript backup
10. SessionStart - Context loading
11. SessionEnd - Cleanup, logging
12. PermissionRequest - Permission auditing
13. Setup - Environment persistence

---

## 2. BB5 Hook Requirements

Based on system analysis, BB5 needs hooks for:

### A. Task Lifecycle Management
- Task claiming from queue
- Task completion validation
- Task state transitions (pending → in_progress → completed)
- Task archival (active/ → completed/)

### B. Timeline Synchronization
- Project timeline updates
- Goal progress updates
- Plan milestone tracking
- Task completion events

### C. Memory & Learning
- Memory extraction from runs (THOUGHTS.md, DECISIONS.md, LEARNINGS.md)
- Skill usage logging
- Skill metrics calculation
- Vector store retention

### D. Metadata Management
- queue.yaml synchronization
- events.yaml logging
- skill-usage.yaml updates
- skill-metrics.yaml updates
- Goal YAML progress updates

### E. Validation & Enforcement
- Task completion criteria validation
- Documentation completeness checks
- Single Source of Truth (SSOT) enforcement
- Skill selection verification (CLAUDE.md Phase 1.5)

---

## 3. Proposed Unified Hook Architecture

### Hook Event Mapping

| Hook Event | Current | Proposed | Purpose |
|------------|---------|----------|---------|
| **SessionStart** | session-start-blackbox5.sh + session-start-navigation.sh | **MERGE** + add run folder creation | Initialize session, detect agent, load context, create run folder |
| **PreToolUse** | pre-tool-security.py + pre-tool-validation.sh + architecture-consistency.sh | **KEEP** + add skill-check validation | Security, validation, skill enforcement |
| **PostToolUse** | timeline-maintenance.sh + context-synchronization.sh | **KEEP** + add state tracking | Timeline updates, progress tracking |
| **SubagentStart** | subagent-tracking.sh | **KEEP** | Log subagent spawn |
| **SubagentStop** | subagent-tracking.sh | **KEEP** + add result capture | Log subagent completion, capture results |
| **Stop** | stop-validate-docs.sh + stop-hierarchy-update.sh | **MERGE** + add checkpoint | Validate docs, update hierarchy, save checkpoint |
| **SessionEnd** | session-end-context-update.sh | **REPLACE** with comprehensive finalization | Task completion, memory extraction, skill logging, timeline update, queue sync |
| **UserPromptSubmit** | user-prompt-context.sh | **OPTIONAL** | Context loading on each prompt |
| **PreCompact** | pre-compact-summarize.sh | **OPTIONAL** | Backup before context compaction |

### New Hook: SessionEnd Comprehensive Finalization

This is the most critical hook - it replaces the simple session-end-context-update.sh with a comprehensive finalization pipeline:

```
SessionEnd Hook Flow:
├── 1. Task Completion Validation
│   ├── Check task.md success criteria
│   ├── Verify RESULTS.md exists and is non-empty
│   ├── Validate all checkboxes marked
│   └── If valid → proceed, else → block with warning
│
├── 2. Memory Extraction (RETAIN)
│   ├── Parse THOUGHTS.md for insights
│   ├── Parse DECISIONS.md for decisions
│   ├── Parse LEARNINGS.md for learnings
│   ├── Parse RESULTS.md for outcomes
│   └── Store in vector store via retain-on-complete.py
│
├── 3. Skill Usage Logging
│   ├── Parse THOUGHTS.md for skill mentions
│   ├── Log to operations/skill-usage.yaml
│   └── Update operations/skill-metrics.yaml
│
├── 4. Timeline Updates
│   ├── Add completion event to timeline.yaml
│   ├── Update goal progress in goals/active/[GOAL]/goal.yaml
│   └── Update plan status if applicable
│
├── 5. Queue Synchronization
│   ├── Update task status in queue.yaml (completed)
│   ├── Add completion timestamp
│   └── Log to events.yaml
│
├── 6. Task Archival
│   ├── Move task from tasks/active/ to tasks/completed/
│   ├── Update task.md status
│   └── Create COMPLETION.md summary
│
├── 7. Git Commit (Optional)
│   ├── Stage all changes
│   ├── Create standardized commit message
│   └── Commit with task reference
│
└── 8. Run Archival
    ├── Update metadata.yaml with end timestamp
    ├── Move run to completed/ directory
    └── Create run summary
```

---

## 4. Implementation Plan

### Phase 1: SessionEnd Hook (Critical)
**Priority:** HIGHEST
**Files to Create:**
- `.claude/hooks/session-end-finalize.sh` - Main orchestrator
- `.claude/hooks/lib/task-validator.sh` - Task completion validation
- `.claude/hooks/lib/memory-extractor.sh` - Memory extraction
- `.claude/hooks/lib/skill-logger.sh` - Skill usage logging
- `.claude/hooks/lib/timeline-updater.sh` - Timeline updates
- `.claude/hooks/lib/queue-sync.sh` - Queue synchronization

**Replaces:** `session-end-context-update.sh`

### Phase 2: SessionStart Hook Enhancement
**Priority:** HIGH
**Files to Modify:**
- `.claude/hooks/session-start-blackbox5.sh` - Add run folder creation

**Adds:**
- Create THOUGHTS.md, RESULTS.md, DECISIONS.md, metadata.yaml
- Export RALF_RUN_DIR, RALF_RUN_ID
- Initialize task context from queue.yaml

### Phase 3: PreToolUse Enhancement
**Priority:** MEDIUM
**Files to Modify:**
- `.claude/hooks/pre-tool-validation.sh` - Add skill-check validation

**Adds:**
- Verify skill selection was checked (CLAUDE.md Phase 1.5)
- Block if TaskUpdate tool used without skill check

### Phase 4: Stop Hook Enhancement
**Priority:** MEDIUM
**Files to Modify:**
- `.claude/hooks/stop-hierarchy-update.sh` - Merge with checkpoint logic

**Adds:**
- Save run checkpoint
- Update metadata.yaml
- Sync THOUGHTS.md

### Phase 5: Cleanup
**Priority:** LOW
**Actions:**
- Archive `bin/ralf-*-hook.sh` files
- Remove `session-end-context-update.sh`
- Update HOOKS.md documentation

---

## 5. Hook Library Structure

```
.claude/hooks/
├── session-start-blackbox5.sh          # Enhanced with run creation
├── session-start-navigation.sh         # Keep as-is
├── pre-tool-security.py                # Keep as-is
├── pre-tool-validation.sh              # Enhanced with skill check
├── architecture-consistency.sh         # Keep as-is
├── post-tool-timeline.sh               # Renamed from timeline-maintenance.sh
├── post-tool-context-sync.sh           # Renamed from context-synchronization.sh
├── subagent-tracking.sh                # Keep as-is
├── stop-validate-docs.sh               # Keep as-is
├── stop-hierarchy-update.sh            # Enhanced with checkpoint
├── session-end-finalize.sh             # NEW - Comprehensive finalization
├── user-prompt-context.sh              # Keep as-is (optional)
├── pre-compact-summarize.sh            # Keep as-is (optional)
└── lib/                                # NEW - Shared libraries
    ├── bb5-common.sh                   # Common functions (detect_agent_type, etc.)
    ├── task-validator.sh               # Task completion validation
    ├── memory-extractor.sh             # Memory extraction
    ├── skill-logger.sh                 # Skill usage logging
    ├── timeline-updater.sh             # Timeline updates
    └── queue-sync.sh                   # Queue synchronization
```

---

## 6. Configuration Updates

### settings.json Changes

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          { "type": "command", "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/session-start-blackbox5.sh" },
          { "type": "command", "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/session-start-navigation.sh" }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          { "type": "command", "command": "python3 /Users/shaansisodia/.blackbox5/.claude/hooks/pre-tool-security.py" },
          { "type": "command", "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/pre-tool-validation.sh" },
          { "type": "command", "command": "bash /Users/shaansisodia/.claude/hooks/architecture-consistency.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          { "type": "command", "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/post-tool-timeline.sh" },
          { "type": "command", "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/post-tool-context-sync.sh" }
        ]
      }
    ],
    "SubagentStart": [
      {
        "matcher": "*",
        "hooks": [
          { "type": "command", "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/subagent-tracking.sh start" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "*",
        "hooks": [
          { "type": "command", "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/subagent-tracking.sh stop" }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/stop-validate-docs.sh" },
          { "type": "command", "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/stop-hierarchy-update.sh" }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          { "type": "command", "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/session-end-finalize.sh" }
        ]
      }
    ]
  }
}
```

---

## 7. Success Criteria

- [ ] SessionStart creates run folder with all required files
- [ ] SessionEnd validates task completion before allowing exit
- [ ] SessionEnd extracts memories and stores in vector store
- [ ] SessionEnd logs skill usage to skill-usage.yaml
- [ ] SessionEnd updates timeline.yaml with completion event
- [ ] SessionEnd syncs queue.yaml with completed status
- [ ] SessionEnd moves task from active/ to completed/
- [ ] PreToolUse validates skill selection for TaskUpdate
- [ ] Stop hook saves checkpoint before exit
- [ ] All hooks use self-discovery (no env var dependencies)
- [ ] Hooks follow fail-silent pattern (never break user experience)

---

## 8. Next Steps

1. **Create Task:** TASK-HOOKS-001 - Implement SessionEnd Finalization Hook
2. **Create Task:** TASK-HOOKS-002 - Enhance SessionStart with Run Creation
3. **Create Task:** TASK-HOOKS-003 - Add Skill Check Validation to PreToolUse
4. **Create Task:** TASK-HOOKS-004 - Enhance Stop Hook with Checkpoint
5. **Create Task:** TASK-HOOKS-005 - Archive RALF Hooks and Update Documentation

---

*This specification merges the best of BB5 Smart Hooks (agent-aware, self-discovering, security-focused) with RALF execution flow (run creation, queue sync, completion handling) into a unified, production-ready hook system.*
