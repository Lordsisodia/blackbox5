# PLAN.md: Design Agent Execution Flow

**Task ID:** TASK-1769978192
**Type:** design | implement
**Priority:** CRITICAL
**Status:** Planning
**Created:** 2026-02-02
**Estimated Effort:** 8 hours

---

## 1. First Principles Analysis

### Why is a Structured Agent Execution Flow Critical?

1. **Enforcement Over Suggestion**: LLMs cannot reliably follow prompt instructions (0% queue sync success rate proven)
2. **Audit Trail**: Every action must be traceable for debugging and compliance
3. **Consistency**: All agents follow the same pattern, reducing confusion
4. **Automation**: Hooks enforce behavior without LLM involvement
5. **Reliability**: Code-based enforcement is deterministic

### What Happens Without Structured Flow?

| Problem | Impact | Evidence |
|---------|--------|----------|
| No run folder created | Lost work, no audit trail | 182-run analysis |
| Missing documentation | Inconsistent output | 0% queue sync |
| No task lifecycle | Duplicate work, no visibility | Critical Blocker #2 |
| Manual status updates | Forgotten updates | 0% automation |
| No context preservation | Repeated mistakes | Task restart issues |

### How Does Hook-Based Enforcement Help?

By moving enforcement from prompts (suggestions) to hooks (code), we achieve:
- **100% reliability** - Hooks execute deterministically
- **Zero LLM tokens** - No context window usage for enforcement
- **<100ms execution** - Fast, invisible to user
- **Consistent behavior** - Same every time

---

## 2. Current State Assessment

### Existing Infrastructure

| Component | Location | Status |
|-----------|----------|--------|
| Run folder creation | `ralf-loop.sh` (lines 156-158) | Working but not enforced |
| Prompts | `2-engine/.autonomous/prompts/` | Partial coverage |
| Task system | `.autonomous/tasks/active/` | Basic structure |
| Queue system | `.autonomous/communications/queue.yaml` | Has status field |
| Events log | `.autonomous/communications/events.yaml` | Logs events |
| Agent identity | `prompts/system/planner-identity.md` | Differentiates agents |

### Gaps in Current Implementation

1. **No hook enforcement** - If Claude run directly, no folder created
2. **No SessionStart hook** - Missing initialization enforcement
3. **No Stop hook** - Missing completion enforcement
4. **No in_progress status** - Only pending/completed exist
5. **No task context linking** - Planner and executor don't share context
6. **No automated task claiming** - Manual selection error-prone

---

## 3. Proposed Solution

### The 7-Phase Agent Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: System Prompt & Runtime Initialization                 │
│ - Hook: SessionStart                                            │
│ - Creates run folder, templates, context                        │
├─────────────────────────────────────────────────────────────────┤
│ Phase 2: Reading the Prompt                                     │
│ - Agent reads system prompt with project memory info            │
│ - Understands location of blackbox structure                    │
├─────────────────────────────────────────────────────────────────┤
│ Phase 3: Task Selection                                         │
│ - Executor looks at main task list                              │
│ - Picks highest priority task (set by planner)                  │
│ - Calls ralf-task-select.sh to claim task                       │
├─────────────────────────────────────────────────────────────────┤
│ Phase 4: Task Folder Creation                                   │
│ - Creates templated task folder                                 │
│ - README.md with goal, reasoning, plan                          │
│ - Location: .autonomous/tasks/working/TASK-XXXX/                │
├─────────────────────────────────────────────────────────────────┤
│ Phase 5: Context and Execution                                  │
│ - Task Context: Filled by planner (links to files)              │
│ - Active Context: Filled by executor (learnings)                │
│ - Step-by-step execution                                        │
├─────────────────────────────────────────────────────────────────┤
│ Phase 6: Logging and Completion                                 │
│ - Step-by-step plan documented                                  │
│ - Timeline/thought log showing steps                            │
│ - Task change log detailing modifications                       │
├─────────────────────────────────────────────────────────────────┤
│ Phase 7: Task Completion                                        │
│ - Hook: Stop                                                    │
│ - Marks task done, moves to backlog                             │
│ - Task folder preserved for reference                           │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 1: System Prompt & Runtime Initialization

**Decision: Option C (Both loop script AND SessionStart hook)**

