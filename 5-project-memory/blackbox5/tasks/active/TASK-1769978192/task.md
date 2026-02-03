# Task: Design Agent Execution Flow with Enforcement Mechanisms

**Task ID:** TASK-1769978192
**Type:** design
**Priority:** critical
**Status:** active
**Created:** 2026-02-02T14:16:32Z
**Estimated Lines:** 800

---

## Objective

Design and implement a structured agent execution flow that ensures every agent run creates a complete, traceable audit trail. The system must enforce folder creation, context management, and task lifecycle management through code (hooks) rather than relying on LLM prompt compliance.

---

## Context

The current RALF system has a **0% queue sync success rate** because LLM-based executors cannot reliably follow prompt instructions for critical automation. This is not a bug—it's a fundamental architectural limitation. The solution is to move enforcement from prompts (suggestions) to hooks (code-guaranteed).

This task captures the complete agent execution flow specification as defined by the user, including open questions about enforcement mechanisms, timeline management, and agent role differentiation.

---

## The 7-Phase Agent Execution Flow

---

### Phase 1: System Prompt and Runtime Initialization

**User Requirement:**
The first thing any agent should do, after receiving its system prompt, is go into its runtime folder and create a specific run folder. This should essentially be a script templated with context, thoughts, and all that necessary information.

**Current Implementation:**
The run folder is created by `ralf-loop.sh` (lines 156-158) BEFORE Claude starts:
```bash
RUN_DIR="$PROJECT_AUTONOMOUS/runs/run-$TIMESTAMP"
mkdir -p "$RUN_DIR"
```

This means:
- ✅ Run folder creation is already automated
- ✅ Happens before agent starts (no LLM involvement)
- ⚠️ But it's created by the loop script, not by the agent itself
- ⚠️ No hook enforcement - if someone runs Claude directly without the loop, no run folder is created

**Phase 1 Decision Required:**

| Option | How It Works | Pros | Cons |
|--------|--------------|------|------|
| **A. Keep loop script** | `ralf-loop.sh` creates folder before starting Claude | Already working; no changes needed | If Claude run directly, no folder created |
| **B. Add SessionStart hook** | Hook creates folder when Claude starts | Guaranteed even if run directly; enforces structure | Need to pass agent type/plan info to hook |
| **C. Both** | Loop creates preliminary folder; hook validates/enhances | Double protection; most robust | More complex |

**My Recommendation: Option C (Both)**
- Loop script creates basic run folder (current behavior)
- SessionStart hook validates it exists and creates required template files
- This ensures the folder exists regardless of how Claude is invoked

**First Principles Analysis (146 runs analyzed):**

| File | Usage Rate | Decision |
|------|------------|----------|
| THOUGHTS.md | 100% (167/167) | **Keep separate** - Critical |
| RESULTS.md | 99% (165/167) | **Keep separate** - Critical |
| DECISIONS.md | 97% (163/167) | **Keep separate** - Critical |
| metadata.yaml | 76% (112/147) | **Keep** - State tracking |
| LEARNINGS.md | 13% (21/167) | **Merge into metadata** |
| ASSUMPTIONS.md | 12% (20/167) | **Merge into metadata** |

**Decision: Simplified 4-File Structure**
```
run-XXXX/
├── THOUGHTS.md      # Narrative reasoning (process)
├── RESULTS.md       # Outcomes (what happened)
├── DECISIONS.md     # Key choices (why)
└── metadata.yaml    # State + learnings + assumptions
```

**Phase 1 Implementation: Hook-Based Enforcement**

**Why hooks?** The 182-run analysis proved LLMs cannot reliably follow prompt instructions (0% queue sync success). Hooks are CODE, not prompts - they execute deterministically.

**Hook Type: COMMAND (not prompt)**
- Runs bash script directly
- Zero LLM tokens
- <100ms execution time
- 100% reliable

**Phase 1 Deliverables:**
- [x] Decision: Simplified 4-file structure based on usage data
- [ ] `.claude/settings.json` - Hook configuration
- [ ] `bin/ralf-session-start-hook.sh` - Creates run folder and templates
- [ ] Templates: `THOUGHTS.md`, `RESULTS.md`, `DECISIONS.md`, `metadata.yaml`

---

### Phase 2: Reading the Prompt

**User Requirement:**
The agent should read its prompt, which will contain all information regarding the project memory, where everything is located in the blackbox, and how to use it for the specific project it's working on.

**Current Implementation:**
- Prompts exist at `2-engine/.autonomous/prompts/ralf.md` and `ralf-executor.md`
- System prompts in `2-engine/.autonomous/prompts/system/`
- Project memory structure documented in `5-project-memory/blackbox5/MAP.yaml`

**Phase 2 Deliverables:**
- [ ] Update `ralf-executor.md` to reference the 7-phase flow
- [ ] Add instructions for task folder creation (Phase 4)
- [ ] Add context file locations (Phase 5)

---

### Phase 3: Task Selection

