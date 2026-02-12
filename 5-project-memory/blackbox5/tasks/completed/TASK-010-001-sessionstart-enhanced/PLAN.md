# PLAN.md: SessionStart Enhanced Hook Implementation

**Task ID:** TASK-010-001-sessionstart-enhanced
**Goal:** IG-010 - Implement World-Class Hook System for BB5
**Plan:** PLAN-010 - BB5 Hook System Implementation
**Status:** Planning
**Priority:** CRITICAL
**Estimated Effort:** 4 hours

---

## 1. First Principles Analysis

### Why is an Enhanced SessionStart Hook Critical?

1. **Foundation of Automation**: Every agent session starts here. If this hook fails, the entire automation pipeline fails.
2. **Context Consistency**: Without standardized initialization, agents work with incomplete or inconsistent context.
3. **Traceability**: Run folders create an audit trail for every agent action.
4. **Memory Integration**: Connecting to vector store memories enables learning from past work.

### What Happens Without This Hook?

| Problem | Impact | Frequency |
|---------|--------|-----------|
| No run folder created | Lost work, no audit trail | Every session |
| Missing documentation files | Inconsistent agent output | Every session |
| No agent type detection | Wrong context loaded | Context-dependent |
| No memory loading | Repeated mistakes | Every similar task |
| No environment setup | Other hooks fail | Cascade failure |

### How Does This Hook Solve the Problem?

The hook combines the best practices from BB5's context loading and ralph-loop's run folder creation into a single, self-discovering initialization system that requires zero environment variables and works for all agent types.

---

## 2. Current State Assessment

### Existing Infrastructure

| Component | Location | Status | Notes |
|-----------|----------|--------|-------|
| SessionStart hook | `.claude/hooks/session-start-blackbox5.sh` | Partial | Basic context loading |
| Run folder creation | `ralf-loop.sh` (lines 156-158) | Working | Created before Claude starts |
| Agent detection | `bb5-discover-context` | Partial | Limited agent types |
| Memory loading | `session_memory_loader.py` | Planned | Not yet implemented |
| Environment export | None | Missing | No standard variables |

### Gaps in Current Implementation

1. **No self-discovery** - Requires environment variables
2. **Limited agent types** - Only detects basic types
3. **No memory integration** - Vector store not queried
4. **No standardized templates** - Files created ad-hoc
5. **No JSON output** - Claude Code doesn't receive context

---

## 3. Proposed Solution

### Hook Architecture

```
SessionStart Triggered
        ↓
Step 1: Self-Discovery
  - Find project root from script location
  - Discover project name
        ↓
Step 2: Agent Type Detection
  - Check path patterns (/planner/, /executor/, /architect/)
  - Check file patterns (queue.yaml, .task-claimed)
  - Check git branch names
        ↓
Step 3: Run Folder Creation
  - Create runs/{agent_type}/run-{timestamp}/
        ↓
Step 4: Required File Creation
  - THOUGHTS.md (reasoning template)
  - RESULTS.md (outcomes template)
  - DECISIONS.md (choices template)
  - metadata.yaml (structured state)
        ↓
Step 5: Memory Loading
  - Query vector store for relevant memories
  - Load past learnings and decisions
        ↓
Step 6: Context Injection
  - Create AGENT_CONTEXT.md
  - Load task details and queue status
        ↓
Step 7: Environment Export
  - Export RALF_RUN_DIR, RALF_RUN_ID, RALF_AGENT_TYPE
        ↓
Return JSON to Claude Code
```

### Files to Create

1. **`.claude/hooks/session-start-enhanced.sh`** - Main hook script
2. **`.claude/hooks/lib/run-initializer.sh`** - Shared library for run creation
3. **`.claude/hooks/lib/agent-detector.sh`** - Agent type detection library

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Self-discovering | No environment variables needed, robust and portable |
| Multiple detection methods | Fallbacks ensure agent type is detected |
| 4-file structure | Based on 182-run analysis (THOUGHTS.md: 100%, RESULTS.md: 99%, DECISIONS.md: 97%) |
| JSON output | Injects context directly into Claude's system prompt |
| Library separation | Reusable components for other hooks |

---

## 4. Implementation Plan

### Phase 1: Create Library Files (60 min)

**1.1 Create `lib/agent-detector.sh`**
- Implement `detect_agent_type()` function
- Support path-based detection
- Support file-based detection
- Support git branch detection
- Return "unknown" if no match