| Option | How It Works | Pros | Cons |
|--------|--------------|------|------|
| A. Keep loop script | `ralf-loop.sh` creates folder before Claude | Already working | No folder if run directly |
| B. Add SessionStart hook | Hook creates folder when Claude starts | Guaranteed even if run directly | Need to pass agent info |
| **C. Both** | Loop creates preliminary; hook validates/enhances | Double protection; most robust | More complex |

**File Structure (Simplified 4-File Based on Usage Data)**

| File | Usage Rate | Decision |
|------|------------|----------|
| THOUGHTS.md | 100% (167/167) | **Keep separate** - Critical |
| RESULTS.md | 99% (165/167) | **Keep separate** - Critical |
| DECISIONS.md | 97% (163/167) | **Keep separate** - Critical |
| metadata.yaml | 76% (112/147) | **Keep** - State tracking |
| LEARNINGS.md | 13% (21/167) | **Merge into metadata** |
| ASSUMPTIONS.md | 12% (20/167) | **Merge into metadata** |

```
run-XXXX/
├── THOUGHTS.md      # Narrative reasoning (process)
├── RESULTS.md       # Outcomes (what happened)
├── DECISIONS.md     # Key choices (why)
└── metadata.yaml    # State + learnings + assumptions
```

### Enforcement Mechanism Decision

**Recommendation: Hook-based enforcement for critical path items**

| Mechanism | Reliability | Speed | Token Cost |
|-----------|-------------|-------|------------|
| Prompt-based | 0% (proven) | N/A | High |
| **Hook-based** | **100%** | **<100ms** | **Zero** |
| Wrapper script | 100% | <100ms | Zero |

**Hook Events to Use:**
- `SessionStart` - Initialize run folder, validate environment
- `UserPromptSubmit` - Validate task selection
- `PreToolUse` - Audit operations
- `PostToolUse` - Detect task file changes
- `Stop` - Enforce queue sync, commit, push

---

## 4. Implementation Plan

### Phase 1: Create Hook Infrastructure (90 min)