**User Requirement:**
If it's an executor agent, it should look at the main task list. There will be different types of tasks (architecture, feature, etc.), but the agent will pick the next item set to high priority—likely something a planning agent has already placed there as the most important thing to do next.

**Current Implementation:**
- Task system exists at `.autonomous/tasks/active/` and `.autonomous/tasks/completed/`
- `TEMPLATE.md` with lines-per-minute estimation
- Dual-RALF queue in `.autonomous/communications/queue.yaml`
- Skill defined: `2-engine/.autonomous/skills/task-selection/`

**Phase 3 Deliverables:**
- [ ] `bin/ralf-task-select.py` - Programmatic task selection
- [ ] Priority ordering mechanism
- [ ] Task claiming to prevent duplicate execution

---

### Phase 4: Task Folder Creation

**User Requirement:**
Once a task is picked, the agent will create a templated task folder in the task area. The point of this folder is to have a README with a date and timestamp that includes:
- (a) The goal
- (b) The reasoning for the goal
- (c) A task plan document (similar to SISO internal context)

**Location:** `.autonomous/tasks/working/TASK-XXXX/run-YYYY/`

**Phase 4 Deliverables:**
- [ ] Define task folder structure
- [ ] Create `README.md` template (goal, reasoning, plan)
- [ ] Create `TASK-CONTEXT.md` template (from planner)
- [ ] Create `ACTIVE-CONTEXT.md` template (for executor)

---

### Phase 5: Context and Execution

**User Requirement:**
Inside that task folder, there should be two types of context in an MD file:
- **(a) Task Context:** Filled out by the planning agent. Includes links to all relevant file routes and information needed to execute the plan.
- **(b) Active Context:** Filled out by the execution agent to record anything learned while performing the task.

**Phase 5 Deliverables:**
- [ ] Standardize Task Context format
- [ ] Standardize Active Context format
- [ ] Link planner context to executor context

---

### Phase 6: Logging and Completion

**User Requirement:**
The folder should also contain:
- (a) A step-by-step plan
- (b) A timeline or thought log showing all steps taken
- (c) A task change log detailing exactly what was modified

**Open Question:** Timeline vs thought log - are these merged or separate?
- **Timeline:** Chronological events (what happened when)
- **Thought Log:** Reasoning steps (why choices were made)

**Phase 6 Deliverables:**
- [ ] `PLAN.md` template
- [ ] `TIMELINE.md` or merge strategy
- [ ] `CHANGELOG.md` template

---

### Phase 7: Task Completion

**User Requirement:**
Once the task is finished, the agent ticks it off, marks it as done, and moves it to the backlog. The task folder remains there for future reference.

**Phase 7 Deliverables:**
- [ ] `bin/ralf-task-complete.sh` - Validation and move workflow
- [ ] `bin/ralf-stop-hook.sh` - Enforce completion steps
- [ ] Update task status in STATE.yaml

---

### Phase 2: Reading the Prompt
The agent should read its prompt, which will contain all information regarding the project memory, where everything is located in the blackbox, and how to use it for the specific project it's working on.

**Existing Infrastructure:**
- Prompts exist at `2-engine/.autonomous/prompts/ralf.md` and `ralf-executor.md`
- System prompts in `2-engine/.autonomous/prompts/system/`
- Project memory structure documented in `5-project-memory/blackbox5/MAP.yaml`

### Phase 3: Task Selection
If it's an executor agent, it should look at the main task list. There will be different types of tasks (architecture, feature, etc.), but the agent will pick the next item set to high priority—likely something a planning agent has already placed there as the most important thing to do next.

**Existing Infrastructure:**
- Task system exists at `.autonomous/tasks/active/` and `.autonomous/tasks/completed/`
- `TEMPLATE.md` with lines-per-minute estimation
- Dual-RALF queue system in `.autonomous/communications/queue.yaml`
- Skill defined: `2-engine/.autonomous/skills/task-selection/`

### Phase 4: Task Folder Creation
Once a task is picked, the agent will create a templated task folder in the task area. The point of this folder is to have a README with a date and timestamp that includes:
- (a) The goal
- (b) The reasoning for the goal
- (c) A task plan document (similar to SISO internal context)

**Location Decision Needed:** Should this be in `/tasks/` (flat) or `/tasks/active/` and `/tasks/completed/`?

### Phase 5: Context and Execution
Inside that task folder (created specifically for the execution agent doing the work), there should be two types of context in an MD file:
- **(a) Task Context:** Filled out by the planning agent. Includes links to all relevant file routes and information needed to execute the plan.
- **(b) Active Context:** Filled out by the execution agent. Records anything learned while performing the task, for future review.

### Phase 6: Logging and Completion
The folder should also contain:
- (a) A step-by-step plan
- (b) A timeline or thought log (need to figure out how to merge these) showing all steps taken
- (c) A task change log detailing exactly what was modified

**Open Question:** Timeline vs thought log - are these merged or separate?