**1.2 Create `lib/run-initializer.sh`**
- Implement `create_run_folder()` function
- Implement `create_template_files()` function
- Define templates for THOUGHTS.md, RESULTS.md, DECISIONS.md, metadata.yaml
- Support custom template variables

### Phase 2: Create Main Hook Script (90 min)

**2.1 Self-Discovery Implementation**
- Determine SCRIPT_DIR from BASH_SOURCE
- Calculate PROJECT_ROOT
- Discover PROJECT_MEMORY_DIR and PROJECT_NAME

**2.2 Agent Detection Integration**
- Source agent-detector.sh
- Call detect_agent_type()
- Set AGENT_TYPE variable

**2.3 Run Folder Creation**
- Generate RUN_TIMESTAMP and RUN_ID
- Create RUNS_DIR and RUN_DIR
- Call library functions to create templates

**2.4 Memory Loading**
- Check for .current-task file
- Call session_memory_loader.py if exists
- Generate RELEVANT_MEMORIES.md

**2.5 Context Injection**
- Create AGENT_CONTEXT.md
- Include task details if claimed
- Include queue status
- Include available commands

**2.6 Environment Export**
- Export RALF_RUN_DIR, RALF_RUN_ID, RALF_PROJECT_ROOT
- Export RALF_PROJECT_NAME, RALF_AGENT_TYPE
- Append to CLAUDE_ENV_FILE if set

**2.7 JSON Output**
- Generate JSON with hookSpecificOutput
- Include agentType, runId, runDir, contextFile
- Echo JSON for Claude Code

### Phase 3: Testing (60 min)

**3.1 Basic Execution Test**
- Start new session
- Verify run folder created
- Verify all files exist
- Verify AGENT_CONTEXT.md populated

**3.2 Agent Type Detection Test**
- Test from planner directory → verify "planner"
- Test from executor directory → verify "executor"
- Test from architect directory → verify "architect"
- Test from unknown directory → verify "unknown"

**3.3 Context Injection Test**
- Start session with claimed task
- Verify task details in AGENT_CONTEXT.md
- Verify acceptance criteria loaded

**3.4 Memory Loading Test**
- Start session on similar task to previous
- Verify RELEVANT_MEMORIES.md created
- Verify past learnings loaded

### Phase 4: Integration (30 min)

**4.1 Update `.claude/settings.json`**
- Add SessionStart hook configuration
- Point to session-start-enhanced.sh

**4.2 Documentation**
- Update hook developer documentation
- Document environment variables exported
- Document JSON output format

---

## 5. Success Criteria

| Criterion | Verification Method |
|-----------|---------------------|
| Run folder created automatically | Check runs/{agent_type}/ directory |
| All required files populated | Verify THOUGHTS.md, RESULTS.md, DECISIONS.md, metadata.yaml exist |
| Agent type detected correctly | Check AGENT_CONTEXT.md for correct type |
| Context loaded from vector store | Verify RELEVANT_MEMORIES.md created |
| Environment variables exported | Check `env | grep RALF_` |
| AGENT_CONTEXT.md created | Verify file with task details |
| JSON output returned | Check Claude Code receives context |
| Works for all agent types | Test planner, executor, architect |
| Self-discovering | Run without env vars, verify works |
| Fails gracefully | Test error conditions |

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Library Files | 60 min | 60 min |
| Phase 2: Main Hook Script | 90 min | 150 min |
| Phase 3: Testing | 60 min | 210 min |
| Phase 4: Integration | 30 min | 240 min |
| **Total** | **4 hours** | |

---

## 7. Integration Points

### Calls Made By This Hook
- `bb5-discover-context` - Get current context
- `bb5-whereami` - Show location
- `session_memory_loader.py` - Load relevant memories

### Called By
- `.claude/settings.json` - SessionStart event

### Provides Context To
- All other hooks via environment variables
- Agent via AGENT_CONTEXT.md
- Claude Code via JSON output

---

## 8. Open Questions

1. Should we support additional agent types beyond planner/executor/architect?
2. Should the hook detect if resuming a previous run vs starting fresh?
3. How much memory history should we load? Last 5? Last 10? All relevant?
4. Should we include git status in the context?
5. Should we check for uncommitted changes and warn?

---

*This is the foundation hook. Everything else builds on this.*