**1.1 Create `.claude/settings.json`**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "$HOME/.blackbox5/bin/ralf-session-start-hook.sh",
        "type": "command"
      }
    ],
    "Stop": [
      {
        "command": "$HOME/.blackbox5/bin/ralf-stop-hook.sh",
        "type": "command"
      }
    ],
    "PostToolUse": [
      {
        "command": "$HOME/.blackbox5/bin/ralf-post-tool-hook.sh",
        "type": "command"
      }
    ]
  }
}
```

**1.2 Create `bin/ralf-session-start-hook.sh`**
- Validate run folder exists (create if missing)
- Create template files (THOUGHTS.md, RESULTS.md, DECISIONS.md, metadata.yaml)
- Load agent context
- Export environment variables
- Return JSON to Claude Code

**1.3 Create `bin/ralf-stop-hook.sh`**
- Check for uncommitted changes
- Enqueue task completion
- Sync queue.yaml
- Move task to completed/ if finished
- Commit and push if configured

**1.4 Create `bin/ralf-post-tool-hook.sh`**
- Detect task file modifications
- Flag for sync if needed
- Log tool usage for audit

### Phase 2: Create Task Selection System (60 min)

**2.1 Create `bin/ralf-task-select.py`**
- Read queue.yaml
- Filter by priority (CRITICAL > HIGH > MEDIUM > LOW)
- Filter by status (pending only)
- Claim task (set status to claimed)
- Create working directory
- Return task ID and context

**2.2 Create task claiming mechanism**
- Update queue.yaml with claimed status
- Set claimed_at and claimed_by timestamps
- Create event in events.yaml
- Create .autonomous/tasks/working/TASK-XXXX/ directory

### Phase 3: Create Task Folder Templates (45 min)

**3.1 Create task folder structure**
```
.autonomous/tasks/working/TASK-XXXX/
├── README.md              # Goal, reasoning, plan
├── TASK-CONTEXT.md        # Planner-filled context
├── ACTIVE-CONTEXT.md      # Executor-filled learnings
├── PLAN.md                # Step-by-step plan
├── TIMELINE.md            # Execution timeline
└── CHANGELOG.md           # What was modified
```

**3.2 Create template files**
- README.md template with goal, reasoning, plan sections
- TASK-CONTEXT.md template with file links
- ACTIVE-CONTEXT.md template for learnings
- PLAN.md template for step-by-step execution
- TIMELINE.md template for chronological events
- CHANGELOG.md template for modifications

### Phase 4: Update Prompts (45 min)

**4.1 Update `2-engine/.autonomous/prompts/ralf-executor.md`**
- Reference the 7-phase flow
- Add instructions for task folder creation
- Add context file locations
- Add task completion requirements

**4.2 Update `2-engine/.autonomous/prompts/ralf-planner.md`**
- Reference task context format
- Add instructions for TASK-CONTEXT.md
- Add priority setting guidelines

### Phase 5: Create Task Lifecycle Scripts (60 min)

**5.1 Create `bin/ralf-task-start.sh`**
- Called by executor when beginning work
- Sets status to in_progress
- Updates heartbeat with task reference
- Creates initial timeline entry

**5.2 Create `bin/ralf-task-complete.sh`**
- Validation and move workflow
- Updates task status in queue.yaml
- Moves task from active/ to completed/
- Updates STATE.yaml with completion
- Archives task folder

### Phase 6: Testing (60 min)

**6.1 Hook Enforcement Test**
- Start session without run folder
- Verify SessionStart hook creates it
- Stop session with uncommitted changes
- Verify Stop hook handles correctly

**6.2 Task Selection Test**
- Run ralf-task-select.py
- Verify claims highest priority task
- Verify creates working directory
- Verify updates queue.yaml

**6.3 Task Lifecycle Test**
- Claim task → verify claimed status
- Start task → verify in_progress status
- Complete task → verify completed status
- Verify move to completed/

**6.4 Integration Test**
- Full flow: SessionStart → Task Select → Execute → Stop
- Verify all files created
- Verify all statuses updated
- Verify timeline complete

---

## 5. Success Criteria

| Criterion | Verification Method |
|-----------|---------------------|
| Document complete agent execution flow | Review 7-phase documentation |
| Enforcement mechanism decided | Hook-based selected |
| Task folder location defined | `.autonomous/tasks/working/` |
| Timeline vs thought log clarified | Timeline = events, Thought = reasoning |
| Hook implementation plan created | 3 hooks defined |
| SessionStart hook implemented | `ralf-session-start-hook.sh` exists |
| Stop hook implemented | `ralf-stop-hook.sh` exists |
| Task selection script created | `ralf-task-select.py` exists |
| Task folder templates created | 6 template files exist |
| Existing prompts updated | `ralf-executor.md` updated |
| Enforcement tested | Run full agent flow |

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Hook Infrastructure | 90 min | 90 min |
| Phase 2: Task Selection System | 60 min | 150 min |
| Phase 3: Task Folder Templates | 45 min | 195 min |
| Phase 4: Update Prompts | 45 min | 240 min |
| Phase 5: Task Lifecycle Scripts | 60 min | 300 min |
| Phase 6: Testing | 60 min | 360 min |
| **Total** | **6 hours** | |

---

## 7. Critical Insight

The 182-run analysis proved that **LLM-based executors cannot reliably follow prompt instructions for critical automation**. This is not a bug—it's a fundamental architectural limitation.

**The Fix:**
```
Current: Planner LLM → Executor LLM → (forgets sync) → Complete
Required: Planner LLM → Executor Script → Calls LLM → Enforces Sync → Complete
```

By moving enforcement to hooks (code), we achieve deterministic behavior regardless of LLM compliance.

---

## 8. Files to Create/Modify

**New Files:**
- `.claude/settings.json` - Hook configuration
- `bin/ralf-session-start-hook.sh` - Session initialization
- `bin/ralf-stop-hook.sh` - Task completion enforcement
- `bin/ralf-post-tool-hook.sh` - File modification detection
- `bin/ralf-task-select.py` - Programmatic task selection
- `bin/ralf-task-start.sh` - Task start handler
- `bin/ralf-task-complete.sh` - Task completion handler
- `.autonomous/tasks/working/TASK-XXXX/` - Task folder template

**Files to Modify:**
- `2-engine/.autonomous/prompts/ralf-executor.md` - Reference new flow
- `2-engine/.autonomous/prompts/ralf-planner.md` - Reference task context
- `2-engine/.autonomous/shell/ralf-loop.sh` - Integrate hooks

---

## 9. Dependencies

- **TASK-010-001** (SessionStart Enhanced Hook) - Provides hook foundation
- **TASK-STATUS-LIFECYCLE-ACTION-PLAN** - Task status automation

---

*Hook-based enforcement transforms RALF from a suggestion-based system to a deterministic automation platform.*
