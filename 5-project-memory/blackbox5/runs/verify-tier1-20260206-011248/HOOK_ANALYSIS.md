# BB5 Hooks Analysis - Critical Findings

**Date:** 2026-02-06
**Purpose:** Understand what hooks exist and which ones we actually want

---

## Current Hook Inventory

### Active Hooks (in .claude/settings.json)

| Hook Event | Script | Purpose | Status |
|------------|--------|---------|--------|
| **SessionStart** | `session-start-blackbox5.sh` | Auto-detect agent type, load context | ✅ Working |
| **SessionStart** | `session-start-navigation.sh` | Discover hierarchy context | ✅ Working |
| **PreToolUse** | `pre-tool-security.py` | Agent-aware security blocking | ✅ Working |
| **PreToolUse** | `pre-tool-validation.sh` | Validate structure before writes | ✅ Working |
| **PreToolUse** | `architecture-consistency.sh` | Enforce naming conventions | ✅ Working |
| **PostToolUse** | `timeline-maintenance.sh` | Auto-update timeline.yaml | ✅ Working |
| **PostToolUse** | `context-synchronization.sh` | Sync goal progress, task status | ✅ Working |
| **SubagentStart** | `subagent-tracking.sh start` | Log agent spawn to events.yaml | ✅ Working |
| **SubagentStop** | `subagent-tracking.sh stop` | Log agent completion | ✅ Working |
| **Stop** | `stop-validate-docs.sh` | Block if templates unfilled | ✅ Working |
| **Stop** | `stop-hierarchy-update.sh` | Update parent timelines | ✅ Working |
| **SessionEnd** | `session-end-context-update.sh` | Final context update | ✅ Working |
| **UserPromptSubmit** | `user-prompt-context.sh` | Load context on prompt | ✅ Working |
| **PreCompact** | `pre-compact-summarize.sh` | Summarize before context compact | ✅ Working |

**Total: 9 unique hook scripts covering 8 hook events**

---

## RALF Hooks (NOT Wired In)

These exist in `bin/` but are NOT called by settings.json:

| Script | Purpose | Lines | Status |
|--------|---------|-------|--------|
| `ralf-session-start-hook.sh` | Create run folder + templates | 249 | ❌ NOT WIRED |
| `ralf-stop-hook.sh` | Validate, sync queue, commit, archive | 398 | ❌ NOT WIRED |
| `ralf-post-tool-hook.sh` | Detect file modifications | 108 | ❌ NOT WIRED |

---

## Critical Finding: Two Parallel Hook Systems

### System A: BB5 Smart Hooks (ACTIVE)
Located: `.claude/hooks/`
- `session-start-blackbox5.sh` - Agent detection + context loading
- `stop-validate-docs.sh` - Documentation validation
- Plus 7 other hooks

**Characteristics:**
- Self-discovering (no env vars)
- Agent-aware (planner/executor/architect)
- Context injection via AGENT_CONTEXT.md
- Security rules by agent type

### System B: RALF Hooks (INACTIVE)
Located: `bin/ralf-*-hook.sh`
- `ralf-session-start-hook.sh` - Run folder creation
- `ralf-stop-hook.sh` - Completion + archival
- `ralf-post-tool-hook.sh` - File change detection

**Characteristics:**
- Assumes RALF_RUN_DIR environment variable
- Creates THOUGHTS.md, RESULTS.md, DECISIONS.md, metadata.yaml
- Syncs queue.yaml
- Git commit + archive

---

## What Each Hook Actually Does

### session-start-blackbox5.sh (ACTIVE)
```
1. Detects agent type from:
   - Run directory path (/planner/, /executor/, /architect/)
   - File patterns (queue.yaml = planner)
   - Git branch name
   - Parent directories

2. Creates AGENT_CONTEXT.md with:
   - Agent type
   - Queue status (pending/completed counts)
   - Claimed task (for executor)
   - Agent-specific commands

3. Returns JSON with additionalContext for Claude
```

### ralf-session-start-hook.sh (NOT ACTIVE)
```
1. Creates run folder: runs/{agent_type}/run-{timestamp}
2. Creates 4 files:
   - THOUGHTS.md (template)
   - RESULTS.md (template)
   - DECISIONS.md (template)
   - metadata.yaml (structured data)
3. Exports RALF_RUN_DIR, RALF_RUN_ID
```

### stop-validate-docs.sh (ACTIVE)
```
1. Checks for required files: THOUGHTS.md, RESULTS.md, DECISIONS.md, ASSUMPTIONS.md, LEARNINGS.md
2. Blocks session end if:
   - Files are missing
   - Files contain "RALF_TEMPLATE: UNFILLED" or "FILL_ME"
3. Can be skipped with RALF_SKIP_DOC_VALIDATION=1
```

### ralf-stop-hook.sh (NOT ACTIVE)
```
1. Validates completion (checks required files)
2. Updates metadata.yaml with timestamps
3. Syncs queue.yaml (marks tasks completed)
4. Git commit with standardized message
5. Archives run folder to completed/
6. Updates events.yaml
```

---

## The Problem

**We have TWO competing hook systems:**

| Feature | BB5 Hooks (Active) | RALF Hooks (Inactive) |
|---------|-------------------|----------------------|
| Run folder creation | ❌ No | ✅ Yes |
| Context loading | ✅ Yes | ❌ No |
| Agent detection | ✅ Self-discovering | ❌ Assumes env vars |
| Queue sync | ❌ No | ✅ Yes |
| Git commit | ❌ No | ✅ Yes |
| Archive | ❌ No | ✅ Yes |
| Documentation validation | ✅ Yes | ❌ No |

**Neither system is complete on its own.**

---

## What We Actually Need

A unified hook system that combines:

1. **From BB5 Hooks:**
   - Agent type detection
   - Context loading
   - Security rules
   - Documentation validation

2. **From RALF Hooks:**
   - Run folder creation
   - Queue synchronization
   - Git commit on completion
   - Archival

---

## Recommendation

**Don't wire the ralf-*-hook.sh scripts as-is.**

Instead:
1. **Merge the functionality** into the existing BB5 hooks
2. **Add run folder creation** to `session-start-blackbox5.sh`
3. **Add queue sync + git commit** to `stop-hierarchy-update.sh`
4. **Keep** `stop-validate-docs.sh` as-is (it's working)
5. **Delete or archive** the ralf-*-hook.sh files to avoid confusion

The BB5 hooks are more mature (agent-aware, self-discovering, security-focused).
The RALF hooks have the execution flow logic we need.

**Merge them, don't replace them.**