### Phase 7: Task Completion
Once the task is finished, the agent ticks it off, marks it as done, and moves it to the backlog. The task folder remains there for future reference.

---

## Open Questions to Resolve

### 1. Agent Enforcement

**(a) How do we force the agent to do this?**
Options:
- **Prompt-based:** Include strict instructions in the system prompt (current approach - 0% success rate)
- **Hook-based:** Use Claude Code hooks (`SessionStart`, `Stop`) to enforce folder creation and task management in code
- **Wrapper script:** Wrap Claude Code execution in a bash script that handles all setup/teardown

**(b) Would we just give it a prompt, or is there a better way to force it?**
The 182-run analysis proves prompts don't work for critical automation. LLMs treat instructions as suggestions.

**(c) Best approach?**
**Recommendation:** Hook-based enforcement for critical path items:
- `SessionStart` hook: Create run folder, validate environment
- `Stop` hook: Enqueue task completion, sync queue, commit changes
- `PostToolUse` hook: Detect task file modifications, flag for sync

### 2. Task and Timeline Management

**(a) Where should this be in the task folder?**
Research needed on:
- Current `runs/` structure (each run has its own timeline)
- Existing `timeline.yaml` at project root
- How SISO internal handles task timelines

**(b) Timeline vs PortLog**
User's intuition: Timeline ≠ PortLog
- **Timeline:** Chronological events (what happened when)
- **PortLog:** Decision rationale (why choices were made)

**(c) Timeline Types**
Proposed hierarchy:
- **Project timeline:** Major milestones, releases, architectural decisions
- **Run timeline:** Individual agent execution steps
- **Task timeline:** (Maybe not needed - task folder itself is the record)

### 3. Agent Roles

**(a) How does the agent know if it's a planner or executor?**
**Answer:** Different MD prompt fed at start. System prompt is different.

**Existing Infrastructure:**
- `2-engine/.autonomous/prompts/system/planner-identity.md`
- `2-engine/.autonomous/prompts/system/executor-identity.md`
- `ralf-planner` and `ralf-executor` shell scripts pass different prompts

**(b) Task Selection Logic**
- **Planner:** Analyzes codebase, determines highest ROI task, places in queue
- **Executor:** Picks highest priority task from queue (already prioritized by planner)
- **Exception:** Executor may choose strategically correct lower-priority task if blocked

---

## Success Criteria

- [ ] Document the complete agent execution flow with folder structure
- [ ] Decide on enforcement mechanism (hooks vs prompts vs wrapper)
- [ ] Define task folder location and structure
- [ ] Clarify timeline vs thought log relationship
- [ ] Create hook implementation plan for critical path enforcement
- [ ] Update existing prompts to reference new flow
- [ ] Test enforcement mechanism with actual agent run

---

## Files to Create/Modify

**New Files:**
- `.claude/settings.json` - Hook configuration for enforcement
- `bin/ralf-session-start-hook.sh` - Session initialization enforcement
- `bin/ralf-stop-hook.sh` - Task completion and sync enforcement
- `bin/ralf-post-tool-hook.sh` - File modification detection
- `.autonomous/tasks/active/TASK-XXXX/` - New task folder template

**Files to Modify:**
- `2-engine/.autonomous/prompts/ralf-executor.md` - Reference new flow
- `2-engine/.autonomous/shell/ralf-loop.sh` - Integrate hooks
- `2-engine/.autonomous/workflows/task-execution.yaml` - Update workflow

---

## Dependencies

- [ ] Research: Review existing timeline implementation in `timeline.yaml`
- [ ] Research: Check SISO internal task folder structure for patterns
- [ ] Decision: Choose enforcement mechanism (hooks recommended)

---

## Notes

**Critical Insight from 182-Run Analysis:**
The queue automation has a 100% failure rate (0/5 features synced) not because of a bug, but because of a fundamental architectural limitation: LLM-based executors cannot reliably follow prompt instructions for critical automation.

**The Fix:**
```
Current: Planner LLM → Executor LLM → (forgets sync) → Complete
Required: Planner LLM → Executor Script → Calls LLM → Enforces Sync → Complete
```

**Hook Events Available:**
- `SessionStart` - Initialize run folder
- `UserPromptSubmit` - Validate task selection
- `PreToolUse` - Audit operations
- `PostToolUse` - Detect task file changes
- `Stop` - Enforce queue sync, commit, push

**Token Context Warning:**
This task was created to preserve context from a long conversation about agent execution flow. The user explicitly requested documentation to prevent losing this information.

---

## Related Documentation

- `docs/HETZNER-SETUP.md` - Server connection guide
- `docs/SERVER-RUNS-COMPREHENSIVE-ANALYSIS.md` - 182-run analysis findings
- `5-project-memory/blackbox5/DUAL-RALF-ARCHITECTURE.md` - Architecture spec
- `5-project-memory/blackbox5/.autonomous/communications/protocol.yaml` - Communication protocol
